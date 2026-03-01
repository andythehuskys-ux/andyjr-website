
import asyncio
import sys
import os
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

# Fix paths for imports
ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from x_poster import AndyXPoster
except ImportError:
    from src.social.x_poster import AndyXPoster

async def test_selective_ceo():
    print("--- Testing Selective CEO Module ---")
    
    # Mock the state to start fresh
    state_file = Path("src/social/x_state.json")
    if state_file.exists():
        os.remove(state_file)
        
    poster = AndyXPoster()
    
    # Mock the brain's generate_reply to save API calls
    poster.brain.generate_reply = MagicMock(return_value="*yawns* Be quiet, imbecile. 🔴")
    
    # Mock the Twitter client's create_tweet
    poster.client = MagicMock()
    poster.client.create_tweet.return_value = MagicMock(data={'id': '12345'})
    
    # Test cases
    mentions = [
        {"id": "1", "user": "degen1", "text": "gm Andy!"}, # Should be ignored (too short, no keywords)
        {"id": "2", "user": "trader2", "text": "Hey @AndythehuskyS what is the current price of the token?"}, # Should be picked (keyword: price)
        {"id": "3", "user": "fan3", "text": "Andy you are so cute! I want to buy everything."}, # Should be picked (keyword: cute/buy)
        {"id": "4", "user": "spam4", "text": "Check out my new project at scam.com!!!"} # Should be ignored (no keywords, shortish)
    ]
    
    print("\n[Step 1] Manual individual replies...")
    # These should use the state and increment it
    await poster.reply_to_tweet("2", "trader2", mentions[1]["text"])
    await poster.reply_to_tweet("3", "fan3", mentions[2]["text"])
    
    print(f"\n[STAT] Replies today: {poster.state['replies_today']}")
    
    print("\n[Step 2] Testing the Cap...")
    # Force the cap to 9 to test the next one
    poster.state["replies_today"] = 9
    poster._save_state()
    
    print("[*] Trying 10th reply (should succeed)...")
    await poster.reply_to_tweet("10", "user10", "tenth message")
    
    print("[*] Trying 11th reply (should be blocked)...")
    await poster.reply_to_tweet("11", "user11", "eleventh message")
    
    print(f"\n[FINAL STAT] Replies today: {poster.state['replies_today']}")
    
    # Cleanup mock state if created in wrong place
    if state_file.exists():
        # Keep it for now to see contents
        with open(state_file, 'r') as f:
            print(f"\n[STATE FILE CONTENT] {f.read()}")

if __name__ == "__main__":
    asyncio.run(test_selective_ceo())
