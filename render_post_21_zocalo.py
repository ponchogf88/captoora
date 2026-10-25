import os
import csv
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

SRC_SCREENSHOT = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280/.user_uploaded/media_1792106508779_4c0bd321.jpg"
ORIG_POST01 = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280/.user_uploaded/media_1792106532968_2a0d44db.jpg"
OUT_DIR = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/BULK_20_POSTS_RENDERED"
ARTIFACT_DIR = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280"
CSV_BUFFER = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/BUFFER_AUTO_CADA_3_HORAS.csv"
CSV_SHEETS = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/CANVA_BULK_CREATE_SHEETS_CAPTOORA.csv"

def get_font(size, bold=False, serif=False):
    candidates = []
    if serif:
        candidates = ["/System/Library/Fonts/Supplemental/Georgia Bold.ttf", "/System/Library/Fonts/NewYork.ttf", "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"]
    elif bold:
        candidates = ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/HelveticaNeue.ttc"]
    else:
        candidates = ["/System/Library/Fonts/HelveticaNeue.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf"]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def extract_captoora_camera_signature():
    """Extracts the exact 'Captoora - MOMENTOS que PERMANECEN' logo with the glowing lens from Poncho's Post #01."""
    im = Image.open(ORIG_POST01).convert("RGBA")
    w, h = im.size
    # In Poncho's 960x1200 image, the logo is at the bottom center: x=260..700, y=1030..1180
    box = (int(w * 0.28), int(h * 0.855), int(w * 0.72), int(h * 0.985))
    crop = im.crop(box)
    arr = np.array(crop).astype(np.float32)
    # Create clean alpha based on luminance + color saturation so the dark stone background behind the logo becomes transparent!
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    max_c = np.maximum(np.maximum(r, g), b)
    # Mask out warm orange marigold petals at the far bottom-right of the logo box (where r > g * 1.4 and b < 60)
    is_marigold = (r > 110) & (g < r * 0.78) & (b < 55)
    alpha = np.clip((max_c - 38.0) * 2.4, 0, 255)
    alpha[is_marigold] = 0
    arr[:, :, 3] = alpha
    sig = Image.fromarray(arr.astype(np.uint8), mode="RGBA")
    return sig.resize((int(sig.width * 0.88), int(sig.height * 0.88)), Image.Resampling.LANCZOS)

