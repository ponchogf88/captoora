import csv
import os
import re
import textwrap
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageFilter

CSV_PATH = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/CANVA_BULK_CREATE_SHEETS_CAPTOORA.csv"
LOGO_PATH = "/Users/user/Desktop/Projects/CAPTOORA LOGO OFICIAL .png"
OUT_DIR = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/BULK_20_POSTS_RENDERED"
ARTIFACT_DIR = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280"
BUFFER_3H_CSV = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/BUFFER_AUTO_CADA_3_HORAS.csv"

os.makedirs(OUT_DIR, exist_ok=True)

FONT_DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
FONT_OPT = "/System/Library/Fonts/Optima.ttc"
FONT_HELV = "/System/Library/Fonts/HelveticaNeue.ttc"

def get_font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def strip_emojis(text):
    # Replace known emojis with clean editorial equivalents or remove so no missing glyph boxes appear
    replacements = {
        "🤡": "[Realidad de Estudio]",
        "⚡️💀": "[Flash Directo]",
        "🧍‍♂️": "[Modo Estatua]",
        "📉🥲": "[Inversión de Estudio]",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Remove any remaining non-latin-1 / high unicode astral plane chars
    return re.sub(r'[\U00010000-\U0010ffff\u2600-\u27bf\ufe0f]', '', text).strip()

THEMES = {
    "1":  {"bg1": "#05060A", "bg2": "#0E1324", "orb1": "#38BDF8", "orb2": "#C084FC", "accent": "#E2E8F0", "moon": True},
    "2":  {"bg1": "#09090B", "bg2": "#181512", "orb1": "#D4AF37", "orb2": "#78350F", "accent": "#FDE68A", "moon": False},
    "3":  {"bg1": "#090A0F", "bg2": "#18181B", "orb1": "#94A3B8", "orb2": "#475569", "accent": "#FFFFFF", "moon": False},
    "4":  {"bg1": "#050507", "bg2": "#141418", "orb1": "#F59E0B", "orb2": "#1E293B", "accent": "#FDE68A", "moon": False},
    "5":  {"bg1": "#040711", "bg2": "#0F172A", "orb1": "#38BDF8", "orb2": "#818CF8", "accent": "#7DD3FC", "moon": True},
    "6":  {"bg1": "#09111E", "bg2": "#0F172A", "orb1": "#0EA5E9", "orb2": "#2563EB", "accent": "#38BDF8", "moon": False},
    "7":  {"bg1": "#0F141C", "bg2": "#1E293B", "orb1": "#F43F5E", "orb2": "#FB923C", "accent": "#FDA4AF", "moon": False},
    "8":  {"bg1": "#0C0F17", "bg2": "#1E1B18", "orb1": "#F59E0B", "orb2": "#EA580C", "accent": "#FCD34D", "moon": False},
    "9":  {"bg1": "#0B0F19", "bg2": "#1E293B", "orb1": "#E2E8F0", "orb2": "#38BDF8", "accent": "#F8FAFC", "moon": False},
    "10": {"bg1": "#061224", "bg2": "#0F2942", "orb1": "#0284C7", "orb2": "#38BDF8", "accent": "#7DD3FC", "moon": False},
    "11": {"bg1": "#120D1D", "bg2": "#1E1B2E", "orb1": "#FACC15", "orb2": "#A855F7", "accent": "#FEF08A", "moon": False},
    "12": {"bg1": "#180A0D", "bg2": "#2A1215", "orb1": "#EF4444", "orb2": "#F97316", "accent": "#FCA5A5", "moon": False},
    "13": {"bg1": "#0B1518", "bg2": "#132A2E", "orb1": "#14B8A6", "orb2": "#38BDF8", "accent": "#5EEAD4", "moon": False},
    "14": {"bg1": "#130B24", "bg2": "#22143B", "orb1": "#C084FC", "orb2": "#EC4899", "accent": "#E9D5FF", "moon": False},
    "15": {"bg1": "#071710", "bg2": "#0E291E", "orb1": "#22C55E", "orb2": "#10B981", "accent": "#86EFAC", "moon": False},
    "16": {"bg1": "#180D06", "bg2": "#2B170A", "orb1": "#EA580C", "orb2": "#D97706", "accent": "#FDBA74", "moon": False},
    "17": {"bg1": "#16060A", "bg2": "#280911", "orb1": "#DC2626", "orb2": "#9333EA", "accent": "#FCA5A5", "moon": True},
    "18": {"bg1": "#070E22", "bg2": "#111E3E", "orb1": "#3B82F6", "orb2": "#D4AF37", "accent": "#93C5FD", "moon": False},
    "19": {"bg1": "#07160E", "bg2": "#10281B", "orb1": "#D4AF37", "orb2": "#15803D", "accent": "#FDE047", "moon": False},
    "20": {"bg1": "#0D0B21", "bg2": "#1B163B", "orb1": "#818CF8", "orb2": "#C084FC", "accent": "#C7D2FE", "moon": False},
}

def draw_crescent_moon(canvas, cx, cy, radius, glow_color):
    moon_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    mdraw = ImageDraw.Draw(moon_layer)
    for r in range(int(radius * 2.2), radius, -4):
        alpha = int(35 * (1 - (r - radius) / (radius * 1.2)) ** 2)
        mdraw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*glow_color, alpha))
    
    moon_disc = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ddraw = ImageDraw.Draw(moon_disc)
    ddraw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=(252, 250, 242, 245))
    offset_x = int(radius * 0.42)
    offset_y = int(-radius * 0.18)
    cut_r = int(radius * 0.88)
    ddraw.ellipse([cx + offset_x - cut_r, cy + offset_y - cut_r, cx + offset_x + cut_r, cy + offset_y + cut_r], fill=(0, 0, 0, 0))
    
    moon_layer = moon_layer.filter(ImageFilter.GaussianBlur(12))
    canvas.alpha_composite(moon_layer)
    canvas.alpha_composite(moon_disc)

