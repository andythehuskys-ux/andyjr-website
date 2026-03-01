
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import google.generativeai as genai

# Fix paths
ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import config

class BrainCompressor:
    """
    The 'CEO's Secretary'. 
    Compresses raw social noise into actionable boardroom intelligence.
    """
    
    def __init__(self):
        self.log_path = Path(__file__).parent / "logs" / "raw_interactions.jsonl"
        self.pulse_path = Path(__file__).parent / "global_pulse.json"
        
        # Setup Gemini
        api_key = config.settings.get("api_keys", {}).get("gemini_api_key")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def load_recent_logs(self, limit=20):
        """Read the last 20 interactions."""
        if not self.log_path.exists():
            return []
            
        logs = []
        with open(self.log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[-limit:]:
                try:
                    logs.append(json.loads(line))
                except:
                    continue
        return logs

    async def generate_summary(self):
        """Use AI to compress the noise into a 'Boardroom Briefing'."""
        logs = self.load_recent_logs()
        if not logs:
            return "No recent activity in the boardroom."

        # Format for AI
        log_text = "\n".join([f"[{l['source']}] {l['user']}: {l['text']}" for l in logs])
        
        prompt = f"""
        You are the Chief Intelligence Officer for Andy Jr. ($ANDYJR).
        Analyze these recent 20 interactions from X and Telegram and provide a ONE SENTENCE summary for the CEO.
        Focus on: What are people talking about? What is the mood? Is there a new meme or complaint?
        
        Tone: Clinical, high-level, corporate.
        
        DATA:
        {log_text}
        
        Summary:
        """
        
        if not self.model:
            return "Boardroom intelligence offline. API Key missing."

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Strategic analysis failed: {e}"

    async def update_pulse(self):
        """Update the global pulse file."""
        summary = await self.generate_summary()
        
        # Basic vibe detection
        vibe = "STABLE"
        if "angry" in summary.lower() or "complaint" in summary.lower():
            vibe = "VOLATILE"
        elif "bullish" in summary.lower() or "moon" in summary.lower():
            vibe = "GROWTH"

        pulse_data = {
            "recent_events": summary, # The compressed summary
            "executive_summary": summary,
            "global_vibe": vibe,
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.pulse_path, 'w', encoding='utf-8') as f:
            json.dump(pulse_data, f, indent=4)
            
        # Also copy to website folder for public fetch
        web_pulse = ROOT / "4_Viral_Launch" / "andy_website" / "global_pulse.json"
        with open(web_pulse, 'w', encoding='utf-8') as f:
            json.dump(pulse_data, f, indent=4)
            
        print(f"[BrainCompressor] Pulse updated and exported to website: {summary}")

if __name__ == "__main__":
    import asyncio
    compressor = BrainCompressor()
    asyncio.run(compressor.update_pulse())
