#!/usr/bin/env python3
"""
Genera EP06 ("JPMorgan, Visa, Mastercard, IMSS, SAT, INE + Clonación de Voz IA + Cameo Terminator")
aplicando la Fórmula de 7 Bloques (formula-reel-lynxstudios.pdf):
  - "¡Waters!" aislado en inglés nativo (language_code="en")
  - Cameo susurrado rápido ("¡Sí, como en Terminator!") con Robot IA Malo T-800
  - Cortes visuales cada ~2-4s (dividiendo frases largas en sub-escenas visuales sin cortar la voz)
  - Silencio dramático de 0.35s antes de El Giro y el CTA
  - Motor ASMR Teclado Mecánico + Bubble Pops UI + Barrido Cyber Terminator
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
from typing import List, Optional, Tuple

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
ENV_FILE = ROOT / ".env"
OUT_AUDIO = ROOT / "proyectos/waters-serie/renders/audio_elevenlabs_v3/EP06_HACKEOS_Y_VOZ"
EP05_OPENING = ROOT / "proyectos/waters-serie/renders/audio_elevenlabs_v3/EP05_FABLE_HYDROGEN/01_tony.mp3"
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
    stability: float = 0.30,
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
# ASMR SFX ENGINE: Mechanical Keyboard + Bubble UI Pops + Cyber Scanner
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


def add_terminator_scanner(buf_l: List[float], buf_r: List[float], start_sec: float, amp: float = 0.34) -> None:
    """Short metallic cyber pulse + red laser lock when T-800 villain bot appears."""
    dur = 0.26
    n_len = int(dur * SR)
    base_idx = int(start_sec * SR)
    phase = 0.0
    for k in range(n_len):
        dt = k / SR
        att = min(1.0, dt / 0.01)
        f_inst = 95.0 + 420.0 * math.exp(-dt * 12.0)
        phase += 2.0 * math.pi * f_inst / SR
        env = att * math.exp(-dt * 11.0)
        val = (math.sin(phase) + 0.45 * math.sin(2.1 * phase) + 0.18 * math.sin(4.7 * phase)) * env
        _add_sample(buf_l, buf_r, base_idx + k, amp * val, pan=0.25)


def build_ep06_sfx(
    visual_schedules: List[Tuple[float, float, List[int], bool, bool]],
    total_sec: float,
    out_wav: Path,
) -> None:
    """
    visual_schedules rows: (t_start, t_dur, pops_frames, is_silent_pause_lead, is_terminator)
    """
    n_total = int((total_sec + 0.5) * SR)
    buf_l = [0.0] * n_total
    buf_r = [0.0] * n_total
    rng = random.Random(20261120)

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

    for t_start, t_dur, pops, silent_pause, is_term in visual_schedules:
        sfx_anchor = t_start + (0.28 if silent_pause else 0.0)
        if is_term:
            add_terminator_scanner(buf_l, buf_r, t_start + 0.05, amp=0.36)

        for pf in pops:
            t_pop = sfx_anchor + (pf / FPS)
            if t_pop < t_start + t_dur - 0.08:
                f0, f1, amp, spk = pop_profiles.get(pf, (295.0, 850.0, 0.36, False))
                add_ui_pop(buf_l, buf_r, t_pop, f0, f1, amp, spk)

        # Fast mechanical keyboard burst while terminal types
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


EP06_SCRIPT = [
    {
        "id": "01_tony",
        "speaker": "tony",
        "text": "[serious] Waters!",
        "language_code": "en",
        "stability": 0.35,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "ALERTA · CYBER BREACH",
                "accentColor": "#FF3B3B",
                "expression": "shock_sweat",
                "cardType": "cyber_hook",
                "stageProp": "none",
                "stepBadge": "!",
                "pillText": "Más de 10 hackeos en México",
                "headlinePrefix": "¡Acaban de filtrar",
                "headlineFocus": "+10 bases",
                "headlineSuffix": "reales!",
                "terminalCmd": "$ scan --targets jpmorgan visa imss sat ine",
                "terminalSub": "! EXPOSICIÓN ACTIVA · NOMBRES, TELÉFONOS Y VOZ",
                "pops": [2, 8, 20, 32],
            }
        ],
    },
    {
        "id": "02_tony",
        "speaker": "tony",
        "text": "[serious] Hackearon proveedores de JPMorgan, Visa y Mastercard... ¡y en México llevan más de diez hackeos este año: IMSS, SAT, INE y hasta el teléfono de la presidenta!",
        "stability": 0.30,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 0.46,
                "topTag": "EE. UU. · PROVEEDORES FILTRADOS",
                "accentColor": "#FF3B3B",
                "expression": "shock_sweat",
                "cardType": "cyber_hook",
                "stageProp": "laptop",
                "stepBadge": "1",
                "pillText": "JPMorgan, Visa y Mastercard",
                "headlinePrefix": "Hackean proveedores de",
                "headlineFocus": "Visa y Bancos",
                "headlineSuffix": "",
                "terminalCmd": "$ inspect --group n0n --targets jpmorgan,visa",
                "terminalSub": "! Nombres, teléfonos y correos expuestos en dark web",
                "pops": [2, 8, 20, 32],
            },
            {
                "ratio": 0.54,
                "topTag": "MÉXICO · FILTRACIONES RECIENTES",
                "accentColor": "#FF3B3B",
                "expression": "sad_cloud",
                "cardType": "breach_evidence",
                "stageProp": "laptop",
                "stepBadge": "2",
                "pillText": "IMSS, SAT, INE y Presidencia",
                "headlinePrefix": "En México ya van",
                "headlineFocus": "+10 hackeos",
                "headlineSuffix": "este año",
                "terminalCmd": "$ dump --imss 20M --sat-ine 150GB --leak verified",
                "terminalSub": "! Datos reales de millones de mexicanos circulando",
                "pops": [2, 8, 20, 32],
            },
        ],
    },
    {
        "id": "03_agy",
        "speaker": "agy",
        "text": "[serious] La mayoría escucha 'no robaron mi tarjeta' y se confía. Pero hay bancos que aún autentican con tu voz... y hoy con IA como ElevenLabs bastan segundos de tu audio para clonarte.",
        "stability": 0.30,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 0.44,
                "topTag": "EL ERROR COMÚN",
                "accentColor": "#FF3B3B",
                "expression": "sad_cloud",
                "cardType": "breach_evidence",
                "stageProp": "voice_wave",
                "stepBadge": "⚠",
                "pillText": "Confiarse porque 'no cayó tu plástico'",
                "headlinePrefix": "El error es creer que",
                "headlineFocus": "estás a salvo",
                "headlineSuffix": "",
                "terminalCmd": "$ check --voice-auth banking_mx --status enabled",
                "terminalSub": "> Con tu nombre + teléfono arman llamada falsa perfecta",
                "pops": [2, 8, 20, 32],
            },
            {
                "ratio": 0.56,
                "topTag": "ELEVENLABS · CLONACIÓN VOCAL",
                "accentColor": "#FF3B3B",
                "expression": "determined_hacker",
                "cardType": "voice_clone_trap",
                "stageProp": "voice_wave",
                "stepBadge": "🎙",
                "pillText": "Clonan tu voz con 3–10 segundos",
                "headlinePrefix": "Bastan 10 segundos para",
                "headlineFocus": "clonar tu voz",
                "headlineSuffix": "con IA",
                "terminalCmd": "$ clone-voice --sample caller_10s.wav --engine ai",
                "terminalSub": "! Biometría de voz bancaria vulnerada al 99%",
                "pops": [2, 8, 20, 32],
            },
        ],
    },
    {
        "id": "04_tony",
        "speaker": "tony",
        "text": "[serious] La IA avanza más rápido que la ciberseguridad. Hoy ya no puedes confiar ni en tu propia voz.",
        "stability": 0.30,
        "lead_silence_sec": 0.35,  # Pausa dramática antes del Giro!
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "EL GIRO CRÍTICO · 2026",
                "accentColor": "#00F5D4",
                "expression": "determined_hacker",
                "cardType": "giro_punch",
                "stageProp": "voice_wave",
                "stepBadge": "⚡",
                "pillText": "La regla que cambia todo hoy",
                "headlinePrefix": "Ya no confíes ni en",
                "headlineFocus": "tu propia voz",
                "headlineSuffix": "",
                "terminalCmd": "$ alert --rule 'AI speed > Cybersecurity defenses'",
                "terminalSub": "⚠ La voz sola YA NO prueba identidad en 2026",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "05_agy",
        "speaker": "agy",
        "text": "[serious] No dependas de tu oído: usa tres escudos. Quita la voz como llave bancaria, pacta una palabra clave familiar...",
        "stability": 0.30,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "ARQUITECTURA ANTI-FRAUDE",
                "accentColor": "#00F5D4",
                "expression": "happy_open",
                "cardType": "three_shields",
                "stageProp": "shield_vault",
                "stepBadge": "🛡",
                "pillText": "3 Escudos que frenan al clon",
                "headlinePrefix": "Activa ya tus",
                "headlineFocus": "3 escudos",
                "headlineSuffix": "de blindaje",
                "terminalCmd": "$ deploy --shields no-voice,family-key,official-app",
                "terminalSub": "✓ Quitamos voz + pactamos palabra clave secreta",
                "pops": [2, 8, 14, 24, 34],
            }
        ],
    },
    {
        "id": "06_tony",
        "speaker": "tony",
        "text": "[whispering] ¡Sí, como en Terminator: lanzas la pregunta trampa, el clon cae... y cuelgas en seco!",
        "stability": 0.24,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "PROTOCOLO T-800 · PREGUNTA TRAMPA",
                "accentColor": "#FF3B3B",
                "expression": "wink",
                "cardType": "terminator_cameo",
                "stageProp": "terminator",
                "stepBadge": "🤫",
                "pillText": "Di un número / pregunta trampa",
                "headlinePrefix": "¡Sí, como en",
                "headlineFocus": "Terminator 2!",
                "headlineSuffix": "🤖📞",
                "terminalCmd": "$ trap-test --ask 'Clave secreta / Num 1 al 10'",
                "terminalSub": "🤖 Clon IA falla la clave -> ❌ ¡CUELGA EN SECO!",
                "pops": [2, 6, 14, 22],
                "is_terminator": True,
            }
        ],
    },
    {
        "id": "07_agy",
        "speaker": "agy",
        "text": "[confident] ...y verifica todo directo en tu app oficial.",
        "stability": 0.32,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "ESCUDO 3 · CANAL OFICIAL",
                "accentColor": "#00F5D4",
                "expression": "happy_arcs",
                "cardType": "step_single",
                "stageProp": "shield_vault",
                "stepBadge": "✓",
                "pillText": "Nunca verifiques en la misma llamada",
                "headlinePrefix": "Verifica todo directo en",
                "headlineFocus": "tu app oficial",
                "headlineSuffix": "",
                "terminalCmd": "$ verify --channel official_bank_app --hangup true",
                "terminalSub": "✓ Cuelga y abre tu app directamente en tu celular",
                "stepTitle": "Cuelga + Abre tu App",
                "stepDetail": "Nunca devuelvas datos por llamada entrante",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "08_agy",
        "speaker": "agy",
        "text": "[serious] Paso uno: desactiva la autenticación solo por voz y exige token en tu app.",
        "stability": 0.32,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "BLINDAJE · PASO 1 DE 4",
                "accentColor": "#00F5D4",
                "expression": "determined_hacker",
                "cardType": "step_single",
                "stageProp": "shield_vault",
                "stepBadge": "1",
                "pillText": "Desactiva biometría solo por voz",
                "headlinePrefix": "Paso 1: exige",
                "headlineFocus": "token + NIP",
                "headlineSuffix": "en tu app",
                "terminalCmd": "$ bank-security --disable voice-only --enable app-token",
                "terminalSub": "✓ Sin token físico o en app, nadie autoriza movimientos",
                "stepTitle": "1. Quita Voz como Llave Única",
                "stepDetail": "Exige NIP + Token digital en tu banco",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "09_agy",
        "speaker": "agy",
        "text": "[serious] Paso dos: no regales diez segundos de plática a números desconocidos. Ante urgencia, cuelga.",
        "stability": 0.32,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "BLINDAJE · PASO 2 DE 4",
                "accentColor": "#00F5D4",
                "expression": "happy_open",
                "cardType": "step_single",
                "stageProp": "voice_wave",
                "stepBadge": "2",
                "pillText": "No regales muestras de tu voz",
                "headlinePrefix": "Paso 2: regla de",
                "headlineFocus": "cero plática",
                "headlineSuffix": "a desconocidos",
                "terminalCmd": "$ anti-vishing --unknown-urgent-call HANGUP",
                "terminalSub": "✓ Menos de 3 seg = sin muestra para clonar tu voz",
                "stepTitle": "2. Cuelga en menos de 10s",
                "stepDetail": "Sin audio largo no pueden entrenar un clon de IA",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "10_agy",
        "speaker": "agy",
        "text": "[excited] Paso tres: activa alertas desde un peso y mantén apagada tu tarjeta digital.",
        "stability": 0.32,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "BLINDAJE · PASO 3 DE 4",
                "accentColor": "#00F5D4",
                "expression": "star_eyes",
                "cardType": "step_single",
                "stageProp": "laptop",
                "stepBadge": "3",
                "pillText": "Control total en tiempo real",
                "headlinePrefix": "Paso 3: apaga tu",
                "headlineFocus": "tarjeta digital",
                "headlineSuffix": "",
                "terminalCmd": "$ card-lock --alerts min=$1MXN --digital-card FROZEN",
                "terminalSub": "✓ Alertas desde $1 + CVV dinámico encendido solo al pagar",
                "stepTitle": "3. Alertas $1 + Tarjeta Apagada",
                "stepDetail": "Bloquea cargos sorpresa aunque tengan tu nombre",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "11_agy",
        "speaker": "agy",
        "text": "[serious] Paso cuatro: crea una palabra clave secreta con tu familia. Sin esa clave, aunque suene igual, es IA.",
        "stability": 0.30,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "BLINDAJE · PASO 4 DE 4",
                "accentColor": "#00F5D4",
                "expression": "zen_proud",
                "cardType": "step_single",
                "stageProp": "terminator",
                "stepBadge": "4",
                "pillText": "Contraseña verbal familiar",
                "headlinePrefix": "Paso 4: pacta una",
                "headlineFocus": "palabra clave",
                "headlineSuffix": "familiar",
                "terminalCmd": "$ family-auth --challenge secret_phrase --if-fail BLOCK",
                "terminalSub": "✓ Aunque suene idéntico a tu hijo o mamá: sin clave es IA",
                "stepTitle": "4. Palabra Secreta Anti-Clon",
                "stepDetail": "Acordada en persona — nunca por WhatsApp ni llamada",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "12_tony",
        "speaker": "tony",
        "text": "[serious] Si te marcan sabiendo tu nombre y con la voz de alguien cercano, no es magia: son veinte millones de datos del IMSS, ciento cincuenta gigas del SAT e INE... más inteligencia artificial.",
        "stability": 0.30,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "EL PUENTE REAL · POR QUÉ PASA",
                "accentColor": "#FF3B3B",
                "expression": "shock_sweat",
                "cardType": "chaos_bridge",
                "stageProp": "voice_wave",
                "stepBadge": "!",
                "pillText": "Tus datos filtrados + voz IA = estafa",
                "headlinePrefix": "No es magia: son tus",
                "headlineFocus": "datos + IA",
                "headlineSuffix": "",
                "terminalCmd": "$ correlate --imss 20M --sat-ine 150GB --voice-ai 10s",
                "terminalSub": "! Saben tu nombre + teléfono + imitan a quien quieres",
                "pops": [2, 8, 16, 26, 36],
            }
        ],
    },
    {
        "id": "13_agy",
        "speaker": "agy",
        "text": "[excited] Comenta BLINDA y te mando gratis la guía de blindaje contra hackeos y clonación de voz.",
        "stability": 0.32,
        "lead_silence_sec": 0.30,  # Pausa breve dramática antes del CTA!
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "GUÍA PDF + CHECKLIST 10 PUNTOS",
                "accentColor": "#00F5D4",
                "expression": "happy_arcs",
                "cardType": "cta_blinda",
                "stageProp": "kit_box",
                "stepBadge": "🚀",
                "pillText": "Guía gratis en tu DM hoy",
                "headlinePrefix": "Comenta la palabra",
                "headlineFocus": "BLINDA",
                "headlineSuffix": "👇",
                "terminalCmd": "$ send-dm --keyword BLINDA --file guia_10_puntos.pdf",
                "terminalSub": "✓ Incluye Protocolo Terminator + Checklist bancaria 2026",
                "stepTitle": "BLINDA",
                "pops": [2, 8, 18],
            }
        ],
    },
    {
        "id": "14_tony",
        "speaker": "tony",
        "text": "[excited] Waters!",
        "language_code": "en",
        "stability": 0.35,
        "lead_silence_sec": 0.0,
        "visuals": [
            {
                "ratio": 1.0,
                "topTag": "SERIE ¡WATERS! · CAPTOORA",
                "accentColor": "#00F5D4",
                "expression": "wink",
                "cardType": "cta_blinda",
                "stageProp": "kit_box",
                "stepBadge": "🌊",
                "pillText": "¡Toma tus precauciones hoy!",
                "headlinePrefix": "No confíes ni en tu voz:",
                "headlineFocus": "¡WATERS!",
                "headlineSuffix": "🌊🛡️",
                "terminalCmd": "$ status --shield ACTIVE --threat AI_VOICE_CLONE_BLOCKED",
                "terminalSub": "✓ Comenta BLINDA y protege a tu familia hoy",
                "stepTitle": "¡WATERS! 🛡️",
                "pops": [2, 8, 18],
            }
        ],
    },
]


def main() -> int:
    api_key = load_api_key()
    OUT_AUDIO.mkdir(parents=True, exist_ok=True)

    # Reuse exact verified native English "Waters!" from EP05 opening if missing
    first_mp3 = OUT_AUDIO / "01_tony.mp3"
    if not first_mp3.exists() and EP05_OPENING.exists():
        shutil.copy2(EP05_OPENING, first_mp3)
        print(f"[EP06] Copiado opening nativo en ingles desde EP05: {first_mp3}")

    beats_out = []
    audio_events = []
    visual_schedules: List[Tuple[float, float, List[int], bool, bool]] = []
    current_frame = 0

    for item in EP06_SCRIPT:
        mp3_path = OUT_AUDIO / f"{item['id']}.mp3"
        if not mp3_path.exists():
            if not api_key:
                print(f"ERROR: Falta ELEVENLABS_API_KEY para {mp3_path}", file=sys.stderr)
                return 1
            vid = TONY_ID if item["speaker"] == "tony" else AGY_ID
            lang = item.get("language_code")
            stab = item.get("stability", 0.32)
            print(f"[EP06] TTS {item['id']} ({item['speaker']}, lang={lang}): {item['text']}")
            tts_to_mp3(item["text"], vid, mp3_path, api_key, stability=stab, language_code=lang)

        dur = probe_duration(mp3_path)
        lead_sil = item.get("lead_silence_sec", 0.0)
        start_sec = current_frame / FPS
        audio_events.append((start_sec + lead_sil + 0.06, mp3_path))

        total_frames_item = max(52, math.ceil((dur + lead_sil + 0.24) * FPS))
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
            is_term = bool(v.get("is_terminator", False))
            visual_schedules.append((v_start_sec, v_dur_sec, v["pops"], is_pause, is_term))

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
            if "stepTitle" in v:
                beat_entry["stepTitle"] = v["stepTitle"]
            if "stepDetail" in v:
                beat_entry["stepDetail"] = v["stepDetail"]

            beats_out.append(beat_entry)
            current_frame += v_frames

    total_sec = current_frame / FPS
    asmr_sfx_wav = OUT_AUDIO / "EP06_asmr_sfx.wav"
    print(f"[EP06] Sintetizando ASMR Teclado + Pops UI + Scanner T-800 en {asmr_sfx_wav}...")
    build_ep06_sfx(visual_schedules, total_sec, asmr_sfx_wav)

    master_wav = OUT_AUDIO / "EP06_master.wav"
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
    existing["EP06_HACKEOS_Y_VOZ"] = beats_out
    BEATS_JSON.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ [EP06_HACKEOS_Y_VOZ] Visual beats={len(beats_out)} | Total frames={current_frame} ({total_sec:.2f}s) | WAV={master_wav}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
