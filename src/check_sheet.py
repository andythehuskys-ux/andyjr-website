
import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))
from config import config

SPREADSHEET_ID = config.settings.get("google", {}).get("spreadsheet_name") or "1xnIbQBVAmP1vpE9Id5lAcTflW0NLcM899oFKBXqqZNE"
CREDS_PATH = ROOT_DIR / "config" / "google_credentials.json"
TAB_NAME = "Viral_Monitor"

def check_sheet():
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(str(CREDS_PATH), scopes=scopes)
        gc = gspread.authorize(creds)
        ss = gc.open_by_key(SPREADSHEET_ID)
        ws = ss.worksheet(TAB_NAME)
        # Get all values including headers
        rows = ws.get_all_values()
        print(f"Total rows in {TAB_NAME}: {len(rows)}")
        if len(rows) > 1:
            print("Row 2 (Top Record):")
            print(rows[1])
        else:
            print("Sheet is empty.")
    except Exception as e:
        print(f"Error checking sheet: {e}")

if __name__ == "__main__":
    check_sheet()
