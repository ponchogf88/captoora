#!/usr/bin/env python3
"""
Motor compartido de audio y coreografía para episodios Waters! Chispa 3D:
  - Síntesis ElevenLabs v3 (con caché por .mp3 y fallback turbo_v2_5 para lang="en")
  - ASMR de teclado mecánico ("Creamy Thock + Tactile Snap") sincronizado
  - Pops orgánicos ("Bubble UI Pop!") + chimes dorados + pausas dramáticas
  - Mezcla master WAV + escritura en episodeBeats.json
"""
import json
import math
import os
import random
import re
import shutil
import struct
import subprocess
import sys
import urllib.error
import urllib.request
import wave
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
ENV_FILE = ROOT / ".env"
BEATS_JSON = ROOT / "proyectos/waters-3d-studio/src/episodeBeats.json"
EP06_OPENING = ROOT / "proyectos/waters-serie/renders/audio_elevenlabs_v3/EP06_HACKEOS_Y_VOZ/01_tony.mp3"
EP06_CLOSING = ROOT / "proyectos/waters-serie/renders/audio_elevenlabs_v3/EP06_HACKEOS_Y_VOZ/14_tony.mp3"
FFMPEG = "/Users/imac/.local/bin/ffmpeg"
FFPROBE = "/Users/imac/.local/bin/ffprobe"
FPS = 30
SR = 44100

TONY_ID = "htFfPSZGJwjBv1CL0aMD"  # Antonio - Confident, Gentle and Clear
AGY_ID = "kl7d390GatBPfqhRTyAl"   # Liza - Natural Mexican Creator


