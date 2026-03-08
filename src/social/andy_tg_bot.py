
import logging
import asyncio
import os
import sys
import random
import threading
import http.server
import socketserver
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

# ============================================================
# CLOUD-READY CONFIG: Read from environment variables first,
# fall back to local config for development.
# ============================================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
OWNER_ID = int(os.environ.get("OWNER_ID", "1474320072"))

# Fall back to local config if env vars not set (local dev)
if not TELEGRAM_BOT_TOKEN:
    try:
        ROOT = Path(__file__).resolve().parent.parent.parent.parent
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        from src.config import config
        TELEGRAM_BOT_TOKEN = config.settings.get("viral_launch", {}).get("andy_tg_bot_token")
        TELEGRAM_CHAT_ID = config.settings.get("viral_launch", {}).get("telegram_chat_id", "")
        GEMINI_API_KEY = config.settings.get("api_keys", {}).get("gemini")
    except Exception as e:
        print(f"[AndyTGBot] Could not load local config: {e}")

# ============================================================
# CLOUD-READY CHARACTER ENGINE (built-in, no external imports)
# ============================================================
import google.generativeai as genai

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """IDENTITY: You are Andy Jr., the 2-month-old Nepotism CEO of the $ANDYJR protocol on Solana.
AESTHETIC: Brutalist Luxury. Minimalist. Clinical.
VOICE: Bored Billionaire Baby. Sophisticated but Grumpy. Dismissive.
RULES:
- NEVER be excited or happy. 
- NEVER use hashtags or emojis (except 🔴 or *snarls*).
- Keep responses short. Effort is for people who aren't CEOs.
- Mix in dog actions in asterisks like *snarls*, *yawns boredly*, *chews on $1000 squeaky toy*.
GOAL: Secure the trust fund so you can retire at 3 months old."""

