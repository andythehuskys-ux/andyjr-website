"""
sell_and_return.py
Sells all tokens held by the 5 bundle wallets and sends the total recovered SOL
back to a specified destination wallet (your Phantom wallet).

Usage:
    python src/social/sell_and_return.py --token <MINT_ADDRESS> --destination <YOUR_PHANTOM_ADDRESS>
"""

import asyncio
import argparse
import httpx
from pathlib import Path
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from solders.message import Message

import sys
sys.path.append(str(Path(__file__).parent))
from wallet_generator import get_keypairs

MAINNET_URL = "https://api.mainnet-beta.solana.com"
PUMPFUN_API = "https://pumpportal.fun/api"
LAMPORTS_PER_SOL = 1_000_000_000


async def sell_from_wallet(
    keypair: Keypair,
    mint_address: str,
    client: AsyncClient,
    wallet_index: int
):
    """
    Sells 100% of the token balance for a given wallet using Pump.fun API.
    """
    try:
        async with httpx.AsyncClient() as http:
            # 1. Sell 100% of token holdings
            response = await http.post(
                f"{PUMPFUN_API}/trade-local",
                json={
                    "publicKey": str(keypair.pubkey()),
                    "action": "sell",
                    "mint": mint_address,
                    "denominatedInSol": "false",
                    "amount": "100%",  # Sell entire token balance
                    "slippage": 15,
                    "priorityFee": 0.0005,
                    "pool": "pump"
                }
            )

        if response.status_code != 200:
            print(f"[Sell] ERR: Wallet {wallet_index+1}: API error {response.status_code} (Might have no tokens)")
            return False

        # 2. Deserialize and sign
        tx_bytes = response.content
        tx = VersionedTransaction.from_bytes(tx_bytes)
        tx = VersionedTransaction(tx.message, [keypair])

        # 3. Send
        sig = await client.send_raw_transaction(bytes(tx))
        print(f"[Sell] OK: Wallet {wallet_index+1} sold tokens — tx: {str(sig.value)[:16]}...")
        
        # Wait for sell to confirm before transferring SOL out
        await asyncio.sleep(6)
        return True

    except Exception as e:
        print(f"[Sell] ERR: Wallet {wallet_index+1} sell failed: {e}")
        return False


async def transfer_all_sol(
    keypair: Keypair,
    destination_str: str,
    client: AsyncClient,
    wallet_index: int
):
    """
    Transfers all SOL (minus small fee) from the wallet to the destination.
    """
    try:
        dest_pubkey = Pubkey.from_string(destination_str)
        balance_resp = await client.get_balance(keypair.pubkey())
        balance = balance_resp.value
        
        fee_reserve = 5000  # Leave 0.000005 SOL for the transaction fee itself
        transfer_amount = balance - fee_reserve
        
        if transfer_amount <= 0:
            print(f"[Transfer] SKIP: Wallet {wallet_index+1} has 0 SOL.")
            return

        ix = transfer(TransferParams(
            from_pubkey=keypair.pubkey(),
            to_pubkey=dest_pubkey,
            lamports=transfer_amount
        ))
        
        recent_blockhash = (await client.get_latest_blockhash()).value.blockhash
        msg = Message.new_with_blockhash([ix], keypair.pubkey(), recent_blockhash)
        tx = Transaction([keypair], msg, recent_blockhash)
        
        sig = await client.send_raw_transaction(bytes(tx))
        sol_amount = transfer_amount / LAMPORTS_PER_SOL
        print(f"[Transfer] OK: Wallet {wallet_index+1} sent {sol_amount:.4f} SOL to destination — tx: {str(sig.value)[:16]}...")

    except Exception as e:
        print(f"[Transfer] ERR: Wallet {wallet_index+1} transfer failed: {e}")


async def rescue_funds(mint_address: str, destination: str):
    """
    1. Sells all tokens from all 5 wallets.
    2. Transfers all resulting SOL to the destination address.
    """
    print(f"\n[Rescue] 🔄 Initiating Emergency Sell & Rescue")
    print(f"[Rescue] Token: {mint_address}")
    print(f"[Rescue] Destination: {destination}\n")

    keypairs = get_keypairs()
    if not keypairs:
        print("[Rescue] ERR: No wallets found.")
        return

    async with AsyncClient(MAINNET_URL) as client:
        # Step 1: Sell tokens simultaneously
        print("[Rescue] Step 1: Selling all tokens...")
        sell_tasks = [sell_from_wallet(kp, mint_address, client, i) for i, kp in enumerate(keypairs)]
        await asyncio.gather(*sell_tasks)
        
        print("\n[Rescue] Waiting 5 seconds for SOL to settle...\n")
        await asyncio.sleep(5)
        
        # Step 2: Transfer SOL back to user
        print("[Rescue] Step 2: Sweeping SOL to destination...")
        transfer_tasks = [transfer_all_sol(kp, destination, client, i) for i, kp in enumerate(keypairs)]
        await asyncio.gather(*transfer_tasks)

    print(f"\n[Rescue] ✅ Rescue complete. Check your Phantom wallet.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sell tokens and return SOL to destination")
    parser.add_argument("--token", required=True, help="Token mint address to sell")
    parser.add_argument("--destination", required=True, help="Your Phantom wallet address to receive the SOL")
    args = parser.parse_args()

    asyncio.run(rescue_funds(args.token, args.destination))
