#!/usr/bin/env python3
"""
Sintetiza capa determinista de SFX Toy-Prop 3D (crack, sirena, pops, ticks de aguja,
slap de curita, acorde de puertas y dings de checklist) y la mezcla limpia (-9 dB + limiter)
sobre el WAV maestro existente (cuesta $0 en ElevenLabs).

Uso:
  python3 proyectos/waters-serie/scripts/add_toyprop_sfx.py --mode s04
  python3 proyectos/waters-serie/scripts/add_toyprop_sfx.py --mode s05
"""
import argparse
import math
import shutil
import struct
import subprocess
import wave
from pathlib import Path
from typing import List, Tuple

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
AUDIO_DIR = ROOT / "proyectos/waters-serie/carbon_ciberseguridad/audio"
S04_IN_WAV = AUDIO_DIR / "carbon_short_60s_master.wav"
S04_OUT_WAV = AUDIO_DIR / "carbon_short_60s_master_sfx.wav"
S04_MP4 = ROOT / "proyectos/waters-serie/renders/ORO_CARBON_CIBERSEGURIDAD_SHORT_60S.mp4"

S05_IN_WAV = AUDIO_DIR / "carbon_explainer_3min_master.wav"
S05_OUT_WAV = AUDIO_DIR / "carbon_explainer_3min_master_sfx.wav"

FFMPEG = shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
FFPROBE = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"
SR = 44100


def _mix_sample(buf_l: List[float], buf_r: List[float], idx: int, val: float, pan: float = 0.0) -> None:
    if 0 <= idx < len(buf_l):
        gain_l = min(1.0, 1.0 - max(0.0, pan) * 0.45)
        gain_r = min(1.0, 1.0 + min(0.0, pan) * 0.45)
        buf_l[idx] += val * gain_l
        buf_r[idx] += val * gain_r


def _prng(seed: int) -> float:
    x = math.sin(seed * 12.9898 + 78.233) * 43758.5453
    return (x - math.floor(x)) * 2.0 - 1.0


def add_crack_impact(buf_l: List[float], buf_r: List[float], t_sec: float) -> None:
    """Golpe plástico + fractura de cristal + sub-thud 95->38 Hz."""
    start = int(t_sec * SR)
    dur_n = int(0.45 * SR)
    for k in range(dur_n):
        dt = k / SR
        # Low sub-thud
        f_sub = 95.0 - (95.0 - 38.0) * min(1.0, dt / 0.16)
        sub = math.sin(2.0 * math.pi * f_sub * dt) * math.exp(-dt * 12.0) * 0.72
        # Glass/plastic crack noise burst
        noise = _prng(start + k) * math.exp(-dt * 34.0) * 0.65
        # Short fracture ping
        ping = math.sin(2.0 * math.pi * (1180.0 - dt * 900.0) * dt) * math.exp(-dt * 26.0) * 0.35
        _mix_sample(buf_l, buf_r, start + k, sub + noise + ping)


def add_siren_pulse(buf_l: List[float], buf_r: List[float], t_sec: float) -> None:
    """Chirp corto de alerta roja 920->620 Hz."""
    start = int(t_sec * SR)
    dur_n = int(0.32 * SR)
    for k in range(dur_n):
        dt = k / SR
        env = math.sin(math.pi * min(1.0, dt / 0.32)) * math.exp(-dt * 4.5)
        f = 920.0 - (920.0 - 620.0) * (dt / 0.32)
        val = (math.sin(2.0 * math.pi * f * dt) * 0.42 + math.sin(2.0 * math.pi * f * 1.5 * dt) * 0.12) * env
        _mix_sample(buf_l, buf_r, start + k, val, pan=0.25)


