import cv2
import numpy as np
from PIL import Image, ImageOps, ImageEnhance

def clean_group_cyclorama(img_path, output_path):
    img = cv2.imread(img_path)
    h, w, _ = img.shape
    
    # 1. Build a synthetic professional studio cyclorama background of size (h, w)
    # A luxury studio gradient: bright center-top, soft falloff to edges and bottom
    Y, X = np.ogrid[:h, :w]
    # Center of light: x = w*0.48, y = h*0.25
    dist_from_light = np.sqrt(((X - w * 0.48) / (w * 0.7)) ** 2 + ((Y - h * 0.25) / (h * 0.6)) ** 2)
    # Background brightness from 244 at center down to 226 at corners
    bg_l = np.clip(245.0 - dist_from_light * 25.0, 222.0, 245.0)
    
    # Add subtle studio floor gradient (horizon around y = h * 0.65)
    horizon_y = int(h * 0.62)
    floor_dist = (Y - horizon_y).astype(np.float32)
    floor_mask = (Y >= horizon_y).astype(np.float32)
    # Floor is slightly warmer / reflective white
    bg_l = bg_l * (1.0 - floor_mask) + (bg_l - floor_dist * 0.03) * floor_mask
    bg_l = np.clip(bg_l, 218.0, 246.0).astype(np.uint8)
    
    # Clean neutral studio gray-white in BGR
    # R=bg_l, G=bg_l, B=bg_l-2 (slight warm pearl tone)
    bg_studio = np.zeros((h, w, 3), dtype=np.uint8)
    bg_studio[:, :, 0] = np.clip(bg_l.astype(int) - 1, 0, 255).astype(np.uint8) # B
    bg_studio[:, :, 1] = bg_l # G
    bg_studio[:, :, 2] = np.clip(bg_l.astype(int) + 1, 0, 255).astype(np.uint8) # R
    
    # 2. Segment the subject bounding area
    # In CPT_0845:
    # Subject bounding box roughly: x from 90 to 710, y from 60 to h-20
    # Clutter on left is x < 85 (louvered closet door)
    # Clutter on right is x > 710 (lamp, shelf, power strip)
    # Upper corners: x < 120 and y < 350 is left door; x > 560 and y < 380 is right clutter
    
    # Let's inspect where the models are using GrabCut with an initialization rect
    rect = (60, 40, w - 120, h - 50)
    mask = np.zeros((h, w), np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    
    # Mark definite background:
    # Left strip (x < 70) is definitely background
    mask[:, :70] = cv2.GC_BGD
    # Right strip (x > 710) is definitely background
    mask[:, 710:] = cv2.GC_BGD
    # Right upper corner (x > 590, y < 320) is definitely lamp/staircase background
    mask[:320, 590:] = cv2.GC_BGD
    # Left upper corner (x < 110, y < 300) is definitely door background
    mask[:300, :110] = cv2.GC_BGD
    # Bottom corners where bare tiles and power strips are:
    mask[int(h*0.75):, 720:] = cv2.GC_BGD
    mask[int(h*0.85):, :60] = cv2.GC_BGD
    
    # Mark probable foreground inside rect
    mask[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]] = cv2.GC_PR_FGD
    
    # Definite foreground: center of each model
    # Model 1 (left/back): x~330, y~150
    # Model 2 (left/center - Tere): x~380, y~350
    # Model 3 (right/center): x~560, y~380
    # Model 4 (right/back): x~660, y~220
    # Products in front: y > 380, 120 < x < 680
    cv2.circle(mask, (330, 150), 30, cv2.GC_FGD, -1)
    cv2.circle(mask, (380, 350), 40, cv2.GC_FGD, -1)
    cv2.circle(mask, (560, 380), 40, cv2.GC_FGD, -1)
    cv2.circle(mask, (660, 220), 30, cv2.GC_FGD, -1)
    mask[380:480, 130:680] = cv2.GC_FGD
    
    print("Running GrabCut...")
    cv2.grabCut(img, mask, None, bgdModel, fgdModel, 4, cv2.GC_INIT_WITH_MASK)
    
    # Subject mask is where mask is FGD or PR_FGD
    subj_mask = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 1.0, 0.0).astype(np.float32)
    
    # Dilate slightly to include contact shadows on the floor
    kernel_shadow = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 7))
    subj_mask_shadow = cv2.dilate(subj_mask, kernel_shadow, iterations=1)
    
    # Soft edge feathering (5px gaussian)
    feathered_mask = cv2.GaussianBlur(subj_mask_shadow, (9, 9), 0)
    feathered_3c = np.repeat(feathered_mask[:, :, np.newaxis], 3, axis=2)
    
    # 3. Tone boost on the original subjects (warm skin, gentle exposure +0.3 EV)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    x = np.arange(256, dtype=np.float32)
    curve = np.clip(255.0 * np.power(x / 255.0, 0.90), 0, 255).astype(np.uint8)
    l_lifted = cv2.LUT(l, curve)
    img_lifted = cv2.cvtColor(cv2.merge((l_lifted, a, b)), cv2.COLOR_LAB2BGR)
    
    # 4. Composite subjects onto synthetic studio background
    composite = (img_lifted * feathered_3c + bg_studio * (1.0 - feathered_3c)).astype(np.uint8)
    
    # 5. Add digital mirror reflection on the floor
    # Floor contact zone is y >= 440
    contact_y = int(h * 0.83)
    sample_h = int(h * 0.16)
    lower_body = composite[contact_y - sample_h:contact_y, :]
    reflection = cv2.flip(lower_body, 0)
    refl_blur = cv2.GaussianBlur(reflection, (11, 3), 0)
    
    fade = np.linspace(0.28, 0.0, sample_h, dtype=np.float32)[:, np.newaxis]
    fade_3c = np.repeat(np.repeat(fade[:, :, np.newaxis], w, axis=1), 3, axis=2)
    
    dest_end = min(h, contact_y + sample_h)
    actual_h = dest_end - contact_y
    base_part = composite[contact_y:dest_end, :].astype(np.float32)
    refl_part = refl_blur[:actual_h, :].astype(np.float32)
    fade_part = fade_3c[:actual_h, :]
    
    composite[contact_y:dest_end, :] = (refl_part * fade_part + base_part * (1.0 - fade_part)).astype(np.uint8)
    
    # 6. Final Polish with PIL
    pil_img = Image.fromarray(cv2.cvtColor(composite, cv2.COLOR_BGR2RGB))
    enh_sh = ImageEnhance.Sharpness(pil_img)
    pil_img = enh_sh.enhance(1.15)
    
    enh_col = ImageEnhance.Color(pil_img)
    pil_img = enh_col.enhance(1.05)
    
    pil_img.save(output_path, quality=95)
    print(f"Saved: {output_path}")

clean_group_cyclorama("/private/tmp/farmasi_samples/group_CPT_0845.JPG.jpg", "/private/tmp/farmasi_samples/clean_group_0845.jpg")
