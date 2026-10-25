import cv2
import numpy as np
from PIL import Image, ImageEnhance

img = cv2.imread("/private/tmp/farmasi_samples/group_editorial_crop.jpg")
h, w, _ = img.shape

# Inpaint mask: where the lamp and door remnants are
inpaint_mask = np.zeros((h, w), dtype=np.uint8)

# Upper right lamp and wall (x > 500, y < 250 outside Model 4)
# Model 4 head is at x=370-440 (in cropped coords), back is at x=450-510
# So anything with x > 515 and y < 350 is lamp/staircase/wall!
pts_lamp = np.array([[505, 0], [w, 0], [w, 360], [520, 260], [505, 140]], dtype=np.int32)
cv2.fillPoly(inpaint_mask, [pts_lamp], 255)

# Upper left closet door remnants (x < 50, y < 300)
pts_door = np.array([[0, 0], [45, 0], [35, 300], [0, 300]], dtype=np.int32)
cv2.fillPoly(inpaint_mask, [pts_door], 255)

# Bottom right floor tile and black cable (x > 580, y > 380)
pts_tile = np.array([[590, 380], [w, 380], [w, h], [580, h]], dtype=np.int32)
cv2.fillPoly(inpaint_mask, [pts_tile], 255)

# Bottom left floor edge (x < 40, y > 380)
pts_bot_left = np.array([[0, 380], [40, 380], [30, h], [0, h]], dtype=np.int32)
cv2.fillPoly(inpaint_mask, [pts_bot_left], 255)

# Inpaint using Telea and Navier-Stokes or synthetic studio fill
# Better yet: create synthetic studio backdrop and blend smoothly in inpaint_mask!
Y, X = np.ogrid[:h, :w]
dist = np.sqrt(((X - w * 0.45) / (w * 0.7)) ** 2 + ((Y - h * 0.22) / (h * 0.6)) ** 2)
bg_l = np.clip(246.0 - dist * 22.0, 226.0, 246.0).astype(np.uint8)

studio_bg = np.zeros((h, w, 3), dtype=np.uint8)
studio_bg[:, :, 0] = np.clip(bg_l.astype(int) - 1, 0, 255).astype(np.uint8)
studio_bg[:, :, 1] = bg_l
studio_bg[:, :, 2] = np.clip(bg_l.astype(int) + 1, 0, 255).astype(np.uint8)

mask_float = inpaint_mask.astype(np.float32) / 255.0
mask_smooth = cv2.GaussianBlur(mask_float, (31, 31), 0)
mask_3c = np.repeat(mask_smooth[:, :, np.newaxis], 3, axis=2)

result = (studio_bg.astype(np.float32) * mask_3c + img.astype(np.float32) * (1.0 - mask_3c)).astype(np.uint8)

# Subtle skin warming and contrast
pil_res = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
enh_con = ImageEnhance.Contrast(pil_res)
pil_res = enh_con.enhance(1.08)

enh_sh = ImageEnhance.Sharpness(pil_res)
pil_res = enh_sh.enhance(1.15)

pil_res.save("/private/tmp/farmasi_samples/group_CPT_0845_PERFECT.jpg", quality=95)
print("Saved /private/tmp/farmasi_samples/group_CPT_0845_PERFECT.jpg")
