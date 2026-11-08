import cv2
import numpy as np
from PIL import Image, ImageOps, ImageEnhance

def studio_master_retouch(img_path, output_path):
    orig = Image.open(img_path)
    orig = ImageOps.exif_transpose(orig)
    w, h = orig.size
    
    img_rgb = np.array(orig.convert("RGB"))
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    
    # 1. White balance & exposure calibration
    c1 = img_bgr[10:int(h*0.15), 10:int(w*0.25)].reshape(-1, 3)
    c2 = img_bgr[10:int(h*0.15), int(w*0.75):w-10].reshape(-1, 3)
    corner_samples = np.vstack([c1, c2])
    mean_bg_bgr = np.mean(corner_samples, axis=0)
    
    # Target clean studio cyclorama: around (240, 242, 244)
    target_bg = np.array([238.0, 240.0, 243.0]) # B, G, R
    
    # Gain factors for background
    gains = target_bg / np.maximum(mean_bg_bgr, 50.0)
    gains = np.clip(gains, 1.0, 1.40)
    
    # 2. LAB luminance curve
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Backdrop mask: high lightness, low saturation
    a_diff = np.abs(a.astype(int) - 128)
    b_diff = np.abs(b.astype(int) - 128)
    
    bg_mask = (l > 140) & (a_diff < 16) & (b_diff < 22)
    floor_y = int(h * 0.82)
    
    # Apply background gains
    img_balanced = img_bgr.astype(np.float32)
    for c in range(3):
        img_balanced[:, :, c] = img_balanced[:, :, c] * gains[c]
    img_balanced = np.clip(img_balanced, 0, 255).astype(np.uint8)
    
    # Smooth background strongly to dissolve fabric folds
    bg_smooth = cv2.bilateralFilter(img_balanced, d=21, sigmaColor=60, sigmaSpace=60)
    bg_smooth = cv2.GaussianBlur(bg_smooth, (51, 51), 0)
    
    # Build soft mask
    mask_float = bg_mask.astype(np.float32)
    mask_float[l < 135] = 0.0
    
    # Protect floor contact shadow (feet area)
    floor_zone = mask_float[floor_y:, :]
    floor_l = l[floor_y:, :]
    floor_zone[floor_l < 210] = 0.0
    mask_float[floor_y:, :] = floor_zone
    
    mask_blur = cv2.GaussianBlur(mask_float, (45, 45), 0)
    mask_3c = np.repeat(mask_blur[:, :, np.newaxis], 3, axis=2)
    
    blended = (bg_smooth * (mask_3c * 0.85) + img_balanced * (1.0 - (mask_3c * 0.85))).astype(np.uint8)
    
    result_pil = Image.fromarray(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))
    
    enhancer_con = ImageEnhance.Contrast(result_pil)
    result_pil = enhancer_con.enhance(1.08)
    
    enhancer_sh = ImageEnhance.Sharpness(result_pil)
    result_pil = enhancer_sh.enhance(1.20)
    
    result_pil.save(output_path, quality=95, optimize=True)
    print(f"Saved v2: {output_path}")

studio_master_retouch("/private/tmp/farmasi_samples/preview_0550.jpg", "/private/tmp/farmasi_samples/retouched_v2_0550.jpg")
studio_master_retouch("/private/tmp/farmasi_samples/preview_CPT_0800.JPG", "/private/tmp/farmasi_samples/retouched_v2_0800.jpg")
studio_master_retouch("/private/tmp/farmasi_samples/preview_CPT_0750.JPG", "/private/tmp/farmasi_samples/retouched_v2_0750.jpg")
