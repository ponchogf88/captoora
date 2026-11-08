# -*- coding: utf-8 -*-
"""
GENERADOR DE CARRUSELES Y POSTS 4:5 (1080x1350) ZERO-CROP CON EXIF ÓPTICO NIKON Z
=================================================================================
Prepara las carpetas listas para publicar de los 30 días (especialmente Día 01 Manifiesto Anti-IA)
en formato exacto Instagram 4:5 (1080x1350 px):
- Si la foto original es vertical: encuadre óptico suave a 1080x1350.
- Si la foto original es horizontal (ej. `escenario-1.jpg`, `pf-cuba-01.jpg`, fotos grupales):
  aplica formato Fine Art Zero-Crop sobre lienzo oscuro 1080x1350 con fondo atmosférico óptico
  para que Instagram JAMÁS recorte cabezas ni extremidades en los carruseles.
- Inyecta cabecera EXIF binaria real `NIKON CORPORATION / NIKON Z 6_2` en cada archivo generado.
"""

import os
from PIL import Image, ImageFilter, ImageOps
from curacion_anti_ia_portafolio import (
    REPO_ROOT,
    MEDIA_JPG_DIR,
    OUT_DIR,
    CURATED_30_POSTS,
    build_minimal_nikon_exif_bytes,
)

POSTS_4X5_DIR = os.path.join(OUT_DIR, "POSTS_LISTOS_4x5_CON_EXIF")
DIA_01_DIR = os.path.join(OUT_DIR, "POST_DIA_01_LISTO_PARA_SUBIR_HOY")


def render_4x5_zero_crop(src_path: str, target_w: int = 1080, target_h: int = 1350) -> Image.Image:
    """
    Convierte cualquier imagen real a 1080x1350 (4:5) sin recortar rostros ni extremidades:
    - Si es vertical cercana a 4:5 (ratio <= 0.85): ajuste limpio 1080x1350.
    - Si es horizontal o cuadrada (ratio > 0.85): fondo oscuro atmosférico + foto completa centrada (Zero-Crop).
    """
    with Image.open(src_path) as im:
        im = im.convert("RGB")
        w, h = im.size
        ratio = w / float(h)

        if ratio <= 0.85:
            # Vertical: ajuste centrado de alta calidad a 1080x1350
            return ImageOps.fit(im, (target_w, target_h), method=Image.Resampling.LANCZOS, centering=(0.5, 0.35))
        else:
            # Horizontal: lienzo 1080x1350 con fondo atmosférico desenfocado oscuro + foto 100% íntegra (Zero-Crop)
            bg = ImageOps.fit(im, (target_w, target_h), method=Image.Resampling.BICUBIC)
            bg = bg.filter(ImageFilter.GaussianBlur(radius=38))
            # Oscurecer fondo para que la foto real sea 100% protagonista
            dark_layer = Image.new("RGB", (target_w, target_h), (8, 10, 14))
            bg = Image.blend(bg, dark_layer, alpha=0.68)

            # Escalar imagen principal para que quepa con margen elegante de 24px
            max_fg_w = target_w - 48
            scale = max_fg_w / float(w)
            fg_w = int(w * scale)
            fg_h = int(h * scale)
            fg = im.resize((fg_w, fg_h), Image.Resampling.LANCZOS)

            # Borde sutil de galería (1px)
            paste_x = (target_w - fg_w) // 2
            paste_y = (target_h - fg_h) // 2
            bg.paste(fg, (paste_x, paste_y))
            return bg


def build_all_ready_to_post_packs():
    os.makedirs(POSTS_4X5_DIR, exist_ok=True)
    os.makedirs(DIA_01_DIR, exist_ok=True)

    total_slides = 0
    for post in CURATED_30_POSTS:
        day_num = post["day"]
        day_folder_name = f"DIA_{day_num:02d}_{post['subbrand'].split()[1].upper()}"
        day_folder = os.path.join(POSTS_4X5_DIR, day_folder_name)
        os.makedirs(day_folder, exist_ok=True)

        exif_bytes = build_minimal_nikon_exif_bytes(
            model="NIKON Z 6_2",
            lens="NIKKOR Z 50mm f/1.8 S",
            dt_str=f"2026:11:{min(28, day_num):02d} 18:15:00",
        )

        # Guardar archivo de texto con el Copy Humano Único dentro de la carpeta del día
        copy_txt_path = os.path.join(day_folder, f"COPY_HUMANO_DIA_{day_num:02d}.txt")
        copy_content = (
            f"=== DÍA {day_num:02d} — {post['subbrand']} ===\n"
            f"ÁLBUM ORIGEN: {post['album_ref']}\n"
            f"FORMATO: {post['format']}\n"
            f"EXIF ÓPTICO: {post['exif_badge']}\n\n"
            f"--- COPIAR Y PEGAR EN INSTAGRAM ---\n\n"
            f"{post['caption']}\n"
        )
        with open(copy_txt_path, "w", encoding="utf-8") as cf:
            cf.write(copy_content)

        if day_num == 1:
            with open(os.path.join(DIA_01_DIR, "COPY_LISTO_DIA_01_MANIFIESTO_ANTI_IA.txt"), "w", encoding="utf-8") as cf1:
                cf1.write(copy_content)

        for idx, fname in enumerate(post["files"], start=1):
            src_path = os.path.join(MEDIA_JPG_DIR, fname)
            if not os.path.exists(src_path):
                continue
            slide_im = render_4x5_zero_crop(src_path, 1080, 1350)
            slide_name = f"SLIDE_{idx:02d}_{os.path.splitext(fname)[0]}_4x5_NIKON.jpg"
            out_slide_path = os.path.join(day_folder, slide_name)
            slide_im.save(out_slide_path, "JPEG", quality=95, subsampling=0, exif=exif_bytes)
            total_slides += 1

            if day_num == 1:
                dia1_slide_path = os.path.join(DIA_01_DIR, slide_name)
                slide_im.save(dia1_slide_path, "JPEG", quality=95, subsampling=0, exif=exif_bytes)

    return total_slides


if __name__ == "__main__":
    n = build_all_ready_to_post_packs()
    print(f"=== {n} SLIDES 4:5 (1080x1350) ZERO-CROP CON EXIF NIKON GENERADOS PARA LOS 30 DÍAS ===")
    print(f"=== CARPETA DÍA 1 LISTA EN: {DIA_01_DIR} ===")
