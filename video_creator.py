#!/usr/bin/env python3
"""
Video Creator Engine para PHOTOOKIS
Genera automáticamente:
1. Video TikTok / Reels (9:16, 1080x1920, cortes rápidos de 1s con overlays de texto)
2. Video YouTube (16:9, 1920x1080, ritmo narrativo suave de 2.5s con disolvencias)
Utiliza ffmpeg para el renderizado acelerado en Mac.
"""

import os
import sys
import glob
import subprocess
from PIL import Image, ImageDraw, ImageFont

def create_slideshow_video(image_folder, output_path, aspect_ratio=(1080, 1920), duration_per_photo=1.0, title="PHARMACY EVENT"):
    """
    Genera un archivo MP4 combinando las mejores fotos usando ffmpeg.
    """
    extensions = ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG")
    images = []
    for ext in extensions:
        images.extend(glob.glob(os.path.join(image_folder, ext)))
    images = sorted(list(set(images)))

    if not images:
        print(f"No hay imágenes en {image_folder} para generar video.")
        return False

    temp_dir = os.path.join(os.path.dirname(output_path), "temp_frames")
    os.makedirs(temp_dir, exist_ok=True)
    target_w, target_h = aspect_ratio

    print(f"Preparando {len(images)} fotogramas para {output_path} ({target_w}x{target_h})...")

    # Preparar frames con el aspecto exacto y texto
    frame_files = []
    for idx, img_p in enumerate(images[:25]): # Máximo 25 fotos para mantener dinámica ágil
        with Image.open(img_p) as img:
            # Crop al centro
            w, h = img.size
            aspect = target_w / float(target_h)
            curr_aspect = w / float(h)
            if curr_aspect > aspect:
                nw = int(h * aspect)
                off = (w - nw) // 2
                img = img.crop((off, 0, off + nw, h))
            else:
                nh = int(w / aspect)
                off = (h - nh) // 2
                img = img.crop((0, off, w, off + nh))

            img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            
            # Superposición gráfica sutil
            draw = ImageDraw.Draw(img)
            # Viñeta inferior oscura
            gradient_box = [0, int(target_h * 0.82), target_w, target_h]
            draw.rectangle(gradient_box, fill=(7, 8, 11, 210))
            
            # Texto básico
            sub_text = f"{title} · FOTO #{idx+1}"
            draw.text((40, target_h - 100), sub_text, fill=(255, 255, 255))
            draw.text((40, target_h - 60), "PHOTOOKIS STUDIO · COBERTURA EXPRESS", fill=(0, 240, 255))

            frame_path = os.path.join(temp_dir, f"frame_{idx:04d}.jpg")
            img.save(frame_path, quality=90)
            frame_files.append(frame_path)

    # Crear lista de concatenación para ffmpeg
    concat_txt = os.path.join(temp_dir, "input.txt")
    with open(concat_txt, "w") as f:
        for f_path in frame_files:
            f.write(f"file '{os.path.abspath(f_path)}'\n")
            f.write(f"duration {duration_per_photo}\n")
        # Repetir último frame para duración de ffmpeg
        if frame_files:
            f.write(f"file '{os.path.abspath(frame_files[-1])}'\n")

    fps = 30
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_txt,
        "-vf", f"fps={fps},format=yuv420p",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        output_path
    ]

    print(f"Renderizando MP4 con ffmpeg: {output_path}...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Limpieza
    for fp in frame_files:
        try: os.remove(fp)
        except: pass
    try: os.remove(concat_txt)
    except: pass
    try: os.rmdir(temp_dir)
    except: pass

    if res.returncode == 0:
        print(f"✅ Video generado exitosamente: {output_path}")
        return True
    else:
        print(f"❌ Error en ffmpeg: {res.stderr.decode('utf-8')[:300]}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 video_creator.py <carpeta_fotos> <carpeta_salida_videos>")
        sys.exit(1)

    in_f = sys.argv[1]
    out_f = sys.argv[2]
    os.makedirs(out_f, exist_ok=True)

    tiktok_video = os.path.join(out_f, "PHARMACY_TIKTOK_9x16.mp4")
    youtube_video = os.path.join(out_f, "PHARMACY_YOUTUBE_16x9.mp4")

    # 1. TikTok 9:16 (1.0s por foto, dinámico)
    create_slideshow_video(in_f, tiktok_video, aspect_ratio=(1080, 1920), duration_per_photo=1.0, title="PHARMACY SUMMIT 2026")

    # 2. YouTube 16:9 (2.5s por foto, narrativo)
    create_slideshow_video(in_f, youtube_video, aspect_ratio=(1920, 1080), duration_per_photo=2.5, title="PHARMACY EVENT RECAP")
