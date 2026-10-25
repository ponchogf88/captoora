import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os

raw_file = "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026/CPT_0845.JPG"
img = cv2.imread(raw_file)
h, w, _ = img.shape
print(f"Loaded: {w}x{h}")

# Step 1: Relight midtones and skin (+0.35 EV)
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
l, a, b = cv2.split(lab)
x = np.arange(256, dtype=np.float32)
curve = np.clip(255.0 * np.power(x / 255.0, 0.88), 0, 255).astype(np.uint8)
l_lifted = cv2.LUT(l, curve)

# Desaturate yellow cast in highlights
b_adj = b.astype(np.float32)
warm_mask = (b > 135) & (l > 130)
b_adj[warm_mask] = b_adj[warm_mask] * 0.94
b_adj = np.clip(b_adj, 0, 255).astype(np.uint8)

relit = cv2.cvtColor(cv2.merge((l_lifted, a, b_adj)), cv2.COLOR_LAB2BGR)

# Step 2: Build synthetic studio cyclorama
Y, X = np.ogrid[:h, :w]
dist = np.sqrt(((X - w * 0.46) / (w * 0.72)) ** 2 + ((Y - h * 0.22) / (h * 0.65)) ** 2)
bg_l = np.clip(246.0 - dist * 22.0, 226.0, 246.0).astype(np.uint8)

studio_bg = np.zeros((h, w, 3), dtype=np.uint8)
studio_bg[:, :, 0] = np.clip(bg_l.astype(int) - 1, 0, 255).astype(np.uint8)
studio_bg[:, :, 1] = bg_l
studio_bg[:, :, 2] = np.clip(bg_l.astype(int) + 1, 0, 255).astype(np.uint8)

# Step 3: Define Clutter Mask (door on left, wall/lamp/stairs on right, power strip)
clutter_mask = np.zeros((h, w), dtype=np.uint8)

# Left door
pts_left = np.array([
    [0, 0], [820, 0], [740, 2100], [520, 2400], [0, 2400]
], dtype=np.int32)
cv2.fillPoly(clutter_mask, [pts_left], 255)

# Left bottom under leg
pts_left_bot = np.array([
    [0, 3350], [680, 3350], [550, h], [0, h]
], dtype=np.int32)
cv2.fillPoly(clutter_mask, [pts_left_bot], 255)

# Right wall, lamp, stairs (contouring Model 4)
pts_right_top = np.array([
    [4280, 0], [w, 0], [w, 2700],
    [4520, 2700], [4420, 2200], [4340, 1500], [4280, 900], [4280, 0]
], dtype=np.int32)
cv2.fillPoly(clutter_mask, [pts_right_top], 255)

# Right power strip & cables behind Model 4 leg
pts_right_cables = np.array([
    [5250, 2900], [w, 2900], [w, h], [5050, h],
    [5180, 3600], [5250, 2900]
], dtype=np.int32)
cv2.fillPoly(clutter_mask, [pts_right_cables], 255)

# Smooth transition mask
mask_f = clutter_mask.astype(np.float32) / 255.0
mask_smooth = cv2.GaussianBlur(mask_f, (121, 121), 0)
mask_3c = np.repeat(mask_smooth[:, :, np.newaxis], 3, axis=2)

# Blend
extended = (studio_bg.astype(np.float32) * mask_3c + relit.astype(np.float32) * (1.0 - mask_3c)).astype(np.uint8)

# Step 4: Crop to balanced luxury composition (keeping all 4 models and all products)
# Crop bounding box: x from 250 to 5750, y from 120 to 3950
crop_x1, crop_x2 = 200, 5800
crop_y1, crop_y2 = 120, 3950
cropped = extended[crop_y1:crop_y2, crop_x1:crop_x2]
ch, cw, _ = cropped.shape

# Step 5: Mirror Reflection Sheen on Floor
refl_h = int(ch * 0.14)
contact_y = int(ch * 0.86)
sample_box = cropped[contact_y - refl_h:contact_y, :]
reflection = cv2.flip(sample_box, 0)
refl_specular = cv2.GaussianBlur(reflection, (31, 7), 0)

fade = np.linspace(0.24, 0.0, refl_h, dtype=np.float32)[:, np.newaxis]
fade_3c = np.repeat(np.repeat(fade[:, :, np.newaxis], cw, axis=1), 3, axis=2)

dest_y2 = min(ch, contact_y + refl_h)
actual_h = dest_y2 - contact_y
cropped_patch = cropped[contact_y:dest_y2, :].astype(np.float32)
refl_p = refl_specular[:actual_h, :].astype(np.float32)
fade_p = fade_3c[:actual_h, :]

cropped[contact_y:dest_y2, :] = np.clip(cropped_patch * (1.0 - fade_p * 0.45) + refl_p * fade_p, 0, 255).astype(np.uint8)

# Step 6: Polish
pil_out = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
enh_con = ImageEnhance.Contrast(pil_out)
pil_out = enh_con.enhance(1.06)
enh_sh = ImageEnhance.Sharpness(pil_out)
pil_out = enh_sh.enhance(1.16)

# Save Master High Res
hq_path = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/01_Alta_Resolucion_Cliente/FARMASI_CPT_0845_GRUPAL_HQ.jpg"
pil_out.save(hq_path, quality=95, optimize=True)
print(f"Saved HQ: {hq_path} ({pil_out.size})")

# Export 4x5 Instagram Post (1080 x 1350)
target_w, target_h = 1080, 1350
target_aspect = 4.0 / 5.0
img_w, img_h = pil_out.size
img_aspect = img_w / float(img_h)

# For group shot, fit horizontally with studio white margins top/bottom
scale_f = target_w / float(img_w)
new_w = target_w
new_h = int(img_h * scale_f)
resized = pil_out.resize((new_w, new_h), Image.Resampling.LANCZOS)

canvas_4x5 = Image.new("RGB", (target_w, target_h), (242, 242, 242))
offset_y = (target_h - new_h) // 2
canvas_4x5.paste(resized, (0, offset_y))
path_4x5 = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/02_Redes_Instagram_4x5/FARMASI_CPT_0845_GRUPAL_4x5.jpg"
canvas_4x5.save(path_4x5, quality=95)
print(f"Saved 4x5: {path_4x5}")

# Export 9x16 Story / Reel (1080 x 1920)
target_sw, target_sh = 1080, 1920
scale_s = target_sw / float(img_w)
new_sw = target_sw
new_sh = int(img_h * scale_s)
resized_s = pil_out.resize((new_sw, new_sh), Image.Resampling.LANCZOS)

canvas_9x16 = Image.new("RGB", (target_sw, target_sh), (240, 240, 240))
offset_sy = (target_sh - new_sh) // 2
canvas_9x16.paste(resized_s, (0, offset_sy))
path_9x16 = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/03_Stories_Reels_9x16/FARMASI_CPT_0845_GRUPAL_9x16.jpg"
canvas_9x16.save(path_9x16, quality=95)
print(f"Saved 9x16: {path_9x16}")

# Copy all 3 to Google Drive
drive_dir = "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026/ENTREGA_RETOQUE_STUDIO_V3"
os.system(f'cp "{hq_path}" "{drive_dir}/01_Alta_Resolucion_Cliente/"')
os.system(f'cp "{path_4x5}" "{drive_dir}/02_Redes_Instagram_4x5/"')
os.system(f'cp "{path_9x16}" "{drive_dir}/03_Stories_Reels_9x16/"')
print("Successfully synced to Google Drive!")
