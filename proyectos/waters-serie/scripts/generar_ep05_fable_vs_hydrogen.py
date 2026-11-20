#!/usr/bin/env python3
"""
Genera EP05 ("Fable 5.2 ($19 / 45 min) vs Gemini 4 Hydrogen ($1.50 o Gratis / 12 min)
+ Clon GTA 6 en 10 min + Modo IA Ilimitado") con:
  - Voces ElevenLabs eleven_v3 (reutilizando MP3 ya generados si existen; "¡Waters!" con lang="en")
  - Motor ASMR de Teclado Mecánico ("Creamy Thock + Tactile Snap") sincronizado a los comandos
  - Pops orgánicos ("Bubble UI Pop!") sincronizados frame a frame con las ventanitas y píldoras
  - Metadata visual completa para ChispaAstronaut3D + Dioramas 3D en episodeBeats.json
"""
import json
import math
import os
import random
import re
import struct
import subprocess
import sys
import urllib.error
import urllib.request
import wave
from pathlib import Path
from typing import List, Optional, Tuple

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
ENV_FILE = ROOT / ".env"
OUT_AUDIO = ROOT / "proyectos/waters-serie/renders/audio_elevenlabs_v3/EP05_FABLE_HYDROGEN"
BEATS_JSON = ROOT / "proyectos/waters-3d-studio/src/episodeBeats.json"
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
    stability: float = 0.32,
    language_code: Optional[str] = None,
) -> None:
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


# ==============================================================================
# ASMR SFX ENGINE: Creamy Mechanical Keyboards + Organic UI Bubble Pops
# ==============================================================================
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
    """
    Synthesizes a creamy PBT keycap mechanical switch press ('Thock + Tactile Snap'):
      1) Tactile click transient (~3.1 kHz crisp housing snap, ~6 ms)
      2) Deep PBT bottom-out thock sweeping ~310 -> 145 Hz (lower for Space/Enter)
      3) Soft spring upstroke tick ~17 ms later
    """
    n_len = int(0.055 * SR)
    base_idx = int(start_sec * SR)
    f_hi = (165.0 if is_enter else rng.uniform(275.0, 355.0))
    f_lo = (92.0 if is_enter else rng.uniform(135.0, 175.0))
    snap_f1 = rng.uniform(2400.0, 3400.0)
    snap_f2 = snap_f1 * rng.uniform(1.32, 1.48)
    vol = amp * (1.30 if is_enter else rng.uniform(0.82, 1.12))

    phase_thock = 0.0
    for k in range(n_len):
        dt = k / SR
        # Smooth 1.2 ms ramp avoids digital edge harshness
        att = min(1.0, dt / 0.0012)

        # Warm pitch drop for PBT keycap body thock
        f_inst = f_lo + (f_hi - f_lo) * math.exp(-dt * 190.0)
        phase_thock += 2.0 * math.pi * f_inst / SR
        thock = math.sin(phase_thock) * math.exp(-dt * 95.0)

        # Crisp switch stem tactile click + subtle micro-grit
        snap_env = math.exp(-dt * 420.0)
        snap = (
            0.55 * math.sin(2.0 * math.pi * snap_f1 * dt)
            + 0.35 * math.sin(2.0 * math.pi * snap_f2 * dt)
            + 0.28 * rng.uniform(-1.0, 1.0)
        ) * snap_env

        # Gentle upstroke bounce around 17 ms
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
    amp: float = 0.42,
    with_sparkle: bool = False,
) -> None:
    """
    Organic glossy bubble 'Pop!' for popup cards, pills, and terminal windows.
    Uses upward pitch glide with rounded attack and optional soft sparkle chime.
    """
    dur = 0.22 if with_sparkle else 0.075
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
                0.24 * math.sin(2.0 * math.pi * 1567.98 * ds)
                + 0.16 * math.sin(2.0 * math.pi * 2349.32 * ds)
            ) * math.exp(-ds * 16.0)

        sample = att * amp * (wave_val * pop_env + sparkle)
        _add_sample(buf_l, buf_r, base_idx + k, sample, pan=0.0)


