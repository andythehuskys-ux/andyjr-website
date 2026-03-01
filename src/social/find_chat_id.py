
import requests
import time

TOKEN = "8753880004:AAEMzwqhmDh3EdBrkrL4qmoLuyrGiOukKG8"

def get_chat_id():
    print("--- Searching for Andy Jr.'s New Boardroom ---")
    print("[*] Waiting for you to tag @AndyJr_CEOBot in the new group...")
    
    last_update_id = 0
    start_time = time.time()
    
    while time.time() - start_time < 120:  # Search for 2 minutes
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_update_id + 1}"
            response = requests.get(url).json()
            
            if response.get("ok") and response.get("result"):
                for update in response["result"]:
                    last_update_id = update["update_id"]
                    
                    # Check for group messages
                    message = update.get("message")
                    if message:
                        chat = message.get("chat")
                        user = message.get("from", {}).get("username", "Unknown")
                        text = message.get("text", "")
                        
                        print(f"[+] Found message from @{user} in '{chat.get('title')}'")
                        print(f"[!] Chat ID: {chat.get('id')}")
                        return chat.get('id')
            
        except Exception as e:
            print(f"[-] Error: {e}")
            
        time.sleep(2)
    
    print("[-] Timeout: No message found. Make sure the bot is in the group and you tagged it!")
    return None

if __name__ == "__main__":
    get_chat_id()
