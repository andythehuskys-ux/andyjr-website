
import json
import base58
from pathlib import Path
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey

class SolanaManager:
    """
    Handles wallet generation, balance checks, and basic Solana interactions.
    """
    
    def __init__(self, rpc_url: str = "https://api.mainnet-beta.solana.com"):
        self.client = Client(rpc_url)
        self.wallet_path = Path(__file__).parent / "wallet.json"
        self.keypair = None
        
    def create_or_load_wallet(self):
        """Generates a new keypair if wallet.json doesn't exist, otherwise loads it."""
        if self.wallet_path.exists():
            print("[*] Loading existing launch wallet...")
            with open(self.wallet_path, 'r') as f:
                secret = json.load(f)
                secret_bytes = bytes(secret)
                if len(secret_bytes) == 32:
                    self.keypair = Keypair.from_seed(secret_bytes)
                else:
                    self.keypair = Keypair.from_bytes(secret_bytes)
        else:
            print("[*] Generating NEW launch wallet...")
            self.keypair = Keypair()
            # Save for persistence
            with open(self.wallet_path, 'w') as f:
                json.dump(list(self.keypair.secret()), f)
            print(f"[!] NEW WALLET CREATED: {self.keypair.pubkey()}")
            print("[!] PLEASE SECURE THE wallet.json FILE IMMEDIATELY.")
            
        return self.keypair

    def get_pubkey(self) -> str:
        if not self.keypair:
            self.create_or_load_wallet()
        return str(self.keypair.pubkey())

    def get_balance(self):
        """Returns balance in SOL."""
        if not self.keypair:
            self.create_or_load_wallet()
        
        response = self.client.get_balance(self.keypair.pubkey())
        balance_lamports = response.value
        return balance_lamports / 1_000_000_000

if __name__ == "__main__":
    # Quick test
    manager = SolanaManager()
    pubkey = manager.get_pubkey()
    balance = manager.get_balance()
    
    print("\n--- Solana Launch Wallet ---")
    print(f"Address: {pubkey}")
    print(f"Balance: {balance} SOL")
    
    if balance < 0.01:
        print("\n[!] WARNING: Wallet is near empty. Funding required for $ANDYJR launch.")
    else:
        print("\n[+] Wallet funded and ready.")
