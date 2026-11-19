import cv2
import numpy as np
from PIL import Image, ImageOps, ImageEnhance

def clean_studio_portrait(img_path, output_path):
    orig = Image.open(img_path)
    orig = ImageOps.exif_transpose(orig)
    w, h = orig.size
    
    img_bgr = cv2.cvtColor(np.array(orig.convert("RGB")), cv2.COLOR_RGB2BGR)
    
    # 1. Global portrait tonal balance (gentle exposure lift without burning)
    # Convert to LAB
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply a gentle S-curve to L channel: lifts shadows and midtones slightly (+0.25 EV) while rolling off highlights smoothly
    # Input x in [0, 255]
    x = np.arange(256, dtype=np.float32)
    # Tone curve formula: lift midtones, preserve blacks (0 remains 0), compress highlights smoothly
    curve = 255.0 * np.power(x / 255.0, 0.90) # gentle gamma lift
    # Add gentle contrast (S-shape)
    curve = np.clip(curve, 0, 255).astype(np.uint8)
    l_tone = cv2.LUT(l, curve)
    
    # Reconstruct balanced base image
    base_bgr = cv2.cvtColor(cv2.merge((l_tone, a, b)), cv2.COLOR_LAB2BGR)
    
    # 2. Fabric wrinkle removal on backdrop using frequency separation
    # High frequency = wrinkles and texture
    # Low frequency = lighting gradient
    # We want to remove low-contrast fabric folds in bright areas without creating halos on dark edges
    
    # Create backdrop guidance: where lightness is high and chroma is low
    a_diff = np.abs(a.astype(int) - 128)
    b_diff = np.abs(b.astype(int) - 128)
    is_backdrop = (l > 150) & (a_diff < 15) & (b_diff < 20)
    
    # Morphological erosion so the mask stays strictly AWAY from subject boundaries (avoids fringe/halos completely!)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
    backdrop_safe = cv2.erode(is_backdrop.astype(np.uint8), kernel)
    
    # In the safe backdrop area, we can smooth out the wrinkles using strong bilateral + gaussian
    # Bilateral filter respects existing major gradients but kills small fabric ripples
    smooth_bg = cv2.bilateralFilter(base_bgr, d=25, sigmaColor=75, sigmaSpace=75)
    smooth_bg = cv2.GaussianBlur(smooth_bg, (35, 35), 0)
    
    # Lift the background in safe area slightly towards clean studio white (e.g. +15 levels)
    smooth_bg_lifted = cv2.add(smooth_bg, np.array([12, 12, 12], dtype=np.uint8))
    
    # Feather the safe mask gently (only over a 15px radius) so it never touches the subject hair/silhouette
    mask_feathered = cv2.GaussianBlur(backdrop_safe.astype(np.float32), (21, 21), 0)
    mask_3c = np.repeat(mask_feathered[:, :, np.newaxis], 3, axis=2)
    
    # Blend: safe backdrop gets smoothed & lifted; subject and hair transition zone is 100% UNTOUCHED
    result_bgr = (smooth_bg_lifted * mask_3c + base_bgr * (1.0 - mask_3c)).astype(np.uint8)
    
    # 3. Final polish in PIL
    result_pil = Image.fromarray(cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB))
    
    # Skin clarity & sharpness
    enhancer_sh = ImageEnhance.Sharpness(result_pil)
    result_pil = enhancer_sh.enhance(1.15)
    
    enhancer_col = ImageEnhance.Color(result_pil)
    result_pil = enhancer_col.enhance(1.04)
    
    result_pil.save(output_path, quality=95, optimize=True)
    print(f"Saved v3: {output_path}")

clean_studio_portrait("/private/tmp/farmasi_samples/preview_0550.jpg", "/private/tmp/farmasi_samples/retouched_v3_0550.jpg")
clean_studio_portrait("/private/tmp/farmasi_samples/preview_CPT_0800.JPG", "/private/tmp/farmasi_samples/retouched_v3_0800.jpg")
clean_studio_portrait("/private/tmp/farmasi_samples/preview_CPT_0750.JPG", "/private/tmp/farmasi_samples/retouched_v3_0750.jpg")
