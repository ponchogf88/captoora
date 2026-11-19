#!/usr/bin/env python3
"""
Captoora Studio — Fondo Negro Terciopelo 'La Morena' para Mancuerna (24, 25, 26).
Replica exactamente el fondo negro ultra-elegante, liso, mate y aterciopelado
de 'La Morena' (DSC01973/DSC01987):
  - Fondo negro uniforme, sin arrugas ni pliegues de tela.
  - Halo sutil y natural de luz de estudio detrás de la cabeza.
  - Micro-grano de sensor ISO idéntico para evitar cualquier banding.
  - Protección estricta biométrica (cabello rubio, rostro, tatuaje, vestido vino, accesorios).
"""
import os, cv2, numpy as np
from PIL import Image

BRAIN = "/Users/imac/.gemini/antigravity/brain/f2879dea-081d-4db4-bc8f-53d5a02e349f"
SRC_DIR = "/Users/imac/Desktop/31 oct selection 1/FARMASI_799_SELECCION_JPG"
PEND_DIR = os.path.join(BRAIN, "scratch/cobrizo_5_edit/PENDIENTES_DE_APROBACION")

JOBS = [
    {
        "fname": "DSC00373.JPG",
        "slug": "24_DSC00373_MANCUERNA_NEGRO_PALETA_PRO",
        # Mancuerna de perfil con paleta rosa y brocha de rubor en el pómulo
        "subj_box": (0.35, 0.12, 0.98, 1.00),
        "props_boxes": [(0.02, 0.20, 0.35, 0.45)], # paleta rosa y mano izquierda
        "glow_center": (0.58, 0.35),
    },
    {
        "fname": "DSC00408.JPG",
        "slug": "25_DSC00408_MANCUERNA_NEGRO_ESPEJO_PRO",
        # Mancuerna de espaldas mirando su reflejo en el espejo de la paleta
        "subj_box": (0.24, 0.05, 1.00, 1.00),
        "props_boxes": [(0.38, 0.18, 0.68, 0.40)], # estuche con espejo y mano
        "glow_center": (0.55, 0.30),
    },
    {
        "fname": "DSC00415.JPG",
        "slug": "26_DSC00415_MANCUERNA_NEGRO_COPA_PRO",
        # Mancuerna en plano medio sosteniendo copa de champaña con fresa
        "subj_box": (0.05, 0.02, 0.98, 1.00),
        "props_boxes": [(0.08, 0.16, 0.42, 0.75)], # copa de champaña y mano
        "glow_center": (0.52, 0.26),
    },
]

