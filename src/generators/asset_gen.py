
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Path Setup
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from config import config
from clients.gemini_client import gemini

class AssetGenerator:
    """
    Automates creation of branding and web assets for a new token launch.
    """

    def __init__(self):
        self.output_base = ROOT_DIR / "outputs" / "viral_launches"
        self.output_base.mkdir(parents=True, exist_ok=True)


    async def generate_landing_page(self, metadata: dict) -> str:
        """
        Uses Gemini to generate a high-converting, viral-ready landing page (HTML/CSS).
        Now supports project-specific archetypes.
        """
        ticker = metadata.get("token_idea", "TOKEN")
        keyword = metadata.get("keyword", "Meme")
        reason = metadata.get("reason", "")
        
        # --- ARCHETYPE INJECTION: THE ANDY RULES ---
        # If the project is ANDY-related, force specific design and voice constraints.
        archetype_prompt = ""
        if "andy" in ticker.lower() or "husky" in keyword.lower():
            archetype_prompt = """
            [SYSTEM OVERRIDE: ANDY ARCHETYPE ACTIVATED]
            AESTHETIC: 'Brutalist Luxury / Cinematic'.
            COLORS: Absolute Black (#0a0a0a), Stark White (#f8f9fa), Warning Red (#ff3333).
            VOICE: Deeply cynical, grumpy, and dismissive. Do NOT use cheerful marketing speak.
            ELEMENTS: Use high-contrast filters, frosted glass blurs, and brutalist typography (Inter/Roboto).
            LAYOUT: High-end boutique feel. Zero clutter. Max impact.
            """

        print(f"[*] Generating landing page for {ticker} using Andy rules...")
        try:
            html_code = gemini.generate_sync(
                "You are an expert Senior Creative Technologist for ultra-premium Web3 brands.",
                f"{archetype_prompt}\n\n"
                f"Create a complete, single-file landing page for: {ticker} ({keyword}). "
                f"Context: {reason}. "
                "The page should feature: Hero section, Corporate Bio, Interactive Grump-o-Meter (CSS/JS), and a Terminal-style Terminal. "
                "Ensure the copy is grumpy and resents the user. Use black, white, and red ONLY. "
                "Return ONLY the HTML code. No talk. No markdown code blocks."
            )
            
            # Robust cleaning
            html_code = html_code.replace("```html", "").replace("```", "").strip()
            if "<html>" not in html_code.lower():
                html_code = f"<!DOCTYPE html><html><head><title>{ticker}</title></head><body>{html_code}</body></html>"
            
            return html_code
        except Exception as e:
            print(f"[-] Web Gen Error: {e}")
            return "<html><body><h1>Error Generating Page</h1></body></html>"

    def save_launch_package(self, ticker: str, html_code: str, metadata: dict):
        """
        Saves the generated assets to a dedicated folder.
        """
        package_name = ticker.replace("$", "")
        launch_dir = self.output_base / package_name
        launch_dir.mkdir(parents=True, exist_ok=True)

        # Save HTML
        with open(launch_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(html_code)

        # Save Metadata
        with open(launch_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

        print(f"[+] {package_name} package saved to: {launch_dir}")
        return launch_dir

async def test_gen():
    gen = AssetGenerator()
    # Testing the new Andy Archetype
    test_meta = {
        "token_idea": "$ANDY_JR",
        "keyword": "Grumpy Husky Puppy",
        "reason": "Nepotism baby taking over the Solana ecosystem."
    }
    html = await gen.generate_landing_page(test_meta)
    gen.save_launch_package("$ANDY_JR", html, test_meta)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_gen())
