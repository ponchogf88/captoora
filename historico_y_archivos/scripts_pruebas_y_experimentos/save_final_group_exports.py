import cv2
from PIL import Image, ImageEnhance
import os

img_bgr = cv2.imread("/private/tmp/farmasi_samples/group_editorial_clean_test.jpg")
pil_img = Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
img_w, img_h = pil_img.size

# 1. Master High Res
hq_path = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/01_Alta_Resolucion_Cliente/FARMASI_CPT_0845_GRUPAL_HQ.jpg"
pil_img.save(hq_path, quality=96, optimize=True)
print(f"Saved HQ ({img_w}x{img_h}): {hq_path}")

# 2. Instagram 4x5 (1080 x 1350)
target_w, target_h = 1080, 1350
scale = target_w / float(img_w)
new_w = target_w
new_h = int(img_h * scale)
resized_4x5 = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

canvas_4x5 = Image.new("RGB", (target_w, target_h), (245, 245, 245))
offset_y = (target_h - new_h) // 2
canvas_4x5.paste(resized_4x5, (0, offset_y))
path_4x5 = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/02_Redes_Instagram_4x5/FARMASI_CPT_0845_GRUPAL_4x5.jpg"
canvas_4x5.save(path_4x5, quality=95)
print(f"Saved 4x5: {path_4x5}")

# 3. Instagram Story / Reels 9x16 (1080 x 1920)
target_sw, target_sh = 1080, 1920
scale_s = target_sw / float(img_w)
new_sw = target_sw
new_sh = int(img_h * scale_s)
resized_9x16 = pil_img.resize((new_sw, new_sh), Image.Resampling.LANCZOS)

canvas_9x16 = Image.new("RGB", (target_sw, target_sh), (242, 242, 242))
offset_sy = (target_sh - new_sh) // 2
canvas_9x16.paste(resized_9x16, (0, offset_sy))
path_9x16 = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/03_Stories_Reels_9x16/FARMASI_CPT_0845_GRUPAL_9x16.jpg"
canvas_9x16.save(path_9x16, quality=95)
print(f"Saved 9x16: {path_9x16}")

# Sync to Google Drive
drive_dir = "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026/ENTREGA_RETOQUE_STUDIO_V3"
os.system(f'cp "{hq_path}" "{drive_dir}/01_Alta_Resolucion_Cliente/"')
os.system(f'cp "{path_4x5}" "{drive_dir}/02_Redes_Instagram_4x5/"')
os.system(f'cp "{path_9x16}" "{drive_dir}/03_Stories_Reels_9x16/"')
print("Successfully synced to Google Drive!")