def build_asmr_and_pop_wav(
    beat_schedules: List[Tuple[float, float, str, List[int]]],
    total_sec: float,
    out_wav: Path,
) -> None:
    """
    Generates synchronized stereo SFX WAV matching every typing terminal line
    and every Remotion PopBox trigger timestamp across all beats.
    """
    n_total = int((total_sec + 0.5) * SR)
    buf_l = [0.0] * n_total
    buf_r = [0.0] * n_total
    rng = random.Random(42069)

    pop_profiles = {
        2: (270.0, 790.0, 0.36, False),   # Numbered green pill
        8: (205.0, 620.0, 0.44, False),   # Main macOS terminal window
        24: (310.0, 880.0, 0.38, False),  # Sub-window #1
        36: (350.0, 980.0, 0.38, False),  # Sub-window #2
        48: (410.0, 1120.0, 0.40, True),  # Sub-window #3 + star sparkle!
    }

    for beat_idx, (t_start, t_dur, cmd_str, pops) in enumerate(beat_schedules):
        # 1. Exact Pop SFX for every UI card entering with spring()
        for pf in pops:
            t_pop = t_start + (pf / FPS)
            if t_pop < t_start + t_dur - 0.10:
                f0, f1, amp, spk = pop_profiles.get(pf, (290.0, 840.0, 0.36, False))
                add_ui_pop(buf_l, buf_r, t_pop, f0, f1, amp, spk)

        # 2. Fast creamy mechanical keyboard ASMR burst while headline & terminal type!
        # Primary typing window: localFrame 9..32 (0.30s..1.07s)
        type_start = t_start + (9.0 / FPS)
        type_end = min(t_start + (44.0 / FPS), t_start + t_dur - 0.15)
        n_keys = max(10, min(22, int((type_end - type_start) * 16.5)))
        if n_keys > 0 and type_end > type_start:
            step = (type_end - type_start) / n_keys
            for ki in range(n_keys):
                jitter = rng.uniform(-0.007, 0.007)
                t_key = type_start + ki * step + jitter
                is_last = ki == (n_keys - 1)
                pan = ((ki % 8) / 7.0 - 0.5) * 0.55
                add_mech_keystroke(
                    buf_l,
                    buf_r,
                    t_key,
                    rng,
                    is_enter=is_last,
                    pan=pan,
                    amp=0.33,
                )

    # Gentle soft limiter / normalization so SFX never clips
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


