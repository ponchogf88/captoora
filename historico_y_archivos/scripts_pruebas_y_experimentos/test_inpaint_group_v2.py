import cv2
import numpy as np
from PIL import Image, ImageEnhance

img = cv2.imread("/private/tmp/farmasi_samples/group_editorial_crop.jpg")
h, w, _ = img.shape

inpaint_mask = np.zeros((h, w), dtype=np.uint8)

# Right clutter (including top right wall above Model 4 head)
# Model 4 head is at x=410, y=100. The wall is x > 460 for y < 100, and x > 490 for y < 250, and x > 510 for y < 380
pts_right = np.array([
    [465, 0], [w, 0], [w, h], [540, h],
    [540, 390], [510, 260], [480, 120], [465, 0]
], dtype=np.int32)
cv2.fillPoly(inpaint_mask, [pts_right], 255)

# Left clutter (door)
pts_door = np.array([[0, 0], [55, 0], [45, 320], [0, 320]], dtype=np.int32)
cv2.fillPoly(inpaint_mask, [pts_door], 255)

# Floor bottom edges
pts_bot_right = np.array([[520, 390], [w, 390], [w, h], [520, h]], dtype=np.int32)
cv2.fillPoly(inpaint_mask, [pts_bot_right], 255)
pts_bot_left = np.array([[0, 380], [50, 380], [35, h], [0, h]], dtype=np.int32)
cv2.fillPoly(inpaint_mask, [pts_bot_left], 255)

# Studio background gradient
Y, X = np.ogrid[:h, :w]
dist = np.sqrt(((X - w * 0.45) / (w * 0.7)) ** 2 + ((Y - h * 0.22) / (h * 0.6)) ** 2)
bg_l = np.clip(246.0 - dist * 20.0, 226.0, 246.0).astype(np.uint8)

studio_bg = np.zeros((h, w, 3), dtype=np.uint8)
studio_bg[:, :, 0] = np.clip(bg_l.astype(int) - 1, 0, 255).astype(np.uint8)
studio_bg[:, :, 1] = bg_l
studio_bg[:, :, 2] = np.clip(bg_l.astype(int) + 1, 0, 255).astype(np.uint8)

mask_float = inpaint_mask.astype(np.float32) / 255.0
mask_smooth = cv2.GaussianBlur(mask_float, (25, 25), 0)
mask_3c = np.repeat(mask_smooth[:, :, np.newaxis], 3, axis=2)

result = (studio_bg.astype(np.float32) * mask_3c + img.astype(np.float32) * (1.0 - mask_3c)).astype(np.uint8)

pil_res = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
enh_con = ImageEnhance.Contrast(pil_res)
pil_res = enh_con.enhance(1.08)

enh_sh = ImageEnhance.Sharpness(pil_res)
pil_res = enh_sh.enhance(1.15)

pil_res.save("/private/tmp/farmasi_samples/group_CPT_0845_FINAL.jpg", quality=95)
print("Saved /private/tmp/farmasi_samples/group_CPT_0845_FINAL.jpg")
