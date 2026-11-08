import cv2
import numpy as np
from PIL import Image

def add_mirror_reflection(img_path, output_path):
    img = cv2.imread(img_path)
    h, w, _ = img.shape
    
    # Floor contact level (approx 83% of height where shoes meet ground)
    contact_y = int(h * 0.85)
    
    # Extract lower body to reflect (from contact_y upwards by about 25% height)
    sample_height = int(h * 0.25)
    body_part = img[contact_y - sample_height:contact_y, :]
    
    # Flip vertically
    reflection = cv2.flip(body_part, 0)
    
    # Create fade gradient mask
    fade = np.linspace(0.35, 0.0, sample_height, dtype=np.float32)[:, np.newaxis]
    fade = np.repeat(fade, w, axis=1)
    fade_3c = np.repeat(fade[:, :, np.newaxis], 3, axis=2)
    
    # Slight horizontal blur on reflection for glossy sheen
    reflection_blurred = cv2.GaussianBlur(reflection, (9, 3), 0)
    
    # Destination in the image
    dest_y_end = min(h, contact_y + sample_height)
    actual_h = dest_y_end - contact_y
    
    base_floor = img[contact_y:dest_y_end, :].astype(np.float32)
    refl_crop = reflection_blurred[:actual_h, :].astype(np.float32)
    fade_crop = fade_3c[:actual_h, :]
    
    # Blend reflection onto floor
    blended_floor = (refl_crop * fade_crop + base_floor * (1.0 - fade_crop)).astype(np.uint8)
    
    img_out = img.copy()
    img_out[contact_y:dest_y_end, :] = blended_floor
    
    cv2.imwrite(output_path, img_out)
    print(f"Saved reflection demo: {output_path}")

add_mirror_reflection("/private/tmp/farmasi_samples/retouched_v3_0550_crop4x5.jpg", "/private/tmp/farmasi_samples/retouched_reflection_0550.jpg")
