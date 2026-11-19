import os, cv2, numpy as np
from PIL import Image
import run_6_mancuerna_blanco_y_grupo as r6
import run_5_more_groups as base

BRAIN = "/Users/imac/.gemini/antigravity/brain/f2879dea-081d-4db4-bc8f-53d5a02e349f"
SRC_DIR = "/Users/imac/Desktop/31 oct selection 1/FARMASI_799_SELECCION_JPG"
SRC_ALL = "/Users/imac/Desktop/31 oct selection 1/FARMASI_31_OCT_26_JPG"
PEND_DIR = os.path.join(BRAIN, "scratch/cobrizo_5_edit/PENDIENTES_DE_APROBACION")
os.makedirs(PEND_DIR, exist_ok=True)

def main():
    print("1. Loading references for seamless white backdrop...")
    ref_7738_u8 = np.asarray(base.load_oriented(os.path.join(SRC_DIR, "DSC07738.JPG")), dtype=np.uint8)
    ref_8485_u8 = np.asarray(base.load_oriented(os.path.join(SRC_DIR, "DSC08485.JPG")), dtype=np.uint8)
    ref_9204_u8 = np.asarray(base.load_oriented(os.path.join(SRC_DIR, "DSC09204 2.JPG")), dtype=np.uint8)
    H0, W0 = ref_7738_u8.shape[:2]
    cloth_folds, rug_detail = base.build_pure_draped_cloth_and_rug_texture(
        H0, W0, ref_7738_u8, ref_8485_u8, ref_9204_u8
    )

    cfg = [c for c in r6.SCENES_6_WHITE if c["fname"] == "DSC08716.JPG"][0]
    src_path = os.path.join(SRC_DIR, cfg["fname"])
    orig_im = base.load_oriented(src_path)
    orig_u8 = np.asarray(orig_im, dtype=np.uint8)
    H, W = orig_u8.shape[:2]

    print("2. Building clean studio white plate for 29...")
    mask, protected = r6.build_mask_v12(orig_u8, cfg)
    plate = base.synthesize_seamless_backdrop(orig_u8, cloth_folds, rug_detail, cfg, mask)

    m3 = mask[:, :, None]
    comp = orig_u8.astype(np.float32) * (1.0 - m3) + plate * m3
    final_u8 = np.clip(np.round(comp), 0, 255).astype(np.uint8)
    final_u8[protected] = orig_u8[protected]

    print("3. Applying highlight recovery & tonal roll-off (no posterization)...")
    # Smooth S-curve compression on highlights above 205 (recovers highlights smoothly)
    lut = np.arange(256, dtype=np.float32)
    for i in range(256):
        if i > 200:
            lut[i] = 200.0 + (i - 200.0) * 0.70
    lut = np.clip(lut, 0, 255).astype(np.uint8)
    
    # Apply tone curve to L channel in LAB
    lab = cv2.cvtColor(final_u8, cv2.COLOR_RGB2LAB)
    lab[..., 0] = cv2.LUT(lab[..., 0], lut)
    final_u8 = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    print("4. Rescuing eyes of right girl using DSC08712 facial landmarks...")
    p_8712 = os.path.join(SRC_ALL, "DSC08712.JPG")
    don_im = base.load_oriented(p_8712)
    don_u8 = np.asarray(don_im, dtype=np.uint8)

    # Face crops in RGB
    y_f0, y_f1 = int(H * 0.34), int(H * 0.48)
    x_f0, x_f1 = int(W * 0.54), int(W * 0.72)
    tgt_crop = final_u8[y_f0:y_f1, x_f0:x_f1].copy()
    don_crop = don_u8[y_f0:y_f1, x_f0:x_f1].copy()

    yunet = "/Users/imac/artemis/models/face_detection_yunet.onnx"
    det = cv2.FaceDetectorYN.create(yunet, "", (tgt_crop.shape[1], tgt_crop.shape[0]), 0.3, 0.3, 5000)
    _, f_tgt = det.detect(tgt_crop)
    det.setInputSize((don_crop.shape[1], don_crop.shape[0]))
    _, f_don = det.detect(don_crop)

    f_t = max(f_tgt, key=lambda f: f[2]*f[3])
    f_d = max(f_don, key=lambda f: f[2]*f[3])
    pt_tgt = f_t[4:14].reshape(5, 2)
    pt_don = f_d[4:14].reshape(5, 2)

    M, _ = cv2.estimateAffinePartial2D(pt_don, pt_tgt)
    warped_don = cv2.warpAffine(don_crop, M, (tgt_crop.shape[1], tgt_crop.shape[0]), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)

    lab_tgt = cv2.cvtColor(tgt_crop, cv2.COLOR_RGB2LAB).astype(np.float32)
    lab_don = cv2.cvtColor(warped_don, cv2.COLOR_RGB2LAB).astype(np.float32)

    diff_low = cv2.GaussianBlur(lab_tgt[:,:,0] - lab_don[:,:,0], (25, 25), 8.0)
    lab_don_matched = lab_don.copy()
    lab_don_matched[:,:,0] = np.clip(lab_don[:,:,0] + diff_low, 0, 255)
    for c in [1, 2]:
        diff_c = cv2.GaussianBlur(lab_tgt[:,:,c] - lab_don[:,:,c], (25, 25), 8.0)
        lab_don_matched[:,:,c] = np.clip(lab_don[:,:,c] + diff_c, 0, 255)

    rgb_don_matched = cv2.cvtColor(np.clip(lab_don_matched, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)

    # Eye-only mask
    mask_eyes = np.zeros((tgt_crop.shape[0], tgt_crop.shape[1]), dtype=np.float32)
    for pt in [pt_tgt[0], pt_tgt[1]]:
        ex, ey = pt
        cv2.circle(mask_eyes, (int(ex), int(ey)), 36, 1.0, -1)
    mask_eyes = cv2.GaussianBlur(mask_eyes, (27, 27), 9.0)[..., None]

    rescued_face = (tgt_crop.astype(np.float32) * (1.0 - mask_eyes) + rgb_don_matched.astype(np.float32) * mask_eyes).astype(np.uint8)
    final_u8[y_f0:y_f1, x_f0:x_f1] = rescued_face

    print("5. Enhancing sharpness & recovering feet/shoes detail...")
    feet_y0, feet_y1 = int(H * 0.70), int(H * 0.98)
    feet_roi = final_u8[feet_y0:feet_y1, :].copy()
    gray_feet = cv2.cvtColor(feet_roi, cv2.COLOR_RGB2GRAY).astype(np.float32)
    low_feet = cv2.GaussianBlur(gray_feet, (0, 0), sigmaX=3.0, sigmaY=3.0)
    high_feet = gray_feet - low_feet
    high_boost = np.sign(high_feet) * np.maximum(0.0, np.abs(high_feet) - 1.2) * 1.35
    final_u8[feet_y0:feet_y1, :] = np.clip(feet_roi.astype(np.float32) + high_boost[..., None], 0, 255).astype(np.uint8)

    print("6. Saving final rescued 29...")
    out_name = "29_DSC08716_MANCUERNA_GRUPO_ROJO_COBRIZO_PRO.jpg"
    p_pend = os.path.join(PEND_DIR, out_name)
    p_brain = os.path.join(BRAIN, out_name)

    Image.fromarray(final_u8).save(p_pend, quality=96, subsampling=0)
    Image.fromarray(final_u8).save(p_brain, quality=96, subsampling=0)

    # Save zoom comparison
    zoom_face = final_u8[y_f0-30:y_f1+30, x_f0-30:x_f1+30]
    Image.fromarray(zoom_face).save(os.path.join(BRAIN, "scratch/cobrizo_5_edit/verify_29_right_face_eyes.jpg"), quality=95)
    print("29 RESCUE COMPLETE!")

if __name__ == "__main__":
    main()
