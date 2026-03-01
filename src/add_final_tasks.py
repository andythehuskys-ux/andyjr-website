
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path
import sys

# Paths
ROOT_DIR = Path("c:/Users/byulh/Documents/Antigravity/crypto_research_system")
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

SPREADSHEET_ID = "1xnIbQBVAmP1vpE9Id5lAcTflW0NLcM899oFKBXqqZNE"
CREDS_PATH = ROOT_DIR / "config" / "google_credentials.json"
TAB_NAME = "Andy_Launch_Checklist"

def append_tasks():
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(str(CREDS_PATH), scopes=scopes)
        gc = gspread.authorize(creds)
        ss = gc.open_by_key(SPREADSHEET_ID)
        ws = ss.worksheet(TAB_NAME)
        
        new_tasks = [
            ["3.1", "Social Branding", "Set Andy Sr. Profile & Boardroom Hierarchy", "TODO", "Set user profile to andy.png + Custom titles", "NO"],
            ["3.2", "Wallet Ops", "Fund Launch Wallet (0.1-0.5 SOL)", "TODO", "Addr: 6tkCDvDjQ8BTPSQ6c58uAXN5eCSGAw4hPQGSgNdg9Lrc", "NO"],
            ["3.3", "Tooling", "Develop & Test Deployment Script", "TODO", "Ensure metadata and bundle buy logic works", "NO"],
            ["3.4", "Execute Launch", "Deploy $ANDYJR on Pump.fun", "TODO", "Trigger final launch loop", "NO"],
            ["3.5", "Post-Launch", "Add Buy Bot & Activate X Smart CEO", "TODO", "Enable social proof loops", "NO"]
        ]
        
        print(f"[*] Appending {len(new_tasks)} tasks to {TAB_NAME}...")
        ws.append_rows(new_tasks)
        print("[+] Success!")
        
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    append_tasks()
