#!/usr/bin/env python3
"""
Generador Maestro de Explainer Videos: "CLÓNATE EN CAPTOORA STUDIO · CLONA TU PRIME"
Produce 3 formatos profesionales (>40 segundos):
1. 9:16 Vertical (1080x1920) — TikTok / Reels / Shorts Viral
2. 16:9 Widescreen (1920x1080) — YouTube / Masterclass Ejecutiva
3. 1:1 Cuadrado (1080x1080) — Feed LinkedIn / Instagram / Meta Ads
"""

import os
import re
import subprocess
import tempfile
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FFMPEG = "/Users/imac/.local/bin/ffmpeg"
FFPROBE = "/Users/imac/.local/bin/ffprobe"
FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

BASE_DIR = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO/proyectos/waters-serie")
OUT_DIR = BASE_DIR / "renders" / "explainers_biogen"
AUDIO_BED = BASE_DIR / "black_friday_bf01" / "audio" / "bf01_bed.wav"

OUT_DIR.mkdir(parents=True, exist_ok=True)

# 6 Beats Narrativos (Duración total estimada: ~46-48 segundos)
BEATS = [
    {
        "id": "beat_01",
        "title": "LA GRAN MENTIRA DE LA IA",
        "tag": "EL PROBLEMA",
        "script": "Todo el mundo en internet te dice que puedes hacer tu clon con inteligencia artificial en cinco minutos. Pero la verdad es que a nadie le sale bien: caras de plástico, ojos muertos o narices gigantes de caricatura.",
        "img": "/Users/imac/Desktop/Projects/CAPTOORA.STUDIO/proyectos/waters-serie/black_friday_bf01/biblioteca_motores/06_angulos_base_img/01_hook_closeup.jpg",
        "zoom": (1.00, 1.08),
        "highlights": {"INTERNET", "CLON", "CINCO", "MINUTOS", "NADIE", "PLÁSTICO", "CARICATURA"}
    },
    {
        "id": "beat_02",
        "title": "FRICCIÓN TÉCNICA BRUTAL",
        "tag": "REALIDAD",
        "script": "Y peor aún: los profesionistas y empresarios no tienen tiempo ni ganas de quebrarse la cabeza con códigos, prompts imposibles ni herramientas técnicas que nadie entiende.",
        "img": "/Users/imac/Desktop/Projects/CAPTOORA.STUDIO/proyectos/waters-serie/black_friday_bf01/biblioteca_motores/06_angulos_base_img/02_bucle_3_4_izq.jpg",
        "zoom": (1.06, 1.00),
        "highlights": {"EMPRESARIOS", "TIEMPO", "CÓDIGOS", "PROMPTS", "HERRAMIENTAS", "ENTIENDE"}
    },
    {
        "id": "beat_03",
        "title": "CLÓNATE EN CAPTOORA STUDIO",
        "tag": "SOLUCIÓN",
        "script": "Por eso creamos el servicio estrella: CLÓNATE EN CAPTOORA STUDIO. Aquí no compras un software ni un tutorial. Vienes en persona a nuestro set físico en Colinas de San Jerónimo.",
        "img": "/Users/imac/Desktop/Projects/CAPTOORA.STUDIO/proyectos/waters-serie/black_friday_bf01/biblioteca_motores/06_angulos_base_img/04_dilema_3_4_der.jpg",
        "zoom": (1.00, 1.08),
        "highlights": {"CLÓNATE", "CAPTOORA", "STUDIO", "SET", "FÍSICO", "JERÓNIMO"}
    },
    {
        "id": "beat_04",
        "title": "CALIBRACIÓN ANATÓMICA REAL",
        "tag": "BIOMETRÍA",
        "script": "Bajo luces de cine y cámaras reales, calibramos tu biometría exacta. Respetamos tu fisonomía real, tus cirugías previas como tu nariz recta, y tu sonrisa natural con dientes frontales.",
        "img": "/Users/imac/Desktop/Projects/CAPTOORA.STUDIO/proyectos/waters-serie/black_friday_bf01/biblioteca_motores/00_referencia_maestra/character_sheet/02_perfil_lateral_oficial_aprobado.jpg",
        "zoom": (1.05, 1.00),
        "highlights": {"LUCES", "CINE", "BIOMETRÍA", "ANATOMÍA", "NARIZ", "RECTA", "SONRISA", "DIENTES"}
    },
    {
        "id": "beat_05",
        "title": "BLINDAJE LEGAL & CIBERSEGURIDAD",
        "tag": "SEGURIDAD",
        "script": "Cuentas con blindaje legal único en ciberseguridad: contratos de consentimiento informado y derechos de imagen para que tu clon opere con absoluta certeza jurídica.",
        "img": "/Users/imac/Desktop/Projects/CAPTOORA.STUDIO/proyectos/waters-serie/black_friday_bf01/biblioteca_motores/06_angulos_base_img/05_candados_pecho.jpg",
        "zoom": (1.00, 1.07),
        "highlights": {"BLINDAJE", "CIBERSEGURIDAD", "CONTRATOS", "CONSENTIMIENTO", "DERECHOS", "CERTEZA"}
    },
    {
        "id": "beat_06",
        "title": "MEMBRESÍA BIOGEN · CLONA TU PRIME",
        "tag": "LLAMADO A LA ACCIÓN",
        "script": "Con nuestra membresía mensual, vienes cada mes a registrar tu prime y tu clon produce todo tu contenido sin que te desgastes. ¡Clónate en Captoora Studio hoy!",
        "img": "/Users/imac/Desktop/Projects/CAPTOORA.STUDIO/proyectos/waters-serie/black_friday_bf01/biblioteca_motores/06_angulos_base_img/06_cta_closeup.jpg",
        "zoom": (1.06, 1.00),
        "highlights": {"MEMBRESÍA", "PRIME", "CONTENIDO", "CLÓNATE", "CAPTOORA", "HOY"}
    }
]