EP05_LINES = [
    {
        "speaker": "tony",
        "text": "[serious] Waters!",
        "language_code": "en",
        "stability": 0.35,
        "topTag": "TERMINAL · HOOK // LIVE",
        "accentColor": "#00F5D4",
        "expression": "happy_open",
        "cardType": "alert_intro",
        "stageProp": "none",
        "stepBadge": "✦",
        "pillText": "Gemini 4 Hydrogen acaba de salir",
        "headlinePrefix": "Google acaba de soltar",
        "headlineFocus": "una bomba",
        "headlineSuffix": "⚡",
        "terminalCmd": "$ compare --models fable-5.2 gemini-4-hydrogen",
        "terminalSub": "> Cargando duelo real: precio, velocidad y 3D...",
        "heroTitle": "FABLE 5.2 vs GEMINI 4",
        "heroSubtitle": "¿$19 USD ó $1.50 USD / GRATIS?",
        "pops": [2, 8, 24, 36],
    },
    {
        "speaker": "tony",
        "text": "[serious] ¿Qué, vas a seguir quemando diecinueve dólares y cuarenta y cinco minutos en Fable cinco punto dos para hacer una sola animación?!",
        "topTag": "ANIMACIÓN 3D · CASA FLOTANTE",
        "accentColor": "#FF4D4D",
        "expression": "sad_cloud",
        "cardType": "vs_duel",
        "stageProp": "floating_house",
        "stepBadge": "1",
        "pillText": "Misma escena: Casa Flotante 3D",
        "headlinePrefix": "Fable 5.2 quemó",
        "headlineFocus": "45 minutos",
        "headlineSuffix": "y $19 USD",
        "terminalCmd": "$ render --model fable-5.2 --scene casa-flotante",
        "terminalSub": "! Costo: $19.00 USD | Tiempo: +45 min...",
        "pops": [2, 8, 24, 36],
    },
    {
        "speaker": "agy",
        "text": "[excited] ¡Para nada! Google acaba de soltar Gemini cuatro Hydrogen: hizo esa misma animación en doce minutos y por un dólar cincuenta... ¡o totalmente gratis!",
        "topTag": "GEMINI 4 HYDROGEN · VELOCIDAD 3.75X",
        "accentColor": "#22C55E",
        "expression": "star_eyes",
        "cardType": "vs_duel",
        "stageProp": "floating_house",
        "stepBadge": "2",
        "pillText": "Fracción de precio y tiempo",
        "headlinePrefix": "Misma animación en",
        "headlineFocus": "12 minutos",
        "headlineSuffix": "y $1.50",
        "terminalCmd": "$ render --model gemini-4-hydrogen --tier free",
        "terminalSub": "✓ Listo en 12 min | $1.50 USD (o $0 gratis)",
        "pops": [2, 8, 24, 36],
    },
    {
        "speaker": "tony",
        "text": "[surprised] ¿Cómo que diez veces más barato?! ¡Enséñame los números reales de la API!",
        "topTag": "API PRICING · 1M TOKENS",
        "accentColor": "#38BDF8",
        "expression": "shock_sweat",
        "cardType": "vs_duel",
        "stageProp": "laptop",
        "stepBadge": "⚡",
        "pillText": "Auditoría real por 1M de tokens",
        "headlinePrefix": "Precio real por",
        "headlineFocus": "10x más barato",
        "headlineSuffix": "en API",
        "terminalCmd": "$ diff --pricing fable-5.2 gemini-4-hydrogen",
        "terminalSub": "> Fable $10/$50 vs Hydrogen $1.50/$7.50 🚀",
        "pops": [2, 8, 24, 36],
    },
    {
        "speaker": "agy",
        "text": "[serious] Mira: Fable cinco cobra diez dólares de entrada y cincuenta de salida. Hydrogen cobra uno cincuenta y siete cincuenta... ¡y en Terminal Bench saltó de dieciocho punto dos a cincuenta y siete por ciento, superando a Fable y a GPT Astra seis!",
        "topTag": "TERMINAL BENCH 4.1 · TOP #5 GLOBAL",
        "accentColor": "#38BDF8",
        "expression": "determined_hacker",
        "cardType": "bench_race",
        "stageProp": "laptop",
        "stepBadge": "3",
        "pillText": "Salto brutal en código y agentes",
        "headlinePrefix": "Terminal Bench subió a",
        "headlineFocus": "57.0%",
        "headlineSuffix": "(Top #5)",
        "terminalCmd": "$ run-bench --suite terminal-4.1 --context 1M",
        "terminalSub": "✓ 3.8 Flash (18.2%) ➔ Hydrogen (57.0%) · 2.5x fast",
        "pops": [2, 8, 24, 36, 48],
    },
    {
        "speaker": "tony",
        "text": "[excited] ¡Aguas! ¿Y sí es cierto que le armó un clon jugable de GTA seis en tres D en solo diez minutos?!",
        "topTag": "VICE CITY 3D CLONE · LIVE DEMO",
        "accentColor": "#DFB15B",
        "expression": "happy_open",
        "cardType": "gta6_build",
        "stageProp": "gta6_city",
        "stepBadge": "4",
        "pillText": "Clon jugable de GTA 6 en 3D",
        "headlinePrefix": "Clon 3D completo en",
        "headlineFocus": "10 minutos",
        "headlineSuffix": "🕹️",
        "terminalCmd": "$ build vice-city-3d --cars --planes --boats",
        "terminalSub": "✓ Mundo abierto 3D generado en un solo prompt",
        "pops": [2, 8, 24, 36],
    },
    {
        "speaker": "agy",
        "text": "[excited] ¡En diez minutos con motos, aviones, barcos y cámara en primera persona! Pero ojo: no uses el Gemini normal. Métete a Google AI Studio y activa razonamiento Extra Alto en modo MAX.",
        "topTag": "AI STUDIO · MODO MAX (XHIGH)",
        "accentColor": "#DFB15B",
        "expression": "zen_proud",
        "cardType": "gta6_build",
        "stageProp": "gta6_city",
        "stepBadge": "5",
        "pillText": "Truco: activa razonamiento Extra Alto",
        "headlinePrefix": "En AI Studio activa",
        "headlineFocus": "Modo MAX",
        "headlineSuffix": "(xhigh)",
        "terminalCmd": "$ aistudio --reasoning extra_high --mode MAX",
        "terminalSub": "✓ Motos, taxis, grúas, barcos y 1ra persona",
        "pops": [2, 8, 24, 36],
    },
    {
        "speaker": "agy",
        "text": "[whispering] Y el secreto para no quedarte en cero por ciento de cuota: usa la pestaña Modo IA directo en google punto com. ¡Ya corre Gemini cuatro Hydrogen ilimitado, sin límite de cinco horas ni semanal!",
        "topTag": "MODO IA GOOGLE · CERO LÍMITES",
        "accentColor": "#22C55E",
        "expression": "happy_arcs",
        "cardType": "three_secrets",
        "stageProp": "laptop",
        "stepBadge": "6",
        "pillText": "3 Rutas para usarlo GRATIS hoy",
        "headlinePrefix": "Google.com pestaña",
        "headlineFocus": "Modo IA",
        "headlineSuffix": "Ilimitado",
        "terminalCmd": "$ route --target google.com/modo-ia --limit none",
        "terminalSub": "✓ Sin freno de 5h ni semanal · ID: gemini-4-hydrogen",
        "pops": [2, 8, 24, 36, 48],
    },
    {
        "speaker": "agy",
        "text": "[excited] Comenta HYDROGEN y te mando los tres links y el ID oculto para conectarlo gratis a tus agentes. ¡Toma tus precauciones!",
        "topTag": "KIT GRATIS · LINKS + ID OCULTO",
        "accentColor": "#DFB15B",
        "expression": "happy_arcs",
        "cardType": "cta_wink",
        "stageProp": "kit_box",
        "stepBadge": "🚀",
        "pillText": "Te mando el kit completo gratis",
        "headlinePrefix": "Comenta la palabra",
        "headlineFocus": "HYDROGEN",
        "headlineSuffix": "👇",
        "terminalCmd": "$ send-dm --keyword HYDROGEN --attach 3-links",
        "terminalSub": "✓ Listo: 3 links + ID gemini-4-hydrogen en tu DM",
        "heroTitle": "COMENTA: HYDROGEN 🚀",
        "heroSubtitle": "3 Links + ID Oculto gemini-4-hydrogen",
        "pops": [2, 8, 36],
    },
    {
        "speaker": "tony",
        "text": "[excited] Waters!... Waters!",
        "language_code": "en",
        "stability": 0.35,
        "topTag": "CIERRE · CHISPA ASTRONAUT",
        "accentColor": "#00F5D4",
        "expression": "wink",
        "cardType": "cta_wink",
        "stageProp": "kit_box",
        "stepBadge": "🌊",
        "pillText": "¡Toma tus precauciones tech!",
        "headlinePrefix": "Nos vemos en el próximo:",
        "headlineFocus": "¡WATERS!",
        "headlineSuffix": "🌊🔥",
        "terminalCmd": "$ echo '10x más barato · 3.75x más rápido'",
        "terminalSub": "✓ Dale like, guarda el truco y comenta HYDROGEN",
        "heroTitle": "¡WATERS! 🌊🔥",
        "heroSubtitle": "10X Más Barato · 3.75X Más Rápido",
        "pops": [2, 8, 24],
    },
]