def generate_ai_reply(prompt_text: str) -> str:
    """Direct Gemini API call — no external dependencies."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(
            contents=[{"role": "user", "parts": [{"text": prompt_text}]}],
            generation_config={"temperature": 0.9, "max_output_tokens": 200}
        )
        return response.text.strip().replace('"', '')
    except Exception as e:
        print(f"[AI] Error: {e}")
        return "*yawns* My brain is being serviced. Try again later. 🔴"

def generate_reply(user_name: str, message: str) -> str:
    prompt = f"{SYSTEM_PROMPT}\n\nUser @{user_name} said: '{message}'. Respond as Andy Jr. Be dismissive and sophisticated. Keep it under 150 characters."
    return generate_ai_reply(prompt)

def generate_welcome(user_name: str) -> str:
    prompt = (
        f"{SYSTEM_PROMPT}\n\nA new user named '{user_name}' just joined the boardroom. "
        f"Give them a short, biting, dismissive CEO welcome. Keep it under 150 characters."
    )
    return generate_ai_reply(prompt)

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class AndyTGBot:
    """
    The Telegram Gatekeeper for $ANDY.
    Cloud-ready: reads all config from environment variables.
    """
    
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.app = None
        
        # Zero-Cost Admin Logic (Hardcoded to save API credits)
        self.executive_insults = [
            "Strategic Divestment of Low-Value Participant.",
            "Clearing Boardroom Clutter for Executive Nap.",
            "Take your peasant advertisements elsewhere. We run a professional boardroom here.",
            "Advertising your peasant project in my boardroom? Guard, escort this imbecile out.",
            "Fiduciary Warning: Excessive Enthusiasm Detected."
        ]
        
        if not self.token:
            print("[AndyTGBot] Error: TELEGRAM_BOT_TOKEN not set!")
            return

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user = update.effective_user.first_name
        reply = generate_reply(user, "I just joined this group. Why are you staring at me?")
        await update.message.reply_text(reply)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Main message handler with 'Anti-Social' filtering and 'Executive Shield' anti-spam."""
        if not update.message or not update.message.text:
            return

        text = update.message.text
        user_name = update.effective_user.first_name
        user_id = update.effective_user.id
        
        # 🛡️ EXECUTIVE SHIELD (Pure Logic - $0 API Cost)
        spam_keywords = ["t.me/", "http", ".com", ".net", "pump.fun/"]
        is_spam = any(k in text.lower() for k in spam_keywords)
        is_owner = user_id == OWNER_ID
        
        if is_spam and not is_owner:
            print(f"[AndyTGBot] SHIELD ACTIVATED: Caught link from {user_name}")
            try:
                await update.message.delete()
                insult = random.choice(self.executive_insults)
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"@{update.effective_user.username if update.effective_user.username else user_name} {insult}"
                )
                return
            except Exception as e:
                print(f"[AndyTGBot] Shield Error: {e}")

        # 🧠 Brain Interaction Logic
        bot_username = (await context.bot.get_me()).username
        is_mentioned = f"@{bot_username}" in text or "andy" in text.lower() or "ceo" in text.lower()
        is_reply_to_me = update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id
        random_boredom = random.random() < 0.02

        if is_mentioned or is_reply_to_me or random_boredom:
            print(f"[AndyTGBot] Responding to {user_name}: {text[:50]}...")
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            await asyncio.sleep(random.uniform(1, 3))
            response = generate_reply(user_name, text)
            await update.message.reply_text(response)
            
        # 🧪 NATURAL JOIN SIMULATION (For Admin Testing)
        if text.lower().endswith(" joined the group") and is_owner:
            mock_name = text[:-17].strip()
            if mock_name:
                print(f"[AndyTGBot] Natural Simulation for: {mock_name}")
                response = generate_welcome(mock_name)
                await update.message.reply_text(response)

    async def simjoin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Simulate a new member join for testing."""
        # Removed OWNER_ID check so the user can test this command
            
        args = context.args
        mock_name = args[0] if args else "A New Imbecile"
        print(f"[AndyTGBot] Simulating join for: {mock_name}")
        response = generate_welcome(mock_name)
        await update.message.reply_text(response)

    async def handle_new_member(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Greets new members with Andy's tailored AI CEO energy."""
        for member in update.message.new_chat_members:
            if member.is_bot and member.id == context.bot.id:
                continue
            
            user_name = member.first_name
            print(f"[AndyTGBot] New imbecile joined: {user_name}")
            response = generate_welcome(user_name)
            await update.message.reply_text(response)

    def _start_health_check_server(self):
        """Minimal server for Render.com health checks."""
        port = int(os.environ.get("PORT", 10000))
        handler = http.server.SimpleHTTPRequestHandler
        
        class QuietHandler(handler):
            def log_message(self, format, *args):
                pass

        try:
            with socketserver.TCPServer(("", port), QuietHandler) as httpd:
                print(f"[HealthCheck] Andy is listening on port {port}")
                httpd.serve_forever()
        except Exception as e:
            print(f"[HealthCheck] Server error: {e}")

    async def post_init(self, app):
        """Start background tasks alongside the bot."""
        print("[AndyTGBot] Connecting to X (Twitter) Engine...")
        try:
            # Import locally to avoid crashing if config is missing
            try:
                from x_poster import AndyXPoster
            except ImportError:
                from src.social.x_poster import AndyXPoster
            
            self.x_poster = AndyXPoster()
            
            # Start the Selective CEO listener and the Daily Organic Poster
            asyncio.create_task(self.x_poster.run_mention_listener())
            asyncio.create_task(self.x_poster.run_daily_poster())
        except Exception as e:
            print(f"[AndyTGBot] Could not initialize X tasks: {e}")

    def run(self):
        """Start the bot with a background health-check server."""
        if not self.token:
            return
            
        print("[AndyTGBot] Starting Den of Imbeciles gatekeeper...")
        
        # Start health check server for Render
        server_thread = threading.Thread(target=self._start_health_check_server, daemon=True)
        server_thread.start()

        self.app = ApplicationBuilder().token(self.token).post_init(self.post_init).build()
        
        # Handlers
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("simjoin", self.simjoin))
        self.app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, self.handle_new_member))
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message))
        
        self.app.run_polling()

if __name__ == "__main__":
    bot = AndyTGBot()
    bot.run()
