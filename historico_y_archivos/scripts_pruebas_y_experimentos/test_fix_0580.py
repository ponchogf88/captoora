import cv2
import numpy as np
from PIL import Image, ImageEnhance

raw_file = "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026/CPT_0580.JPG"
img = cv2.imread(raw_file)
h, w, _ = img.shape
print(f"Loaded 0580: {w}x{h}")

# Relight
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
l, a, b = cv2.split(lab)
x = np.arange(256, dtype=np.float32)
curve = np.clip(255.0 * np.power(x / 255.0, 0.88), 0, 255).astype(np.uint8)
l_lifted = cv2.LUT(l, curve)
relit = cv2.cvtColor(cv2.merge((l_lifted, a, b)), cv2.COLOR_LAB2BGR)

# Studio background
Y, X = np.ogrid[:h, :w]
dist = np.sqrt(((X - w * 0.45) / (w * 0.7)) ** 2 + ((Y - h * 0.25) / (h * 0.6)) ** 2)
bg_l = np.clip(246.0 - dist * 18.0, 230.0, 246.0).astype(np.uint8)
studio_bg = np.zeros((h, w, 3), dtype=np.uint8)
studio_bg[:, :, 0] = np.clip(bg_l.astype(int) - 1, 0, 255).astype(np.uint8)
studio_bg[:, :, 1] = bg_l
studio_bg[:, :, 2] = np.clip(bg_l.astype(int) + 1, 0, 255).astype(np.uint8)

# Clutter / Backdrop fold mask
# Tere is roughly centered from x=2000 to x=4800, y=800 to h
# Backdrop folds on left (x < 1800) and right (x > 5000)
mask_fold = np.zeros((h, w), dtype=np.uint8)
# Left backdrop
pts_l = np.array([[0, 0], [1800, 0], [1700, h], [0, h]], dtype=np.int32)
cv2.fillPoly(mask_fold, [pts_l], 255)
# Right backdrop
pts_r = np.array([[5100, 0], [w, 0], [w, h], [5000, h]], dtype=np.int32)
cv2.fillPoly(mask_fold, [pts_r], 255)

mask_f = mask_fold.astype(np.float32) / 255.0
mask_smooth = cv2.GaussianBlur(mask_f, (91, 91), 0)
mask_3c = np.repeat(mask_smooth[:, :, np.newaxis], 3, axis=2)

out = (studio_bg.astype(np.float32) * mask_3c + relit.astype(np.float32) * (1.0 - mask_3c)).astype(np.uint8)

# Arm blemish removal on right upper arm:
# Let's inspect where the arm blemish is on CPT_0580
# Crop arm area to inspect
arm_crop = out[1800:3200, 3200:4600]
cv2.imwrite("/private/tmp/farmasi_samples/arm_crop_0580.jpg", arm_crop)
print("Saved arm crop to /private/tmp/farmasi_samples/arm_crop_0580.jpg")
