import os
from PIL import Image, ImageDraw, ImageOps

BASE = "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO"
ARTIFACT_DIR = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280"

selected = []
for root, dirs, files in os.walk(BASE):
    imgs = [f for f in sorted(files) if f.lower().endswith(('.jpg', '.jpeg', '.png')) and not f.startswith('.')]
    if imgs:
        # Take up to 2 representative images from each folder
        step = max(1, len(imgs) // 2)
        for f in imgs[::step][:2]:
            selected.append(os.path.join(root, f))

print(f"Sampled {len(selected)} images across all portfolio folders")
cols = 6
rows = (len(selected) + cols - 1) // cols
tw, th = 260, 260
sheet = Image.new("RGB", (cols * tw, rows * th), (15, 15, 20))
draw = ImageDraw.Draw(sheet)

with open("/Users/user/Desktop/Projects/CAPTOORA.STUDIO/sampled_portfolio.txt", "w") as out_f:
    for idx, p in enumerate(selected):
        out_f.write(f"{idx}\t{p}\n")
        try:
            im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
            im.thumbnail((tw - 10, th - 30))
            r = idx // cols
            c = idx % cols
            sheet.paste(im, (c * tw + 5, r * th + 5))
            folder = os.path.basename(os.path.dirname(p))[:14]
            fname = os.path.basename(p)[:12]
            draw.rectangle([(c * tw, (r + 1) * th - 24), ((c + 1) * tw, (r + 1) * th)], fill=(0, 0, 0))
            draw.text((c * tw + 6, (r + 1) * th - 20), f"S{idx}: {folder}/{fname}", fill=(100, 255, 180))
        except Exception as e:
            pass

sheet.save(os.path.join(ARTIFACT_DIR, "portfolio_folders_sampled.jpg"), quality=88)
print("Saved portfolio_folders_sampled.jpg")