def load_api_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key and ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("ELEVENLABS_API_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val.startswith("sk_"):
                    return val
    return key


def tts_to_mp3(
    text: str,
    voice_id: str,
    out_path: Path,
    api_key: str,
    stability: float = 0.30,
    language_code: Optional[str] = None,
) -> None:
    """Synthesizes TTS audio via ElevenLabs v3 with turbo_v2_5 fallback if needed."""
    def _post(body_dict: dict) -> bytes:
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            data=json.dumps(body_dict).encode("utf-8"),
            headers={
                "xi-api-key": api_key,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()

    body = {
        "text": text,
        "model_id": "eleven_v3",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": 0.78,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }
    if language_code:
        body["language_code"] = language_code

    try:
        out_path.write_bytes(_post(body))
    except urllib.error.HTTPError as err:
        if language_code and err.code in (400, 422):
            clean_text = re.sub(r"\[[^\]]+\]\s*", "", text).strip()
            fallback_body = {
                "text": clean_text,
                "model_id": "eleven_turbo_v2_5",
                "language_code": language_code,
                "voice_settings": {
                    "stability": stability,
                    "similarity_boost": 0.78,
                    "style": 0.0,
                    "use_speaker_boost": True,
                },
            }
            out_path.write_bytes(_post(fallback_body))
        else:
            raise


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


def _add_sample(buf_l: List[float], buf_r: List[float], idx: int, val: float, pan: float = 0.0) -> None:
    if 0 <= idx < len(buf_l):
        gl = math.sqrt(0.5 * (1.0 - max(-0.85, min(0.85, pan))))
        gr = math.sqrt(0.5 * (1.0 + max(-0.85, min(0.85, pan))))
        buf_l[idx] += val * gl
        buf_r[idx] += val * gr


def add_mech_keystroke(
    buf_l: List[float],
    buf_r: List[float],
    start_sec: float,
    rng: random.Random,
    is_enter: bool = False,
    pan: float = 0.0,
    amp: float = 0.34,
) -> None:
    """Creamy PBT mechanical keycap stroke (tactile snap + warm bottom-out thock)."""
    n_len = int(0.055 * SR)
    base_idx = int(start_sec * SR)
    f_hi = 165.0 if is_enter else rng.uniform(275.0, 355.0)
    f_lo = 92.0 if is_enter else rng.uniform(135.0, 175.0)
    snap_f1 = rng.uniform(2400.0, 3400.0)
    snap_f2 = snap_f1 * rng.uniform(1.32, 1.48)
    vol = amp * (1.30 if is_enter else rng.uniform(0.82, 1.12))

    phase_thock = 0.0
    for k in range(n_len):
        dt = k / SR
        att = min(1.0, dt / 0.0012)
        f_inst = f_lo + (f_hi - f_lo) * math.exp(-dt * 190.0)
        phase_thock += 2.0 * math.pi * f_inst / SR
        thock = math.sin(phase_thock) * math.exp(-dt * 95.0)

        snap_env = math.exp(-dt * 420.0)
        snap = (
            0.55 * math.sin(2.0 * math.pi * snap_f1 * dt)
            + 0.35 * math.sin(2.0 * math.pi * snap_f2 * dt)
            + 0.28 * rng.uniform(-1.0, 1.0)
        ) * snap_env

        upstroke = 0.0
        if dt > 0.016:
            du = dt - 0.016
            upstroke = 0.24 * math.sin(2.0 * math.pi * (snap_f1 * 0.72) * du) * math.exp(-du * 360.0)

        sample = att * vol * (0.72 * thock + 0.58 * snap + upstroke)
        _add_sample(buf_l, buf_r, base_idx + k, sample, pan)


def add_ui_pop(
    buf_l: List[float],
    buf_r: List[float],
    start_sec: float,
    f_start: float = 240.0,
    f_end: float = 760.0,
    amp: float = 0.40,
    with_sparkle: bool = False,
) -> None:
    """Glossy bubble Pop SFX synchronized with popping UI windows/pills."""
    dur = 0.20 if with_sparkle else 0.072
    n_len = int(dur * SR)
    base_idx = int(start_sec * SR)
    phase = 0.0
    for k in range(n_len):
        dt = k / SR
        att = min(1.0, dt / 0.0028)
        f_inst = f_start + (f_end - f_start) * (1.0 - math.exp(-dt * 82.0))
        phase += 2.0 * math.pi * f_inst / SR
        pop_env = math.exp(-dt * 58.0)
        wave_val = math.sin(phase) + 0.20 * math.sin(2.0 * phase)

        sparkle = 0.0
        if with_sparkle and dt > 0.012:
            ds = dt - 0.012
            sparkle = (
                0.22 * math.sin(2.0 * math.pi * 1567.98 * ds)
                + 0.14 * math.sin(2.0 * math.pi * 2349.32 * ds)
            ) * math.exp(-ds * 16.0)

        sample = att * amp * (wave_val * pop_env + sparkle)
        _add_sample(buf_l, buf_r, base_idx + k, sample, pan=0.0)


def build_sfx_track(
    visual_schedules: List[Tuple[float, float, List[int], bool]],
    total_sec: float,
    out_wav: Path,
    seed: int,
) -> None:
    """Renders stereo WAV containing mechanical keyboard bursts and UI bubble Pops."""
    n_total = int((total_sec + 0.5) * SR)
    buf_l = [0.0] * n_total
    buf_r = [0.0] * n_total
    rng = random.Random(seed)

    pop_profiles = {
        2: (265.0, 780.0, 0.36, False),
        6: (215.0, 650.0, 0.42, False),
        8: (205.0, 620.0, 0.44, False),
        14: (310.0, 880.0, 0.38, False),
        16: (310.0, 880.0, 0.38, False),
        18: (330.0, 920.0, 0.38, False),
        20: (305.0, 860.0, 0.38, False),
        22: (390.0, 1080.0, 0.40, True),
        24: (335.0, 940.0, 0.38, False),
        26: (355.0, 980.0, 0.38, False),
        32: (360.0, 1020.0, 0.39, True),
        34: (375.0, 1050.0, 0.39, True),
        36: (395.0, 1100.0, 0.40, True),
    }

    for t_start, t_dur, pops, silent_pause in visual_schedules:
        sfx_anchor = t_start + (0.28 if silent_pause else 0.0)
        for pf in pops:
            t_pop = sfx_anchor + (pf / FPS)
            if t_pop < t_start + t_dur - 0.08:
                f0, f1, amp, spk = pop_profiles.get(pf, (295.0, 850.0, 0.36, False))
                add_ui_pop(buf_l, buf_r, t_pop, f0, f1, amp, spk)

        type_start = sfx_anchor + (8.0 / FPS)
        type_end = min(sfx_anchor + (34.0 / FPS), t_start + t_dur - 0.12)
        n_keys = max(7, min(16, int((type_end - type_start) * 16.5)))
        if n_keys > 0 and type_end > type_start:
            step = (type_end - type_start) / n_keys
            for ki in range(n_keys):
                t_key = type_start + ki * step + rng.uniform(-0.006, 0.006)
                pan = ((ki % 8) / 7.0 - 0.5) * 0.55
                add_mech_keystroke(
                    buf_l,
                    buf_r,
                    t_key,
                    rng,
                    is_enter=(ki == n_keys - 1),
                    pan=pan,
                    amp=0.33,
                )

    peak = max(
        0.001,
        max(max(abs(x) for x in buf_l), max(abs(x) for x in buf_r)),
    )
    gain = min(1.0, 0.85 / peak)

    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        frames = bytearray()
        for l_val, r_val in zip(buf_l, buf_r):
            il = max(-32767, min(32767, int(l_val * gain * 32767.0)))
            ir = max(-32767, min(32767, int(r_val * gain * 32767.0)))
            frames.extend(struct.pack("<hh", il, ir))
        wf.writeframes(bytes(frames))


def compile_episode_audio(
    ep_tag: str,
    beats_key: str,
    out_dir: Path,
    script: List[Dict[str, Any]],
    seed: int = 2026,
) -> int:
    """Synthesizes/reuses TTS clips, mixes SFX + voice WAV, and writes beats to episodeBeats.json."""
    api_key = load_api_key()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Reuse exact native English "Waters!" opening & closing if available
    first_mp3 = out_dir / "01_tony.mp3"
    if not first_mp3.exists() and EP06_OPENING.exists():
        shutil.copy2(EP06_OPENING, first_mp3)
        print(f"[{ep_tag}] Copiado opening nativo en ingles: {first_mp3}")

    last_id = script[-1]["id"]
    last_mp3 = out_dir / f"{last_id}.mp3"
    if not last_mp3.exists() and EP06_CLOSING.exists():
        shutil.copy2(EP06_CLOSING, last_mp3)
        print(f"[{ep_tag}] Copiado closing nativo en ingles: {last_mp3}")

    beats_out = []
    audio_events = []
    visual_schedules: List[Tuple[float, float, List[int], bool]] = []
    current_frame = 0

    for item in script:
        mp3_path = out_dir / f"{item['id']}.mp3"
        if not mp3_path.exists():
            if not api_key:
                print(f"ERROR: Falta ELEVENLABS_API_KEY para {mp3_path}", file=sys.stderr)
                return 1
            vid = TONY_ID if item["speaker"] == "tony" else AGY_ID
            lang = item.get("language_code")
            stab = item.get("stability", 0.30)
            print(f"[{ep_tag}] TTS {item['id']} ({item['speaker']}, lang={lang}): {item['text']}")
            tts_to_mp3(item["text"], vid, mp3_path, api_key, stability=stab, language_code=lang)

        dur = probe_duration(mp3_path)
        lead_sil = item.get("lead_silence_sec", 0.0)
        start_sec = current_frame / FPS
        audio_events.append((start_sec + lead_sil + 0.06, mp3_path))

        total_frames_item = max(50, math.ceil((dur + lead_sil + 0.22) * FPS))
        vis_list = item["visuals"]

        allocated = 0
        for vi, v in enumerate(vis_list):
            if vi < len(vis_list) - 1:
                v_frames = max(36, round(total_frames_item * v["ratio"]))
            else:
                v_frames = total_frames_item - allocated
            allocated += v_frames

            v_start_sec = current_frame / FPS
            v_dur_sec = v_frames / FPS
            is_pause = lead_sil > 0.0 and vi == 0
            visual_schedules.append((v_start_sec, v_dur_sec, v["pops"], is_pause))

            beat_entry = {
                "durationInFrames": v_frames,
                "topTag": v["topTag"],
                "accentColor": v["accentColor"],
                "expression": v["expression"],
                "cardType": v["cardType"],
                "stageProp": v["stageProp"],
                "stepBadge": v["stepBadge"],
                "pillText": v["pillText"],
                "headlinePrefix": v["headlinePrefix"],
                "headlineFocus": v["headlineFocus"],
                "headlineSuffix": v.get("headlineSuffix", ""),
                "terminalCmd": v["terminalCmd"],
                "terminalSub": v["terminalSub"],
                "pops": v["pops"],
                "speaking": True,
            }
            for opt_key in ("safeMode", "giroTop", "giroBottom", "cardItems", "stepTitle", "stepDetail"):
                if opt_key in v:
                    beat_entry[opt_key] = v[opt_key]

            beats_out.append(beat_entry)
            current_frame += v_frames

    total_sec = current_frame / FPS
    asmr_sfx_wav = out_dir / f"{ep_tag}_asmr_sfx.wav"
    print(f"[{ep_tag}] Sintetizando ASMR Teclado + Pops UI en {asmr_sfx_wav}...")
    build_sfx_track(visual_schedules, total_sec, asmr_sfx_wav, seed=seed)

    master_wav = out_dir / f"{ep_tag}_master.wav"
    inputs = [
        "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo:d={total_sec:.3f}",
        "-i", str(asmr_sfx_wav),
    ]
    filters = ["[1:a]volume=0.68[sfx]"]
    mix = ["[0:a]", "[sfx]"]
    for i, (st, p) in enumerate(audio_events, start=2):
        inputs.extend(["-i", str(p)])
        ms = int(st * 1000)
        lbl = f"[v{i}]"
        filters.append(f"[{i}:a]adelay={ms}|{ms},volume=1.24{lbl}")
        mix.append(lbl)

    fc = ";".join(filters) + ";" + "".join(mix) + f"amix=inputs={len(mix)}:duration=longest:normalize=0[aout]"
    subprocess.run(
        [FFMPEG, "-y", *inputs, "-filter_complex", fc, "-map", "[aout]", "-ar", "44100", "-ac", "2", str(master_wav)],
        check=True,
    )

    existing = json.loads(BEATS_JSON.read_text(encoding="utf-8")) if BEATS_JSON.exists() else {}
    existing[beats_key] = beats_out
    BEATS_JSON.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ [{beats_key}] Visual beats={len(beats_out)} | Total frames={current_frame} ({total_sec:.2f}s) | WAV={master_wav}")
    return 0