def add_pop_whoosh(buf_l: List[float], buf_r: List[float], t_sec: float, pitch_scale: float = 1.0) -> None:
    """Pop juguetón 280->740 Hz para entradas de escena Toy-Prop."""
    start = int(t_sec * SR)
    dur_n = int(0.16 * SR)
    f0 = 280.0 * pitch_scale
    f1 = 740.0 * pitch_scale
    for k in range(dur_n):
        dt = k / SR
        u = dt / 0.16
        f = f0 + (f1 - f0) * (u ** 0.75)
        env = math.sin(math.pi * u) * math.exp(-dt * 10.0)
        val = math.sin(2.0 * math.pi * f * dt) * env * 0.55
        _mix_sample(buf_l, buf_r, start + k, val)


def add_gauge_sweep(buf_l: List[float], buf_r: List[float], t_sec: float) -> None:
    """Ticks mecánicos de aguja girando en SemiGauge3D."""
    for step in range(6):
        st = int((t_sec + step * 0.07) * SR)
        dur_n = int(0.035 * SR)
        f = 640.0 + step * 85.0
        for k in range(dur_n):
            dt = k / SR
            val = math.sin(2.0 * math.pi * f * dt) * math.exp(-dt * 95.0) * 0.32
            _mix_sample(buf_l, buf_r, st + k, val, pan=(step - 2.5) * 0.15)


def add_bandage_slap(buf_l: List[float], buf_r: List[float], t_sec: float) -> None:
    """Whoosh rápido + golpe elástico de curita 180->90 Hz."""
    start = int(t_sec * SR)
    dur_n = int(0.24 * SR)
    for k in range(dur_n):
        dt = k / SR
        if dt < 0.08:
            whoosh = _prng(start + k) * (dt / 0.08) * 0.22
            _mix_sample(buf_l, buf_r, start + k, whoosh)
        else:
            s_dt = dt - 0.08
            f = 180.0 - 90.0 * min(1.0, s_dt / 0.1)
            thump = math.sin(2.0 * math.pi * f * s_dt) * math.exp(-s_dt * 24.0) * 0.65
            click = math.sin(2.0 * math.pi * 1450.0 * s_dt) * math.exp(-s_dt * 110.0) * 0.25
            _mix_sample(buf_l, buf_r, start + k, thump + click)


def add_doors_chime(buf_l: List[float], buf_r: List[float], t_sec: float) -> None:
    """Acorde menor grave estilo dilema Puerta 1 vs Puerta 2."""
    start = int(t_sec * SR)
    dur_n = int(0.65 * SR)
    for k in range(dur_n):
        dt = k / SR
        env = min(1.0, dt / 0.02) * math.exp(-dt * 4.5)
        val = (
            math.sin(2.0 * math.pi * 220.0 * dt) * 0.32
            + math.sin(2.0 * math.pi * 261.63 * dt) * 0.26
            + math.sin(2.0 * math.pi * 329.63 * dt) * 0.18
        ) * env
        _mix_sample(buf_l, buf_r, start + k, val)


