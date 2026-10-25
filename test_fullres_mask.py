import cv2
import numpy as np

# Load full res or 1500x1000 for rapid mask prototyping
full_path = "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026/CPT_0845.JPG"
img = cv2.imread(full_path)
h, w, _ = img.shape # 4000, 6000

# Scale factor for prototype: 0.25 (1500 x 1000)
scale = 0.25
preview = cv2.resize(img, (int(w * scale), int(h * scale)))
ph, pw, _ = preview.shape

mask = np.zeros((ph, pw), dtype=np.uint8)

# 1. Left closet clutter
# In full res: (0,0) -> (780,0) -> (700, 2200) -> (450, 2400) -> (0, 2400)
pts_left_closet = np.array([
    [0, 0], [int(780*scale), 0], [int(700*scale), int(2200*scale)],
    [int(450*scale), int(2400*scale)], [0, int(2400*scale)]
], dtype=np.int32)
cv2.fillPoly(mask, [pts_left_closet], 255)

# Left bottom under leg
pts_left_bot = np.array([
    [0, int(3350*scale)], [int(650*scale), int(3350*scale)],
    [int(500*scale), ph], [0, ph]
], dtype=np.int32)
cv2.fillPoly(mask, [pts_left_bot], 255)

# 2. Right wall & lamp & stairs (above Model 3)
# Head of Model 3 ends at x ~ 4300, y ~ 1000
# Back of Model 3 curves down to (4450, 2600)
pts_right_wall = np.array([
    [int(4320*scale), 0], [pw, 0], [pw, int(2700*scale)],
    [int(4480*scale), int(2700*scale)],
    [int(4400*scale), int(2200*scale)],
    [int(4320*scale), int(1500*scale)],
    [int(4300*scale), int(900*scale)],
    [int(4320*scale), 0]
], dtype=np.int32)
cv2.fillPoly(mask, [pts_right_wall], 255)

# 3. Right power strip & equipment (behind/under Model 3 legs)
pts_power_strip = np.array([
    [int(5200*scale), int(2900*scale)], [pw, int(2900*scale)],
    [pw, ph], [int(5100*scale), ph],
    [int(5150*scale), int(3650*scale)],
    [int(5200*scale), int(2900*scale)]
], dtype=np.int32)
cv2.fillPoly(mask, [pts_power_strip], 255)

# Visual overlay: red on masked areas
overlay = preview.copy()
overlay[mask == 255] = overlay[mask == 255] * 0.3 + np.array([0, 0, 255]) * 0.7

cv2.imwrite("/private/tmp/farmasi_samples/mask_inspection_overlay.jpg", overlay)
print("Saved mask inspection overlay")
