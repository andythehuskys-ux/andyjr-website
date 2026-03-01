
import asyncio
import os
import sys
from pathlib import Path

# Setup Path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from viral_launch.monitor import ViralMonitor

async def run_dummy_test():
    print("[*] Starting Dummy Test for Telegram and Google Sheets...")
    
    # Initialize monitor (this will connect to Sheets)
    monitor = ViralMonitor()
    
    # 1. Prepare Fake Data
    fake_tweet = {
        "author": "ElonMusk_Dummy",
        "text": "TOP INSERT TEST: Checking if this appears at row 2! #Verify",
        "url": "https://x.com/elonmusk/status/TOP_TEST", 
        "id": 888888888
    }
    
    fake_analysis = {
        "is_viral": True,
        "keyword": "TopInsert",
        "token_idea": "$TOP",
        "reason": "Verifying new signals appear at row 2 instead of the end."
    }
    
    # 2. Trigger Processing
    print("[*] Processing Dummy Spark...")
    await monitor.process_spark(fake_tweet, fake_analysis)
    
    print("[!] Dummy Test Complete. Check Telegram and Google Sheet (8th column).")

if __name__ == "__main__":
    asyncio.run(run_dummy_test())
