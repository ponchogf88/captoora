import cv2
import numpy as np
from PIL import Image, ImageEnhance

def studio_backdrop_extension(img_path, output_path):
    img = cv2.imread(img_path)
    h, w, _ = img.shape
    
    # 1. Base portrait illumination & warm skin glow (Relighting without cutting)
    # Convert to LAB for pure luminance curve
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Gamma lift on midtones: brightens faces and products (+0.4 EV)
    x = np.arange(256, dtype=np.float32)
    curve = np.clip(255.0 * np.power(x / 255.0, 0.88), 0, 255).astype(np.uint8)
    l_lifted = cv2.LUT(l, curve)
    
    # Tone down excess yellow from wall reflection
    b_adj = b.astype(np.float32)
    warm_mask = (b > 135) & (l > 130)
    b_adj[warm_mask] = b_adj[warm_mask] * 0.95
    b_adj = np.clip(b_adj, 0, 255).astype(np.uint8)
    
    base = cv2.cvtColor(cv2.merge((l_lifted, a, b_adj)), cv2.COLOR_LAB2BGR)
    
    # 2. Build Studio Cyclorama Background
    # High-end studio gradient: center is clean white (245), falling off softly to pearl gray (230)
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt(((X - w * 0.46) / (w * 0.7)) ** 2 + ((Y - h * 0.25) / (h * 0.6)) ** 2)
    bg_l = np.clip(246.0 - dist * 22.0, 226.0, 246.0).astype(np.uint8)
    
    studio_bg = np.zeros((h, w, 3), dtype=np.uint8)
    studio_bg[:, :, 0] = np.clip(bg_l.astype(int) - 1, 0, 255).astype(np.uint8)
    studio_bg[:, :, 1] = bg_l
    studio_bg[:, :, 2] = np.clip(bg_l.astype(int) + 1, 0, 255).astype(np.uint8)
    
    # 3. Define the Clutter Replacement Mask (Where the room walls, door, and cables are)
    # Left clutter: Closet louvered door is strictly at x < 100, y < 450
    # Left floor edge: x < 70, y >= 450
    # Right clutter: Lamp, black shelf, staircase, yellow wall at x > 620, y < 350
    # Right floor clutter: Power strip, black shoe, tiles at x > 720, y >= 350
    
    clutter_mask = np.zeros((h, w), dtype=np.float32)
    
    # Left door area: polygon
    pts_left = np.array([[0, 0], [105, 0], [90, 320], [60, h], [0, h]], dtype=np.int32)
    cv2.fillPoly(clutter_mask, [pts_left], 1.0)
    
    # Right wall & furniture area: polygon
    pts_right = np.array([
        [600, 0], [w, 0], [w, h], [730, h], 
        [715, 390], [620, 260], [600, 100]
    ], dtype=np.int32)
    cv2.fillPoly(clutter_mask, [pts_right], 1.0)
    
    # Floor seam and wrinkles (outside the models):
    # Smooth the floor plastic tape lines on the left and right borders
    pts_floor_left = np.array([[0, int(h*0.75)], [140, int(h*0.75)], [100, h], [0, h]], dtype=np.int32)
    cv2.fillPoly(clutter_mask, [pts_floor_left], 1.0)
    
    # Protect Model 1 hand (top left): Model 1 hand holding purple jar is around x=200-280, y=110-180 (far away from x=105)
    # Protect Model 4 arm/back (right): Model 4 is at x=610-670, y=140-300
    # Let us refine the right mask so it cuts right behind Model 4 arm:
    # Model 4 back silhouette: between x=620 and x=660
    
    # Soft feather the clutter mask heavily so it transitions invisibly into the existing white sheet!
    mask_blurred = cv2.GaussianBlur(clutter_mask, (41, 41), 0)
    mask_3c = np.repeat(mask_blurred[:, :, np.newaxis], 3, axis=2)
    
    # 4. Also smooth the existing center white fabric wrinkles
    # The center fabric is between x=100 and x=600, y < 350
    # Apply bilateral smoothing exclusively to high-luminance, low-saturation backdrop pixels
    a_diff = np.abs(a.astype(int) - 128)
    b_diff = np.abs(b.astype(int) - 128)
    is_center_cloth = (l > 155) & (a_diff < 15) & (b_diff < 18) & (X > 90) & (X < 620) & (Y < 350)
    
    # Erode cloth mask so it stays away from hair
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    safe_cloth = cv2.erode(is_center_cloth.astype(np.uint8), kernel)
    cloth_feather = cv2.GaussianBlur(safe_cloth.astype(np.float32), (25, 25), 0)
    
    smooth_base = cv2.bilateralFilter(base, d=21, sigmaColor=60, sigmaSpace=60)
    smooth_base = cv2.GaussianBlur(smooth_base, (25, 25), 0)
    
    # Blend cloth smoothing into base
    cloth_3c = np.repeat(cloth_feather[:, :, np.newaxis], 3, axis=2)
    base_smoothed = (smooth_base * cloth_3c + base * (1.0 - cloth_3c)).astype(np.uint8)
    
    # 5. Composite: replace clutter with synthetic studio background
    out = (studio_bg.astype(np.float32) * mask_3c + base_smoothed.astype(np.float32) * (1.0 - mask_3c)).astype(np.uint8)
    
    # 6. Add glossy floor reflection onto the bottom
    contact_y = int(h * 0.85)
    refl_h = int(h * 0.15)
    sample_box = out[contact_y - refl_h:contact_y, :]
    reflection = cv2.flip(sample_box, 0)
    refl_specular = cv2.GaussianBlur(reflection, (15, 3), 0)
    
    fade = np.linspace(0.25, 0.0, refl_h, dtype=np.float32)[:, np.newaxis]
    fade_3c = np.repeat(np.repeat(fade[:, :, np.newaxis], w, axis=1), 3, axis=2)
    
    dest_y2 = min(h, contact_y + refl_h)
    act_h = dest_y2 - contact_y
    out_patch = out[contact_y:dest_y2, :].astype(np.float32)
    refl_p = refl_specular[:act_h, :].astype(np.float32)
    fade_p = fade_3c[:act_h, :]
    
    out[contact_y:dest_y2, :] = np.clip(out_patch * (1.0 - fade_p * 0.5) + refl_p * fade_p, 0, 255).astype(np.uint8)
    
    # 7. Final Polish
    pil_img = Image.fromarray(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
    enh_sh = ImageEnhance.Sharpness(pil_img)
    pil_img = enh_sh.enhance(1.15)
    
    enh_c = ImageEnhance.Color(pil_img)
    pil_img = enh_c.enhance(1.04)
    
    pil_img.save(output_path, quality=95, optimize=True)
    print(f"Saved: {output_path}")

studio_backdrop_extension("/private/tmp/farmasi_samples/group_CPT_0845.JPG.jpg", "/private/tmp/farmasi_samples/outpainted_0845.jpg")