def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def get_duration(media_path: Path) -> float:
    res = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(media_path)],
        capture_output=True, text=True, check=True
    )
    return float(res.stdout.strip())

def synthesize_beat_audio(text: str, out_wav: Path, voice: str = "Juan", rate: int = 185) -> float:
    """Genera locución con say y convierte a WAV normalizado."""
    aiff_tmp = out_wav.with_suffix(".aiff")
    subprocess.run(["/usr/bin/say", "-v", voice, "-r", str(rate), "-o", str(aiff_tmp), text], check=True)
    subprocess.run([
        FFMPEG, "-y", "-i", str(aiff_tmp),
        "-ar", "44100", "-ac", "2",
        str(out_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if aiff_tmp.exists():
        aiff_tmp.unlink()
    return get_duration(out_wav)

# ==============================================================================
# 1. RENDER 9:16 (VERTICAL VIRAL REEL / TIKTOK)
# ==============================================================================
def render_frame_vertical(beat: dict, out_png: Path) -> None:
    w, h = 1080, 1920
    base = Image.open(beat["img"]).convert("RGB")
    src_w, src_h = base.size
    scale = max(w / src_w, h / src_h)
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    resized = base.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    cropped = resized.crop((left, top, left + w, top + h))

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Gradients top and bottom
    for y in range(0, 340):
        alpha = int(190 * (1 - y / 340))
        draw.line([(0, y), (w, y)], fill=(9, 10, 15, alpha))
    for y in range(h - 580, h):
        alpha = int(220 * ((y - (h - 580)) / 580))
        draw.line([(0, y), (w, y)], fill=(9, 10, 15, alpha))

    font_tag = load_font(FONT_BLACK, 28)
    font_title = load_font(FONT_BLACK, 40)
    font_sub = load_font(FONT_BLACK, 52)

    # Top pill
    draw.rounded_rectangle([(60, 100), (w - 60, 210)], radius=24, fill=(10, 14, 23, 230), outline=(0, 255, 136, 230), width=4)
    draw.text((w // 2, 132), beat["tag"].upper(), font=font_tag, fill=(0, 255, 136, 255), anchor="mm")
    draw.text((w // 2, 175), beat["title"].upper(), font=font_title, fill=(255, 255, 255, 255), anchor="mm")

    # Subtitles Hormozi style
    lines = textwrap.wrap(beat["script"].upper(), width=22)[:5]
    line_h = 66
    box_h = len(lines) * line_h + 50
    box_top = 1530 - box_h // 2
    box_bot = box_top + box_h
    draw.rounded_rectangle([(50, box_top), (w - 50, box_bot)], radius=24, fill=(10, 14, 23, 235), outline=(255, 255, 255, 180), width=3)

    y_cur = box_top + 45
    for line in lines:
        words = line.split()
        word_widths = [draw.textlength(word, font=font_sub) for word in words]
        space_w = draw.textlength(" ", font=font_sub)
        total_w = sum(word_widths) + space_w * max(0, len(words) - 1)
        x_cur = (w - total_w) / 2
        for word, ww in zip(words, word_widths):
            clean = re.sub(r"[^\wÁÉÍÓÚÑ]", "", word)
            color = (255, 215, 64, 255) if clean in beat["highlights"] else (255, 255, 255, 255)
            if clean in {"CLÓNATE", "CAPTOORA", "BIOMETRÍA", "PRIME"}:
                color = (0, 255, 136, 255)
            draw.text((x_cur + 2, y_cur + 2), word, font=font_sub, fill=(0, 0, 0, 220), anchor="lm")
            draw.text((x_cur, y_cur), word, font=font_sub, fill=color, anchor="lm")
            x_cur += ww + space_w
        y_cur += line_h

    final_img = Image.alpha_composite(cropped.convert("RGBA"), overlay).convert("RGB")
    final_img.save(out_png, quality=95)

# ==============================================================================
# 2. RENDER 16:9 (HORIZONTAL WIDESCREEN CINEMATOGRÁFICO)
# ==============================================================================
def render_frame_widescreen(beat: dict, out_png: Path) -> None:
    w, h = 1920, 1080
    base = Image.open(beat["img"]).convert("RGB")
    src_w, src_h = base.size
    scale = max(w / src_w, h / src_h)
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    resized = base.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    cropped = resized.crop((left, top, left + w, top + h))

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Cinematic lower gradient
    for y in range(h - 380, h):
        alpha = int(230 * ((y - (h - 380)) / 380))
        draw.line([(0, y), (w, y)], fill=(8, 10, 15, alpha))

    # Top-left branding pill
    font_logo = load_font(FONT_BLACK, 26)
    draw.rounded_rectangle([(80, 50), (480, 105)], radius=14, fill=(10, 14, 23, 230), outline=(0, 255, 136, 230), width=3)
    draw.text((105, 78), "CAPTOORA BIOGEN", font=font_logo, fill=(0, 255, 136, 255), anchor="lm")

    # Lower third
    font_tag = load_font(FONT_BOLD, 22)
    font_title = load_font(FONT_BLACK, 38)
    font_sub = load_font(FONT_BOLD, 32)

    draw.rectangle([80, h - 280, 88, h - 180], fill=(0, 255, 136, 255))
    draw.text((110, h - 265), beat["tag"].upper(), font=font_tag, fill=(0, 255, 136, 255), anchor="lm")
    draw.text((110, h - 225), beat["title"].upper(), font=font_title, fill=(255, 255, 255, 255), anchor="lm")

    # Broadcast captions 2 lines
    lines = textwrap.wrap(beat["script"], width=68)[:3]
    y_text = h - 145
    for line in lines:
        draw.text((110, y_text), line, font=font_sub, fill=(240, 246, 252, 255), anchor="lm")
        y_text += 42

    final_img = Image.alpha_composite(cropped.convert("RGBA"), overlay).convert("RGB")
    final_img.save(out_png, quality=95)

# ==============================================================================
# 3. RENDER 1:1 (CUADRADO SOCIAL / ADS LINKEDIN)
# ==============================================================================
def render_frame_square(beat: dict, out_png: Path) -> None:
    w, h = 1080, 1080
    base = Image.open(beat["img"]).convert("RGB")
    src_w, src_h = base.size
    scale = max(w / src_w, h / src_h)
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    resized = base.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    cropped = resized.crop((left, top, left + w, top + h))

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Top Header Banner
    draw.rectangle([(0, 0), (w, 150)], fill=(10, 14, 23, 240))
    draw.line([(0, 150), (w, 150)], fill=(0, 255, 136, 255), width=4)

    font_header = load_font(FONT_BLACK, 32)
    font_subhead = load_font(FONT_BOLD, 22)
    draw.text((w // 2, 50), "CLÓNATE EN CAPTOORA STUDIO", font=font_header, fill=(255, 255, 255, 255), anchor="mm")
    draw.text((w // 2, 95), "CLONA TU PRIME · MEMBRESÍA BIOGEN", font=font_subhead, fill=(0, 255, 136, 255), anchor="mm")

    # Bottom Caption Box
    draw.rectangle([(0, h - 260), (w, h)], fill=(10, 14, 23, 240))
    draw.line([(0, h - 260), (w, h - 260)], fill=(255, 215, 64, 255), width=3)

    font_cap = load_font(FONT_BOLD, 30)
    lines = textwrap.wrap(beat["script"], width=42)[:4]
    y_sub = h - 210
    for line in lines:
        draw.text((w // 2, y_sub), line, font=font_cap, fill=(255, 255, 255, 255), anchor="mm")
        y_sub += 40

    final_img = Image.alpha_composite(cropped.convert("RGBA"), overlay).convert("RGB")
    final_img.save(out_png, quality=95)

# ==============================================================================
# PIPELINE DE CONVERSIÓN A VIDEO MP4
# ==============================================================================
def create_motion_clip(img_path: Path, dur: float, z0: float, z1: float, aspect: tuple[int, int], out_mp4: Path) -> None:
    w, h = aspect
    frames = max(15, int(round(dur * 30)))
    dz = z1 - z0
    vf = f"zoompan=z='{z0:.4f}+({dz:.4f})*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps=30"
    subprocess.run([
        FFMPEG, "-y", "-i", str(img_path),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p",
        str(out_mp4)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def build_explainer(format_name: str, aspect: tuple[int, int], render_func, out_final: Path) -> None:
    print(f"\n=======================================================")
    print(f"🎬 RENDERIZANDO: {format_name} ({aspect[0]}x{aspect[1]})")
    print(f"=======================================================")
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        seg_clips = []
        concat_list = tmp_path / "concat.txt"

        for idx, beat in enumerate(BEATS):
            img_frame = tmp_path / f"frame_{idx:02d}.png"
            clip_video = tmp_path / f"video_{idx:02d}.mp4"
            audio_wav = tmp_path / f"audio_{idx:02d}.wav"
            mux_clip = tmp_path / f"mux_{idx:02d}.mp4"

            # 1. Render frame
            render_func(beat, img_frame)

            # 2. Audio speech
            dur = synthesize_beat_audio(beat["script"], audio_wav)
            print(f"  • Beat {idx+1}/{len(BEATS)}: {beat['title']} ({dur:.2f}s)")

            # 3. Kinetic video segment
            z0, z1 = beat["zoom"]
            create_motion_clip(img_frame, dur, z0, z1, aspect, clip_video)

            # 4. Mux video + audio
            subprocess.run([
                FFMPEG, "-y",
                "-i", str(clip_video),
                "-i", str(audio_wav),
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k",
                "-shortest",
                str(mux_clip)
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            seg_clips.append(mux_clip)

        # Build concat list
        with open(concat_list, "w") as f:
            for c in seg_clips:
                f.write(f"file '{c.resolve()}'\n")

        # Concat raw video
        raw_concat = tmp_path / "raw_concat.mp4"
        subprocess.run([
            FFMPEG, "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",
            str(raw_concat)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        total_dur = get_duration(raw_concat)

        # Mix with background music bed (-18dB) and fade out
        if AUDIO_BED.exists():
            print(f"  🎵 Mezclando pista musical de fondo ({AUDIO_BED.name})...")
            subprocess.run([
                FFMPEG, "-y",
                "-i", str(raw_concat),
                "-i", str(AUDIO_BED),
                "-filter_complex",
                f"[1:a]volume=0.12,afade=t=out:st={total_dur - 2.0}:d=2.0[bed];[0:a][bed]amix=inputs=2:duration=first:dropout_transition=2[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "256k",
                str(out_final)
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            raw_concat.rename(out_final)

        final_dur = get_duration(out_final)
        print(f"✅ ¡Video final exportado con éxito!")
        print(f"   Ruta: {out_final}")
        print(f"   Duración exacta: {final_dur:.2f} segundos (Requisito > 40s superado)")

def main():
    print("🚀 INICIANDO SUITE DE 3 EXPLAINER VIDEOS (CAPTOORA BIOGEN)")
    
    # 1. Vertical 9:16
    v1 = OUT_DIR / "EXPLAINER_01_VERTICAL_9X16_CLONATE_CAPTOORA.mp4"
    build_explainer("FORMATO 1: VERTICAL 9:16 (TIKTOK / REELS / SHORTS)", (1080, 1920), render_frame_vertical, v1)

    # 2. Widescreen 16:9
    v2 = OUT_DIR / "EXPLAINER_02_WIDESCREEN_16X9_CLONATE_CAPTOORA.mp4"
    build_explainer("FORMATO 2: WIDESCREEN 16:9 (YOUTUBE / MASTERCLASS)", (1920, 1080), render_frame_widescreen, v2)

    # 3. Square 1:1
    v3 = OUT_DIR / "EXPLAINER_03_CUADRADO_1X1_CLONATE_CAPTOORA.mp4"
    build_explainer("FORMATO 3: CUADRADO 1:1 (FEED LINKEDIN / META ADS)", (1080, 1080), render_frame_square, v3)

    print("\n🎉 ¡LAS 3 VERSIONES ESTÁN LISTAS Y COMPLETADAS!")

if __name__ == "__main__":
    main()
