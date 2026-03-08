
import tweepy
import asyncio
from typing import Optional
import sys
import os
import json
import time
from datetime import datetime, date
from pathlib import Path

# Fix paths for imports
ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import without leading dot when running as script
# We only import config if we need it (to prevent crashes on Render where settings.yaml is ignored)
try:
    from character_engine import AndyCharacterEngine
except ImportError:
    from src.social.character_engine import AndyCharacterEngine

class AndyXPoster:
    """
    Automated X/Twitter poster for $ANDY.
    Connects the "Brain" (CharacterEngine) to the "Voice" (Tweepy/X API).
    """
    
    def __init__(self):
        # Check environment variables first (for Render/Cloud deployments)
        self.api_key = os.environ.get("TWITTER_API_KEY")
        self.api_secret = os.environ.get("TWITTER_API_SECRET")
        self.access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
        self.access_secret = os.environ.get("TWITTER_ACCESS_SECRET")
        
        # Fallback to local settings.yaml if env vars are missing
        if not all([self.api_key, self.api_secret, self.access_token, self.access_secret]):
            try:
                from src.config import config
                keys = config.settings.get("api_keys", {})
                self.api_key = self.api_key or keys.get("twitter_api_key")
                self.api_secret = self.api_secret or keys.get("twitter_api_secret")
                self.access_token = self.access_token or keys.get("twitter_access_token")
                self.access_secret = self.access_secret or keys.get("twitter_access_secret")
            except Exception as e:
                print(f"[AndyXPoster] Warning: No local config found ({e})")
        
        self.client = None
        self.brain = AndyCharacterEngine() # Use the centralized brain
        
        # Check if keys are set
        # Stats and State
        self.state_file = Path(__file__).parent / "x_state.json"
        self._load_state()
        
        self.pulse_log = ROOT / "4_Viral_Launch" / "src" / "social" / "logs" / "raw_interactions.jsonl"
        
        if all([self.api_key, self.api_secret, self.access_token, self.access_secret]):
            try:
                self.client = tweepy.Client(
                    consumer_key=self.api_key,
                    consumer_secret=self.api_secret,
                    access_token=self.access_token,
                    access_token_secret=self.access_secret,
                    wait_on_rate_limit=True
                )
                print("[AndyXPoster] Twitter client initialized.")
            except Exception as e:
                print(f"[AndyXPoster] Failed to init Tweepy: {e}")
        else:
            print("[AndyXPoster] Twitter keys missing from settings.yaml. Posting disabled.")

    def _load_state(self):
        """Load state (reply counts, etc.) from JSON."""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                self.state = json.load(f)
        else:
            self.state = {"last_reset": str(date.today()), "replies_today": 0}
        
        # Reset if it's a new day
        if self.state["last_reset"] != str(date.today()):
            self.state = {"last_reset": str(date.today()), "replies_today": 0}
            self._save_state()

    def _save_state(self):
        """Save state to JSON."""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f)

    def _log_interaction(self, source: str, user: str, text: str):
        """Log raw interaction for brain compression."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "user": user,
            "text": text
        }
        try:
            with open(self.pulse_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[AndyXPoster] Logging error: {e}")

    def can_reply(self) -> bool:
        """Check if target cap (10/day) reached."""
        self._load_state() # Refresh state
        return self.state["replies_today"] < 10

    async def generate_post(self, context: Optional[str] = None) -> str:
        """Generate a post using the Andy brain."""
        # Use the engine's tweet generation logic
        return self.brain.generate_tweet(topic=context)

    async def post_tweet(self, text: str) -> Optional[str]:
        """Post a tweet to X."""
        if not self.client:
            print(f"[AndyXPoster] (SIMULATION) Would post: {text}")
            return None
        
        # Try v2 first
        try:
            print("[AndyXPoster] Attempting v2 post...")
            response = self.client.create_tweet(text=text)
            tweet_id = response.data['id']
            print(f"[AndyXPoster] Posted (v2): https://x.com/user/status/{tweet_id}")
            return tweet_id
        except Exception as e:
            print(f"[AndyXPoster] v2 error: {e}")
            
            # Fallback to v1.1
            try:
                print("[AndyXPoster] Falling back to v1.1 post...")
                auth = tweepy.OAuth1UserHandler(self.api_key, self.api_secret, self.access_token, self.access_secret)
                api = tweepy.API(auth)
                status = api.update_status(status=text)
                tweet_id = status.id_str
                print(f"[AndyXPoster] Posted (v1.1): https://x.com/user/status/{tweet_id}")
                return tweet_id
            except Exception as e2:
                print(f"[AndyXPoster] v1.1 error: {e2}")
                return None

    async def reply_to_tweet(self, tweet_id: str, user_name: str, message: str) -> Optional[str]:
        """Reply to a tweet using the Andy brain."""
        if not self.can_reply():
            print("[AndyXPoster] Daily reply cap reached. Ignoring mention.")
            return None

        if not self.client:
            print(f"[AndyXPoster] (SIMULATION) Would reply to {user_name}: {message}")
            return None
            
        print(f"[*] Thinking about replying to @{user_name}...")
        reply_content = self.brain.generate_reply(user_name, message)
        
        try:
            response = self.client.create_tweet(
                text=reply_content,
                in_reply_to_tweet_id=tweet_id
            )
            
            # Increment and save
            self.state["replies_today"] += 1
            self._save_state()
            
            print(f"[AndyXPoster] Replied to @{user_name}: {reply_content.encode('ascii', 'ignore').decode('ascii')}")
            return response.data['id']
        except Exception as e:
            print(f"[AndyXPoster] Error replying: {e}")
            return None

    async def run_mention_listener(self):
        """The 'Selective CEO' Main Loop. Polls for mentions and engages selectively."""
        if not self.client:
            print("[AndyXPoster] Listener requires active client.")
            return

        print("[AndyXPoster] Smart Listener started. Monitoring for high-value imbeciles...")
        
        # Get my user ID for mention search
        try:
            me = self.client.get_me()
            my_id = me.data.id
        except Exception as e:
            print(f"[AndyXPoster] Could not get user ID: {e}")
            return

        last_id = self.state.get("last_mention_id")

        while True:
            try:
                # Refresh state
                self._load_state()
                
                # Fetch mentions
                mentions = self.client.get_users_mentions(
                    id=my_id,
                    since_id=last_id,
                    user_auth=True,
                    expansions=['author_id']
                )

                if mentions.data:
                    # Update local state for sync
                    users = {u.id: u.username for u in mentions.includes['users']}
                    self.state["last_mention_id"] = mentions.meta['newest_id']
                    self._save_state()
                    
                    # Convert to brain format
                    batch = []
                    for m in mentions.data:
                        batch.append({
                            "id": m.id,
                            "user": users.get(m.author_id, "unknown"),
                            "text": m.text
                        })
                    
                    # Use brain to pick the interesting ones
                    interesting_replies = self.brain.handle_mentions_batch(batch)
                    
                    for item in interesting_replies:
                        # Log the interaction for global awareness
                        self._log_interaction("X", item.get("user", "imbecile"), item["text"])
                        
                        if self.can_reply():
                            await self.reply_to_tweet(item["mention_id"], "imbecile", item["reply"])
                            # In real production, we'd pass the actual username from batch
                        else:
                            break
                
            except Exception as e:
                print(f"[AndyXPoster] Listener loop error: {e}")
            
            # Nap between checks to satisfy Andy and Twitter rate limits
            await asyncio.sleep(300) # 5 minute check interval

    async def run_daily_poster(self):
        """Posts an organic tweet once a day."""
        if not self.client:
            print("[AndyXPoster] Daily poster requires active client.")
            return

        print("[AndyXPoster] Daily organic poster started. (Runs every 24h)")
        
        # Wait 1 hour after boot before the very first scheduled post, to avoid spamming on restarts.
        # But for testing, maybe we want it to run sooner? Let's give it 60 minutes.
        await asyncio.sleep(3600)
        
        while True:
            try:
                print("[AndyXPoster] Generating daily organic thought...")
                topic = "Current macro events, inflation, or tech news contrasted with finding a good place to nap."
                tweet = await self.generate_post(topic)
                
                if len(tweet) > 3:
                    await self.post_tweet(tweet)
            except Exception as e:
                print(f"[AndyXPoster] Error in daily poster: {e}")
                
            # Sleep for exactly 1 day (86400 seconds)
            await asyncio.sleep(86400)
if __name__ == "__main__":
    async def main():
        poster = AndyXPoster()
        
        print("\n--- Andy Jr. X Control Panel ---")
        print("1. Post a manual tweet")
        print("2. Run Smart Listener (Selective CEO)")
        print("3. Test Daily Cap status")
        
        choice = input("\nSelect an action (1-3): ")
        
        if choice == "1":
            topic = input("Enter topic (or leave blank): ")
            tweet = await poster.generate_post(topic)
            print(f"\n[Generated] {tweet}")
            confirm = input("Post this? (y/n): ")
            if confirm.lower() == 'y':
                await poster.post_tweet(tweet)
        elif choice == "2":
            await poster.run_mention_listener()
        elif choice == "3":
            poster._load_state()
            print(f"\n[Cap Status] Replies sent today: {poster.state['replies_today']}/10")
            print(f"[Last Reset] {poster.state['last_reset']}")
        else:
            print("Invalid choice.")

    # Use run since we are in top-level
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[AndyXPoster] Shutting down...")
