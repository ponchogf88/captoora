#!/usr/bin/env python3
"""
Genera y mezcla los audios maestros (Short 60s 9:16 + Explicativo ~3 min 16:9)
para la serie ¿Oro Puro o Puro Humo? sobre Gemini 4 Carbon en Ciberseguridad.
Reutiliza waters_audio_engine.py y guarda cache MP3 por bloque (cero re-síntesis).
"""
import json
import math
import random
import struct
import subprocess
import sys
import urllib.request
import wave
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
SCRIPTS_DIR = ROOT / "proyectos/waters-serie/scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import waters_audio_engine as engine  # noqa: E402

WORK_DIR = ROOT / "proyectos/waters-serie/carbon_ciberseguridad"
AUDIO_DIR = WORK_DIR / "audio"
CACHE_SHORT = AUDIO_DIR / "cache/short_60s"
CACHE_LONG = AUDIO_DIR / "cache/explainer_3min"
TIMINGS_JSON = AUDIO_DIR / "carbon_timings.json"

FFMPEG = engine.FFMPEG
FFPROBE = engine.FFPROBE
SR = 44100


SHORT_SCRIPT: List[Dict[str, Any]] = [
    {
        "id": "S1_hook",
        "pause_after": 0.25,
        "text": (
            "¿Google dice que Gemini cuatro Carbon es el nuevo rey en ciberseguridad? "
            "Aquí no creemos nada sin ver las pruebas."
        ),
    },
    {
        "id": "S2_secbench",
        "pause_after": 0.25,
        "text": (
            "Prueba uno: SEC-bench Pro. Carbon logró ochenta y ocho punto dos por ciento "
            "cazando fallos reales en Docker, arriba de GPT-seis punto dos Astra."
        ),
    },
    {
        "id": "S3_exploitgym",
        "pause_after": 0.25,
        "text": (
            "Prueba dos: ExploitGym, de UC Berkeley y Max Planck. "
            "Carbon sacó cincuenta y cuatro punto ocho por ciento, frente a cuarenta y dos punto cuatro "
            "de Astra y treinta y cuatro punto cinco de Claude Opus cinco punto cinco."
        ),
    },
    {
        "id": "S4_cwebench",
        "pause_after": 0.25,
        "text": (
            "Prueba tres: CWE-bench, de Collinear AI. "
            "Setenta y uno por ciento parchando repos sin pista previa, superando el sesenta y ocho "
            "de OpenAI y sesenta y siete de Anthropic."
        ),
    },
    {
        "id": "S5_letrachiquita",
        "pause_after": 0.25,
        "text": (
            "Pero va la letra chiquita: esas tres notas no se suman. "
            "Astra sacó cien en ExploitBench, Claude Fable sigue fortísimo en código diario, "
            "y Carbon quema más thinking tokens."
        ),
    },
    {
        "id": "S6_cta",
        "pause_after": 0.35,
        "text": (
            "En tu plan Google Pro úsalo como cirujano para auditorías, no para todo. "
            "Comenta CARBON para recibir los links a los tres estudios."
        ),
    },
]


