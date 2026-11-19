import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os

# Load original high-res image 6000x4000
raw_file = "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026/CPT_0845.JPG"
img = cv2.imread(raw_file)
h, w, _ = img.shape # 4000, 6000

# 1. Relight midtones and skin (+0.35 EV)
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
l, a, b = cv2.split(lab)
x = np.arange(256, dtype=np.float32)
curve = np.clip(255.0 * np.power(x / 255.0, 0.88), 0, 255).astype(np.uint8)
l_lifted = cv2.LUT(l, curve)

# Tone down yellow cast
b_adj = b.astype(np.float32)
warm_mask = (b > 135) & (l > 130)
b_adj[warm_mask] = b_adj[warm_mask] * 0.94
b_adj = np.clip(b_adj, 0, 255).astype(np.uint8)
relit = cv2.cvtColor(cv2.merge((l_lifted, a, b_adj)), cv2.COLOR_LAB2BGR)

# 2. Studio Infinity Backdrop (White / soft warm pearl)
Y, X = np.ogrid[:h, :w]
dist = np.sqrt(((X - w * 0.46) / (w * 0.72)) ** 2 + ((Y - h * 0.22) / (h * 0.65)) ** 2)
bg_l = np.clip(246.0 - dist * 20.0, 228.0, 246.0).astype(np.uint8)

studio_bg = np.zeros((h, w, 3), dtype=np.uint8)
studio_bg[:, :, 0] = np.clip(bg_l.astype(int) - 1, 0, 255).astype(np.uint8)
studio_bg[:, :, 1] = bg_l
studio_bg[:, :, 2] = np.clip(bg_l.astype(int) + 1, 0, 255).astype(np.uint8)

# 3. Precision Mask to remove ALL room clutter, stands, blue cloths and door slats
clutter_mask = np.zeros((h, w), dtype=np.uint8)

# Left door: generous polygon covering all slats up to fabric
pts_left = np.array([
    [0, 0], [950, 0], [860, 2100], [520, 2400], [0, 2400]
], dtype=np.int32)
cv2.fillPoly(clutter_mask, [pts_left], 255)

# Left bottom under leg
pts_left_bot = np.array([
    [0, 3350], [680, 3350], [550, h], [0, h]
], dtype=np.int32)
cv2.fillPoly(clutter_mask, [pts_left_bot], 255)

# Right wall, lamp, stairs, AND blue cloth behind Model 4:
# Model 4 back silhouette is at x ~ 4320-4480.
# The blue cloth is between x = 4220 and 4400, y = 1200-1800!
# We trace right along Model 4 hair/shoulder/back:
pts_right = np.array([
    [4240, 0], [w, 0], [w, 2750],
    [4520, 2750], [4440, 2200], [4360, 1650], [4260, 1200],
    [4200, 750], [4240, 0]
], dtype=np.int32)
cv2.fillPoly(clutter_mask, [pts_right], 255)

# Floor: smooth tiles across the entire bottom while preserving the products
# Product bounding box: x from 600 to 4700, y from 2850 to 3800
# Below y = 3800 is bare tile and wrinkled cellophane!
pts_floor_bottom = np.array([
    [0, 3800], [w, 3800], [w, h], [0, h]
], dtype=np.int32)
cv2.fillPoly(clutter_mask, [pts_floor_bottom], 255)

# Right corner clutter (power strip, bags, shoes):
pts_right_bot = np.array([
    [4850, 2800], [w, 2800], [w, h], [4850, h]
], dtype=np.int32)
cv2.fillPoly(clutter_mask, [pts_right_bot], 255)

# Smooth transition mask
mask_f = clutter_mask.astype(np.float32) / 255.0
mask_smooth = cv2.GaussianBlur(mask_f, (91, 91), 0)
mask_3c = np.repeat(mask_smooth[:, :, np.newaxis], 3, axis=2)

extended = (studio_bg.astype(np.float32) * mask_3c + relit.astype(np.float32) * (1.0 - mask_3c)).astype(np.uint8)

# 4. Crop to clean, balanced fashion editorial (eliminating right foot/power strip clutter)
# x from 380 to 4820, y from 80 to 3880
crop = extended[80:3880, 380:4820]
ch, cw, _ = crop.shape

# 5. Mirror floor reflection sheen on bottom
refl_h = int(ch * 0.12)
contact_y = int(ch * 0.88)
sample_box = crop[contact_y - refl_h:contact_y, :]
reflection = cv2.flip(sample_box, 0)
refl_specular = cv2.GaussianBlur(reflection, (35, 7), 0)

fade = np.linspace(0.22, 0.0, refl_h, dtype=np.float32)[:, np.newaxis]
fade_3c = np.repeat(np.repeat(fade[:, :, np.newaxis], cw, axis=1), 3, axis=2)

dest_y2 = min(ch, contact_y + refl_h)
actual_h = dest_y2 - contact_y
crop_patch = crop[contact_y:dest_y2, :].astype(np.float32)
refl_p = refl_specular[:actual_h, :].astype(np.float32)
fade_p = fade_3c[:actual_h, :]

crop[contact_y:dest_y2, :] = np.clip(crop_patch * (1.0 - fade_p * 0.4) + refl_p * fade_p, 0, 255).astype(np.uint8)

# 6. Polish
pil_out = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
enh_con = ImageEnhance.Contrast(pil_out)
pil_out = enh_con.enhance(1.06)
enh_sh = ImageEnhance.Sharpness(pil_out)
pil_out = enh_sh.enhance(1.15)

out_path = "/private/tmp/farmasi_samples/group_flaws_fixed_v3.jpg"
pil_out.save(out_path, quality=96)
print(f"Saved: {out_path} ({pil_out.size})")
