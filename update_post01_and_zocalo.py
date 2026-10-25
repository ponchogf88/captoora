import os
import csv
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ORIG_POST01 = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280/.user_uploaded/media_1792106532968_2a0d44db.jpg"
OUT_DIR = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/BULK_20_POSTS_RENDERED"
ARTIFACT_DIR = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280"
CSV_SHEETS = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/CANVA_BULK_CREATE_SHEETS_CAPTOORA.csv"
CSV_BUFFER = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/BUFFER_AUTO_CADA_3_HORAS.csv"

# 1. Update Post #01 with Poncho's exact master piece (resized/standardized to 1080x1350 HQ)
im01 = Image.open(ORIG_POST01).convert("RGB")
im01_1080 = im01.resize((1080, 1350), Image.Resampling.LANCZOS)
post01_path = os.path.join(OUT_DIR, "POST_01_FRASE_PREMIUM.jpg")
im01_1080.save(post01_path, quality=96)
im01_1080.save(os.path.join(ARTIFACT_DIR, "bulk_post_01.jpg"), quality=95)
print("✓ Post #01 actualizado con la imagen maestra original de Poncho (Luna Menguante + Cempasúchil + Captoora)")

# 2. Extract the exact bottom logo from Poncho's image so we can also use it cleanly or create a matching sibling version of Post #21 (Zócalo)
# Let's also create a version of Post #21 that blends Poncho's exact Captoora bottom signature + Glassmorphism card!
# And let's rebuild the Mosaic (now 21 posts: 3x7 or 5x4+1) so Poncho sees his exact Post #01 and Post #21 in the master sheet!
all_files = sorted([f for f in os.listdir(OUT_DIR) if f.startswith("POST_") and f.endswith(".jpg")])
cols, rows = 5, 5
thumb_w, thumb_h = 360, 450
grid = Image.new("RGB", (cols * thumb_w + (cols + 1) * 16, 4 * thumb_h + 5 * 16), (12, 13, 18))
for i, fname in enumerate(all_files[:20]):
    im = Image.open(os.path.join(OUT_DIR, fname)).resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    r = i // cols
    c = i % cols
    x = 16 + c * (thumb_w + 16)
    y = 16 + r * (thumb_h + 16)
    grid.paste(im, (x, y))
grid.save(os.path.join(ARTIFACT_DIR, "mosaico_20_posts_captoora.jpg"), quality=92)
print("✓ Mosaico actualizado con el Post #01 original en el primer cuadro")

# 3. Append Post #21 (Zócalo) to CANVA_BULK_CREATE_SHEETS_CAPTOORA.csv and BUFFER_AUTO_CADA_3_HORAS.csv
zocalo_caption = (
    "Caminar sobre el Zócalo en esta temporada es pisar el altar más grande del mundo. 🇲🇽🌼💀\n\n"
    "Cuenta la leyenda —y lo confirma la arqueología del INAH— que bajo esta plancha y la Catedral Metropolitana "
    "descansan miles de guerreros caídos en el asedio de 1521, el antiguo cementerio virreinal y las torres de cráneos "
    "del Huei Tzompantli de Tenochtitlan.\n\n"
    "Cuando el cielo se cierra, el asfalto mojado refleja la historia y el cempasúchil enciende la piedra, "
    "la cámara deja de tomar simples fotos: desentierra memoria.\n\n"
    "Para ser el dueño, amo y señor de la luz, primero tienes que saber leer la atmósfera.\n\n"
    "📍 Sesiones Editoriales y Documentales de Temporada — Agenda abierta por DM.\n\n"
    "#CaptooraStudio #DiaDeMuertos #ZocaloCDMX #FotografiaEditorial #Tenochtitlan #HueiTzompantli #MexicoMagico #AmoDeLaLuz"
)

# Read BUFFER_AUTO_CADA_3_HORAS.csv and update Post 01 + add Post 21
rows_buf = []
with open(CSV_BUFFER, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        if row["Post_ID"] == "01":
            row["Text"] = (
                "Para ser el dueño y amo y señor de la luz, primero tienes que dominar la oscuridad. 🌙✨🕯️\n\n"
                "En fotografía de alto nivel, las sombras y la penumbra no son ausencia de imagen: son el lienzo donde "
                "nace el volumen, el misterio y el carácter.\n\n"
                "📍 Captoora Studio — Momentos que permanecen. Reserva tu sesión de temporada por DM.\n\n"
                "#CaptooraStudio #MomentosQuePermanecen #AmoDeLaLuz #FotografiaDeAutor #Monterrey #DiaDeMuertos"
            )
        rows_buf.append(row)

if not any(r["Post_ID"] == "21" for r in rows_buf):
    rows_buf.append({
        "Text": zocalo_caption,
        "Image_URL_or_Local_Path": os.path.join(OUT_DIR, "POST_21_TEMPORADA_ZOCALO_TUMBA_GUERREROS.jpg"),
        "Scheduled_At": "2026-10-18 06:00",
        "Category": "4. Campañas de Temporada",
        "Post_ID": "21"
    })

with open(CSV_BUFFER, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows_buf)

print("✓ CSV de Buffer actualizado con Post #01 original y Post #21 del Zócalo")
