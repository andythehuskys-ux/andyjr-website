import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'C:/Users/byulh/Documents/Antigravity/crypto_research_system')

import gspread
from google.oauth2.service_account import Credentials

scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file(
    'C:/Users/byulh/Documents/Antigravity/crypto_research_system/config/google_credentials.json',
    scopes=scopes
)
gc = gspread.authorize(creds)
ss = gc.open_by_key('1xnIbQBVAmP1vpE9Id5lAcTflW0NLcM899oFKBXqqZNE')

# Create or get tab
try:
    ws = ss.add_worksheet(title='Andy_Launch_Checklist', rows=120, cols=6)
    print('Created new tab: Andy_Launch_Checklist')
except Exception as e:
    ws = ss.worksheet('Andy_Launch_Checklist')
    ws.clear()
    print('Cleared existing tab')

# Headers
header = [['#', 'Module', 'Task', 'Status', 'Notes', 'Done']]
ws.update('A1:F1', header)
ws.format('A1:F1', {'textFormat': {'bold': True, 'fontSize': 11}})

rows = [
    # IDENTITY
    ['', '--- ANDY ($ANDY) — Identity ---', '', '', '', ''],
    ['0.1', 'Identity', 'Token name: $ANDY', 'DONE', 'Andy the Husky', 'YES'],
    ['0.2', 'Identity', 'Character: Dramatic talking husky', 'DONE', 'Complains. Argues. Howls.', 'YES'],
    ['0.3', 'Identity', 'Chain: Solana via Pump.fun', 'DONE', '', 'YES'],
    ['0.4', 'Identity', 'Get good photo of Andy for logo/pfp', 'TODO', 'Real photo = authentic edge', ''],
    ['', '', '', '', '', ''],

    # MODULE 1
    ['', '--- MODULE 1: X / Twitter ---', '', '', '', ''],
    ['1.1', 'X Manual', 'Create X account at x.com', 'TODO', 'New account for Andy', ''],
    ['1.2', 'X Manual', 'Set username (@AndyTheHusky or @AndySolana)', 'TODO', '', ''],
    ['1.3', 'X Manual', 'Upload Andy photo as profile picture', 'TODO', '', ''],
    ['1.4', 'X Manual', 'Write bio in Andy voice', 'TODO', 'i am andy. i have opinions. $ANDY on sol', ''],
    ['1.5', 'X API', 'Apply for X Developer access (developer.x.com)', 'TODO', 'Need Read + Write permissions', ''],
    ['1.6', 'X API', 'Get API Key + API Secret', 'TODO', '', ''],
    ['1.7', 'X API', 'Get Access Token + Access Token Secret', 'TODO', '', ''],
    ['1.8', 'X API', 'Add all 4 keys to settings.yaml', 'TODO', '', ''],
    ['1.9', 'X Build', 'Build social/x_poster.py', 'TODO', 'Gemini generates Andy tweets on schedule', ''],
    ['1.10', 'X Build', 'Build reply module (replies to mentions in character)', 'TODO', '', ''],
    ['1.11', 'X Test', 'Post first Andy tweet automatically', 'TODO', '', ''],
    ['', '', '', '', '', ''],

    # MODULE 2
    ['', '--- MODULE 2: Landing Page (Website) ---', '', '', '', ''],
    ['2.1', 'Website', 'Generate Andy logo from photo (Gemini Image)', 'TODO', 'Or use real photo directly', ''],
    ['2.2', 'Website', 'Upgrade asset_gen.py with Andy theme + voice', 'TODO', 'Dark mode, Andy personality copy', ''],
    ['2.3', 'Website', 'Add Talk to Andy chat UI on website', 'TODO', 'Gemini API with Andy personality', ''],
    ['2.4', 'Website', 'Wire X link into page', 'TODO', 'After Module 1 done', ''],
    ['2.5', 'Website', 'Wire Telegram link into page', 'TODO', 'After Module 3 done', ''],
    ['2.6', 'Website', 'Wire CA into buy button', 'TODO', 'After Module 6 (Pump.fun) done', ''],
    ['2.7', 'Website', 'Deploy to Vercel or GitHub Pages', 'TODO', 'Free hosting, live public URL', ''],
    ['2.8', 'Website', 'Test all links and chat work', 'TODO', '', ''],
    ['', '', '', '', '', ''],

    # MODULE 3
    ['', '--- MODULE 3: Telegram Group + Bot ---', '', '', '', ''],
    ['3.1', 'Telegram', 'Create Telegram group manually', 'TODO', 'Public group for Andy community', ''],
    ['3.2', 'Telegram', 'Add Andy bot to the group', 'TODO', 'Bot token already in settings.yaml', ''],
    ['3.3', 'Telegram', 'Build welcome bot (greets new members in Andy voice)', 'TODO', '', ''],
    ['3.4', 'Telegram', 'Build Andy reply bot (responds to messages in character)', 'TODO', 'Gemini + Andy personality', ''],
    ['3.5', 'Telegram', 'Build price bot (DexScreener updates after launch)', 'TODO', 'After token deploys', ''],
    ['3.6', 'Telegram', 'Build anti-spam bot (remove scam links)', 'TODO', '', ''],
    ['3.7', 'Telegram', 'Test full group flow', 'TODO', '', ''],
    ['', '', '', '', '', ''],

    # MODULE 4
    ['', '--- MODULE 4: Andy AI Character ---', '', '', '', ''],
    ['4.1', 'AI Character', 'Write Andy system prompt (personality definition)', 'TODO', 'Dramatic stubborn vocal husky voice', ''],
    ['4.2', 'AI Character', 'Build social/ai_character.py (core engine)', 'TODO', 'Gemini-powered, Andy personality', ''],
    ['4.3', 'AI Character', 'Connect Andy to X (auto posts + reply to mentions)', 'TODO', '', ''],
    ['4.4', 'AI Character', 'Connect Andy to Telegram (replies in group)', 'TODO', '', ''],
    ['4.5', 'AI Character', 'Connect Andy to Website chat UI', 'TODO', '', ''],
    ['4.6', 'AI Character', 'Test: Andy responds correctly on all 3 channels', 'TODO', '', ''],
    ['', '', '', '', '', ''],

    # MODULE 5
    ['', '--- MODULE 5: Orchestrator ---', '', '', '', ''],
    ['5.1', 'Orchestrator', 'Build run_andy_launch.py (chains all modules)', 'TODO', 'One command triggers 1 to 4 in sequence', ''],
    ['5.2', 'Orchestrator', 'Log launch data to Google Sheets (Viral_Monitor)', 'TODO', '', ''],
    ['5.3', 'Orchestrator', 'Send launch complete Telegram alert to you', 'TODO', 'With all links: CA, site, X, TG', ''],
    ['5.4', 'Orchestrator', 'Dry run test (without deploying token)', 'TODO', '', ''],
    ['', '', '', '', '', ''],

    # MODULE 6 - LAST
    ['', '--- MODULE 6: Pump.fun Token Launch (LAST) ---', '', '', '', ''],
    ['6.1', 'Pump.fun', 'Build solana/launcher.py', 'TODO', 'Pump.fun API integration', ''],
    ['6.2', 'Pump.fun', 'Generate fresh Solana deployer wallet', 'TODO', '', ''],
    ['6.3', 'Pump.fun', 'Fund wallet with SOL (~0.05 SOL for deploy + snipe)', 'TODO', '', ''],
    ['6.4', 'Pump.fun', 'Deploy $ANDY token (name, ticker, desc, Andy photo)', 'TODO', 'THE LAUNCH MOMENT', ''],
    ['6.5', 'Pump.fun', 'CA auto-pastes into website, X, Telegram simultaneously', 'TODO', '', ''],
    ['6.6', 'Pump.fun', 'Verify $ANDY pair live on DexScreener', 'TODO', '', ''],
    ['6.7', 'Pump.fun', 'Pin CA tweet on X', 'TODO', '', ''],
    ['6.8', 'Pump.fun', 'Announce in Telegram group', 'TODO', '', ''],
]

