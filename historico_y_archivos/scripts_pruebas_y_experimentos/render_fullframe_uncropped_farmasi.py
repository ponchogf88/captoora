import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
import os

RAW_DIR = "/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/PORTAFOLIO/GROUPS/FARMASI SESSION 10 10 2026"
ARTIFACT_DIR = "/Users/user/.gemini/antigravity/brain/cf04fa2d-a692-4959-953d-a57ba80d2280"
OUT_HQ_DIR = "/Users/user/Desktop/Projects/CAPTOORA.STUDIO/ENTREGAS_CLIENTES/FARMASI_SESION_10_OCT/01_Alta_Resolucion_Cliente"

os.makedirs(OUT_HQ_DIR, exist_ok=True)

def load_oriented_bgr(path):
    pil_im = Image.open(path)
    pil_im = ImageOps.exif_transpose(pil_im)
    rgb = np.array(pil_im)
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

def studio_relight(img, gamma=0.87):
    # Lift midtones & shadows cleanly in LAB + subtle skin-friendly contrast & warmth balance
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    x = np.arange(256, dtype=np.float32)
    curve = np.clip(255.0 * np.power(x / 255.0, gamma), 0, 255).astype(np.uint8)
    l_lifted = cv2.LUT(l, curve)
    # Neutralize slight yellow indoor cast on white backdrop (reduce b channel slightly in bright areas)
    bright_mask = (l_lifted.astype(np.float32) / 255.0) ** 2
    b_clean = np.clip(b.astype(np.float32) - bright_mask * 5.0, 0, 255).astype(np.uint8)
    return cv2.cvtColor(cv2.merge((l_lifted, a, b_clean)), cv2.COLOR_LAB2BGR)

def make_studio_bg(h, w, center_val=239, edge_val=226):
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt(((X - w * 0.5) / (w * 0.7)) ** 2 + ((Y - h * 0.45) / (h * 0.7)) ** 2)
    bg_l = np.clip(center_val - dist * (center_val - edge_val), edge_val, center_val).astype(np.uint8)
    studio_bg = np.zeros((h, w, 3), dtype=np.uint8)
    studio_bg[:, :, 0] = np.clip(bg_l.astype(int) - 2, 0, 255).astype(np.uint8)
    studio_bg[:, :, 1] = bg_l
    studio_bg[:, :, 2] = np.clip(bg_l.astype(int) + 2, 0, 255).astype(np.uint8)
    return studio_bg

def blend_mask(relit, studio_bg, mask, blur_k=171):
    mask_f = mask.astype(np.float32) / 255.0
    mask_smooth = cv2.GaussianBlur(mask_f, (blur_k, blur_k), 0)
    mask_3c = np.repeat(mask_smooth[:, :, np.newaxis], 3, axis=2)
    return (studio_bg.astype(np.float32) * mask_3c + relit.astype(np.float32) * (1.0 - mask_3c)).astype(np.uint8)

def save_outputs(comp, code):
    pil_out = Image.fromarray(cv2.cvtColor(comp, cv2.COLOR_BGR2RGB))
    pil_out = ImageEnhance.Sharpness(pil_out).enhance(1.12)
    pil_out = ImageEnhance.Contrast(pil_out).enhance(1.04)
    hq_path = os.path.join(OUT_HQ_DIR, f"FARMASI_CPT_{code}_FULLFRAME_HQ.jpg")
    pil_out.save(hq_path, quality=96)
    
    prev = pil_out.copy()
    prev.thumbnail((1400, 1400), Image.Resampling.LANCZOS)
    art_path = os.path.join(ARTIFACT_DIR, f"farmasi_fullframe_{code}.jpg")
    prev.save(art_path, quality=92)
    print(f"✓ {code}: Full-Frame ({pil_out.width}x{pil_out.height}) CERO RECORTE DE PERSONAS")

