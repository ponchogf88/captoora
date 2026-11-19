import os, glob
from PIL import Image, ImageDraw, ImageFont

PORT_DIR = "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA"
ARTIFACT_DIR = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280"

files = []
for root, dirs, fnames in os.walk(PORT_DIR):
    for f in sorted(fnames):
        if f.lower().endswith(('.jpg', '.jpeg', '.png')) and not f.startswith('.'):
            files.append(os.path.join(root, f))

print(f"Total portfolio images found: {len(files)}")
# Build a visual contact sheet of the first 36 images so we can see what's inside each photo!
cols = 6
rows = 6
tw, th = 260, 260
sheet = Image.new("RGB", (cols * tw, rows * th), (15, 15, 20))
draw = ImageDraw.Draw(sheet)

for idx, p in enumerate(files[:36]):
    try:
        im = Image.open(p).convert("RGB")
        im.thumbnail((tw - 10, th - 30))
        r = idx // cols
        c = idx % cols
        x = c * tw + 5
        y = r * th + 5
        sheet.paste(im, (x, y))
        short_name = os.path.basename(os.path.dirname(p))[:10] + "/" + os.path.basename(p)[:18]
        draw.rectangle([(c * tw, (r + 1) * th - 24), ((c + 1) * tw, (r + 1) * th)], fill=(0, 0, 0))
        draw.text((c * tw + 6, (r + 1) * th - 20), f"{idx}: {short_name}", fill=(255, 220, 100))
    except Exception as e:
        pass

sheet.save(os.path.join(ARTIFACT_DIR, "portfolio_sheet_1.jpg"), quality=88)

if len(files) > 36:
    sheet2 = Image.new("RGB", (cols * tw, rows * th), (15, 15, 20))
    draw2 = ImageDraw.Draw(sheet2)
    for idx, p in enumerate(files[36:72], start=36):
        try:
            im = Image.open(p).convert("RGB")
            im.thumbnail((tw - 10, th - 30))
            r = (idx - 36) // cols
            c = (idx - 36) % cols
            x = c * tw + 5
            y = r * th + 5
            sheet2.paste(im, (x, y))
            short_name = os.path.basename(os.path.dirname(p))[:10] + "/" + os.path.basename(p)[:18]
            draw2.rectangle([(c * tw, (r + 1) * th - 24), ((c + 1) * tw, (r + 1) * th)], fill=(0, 0, 0))
            draw2.text((c * tw + 6, (r + 1) * th - 20), f"{idx}: {short_name}", fill=(255, 220, 100))
        except Exception as e:
            pass
    sheet2.save(os.path.join(ARTIFACT_DIR, "portfolio_sheet_2.jpg"), quality=88)

with open("/Users/user/Desktop/Projects/CAPTOORA.STUDIO/portfolio_index.txt", "w") as f:
    for idx, p in enumerate(files):
        f.write(f"{idx}\t{p}\n")
print("Saved portfolio contact sheets")