LONG_SCRIPT: List[Dict[str, Any]] = [
    {
        "id": "L01_hook",
        "chapter": "01 · El Reclamo",
        "pause_after": 0.35,
        "text": (
            "Google acaba de habilitar Gemini cuatro Carbon dentro de Google Pro y lo presume como su modelo "
            "estrella en ciberseguridad. Pero con filtro ¿Oro Puro o Puro Humo?, la primera pregunta es obligada: "
            "¿de dónde sacó esos datos, contra quién compitió y qué letra chiquita hay detrás?"
        ),
    },
    {
        "id": "L02_origen",
        "chapter": "02 · Origen",
        "pause_after": 0.35,
        "text": (
            "Primero los hechos: DeepMind anunció Carbon el veintiocho de octubre y lo abrió a desarrolladores "
            "el diez de noviembre de dos mil veintiséis. Como detecta y encadena fallos complejos, "
            "al inicio lo restringieron al Programa Fairwind para defensores verificados y pruebas "
            "previas con el gobierno de Estados Unidos."
        ),
    },
    {
        "id": "L03_secbench",
        "chapter": "03 · SEC-bench Pro",
        "pause_after": 0.35,
        "text": (
            "Prueba número uno: SEC-bench Pro, enfocada en cacería real de vulnerabilidades dentro "
            "de contenedores Docker sobre motores como V8, SpiderMonkey y el kernel de Linux. "
            "Aquí Gemini cuatro Carbon marcó ochenta y ocho punto dos por ciento, "
            "superando por margen estrecho a GPT-seis punto dos Astra, que rondó el ochenta y cinco a ochenta y seis por ciento."
        ),
    },
    {
        "id": "L04_exploitgym",
        "chapter": "04 · ExploitGym",
        "pause_after": 0.35,
        "text": (
            "Prueba número dos: ExploitGym, presentada en mayo de dos mil veintiséis por investigadores "
            "de UC Berkeley, Instituto Max Planck, Santa Bárbara y Arizona, junto con gente de Anthropic, OpenAI y Google. "
            "Evalúa si el modelo arma un exploit funcional sobre ochocientos noventa y ocho fallos reales. "
            "Aquí Carbon marcó su ventaja más clara: cincuenta y cuatro punto ocho por ciento, "
            "contra cuarenta y dos punto cuatro de Astra y treinta y cuatro punto cinco de Claude Opus cinco punto cinco."
        ),
    },
    {
        "id": "L05_cwebench",
        "chapter": "05 · CWE-bench",
        "pause_after": 0.35,
        "text": (
            "Prueba número tres: CWE-bench, liberada en octubre por Collinear AI, un tercero independiente. "
            "Aquí se mide defensa pura: al agente le dan un repositorio sin decirle dónde está el error y debe hallarlo "
            "y parcharlo sin romper la app. Carbon logró setenta y uno por ciento frente a cerca de sesenta y ocho "
            "de OpenAI y sesenta y siete de Anthropic."
        ),
    },
    {
        "id": "L06_vs_astra_fable",
        "chapter": "06 · Vs Astra y Fable",
        "pause_after": 0.35,
        "text": (
            "¿Y qué hacen los rivales que Carbon no hace solo? GPT-seis Astra es su competidor más cercano "
            "y reportó cien por ciento en ExploitBench, alcanzando nivel Crítico en seguridad de OpenAI. "
            "Por su parte, Claude Opus cinco punto cinco y Fable cinco punto dos pelean el liderazgo en agentes "
            "de programación diaria; además, Anthropic aplica candados estrictos en modelos abiertos "
            "y reserva capacidades ofensivas sensibles para programas cerrados."
        ),
    },
    {
        "id": "L07_vs_grok",
        "chapter": "06 · Vs Grok y Ranking",
        "pause_after": 0.35,
        "text": (
            "¿Y dónde queda Grok? Los modelos Grok cuatro punto seis y cuatro punto siete también se prueban "
            "en suites como CyberGym y ExploitGym o dentro de editores como Cursor, pero no publicaron puntajes por arriba "
            "de Carbon en esta triple tabla. Al debutar, Carbon lideró el índice Artificial Analysis cinco punto cero "
            "con cincuenta y nueve puntos, seguido de cerca por Opus con cincuenta y ocho y Astra con cincuenta y siete."
        ),
    },
    {
        "id": "L08_letrachiquita_1",
        "chapter": "07 · Letra Chiquita I",
        "pause_after": 0.35,
        "text": (
            "Ahora la letra chiquita crítica. Primero: estas tres cifras miden datasets distintos "
            "y no pueden multiplicarse ni sumarse como porcentaje mágico de inmunidad. "
            "Segundo: el puntaje al primer intento, pass at one, esconde estabilidad: "
            "Carbon piensa mucho más tiempo usando thinking tokens, así que cada respuesta cuesta más cuota."
        ),
    },
    {
        "id": "L09_letrachiquita_2",
        "chapter": "07 · Letra Chiquita II",
        "pause_after": 0.35,
        "text": (
            "Tercero: casi todas estas pruebas corren en laboratorios Docker con fallos históricos conocidos. "
            "Tener setenta y uno por ciento en parches no significa que puedas soltar un agente sin supervisión "
            "en producción; el veintinueve por ciento restante sigue necesitando criterio humano y arquitectura defensiva."
        ),
    },
    {
        "id": "L10_finops_pro",
        "chapter": "08 · Regla Google Pro",
        "pause_after": 0.35,
        "text": (
            "¿Cómo aprovecharlo hoy si pagas Google AI Pro? Usa la regla del cirujano: "
            "deja a Neon o Hydrogen para la talacha diaria y usa Carbon solo cuando toque auditar "
            "un repositorio sospechoso, revisar seguridad o resolver un bloqueo difícil."
        ),
    },
    {
        "id": "L11_cta",
        "chapter": "09 · Fuentes y CTA",
        "pause_after": 0.45,
        "text": (
            "Puedes verificar cada número en el blog de DeepMind, los papers de ExploitGym y SEC-bench Pro, "
            "CWE-bench punto com y Artificial Analysis. Veredicto: músculo real en pruebas, con letra chiquita clara. "
            "Comenta AUDITA si quieres la checklist de seguridad y los enlaces directos."
        ),
    },
]