def process_all():
    # 1. CPT_0845 (6000x4000 Horizontal Group)
    # Left model's legs go all the way to x=0 at y=2200..3300! Right model's sneaker goes to x=5940 at y=2800..3400!
    # So we ONLY mask the top-left closet door above y=2150, and top-right room/railing/blue bag above y=2250 + power strip at x>5300, y=2450..2950!
    img = load_oriented_bgr(os.path.join(RAW_DIR, "CPT_0845.JPG"))
    h, w, _ = img.shape
    relit = studio_relight(img, 0.87)
    bg = make_studio_bg(h, w, 238, 224)
    mask = np.zeros((h, w), dtype=np.uint8)
    # Top-left closet door ONLY (above the left model's legs y<2180, left of fabric x<820)
    cv2.fillPoly(mask, [np.array([[0, 0], [820, 0], [650, 2150], [0, 2250]], dtype=np.int32)], 255)
    # Right side room wall, lamp & railing ONLY (above right model's extended leg y<2350, right of model x>4350)
    cv2.fillPoly(mask, [np.array([[4280, 0], [w, 0], [w, 2400], [4480, 2320], [4350, 1600]], dtype=np.int32)], 255)
    # Bottom-right corner cables/bag below sneaker (y>3480, x>5250)
    cv2.fillPoly(mask, [np.array([[5300, 3500], [w, 3450], [w, h], [5200, h]], dtype=np.int32)], 255)
    comp = blend_mask(relit, bg, mask, 151)
    save_outputs(comp, "0845")

    # 2. CPT_0550 (4000x6000 Upright Vertical Portrait)
    # Backdrop already covers almost the entire frame! Only a tiny top-right hallway strip (x>3250, y<1400) is visible, well above her left arm (which is at y=1800..3200).
    img = load_oriented_bgr(os.path.join(RAW_DIR, "CPT_0550.JPG"))
    h, w, _ = img.shape
    relit = studio_relight(img, 0.86)
    bg = make_studio_bg(h, w, 240, 228)
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask, [np.array([[3300, 0], [w, 0], [w, 1300], [3400, 1300]], dtype=np.int32)], 255)
    comp = blend_mask(relit, bg, mask, 151)
    save_outputs(comp, "0550")

    # 3. CPT_0580 (4000x6000 Upright Vertical Portrait with Stool)
    # Model is in center; stool is on left (x=550..1650); hallway door frame is on far top-left (x<950, y<1450)
    img = load_oriented_bgr(os.path.join(RAW_DIR, "CPT_0580.JPG"))
    h, w, _ = img.shape
    relit = studio_relight(img, 0.86)
    bg = make_studio_bg(h, w, 240, 226)
    mask = np.zeros((h, w), dtype=np.uint8)
    # Clean only the top-left hallway/railing above the stool (y<1450, x<950)
    cv2.fillPoly(mask, [np.array([[0, 0], [950, 0], [900, 1350], [0, 1450]], dtype=np.int32)], 255)
    comp = blend_mask(relit, bg, mask, 151)
    save_outputs(comp, "0580")

    # 4. CPT_0630 (4000x6000 Upright Vertical Portrait - Fitness Dumbbell)
    # Model is in center; products at bottom-left; small clip light at bottom-right/top-left depending on orientation
    img = load_oriented_bgr(os.path.join(RAW_DIR, "CPT_0630.JPG"))
    h, w, _ = img.shape
    relit = studio_relight(img, 0.87)
    comp = relit
    save_outputs(comp, "0630")

    # 5. CPT_0700 (4000x6000 Upright Vertical Portrait - Black Dress & Boots)
    img = load_oriented_bgr(os.path.join(RAW_DIR, "CPT_0700.JPG"))
    h, w, _ = img.shape
    relit = studio_relight(img, 0.87)
    comp = relit
    save_outputs(comp, "0700")

    # 6. CPT_0750 (6000x4000 Horizontal Portrait - Seated Redhead with Nutriplus)
    # Left edge has a dumbbell/White sneaker goes to x=120! Right edge has blue bag & light stand at x>5450!
    img = load_oriented_bgr(os.path.join(RAW_DIR, "CPT_0750.JPG"))
    h, w, _ = img.shape
    relit = studio_relight(img, 0.86)
    bg = make_studio_bg(h, w, 238, 224)
    mask = np.zeros((h, w), dtype=np.uint8)
    # Clean ONLY the right edge blue bag and light stand (x>5450), staying 450px away from her left hand (which ends at x=4980)
    cv2.fillPoly(mask, [np.array([[5450, 0], [w, 0], [w, h], [5400, h]], dtype=np.int32)], 255)
    comp = blend_mask(relit, bg, mask, 151)
    save_outputs(comp, "0750")

    # 7. CPT_0800 (4000x6000 Upright Vertical Portrait - Collagen Shot Close-Up)
    img = load_oriented_bgr(os.path.join(RAW_DIR, "CPT_0800.JPG"))
    h, w, _ = img.shape
    relit = studio_relight(img, 0.87)
    comp = relit
    save_outputs(comp, "0800")

if __name__ == "__main__":
    process_all()
