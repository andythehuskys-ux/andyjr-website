"""
fund_wallets.py
Distributes SOL from a main "source" wallet to all 5 bundle wallets.
Run this BEFORE launching the token.

Usage:
    python src/social/fund_wallets.py --source <PRIVATE_KEY_BASE58> --sol 0.3 --network mainnet
    python src/social/fund_wallets.py --source <PRIVATE_KEY_BASE58> --sol 0.3 --network devnet

The --sol amount is the TOTAL to distribute across all wallets.
Each wallet gets an equal share (e.g., 0.3 SOL / 5 wallets = 0.06 SOL each).
"""

import argparse
import time
from pathlib import Path
from solana.rpc.api import Client
from solana.rpc.commitment import Confirmed
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from solders.message import Message

# Local import
import sys
sys.path.append(str(Path(__file__).parent))
from wallet_generator import load_wallets, DEVNET_URL

MAINNET_URL = "https://api.mainnet-beta.solana.com"
LAMPORTS_PER_SOL = 1_000_000_000

def get_client(network: str) -> Client:
    url = DEVNET_URL if network == "devnet" else MAINNET_URL
    print(f"[FundWallets] Network: {network.upper()} ({url})")
    return Client(url)

def get_balance(client: Client, pubkey: Pubkey) -> float:
    resp = client.get_balance(pubkey)
    return resp.value / LAMPORTS_PER_SOL

def fund_wallets(source_secret_list: list, total_sol: float, network: str = "devnet"):
    """
    Distributes SOL evenly from source wallet to all bundle wallets.
    """
    client = get_client(network)
    source_kp = Keypair.from_bytes(bytes(source_secret_list))
    wallets = load_wallets()

    if not wallets:
        print("[FundWallets] ❌ No bundle wallets found. Run wallet_generator.py first.")
        return

    per_wallet_sol = total_sol / len(wallets)
    per_wallet_lamports = int(per_wallet_sol * LAMPORTS_PER_SOL)

    source_balance = get_balance(client, source_kp.pubkey())
    print(f"\n[FundWallets] Source wallet: {source_kp.pubkey()}")
    print(f"[FundWallets] Source balance: {source_balance:.4f} SOL")
    print(f"[FundWallets] Distributing {total_sol} SOL across {len(wallets)} wallets")
    print(f"[FundWallets] Each wallet receives: {per_wallet_sol:.4f} SOL\n")

    if source_balance < total_sol + 0.01:  # +0.01 for tx fees
        print(f"[FundWallets] ❌ Insufficient balance. Need {total_sol + 0.01:.3f} SOL, have {source_balance:.4f} SOL")
        return

    for w in wallets:
        dest = Pubkey.from_string(w["pubkey"])
        
        # Build transaction
        ix = transfer(TransferParams(
            from_pubkey=source_kp.pubkey(),
            to_pubkey=dest,
            lamports=per_wallet_lamports
        ))
        
        recent_blockhash = client.get_latest_blockhash().value.blockhash
        msg = Message.new_with_blockhash([ix], source_kp.pubkey(), recent_blockhash)
        tx = Transaction([source_kp], msg, recent_blockhash)
        
        resp = client.send_transaction(tx)
        sig = str(resp.value)
        
        print(f"[FundWallets] ✅ Wallet {w['index']+1} ({w['pubkey'][:8]}...) funded — tx: {sig[:16]}...")
        time.sleep(0.5)  # Avoid rate limiting

    print(f"\n[FundWallets] ✅ All wallets funded. Ready for bundle buy.")
    print(f"[FundWallets] Next step: Run bundle_buy.py at launch time.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fund bundle wallets from source wallet")
    parser.add_argument("--source-file", help="Path to source wallet JSON file (list of ints)", default=None)
    parser.add_argument("--sol", type=float, default=0.3, help="Total SOL to distribute")
    parser.add_argument("--network", choices=["mainnet", "devnet"], default="devnet")
    args = parser.parse_args()

    if args.source_file:
        import json
        with open(args.source_file) as f:
            secret = json.load(f)
        fund_wallets(secret, args.sol, args.network)
    else:
        print("[FundWallets] Usage: python fund_wallets.py --source-file wallet.json --sol 0.3 --network devnet")
        print("[FundWallets] For devnet testing, you need a funded devnet wallet.")
        print("[FundWallets] Get free devnet SOL: https://faucet.solana.com")