def add_check_ding(buf_l: List[float], buf_r: List[float], t_sec: float, note_hz: float) -> None:
    """Ding brillante de palomita verde en portapapeles 3D."""
    start = int(t_sec * SR)
    dur_n = int(0.45 * SR)
    for k in range(dur_n):
        dt = k / SR
        env = min(1.0, dt / 0.008) * math.exp(-dt * 8.5)
        val = (
            math.sin(2.0 * math.pi * note_hz * dt) * 0.42
            + math.sin(2.0 * math.pi * note_hz * 2.0 * dt) * 0.16 * math.exp(-dt * 14.0)
        ) * env
        _mix_sample(buf_l, buf_r, start + k, val, pan=-0.2)


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            FFPROBE,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def write_sfx_and_mix(in_wav: Path, out_wav: Path, cues: List[Tuple[str, float, float]]) -> None:
    dur = probe_duration(in_wav)
    n_total = int((dur + 0.2) * SR)
    buf_l = [0.0] * n_total
    buf_r = [0.0] * n_total

    for kind, t_sec, param in cues:
        if kind == "crack":
            add_crack_impact(buf_l, buf_r, t_sec)
        elif kind == "siren":
            add_siren_pulse(buf_l, buf_r, t_sec)
        elif kind == "pop":
            add_pop_whoosh(buf_l, buf_r, t_sec, pitch_scale=param)
        elif kind == "gauge":
            add_gauge_sweep(buf_l, buf_r, t_sec)
        elif kind == "bandage":
            add_bandage_slap(buf_l, buf_r, t_sec)
        elif kind == "doors":
            add_doors_chime(buf_l, buf_r, t_sec)
        elif kind == "ding":
            add_check_ding(buf_l, buf_r, t_sec, note_hz=param)

    sfx_tmp = out_wav.with_name(out_wav.stem + "_layer.wav")
    raw = bytearray()
    for l_val, r_val in zip(buf_l, buf_r):
        il = max(-32767, min(32767, int(l_val * 32767.0)))
        ir = max(-32767, min(32767, int(r_val * 32767.0)))
        raw.extend(struct.pack("<hh", il, ir))
    with wave.open(str(sfx_tmp), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(bytes(raw))

    # Mix SFX cleanly at -9 dB (0.355 linear) + limiter over existing master WAV
    cmd = [
        FFMPEG,
        "-y",
        "-i",
        str(in_wav),
        "-i",
        str(sfx_tmp),
        "-filter_complex",
        "[1:a]volume=0.355[sfx];[0:a][sfx]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,alimiter=limit=0.95[out]",
        "-map",
        "[out]",
        "-c:a",
        "pcm_s16le",
        "-ar",
        str(SR),
        "-ac",
        "2",
        str(out_wav),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sfx_tmp.unlink(missing_ok=True)
    print(f"✅ SFX mezclados en {out_wav} ({probe_duration(out_wav):.2f}s)")


def remux_mp4(mp4_path: Path, audio_wav: Path) -> None:
    tmp_mp4 = mp4_path.with_name(mp4_path.stem + "_sfx_tmp.mp4")
    cmd = [
        FFMPEG,
        "-y",
        "-i",
        str(mp4_path),
        "-i",
        str(audio_wav),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        "-shortest",
        str(tmp_mp4),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tmp_mp4.replace(mp4_path)
    print(f"🎬 MP4 remuxeado sin re-codificar video: {mp4_path}")


S04_CUES: List[Tuple[str, float, float]] = [
    ("crack", 1.05, 1.0),
    ("siren", 1.85, 1.0),
    ("pop", 7.12, 1.0),
    ("pop", 17.93, 1.1),
    ("gauge", 18.25, 1.0),
    ("pop", 34.10, 1.05),
    ("bandage", 34.90, 1.0),
    ("doors", 49.23, 1.0),
    ("pop", 64.12, 1.15),
    ("ding", 64.45, 1046.5),  # C6
    ("ding", 65.72, 1318.5),  # E6
    ("ding", 66.98, 1568.0),  # G6
]

S05_CUES: List[Tuple[str, float, float]] = [
    ("crack", 1.05, 1.0),
    ("siren", 1.95, 1.0),
    ("pop", 21.86, 0.95),
    ("pop", 41.97, 1.0),
    ("pop", 68.16, 1.1),
    ("gauge", 68.50, 1.0),
    ("pop", 104.35, 1.05),
    ("bandage", 105.15, 1.0),
    ("doors", 128.54, 1.0),
    ("pop", 158.01, 1.15),
    ("doors", 189.40, 1.0),
    ("pop", 215.27, 1.0),
    ("gauge", 215.60, 1.0),
    ("pop", 234.34, 1.1),
    ("pop", 250.29, 1.2),
    ("ding", 250.62, 1046.5),
    ("ding", 251.89, 1318.5),
    ("ding", 253.15, 1568.0),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["s04", "s05"], required=True)
    args = parser.parse_args()

    if args.mode == "s04":
        write_sfx_and_mix(S04_IN_WAV, S04_OUT_WAV, S04_CUES)
        remux_mp4(S04_MP4, S04_OUT_WAV)
    else:
        write_sfx_and_mix(S05_IN_WAV, S05_OUT_WAV, S05_CUES)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
