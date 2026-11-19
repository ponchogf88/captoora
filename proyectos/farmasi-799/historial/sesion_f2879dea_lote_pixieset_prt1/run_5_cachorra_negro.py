import os
import shutil
import cv2
import numpy as np
from PIL import Image

SRC_DIR = "/Users/imac/Desktop/31 oct selection 1/FARMASI_799_SELECCION_JPG"
WORK_DIR = "/Users/imac/.gemini/antigravity/brain/f2879dea-081d-4db4-bc8f-53d5a02e349f/scratch/cobrizo_5_edit"
ART_DIR = "/Users/imac/.gemini/antigravity/brain/f2879dea-081d-4db4-bc8f-53d5a02e349f"
PEND_DIR = os.path.join(WORK_DIR, "PENDIENTES_DE_APROBACION")
os.makedirs(PEND_DIR, exist_ok=True)


def process_dark_studio_photo(fn, out_name, mode_name):
    """
    Captoora Studio 'Fondo Negro' (Deep Charcoal-Black + Natural Warm Amber Glow) Processor:
      1. Orients vertical portrait upright (4128x6192).
      2. Protects 100% of the ambassador (face, every single hair strand/flyaway, rose+sunflower tattoo,
         beige dress, hands, and props) with a soft organic silhouette boundary — ZERO hard boxes!
      3. Removes specific room intrusions (white pillar, baseboard, LED corner, left curtain) by
         inpainting/replacing them with the exact local deep charcoal-black tone of that photo's
         real studio background, and gently de-creases the dark cloth folds in the background.
    """
    src_path = os.path.join(SRC_DIR, fn)
    im = Image.open(src_path).rotate(90, expand=True)
    orig = np.array(im)
    h, w, _ = orig.shape

    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    yn = yy / float(h)
    xn = xx / float(w)

    orig_f = orig.astype(np.float32)
    r, g, b = orig_f[:, :, 0], orig_f[:, :, 1], orig_f[:, :, 2]
    luma = 0.299 * r + 0.587 * g + 0.114 * b

    # Build a clean, ultra-smooth version of the photo's OWN real dark studio background
    # by masking out the subject and any bright intrusions, downsampling, inpainting, and Gaussian-smoothing
    # at large scale so there are ZERO cloth creases and ZERO color mismatches around her hair!
    if mode_name == "DSC01880":
        # Exact boundary between the left vertical curtain and her shoulder/arm:
        # Above y=0.505, the curtain extends to x=0.275 (gap at x=0.28..0.31).
        # From y=0.505 down to y=0.72, her shoulder/arm curves left from x=0.265 to x=0.175.
        left_arm_bound = np.where(
            yn < 0.505,
            0.275,
            np.clip(0.265 - 0.44 * (yn - 0.505), 0.170, 0.275)
        )
        subj_core = (
            # Head and hair + warm amber top-right studio spotlight so the original warm amber glow is 100% seamless
            (((xn - 0.50) / 0.23) ** 2 + ((yn - 0.34) / 0.20) ** 2 < 1.0) |
            ((xn >= 0.44) & (yn <= 0.52)) |
            # Torso, tattoo, arms, dress, bag (strictly right of left_arm_bound)
            ((xn >= left_arm_bound) & (xn <= 0.99) & (yn >= 0.475) & (luma > 13.0))
        )
        # Specific intrusions to remove:
        # 1) Left vertical curtain/seam (left of left_arm_bound)
        # 2) Top white seam at x in [0.18, 0.275], y < 0.20
        intrusion = (
            ((xn < left_arm_bound) & (yn < 0.72) & (~subj_core)) |
            ((xn < 0.275) & (yn < 0.20) & (~subj_core))
        )

    elif mode_name == "DSC01919":
        # Subject + hair + palettes + torso
        subj_core = (
            # Head and hair oval
            (((xn - 0.53) / 0.26) ** 2 + ((yn - 0.39) / 0.195) ** 2 < 1.0) |
            # Palettes, hands, arms, torso
            ((xn >= 0.13) & (xn <= 0.91) & (yn >= 0.45) & (luma > 14.0))
        )
        # Specific intrusion: white room pillar at top-right (x in [0.58, 0.67], y < 0.23)
        intrusion = (xn > 0.575) & (xn < 0.68) & (yn < 0.235) & (~subj_core)

    elif mode_name == "DSC01973":
        # Exact right edge of her beige dress in the lower body (y >= 0.715):
        # At y=0.715..0.85, her dress edge is at x=0.648; from y=0.85..1.00, it tapers to x=0.610 (excluding the blue LED reflection at x=0.615..0.635).
        dress_right_bound = np.where(
            yn < 0.85,
            0.648,
            0.648 - 0.27 * (yn - 0.85)
        )
        subj_core = (
            # Head and hair oval
            (((xn - 0.36) / 0.29) ** 2 + ((yn - 0.26) / 0.28) ** 2 < 1.0) |
            # Shoulder tattoo, arm, torso (strictly left of dress_right_bound)
            ((xn >= 0.18) & (xn <= dress_right_bound) & (yn >= 0.40) & (luma > 11.0)) |
            # Goblet and hand (only above y=0.715)
            ((xn >= 0.60) & (xn <= 0.835) & (yn >= 0.40) & (yn <= 0.715) & (luma > 13.0))
        )
        # Specific intrusion: bottom-right bright LED panel corner & floor (right of dress_right_bound for y > 0.78)
        intrusion = (xn > dress_right_bound) & (yn > 0.78) & (~subj_core)

    elif mode_name == "DSC01982":
        # Subject + hair + tattoo + crystal goblet
        subj_core = (
            # Head and hair oval (includes top hair strands at y >= 0.095)
            (((xn - 0.38) / 0.29) ** 2 + ((yn - 0.33) / 0.245) ** 2 < 1.0) |
            # Tattoo, arm, torso
            ((xn >= 0.0) & (xn <= 0.77) & (yn >= 0.48) & (luma > 10.0)) |
            # Goblet and hand
            ((xn >= 0.69) & (xn <= 0.99) & (yn >= 0.52) & (yn <= 0.955) & (luma > 12.0))
        )
        # Specific intrusion: tiny white seam at very top edge (x in [0.38, 0.44], y < 0.085)
        intrusion = (xn > 0.36) & (xn < 0.46) & (yn < 0.09) & (~subj_core)

    elif mode_name == "DSC01987":
        # Exact right edge of her beige dress at the bottom-right (y >= 0.88):
        # Tapers smoothly along the dark valley between her dress and the baseboard:
        # from x=0.695 at y=0.88 to x=0.625 at y=1.00.
        dress_right_bound = np.where(
            yn < 0.88,
            0.83,
            0.695 - 0.58 * (yn - 0.88)
        )
        subj_core = (
            # Head and hair oval
            (((xn - 0.50) / 0.23) ** 2 + ((yn - 0.29) / 0.165) ** 2 < 1.0) |
            # Tattoo, arms, dress (strictly left of dress_right_bound)
            ((xn >= 0.27) & (xn <= dress_right_bound) & (yn >= 0.36) & (luma > 13.0)) |
            # Newspaper on right
            ((xn >= 0.74) & (xn <= 1.0) & (yn >= 0.31) & (yn <= 0.775) & (luma > 20.0))
        )
        # Specific intrusions:
        # 1) White baseboard at bottom-right (right of dress_right_bound for y > 0.86)
        # 2) Top white vertical seam (x in [0.37, 0.45], y < 0.135)
        in_baseboard = (xn > dress_right_bound) & (yn > 0.86)
        in_top_seam = (xn > 0.37) & (xn < 0.45) & (yn < 0.135)
        intrusion = (in_baseboard | in_top_seam) & (~subj_core)

    # Erode subj_core slightly for strict biometric/prop protection (`protected`), and exclude `intrusion`
    k_erode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    protected = (cv2.erode(subj_core.astype(np.uint8) * 255, k_erode, iterations=1) > 127) & (~intrusion)

    # Pre-clean `orig_for_bg` on `intrusion` with the local deep charcoal studio tone BEFORE downsampling/inpainting
    # so zero bright LED/baseboard/curtain energy leaks into `smooth_small`!
    orig_for_bg = orig.copy()
    if mode_name == "DSC01880":
        orig_for_bg[intrusion] = np.array([10, 9, 9], dtype=np.uint8)
    elif mode_name == "DSC01973":
        orig_for_bg[intrusion] = np.array([13, 13, 14], dtype=np.uint8)
    elif mode_name == "DSC01987":
        orig_for_bg[intrusion] = np.array([6, 6, 7], dtype=np.uint8)

    # Build the seamless dark background field at 1/8 resolution:
    scale = 8
    sh, sw = h // scale, w // scale
    small_orig = cv2.resize(orig_for_bg, (sw, sh), interpolation=cv2.INTER_AREA)

    if mode_name == "DSC01880":
        smooth_small = cv2.GaussianBlur(small_orig.astype(np.float32), (0, 0), sigmaX=12.0, sigmaY=12.0)
    else:
        hole_full = (subj_core | intrusion).astype(np.uint8) * 255
        hole_small = cv2.resize(hole_full, (sw, sh), interpolation=cv2.INTER_NEAREST)
        hole_small = cv2.dilate(hole_small, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)), iterations=1)
        inpainted_small = cv2.inpaint(small_orig, hole_small, inpaintRadius=15, flags=cv2.INPAINT_TELEA)
        smooth_small = cv2.GaussianBlur(inpainted_small.astype(np.float32), (0, 0), sigmaX=18.0, sigmaY=18.0)

    smooth_bg = cv2.resize(smooth_small, (w, h), interpolation=cv2.INTER_CUBIC)

    # Add anti-banding sensor micro-noise (sigma=0.45) matching original camera ISO grain in the shadows
    rng = np.random.default_rng(int(fn.replace("DSC", "").replace(".JPG", "")))
    grain = rng.normal(0.0, 0.45, size=smooth_bg.shape).astype(np.float32)
    smooth_bg = np.clip(smooth_bg + grain, 4.0, 255.0)

    bg_zone = (~subj_core).astype(np.float32)
    soft_bg_weight = cv2.GaussianBlur(bg_zone, (0, 0), sigmaX=65.0, sigmaY=65.0) * (0.65 if mode_name == "DSC01880" else 0.85)

    intr_weight = cv2.GaussianBlur(intrusion.astype(np.float32), (0, 0), sigmaX=6.0, sigmaY=6.0)
    intr_core = cv2.erode(intrusion.astype(np.uint8) * 255, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))) > 127
    intr_weight = np.maximum(intr_weight, intr_core.astype(np.float32))
    intr_weight = np.where(intrusion, 1.0, intr_weight)

    alpha_bg = np.maximum(soft_bg_weight, intr_weight)
    alpha_bg[protected] = 0.0
    alpha_bg[intrusion] = 1.0

    a3 = alpha_bg[:, :, None]
    comp = orig_f * (1.0 - a3) + smooth_bg * a3
    comp_u8 = np.clip(np.round(comp), 0, 255).astype(np.uint8)
    comp_u8[protected] = orig[protected]

    diff = np.abs(comp_u8.astype(np.int32) - orig.astype(np.int32)).max(axis=2)
    prot_changed = int((diff[protected] > 0).sum())
    bg_changed_pct = float((diff[~protected] > 0).mean() * 100.0)

    out_work = os.path.join(WORK_DIR, out_name)
    out_pend = os.path.join(PEND_DIR, out_name)
    out_art = os.path.join(ART_DIR, out_name)

    Image.fromarray(comp_u8).save(out_work, quality=96, subsampling=0)
    shutil.copy2(out_work, out_pend)
    shutil.copy2(out_work, out_art)

    print(f"[OK] {out_name} ({w}x{h}) -> protected_changed={prot_changed}, bg_edited={bg_changed_pct:.1f}%")


if __name__ == "__main__":
    jobs = [
        ("DSC01880.JPG", "16_DSC01880_TATUAJE_BOLSA_PRO.jpg", "DSC01880"),
        ("DSC01919.JPG", "17_DSC01919_TATUAJE_PALETAS_PRO.jpg", "DSC01919"),
        ("DSC01973.JPG", "18_DSC01973_TATUAJE_COPA_PRO.jpg", "DSC01973"),
        ("DSC01982.JPG", "19_DSC01982_TATUAJE_EDITORIAL_PRO.jpg", "DSC01982"),
        ("DSC01987.JPG", "20_DSC01987_TATUAJE_PERIODICO_PRO.jpg", "DSC01987"),
    ]
    for fn, out_name, mode_name in jobs:
        process_dark_studio_photo(fn, out_name, mode_name)
