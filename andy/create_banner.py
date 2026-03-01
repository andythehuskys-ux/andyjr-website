from PIL import Image, ImageFilter
import os
import sys

def create_banner():
    # Paths
    base_dir = r"c:\Users\byulh\Documents\Antigravity\crypto_research_system\4_Viral_Launch\andy"
    input_path = os.path.join(base_dir, "IMG_8128.jpg")
    output_path = os.path.join(base_dir, "banner_1500x500.jpg")
    
    if not os.path.exists(input_path):
        print(f"Error: Could not find {input_path}")
        return

    # Target dimensions for Twitter banner
    target_w, target_h = 1500, 500
    
    # Open the original image
    with Image.open(input_path) as img:
        # 1. Create blurred background (crop to 3:1 aspect ratio then blur)
        orig_w, orig_h = img.size
        
        # Calculate crop for background
        # We want 1500:500 (3:1) out of whatever the original is
        bg_aspect = target_w / target_h
        img_aspect = orig_w / orig_h
        
        if img_aspect > bg_aspect:
            # Image is wider than 3:1 - crop width
            new_w = int(orig_h * bg_aspect)
            left = (orig_w - new_w) / 2
            top = 0
            right = left + new_w
            bottom = orig_h
        else:
            # Image is taller than 3:1 - crop height
            new_h = int(orig_w / bg_aspect)
            left = 0
            # Center vertically but bias slightly towards the top where faces usually are
            top = (orig_h - new_h) * 0.3
            right = orig_w
            bottom = top + new_h
            
        bg = img.crop((left, top, right, bottom))
        bg = bg.resize((target_w, target_h), Image.Resampling.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(radius=20))
        
        # 2. Resize original to fit height (500)
        scale = target_h / orig_h
        fg_w = int(orig_w * scale)
        fg_h = target_h
        fg = img.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
        
        # 3. Paste fg onto bg
        paste_x = (target_w - fg_w) // 2
        paste_y = 0
        
        bg.paste(fg, (paste_x, paste_y))
        
        # Save
        bg.save(output_path, quality=95)
        print(f"Success! Created strictly sized banner at {output_path}")

if __name__ == "__main__":
    create_banner()
