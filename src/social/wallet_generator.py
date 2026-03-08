"""
wallet_generator.py
Generates 5 fresh Solana wallets for the multi-wallet bundle buy strategy.
Each wallet is saved securely to a local JSON file (NEVER commit this file).

Usage:
    python src/social/wallet_generator.py
"""

import json
import os
from pathlib import Path
from solders.keypair import Keypair

# ============================================================
# CONFIG
# ============================================================
NUM_WALLETS = 5
WALLETS_DIR = Path(__file__).parent / "bundle_wallets"
WALLETS_FILE = WALLETS_DIR / "wallets.json"
RPC_URL = "https://api.mainnet-beta.solana.com"
DEVNET_URL = "https://api.devnet.solana.com"

def generate_wallets(num: int = NUM_WALLETS, overwrite: bool = False) -> list:
    """
    Generates N fresh Solana wallets and saves them to bundle_wallets/wallets.json.
    Each entry contains: index, public key, secret key (base58).
    """
    WALLETS_DIR.mkdir(exist_ok=True)

    if WALLETS_FILE.exists() and not overwrite:
        print(f"[WalletGen] Wallets already exist at {WALLETS_FILE}")
        print("[WalletGen] Use overwrite=True to regenerate. Loading existing wallets...")
        return load_wallets()

    wallets = []
    for i in range(num):
        kp = Keypair()
        entry = {
            "index": i,
            "pubkey": str(kp.pubkey()),
            "secret": list(kp.secret()),  # Raw bytes as list
        }
        wallets.append(entry)
        print(f"[WalletGen] Wallet {i+1}: {entry['pubkey']}")

    with open(WALLETS_FILE, "w") as f:
        json.dump(wallets, f, indent=2)

    print(f"\n[WalletGen] OK: {num} wallets saved to {WALLETS_FILE}")
    print("[WalletGen] !! THIS FILE CONTAINS PRIVATE KEYS. NEVER COMMIT IT TO GITHUB.")
    print("[WalletGen] Next step: Fund each wallet with SOL using fund_wallets.py")
    return wallets


def load_wallets() -> list:
    """Load existing wallets from file."""
    if not WALLETS_FILE.exists():
        print("[WalletGen] No wallets found. Run generate_wallets() first.")
        return []

    with open(WALLETS_FILE, "r") as f:
        return json.load(f)


def get_keypairs() -> list:
    """Returns a list of Keypair objects from saved wallets."""
    wallets = load_wallets()
    keypairs = []
    for w in wallets:
        secret_bytes = bytes(w["secret"])
        if len(secret_bytes) == 32:
            keypairs.append(Keypair.from_seed(secret_bytes))
        else:
            keypairs.append(Keypair.from_bytes(secret_bytes))
    return keypairs


def print_wallet_summary():
    """Print a clean summary of all wallets."""
    wallets = load_wallets()
    if not wallets:
        return

    print("\n=== Bundle Wallet Summary ===")
    for w in wallets:
        print(f"  Wallet {w['index']+1}: {w['pubkey']}")
    print(f"Total wallets: {len(wallets)}")
    print(f"File: {WALLETS_FILE}")
    print("=============================\n")


if __name__ == "__main__":
    import sys
    overwrite = "--overwrite" in sys.argv

    print("=" * 50)
    print("$ANDYJR Bundle Wallet Generator")
    print("=" * 50)

    generate_wallets(num=NUM_WALLETS, overwrite=overwrite)
    print_wallet_summary()
