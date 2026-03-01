
import os
import sys
from datetime import datetime

# BRUTE FORCE PATH FIX: Add root directory to sys.path
# This allows 'from config import config' to work regardless of where this script is run
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(ROOT_DIR)

from src.outputs.sheets_client import get_sheets_client

# Constants
SPREADSHEET_ID = "1xnIbQBVAmP1vpE9Id5lAcTflW0NLcM899oFKBXqqZNE"
TAB_NAME = "Viral_Monitor"

def debug_sheet_update():
    print(f"[*] Connecting to Sheet: {SPREADSHEET_ID}...")
    
    try:
        # 1. Auth (using the existing helper which handles credentials)
        client = get_sheets_client()
        print("   [+] Auth Successful.")
        
        # 2. Open Sheet
        sheet = client.open_by_key(SPREADSHEET_ID)
        print(f"   [+] Opened Spreadsheet: {sheet.title}")
        
        # 3. Find Tab
        try:
            ws = sheet.worksheet(TAB_NAME)
            print(f"   [+] Found Tab: {TAB_NAME}")
        except Exception as e:
            print(f"   [-] Tab '{TAB_NAME}' NOT FOUND. Creating it...")
            ws = sheet.add_worksheet(title=TAB_NAME, rows=1000, cols=10)
            ws.append_row(["Timestamp", "Author", "Tweet", "Viral_Keyword", "Ticker_Idea", "Analysis", "Launch_Score"])
            print("   [+] Created Tab and Headers.")

        # 4. Append Test Row
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_row = [
            timestamp,
            "DEBUG_BOT",
            "This is a test injection to verify connectivity.",
            "TEST_KEYWORD",
            "$TEST",
            "Debug Analysis: System Operational",
            "TEST"
        ]
        
        ws.append_row(test_row)
        print(f"   [+] Successfully appended row: {test_row}")
        
    except Exception as e:
        print(f"[-] CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_sheet_update()
