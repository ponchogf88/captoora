import os, glob
from PIL import Image, ImageDraw, ImageOps

DIRS = [
    "/Users/user/Desktop/Projects/SESSIONS PORTAFOLIO",
    "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026",
    "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/POSTS",
    "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/CAMARA/BRAND/MEDIA KIT",
]
ARTIFACT_DIR = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280"

valid_files = []
for d in DIRS:
    if not os.path.exists(d):
        continue
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f)
        if os.path.isfile(p) and f.lower().endswith(('.jpg', '.jpeg', '.png')) and os.path.getsize(p) > 25000:
            try:
                im = Image.open(p)
                im.verify()
                valid_files.append(p)
            except Exception:
                pass

print(f"Found {len(valid_files)} materialized valid high-res photos")
cols = 6
rows = min(8, (len(valid_files) + cols - 1) // cols)
tw, th = 260, 260
sheet = Image.new("RGB", (cols * tw, rows * th), (14, 15, 20))
draw = ImageDraw.Draw(sheet)

with open("/Users/user/Desktop/Projects/CAPTOORA.STUDIO/valid_photos.txt", "w") as out_f:
    for idx, p in enumerate(valid_files[:48]):
        out_f.write(f"{idx}\t{p}\n")
        im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        im.thumbnail((tw - 10, th - 28))
        r = idx // cols
        c = idx % cols
        sheet.paste(im, (c * tw + 5, r * th + 5))
        draw.rectangle([(c * tw, (r + 1) * th - 22), ((c + 1) * tw, (r + 1) * th)], fill=(0, 0, 0))
        draw.text((c * tw + 6, (r + 1) * th - 19), f"#{idx}: {os.path.basename(p)[:18]}", fill=(255, 215, 80))

sheet.save(os.path.join(ARTIFACT_DIR, "valid_portfolio_sheet.jpg"), quality=88)
