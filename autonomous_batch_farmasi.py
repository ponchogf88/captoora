import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import os
import glob

raw_dir = "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026"
out_dir_hq = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/01_Alta_Resolucion_Cliente"
out_dir_icloud = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/Captoora/ENTREGA_FARMASI_TERE_10_OCT/01_Alta_Resolucion_Cliente")
os.makedirs(out_dir_hq, exist_ok=True)
os.makedirs(out_dir_icloud, exist_ok=True)

# 1. Processing CPT_0580 (Tere close-up with bottle)
def process_0580():
    p = os.path.join(raw_dir, "CPT_0580.JPG")
    img = cv2.imread(p)
    h, w, _ = img.shape
    
    # Relight
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    x = np.arange(256, dtype=np.float32)
    curve = np.clip(255.0 * np.power(x / 255.0, 0.88), 0, 255).astype(np.uint8)
    l_lifted = cv2.LUT(l, curve)
    relit = cv2.cvtColor(cv2.merge((l_lifted, a, b)), cv2.COLOR_LAB2BGR)
    
    # Pure studio backdrop on sides
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt(((X - w * 0.45) / (w * 0.7)) ** 2 + ((Y - h * 0.25) / (h * 0.6)) ** 2)
    bg_l = np.clip(246.0 - dist * 16.0, 230.0, 246.0).astype(np.uint8)
    studio_bg = np.zeros((h, w, 3), dtype=np.uint8)
    studio_bg[:, :, 0] = np.clip(bg_l.astype(int) - 1, 0, 255).astype(np.uint8)
    studio_bg[:, :, 1] = bg_l
    studio_bg[:, :, 2] = np.clip(bg_l.astype(int) + 1, 0, 255).astype(np.uint8)
    
    # Mask sides (wrinkles & door/wall)
    mask = np.zeros((h, w), dtype=np.uint8)
    pts_l = np.array([[0, 0], [1300, 0], [1150, h], [0, h]], dtype=np.int32)
    cv2.fillPoly(mask, [pts_l], 255)
    pts_r = np.array([[3100, 0], [w, 0], [w, h], [3150, h]], dtype=np.int32)
    cv2.fillPoly(mask, [pts_r], 255)
    # Floor plastic line at bottom (y > 4400)
    pts_floor = np.array([[0, 4400], [w, 4400], [w, h], [0, h]], dtype=np.int32)
    cv2.fillPoly(mask, [pts_floor], 255)
    
    # Protect Tere from mask:
    # Tere spans x from 1400 to 3000, y from 1100 to 5700
    mask_f = mask.astype(np.float32) / 255.0
    mask_smooth = cv2.GaussianBlur(mask_f, (81, 81), 0)
    mask_3c = np.repeat(mask_smooth[:, :, np.newaxis], 3, axis=2)
    
    comp = (studio_bg.astype(np.float32) * mask_3c + relit.astype(np.float32) * (1.0 - mask_3c)).astype(np.uint8)
    
    # Crop to clean vertical 3:4
    crop = comp[200:5800, 400:3600]
    
    pil_out = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    enh = ImageEnhance.Sharpness(pil_out)
    pil_out = enh.enhance(1.12)
    
    target_loc = os.path.join(out_dir_hq, "FARMASI_CPT_0580_HQ.jpg")
    target_icloud = os.path.join(out_dir_icloud, "FARMASI_CPT_0580_HQ.jpg")
    pil_out.save(target_loc, quality=96)
    pil_out.save(target_icloud, quality=96)
    print("✓ CPT_0580 procesada y sincronizada")

