"""
bundle_buy.py
Executes simultaneous buy of a Pump.fun token from all 5 bundle wallets.
All buys happen in parallel using asyncio — making them appear as organic buyers.

Usage (devnet practice):
    python src/social/bundle_buy.py --token <MINT_ADDRESS> --sol 0.06 --network devnet

Usage (real launch):
    python src/social/bundle_buy.py --token <MINT_ADDRESS> --sol 0.06 --network mainnet

The --sol amount is PER WALLET (so 5 wallets × 0.06 SOL = 0.3 SOL total spent).

HOW PUMP.FUN BUYS WORK:
    Pump.fun has a bonding curve. To buy, you send SOL to the token's bonding curve
    program. We use the Pump.fun API to get the current price and build the transaction.
"""

import asyncio
import argparse
import time
import json
import httpx
from pathlib import Path
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction

import sys
sys.path.append(str(Path(__file__).parent))
from wallet_generator import get_keypairs, DEVNET_URL

MAINNET_URL = "https://api.mainnet-beta.solana.com"
PUMPFUN_API = "https://pumpportal.fun/api"
LAMPORTS_PER_SOL = 1_000_000_000


async def buy_from_wallet(
    keypair: Keypair,
    mint_address: str,
    sol_amount: float,
    client: AsyncClient,
    wallet_index: int
) -> bool:
    """
    Executes a single buy transaction from one wallet via Pump.fun API.
    """
    try:
        # 1. Get the buy transaction from Pump.fun's API
        async with httpx.AsyncClient() as http:
            response = await http.post(
                f"{PUMPFUN_API}/trade-local",
                json={
                    "publicKey": str(keypair.pubkey()),
                    "action": "buy",
                    "mint": mint_address,
                    "amount": sol_amount,
                    "denominatedInSol": "true",
                    "slippage": 15,         # 15% slippage tolerance (meme coins are volatile)
                    "priorityFee": 0.0005,  # Small priority fee to get included quickly
                    "pool": "pump"
                }
            )

        if response.status_code != 200:
            print(f"[Bundle] ❌ Wallet {wallet_index+1}: API error {response.status_code}")
            return False

        # 2. Deserialize and sign the transaction
        tx_bytes = response.content
        tx = VersionedTransaction.from_bytes(tx_bytes)
        
        # Sign with our wallet
        tx = VersionedTransaction(tx.message, [keypair])

        # 3. Send to blockchain
        blockhash = (await client.get_latest_blockhash()).value.blockhash
        sig = await client.send_raw_transaction(bytes(tx))
        
        print(f"[Bundle] ✅ Wallet {wallet_index+1} ({str(keypair.pubkey())[:8]}...): {sol_amount} SOL — tx: {str(sig.value)[:16]}...")
        return True

    except Exception as e:
        print(f"[Bundle] ❌ Wallet {wallet_index+1} failed: {e}")
        return False


async def bundle_buy(mint_address: str, sol_per_wallet: float, network: str):
    """
    Fires all wallet buys simultaneously using asyncio.gather.
    This is what makes them look like organic buyers — all in the same moment.
    """
    rpc_url = DEVNET_URL if network == "devnet" else MAINNET_URL
    keypairs = get_keypairs()

    if not keypairs:
        print("[Bundle] ❌ No wallets found. Run wallet_generator.py first.")
        return

    if network == "devnet":
        print("[Bundle] ⚠️  DEVNET MODE — No real SOL spent.")
        print("[Bundle] ⚠️  Pump.fun does not support devnet, so buy txs will fail — this tests wallet/connection only.")
    else:
        total = sol_per_wallet * len(keypairs)
        print(f"[Bundle] 🔴 MAINNET MODE — Spending {total:.3f} SOL total ({sol_per_wallet} SOL × {len(keypairs)} wallets)")

    print(f"[Bundle] Token: {mint_address}")
    print(f"[Bundle] Wallets: {len(keypairs)}")
    print(f"[Bundle] Firing all buys simultaneously...\n")

    async with AsyncClient(rpc_url) as client:
        # Fire all buys at the exact same time
        results = await asyncio.gather(*[
            buy_from_wallet(kp, mint_address, sol_per_wallet, client, i)
            for i, kp in enumerate(keypairs)
        ])

    success = sum(results)
    print(f"\n[Bundle] Complete: {success}/{len(keypairs)} buys successful.")
    if success == len(keypairs):
        print("[Bundle] 🚀 Perfect bundle buy executed!")
    else:
        print("[Bundle] ⚠️  Some wallets failed. Check logs above.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute multi-wallet bundle buy on Pump.fun")
    parser.add_argument("--token", required=True, help="Token mint address (from Pump.fun)")
    parser.add_argument("--sol", type=float, default=0.06, help="SOL to spend per wallet (default: 0.06)")
    parser.add_argument("--network", choices=["mainnet", "devnet"], default="devnet")
    args = parser.parse_args()

    asyncio.run(bundle_buy(args.token, args.sol, args.network))
