
import tweepy
import sys
import os
from pathlib import Path

# Fix paths for imports
ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import config

def test_twitter_keys():
    print("--- $ANDY X Key Validator ---")
    
    # Load keys
    keys = config.settings.get("api_keys", {})
    api_key = keys.get("twitter_api_key")
    api_secret = keys.get("twitter_api_secret")
    access_token = keys.get("twitter_access_token")
    access_secret = keys.get("twitter_access_secret")
    
    if not all([api_key, api_secret, access_token, access_secret]):
        print("[-] Error: One or more Twitter keys are missing from config/settings.yaml")
        return

    print(f"[*] Testing connection for API Key: {api_key[:5]}...")

    # 1. Test v2 Client (Basic/Pro/Free)
    print("\n[Step 1] Testing Twitter API v2 (Client)...")
    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret
        )
        # Try a simple fetch of the authenticated user
        me = client.get_me()
        if me.data:
            print(f"[+] Success! Connected as: @{me.data.username} (ID: {me.data.id})")
        else:
            print("[-] Connected, but 'get_me()' returned no data. Check App permissions.")
    except Exception as e:
        print(f"[-] v2 Error: {e}")

    # 2. Test v1.1 API (Required for some legacy actions/media)
    print("\n[Step 2] Testing Twitter API v1.1 (OAuth1UserHandler)...")
    try:
        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
        api = tweepy.API(auth)
        user = api.verify_credentials()
        if user:
            print(f"[+] Success! v1.1 Credentials Verified: @{user.screen_name}")
        else:
            print("[-] v1.1 Failed: Could not verify credentials.")
    except Exception as e:
        print(f"[-] v1.1 Error: {e}")

    print("\n--- Troubleshooting Guide ---")
    print("1. 401 Unauthorized: Your keys/tokens are wrong or regenerated.")
    print("2. 403 Forbidden: Your App doesn't have 'Read and Write' permissions.")
    print("3. Check 'User authentication settings' in the Twitter Dev Portal.")

if __name__ == "__main__":
    test_twitter_keys()
