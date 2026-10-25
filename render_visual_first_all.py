import os
import csv
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

SRC_ZOCALO = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280/.user_uploaded/media_1792106508779_4c0bd321.jpg"
ORIG_POST01 = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280/.user_uploaded/media_1792106532968_2a0d44db.jpg"
OUT_DIR = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/BULK_20_POSTS_RENDERED"
ARTIFACT_DIR = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280"
SESS_DIR = "/Users/user/Desktop/Projects/SESSIONS PORTAFOLIO"
FARM_DIR = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/01_Alta_Resolucion_Cliente"

os.makedirs(OUT_DIR, exist_ok=True)

def get_font(size, bold=False, serif=False):
    candidates = []
    if serif:
        candidates = ["/System/Library/Fonts/Supplemental/Georgia Bold.ttf", "/System/Library/Fonts/NewYork.ttf"]
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

def extract_captoora_lens_logo(scale=0.82):
    im = Image.open(ORIG_POST01).convert("RGBA")
    w, h = im.size
    box = (int(w * 0.285), int(h * 0.860), int(w * 0.715), int(h * 0.982))
    crop = im.crop(box)
    arr = np.array(crop).astype(np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    ch, cw, _ = arr.shape
    is_white = (r > 130) & (g > 130) & (b > 130)
    is_purple = (b > 75) & (b > g * 1.05)
    is_green = (g > 65) & (g > r * 1.10)
    Y, X = np.ogrid[:ch, :cw]
    lens_dist = np.sqrt((X - cw * 0.485)**2 + (Y - ch * 0.37)**2)
    is_lens = lens_dist < (ch * 0.32)
    mask = np.where(is_white | is_purple | is_green | is_lens, 255.0, 0.0).astype(np.uint8)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    arr[:, :, 3] = mask
    return Image.fromarray(arr.astype(np.uint8), mode="RGBA").resize((int(cw * scale), int(ch * scale)), Image.Resampling.LANCZOS)

LENS_LOGO = extract_captoora_lens_logo(0.78)

def fit_cover_4x5(img_path, W=1080, H=1350):
    im = ImageOps.exif_transpose(Image.open(img_path)).convert("RGB")
    iw, ih = im.size
    target_ratio = W / float(H)
    cur_ratio = iw / float(ih)
    if cur_ratio > target_ratio:
        new_h = H
        new_w = int(cur_ratio * new_h)
    else:
        new_w = W
        new_h = int(new_w / cur_ratio)
    resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    x0 = (new_w - W) // 2
    y0 = int((new_h - H) * 0.25) # Favor keeping heads/upper subjects intact!
    return resized.crop((x0, y0, x0 + W, y0 + H))

def draw_camera_hud_icons(draw, x, y, exif_str="1/160s  •  f/2.8  •  ISO 100"):
    # Minimalist translucent HUD pill with camera icon + 3-4 words MAX so the photo dominates 92% of the frame!
    f_hud = get_font(21, bold=True)
    tb = draw.textbbox((0, 0), exif_str, font=f_hud)
    pw = (tb[2] - tb[0]) + 84
    draw.rounded_rectangle([(x, y), (x + pw, y + 48)], radius=24, fill=(10, 12, 16, 155), outline=(255, 255, 255, 95), width=1)
    # Draw minimalist vector camera icon inside pill
    cx, cy = x + 32, y + 24
    draw.rounded_rectangle([(cx - 14, cy - 9), (cx + 14, cy + 10)], radius=4, outline=(245, 185, 75, 255), width=2)
    draw.ellipse([(cx - 5, cy - 5), (cx + 5, cy + 5)], outline=(245, 185, 75, 255), width=2)
    draw.rectangle([(cx - 5, cy - 13), (cx + 5, cy - 9)], fill=(245, 185, 75, 255))
    draw.text((x + 60, y + 12), exif_str, font=f_hud, fill=(245, 245, 250, 245))

def render_photo_first_post(img_path, short_hook, hud_badge, out_filename, artifact_copy=None):
    W, H = 1080, 1350
    photo = fit_cover_4x5(img_path, W, H)
    photo = ImageEnhance.Sharpness(photo).enhance(1.15)
    photo = ImageEnhance.Contrast(photo).enhance(1.04)
    
    comp = photo.convert("RGBA")
    # Only a very subtle bottom gradient in the last 210px (85% of the photo is completely untouched!)
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grad)
    for y in range(H - 240, H):
        alpha = int(205 * ((y - (H - 240)) / 240.0))
        gdraw.line([(0, y), (W, y)], fill=(6, 7, 10, alpha))
    comp = Image.alpha_composite(comp, grad)
    
    draw = ImageDraw.Draw(comp)
    # Top-left HUD icon badge
    draw_camera_hud_icons(draw, 44, 44, hud_badge)
    
    # Minimalist 2-4 word visual title above the bottom Captoora lens signature (never covering the subject's face or body!)
    if short_hook:
        f_hook = get_font(34, bold=True, serif=True)
        tb = draw.textbbox((0, 0), short_hook, font=f_hook)
        tw = tb[2] - tb[0]
        tx = (W - tw) // 2
        ty = H - 172
        draw.text((tx + 2, ty + 2), short_hook, font=f_hook, fill=(0, 0, 0, 210))
        draw.text((tx, ty), short_hook, font=f_hook, fill=(255, 255, 255, 250))
        
    # Paste Captoora Lens Signature at the very bottom (y = H - 115)
    lx = (W - LENS_LOGO.width) // 2
    comp.paste(LENS_LOGO, (lx, H - 116), LENS_LOGO)
    
    out_rgb = comp.convert("RGB")
    out_rgb.save(os.path.join(OUT_DIR, out_filename), quality=95)
    if artifact_copy:
        out_rgb.save(os.path.join(ARTIFACT_DIR, artifact_copy), quality=93)

