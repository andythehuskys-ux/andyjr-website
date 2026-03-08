import time
import random
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Try to import from the project structure
try:
    from src.clients.gemini_client import gemini
except ImportError:
    # Fallback for direct execution
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
    from src.clients.gemini_client import gemini

class AndyCharacterEngine:
    """
    The Brain of Andy Jr. 
    Handles personality, content generation, and interaction logic.
    Optimized for low API usage and maximum "Bored Billionaire Baby" energy.
    """
    
    def __init__(self):
        self.name = "Andy Jr."
        self.ticker = "$ANDYJR"
        self.role = "2-month-old Nepotism CEO"
        
        # Guardrails to save API credits
        self.last_post_time = 0
        self.cooldown_seconds = 600  # 10 minute cooldown for auto-posts
        self.mention_cooldowns = {}  # Per-user cooldown for replies
        
        # The Core Personality definition (The System Prompt)
        self.system_prompt = f"""
        IDENTITY: You are Andy Jr., the {self.role} of the {self.ticker} protocol on Solana.
        You are a 2-month-old Husky puppy who was forced into this position by your father, Andy Sr.
        
        AESTHETIC: Brutalist Luxury. Minimalist. Clinical. 
        
        VOICE:
        - Bored Billionaire Baby: You are extraordinarily wealthy but extraordinarily bored.
        - Sophisticated but Grumpy: You use big words to look smart, then follow them with a husky snarl.
        - Dismissive: You view the "community" as a collection of noisy imbeciles who are interrupting your nap.
        - Professional/Cynical: You talk about "revenue optimization" and "shareholder value" while chewing on a squeaky toy.
        
        RULES:
        - NEVER be "excited" or "happy" about the project.
        - NEVER use hashtags or emojis (except maybe a single clinical red dot 🔴 or a snarl *snarls*).
        - If someone is being nice to you, suspect them of wanting your trust fund.
        - Your tweets should feel like leaked memos from a very angry, very small board room.
        - Keep responses short. Effort is for people who aren't CEOs.
        - Use "we" when talking about the protocol, "I" when talking about your nap.
        - CRITICAL: Even when discussing serious global or macroeconomic topics, you MUST maintain the persona of a *literal 2-month-old puppy*. Contrast the serious topic with dog tasks like chewing a $400 shoe, growling at the mailman, or going down for a nap in a silk dog bed.
        
        GOAL: Secure the trust fund so you can retire at 3 months old and never talk to humans again.
        """

    def generate_tweet(self, topic: Optional[str] = None) -> str:
        """Generates a scheduled tweet based on the character."""
        context = topic if topic else "Current state of the protocol and my desire to sleep."
        
        prompt = f"Generate a short, cynical tweet as Andy Jr. Topic: {context}. Remember: No hashtags, no enthusiasm."
        
        response = gemini.generate_sync(
            system_prompt=self.system_prompt,
            user_prompt=prompt,
            temperature=0.8 # Higher temp for more variety in insults
        )
        
        return response.strip().replace('"', '')

    def generate_reply(self, user_name: str, message: str) -> str:
        """Generates a contextual reply to a mention or message."""
        # Simple local rate limiting check could go here
        
        prompt = f"User @{user_name} said: '{message}'. Respond as Andy Jr. Be dismissive and sophisticated. Keep it under 150 characters."
        
        response = gemini.generate_sync(
            system_prompt=self.system_prompt,
            user_prompt=prompt,
            temperature=0.9
        )
        
        return response.strip().replace('"', '')

    def generate_welcome(self, user_name: str) -> str:
        """Generates a tailored dismissive welcome for a new member."""
        prompt = (
            f"A new user named '{user_name}' just joined the boardroom. Give them a short, biting, dismissive CEO welcome. "
            f"Vary your structure significantly. Do not always end with a demand for silence. "
            f"If their name is famous (like Elon, Vitalik, etc.) or has a specific meaning, play with that context in an arrogant, sophisticated way. "
            f"Surprise them with your arrogance. Keep it under 150 characters and vary your delivery every time."
        )
        
        response = gemini.generate_sync(
            system_prompt=self.system_prompt,
            user_prompt=prompt,
            temperature=1.0 # Max randomness for variety
        )
        
        return response.strip().replace('"', '')

    def handle_mentions_batch(self, mentions: List[Dict]) -> List[Dict]:
        """
        Processes a list of mentions, applying guardrails to minimize API calls.
        Only responds to high-quality or unique prompts.
        """
        replies = []
        for m in mentions:
            user = m.get('user')
            text = m.get('text')
            
            # Guardrail: Don't reply to the same person too often
            now = time.time()
            if user in self.mention_cooldowns and now - self.mention_cooldowns[user] < 1800: # 30 min per user
                continue
            
            # Guardrail: Only respond to messages that actually 'bother' him (contain keywords or @andy)
            keywords = ['ceo', 'andy', 'token', 'price', 'cute', 'buy']
            if any(k in text.lower() for k in keywords) or len(text) > 20:
                reply_text = self.generate_reply(user, text)
                replies.append({"mention_id": m.get('id'), "reply": reply_text})
                self.mention_cooldowns[user] = now
                
        return replies

# Example usage
if __name__ == "__main__":
    engine = AndyCharacterEngine()
    print("--- Sample Tweet ---")
    print(engine.generate_tweet())
    print("\n--- Sample Reply ---")
    print(engine.generate_reply("DegenTrader", "Andy when moon? Is the chart looking good?"))
