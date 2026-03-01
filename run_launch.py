"""
Viral Launch Monitor - Entry Point
Runs: Viral Monitor (Twitter -> Sheet -> Telegram -> Asset Gen)
"""
import sys
import os
import asyncio
from pathlib import Path

# Fix Path: Add root and src to sys.path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "4_Viral_Launch/src"))

# Import Monitor
from src.monitor import ViralMonitor

async def main():
    print(f"\n{'='*60}")
    print(f"!!! VIRAL LAUNCH PAD !!!")
    print(f"{'='*60}\n")
    
    print("1. Start Monitor (Live Mode) [LIVE]")
    print("2. Run Dummy Test (Check Alerts) [TEST]")
    print("3. Check Google Sheet Status [SHEET]")
    
    choice = input("\nSelect action (1-3): ").strip()
    
    try:
        if choice == "1":
            print("\n[*] Initializing Viral Monitor...")
            monitor = ViralMonitor()
            await monitor.login()
            print("[+] Monitor Active. Ctrl+C to stop.")
            while True:
                await monitor.run_cycle()
                await asyncio.sleep(3600) # Default to 1hr (Change in settings.yaml)
                
        elif choice == "2":
            # We need to import the dummy test module
            # Since we moved it, let's just run it as a subprocess or import if available
            os.system("python 4_Viral_Launch/src/dummy_test.py")
            
        elif choice == "3":
            os.system("python 4_Viral_Launch/src/check_sheet.py")
            
        else:
            print("Invalid choice.")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