ws.append_rows(rows, value_input_option='RAW')

# Color module header rows
module_rows = [2, 8, 21, 31, 40, 48, 54]
colors = [
    {'red': 0.15, 'green': 0.15, 'blue': 0.25},  # identity - dark blue
    {'red': 0.0,  'green': 0.15, 'blue': 0.25},  # M1 - blue
    {'red': 0.0,  'green': 0.2,  'blue': 0.15},  # M2 - green
    {'red': 0.15, 'green': 0.05, 'blue': 0.25},  # M3 - purple
    {'red': 0.25, 'green': 0.05, 'blue': 0.15},  # M4 - pink
    {'red': 0.2,  'green': 0.1,  'blue': 0.0},   # M5 - orange
    {'red': 0.25, 'green': 0.2,  'blue': 0.0},   # M6 - yellow
]

for i, row_idx in enumerate(module_rows):
    actual_row = row_idx + 1  # offset for header
    ws.format(f'A{actual_row}:F{actual_row}', {
        'backgroundColor': colors[i],
        'textFormat': {'bold': True, 'foregroundColor': {'red': 0.8, 'green': 0.8, 'blue': 0.8}}
    })

# Format DONE rows
ws.format('D1:D120', {'horizontalAlignment': 'CENTER'})
ws.format('F1:F120', {'horizontalAlignment': 'CENTER'})

# Freeze header
ws.freeze(rows=1)

print('Checklist created successfully!')
print('Open: https://docs.google.com/spreadsheets/d/1xnIbQBVAmP1vpE9Id5lAcTflW0NLcM899oFKBXqqZNE/edit#gid=' + str(ws.id))