def prepare_clean_logo(logo_path):
    if not os.path.exists(logo_path):
        return None
    im = Image.open(logo_path).convert("RGBA")
    # Make dark background pixels transparent so only the white emblem shines
    datas = im.getdata()
    new_data = []
    for item in datas:
        r, g, b, a = item
        brightness = (r + g + b) / 3.0
        if brightness < 45:
            new_data.append((255, 255, 255, 0))
        else:
            alpha = int(min(255, max(0, (brightness - 45) * 1.35)))
            new_data.append((255, 255, 255, alpha))
    im.putdata(new_data)
    return im

def render_post(row, logo_img):
    pid = row[0]
    cat = strip_emojis(row[1])
    title = strip_emojis(row[2])
    main_phrase = strip_emojis(row[3])
    sub_phrase = strip_emojis(row[4])
    cta = strip_emojis(row[5])
    
    W, H = 1080, 1350
    theme = THEMES.get(pid, THEMES["1"])
    c1 = hex_to_rgb(theme["bg1"])
    c2 = hex_to_rgb(theme["bg2"])
    orb1 = hex_to_rgb(theme["orb1"])
    orb2 = hex_to_rgb(theme["orb2"])
    acc = hex_to_rgb(theme["accent"])
    
    base = Image.new("RGBA", (W, H), (*c1, 255))
    draw = ImageDraw.Draw(base)
    for y in range(H):
        t = y / H
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    orbs = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(orbs)
    odraw.ellipse([-120, 80, 580, 780], fill=(*orb1, 75))
    odraw.ellipse([480, 560, 1180, 1260], fill=(*orb2, 70))
    odraw.ellipse([250, -100, 850, 450], fill=(*acc, 35))
    orbs = orbs.filter(ImageFilter.GaussianBlur(110))
    base.alpha_composite(orbs)
    
    if theme["moon"]:
        star_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sdraw = ImageDraw.Draw(star_layer)
        for i in range(65):
            sx = (i * 173 + int(pid) * 41) % W
            sy = (i * 293 + int(pid) * 97) % int(H * 0.55)
            sr = 1 if i % 3 != 0 else 2
            salpha = 60 + (i * 37) % 140
            sdraw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 255, salpha))
        base.alpha_composite(star_layer)
        draw_crescent_moon(base, cx=820, cy=230, radius=95, glow_color=acc)
        
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grid)
    gdraw.rectangle([54, 54, W - 54, H - 54], outline=(255, 255, 255, 28), width=1)
    gdraw.line([(54, 175), (W - 54, 175)], fill=(255, 255, 255, 22), width=1)
    gdraw.line([(54, H - 165), (W - 54, H - 165)], fill=(255, 255, 255, 22), width=1)
    base.alpha_composite(grid)
    
    card_x1, card_y1, card_x2, card_y2 = 95, 260, W - 95, H - 230
    crop_bg = base.crop((card_x1, card_y1, card_x2, card_y2)).filter(ImageFilter.GaussianBlur(25))
    base.paste(crop_bg, (card_x1, card_y1))
    
    f_header = get_font(FONT_HELV, 22, index=1)
    f_pill = get_font(FONT_HELV, 20, index=1)
    f_main = get_font(FONT_DIDOT, 54, index=1)
    f_sub = get_font(FONT_OPT, 30, index=0)
    f_cta = get_font(FONT_HELV, 23, index=1)
    f_num = get_font(FONT_DIDOT, 34, index=0)
    
    pill_text = f"{cat.upper()}   |   {title.upper()}"
    temp_draw = ImageDraw.Draw(base)
    text_w = temp_draw.textlength(pill_text, font=f_pill)
    pill_w = int(text_w + 56)
    pill_h = 52
    pill_x = card_x1 + 55
    pill_y = card_y1 + 52
    
    glass = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gldraw = ImageDraw.Draw(glass)
    gldraw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=38, fill=(255, 255, 255, 22), outline=(255, 255, 255, 75), width=2)
    gldraw.rounded_rectangle([card_x1 + 3, card_y1 + 3, card_x2 - 3, card_y2 - 3], radius=36, outline=(255, 255, 255, 24), width=1)
    gldraw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=26, fill=(*acc, 38), outline=(*acc, 145), width=1)
    base.alpha_composite(glass)
    
    tdraw = ImageDraw.Draw(base)
    tdraw.text((88, 98), "CAPTOORA STUDIO   •   MONTERREY", font=f_header, fill=(255, 255, 255, 215))
    tdraw.text((W - 165, 92), f"#{int(pid):02d}/20", font=f_num, fill=(*acc, 235))
    tdraw.text((pill_x + 28, pill_y + 13), pill_text, font=f_pill, fill=(255, 255, 255, 248))
    
    wrapped_main = textwrap.wrap(f"“{main_phrase}”", width=23)
    cur_y = pill_y + 102
    for line in wrapped_main[:6]:
        tdraw.text((card_x1 + 55, cur_y), line, font=f_main, fill=(255, 255, 255, 252))
        cur_y += 68
        
    cur_y += 22
    tdraw.line([(card_x1 + 55, cur_y), (card_x1 + 235, cur_y)], fill=(*acc, 215), width=3)
    cur_y += 36
    
    wrapped_sub = textwrap.wrap(sub_phrase, width=41)
    for line in wrapped_sub[:5]:
        tdraw.text((card_x1 + 55, cur_y), line, font=f_sub, fill=(226, 232, 240, 230))
        cur_y += 45
        
    cta_y = card_y2 - 92
    tdraw.line([(card_x1 + 55, cta_y - 22), (card_x2 - 55, cta_y - 22)], fill=(255, 255, 255, 35), width=1)
    # Draw clean vector diamond bullet
    dx, dy = card_x1 + 65, cta_y + 14
    tdraw.polygon([(dx, dy - 8), (dx + 8, dy), (dx, dy + 8), (dx - 8, dy)], fill=(*acc, 250))
    tdraw.text((card_x1 + 88, cta_y), cta, font=f_cta, fill=(*acc, 250))
    
    tdraw.text((88, H - 118), "COLINAS DE SAN JERÓNIMO, MTY   |   WA: 81 4005-0088", font=f_header, fill=(255, 255, 255, 190))
    
    if logo_img:
        logo_h = 86
        aspect = logo_img.width / logo_img.height
        logo_w = int(logo_h * aspect)
        logo_resized = logo_img.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        base.alpha_composite(logo_resized, (W - logo_w - 82, H - 150))
        
    return base.convert("RGB")