def main() -> int:
    api_key = load_api_key()
    OUT_AUDIO.mkdir(parents=True, exist_ok=True)

    beats_out = []
    audio_events = []
    beat_schedules: List[Tuple[float, float, str, List[int]]] = []
    current_frame = 0

    for idx, item in enumerate(EP05_LINES, start=1):
        mp3_path = OUT_AUDIO / f"{idx:02d}_{item['speaker']}.mp3"
        if not mp3_path.exists():
            if not api_key:
                print(f"ERROR: Falta ELEVENLABS_API_KEY para {mp3_path}", file=sys.stderr)
                return 1
            vid = TONY_ID if item["speaker"] == "tony" else AGY_ID
            lang = item.get("language_code")
            stab = item.get("stability", 0.32)
            print(f"[EP05] TTS {idx:02d} ({item['speaker']}, lang={lang}): {item['text']}")
            tts_to_mp3(item["text"], vid, mp3_path, api_key, stability=stab, language_code=lang)

        dur = probe_duration(mp3_path)
        start_sec = current_frame / FPS
        needed_frames = max(54, math.ceil((dur + 0.28) * FPS))
        beat_dur_sec = needed_frames / FPS

        audio_events.append((start_sec + 0.08, mp3_path))
        beat_schedules.append((start_sec, beat_dur_sec, item["terminalCmd"], item["pops"]))

        beat_entry = {
            "durationInFrames": needed_frames,
            "topTag": item["topTag"],
            "accentColor": item["accentColor"],
            "expression": item["expression"],
            "cardType": item["cardType"],
            "stageProp": item["stageProp"],
            "stepBadge": item["stepBadge"],
            "pillText": item["pillText"],
            "headlinePrefix": item["headlinePrefix"],
            "headlineFocus": item["headlineFocus"],
            "headlineSuffix": item["headlineSuffix"],
            "terminalCmd": item["terminalCmd"],
            "terminalSub": item["terminalSub"],
            "speaking": True,
        }
        if "heroTitle" in item:
            beat_entry["heroTitle"] = item["heroTitle"]
        if "heroSubtitle" in item:
            beat_entry["heroSubtitle"] = item["heroSubtitle"]

        beats_out.append(beat_entry)
        current_frame += needed_frames

    total_sec = current_frame / FPS
    asmr_sfx_wav = OUT_AUDIO / "EP05_asmr_sfx.wav"
    print(f"[EP05] Sintetizando ASMR Teclado Mecanico + Pops UI en {asmr_sfx_wav}...")
    build_asmr_and_pop_wav(beat_schedules, total_sec, asmr_sfx_wav)

    master_wav = OUT_AUDIO / "EP05_master.wav"
    inputs = [
        "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo:d={total_sec:.3f}",
        "-i", str(asmr_sfx_wav),
    ]
    # ASMR keyboard + delicious pops balanced clearly under voice without masking speech
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
    existing["EP05_FABLE_HYDROGEN"] = beats_out
    BEATS_JSON.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ [EP05_FABLE_HYDROGEN] Total frames={current_frame} ({total_sec:.2f}s) | SFX={asmr_sfx_wav} | WAV={master_wav}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
