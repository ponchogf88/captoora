import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

OUT_DIR = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/BULK_20_POSTS_RENDERED"
ARTIFACT_DIR = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280"
ORIG_POST01 = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280/.user_uploaded/media_1792106532968_2a0d44db.jpg"
SESS_DIR = "/Users/user/Desktop/Projects/SESSIONS PORTAFOLIO"

from render_visual_first_all import LENS_LOGO, get_font, fit_cover_4x5

W, H = 1080, 1350
slide1_pil = Image.open(os.path.join(OUT_DIR, "POST_21_SLIDE_1_ZOCALO_HD_LIMPIO.jpg")).convert("RGB")

# SLIDE 2: Crop ORIG_POST01 at y=520..980 so it does NOT include the original logo from ORIG_POST01!
s2 = Image.new("RGBA", (W, H), (10, 11, 15, 255))
zoom_crop = slide1_pil.crop((60, 420, 1020, 990)).resize((W, 640), Image.Resampling.LANCZOS)
altar_ref = Image.open(ORIG_POST01).convert("RGB").crop((0, 500, 960, 980)).resize((W, 710), Image.Resampling.LANCZOS)
s2.paste(zoom_crop.convert("RGBA"), (0, 0))
s2.paste(altar_ref.convert("RGBA"), (0, 640))

s2_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d2 = ImageDraw.Draw(s2_overlay)
for y in range(540, 740):
    dist = abs(y - 640) / 100.0
    alpha = int(220 * (1.0 - dist))
    d2.line([(0, y), (W, y)], fill=(10, 11, 15, alpha))
for y in range(H - 220, H):
    alpha = int(215 * ((y - (H - 220)) / 220.0))
    d2.line([(0, y), (W, y)], fill=(8, 9, 12, alpha))

f_badge = get_font(20, bold=True)
d2.rounded_rectangle([(48, 48), (590, 102)], radius=26, fill=(12, 14, 18, 195), outline=(245, 166, 35, 190), width=2)
d2.text((74, 63), "NIVEL 0.0m  •  PLANCHA Y ALTAR ACTUAL", font=f_badge, fill=(245, 185, 75, 255))

d2.line([(48, 640), (W - 48, 640)], fill=(245, 166, 35, 210), width=2)
d2.rounded_rectangle([(48, 613), (680, 667)], radius=26, fill=(12, 14, 18, 220), outline=(245, 166, 35, 220), width=2)
d2.text((74, 628), "NIVEL -4.5m  •  HUEI TZOMPANTLI (+650 CRÁNEOS INAH)", font=f_badge, fill=(255, 215, 110, 255))

d2.rounded_rectangle([(48, 1110), (720, 1164)], radius=26, fill=(12, 14, 18, 215), outline=(185, 130, 255, 195), width=2)
d2.text((74, 1125), "NIVEL -7.0m  •  GUERREROS CAÍDOS EN EL ASEDIO DE 1521", font=f_badge, fill=(225, 195, 255, 255))

