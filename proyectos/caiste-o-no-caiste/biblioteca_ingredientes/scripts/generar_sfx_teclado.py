#!/usr/bin/env python3
"""
Genera el Pack #1 de SFX de Teclado Mecánico Cremoso ("thocky / creamy PBT")
y efectos UI limpios para la Biblioteca de Ingredientes de ¿Caíste o no caíste?.
Usa exclusivamente Python stdlib + FFmpeg (48 kHz PCM WAV + MP3 192k).
"""
import math
import random
import shutil
import subprocess
import wave
from array import array
from pathlib import Path

SR = 48000
FFMPEG = "/Users/imac/.local/bin/ffmpeg"
FFPROBE = "/Users/imac/.local/bin/ffprobe"

BASE_DIR = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO/proyectos/caiste-o-no-caiste/biblioteca_ingredientes")
OUT_DIR = BASE_DIR / "01_sfx_teclado_mecanico"
TPL_ASSETS_DIR = BASE_DIR / "04_plantilla_texto_dinamico_teclado/assets"


def synth_creamy_key(rng: random.Random, is_enter: bool = False, gain: float = 1.0) -> list[float]:
    """Sintetiza 1 pulsación física de teclado mecánico cremoso (3 capas)."""
    dur = 0.24 if is_enter else 0.17
    n = int(SR * dur)
    buf = [0.0] * n

    f_start = rng.uniform(135.0, 155.0) if is_enter else rng.uniform(210.0, 275.0)
    f_end = f_start * 0.64
    thock_decay = 42.0 if is_enter else rng.uniform(52.0, 68.0)

    # Frecuencias del click PBT de switch (sin ruido blanco crudo estridente)
    click_f1 = rng.uniform(1900.0, 2500.0) if is_enter else rng.uniform(2400.0, 3300.0)
    click_f2 = click_f1 * rng.uniform(1.31, 1.48)
    click_f3 = click_f1 * rng.uniform(1.68, 1.89)
    click_decay = rng.uniform(180.0, 240.0)

    up_delay = rng.uniform(0.036, 0.054)
    up_freq = rng.uniform(330.0, 440.0)

    phase = 0.0
    p1 = p2 = p3 = 0.0
    for i in range(n):
        t = i / SR
        # 1) Bottom-out "thock" cálido con caída rápida de pitch
        inst_f = f_end + (f_start - f_end) * math.exp(-t * 95.0)
        phase += 2.0 * math.pi * inst_f / SR
        thock = math.sin(phase) * math.exp(-t * thock_decay) * (0.85 if is_enter else 0.68)
        # Segundo armónico cálido de caja
        thock += 0.22 * math.sin(phase * 1.98) * math.exp(-t * (thock_decay * 1.45))

        # 2) Tactile keycap click corto (transiente limpio, cero silbido)
        p1 += 2.0 * math.pi * click_f1 / SR
        p2 += 2.0 * math.pi * click_f2 / SR
        p3 += 2.0 * math.pi * click_f3 / SR
        click_env = math.exp(-t * click_decay)
        click = (0.45 * math.sin(p1) + 0.35 * math.sin(p2) + 0.20 * math.sin(p3)) * click_env * 0.26

        # 3) Upstroke suave (rebote del resorte/tecla)
        up = 0.0
        if t >= up_delay:
            tu = t - up_delay
            up = math.sin(2.0 * math.pi * up_freq * tu) * math.exp(-tu * 115.0) * 0.16

        # Fade-in ultrarrápido (0.5ms) para evitar clics digitales sin matar ataque
        atk = min(1.0, t / 0.0006)
        buf[i] = (thock + click + up) * atk * gain

    return buf


def mix_into(dest: list[float], src: list[float], start_sec: float) -> None:
    start_idx = int(start_sec * SR)
    limit = len(dest)
    for i, s in enumerate(src):
        pos = start_idx + i
        if 0 <= pos < limit:
            dest[pos] += s


def normalize_and_write(path_wav: Path, samples: list[float], target_peak: float = 0.86) -> None:
    peak = max((abs(s) for s in samples), default=1e-6)
    scale = min(1.8, target_peak / max(peak, 1e-6))
    # Fade-out últimos 25ms para cero clicks al final
    fade_len = min(len(samples), int(0.025 * SR))
    pcm = array("h")
    total = len(samples)
    for idx, s in enumerate(samples):
        val = s * scale
        if idx >= total - fade_len:
            val *= (total - idx) / max(1, fade_len)
        # Soft clip tanh ligero para calidez analógica
        val = math.tanh(val)
        pcm.append(max(-32767, min(32767, int(val * 32767.0))))

    with wave.open(str(path_wav), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())

    path_mp3 = path_wav.with_suffix(".mp3")
    subprocess.run(
        [FFMPEG, "-y", "-i", str(path_wav), "-c:a", "libmp3lame", "-b:a", "192k", "-loglevel", "error", str(path_mp3)],
        check=True,
    )


