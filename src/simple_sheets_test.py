
import os
import sys
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.parent.parent
CREDENTIALS_PATH = ROOT_DIR / "config" / "google_credentials.json"
SPREADSHEET_ID = "1xnIbQBVAmP1vpE9Id5lAcTflW0NLcM899oFKBXqqZNE"
TAB_NAME = "Viral_Monitor"

def simple_debug_update():
    print(f"[*] Starting Simple Sheet Update...")
    print(f"[*] Root: {ROOT_DIR}")
    print(f"[*] Creds: {CREDENTIALS_PATH}")
    
    if not CREDENTIALS_PATH.exists():
        print("[-] Credentials not found!")
        return

    try:
        # Auth
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(str(CREDENTIALS_PATH), scopes=scopes)
        client = gspread.authorize(creds)
        print("[+] Authorized.")

        # Open
        ss = client.open_by_key(SPREADSHEET_ID)
        print(f"[+] Opened: {ss.title}")

        # Tab
        try:
            ws = ss.worksheet(TAB_NAME)
            print(f"[+] Found Tab: {TAB_NAME}")
        except:
            print(f"[-] Tab {TAB_NAME} not found. Creating...")
            ws = ss.add_worksheet(title=TAB_NAME, rows=1000, cols=10)

        # Append
        row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "DEBUG_SIMPLE", "Simulated tweet", "KEYWORD", "$TICKER", "Analysis", "HIGH"]
        ws.append_row(row)
        print(f"[+] Appended row: {row}")

    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    simple_debug_update()