def process_velvet_black(job):
    src_path = os.path.join(SRC_DIR, job["fname"])
    # Original orientation: vertical
    orig_im = Image.open(src_path)
    # Check orientation
    w_raw, h_raw = orig_im.size
    if w_raw > h_raw:
        orig_im = orig_im.rotate(90, expand=True)
    orig = np.array(orig_im)
    h, w, _ = orig.shape

    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    yn = yy / float(h)
    xn = xx / float(w)

    r, g, b = orig[..., 0].astype(np.float32), orig[..., 1].astype(np.float32), orig[..., 2].astype(np.float32)
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    warmth = r - b

    # 1. Subject detection & protection mask
    # Inside the bounding region, skin, blonde hair, burgundy dress or props have warmth > 8 or luma > 18
    in_subj_box = np.zeros((h, w), dtype=bool)
    bx0, by0, bx1, by1 = job["subj_box"]
    in_subj_box[int(h*by0):int(h*by1), int(w*bx0):int(w*bx1)] = True
    for px0, py0, px1, py1 in job["props_boxes"]:
        in_subj_box[int(h*py0):int(h*py1), int(w*px0):int(w*px1)] = True

    # Subject pixels: warm skin/hair/dress or bright props
    is_subject = in_subj_box & ((warmth > 8.0) | (luma > 22.0) | ((r > 30.0) & (b < 35.0)))
    
    # Morphological clean on subject to include all interior dress folds and hair
    k_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    k_dilate = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    subj_clean = cv2.morphologyEx(is_subject.astype(np.uint8)*255, cv2.MORPH_CLOSE, k_close)
    subj_clean = cv2.dilate(subj_clean, k_dilate, iterations=1) > 127

    # Strict protected core (inner subject)
    k_erode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    protected = cv2.erode(subj_clean.astype(np.uint8)*255, k_erode) > 127

    # 2. Build the smooth velvety background
    # Downsample background to 1/8 resolution
    scale = 8
    sh, sw = h // scale, w // scale
    small_orig = cv2.resize(orig, (sw, sh), interpolation=cv2.INTER_AREA)
    small_hole = cv2.resize(subj_clean.astype(np.uint8)*255, (sw, sh), interpolation=cv2.INTER_NEAREST)
    small_hole = cv2.dilate(small_hole, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)), iterations=1)

    # Inpaint background hole
    inpainted = cv2.inpaint(small_orig, small_hole, inpaintRadius=21, flags=cv2.INPAINT_TELEA)

    # Smooth out creases with large Gaussian blur (exact 'Morena' recipe)
    smooth_small = cv2.GaussianBlur(inpainted.astype(np.float32), (0, 0), sigmaX=22.0, sigmaY=22.0)

    # Tone match background to elegant velvety deep charcoal (RGB ~ 10, 10, 10 at edges with subtle warm studio falloff)
    # Target background base level: mean luma ~ 11.0, subtle warm tint R-B ~ 1.5 (like morena_18: 13.5, 13.0, 12.7)
    sm_luma = 0.299 * smooth_small[..., 0] + 0.587 * smooth_small[..., 1] + 0.114 * smooth_small[..., 2]
    # Smooth radial studio spotlight behind the head
    gx, gy = job["glow_center"]
    syy, sxx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    dist_sq = ((sxx / sw - gx) / 0.35)**2 + ((syy / sh - gy) / 0.30)**2
    glow = np.exp(-dist_sq * 1.8) * 12.0 # subtle 12-luma warm amber glow

    # Base velvety charcoal black: [10, 10, 11] + amber glow [glow, glow*0.85, glow*0.6]
    velvet_bg_small = np.zeros_like(smooth_small)
    velvet_bg_small[..., 0] = np.clip(10.0 + glow * 1.05 + (smooth_small[..., 0] - sm_luma.mean()) * 0.15, 6.0, 38.0)
    velvet_bg_small[..., 1] = np.clip(10.0 + glow * 0.90 + (smooth_small[..., 1] - sm_luma.mean()) * 0.15, 6.0, 34.0)
    velvet_bg_small[..., 2] = np.clip(11.0 + glow * 0.70 + (smooth_small[..., 2] - sm_luma.mean()) * 0.15, 6.0, 30.0)

    # Upscale velvety background to full resolution
    smooth_bg = cv2.resize(velvet_bg_small, (w, h), interpolation=cv2.INTER_CUBIC)

    # Add authentic camera ISO micro-grain (sigma=0.45) to ensure 0 banding
    seed = int("".join(c for c in job["fname"] if c.isdigit()))
    rng = np.random.default_rng(seed)
    grain = rng.normal(0.0, 0.45, size=smooth_bg.shape).astype(np.float32)
    smooth_bg = np.clip(smooth_bg + grain, 4.0, 255.0)

    # 3. Soft seamless edge transition
    bg_weight = cv2.GaussianBlur((~subj_clean).astype(np.float32), (0, 0), sigmaX=35.0, sigmaY=35.0)
    bg_weight[protected] = 0.0

    a3 = bg_weight[..., None]
    comp = orig.astype(np.float32) * (1.0 - a3) + smooth_bg * a3
    comp_u8 = np.clip(np.round(comp), 0, 255).astype(np.uint8)
    comp_u8[protected] = orig[protected]

    # Save to PENDIENTES and BRAIN
    out_name = f"{job['slug']}.jpg"
    p_pend = os.path.join(PEND_DIR, out_name)
    p_brain = os.path.join(BRAIN, out_name)

    Image.fromarray(comp_u8).save(p_pend, quality=96, subsampling=0)
    Image.fromarray(comp_u8).save(p_brain, quality=96, subsampling=0)
    print(f"[OK] {out_name} -> Velvet Black Studio Background Applied!")

def main():
    for job in JOBS:
        process_velvet_black(job)
    print("ALL 3 VELVET BLACK PHOTOS COMPLETED!")

if __name__ == "__main__":
    main()