def main():
    logo_img = prepare_clean_logo(LOGO_PATH)
    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        rows = reader[1:]
        
    rendered_images = []
    schedule_rows = [["Post_ID", "Fecha_Hora_Programada", "Categoria", "Titulo", "Archivo_Imagen", "Text_Copy_Completo"]]
    start_dt = datetime(2026, 10, 15, 18, 0)
    
    for idx, row in enumerate(rows):
        img = render_post(row, logo_img)
        pid = int(row[0])
        fname = f"POST_{pid:02d}_{row[1].replace(' ', '_').upper()}.jpg"
        out_path = os.path.join(OUT_DIR, fname)
        img.save(out_path, quality=95)
        rendered_images.append((pid, fname, img, row))
        
        sched_time = start_dt + timedelta(hours=3 * idx)
        schedule_rows.append([
            f"#{pid:02d}",
            sched_time.strftime("%Y-%m-%d %H:%M"),
            row[1],
            row[2],
            out_path,
            row[8]
        ])
        
    with open(BUFFER_3H_CSV, mode="w", newline="", encoding="utf-8") as bf:
        writer = csv.writer(bf)
        writer.writerows(schedule_rows)
        
    thumb_w, thumb_h = 360, 450
    cols, r_count = 5, 4
    pad = 24
    grid_w = cols * thumb_w + (cols + 1) * pad
    grid_h = r_count * thumb_h + (r_count + 1) * pad + 110
    grid_img = Image.new("RGB", (grid_w, grid_h), (10, 12, 18))
    gdraw = ImageDraw.Draw(grid_img)
    f_title = get_font(FONT_HELV, 38, index=1)
    gdraw.text((pad, 32), "CAPTOORA STUDIO   •   LOTE DE 20 PUBLICACIONES GLASSMORPHISM (CADA 3 HORAS)", font=f_title, fill=(255, 255, 255))
    
    for i, (pid, fname, im, _) in enumerate(rendered_images):
        c = i % cols
        r = i // cols
        x = pad + c * (thumb_w + pad)
        y = 110 + pad + r * (thumb_h + pad)
        t_im = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        grid_img.paste(t_im, (x, y))
        
    mosaic_path = os.path.join(ARTIFACT_DIR, "mosaico_20_posts_captoora.jpg")
    grid_img.save(mosaic_path, quality=92)
    grid_img.save(os.path.join(OUT_DIR, "00_MOSAICO_20_POSTS_CAPTOORA.jpg"), quality=95)
    
    for pid, fname, im, _ in rendered_images:
        if pid in (1, 2, 6, 11, 12, 16, 17):
            im.save(os.path.join(ARTIFACT_DIR, f"bulk_post_{pid:02d}.jpg"), quality=93)
            
    print("✓ 20 Posts y Mosaico perfeccionados sin errores de glifos ni bordes.")

if __name__ == "__main__":
    main()
