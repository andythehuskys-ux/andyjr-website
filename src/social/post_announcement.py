
import asyncio
import sys
import os
from pathlib import Path

# Fix paths for imports
ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from x_poster import AndyXPoster
except ImportError:
    from src.social.x_poster import AndyXPoster

async def post_first_tweet():
    print("--- $ANDY First Official Tweet ---")
    poster = AndyXPoster()
    
    # Topic for the launch tweet
    topic = "The $ANDYJR protocol is LIVE. Here is the contract address: CMTGEUstWG3AjTpfKRS4yA9ujdMZgpSjcTuyroCApump. Do what you will with it. Or don't. I'm taking a nap."
    
    print(f"[*] Generating announcement about: {topic}")
    tweet_text = await poster.generate_post(topic)
    
    print(f"\n[ANDY BRAIN] Generated: {tweet_text}")
    print("\n[POSTING] Sending to X...")
    
    tweet_id = await poster.post_tweet(tweet_text)
    
    if tweet_id:
        print(f"\n[SUCCESS] First tweet is LIVE!")
        print(f"URL: https://x.com/AndythehuskyS/status/{tweet_id}")
    else:
        print("\n[FAILED] Could not post tweet. Check console logs above.")

if __name__ == "__main__":
    asyncio.run(post_first_tweet())