def render_zocalo_post():
    raw = Image.open(SRC_SCREENSHOT).convert("RGB")
    rw, rh = raw.size
    crop_box = (0, int(rh * 0.115), rw, int(rh * 0.658))
    photo = raw.crop(crop_box)
    
    # Inpaint out the "1/19" Instagram carousel pill in the top-right corner of the photo!
    bgr = cv2.cvtColor(np.array(photo), cv2.COLOR_RGB2BGR)
    ph, pw, _ = bgr.shape
    inpaint_mask = np.zeros((ph, pw), dtype=np.uint8)
    # Top-right corner where "1/19" pill sits (x > 82% of width, y < 14% of height)
    cv2.rectangle(inpaint_mask, (int(pw * 0.82), 0), (pw, int(ph * 0.14)), 255, -1)
    bgr_clean = cv2.inpaint(bgr, inpaint_mask, 15, cv2.INPAINT_TELEA)
    photo_clean = Image.fromarray(cv2.cvtColor(bgr_clean, cv2.COLOR_BGR2RGB))
    
    W, H = 1080, 1350
    # Resize photo_clean so the full Zócalo scene (sky, flag, cathedral, skeletons, cempasúchil, and wet stone floor) fills 1080x1180
    photo_up = photo_clean.resize((W, 1180), Image.Resampling.LANCZOS)
    photo_up = ImageEnhance.Sharpness(photo_up).enhance(1.30)
    photo_up = ImageEnhance.Contrast(photo_up).enhance(1.06)
    
    canvas = Image.new("RGB", (W, H), (10, 11, 15))
    canvas.paste(photo_up, (0, 0))
    floor_strip = photo_up.crop((0, 950, W, 1180)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    floor_strip = floor_strip.resize((W, 190), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(radius=8))
    canvas.paste(floor_strip, (0, 1160))
    
    # Smooth editorial gradient at the bottom for the Glassmorphism card & Captoora signature
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for y in range(200):
        alpha = int(115 * (1.0 - y / 200.0))
        odraw.line([(0, y), (W, y)], fill=(8, 10, 14, alpha))
    for y in range(820, H):
        alpha = int(230 * ((y - 820) / float(H - 820)))
        odraw.line([(0, y), (W, y)], fill=(7, 8, 12, alpha))
        
    comp = Image.alpha_composite(canvas.convert("RGBA"), overlay)
    
    # Position the Glassmorphism card at y=835..1195 so:
    # 1) Above y=835: 100% of the Cathedral, Flag, Xoloitzcuintles, Tzompantli God, AND the orange Cempasúchil border + wet floor reflection are completely visible!
    # 2) Below y=1195: The iconic "Captoora - MOMENTOS que PERMANECEN" camera lens logo sits centered at the bottom, matching Post #01!
    card_x0, card_y0, card_x1, card_y1 = 68, 835, 1012, 1195
    crop_region = comp.crop((card_x0, card_y0, card_x1, card_y1)).filter(ImageFilter.GaussianBlur(radius=26))
    tint = Image.new("RGBA", (card_x1 - card_x0, card_y1 - card_y0), (14, 16, 22, 165))
    frosted = Image.alpha_composite(crop_region, tint)
    
    mask = Image.new("L", (card_x1 - card_x0, card_y1 - card_y0), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([(0, 0), (card_x1 - card_x0 - 1, card_y1 - card_y0 - 1)], radius=32, fill=255)
    
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle([(card_x0 + 6, card_y0 + 14), (card_x1 + 6, card_y1 + 14)], radius=32, fill=(0, 0, 0, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=20))
    comp = Image.alpha_composite(comp, shadow)
    comp.paste(frosted, (card_x0, card_y0), mask)
    
    # Specular Glassmorphism border
    b_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(b_layer)
    bdraw.rounded_rectangle([(card_x0, card_y0), (card_x1, card_y1)], radius=32, outline=(255, 255, 255, 110), width=2)
    bdraw.rounded_rectangle([(card_x0 + 2, card_y0 + 2), (card_x1 - 2, card_y1 - 2)], radius=30, outline=(245, 158, 11, 80), width=1)
    comp = Image.alpha_composite(comp, b_layer)
    
    draw = ImageDraw.Draw(comp)
    f_tag = get_font(19, bold=True)
    f_head = get_font(38, bold=True, serif=True)
    f_sub = get_font(23, bold=False)
    
    # Top Pill Badge
    pill_text = "CRÓNICA DE TEMPORADA  •  ZÓCALO DE TENOCHTITLAN"
    tb = draw.textbbox((0, 0), pill_text, font=f_tag)
    pw_pill = (tb[2] - tb[0]) + 48
    draw.rounded_rectangle([(68, 48), (68 + pw_pill, 94)], radius=23, fill=(14, 16, 22, 175), outline=(245, 166, 35, 150), width=1)
    draw.text((68 + 24, 60), pill_text, font=f_tag, fill=(245, 185, 75, 255))
    
    headline = "Pisar el Zócalo en noviembre es caminar sobre el altar más grande del mundo."
    subtext = "Bajo la piedra mojada y el cempasúchil descansan los guerreros caídos de 1521 y el Huei Tzompantli de Tenochtitlan. En esta temporada, la lente no solo captura luz: desentierra memoria."
    
    max_tw = (card_x1 - card_x0) - 96
    h_lines = wrap_text(draw, headline, f_head, max_tw)
    s_lines = wrap_text(draw, subtext, f_sub, max_tw)
    
    curr_y = card_y0 + 36
    draw.rounded_rectangle([(card_x0 + 48, curr_y), (card_x0 + 135, curr_y + 5)], radius=2, fill=(245, 158, 11, 255))
    curr_y += 22
    
    for line in h_lines:
        draw.text((card_x0 + 48 + 2, curr_y + 2), line, font=f_head, fill=(0, 0, 0, 170))
        draw.text((card_x0 + 48, curr_y), line, font=f_head, fill=(255, 255, 255, 255))
        curr_y += 46
        
    curr_y += 14
    for line in s_lines:
        draw.text((card_x0 + 48, curr_y), line, font=f_sub, fill=(220, 225, 235, 240))
        curr_y += 33
        
    # Paste Poncho's iconic "Captoora - MOMENTOS que PERMANECEN" lens logo centered at the bottom (y=1208)
    sig = extract_captoora_camera_signature()
    sig_x = (W - sig.width) // 2
    comp.paste(sig, (sig_x, 1206), sig)
    
    out_rgb = comp.convert("RGB")
    out_path = os.path.join(OUT_DIR, "POST_21_TEMPORADA_ZOCALO_TUMBA_GUERREROS.jpg")
    art_path = os.path.join(ARTIFACT_DIR, "bulk_post_21_zocalo.jpg")
    out_rgb.save(out_path, quality=96)
    out_rgb.save(art_path, quality=95)
    print("✓ Renderizado limpio POST_21_TEMPORADA_ZOCALO_TUMBA_GUERREROS.jpg")

if __name__ == "__main__":
    render_zocalo_post()

def fix_logo_clean():
    # Let's refine extract_captoora_camera_signature so the rectangle edges fade to 0 alpha smoothly and marigold orange pixels are 100% transparent
    im = Image.open(ORIG_POST01).convert("RGBA")
    w, h = im.size
    box = (int(w * 0.285), int(h * 0.860), int(w * 0.715), int(h * 0.982))
    crop = im.crop(box)
    arr = np.array(crop).astype(np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    ch, cw, _ = arr.shape
    
    # Keep white letters (r>120, g>120, b>120), purple/violet lens & tagline (b > r*0.85 and b > 65), and emerald green wave (g > r*1.15 and g > 60)
    is_white = (r > 130) & (g > 130) & (b > 130)
    is_purple = (b > 75) & (b > g * 1.05)
    is_green = (g > 65) & (g > r * 1.10)
    keep = is_white | is_purple | is_green
    
    # Also keep the central camera lens circle (center x=cw*0.485, y=ch*0.38, radius=ch*0.33)
    Y, X = np.ogrid[:ch, :cw]
    lens_dist = np.sqrt((X - cw * 0.485)**2 + (Y - ch * 0.37)**2)
    is_lens = lens_dist < (ch * 0.32)
    
    mask = np.where(keep | is_lens, 255.0, 0.0).astype(np.uint8)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    arr[:, :, 3] = mask
    return Image.fromarray(arr.astype(np.uint8), mode="RGBA").resize((int(cw * 0.88), int(ch * 0.88)), Image.Resampling.LANCZOS)

extract_captoora_camera_signature = fix_logo_clean
render_zocalo_post()