def make_typing_burst(seed: int, total_dur: float, end_enter: bool = True) -> list[float]:
    rng = random.Random(seed)
    buf = [0.0] * int(SR * total_dur)
    t = 0.04
    word_left = rng.randint(4, 7)
    end_limit = total_dur - (0.38 if end_enter else 0.22)
    while t < end_limit:
        is_space = (word_left == 0)
        key_wav = synth_creamy_key(rng, is_enter=is_space, gain=rng.uniform(0.75, 1.05))
        mix_into(buf, key_wav, t)
        if is_space:
            t += rng.uniform(0.11, 0.16)
            word_left = rng.randint(3, 8)
        else:
            t += rng.uniform(0.055, 0.105)
            word_left -= 1
    if end_enter:
        enter_wav = synth_creamy_key(rng, is_enter=True, gain=1.18)
        mix_into(buf, enter_wav, total_dur - 0.34)
    return buf


def synth_bubble_pop() -> list[float]:
    dur = 0.24
    n = int(SR * dur)
    buf = [0.0] * n
    phase = 0.0
    for i in range(n):
        t = i / SR
        f = 340.0 + 520.0 * (1.0 - math.exp(-t * 48.0))
        phase += 2.0 * math.pi * f / SR
        env = math.sin(min(1.0, t / 0.012) * math.pi * 0.5) * math.exp(-t * 28.0)
        buf[i] = math.sin(phase) * env * 0.85
    return buf


def synth_soft_whoosh() -> list[float]:
    rng = random.Random(901)
    dur = 0.38
    n = int(SR * dur)
    buf = [0.0] * n
    # Filtered resonant sweep sin estridencia
    lp1 = lp2 = 0.0
    p_hum = 0.0
    for i in range(n):
        t = i / SR
        u = t / dur
        env = math.sin(math.pi * u) ** 1.6
        cutoff = 0.04 + 0.14 * math.sin(math.pi * u)
        raw = rng.uniform(-1.0, 1.0)
        lp1 += cutoff * (raw - lp1)
        lp2 += cutoff * (lp1 - lp2)
        p_hum += 2.0 * math.pi * (140.0 + 180.0 * u) / SR
        buf[i] = (lp2 * 1.4 + math.sin(p_hum) * 0.18) * env
    return buf


def synth_guardrail_chime() -> list[float]:
    dur = 1.25
    n = int(SR * dur)
    buf = [0.0] * n
    notes = [(0.00, 523.25), (0.09, 659.25), (0.18, 783.99), (0.28, 1046.50)]
    for t0, freq in notes:
        start = int(t0 * SR)
        for i in range(start, n):
            tu = (i - start) / SR
            env = min(1.0, tu / 0.006) * math.exp(-tu * 4.4)
            tone = math.sin(2.0 * math.pi * freq * tu) + 0.25 * math.sin(4.0 * math.pi * freq * tu) * math.exp(-tu * 9.0)
            buf[i] += tone * env * 0.36
    return buf


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TPL_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    specs = [
        ("sfx_teclado_creamy_rafaga_3s.wav", make_typing_burst(101, 3.0, end_enter=True)),
        ("sfx_teclado_creamy_rafaga_6s.wav", make_typing_burst(202, 6.0, end_enter=True)),
        ("sfx_teclado_tecla_suelta_01.wav", synth_creamy_key(random.Random(301), is_enter=False, gain=1.0)),
        ("sfx_teclado_tecla_suelta_02.wav", synth_creamy_key(random.Random(302), is_enter=False, gain=1.0)),
        ("sfx_teclado_tecla_suelta_03.wav", synth_creamy_key(random.Random(303), is_enter=False, gain=1.0)),
        ("sfx_teclado_enter_thock.wav", synth_creamy_key(random.Random(404), is_enter=True, gain=1.15)),
        ("sfx_pop_burbuja_ui.wav", synth_bubble_pop()),
        ("sfx_whoosh_suave_tarjeta.wav", synth_soft_whoosh()),
        ("sfx_guardrail_dorado_chime.wav", synth_guardrail_chime()),
    ]

    for fname, samples in specs:
        out_wav = OUT_DIR / fname
        normalize_and_write(out_wav, samples)
        res = subprocess.run(
            [FFPROBE, "-v", "error", "-show_entries", "format=duration:stream=sample_rate,codec_name", "-of", "default=noprint_wrappers=1:nokey=1", str(out_wav)],
            capture_output=True, text=True, check=True,
        )
        info = " | ".join(line.strip() for line in res.stdout.splitlines() if line.strip())
        print(f"OK {fname} ({out_wav.stat().st_size} B) + .mp3 -> {info}")

    # Copia local para la plantilla HyperFrames
    shutil.copy2(OUT_DIR / "sfx_teclado_creamy_rafaga_3s.wav", TPL_ASSETS_DIR / "sfx_teclado_creamy_rafaga_3s.wav")
    print(f"OK copied burst to {TPL_ASSETS_DIR / 'sfx_teclado_creamy_rafaga_3s.wav'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
