#!/usr/bin/env python3
"""
La Fábrica ¡WATERS! — Generador Local de Reels Verticales 9:16
Ensambla poses de plastilina 3D, subtítulos estilo Hormozi (#DFB15B / #FF4D4D),
voz en español (o audio personalizado de Chuy / ElevenLabs) y renderiza MP4 H.264.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO/proyectos/waters-serie")
ASSETS_DIR = BASE_DIR / "assets"
RENDERS_DIR = BASE_DIR / "renders"
CALENDAR_JSON = BASE_DIR / "calendario_30_dias.json"

FFMPEG = "/Users/imac/.local/bin/ffmpeg"
FFPROBE = "/Users/imac/.local/bin/ffprobe"
FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

WIDTH, HEIGHT = 1080, 1920
HIGHLIGHT_WORDS = {
    "WATERS", "DINERO", "TIEMPO", "TRABAJO", "CLIENTES", "JUICIO",
    "CLAUDE", "WHATSAPP", "BOT", "DESCUENTO", "DEMANDA", "MULTAS",
    "TRIBUNAL", "VIRTUAL", "404", "CPCNL", "75", "64", "FEJUD",
    "PENSION", "COPIAS", "POSICIONES", "INFORMATICA", "SUGERENCIAS",
    "COMENTA", "GUARDA", "SEGURO", "BLINDAJE", "LEGAL", "PROMPT",
    "TERMINO", "UAPA", "IMASC", "RED", "TEAM", "RFC", "CURP", "CLABE"
}


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    """Carga fuente TrueType con respaldo por defecto."""
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def clean_speech_text(raw: str) -> str:
    """Prepara el texto de guion para síntesis de voz natural en español."""
    txt = re.sub(r"\[[^\]]+\]", "", raw)
    txt = txt.replace("¡", "").replace("!", "! ").replace("—", "")
    txt = txt.replace("Arts.", "artículos").replace("Art.", "artículo")
    txt = txt.replace("PJENL", "Poder Judicial de Nuevo León")
    txt = txt.replace("CPCNL", "Código de Procedimientos Civiles")
    txt = txt.replace("SiC@Vi", "Sicavi")
    txt = txt.replace("TVConvenio.pdf", "convenio del Tribunal Virtual")
    txt = txt.replace("pjenl.gob.mx/Instituto/Tutoriales/", "la página oficial de tutoriales del Instituto")
    txt = txt.replace("WATERS", "guáters")
    return re.sub(r"\s+", " ", txt).strip()


def split_caption_chunks(text: str, max_words: int = 7) -> list[str]:
    """Divide una locución en bloques cortos para subtítulos estilo Hormozi."""
    clean = re.sub(r"\[[^\]]+\]", "", text).replace("—", "").strip()
    if not clean:
        return ["¡¡¡WATERS!!!"]
    # Divide primero por frases fuertes, luego por max_words
    sentences = re.split(r"(?<=[.!?:])\s+", clean)
    chunks = []
    for sent in sentences:
        words = sent.split()
        for i in range(0, len(words), max_words):
            chunk = " ".join(words[i:i + max_words]).strip()
            if chunk:
                chunks.append(chunk)
    return chunks or [clean]


def pose_for_beat_index(idx: int, total: int, cast: str = "v01") -> Path:
    """Asigna la imagen del personaje según cast y fase narrativa."""
    if cast == "v01":
        v01_dir = ASSETS_DIR / "v01"
        p_susto = v01_dir / "pose_01_susto.jpg"
        p_victima = v01_dir / "cameo_victima_v04.jpg"
        p_experto = v01_dir / "v01_pose_02_experto_mascotita.jpg"
        p_cta = v01_dir / "v01_pose_03_cta_mascotita.jpg"
        if idx == 0:
            return p_susto
        elif idx == 1 and p_victima.exists():
            return p_victima
        elif idx == total - 1 and p_cta.exists():
            return p_cta
        elif p_experto.exists():
            return p_experto
        return p_susto

    if idx == 0 or idx == 1:
        return ASSETS_DIR / "pose_01_susto_waters.jpg"
    elif idx == total - 1:
        return ASSETS_DIR / "pose_04_cierre_cta.jpg"
    elif idx == total - 2:
        return ASSETS_DIR / "pose_03_blindaje_experto.jpg"
    return ASSETS_DIR / "pose_02_alerta_riesgo.jpg"


def render_frame(
    pose_path: Path,
    top_badge: str,
    impacts: list[str],
    caption_text: str,
    is_shock_beat: bool,
    out_img: Path,
    zoom_factor: float = 1.0
) -> None:
    """Compone frame maestro 1242x2208 con badge y subtítulos Hormozi listo para zoompan fluido."""
    master_w, master_h = 1242, 2208
    base = Image.open(pose_path).convert("RGB")
    src_w, src_h = base.size
    scale = max(master_w / src_w, master_h / src_h)
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    resized = base.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = max(0, (new_w - master_w) // 2)
    top = max(0, int((new_h - master_h) * 0.25))
    cropped = resized.crop((left, top, left + master_w, top + master_h)).convert("RGBA")

    # Escalamos overlay a 1242x2208 manteniendo proporciones idénticas a 1080x1920
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Gradiente superior e inferior para legibilidad
    for y in range(0, 320):
        alpha = int(175 * (1 - y / 320))
        draw.line([(0, y), (WIDTH, y)], fill=(8, 10, 16, alpha))
    for y in range(HEIGHT - 560, HEIGHT):
        alpha = int(220 * ((y - (HEIGHT - 560)) / 560))
        draw.line([(0, y), (WIDTH, y)], fill=(8, 10, 16, alpha))

    font_badge = load_font(FONT_BLACK, 34)
    font_sub = load_font(FONT_BOLD, 26)
    font_cap = load_font(FONT_BLACK, 54 if not is_shock_beat else 118)

    pill_color = (220, 38, 38, 235) if is_shock_beat else (15, 23, 42, 225)
    border_col = (255, 255, 255, 230) if is_shock_beat else (223, 177, 91, 240)
    draw.rounded_rectangle([(60, 110), (WIDTH - 60, 215)], radius=24, fill=pill_color, outline=border_col, width=4)
    draw.text((WIDTH // 2, 142), top_badge.upper(), font=font_badge, fill=(255, 255, 255, 255), anchor="mm")
    impact_line = "  |  ".join([re.sub(r"[^\w\sáéíóúÁÉÍÓÚñÑ]", "", x).strip().upper() for x in impacts[:4]])
    draw.text((WIDTH // 2, 188), impact_line, font=font_sub, fill=(223, 177, 91, 255), anchor="mm")

    if is_shock_beat:
        txt = "¡¡¡WATERS!!!"
        draw.text((WIDTH // 2 + 6, 470 + 6), txt, font=font_cap, fill=(0, 0, 0, 230), anchor="mm")
        draw.text((WIDTH // 2, 470), txt, font=font_cap, fill=(255, 215, 64, 255), stroke_width=8, stroke_fill=(180, 20, 20, 255), anchor="mm")

        hook_box_font = load_font(FONT_BLACK, 44)
        draw.rounded_rectangle([(80, 1340), (WIDTH - 80, 1510)], radius=28, fill=(10, 14, 23, 225), outline=(255, 77, 77, 255), width=5)
        draw.text((WIDTH // 2, 1425), "SUSPIRO DE PÁNICO + ALERTA", font=hook_box_font, fill=(255, 255, 255, 255), anchor="mm")
    else:
        lines = textwrap.wrap(caption_text.upper(), width=22)[:4]
        line_h = 68
        box_h = max(140, len(lines) * line_h + 54)
        box_top = 1480 - box_h // 2
        box_bot = box_top + box_h
        draw.rounded_rectangle(
            [(64, box_top), (WIDTH - 64, box_bot)],
            radius=28,
            fill=(10, 14, 23, 228),
            outline=(223, 177, 91, 210),
            width=4
        )
        y_cursor = box_top + 48
        for line in lines:
            words = line.split()
            word_widths = []
            space_w = draw.textlength(" ", font=font_cap)
            for w in words:
                word_widths.append(draw.textlength(w, font=font_cap))
            total_w = sum(word_widths) + space_w * max(0, len(words) - 1)
            x_cursor = (WIDTH - total_w) / 2
            for w, ww in zip(words, word_widths):
                clean_w = re.sub(r"[^\wÁÉÍÓÚÑ]", "", w)
                color = (223, 177, 91, 255) if clean_w in HIGHLIGHT_WORDS else (255, 255, 255, 255)
                if clean_w in {"WATERS", "404", "MULTAS", "DESMADRE", "PELIGRO", "ARNESES", "GUARDRAILS", "MARKETPLACE"}:
                    color = (255, 85, 85, 255)
                draw.text((x_cursor + 3, y_cursor + 3), w, font=font_cap, fill=(0, 0, 0, 220), anchor="lm")
                draw.text((x_cursor, y_cursor), w, font=font_cap, fill=color, anchor="lm")
                x_cursor += ww + space_w
            y_cursor += line_h

    overlay_scaled = overlay.resize((master_w, master_h), Image.Resampling.LANCZOS)
    combined = Image.alpha_composite(cropped, overlay_scaled).convert("RGB")
    combined.save(out_img, quality=94)


def render_motion_segment(img_path: Path, dur: float, z0: float, z1: float, shake: bool, out_ts: Path) -> None:
    """Convierte un fotograma maestro en clip MP4 animado continuo a 30fps con zoompan/shake."""
    frames = max(15, int(round(dur * 30)))
    dz = z1 - z0
    x_expr = "iw/2-(iw/zoom/2)"
    if shake:
        x_expr = "iw/2-(iw/zoom/2)+12*sin(on*1.3)"
    vf = (
        f"zoompan=z='{z0:.4f}+({dz:.4f})*on/{frames}':"
        f"x='{x_expr}':y='ih/2-(ih/zoom/2)':"
        f"d={frames}:s={WIDTH}x{HEIGHT}:fps=30"
    )
    if shake:
        vf += ",fade=t=in:st=0:d=0.12:color=white"
    subprocess.run([
        FFMPEG, "-y", "-i", str(img_path),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "21", "-pix_fmt", "yuv420p",
        str(out_ts)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_duration(media_path: Path) -> float:
    """Obtiene la duración exacta de audio o video vía ffprobe."""
    res = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(media_path)],
        capture_output=True, text=True, check=True
    )
    return float(res.stdout.strip())


def build_gasp_sfx(out_wav: Path) -> None:
    """Sintetiza sonido breve de inhalación/alerta cómica antes de ¡WATERS!."""
    subprocess.run([
        FFMPEG, "-y", "-f", "lavfi",
        "-i", "anoisesrc=d=0.45:c=white:a=0.15,bandpass=f=1200:w=800,afade=t=in:ss=0:d=0.25,afade=t=out:st=0.32:d=0.13",
        "-f", "lavfi", "-i", "sine=f=520:d=0.28,afade=t=out:st=0.12:d=0.16",
        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[aout]",
        "-map", "[aout]", "-ar", "44100", "-ac", "1", str(out_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def synthesize_tts(text: str, out_wav: Path, voice: str = "Juan", rate: int = 195) -> None:
    """Genera locución en español con macOS say y la normaliza a WAV 44.1kHz."""
    aiff_tmp = out_wav.with_suffix(".aiff")
    subprocess.run(["/usr/bin/say", "-v", voice, "-r", str(rate), "-o", str(aiff_tmp), text], check=True)
    subprocess.run([
        FFMPEG, "-y", "-i", str(aiff_tmp), "-ar", "44100", "-ac", "1", str(out_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    aiff_tmp.unlink(missing_ok=True)


def build_silent_audio(out_wav: Path, duration_sec: float) -> None:
    """Genera pista silenciosa de duración exacta para modo --solo-video / --sin-voz-robot."""
    subprocess.run([
        FFMPEG, "-y", "-f", "lavfi",
        "-i", f"anullsrc=r=44100:cl=mono",
        "-t", f"{duration_sec:.3f}", str(out_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def build_impact_plus_silence(out_wav: Path, duration_sec: float) -> None:
    """Genera impacto sutil de golpe/alerta al 0:00 seguido de silencio limpio (0 voz robótica)."""
    sfx = out_wav.with_name("impact_00.wav")
    sil = out_wav.with_name("silence_tail.wav")
    rem = max(1.0, duration_sec - 0.55)
    subprocess.run([
        FFMPEG, "-y", "-f", "lavfi",
        "-i", "sine=f=180:d=0.18,afade=t=out:st=0.05:d=0.13",
        "-f", "lavfi", "-i", "sine=f=520:d=0.37,afade=t=out:st=0.10:d=0.27",
        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1,volume=0.35[aout]",
        "-map", "[aout]", "-ar", "44100", "-ac", "1", str(sfx)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run([
        FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
        "-t", f"{rem:.3f}", str(sil)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run([
        FFMPEG, "-y", "-i", str(sfx), "-i", str(sil),
        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[aout]",
        "-map", "[aout]", str(out_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sfx.unlink(missing_ok=True)
    sil.unlink(missing_ok=True)


def assemble_episode(
    episode: dict,
    out_mp4: Path,
    external_audio: Path | None = None,
    voice: str = "Juan",
    solo_video: bool = False,
    cast: str = "v01"
) -> None:
    """Construye el video MP4 completo para un episodio del calendario."""
    RENDERS_DIR.mkdir(parents=True, exist_ok=True)
    beats = list(episode["guion"].items())
    total_beats = len(beats)
    top_badge = f"EP. {episode['dia']:02d} · {episode['pilar']}"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        slide_entries = []  # list of (img_path, duration)
        beat_audio_files = []

        # Preparar audios y duraciones por beat
        beat_durations = []
        if solo_video:
            beat_durations = []
            for b_idx, (_, beat_text) in enumerate(beats):
                if b_idx == 0:
                    beat_durations.append(2.2)
                else:
                    words = max(8, len(beat_text.split()))
                    beat_durations.append(round(words / 2.6, 2))
            full_audio = tmp / "solo_impact_silence.wav"
            build_impact_plus_silence(full_audio, sum(beat_durations))
        elif external_audio is None:
            for b_idx, (beat_label, beat_text) in enumerate(beats):
                wav_path = tmp / f"beat_{b_idx}.wav"
                if b_idx == 0:
                    sfx_wav = tmp / "gasp_sfx.wav"
                    shout_wav = tmp / "waters_shout.wav"
                    build_gasp_sfx(sfx_wav)
                    synthesize_tts("¡Guáters!", shout_wav, voice=voice, rate=185)
                    subprocess.run([
                        FFMPEG, "-y", "-i", str(sfx_wav), "-i", str(shout_wav),
                        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[aout]",
                        "-map", "[aout]", str(wav_path)
                    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    speech = clean_speech_text(beat_text)
                    synthesize_tts(speech, wav_path, voice=voice, rate=195)
                beat_audio_files.append(wav_path)
                beat_durations.append(get_duration(wav_path))

            # Concatenar audio completo
            full_audio = tmp / "full_audio.wav"
            concat_txt = tmp / "audio_concat.txt"
            concat_txt.write_text("\n".join([f"file '{p}'" for p in beat_audio_files]), encoding="utf-8")
            subprocess.run([
                FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_txt),
                "-c", "copy", str(full_audio)
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            full_audio = external_audio
            total_dur = get_duration(full_audio)
            char_weights = [max(10, len(t)) for _, t in beats]
            weight_sum = sum(char_weights)
            beat_durations = [total_dur * (w / weight_sum) for w in char_weights]

        # Renderizar tarjetas y segmentos animados continuos (30fps zoompan + shake en shock)
        clip_files = []
        slide_idx = 0
        for b_idx, ((beat_label, beat_text), b_dur) in enumerate(zip(beats, beat_durations)):
            pose_path = pose_for_beat_index(b_idx, total_beats, cast=cast)
            if b_idx == 0:
                img_path = tmp / f"slide_{slide_idx:03d}.jpg"
                clip_path = tmp / f"clip_{slide_idx:03d}.mp4"
                render_frame(pose_path, top_badge, episode["impactos"], "¡¡¡WATERS!!!", True, img_path)
                render_motion_segment(img_path, b_dur, 1.00, 1.13, shake=True, out_ts=clip_path)
                clip_files.append(clip_path)
                slide_idx += 1
            else:
                chunks = split_caption_chunks(beat_text, max_words=7)
                word_counts = [max(1, len(c.split())) for c in chunks]
                wc_sum = sum(word_counts)
                # Alterna push-in (1.00->1.09) y pull-out (1.09->1.01) continuo por beat
                z_a, z_b = (1.00, 1.09) if (b_idx % 2 == 1) else (1.09, 1.01)
                t_acc = 0.0
                for c, wc in zip(chunks, word_counts):
                    c_dur = b_dur * (wc / wc_sum)
                    p0 = t_acc / max(0.1, b_dur)
                    p1 = (t_acc + c_dur) / max(0.1, b_dur)
                    z0 = z_a + (z_b - z_a) * p0
                    z1 = z_a + (z_b - z_a) * p1
                    t_acc += c_dur
                    img_path = tmp / f"slide_{slide_idx:03d}.jpg"
                    clip_path = tmp / f"clip_{slide_idx:03d}.mp4"
                    render_frame(pose_path, top_badge, episode["impactos"], c, False, img_path)
                    render_motion_segment(img_path, c_dur, z0, z1, shake=False, out_ts=clip_path)
                    clip_files.append(clip_path)
                    slide_idx += 1

        # Unir clips animados sin recomprimir video y muxear audio
        vid_concat = tmp / "video_concat.txt"
        vid_concat.write_text("\n".join([f"file '{c}'" for c in clip_files]), encoding="utf-8")

        subprocess.run([
            FFMPEG, "-y",
            "-f", "concat", "-safe", "0", "-i", str(vid_concat),
            "-i", str(full_audio),
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
            str(out_mp4)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def parse_range(lote_str: str) -> list[int]:
    """Convierte rangos tipo '1-5' o '1,2,3' en lista de días."""
    days = []
    for part in lote_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            days.extend(range(int(start), int(end) + 1))
        elif part:
            days.append(int(part))
    return days


def main():
    parser = argparse.ArgumentParser(description="La Fábrica ¡WATERS! — Generador automático de Reels 9:16")
    parser.add_argument("--dia", type=int, default=1, help="Número de día en el calendario de 30 días (1..30)")
    parser.add_argument("--lote", type=str, default=None, help="Rango o lista de días para producción nocturna (ej. 1-30)")
    parser.add_argument("--output", type=str, default=None, help="Ruta de salida .mp4")
    parser.add_argument("--audio", type=str, default=None, help="Audio personalizado opcional (ej. voz grabada o ElevenLabs)")
    parser.add_argument("--voice", type=str, default="Juan", help="Voz macOS say (por defecto Juan es_MX)")
    parser.add_argument("--cast", type=str, default="v01", choices=["v01", "v00"], help="Elenco visual (v01 Hoodie + Mascotita, o v00 Saco Azul)")
    parser.add_argument("--solo-video", "--sin-voz-robot", dest="solo_video", action="store_true", help="Renderiza con pista con golpe inicial sin voz robótica")
    args = parser.parse_args()

    episodes = json.loads(CALENDAR_JSON.read_text(encoding="utf-8"))
    target_days = parse_range(args.lote) if args.lote else [args.dia]

    for dia in target_days:
        ep = next((e for e in episodes if e["dia"] == dia), None)
        if ep is None:
            print(f"[AVISO] Día {dia} no encontrado en {CALENDAR_JSON}, omitiendo.")
            continue
        out_path = Path(args.output) if (args.output and len(target_days) == 1) else (RENDERS_DIR / f"WATERS_{ep['dia']:03d}.mp4")
        ext_audio = Path(args.audio) if (args.audio and len(target_days) == 1) else None
        print(f"[Fábrica ¡WATERS!] Renderizando Día {ep['dia']} (cast={args.cast}): {ep['titulo_viral']} -> {out_path}")
        assemble_episode(ep, out_path, external_audio=ext_audio, voice=args.voice, solo_video=args.solo_video, cast=args.cast)
        dur = get_duration(out_path)
        print(f"[OK] Video generado en {out_path} ({dur:.2f}s)")


if __name__ == "__main__":
    main()
