import os
import sys
import json
import asyncio
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime
import requests
import gspread
from google.oauth2.service_account import Credentials

# --- ENGINE PATH SETUP ---
# --- ENGINE PATH SETUP ---
ROOT_DIR = Path(__file__).parent.parent.parent
# Add root to sys.path
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
    
# Add local src to sys.path
LOCAL_SRC = Path(__file__).parent
if str(LOCAL_SRC) not in sys.path:
    sys.path.insert(0, str(LOCAL_SRC))
    
# Add shared src to sys.path
SHARED_SRC = ROOT_DIR / "src"
if str(SHARED_SRC) not in sys.path:
    sys.path.insert(0, str(SHARED_SRC))

from config import config
from clients.gemini_client import gemini
from clients.twitter_client import TwitterClient
from viral_launch.generators.asset_gen import AssetGenerator

# --- CONFIGURATION ---
SPREADSHEET_ID = config.settings.get("google", {}).get("spreadsheet_name") or "1xnIbQBVAmP1vpE9Id5lAcTflW0NLcM899oFKBXqqZNE"
TAB_NAME = "Viral_Monitor"
CREDS_PATH = ROOT_DIR / "config" / "google_credentials.json"

TELEGRAM_BOT_TOKEN = config.settings.get("viral_launch", {}).get("telegram_bot_token") or config.settings.get("api_keys", {}).get("telegram_bot")
TELEGRAM_CHAT_ID = config.settings.get("viral_launch", {}).get("telegram_chat_id") or config.settings.get("telegram", {}).get("chat_id")

