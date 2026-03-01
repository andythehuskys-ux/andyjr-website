
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

# Fix paths for imports
ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import config
from character_engine import AndyCharacterEngine

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class AndyTGBot:
    """
    The Telegram Gatekeeper for $ANDY.
    Manages the 'Den of Imbeciles' group chat with high efficiency.
    """
    
    def __init__(self):
        # Load keys
        self.token = config.settings.get("viral_launch", {}).get("andy_tg_bot_token")
        self.chat_id = config.settings.get("viral_launch", {}).get("telegram_chat_id")
        
        self.brain = AndyCharacterEngine()
        self.app = None
        self.pulse_log = ROOT / "4_Viral_Launch" / "src" / "social" / "logs" / "raw_interactions.jsonl"
        
        # Zero-Cost Admin Logic (Hardcoded to save API credits)
        self.executive_insults = [
            "Strategic Divestment of Low-Value Participant.",
            "Clearing Boardroom Clutter for Executive Nap.",
            "Take your peasant advertisements elsewhere. We run a professional boardroom here.",
            "Advertising your peasant project in my boardroom? Guard, escort this imbecile out.",
            "Fiduciary Warning: Excessive Enthusiasm Detected."
        ]
        
        if not self.token:
            print("[AndyTGBot] Error: telegram_bot_token missing from settings.yaml")
            return

    def _log_interaction(self, source: str, user: str, text: str):
        """Log raw interaction for brain compression."""
        from datetime import datetime
        import json
        entry = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "user": user,
            "text": text
        }
        try:
            with open(self.pulse_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[AndyTGBot] Logging error: {e}")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user = update.effective_user.first_name
        reply = self.brain.generate_reply(user, "I just joined this group. Why are you staring at me?")
        await update.message.reply_text(reply)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Main message handler with 'Anti-Social' filtering and 'Executive Shield' anti-spam."""
        if not update.message or not update.message.text:
            return

        text = update.message.text
        user_name = update.effective_user.first_name
        user_id = update.effective_user.id
        
        # 🛡️ EXECUTIVE SHIELD (Pure Logic - $0 API Cost)
        # Check for spam patterns: links, certain keywords
        spam_keywords = ["t.me/", "http", ".com", ".net", "pump.fun/"]
        is_spam = any(k in text.lower() for k in spam_keywords)
        
        # We don't want to ban the owner (you)
        is_owner = str(user_id) in config.settings.get("telegram", {}).get("chat_id", "") or user_id == 1474320072
        
        if is_spam and not is_owner:
            print(f"[AndyTGBot] SHIELD ACTIVATED: Caught link from {user_name}")
            try:
                # 1. Delete the offensive message
                await update.message.delete()
                # 2. Bark at them (Free hardcoded response)
                insult = random.choice(self.executive_insults)
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"@{update.effective_user.username if update.effective_user.username else user_name} {insult}"
                )
                return # Stop processing
            except Exception as e:
                print(f"[AndyTGBot] Shield Error (Probably missing Admin perms): {e}")

        # 🧠 Brain Interaction Logic (Tagging/Mentions)
        bot_username = (await context.bot.get_me()).username
        is_mentioned = f"@{bot_username}" in text or "andy" in text.lower() or "ceo" in text.lower()
        is_reply_to_me = update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id
        random_boredom = random.random() < 0.02

        if is_mentioned or is_reply_to_me or random_boredom:
            print(f"[AndyTGBot] Responding to {user_name}: {text[:50]}...")
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            await asyncio.sleep(random.uniform(1, 3))
            response = self.brain.generate_reply(user_name, text)
            self._log_interaction("TG", user_name, text)
            await update.message.reply_text(response)
            
        # 🧪 NATURAL JOIN SIMULATION (For Admin Testing)
        if text.lower().endswith(" joined the group") and is_owner:
            mock_name = text[:-17].strip() # Extract name before " joined the group"
            if mock_name:
                print(f"[AndyTGBot] Natural Simulation for: {mock_name}")
                # Use the real welcome logic
                response = self.brain.generate_welcome(mock_name)
                await update.message.reply_text(response)

    async def simjoin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Simulate a new member join for testing (Owner Only)."""
        user_id = update.effective_user.id
        is_owner = str(user_id) in config.settings.get("telegram", {}).get("chat_id", "") or user_id == 1474320072
        
        if not is_owner:
            return
            
        args = context.args
        mock_name = args[0] if args else "A New Imbecile"
        
        print(f"[AndyTGBot] Simulating join for: {mock_name}")
        
        # Manually trigger the brain welcome for the mock name
        response = self.brain.generate_welcome(mock_name)
        
        await update.message.reply_text(response)

    async def handle_new_member(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Greets new members with Andy's tailored AI CEO energy."""
        for member in update.message.new_chat_members:
            if member.is_bot and member.id == context.bot.id:
                continue
            
            user_name = member.first_name
            print(f"[AndyTGBot] New imbecile joined: {user_name}")
            
            # Use the engine to generate a dismissive welcome
            response = self.brain.generate_welcome(user_name)
            self._log_interaction("TG", user_name, f"LOG: {user_name} JOINED THE BOARDROOM")
            await update.message.reply_text(response)

    def _start_health_check_server(self):
        """Minimal server for Render.com health checks."""
        port = int(os.environ.get("PORT", 10000))
        handler = http.server.SimpleHTTPRequestHandler
        
        # Suppress standard logging to keep Render logs clean
        class QuietHandler(handler):
            def log_message(self, format, *args):
                pass

        try:
            with socketserver.TCPServer(("", port), QuietHandler) as httpd:
                print(f"[HealthCheck] Andy is listening for boardroom requests on port {port}")
                httpd.serve_forever()
        except Exception as e:
            print(f"[HealthCheck] Server error: {e}")

    def run(self):
        """Start the bot with a background health-check server."""
        if not self.token:
            return
            
        print("[AndyTGBot] Starting Den of Imbeciles gatekeeper...")
        
        # Start health check server for Render in a separate thread
        server_thread = threading.Thread(target=self._start_health_check_server, daemon=True)
        server_thread.start()

        self.app = ApplicationBuilder().token(self.token).build()
        
        # Handlers
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("simjoin", self.simjoin))
        self.app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, self.handle_new_member))
        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_message))
        
        self.app.run_polling()

if __name__ == "__main__":
    bot = AndyTGBot()
    bot.run()