# ==============================================================================
# PART 1: ZOCALO 3-SLIDE HD CAROUSEL (ZERO TEXT ON SLIDE 1!)
# ==============================================================================
def build_zocalo_carousel():
    W, H = 1080, 1350
    raw = Image.open(SRC_ZOCALO).convert("RGB")
    rw, rh = raw.size
    # Exact crop of the Zócalo photograph from screenshot
    photo = raw.crop((0, int(rh * 0.115), rw, int(rh * 0.658)))
    bgr = cv2.cvtColor(np.array(photo), cv2.COLOR_RGB2BGR)
    ph, pw, _ = bgr.shape
    # Inpaint out the "1/19" pill in top-right corner
    mask = np.zeros((ph, pw), dtype=np.uint8)
    cv2.rectangle(mask, (int(pw * 0.81), 0), (pw, int(ph * 0.145)), 255, -1)
    bgr_clean = cv2.inpaint(bgr, mask, 15, cv2.INPAINT_TELEA)
    
    # HD Upscale & Micro-Contrast Enhancement (Unsharp Mask + CLAHE on L channel)
    bgr_hd = cv2.resize(bgr_clean, (W, H), interpolation=cv2.INTER_LANCZOS4)
    lab = cv2.cvtColor(bgr_hd, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=1.4, tileGridSize=(8, 8))
    l_hd = clahe.apply(l)
    bgr_hd = cv2.cvtColor(cv2.merge((l_hd, a, b)), cv2.COLOR_LAB2BGR)
    
    slide1_pil = Image.fromarray(cv2.cvtColor(bgr_hd, cv2.COLOR_BGR2RGB))
    slide1_pil = ImageEnhance.Sharpness(slide1_pil).enhance(1.35)
    
    # SLIDE 1: 100% CLEAN HD PHOTOGRAPH! Zero text covering the Día de Muertos altar, Xoloitzcuintles, Cempasúchil or wet stone!
    # Only a tiny subtle Captoora lens signature in the very bottom-right corner on the dark wet stone
    s1_rgba = slide1_pil.convert("RGBA")
    small_logo = LENS_LOGO.resize((int(LENS_LOGO.width * 0.65), int(LENS_LOGO.height * 0.65)), Image.Resampling.LANCZOS)
    s1_rgba.paste(small_logo, (W - small_logo.width - 36, H - small_logo.height - 28), small_logo)
    s1_rgb = s1_rgba.convert("RGB")
    s1_rgb.save(os.path.join(OUT_DIR, "POST_21_SLIDE_1_ZOCALO_HD_LIMPIO.jpg"), quality=96)
    s1_rgb.save(os.path.join(ARTIFACT_DIR, "zocalo_slide_1_hd_limpio.jpg"), quality=95)
    
    # SLIDE 2: Visual Reference of the Underground Necropolis / Huei Tzompantli + Atmospheric Altar (from Poncho's candle/altar world + Zócalo architectural detail)
    # Let's compose a cinematic Split Visual Reference: Top = Close-up zoom of the Aztec Deity & Xoloitzcuintles on the Zócalo altar; Bottom = Candlelit Pre-Hispanic Stone Sanctuary & Huei Tzompantli archaeological diagram!
    s2 = Image.new("RGBA", (W, H), (10, 11, 15, 255))
    # Top half (y=0..640): Dramatic zoom into the Aztec Mictlantecuhtli / Xoloitzcuintle sculptures & Cempasúchil from the Zócalo photo
    zoom_crop = slide1_pil.crop((80, 480, 1000, 1020)).resize((W, 640), Image.Resampling.LANCZOS)
    # Bottom half (y=640..1350): Candlelit stone steps & marigold petals from Poncho's master image
    altar_ref = Image.open(ORIG_POST01).convert("RGB").crop((0, 580, 960, 1050)).resize((W, 710), Image.Resampling.LANCZOS)
    s2.paste(zoom_crop.convert("RGBA"), (0, 0))
    s2.paste(altar_ref.convert("RGBA"), (0, 640))
    
    # Smooth blend between top & bottom visual references + HUD archaeological depth markers (visual diagrams, NOT walls of text!)
    s2_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(s2_overlay)
    for y in range(540, 740):
        dist = abs(y - 640) / 100.0
        alpha = int(220 * (1.0 - dist))
        d2.line([(0, y), (W, y)], fill=(10, 11, 15, alpha))
    for y in range(H - 220, H):
        alpha = int(210 * ((y - (H - 220)) / 220.0))
        d2.line([(0, y), (W, y)], fill=(8, 9, 12, alpha))
        
    # Stratigraphic Depth HUD (Visual Icons showing the 3 underground layers of the Zócalo!)
    f_badge = get_font(20, bold=True)
    f_title = get_font(30, bold=True, serif=True)
    # Layer 1 marker at y=110
    d2.rounded_rectangle([(48, 48), (590, 102)], radius=26, fill=(12, 14, 18, 185), outline=(245, 166, 35, 180), width=2)
    d2.text((74, 63), "NIVEL 0.0m  •  PLANCHA Y ALTAR ACTUAL", font=f_badge, fill=(245, 185, 75, 255))
    
    # Layer 2 marker at y=615 (Stratigraphic line)
    d2.line([(48, 640), (W - 48, 640)], fill=(245, 166, 35, 200), width=2)
    d2.rounded_rectangle([(48, 613), (680, 667)], radius=26, fill=(12, 14, 18, 215), outline=(245, 166, 35, 220), width=2)
    d2.text((74, 628), "NIVEL -4.5m  •  HUEI TZOMPANTLI (+650 CRÁNEOS INAH)", font=f_badge, fill=(255, 215, 110, 255))
    
    # Layer 3 marker at y=1140
    d2.rounded_rectangle([(48, 1120), (720, 1174)], radius=26, fill=(12, 14, 18, 205), outline=(185, 130, 255, 190), width=2)
    d2.text((74, 1135), "NIVEL -7.0m  •  GUERREROS CAÍDOS EN EL ASEDIO DE 1521", font=f_badge, fill=(225, 195, 255, 255))
    
    s2_comp = Image.alpha_composite(s2, s2_overlay)
    s2_comp.paste(LENS_LOGO, ((W - LENS_LOGO.width) // 2, H - 118), LENS_LOGO)
    s2_rgb = s2_comp.convert("RGB")
    s2_rgb.save(os.path.join(OUT_DIR, "POST_21_SLIDE_2_ESTRATIGRAFIA_TZOMPANTLI.jpg"), quality=95)
    s2_rgb.save(os.path.join(ARTIFACT_DIR, "zocalo_slide_2_referencia.jpg"), quality=94)
    
    # SLIDE 3: Visual Camera Technique & Optical Breakdown + WhatsApp Direct Studio CTA!
    # Background: Real Nikon DSLR lens + Zócalo wet floor reflection + Visual Optical HUD Icons
    s3 = Image.new("RGBA", (W, H), (10, 11, 15, 255))
    cam_bg = fit_cover_4x5(os.path.join(SESS_DIR, "Camera.jpg"), W, H)
    # Blend Zócalo sky/flag subtly into the top of the camera viewfinder scene
    s3.paste(cam_bg.convert("RGBA"), (0, 0))
    
    # Inset visual preview of the Zócalo shot with optical grid lines (Rule of Thirds + Low Angle Reflection vectors)
    inset = slide1_pil.resize((460, 575), Image.Resampling.LANCZOS)
    idraw = ImageDraw.Draw(inset)
    # Draw golden Rule-of-Thirds & Low-Angle optical vectors on the inset photo
    idraw.line([(153, 0), (153, 575)], fill=(245, 185, 75), width=2)
    idraw.line([(306, 0), (306, 575)], fill=(245, 185, 75), width=2)
    idraw.line([(0, 380), (460, 380)], fill=(100, 240, 210), width=3) # Wet floor horizon reflection line
    
    s3_ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d3 = ImageDraw.Draw(s3_ov)
    # Darken background slightly so visual HUD cards and inset photo pop
    d3.rectangle([(0, 0), (W, H)], fill=(8, 10, 15, 145))
    
    s3_comp = Image.alpha_composite(s3, s3_ov)
    # Paste optical inset on the left (x=56, y=140)
    s3_comp.paste(inset.convert("RGBA"), (56, 140))
    d3_final = ImageDraw.Draw(s3_comp)
    d3_final.rounded_rectangle([(54, 138), (518, 717)], radius=16, outline=(245, 185, 75, 220), width=3)
    
    # Top header badge
    d3_final.rounded_rectangle([(56, 52), (590, 102)], radius=25, fill=(14, 16, 22, 210), outline=(245, 185, 75, 180), width=2)
    d3_final.text((82, 66), "ANÁLISIS ÓPTICO CAPTOORA  •  TÉCNICA", font=f_badge, fill=(245, 185, 75, 255))
    
    # 3 Visual Spec Badges on the right of the inset (x=548..1024)
    specs = [
        ("ÁNGULO CONTRAPICADO RASANTE", "Lente a 15 cm del piso mojado para duplicar el altar en el reflejo."),
        ("RANGO DINÁMICO EN TORMENTA", "Subexposición -1.3 EV para salvar textura en nubes dramáticas."),
        ("CONTRASTE CROMÁTICO", "Cempasúchil (590nm) + Bandera vs. Piedra Volcánica Fría.")
    ]
    f_spec_t = get_font(21, bold=True)
    f_spec_b = get_font(19, bold=False)
    sy = 148
    for stitle, sdesc in specs:
        d3_final.rounded_rectangle([(548, sy), (1024, sy + 172)], radius=22, fill=(16, 19, 26, 215), outline=(255, 255, 255, 75), width=1)
        d3_final.rounded_rectangle([(568, sy + 22), (610, sy + 27)], radius=2, fill=(245, 166, 35, 255))
        d3_final.text((568, sy + 38), stitle, font=f_spec_t, fill=(255, 255, 255, 255))
        # Wrap short description
        words = sdesc.split()
        l1 = " ".join(words[:6])
        l2 = " ".join(words[6:])
        d3_final.text((568, sy + 76), l1, font=f_spec_b, fill=(205, 212, 225, 240))
        d3_final.text((568, sy + 104), l2, font=f_spec_b, fill=(205, 212, 225, 240))
        sy += 194
        
    # Bottom Luxury Glassmorphism WhatsApp CTA Card (y=775..1165)
    d3_final.rounded_rectangle([(56, 775), (1024, 1155)], radius=32, fill=(14, 18, 24, 225), outline=(46, 213, 115, 210), width=2)
    f_cta_h = get_font(36, bold=True, serif=True)
    f_cta_s = get_font(24, bold=False)
    f_btn = get_font(24, bold=True)
    d3_final.text((100, 815), "¿Quieres retratos con esta dirección de arte?", font=f_cta_h, fill=(255, 255, 255, 255))
    d3_final.text((100, 872), "Conoce nuestro estudio en Monterrey y agenda tu sesión de temporada.", font=f_cta_s, fill=(210, 220, 230, 240))
    
    # Green WhatsApp Pill Button
    d3_final.rounded_rectangle([(100, 945), (680, 1025)], radius=40, fill=(37, 211, 102, 255))
    d3_final.text((145, 972), "📲  MÁNDANOS WHATSAPP • AGENDA ABIERTA", font=f_btn, fill=(10, 15, 12, 255))
    d3_final.text((100, 1065), "📍 San Jerónimo, Monterrey, N.L.  •  @captoora.studio", font=f_spec_b, fill=(180, 195, 210, 230))
    
    # Official Captoora Lens Signature at the bottom
    s3_comp.paste(LENS_LOGO, ((W - LENS_LOGO.width) // 2, H - 148), LENS_LOGO)
    s3_rgb = s3_comp.convert("RGB")
    s3_rgb.save(os.path.join(OUT_DIR, "POST_21_SLIDE_3_TECNICA_Y_CTA_WHATSAPP.jpg"), quality=95)
    s3_rgb.save(os.path.join(ARTIFACT_DIR, "zocalo_slide_3_tecnica_cta.jpg"), quality=94)
    print("✓ Carrusel de 3 Slides del Zócalo renderizado (Slide 1 100% limpio HD)")

# ==============================================================================
# PART 2: REBUILD ALL 20 BULK POSTS WITH 100% REAL PORTFOLIO PHOTOGRAPHY!
# ==============================================================================
def rebuild_all_20_photo_posts():
    # Post 01 is Poncho's exact master image (Moon + Cloaked Figure + Candles)
    im01 = Image.open(ORIG_POST01).convert("RGB").resize((1080, 1350), Image.Resampling.LANCZOS)
    im01.save(os.path.join(OUT_DIR, "POST_01_FRASE_PREMIUM.jpg"), quality=96)
    im01.save(os.path.join(ARTIFACT_DIR, "bulk_post_01.jpg"), quality=95)
    
    photo_posts = [
        # (post_num, filename, photo_path, hud_badge, minimal_3word_hook, artifact_preview)
        (2, "POST_02_FRASE_PREMIUM.jpg", os.path.join(SESS_DIR, "T01_blazer_overshoulder.jpg"), "85mm  •  f/1.8  •  ISO 100", "Impone presencia.", "bulk_post_02.jpg"),
        (3, "POST_03_FRASE_PREMIUM.jpg", os.path.join(SESS_DIR, "C06_muelle_atardecer.jpg"), "50mm  •  f/2.0  •  GOLDEN HOUR", "Un segundo eterno.", None),
        (4, "POST_04_FRASE_PREMIUM.jpg", os.path.join(SESS_DIR, "G04_seated_office.jpg"), "35mm  •  f/2.8  •  EDITORIAL", "El lujo en la sombra.", None),
        (5, "POST_05_FRASE_PREMIUM.jpg", os.path.join(SESS_DIR, "T02_lowbun_gaze.jpg"), "85mm  •  f/1.4  •  RETRATO", "Cómo quieres ser recordado.", None),
        
        (6, "POST_06_EDUCACIONAL.jpg", os.path.join(SESS_DIR, "Camera.jpg"), "1/160s  •  f/8.0  •  ISO 100", "La Fórmula de Estudio.", "bulk_post_06.jpg"),
        (7, "POST_07_EDUCACIONAL.jpg", os.path.join(SESS_DIR, "G03_profile_side.jpg"), "45° KEY LIGHT  •  85mm", "El ángulo que estiliza.", None),
        (8, "POST_08_EDUCACIONAL.jpg", os.path.join(SESS_DIR, "08_balcony_sunset_linen.jpg"), "LUZ NATURAL  vs  FLASH", "Domina ambas luces.", None),
        (9, "POST_09_EDUCACIONAL.jpg", os.path.join(SESS_DIR, "G01_lobby_pantsuit.jpg"), "COLORIMETRÍA  •  5300K", "El poder del negro en estudio.", None),
        (10, "POST_10_EDUCACIONAL.jpg", os.path.join(SESS_DIR, "JT01_overshoulder_ponytail.jpg"), "DIRECCIÓN DE POSE  •  MANOS", "Tensión elegante.", None),
        
        (11, "POST_11_MEME_ESTUDIO.jpg", os.path.join(SESS_DIR, "Camera_1.jpg"), "RAW SIN EDITAR  •  45MP", "«Pásame las fotos sin editar»", "bulk_post_11.jpg"),
        (12, "POST_12_MEME_ESTUDIO.jpg", os.path.join(SESS_DIR, "Camera_Floating.PNG"), "85mm GM  •  PRO STUDIO", "«Mi primo cobra $200»", "bulk_post_12.jpg"),
        (13, "POST_13_MEME_ESTUDIO.jpg", os.path.join(SESS_DIR, "AMIGA_CORE.jpg"), "1 TOMANDO FOTO  •  4 DIRIGIENDO", "Equipo de producción.", None),
        (14, "POST_14_MEME_ESTUDIO.jpg", os.path.join(SESS_DIR, "JT03_smile_ponytail.jpg"), "TOMA #4  •  PERFECCIÓN", "«No soy fotogénica»", None),
        (15, "POST_15_MEME_ESTUDIO.jpg", os.path.join(SESS_DIR, "Camera lens.jpg"), "ÓPTICA MASTER  •  CAPTOORA", "Inversión en nitidez.", None),
        
        (16, "POST_16_TEMPORADA.jpg", os.path.join(SESS_DIR, "PUMPKIN_PATCH_MKT_0926_01.jpg"), "OTOÑO  •  MONTERREY", "Temporada de Otoño.", "bulk_post_16.jpg"),
        (17, "POST_17_TEMPORADA.jpg", os.path.join(SESS_DIR, "PUMPKIN_PATCH_MKT_0926_02.jpg"), "GOLDEN AUTUMN  •  RETRATO", "Atmósfera de Octubre.", "bulk_post_17.jpg"),
        (18, "POST_18_TEMPORADA.jpg", os.path.join(FARM_DIR, "FARMASI_CPT_0845_FULLFRAME_HQ.jpg"), "BRANDING  •  E-COMMERCE", "Imagen Corporativa Q4.", None),
        (19, "POST_19_TEMPORADA.jpg", os.path.join(SESS_DIR, "C04_orilla_golden_hour.jpg"), "PREVENTA  •  FAMILIA", "Sesiones de Fin de Año.", None),
        (20, "POST_20_TEMPORADA.jpg", os.path.join(SESS_DIR, "03_barrio_antiguo_bookstore.jpg"), "GIFT CARD  •  CAPTOORA", "Regala momentos eternos.", None),
    ]
    
    for pnum, fname, ppath, badge, hook, art_copy in photo_posts:
        render_photo_first_post(ppath, hook, badge, fname, art_copy)
        
    # Build updated 5x4 Contact Sheet Mosaic of all 20 Photo-First Posts!
    all_files = [
        "POST_01_FRASE_PREMIUM.jpg", "POST_02_FRASE_PREMIUM.jpg", "POST_03_FRASE_PREMIUM.jpg", "POST_04_FRASE_PREMIUM.jpg", "POST_05_FRASE_PREMIUM.jpg",
        "POST_06_EDUCACIONAL.jpg", "POST_07_EDUCACIONAL.jpg", "POST_08_EDUCACIONAL.jpg", "POST_09_EDUCACIONAL.jpg", "POST_10_EDUCACIONAL.jpg",
        "POST_11_MEME_ESTUDIO.jpg", "POST_12_MEME_ESTUDIO.jpg", "POST_13_MEME_ESTUDIO.jpg", "POST_14_MEME_ESTUDIO.jpg", "POST_15_MEME_ESTUDIO.jpg",
        "POST_16_TEMPORADA.jpg", "POST_17_TEMPORADA.jpg", "POST_18_TEMPORADA.jpg", "POST_19_TEMPORADA.jpg", "POST_20_TEMPORADA.jpg"
    ]
    cols, rows = 5, 4
    tw, th = 360, 450
    grid = Image.new("RGB", (cols * tw + (cols + 1) * 16, rows * th + (rows + 1) * 16), (10, 11, 15))
    for i, f in enumerate(all_files):
        im = Image.open(os.path.join(OUT_DIR, f)).resize((tw, th), Image.Resampling.LANCZOS)
        r = i // cols
        c = i % cols
        grid.paste(im, (16 + c * (tw + 16), 16 + r * (th + 16)))
    grid.save(os.path.join(ARTIFACT_DIR, "mosaico_20_posts_captoora.jpg"), quality=92)
    print("✓ Los 20 Posts reconstruidos con FOTOGRAFÍA REAL AL 100% (Cero láminas de puro texto)")

if __name__ == "__main__":
    build_zocalo_carousel()
    rebuild_all_20_photo_posts()