def build_ambient_bed(total_sec: float, out_wav: Path, seed: int = 77) -> None:
    """Cama investigativa sutil y determinista a muy bajo nivel (-24 dB) para no tapar la voz."""
    n_total = int((total_sec + 0.3) * SR)
    rng = random.Random(seed)
    # Acorde menor cálido suave (La menor suave: A2=110, E3=164.81, C4=261.63, G4=392.0)
    freqs = (110.0, 164.81, 261.63, 392.0)
    buf = bytearray()
    for i in range(n_total):
        t = i / SR
        env_fade = min(1.0, t / 0.8) * min(1.0, max(0.0, (total_sec - t) / 0.9))
        pulse = 0.72 + 0.28 * math.sin(2.0 * math.pi * 0.25 * t)
        val = 0.0
        for idx, f in enumerate(freqs):
            val += math.sin(2.0 * math.pi * f * t + idx * 0.6) * (0.28 / (idx + 1))
        # Micro pulso de reloj cada 1.0s muy suave
        sub = t % 1.0
        tick = math.sin(2.0 * math.pi * 880.0 * sub) * math.exp(-sub * 85.0) * 0.045
        sample = (val * 0.14 * pulse + tick) * env_fade
        s_i = max(-32767, min(32767, int(sample * 32767.0)))
        buf.extend(struct.pack("<hh", s_i, s_i))
        _ = rng  # determinism guard
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(bytes(buf))


