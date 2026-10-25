import cv2
import numpy as np
from PIL import Image, ImageOps, ImageEnhance

def studio_retouch_cyclorama(img_path, output_path):
    # Load image
    orig = Image.open(img_path)
    orig = ImageOps.exif_transpose(orig)
    w, h = orig.size
    
    # Convert to RGB numpy
    img_rgb = np.array(orig.convert("RGB"))
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    
    # 1. Exposure & Contrast curve (S-Curve & brightness)
    # Convert to LAB for luminance adjustment without color shift
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE or gentle gamma curve to L channel
    # Gentle lift of midtones: gamma = 0.88 (brightens slightly)
    inv_gamma = 1.0 / 0.88
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    l_boosted = cv2.LUT(l, table)
    
    lab_boosted = cv2.merge((l_boosted, a, b))
    img_lifted = cv2.cvtColor(lab_boosted, cv2.COLOR_LAB2BGR)
    
    # 2. Identify the backdrop (high lightness, low chroma)
    # Background in studio is bright (>160 luminance) and relatively neutral (|a-128| < 15, |b-128| < 18)
    a_diff = np.abs(a.astype(int) - 128)
    b_diff = np.abs(b.astype(int) - 128)
    
    # Backdrop mask: high lightness, low saturation, mostly upper and mid regions
    backdrop_candidate = (l > 150) & (a_diff < 14) & (b_diff < 18)
    
    # Create a smooth blurred version of the background to dissolve fabric wrinkles
    # Large bilateral or gaussian blur
    bg_smoothed = cv2.bilateralFilter(img_lifted, d=15, sigmaColor=40, sigmaSpace=40)
    bg_smoothed = cv2.GaussianBlur(bg_smoothed, (35, 35), 0)
    
    # Distance transform or soft blending mask
    mask_float = backdrop_candidate.astype(np.float32)
    
    # Exclude the floor shadow zone directly near the feet/floor (bottom 15% should preserve shadow)
    # Let shadow areas retain original texture and depth
    # Floor contact shadow is where l is slightly lower (100 < l < 180) near the bottom
    floor_y_start = int(h * 0.75)
    shadow_mask = np.zeros_like(mask_float)
    shadow_mask[floor_y_start:, :] = (l[floor_y_start:, :] < 195).astype(np.float32)
    
    # Reduce backdrop smoothing where shadows live to preserve contact
    mask_float = np.clip(mask_float - (shadow_mask * 0.85), 0, 1)
    
    # Blur mask for ultra smooth transition (no halos)
    mask_blur = cv2.GaussianBlur(mask_float, (31, 31), 0)
    mask_3c = np.repeat(mask_blur[:, :, np.newaxis], 3, axis=2)
    
    # Blend smoothed backdrop with lifted image
    # Note: blend smoothly, keeping a 70% smoothed background, 30% original texture so it feels like real studio cyclorama
    retouched_bgr = (bg_smoothed * (mask_3c * 0.75) + img_lifted * (1.0 - (mask_3c * 0.75))).astype(np.uint8)
    
    # Convert back to PIL for final sharpness & subtle warm color grade
    result_pil = Image.fromarray(cv2.cvtColor(retouched_bgr, cv2.COLOR_BGR2RGB))
    
    # Micro sharpness for eyes, hair, jewelry
    enhancer_sh = ImageEnhance.Sharpness(result_pil)
    result_pil = enhancer_sh.enhance(1.15)
    
    # Subtle color vibrance
    enhancer_c = ImageEnhance.Color(result_pil)
    result_pil = enhancer_c.enhance(1.05)
    
    result_pil.save(output_path, quality=95, optimize=True)
    print(f"Saved: {output_path}")

studio_retouch_cyclorama("/private/tmp/farmasi_samples/preview_0550.jpg", "/private/tmp/farmasi_samples/retouched_0550.jpg")
studio_retouch_cyclorama("/private/tmp/farmasi_samples/preview_CPT_0800.JPG", "/private/tmp/farmasi_samples/retouched_0800.jpg")
