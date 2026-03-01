import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path
import sys

# Paths
ROOT_DIR = Path("c:/Users/byulh/Documents/Antigravity/crypto_research_system")
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

from config import config

SPREADSHEET_ID = "1xnIbQBVAmP1vpE9Id5lAcTflW0NLcM899oFKBXqqZNE"
CREDS_PATH = ROOT_DIR / "config" / "google_credentials.json"
TAB_NAME = "Andy_Launch_Checklist"

def view_checklist():
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(str(CREDS_PATH), scopes=scopes)
        gc = gspread.authorize(creds)
        ss = gc.open_by_key(SPREADSHEET_ID)
        ws = ss.worksheet(TAB_NAME)
        
        values = ws.get_all_values()
        if not values:
            return
            
        headers = values[0]
        rows = values[1:]
        
        print("=== ANDY LAUNCH CHECKLIST ===")
        print(f"Total Rows Tracked: {len(rows)}")
        print("-" * 80)
        
        # Windows console encoding safeguard 
        sys.stdout.reconfigure(encoding='utf-8')
        
        for row in rows:
            if not row[0].strip():
                continue
                
            task_id = row[0]
            category = row[2]
            action = row[4]
            done = row[6] if len(row) > 6 else ""
            
            status_icon = "[X]" if "YES" in str(done).upper() else "[ ]"
            
            # Print specifically the top 15 tasks to save console space
            if task_id.startswith("0.") or task_id.startswith("1.") or task_id.startswith("2."):
                print(f"{status_icon} | {task_id.ljust(4)} | {category[:20].ljust(20)} | {action}")
                 
    except Exception as e:
        print(f"[-] Error reading checklist: {e}")

if __name__ == "__main__":
    view_checklist()