# 2. Processing CPT_0630 (Girl in boots on stool)
def process_0630():
    p = os.path.join(raw_dir, "CPT_0630.JPG")
    img = cv2.imread(p)
    h, w, _ = img.shape
    
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    x = np.arange(256, dtype=np.float32)
    curve = np.clip(255.0 * np.power(x / 255.0, 0.88), 0, 255).astype(np.uint8)
    l_lifted = cv2.LUT(l, curve)
    relit = cv2.cvtColor(cv2.merge((l_lifted, a, b)), cv2.COLOR_LAB2BGR)
    
    studio_bg = np.full((h, w, 3), 242, dtype=np.uint8)
    
    # Mask left door and right wall
    mask = np.zeros((h, w), dtype=np.uint8)
    pts_l = np.array([[0, 0], [900, 0], [750, h], [0, h]], dtype=np.int32)
    cv2.fillPoly(mask, [pts_l], 255)
    pts_r = np.array([[3300, 0], [w, 0], [w, h], [3200, h]], dtype=np.int32)
    cv2.fillPoly(mask, [pts_r], 255)
    # Floor power strip (bottom left corner x < 600, y > 4500)
    pts_fl = np.array([[0, 4500], [600, 4500], [600, h], [0, h]], dtype=np.int32)
    cv2.fillPoly(mask, [pts_fl], 255)
    
    mask_f = mask.astype(np.float32) / 255.0
    mask_smooth = cv2.GaussianBlur(mask_f, (81, 81), 0)
    mask_3c = np.repeat(mask_smooth[:, :, np.newaxis], 3, axis=2)
    
    comp = (studio_bg.astype(np.float32) * mask_3c + relit.astype(np.float32) * (1.0 - mask_3c)).astype(np.uint8)
    crop = comp[100:5850, 450:3550]
    
    pil_out = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    enh = ImageEnhance.Sharpness(pil_out)
    pil_out = enh.enhance(1.12)
    
    target_loc = os.path.join(out_dir_hq, "FARMASI_CPT_0630_HQ.jpg")
    target_icloud = os.path.join(out_dir_icloud, "FARMASI_CPT_0630_HQ.jpg")
    pil_out.save(target_loc, quality=96)
    pil_out.save(target_icloud, quality=96)
    print("✓ CPT_0630 procesada y sincronizada")

# 3. Processing CPT_0750 (Tere standing full body polka dots)
def process_0750():
    p = os.path.join(raw_dir, "CPT_0750.JPG")
    img = cv2.imread(p) # 4000x6000 horizontal
    h, w, _ = img.shape
    
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    x = np.arange(256, dtype=np.float32)
    curve = np.clip(255.0 * np.power(x / 255.0, 0.88), 0, 255).astype(np.uint8)
    l_lifted = cv2.LUT(l, curve)
    relit = cv2.cvtColor(cv2.merge((l_lifted, a, b)), cv2.COLOR_LAB2BGR)
    
    # In CPT_0750, Tere is centered from x=2100 to 4800, y=700 to 3800
    studio_bg = np.full((h, w, 3), 242, dtype=np.uint8)
    
    # Mask sides (folds and floor plastic line)
    mask = np.zeros((h, w), dtype=np.uint8)
    pts_l = np.array([[0, 0], [1800, 0], [1600, h], [0, h]], dtype=np.int32)
    cv2.fillPoly(mask, [pts_l], 255)
    pts_r = np.array([[5200, 0], [w, 0], [w, h], [5000, h]], dtype=np.int32)
    cv2.fillPoly(mask, [pts_r], 255)
    # Floor plastic line at left and right of feet
    pts_fl = np.array([[0, 3200], [2100, 3200], [2100, h], [0, h]], dtype=np.int32)
    cv2.fillPoly(mask, [pts_fl], 255)
    pts_fr = np.array([[3600, 3400], [w, 3400], [w, h], [3600, h]], dtype=np.int32)
    cv2.fillPoly(mask, [pts_fr], 255)
    
    mask_f = mask.astype(np.float32) / 255.0
    mask_smooth = cv2.GaussianBlur(mask_f, (81, 81), 0)
    mask_3c = np.repeat(mask_smooth[:, :, np.newaxis], 3, axis=2)
    
    comp = (studio_bg.astype(np.float32) * mask_3c + relit.astype(np.float32) * (1.0 - mask_3c)).astype(np.uint8)
    # Crop to vertical portrait
    crop = comp[100:3950, 1400:5200]
    
    pil_out = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    enh = ImageEnhance.Sharpness(pil_out)
    pil_out = enh.enhance(1.12)
    
    target_loc = os.path.join(out_dir_hq, "FARMASI_CPT_0750_HQ.jpg")
    target_icloud = os.path.join(out_dir_icloud, "FARMASI_CPT_0750_HQ.jpg")
    pil_out.save(target_loc, quality=96)
    pil_out.save(target_icloud, quality=96)
    print("✓ CPT_0750 procesada y sincronizada")

