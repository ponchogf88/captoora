#!/usr/bin/env python3
"""
FotoOrquestador - Core Batch Processing Engine
Especializado para el stack de hardware y software del usuario.
Preserva siempre los originales intactos.
"""

import os
import sys
import glob
import datetime
from PIL import Image, ImageEnhance, ImageOps

PRESETS = {
    "instagram_feed": {
        "name": "Instagram Feed",
        "ratio": (4, 5),
        "target_size": (1080, 1350),
        "exp_factor": 1.23,       # +0.3 exposición
        "contrast_factor": 1.15,  # +15 contraste
        "color_factor": 1.10,     # +10 saturación
        "sharpness_factor": 1.30, # nitidez ligera
        "format": "JPEG",
        "quality": 85,
        "prefix": "IG",
        "ext": "jpg"
    },
    "instagram_stories": {
        "name": "Instagram Stories / Reels",
        "ratio": (9, 16),
        "target_size": (1080, 1920),
        "exp_factor": 1.15,       # +0.2 exposición
        "contrast_factor": 1.10,  # +10 contraste
        "color_factor": 1.0,
        "sharpness_factor": 1.40, # nitidez moderada
        "format": "JPEG",
        "quality": 80,
        "prefix": "STORY",
        "ext": "jpg"
    },
    "tiktok": {
        "name": "TikTok / Vertical",
        "ratio": (9, 16),
        "target_size": (1080, 1920),
        "exp_factor": 1.30,       # +0.4 exposición
        "contrast_factor": 1.20,  # +20 contraste
        "color_factor": 1.05,     # +5 saturación
        "sharpness_factor": 1.40, # nitidez media
        "format": "JPEG",
        "quality": 85,
        "prefix": "TT",
        "ext": "jpg"
    },
    "web_portfolio": {
        "name": "Web / Portfolio",
        "ratio": None,            # Original o 3:2 / 16:9
        "max_long_edge": 2000,
        "exp_factor": 1.0,        # Exposición neutra
        "contrast_factor": 1.08,  # Contraste suave (+8)
        "color_factor": 1.0,
        "sharpness_factor": 1.20, # Nitidez ligera
        "format": "WEBP",
        "quality": 80,
        "prefix": "WEB",
        "ext": "webp"
    },
    "entrega_cliente": {
        "name": "Entrega a Cliente",
        "ratio": None,            # Original
        "exp_factor": 1.05,       # Corrección leve
        "contrast_factor": 1.05,
        "color_factor": 1.0,
        "sharpness_factor": 1.15, # Nitidez muy ligera
        "format": "JPEG",
        "quality": 95,
        "prefix": "CLIENTE",
        "ext": "jpg"
    },
    "miniatura": {
        "name": "Miniatura / Thumbnail",
        "ratio": (1, 1),
        "target_size": (1200, 1200),
        "exp_factor": 1.23,       # +0.3 exposición
        "contrast_factor": 1.15,  # +15 contraste
        "color_factor": 1.0,
        "sharpness_factor": 1.40, # Nitidez media
        "format": "JPEG",
        "quality": 80,
        "prefix": "THUMB",
        "ext": "jpg"
    },
    "whatsapp": {
        "name": "WhatsApp / Rápido",
        "ratio": None,
        "max_long_edge": 1600,
        "exp_factor": 1.15,       # +0.2 exposición
        "contrast_factor": 1.08,  # Contraste suave
        "color_factor": 1.0,
        "sharpness_factor": 1.15,
        "format": "JPEG",
        "quality": 75,
        "prefix": "WA",
        "ext": "jpg"
    }
}

def center_crop_to_ratio(img, target_ratio):
    w, h = img.size
    target_w_ratio, target_h_ratio = target_ratio
    current_ratio = w / h
    target_aspect = target_w_ratio / target_h_ratio

    if abs(current_ratio - target_aspect) < 0.005:
        return img

    if current_ratio > target_aspect:
        new_w = int(h * target_aspect)
        offset = (w - new_w) // 2
        return img.crop((offset, 0, offset + new_w, h))
    else:
        new_h = int(w / target_aspect)
        offset = (h - new_h) // 2
        return img.crop((0, offset, w, offset + new_h))

def apply_adjustments(img, preset_cfg):
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    if preset_cfg.get("ratio"):
        img = center_crop_to_ratio(img, preset_cfg["ratio"])

    if preset_cfg.get("target_size"):
        img = img.resize(preset_cfg["target_size"], Image.Resampling.LANCZOS)
    elif preset_cfg.get("max_long_edge"):
        w, h = img.size
        long_edge = max(w, h)
        if long_edge > preset_cfg["max_long_edge"]:
            scale = preset_cfg["max_long_edge"] / float(long_edge)
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

    if preset_cfg.get("exp_factor", 1.0) != 1.0:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(preset_cfg["exp_factor"])

    if preset_cfg.get("contrast_factor", 1.0) != 1.0:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(preset_cfg["contrast_factor"])

    if preset_cfg.get("color_factor", 1.0) != 1.0:
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(preset_cfg["color_factor"])

    if preset_cfg.get("sharpness_factor", 1.0) != 1.0:
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(preset_cfg["sharpness_factor"])

    return img

def process_batch(input_dir, output_dir, preset_key, client_name=None, date_str=None):
    if preset_key not in PRESETS:
        raise ValueError(f"Preset '{preset_key}' no reconocido. Disponibles: {list(PRESETS.keys())}")

    preset_cfg = PRESETS[preset_key]
    
    if not date_str:
        date_str = datetime.datetime.now().strftime("%Y%m%d")

    os.makedirs(output_dir, exist_ok=True)

    extensions = ("*.jpg", "*.jpeg", "*.png", "*.webp", "*.JPG", "*.JPEG", "*.PNG", "*.WEBP")
    image_paths = []
    for ext in extensions:
        image_paths.extend(glob.glob(os.path.join(input_dir, ext)))

    image_paths = sorted(list(set(image_paths)))
    total = len(image_paths)
    processed = []
    errors = []

    for idx, img_path in enumerate(image_paths, start=1):
        try:
            filename = os.path.basename(img_path)
            if preset_key == "entrega_cliente" and client_name:
                out_name = f"{client_name.upper()}_{date_str}_{idx:03d}.{preset_cfg['ext']}"
            else:
                out_name = f"{preset_cfg['prefix']}_{date_str}_{idx:03d}.{preset_cfg['ext']}"

            dest_path = os.path.join(output_dir, out_name)

            with Image.open(img_path) as img:
                out_img = apply_adjustments(img, preset_cfg)
                save_kwargs = {"quality": preset_cfg["quality"]}
                if preset_cfg["format"] == "JPEG":
                    save_kwargs["optimize"] = True
                out_img.save(dest_path, format=preset_cfg["format"], **save_kwargs)

            processed.append({
                "original": filename,
                "salida": out_name,
                "ruta_completa": dest_path
            })
        except Exception as e:
            errors.append({"archivo": os.path.basename(img_path), "error": str(e)})

    return {
        "preset": preset_cfg["name"],
        "total": total,
        "procesados": len(processed),
        "errores": errors,
        "archivos": processed,
        "output_dir": output_dir
    }

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python3 foto_engine.py <input_dir> <output_dir> <preset_key> [client_name]")
        sys.exit(1)

    in_d = sys.argv[1]
    out_d = sys.argv[2]
    p_key = sys.argv[3]
    c_name = sys.argv[4] if len(sys.argv) > 4 else None

    res = process_batch(in_d, out_d, p_key, c_name)
    print(f"Resumen: {res['procesados']}/{res['total']} procesados con éxito en {out_d}")