def mix_piece(
    tag: str,
    script: List[Dict[str, Any]],
    cache_dir: Path,
    master_wav: Path,
    api_key: str,
    seed: int,
) -> Dict[str, Any]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    clips: List[Dict[str, Any]] = []
    t_cursor = 0.15
    total_chars = 0

    for item in script:
        mp3_path = cache_dir / f"{item['id']}.mp3"
        chars = len(item["text"])
        total_chars += chars
        if not mp3_path.exists():
            if not api_key:
                raise RuntimeError(f"Falta ELEVENLABS_API_KEY para sintetizar {item['id']}")
            print(f"[{tag}] TTS {item['id']} ({chars} chars)...")
            engine.tts_to_mp3(
                item["text"],
                engine.TONY_ID,
                mp3_path,
                api_key,
                stability=0.34,
                language_code="es",
            )
        else:
            print(f"[{tag}] Cache HIT {item['id']} ({chars} chars)")

        dur = engine.probe_duration(mp3_path)
        pause = float(item.get("pause_after", 0.25))
        start_s = round(t_cursor, 3)
        end_s = round(t_cursor + dur + pause, 3)
        clips.append(
            {
                "id": item["id"],
                "chapter": item.get("chapter", item["id"]),
                "start": start_s,
                "voice_end": round(t_cursor + dur, 3),
                "end": end_s,
                "duration": round(end_s - start_s, 3),
                "voice_dur": round(dur, 3),
                "chars": chars,
                "mp3": str(mp3_path.relative_to(ROOT)),
            }
        )
        t_cursor = end_s

    total_dur = round(t_cursor + 0.35, 2)

    # Sintetizar capa SFX (teclado mecánico + pop al arranque de cada bloque)
    n_total = int((total_dur + 0.5) * SR)
    buf_l = [0.0] * n_total
    buf_r = [0.0] * n_total
    rng = random.Random(seed)

    for ci, cl in enumerate(clips):
        st = cl["start"]
        engine.add_ui_pop(
            buf_l,
            buf_r,
            max(0.02, st - 0.04),
            f_start=260.0 + (ci % 4) * 35.0,
            f_end=780.0 + (ci % 4) * 50.0,
            amp=0.30,
            with_sparkle=(ci == 0 or ci == len(clips) - 1),
        )
        # Breve ráfaga de teclas mecánicas al inicio de cada bloque de datos
        for ki in range(6):
            tk = st + 0.06 + ki * 0.055 + rng.uniform(-0.005, 0.005)
            engine.add_mech_keystroke(
                buf_l,
                buf_r,
                tk,
                rng,
                is_enter=(ki == 5),
                pan=((ki % 5) - 2) * 0.14,
                amp=0.18,
            )

    sfx_wav = AUDIO_DIR / f"{tag}_sfx.wav"
    peak = max(0.001, max(max(abs(x) for x in buf_l), max(abs(x) for x in buf_r)))
    gain = min(1.0, 0.72 / peak)
    with wave.open(str(sfx_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        raw = bytearray()
        for lv, rv in zip(buf_l, buf_r):
            raw.extend(struct.pack("<hh", max(-32767, min(32767, int(lv * gain * 32767))), max(-32767, min(32767, int(rv * gain * 32767)))))
        wf.writeframes(bytes(raw))

    bed_wav = AUDIO_DIR / f"{tag}_bed.wav"
    build_ambient_bed(total_dur, bed_wav, seed=seed + 11)

    # Mezcla maestra final en WAV
    inputs = [
        "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=stereo:d={total_dur:.3f}",
        "-i", str(sfx_wav),
        "-i", str(bed_wav),
    ]
    filters = ["[1:a]volume=0.58[sfx]", "[2:a]volume=0.22[bed]"]
    mix_labels = ["[0:a]", "[sfx]", "[bed]"]
    for idx, cl in enumerate(clips, start=3):
        inputs.extend(["-i", str(ROOT / cl["mp3"])])
        ms = int(cl["start"] * 1000)
        lbl = f"[v{idx}]"
        filters.append(f"[{idx}:a]adelay={ms}|{ms},volume=1.28{lbl}")
        mix_labels.append(lbl)

    fc = ";".join(filters) + ";" + "".join(mix_labels) + f"amix=inputs={len(mix_labels)}:duration=longest:normalize=0,alimiter=limit=0.92[aout]"
    subprocess.run(
        [FFMPEG, "-y", *inputs, "-filter_complex", fc, "-map", "[aout]", "-t", f"{total_dur:.3f}", "-ar", str(SR), "-ac", "2", str(master_wav)],
        check=True,
        capture_output=True,
    )

    probe_out = subprocess.check_output(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration:stream=codec_name,sample_rate", "-of", "default=noprint_wrappers=1:nokey=1", str(master_wav)],
        text=True,
    ).strip().replace("\n", " | ")
    print(f"OK {master_wav.name} ({master_wav.stat().st_size} B) -> {probe_out}")

    return {
        "total_duration": total_dur,
        "total_chars": total_chars,
        "master_wav": str(master_wav.relative_to(ROOT)),
        "clips": clips,
    }


def check_elevenlabs_quota(api_key: str) -> Dict[str, Any]:
    try:
        req = urllib.request.Request(
            "https://api.elevenlabs.io/v1/user/subscription",
            headers={"xi-api-key": api_key},
        )
        data = json.loads(urllib.request.urlopen(req, timeout=15).read())
        used = int(data.get("character_count", 0))
        limit = int(data.get("character_limit", 0))
        return {"character_count": used, "character_limit": limit, "remaining": limit - used}
    except Exception as exc:
        return {"error": str(exc)}


def main() -> int:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    api_key = engine.load_api_key()
    before = check_elevenlabs_quota(api_key) if api_key else {}
    print("ElevenLabs quota BEFORE:", before)

    short_meta = mix_piece(
        "short_60s",
        SHORT_SCRIPT,
        CACHE_SHORT,
        AUDIO_DIR / "carbon_short_60s_master.wav",
        api_key,
        seed=401,
    )
    long_meta = mix_piece(
        "explainer_3min",
        LONG_SCRIPT,
        CACHE_LONG,
        AUDIO_DIR / "carbon_explainer_3min_master.wav",
        api_key,
        seed=502,
    )

    after = check_elevenlabs_quota(api_key) if api_key else {}
    print("ElevenLabs quota AFTER:", after)

    payload = {
        "short_60s": short_meta,
        "explainer_3min": long_meta,
        "elevenlabs_quota_before": before,
        "elevenlabs_quota_after": after,
    }
    TIMINGS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote timings -> {TIMINGS_JSON}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