class ViralMonitor:
    """
    Monitors high-value Twitter accounts for 'Viral Sparks' (keywords/memes).
    Logs to Google Sheets and Telegram using direct, robust methods.
    """

    def __init__(self):
        print("[TRACE] __init__ start")
        # Initialize stable Twitter Client (uses twitterapi.io)
        self.twitter = TwitterClient()
        print("[TRACE] Twitter Client Initialized")
        
        # Initialize Google Sheets (Directly to avoid import hell)
        self.sheets_initialized = False
        try:
            print("[TRACE] Connecting to Google Sheets...")
            scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
            self.creds = Credentials.from_service_account_file(str(CREDS_PATH), scopes=scopes)
            self.gc = gspread.authorize(self.creds)
            self.sheets_initialized = True
            print("[+] ViralMonitor: Google Sheets Connected.")
        except Exception as e:
            print(f"[-] ViralMonitor: Sheets Connection Error: {e}")
            
        # Initialize Asset Generator
        self.generator = AssetGenerator()
        print("[+] ViralMonitor: Asset Generator Initialized.")
        # deduplication
        self.processed_tweet_ids = set()
        print("[TRACE] __init__ end")

    async def login(self):
        """No manual login needed for TwitterClient (API Key based)."""
        pass

    async def send_telegram_alert(self, message: str):
        """Send message to the dedicated Telegram channel."""
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            print("[-] Telegram config missing.")
            return

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        try:
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200:
                print(f"[+] Telegram Alert Sent to {TELEGRAM_CHAT_ID}.")
            else:
                print(f"[-] Telegram Failed: {resp.text}")
        except Exception as e:
            print(f"[-] Telegram Alert Error: {e}")

    async def log_to_sheet(self, tweet: Dict, analysis: Dict):
        """Log the viral spark to Google Sheets."""
        if not self.sheets_initialized: return

        try:
            ss = self.gc.open_by_key(SPREADSHEET_ID)
            try:
                ws = ss.worksheet(TAB_NAME)
            except:
                ws = ss.add_worksheet(title=TAB_NAME, rows=1000, cols=10)
                ws.append_row(["Timestamp", "Author", "Tweet", "Keyword", "Ticker", "Reason", "Score", "Link", "Action"])

            row = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                tweet['author'],
                tweet['text'][:200], # Truncate for sheet
                analysis.get('keyword', ''),
                analysis.get('token_idea', ''),
                analysis.get('reason', ''),
                "HIGH",
                tweet.get('url', ''), # Column 8: link
                ""                   # Column 9: Action
            ]
            ws.insert_row(row, index=2)
            print(f"   [+] Logged to Google Sheet: {TAB_NAME} (at top)")
        except Exception as e:
            print(f"   [-] Sheet Log Error: {e}")

    # Targets to monitor
    targets = [
        "elonmusk", "realDonaldTrump", "VitalikButerin", 
        "cz_binance", "yoheinakajima", "MustStopMurad",
        "blknoiz06", "HsakaTrades", "InternetH0F", "PopBase", "Dexerto"
    ]

    async def get_latest_tweets(self, username: str) -> List[Dict]:
        """Fetch latest tweets using the stable API client."""
        try:
            # First get user info to get the ID if needed, or search directly
            # For simplicity, search "from:username"
            query = f"from:{username}"
            resp = await self.twitter.search_tweets(query, query_type="Latest", max_results=5)
            formatted = self.twitter.format_tweets(resp)
            
            # Map to our internal format, including the original URL
            return [{
                "id": t['tweet_id'], 
                "text": t['content'], 
                "author": t['author'],
                "url": t.get('url', f"https://x.com/{t['author']}/status/{t['tweet_id']}")
            } for t in formatted]
        except Exception as e:
            print(f"[-] Error fetching @{username}: {e}")
            return []

    async def analyze_tweet(self, tweet: Dict) -> Dict:
        """Use Gemini to identify Viral Sparks."""
        prompt = f"""
        Analyze this tweet for VIRAL LAUNCH POTENTIAL.
        Author: @{tweet['author']}
        Tweet: "{tweet['text']}"
        Criteria: Absurd, funny, noun-heavy, or highly memeable events.
        Output JSON: {{"is_viral": bool, "keyword": "str", "token_idea": "str", "reason": "str"}}
        """
        try:
            response = gemini.generate_sync("You are a Meme Coin Trend Analyst.", prompt)
            clean_json = response.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            # print(f"[-] Gemini Error: {e}")
            return {"is_viral": False}

    async def process_spark(self, tweet: Dict, analysis: Dict):
        """Handle a detected viral spark."""
        print(f"[!] VIRAL SPARK DETECTED: @{tweet['author']}")
        print(f"   Ticker: {analysis.get('token_idea')}")
        
        # 1. Sheet Log
        await self.log_to_sheet(tweet, analysis)
        
        # 2. Asset Generation (Downstream Action)
        print(f"[*] Starting Asset Generation for {analysis.get('token_idea')}...")
        html = await self.generator.generate_landing_page(analysis)
        launch_dir = self.generator.save_launch_package(analysis.get('token_idea'), html, analysis)
        
        # 3. Telegram Alert
        tweet_url = tweet.get('url', '#')
        msg = (
            f"<b>🚀 VIRAL SPARK DETECTED</b>\n\n"
            f"<b>From:</b> @{tweet['author']}\n"
            f"<b>Keyword:</b> {analysis.get('keyword')}\n"
            f"<b>Ticker:</b> <code>{analysis.get('token_idea')}</code>\n\n"
            f"<b>Reason:</b> {analysis.get('reason')}\n\n"
            f"<b>🔗 <a href='{tweet_url}'>View Original Tweet</a></b>\n\n"
            f"<b>✅ LAUNCH ASSETS READY:</b>\n"
            f"<code>{launch_dir}</code>\n\n"
            f"<b>Tweet:</b> <i>{tweet['text'][:150]}...</i>"
        )
        await self.send_telegram_alert(msg)

    async def run_cycle(self, is_priming: bool = False):
        """Single scan cycle."""
        now_str = datetime.now().strftime('%H:%M:%S')
        if not is_priming:
            print(f"[-] {now_str} | Scanning {len(self.targets)} targets...")
        
        all_tweets = []
        for target in self.targets:
            tweets = await self.get_latest_tweets(target)
            # Filter for new ones
            new_tweets = [t for t in tweets if t['id'] not in self.processed_tweet_ids]
            
            # If priming, just add to set and don't collect for analysis
            if is_priming:
                for t in tweets:
                    self.processed_tweet_ids.add(t['id'])
                continue

            all_tweets.extend(new_tweets)
            
            # Keep track of IDs
            for t in tweets:
                self.processed_tweet_ids.add(t['id'])
                
            await asyncio.sleep(1) # Faster with API

        if is_priming:
            print(f"    [+] Monitor Primed (Ignoring {len(self.processed_tweet_ids)} existing tweets).")
            return

        if not all_tweets:
            print(f"    [.] No new tweets to analyze.")
            return

        print(f"    [+] Analyzing {len(all_tweets)} NEW tweets...")
        for tweet in all_tweets:
            analysis = await self.analyze_tweet(tweet)
            if analysis.get("is_viral"):
                await self.process_spark(tweet, analysis)

if __name__ == "__main__":
    print("[TRACE] Inside __main__")
    monitor = ViralMonitor()
    
    async def main():
        print("[TRACE] main() start")
        await monitor.login()
        
        # Prime the monitor: Fill seen IDs with current tweets so we don't alert on startup
        print("[*] Priming Monitor (Syncing with current Twitter state)...")
        await monitor.run_cycle(is_priming=True)
        
        print("[*] Starting Real Loop...")

        while True:
            try:
                await monitor.run_cycle()
            except Exception as e:
                print(f"[-] Loop Error: {e}")
            
            sleep_sec = config.settings.get("viral_launch", {}).get("alert_frequency_seconds", 60)
            print(f"[-] Sleeping for {sleep_sec}s...")
            await asyncio.sleep(sleep_sec)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[!] Monitor stopped.")