# 4. Processing CPT_0800 (Girl with dumbbell)
def process_0800():
    p = os.path.join(raw_dir, "CPT_0800.JPG")
    img = cv2.imread(p) # 4000x6000 vertical
    h, w, _ = img.shape
    
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    x = np.arange(256, dtype=np.float32)
    curve = np.clip(255.0 * np.power(x / 255.0, 0.88), 0, 255).astype(np.uint8)
    l_lifted = cv2.LUT(l, curve)
    relit = cv2.cvtColor(cv2.merge((l_lifted, a, b)), cv2.COLOR_LAB2BGR)
    
    studio_bg = np.full((h, w, 3), 242, dtype=np.uint8)
    
    # Mask right wall, lamp, and bottom left power strip
    mask = np.zeros((h, w), dtype=np.uint8)
    pts_r = np.array([[3350, 0], [w, 0], [w, h], [3200, h]], dtype=np.int32)
    cv2.fillPoly(mask, [pts_r], 255)
    pts_l = np.array([[0, 0], [700, 0], [600, h], [0, h]], dtype=np.int32)
    cv2.fillPoly(mask, [pts_l], 255)
    # Bottom left power strip
    pts_bl = np.array([[0, 4200], [1200, 4200], [1200, h], [0, h]], dtype=np.int32)
    cv2.fillPoly(mask, [pts_bl], 255)
    
    mask_f = mask.astype(np.float32) / 255.0
    mask_smooth = cv2.GaussianBlur(mask_f, (81, 81), 0)
    mask_3c = np.repeat(mask_smooth[:, :, np.newaxis], 3, axis=2)
    
    comp = (studio_bg.astype(np.float32) * mask_3c + relit.astype(np.float32) * (1.0 - mask_3c)).astype(np.uint8)
    crop = comp[150:5850, 400:3600]
    
    pil_out = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    enh = ImageEnhance.Sharpness(pil_out)
    pil_out = enh.enhance(1.12)
    
    target_loc = os.path.join(out_dir_hq, "FARMASI_CPT_0800_HQ.jpg")
    target_icloud = os.path.join(out_dir_icloud, "FARMASI_CPT_0800_HQ.jpg")
    pil_out.save(target_loc, quality=96)
    pil_out.save(target_icloud, quality=96)
    print("✓ CPT_0800 procesada y sincronizada")

# 5. Processing CPT_0550 (Redhead on floor)
def process_0550():
    p = os.path.join(raw_dir, "CPT_0550.JPG")
    img = cv2.imread(p) # 4000x6000 vertical
    h, w, _ = img.shape
    
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    x = np.arange(256, dtype=np.float32)
    curve = np.clip(255.0 * np.power(x / 255.0, 0.88), 0, 255).astype(np.uint8)
    l_lifted = cv2.LUT(l, curve)
    relit = cv2.cvtColor(cv2.merge((l_lifted, a, b)), cv2.COLOR_LAB2BGR)
    
    studio_bg = np.full((h, w, 3), 242, dtype=np.uint8)
    
    # Mask right blue cloth and stand
    mask = np.zeros((h, w), dtype=np.uint8)
    pts_r = np.array([[3100, 0], [w, 0], [w, h], [2800, h]], dtype=np.int32)
    cv2.fillPoly(mask, [pts_r], 255)
    pts_l = np.array([[0, 0], [600, 0], [500, h], [0, h]], dtype=np.int32)
    cv2.fillPoly(mask, [pts_l], 255)
    
    mask_f = mask.astype(np.float32) / 255.0
    mask_smooth = cv2.GaussianBlur(mask_f, (81, 81), 0)
    mask_3c = np.repeat(mask_smooth[:, :, np.newaxis], 3, axis=2)
    
    comp = (studio_bg.astype(np.float32) * mask_3c + relit.astype(np.float32) * (1.0 - mask_3c)).astype(np.uint8)
    crop = comp[100:5850, 300:3500]
    
    pil_out = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    enh = ImageEnhance.Sharpness(pil_out)
    pil_out = enh.enhance(1.12)
    
    target_loc = os.path.join(out_dir_hq, "FARMASI_CPT_0550_HQ.jpg")
    target_icloud = os.path.join(out_dir_icloud, "FARMASI_CPT_0550_HQ.jpg")
    pil_out.save(target_loc, quality=96)
    pil_out.save(target_icloud, quality=96)
    print("✓ CPT_0550 procesada y sincronizada")

if __name__ == "__main__":
    print("Iniciando procesamiento autónomo de lote Farmasi...")
    process_0580()
    process_0630()
    process_0750()
    process_0800()
    process_0550()
    print("🎉 Lote completo procesado y sincronizado a iCloud Drive!")
