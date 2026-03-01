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

def update_checklist(task_id: str, status: str = "DONE", done: str = "YES", notes: str = None):
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(str(CREDS_PATH), scopes=scopes)
        gc = gspread.authorize(creds)
        ss = gc.open_by_key(SPREADSHEET_ID)
        ws = ss.worksheet(TAB_NAME)
        
        cell = ws.find(task_id)
        if not cell:
            print(f"[-] Task ID {task_id} not found in sheet.")
            return False
            
        row = cell.row
        ws.update_cell(row, 4, status)
        ws.update_cell(row, 6, done)
        if notes:
            ws.update_cell(row, 5, notes)
            
        print(f"[+] Updated Task {task_id} in {TAB_NAME}.")
        return True
    except Exception as e:
        print(f"[-] Error updating checklist: {e}")
        return False

if __name__ == "__main__":
    for t_id in ["1.5", "1.6", "1.7", "1.8", "1.9"]:
        update_checklist(t_id, "DONE", "YES", "API Keys added")
