import cv2
import os
from PIL import Image

RAW_DIR = "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026"
ARTIFACT_DIR = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280"

for code in ["0845", "0550", "0580", "0630", "0700", "0750", "0800"]:
    im = Image.open(os.path.join(RAW_DIR, f"CPT_{code}.JPG"))
    im.thumbnail((1000, 1000))
    im.save(os.path.join(ARTIFACT_DIR, f"raw_check_{code}.jpg"), quality=85)
print("Saved raw checks")