s2_comp = Image.alpha_composite(s2, s2_overlay)
s2_comp.paste(LENS_LOGO, ((W - LENS_LOGO.width) // 2, H - 122), LENS_LOGO)
s2_comp.convert("RGB").save(os.path.join(OUT_DIR, "POST_21_SLIDE_2_ESTRATIGRAFIA_TZOMPANTLI.jpg"), quality=95)
s2_comp.convert("RGB").save(os.path.join(ARTIFACT_DIR, "zocalo_slide_2_referencia.jpg"), quality=94)

# SLIDE 3: Clean vector icons (no unicode boxes) + wider green WhatsApp CTA button!
s3 = Image.new("RGBA", (W, H), (10, 11, 15, 255))
cam_bg = fit_cover_4x5(os.path.join(SESS_DIR, "Camera.jpg"), W, H)
s3.paste(cam_bg.convert("RGBA"), (0, 0))

inset = slide1_pil.resize((460, 575), Image.Resampling.LANCZOS)
idraw = ImageDraw.Draw(inset)
idraw.line([(153, 0), (153, 575)], fill=(245, 185, 75), width=2)
idraw.line([(306, 0), (306, 575)], fill=(245, 185, 75), width=2)
idraw.line([(0, 380), (460, 380)], fill=(100, 240, 210), width=3)

s3_ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d3 = ImageDraw.Draw(s3_ov)
d3.rectangle([(0, 0), (W, H)], fill=(8, 10, 15, 150))
s3_comp = Image.alpha_composite(s3, s3_ov)
s3_comp.paste(inset.convert("RGBA"), (56, 140))

d3_final = ImageDraw.Draw(s3_comp)
d3_final.rounded_rectangle([(54, 138), (518, 717)], radius=16, outline=(245, 185, 75, 220), width=3)
d3_final.rounded_rectangle([(56, 52), (590, 102)], radius=25, fill=(14, 16, 22, 215), outline=(245, 185, 75, 180), width=2)
d3_final.text((82, 66), "ANÁLISIS ÓPTICO CAPTOORA  •  TÉCNICA", font=f_badge, fill=(245, 185, 75, 255))

specs = [
    ("ÁNGULO CONTRAPICADO RASANTE", "Lente a 15 cm del piso mojado para duplicar el altar en el reflejo."),
    ("RANGO DINÁMICO EN TORMENTA", "Subexposición -1.3 EV para salvar textura en nubes dramáticas."),
    ("CONTRASTE CROMÁTICO", "Cempasúchil (590nm) + Bandera vs. Piedra Volcánica Fría.")
]
f_spec_t = get_font(21, bold=True)
f_spec_b = get_font(19, bold=False)
sy = 148
for stitle, sdesc in specs:
    d3_final.rounded_rectangle([(548, sy), (1024, sy + 172)], radius=22, fill=(16, 19, 26, 220), outline=(255, 255, 255, 80), width=1)
    d3_final.rounded_rectangle([(568, sy + 22), (610, sy + 27)], radius=2, fill=(245, 166, 35, 255))
    d3_final.text((568, sy + 38), stitle, font=f_spec_t, fill=(255, 255, 255, 255))
    words = sdesc.split()
    d3_final.text((568, sy + 76), " ".join(words[:6]), font=f_spec_b, fill=(205, 212, 225, 240))
    d3_final.text((568, sy + 104), " ".join(words[6:]), font=f_spec_b, fill=(205, 212, 225, 240))
    sy += 194

d3_final.rounded_rectangle([(56, 775), (1024, 1155)], radius=32, fill=(14, 18, 24, 230), outline=(46, 213, 115, 215), width=2)
f_cta_h = get_font(36, bold=True, serif=True)
f_cta_s = get_font(23, bold=False)
f_btn = get_font(23, bold=True)
d3_final.text((96, 815), "¿Quieres retratos con esta dirección de arte?", font=f_cta_h, fill=(255, 255, 255, 255))
d3_final.text((96, 872), "Conoce nuestro estudio en Monterrey y agenda tu sesión de temporada.", font=f_cta_s, fill=(210, 220, 230, 240))

# Wide WhatsApp Green Pill Button with vector icon (no unicode box)
btn_text = "WHATSAPP DIRECTO  •  AGENDA TU SESIÓN EN CAPTOORA"
tb_btn = d3_final.textbbox((0, 0), btn_text, font=f_btn)
btn_w = (tb_btn[2] - tb_btn[0]) + 110
d3_final.rounded_rectangle([(96, 942), (96 + btn_w, 1022)], radius=40, fill=(37, 211, 102, 255))
# Vector phone/chat circle inside button
d3_final.ellipse([(124, 964), (160, 1000)], fill=(10, 25, 15, 255))
d3_final.ellipse([(134, 974), (150, 990)], outline=(37, 211, 102, 255), width=3)
d3_final.text((176, 969), btn_text, font=f_btn, fill=(8, 14, 10, 255))

# Vector pin icon + studio location
d3_final.ellipse([(96, 1068), (112, 1084)], fill=(245, 185, 75, 255))
d3_final.text((124, 1064), "San Jerónimo, Monterrey, N.L.  •  @captoora.studio", font=f_spec_b, fill=(195, 205, 220, 240))

s3_comp.paste(LENS_LOGO, ((W - LENS_LOGO.width) // 2, H - 148), LENS_LOGO)
s3_comp.convert("RGB").save(os.path.join(OUT_DIR, "POST_21_SLIDE_3_TECNICA_Y_CTA_WHATSAPP.jpg"), quality=95)
s3_comp.convert("RGB").save(os.path.join(ARTIFACT_DIR, "zocalo_slide_3_tecnica_cta.jpg"), quality=94)
print("✓ Slides 2 y 3 corregidos y auditados")

# Fix Slide 2 bottom crop so it spans full width (W=1080) and cuts ABOVE the bottom logo of ORIG_POST01
orig_im = Image.open(ORIG_POST01).convert("RGB")
ow, oh = orig_im.size
s2 = Image.new("RGBA", (W, H), (10, 11, 15, 255))
zoom_crop = slide1_pil.crop((40, 400, 1040, 1010)).resize((W, 640), Image.Resampling.LANCZOS)
altar_ref = orig_im.crop((0, int(oh * 0.50), ow, int(oh * 0.855))).resize((W, 710), Image.Resampling.LANCZOS)
s2.paste(zoom_crop.convert("RGBA"), (0, 0))
s2.paste(altar_ref.convert("RGBA"), (0, 640))

s2_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d2 = ImageDraw.Draw(s2_overlay)
for y in range(540, 740):
    dist = abs(y - 640) / 100.0
    alpha = int(225 * (1.0 - dist))
    d2.line([(0, y), (W, y)], fill=(10, 11, 15, alpha))
for y in range(H - 220, H):
    alpha = int(220 * ((y - (H - 220)) / 220.0))
    d2.line([(0, y), (W, y)], fill=(8, 9, 12, alpha))

d2.rounded_rectangle([(48, 48), (590, 102)], radius=26, fill=(12, 14, 18, 195), outline=(245, 166, 35, 190), width=2)
d2.text((74, 63), "NIVEL 0.0m  •  PLANCHA Y ALTAR ACTUAL", font=f_badge, fill=(245, 185, 75, 255))

d2.line([(48, 640), (W - 48, 640)], fill=(245, 166, 35, 210), width=2)
d2.rounded_rectangle([(48, 613), (680, 667)], radius=26, fill=(12, 14, 18, 225), outline=(245, 166, 35, 220), width=2)
d2.text((74, 628), "NIVEL -4.5m  •  HUEI TZOMPANTLI (+650 CRÁNEOS INAH)", font=f_badge, fill=(255, 215, 110, 255))

d2.rounded_rectangle([(48, 1110), (720, 1164)], radius=26, fill=(12, 14, 18, 215), outline=(185, 130, 255, 195), width=2)
d2.text((74, 1125), "NIVEL -7.0m  •  GUERREROS CAÍDOS EN EL ASEDIO DE 1521", font=f_badge, fill=(225, 195, 255, 255))

s2_comp = Image.alpha_composite(s2, s2_overlay)
s2_comp.paste(LENS_LOGO, ((W - LENS_LOGO.width) // 2, H - 122), LENS_LOGO)
s2_comp.convert("RGB").save(os.path.join(OUT_DIR, "POST_21_SLIDE_2_ESTRATIGRAFIA_TZOMPANTLI.jpg"), quality=95)
s2_comp.convert("RGB").save(os.path.join(ARTIFACT_DIR, "zocalo_slide_2_referencia.jpg"), quality=94)
print("✓ Slide 2 100% limpio y a ancho completo")
