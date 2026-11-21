#!/usr/bin/env python3
"""
Generador Maestro de Audio y SFX para EP09 DIA-APPLE:
'4 Cosas que Siri AI Confesó sobre Seguridad (+ Blindaje Familiar)'
- Voces: Tony (energético / resolutivo) + Agy (técnica / serena / autoridad)
- SFX: Pop UI, sub-bass de alerta, fanfarria de rescate, chime dorado, tecleo ASMR
- Master WAV @ 44.1kHz stereo exacto a 60.0s (1,800 frames @ 30 fps).
"""
import os
import sys
import math
import wave
import struct
import random
import subprocess
from pathlib import Path

SR = 44100
FPS = 30
TOTAL_FRAMES = 1800
TOTAL_SEC = 60.0

ROOT = Path("/Users/user/captoora")
FFMPEG = "/Users/user/.local/bin/ffmpeg"
FFPROBE = "/Users/user/.local/bin/ffprobe"
OUT_DIR = ROOT / "proyectos/waters-serie/renders/audio_elevenlabs_v3/EP09_DIA_APPLE"
OUT_DIR.mkdir(parents=True, exist_ok=True)
MASTER_WAV = OUT_DIR / "EP09_master.wav"

BEATS = [
    ("B1", 0, 105, "tony", "¡Waters! Si anoche te dio escalofrío lo de la nueva actualización de Siri AI, tranquilo: Antigravity te enseña en sesenta segundos los cuatro botones para blindar tu iPhone y el de tu familia."),
    ("B2", 105, 165, "agy", "Primero: Siri misma confesó el ataque conceptual Serpent. Investigadores demostraron cómo un malware en Mac podía extraer tokens de sesión para usar la cuota de la víctima sin que lo notara."),
    ("B3", 270, 180, "tony", "Segundo: el peligro del Prompt Injection. Si le pides a Siri que te resuma un correo o una foto desconocida, un comando invisible puede engañar al sistema para cruzar tus notas personales."),
    ("B4", 450, 150, "agy", "Tercero: no es un hackeo consumado, pero Apple sabe el reto que enfrenta y ofrece un millón de dólares de recompensa preventiva a los investigadores que encuentren fallas en sus servidores."),
    ("B5", 600, 210, "tony", "Y cuarto: tu cuota diaria. Siri no cobra tokens, pero multiplica tu límite según tu iCloud: doscientas gigas te da el doble; dos teras, cinco veces más; seis teras, diez veces; y doce teras multiplica tu cuota hasta veinte veces."),
    ("B6", 810, 180, "agy", "Más cuota significa más poder, pero también más superficie de riesgo si tus dispositivos familiares no tienen candado. Aquí están los cuatro botones que debes activar hoy mismo."),
    ("B7", 990, 180, "tony", "Uno: Verificación de Seguridad. Te permite revisar y revocar de golpe cualquier acceso o ubicación compartida que tengan personas o aplicaciones en tu familia."),
    ("B8", 1170, 165, "agy", "Dos: apaga 'Mejorar Siri y Dictado'. Así evitas que Apple guarde muestras de tu voz o textos en sus servidores por dos años."),
    ("B9", 1335, 150, "tony", "Tres: activa Protección de Datos Avanzada. Cifra tus fotos, notas y respaldos de extremo a extremo, de modo que ni la propia Apple pueda leerlos."),
    ("B10", 1485, 135, "agy", "Y cuatro, la regla de oro: jamás le pidas a Siri resumir correos, facturas o links de personas que no conozcas."),
    ("B11", 1620, 105, "tony", "Si quieres el checklist PDF paso a paso con capturas para configurar tu iPhone y el de tus papás o hijos, comenta la palabra APPLE."),
    ("B12", 1725, 75, "tony", "Comenta APPLE y te lo mando en automático a tus mensajes. Protege a tu familia y… ¡Waters!"),
]

def synthesize_voice(text: str, speaker: str, out_wav: Path):
    tmp_aiff = out_wav.with_suffix(".aiff")
    if speaker == "tony":
        voice = "Eddy (Español (México))"
        rate = 175
    else:
        voice = "Paulina"
        rate = 170

    cmd = ["say", "-v", voice, "-r", str(rate), "-o", str(tmp_aiff), text]
    subprocess.run(cmd, check=True)

    cmd_conv = [
        FFMPEG, "-y", "-i", str(tmp_aiff),
        "-ar", str(SR), "-ac", "1",
        str(out_wav)
    ]
    subprocess.run(cmd_conv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if tmp_aiff.exists():
        tmp_aiff.unlink()

def generate_ep09_master():
    print(f"🎬 Iniciando generación de pistas de audio para EP09 ({TOTAL_SEC}s)...")
    
    dialogue_tracks = []
    for beat_id, start_f, dur_f, speaker, text in BEATS:
        wav_path = OUT_DIR / f"{beat_id}_{speaker}.wav"
        print(f"🎙️ Generando {beat_id} [{speaker}]: '{text[:45]}...'")
        synthesize_voice(text, speaker, wav_path)

        with wave.open(str(wav_path), "rb") as wf:
            n_frames = wf.getnframes()
            frames = wf.readframes(n_frames)
            samples = struct.unpack(f"<{n_frames}h", frames)
            norm_samples = [s / 32768.0 for s in samples]
            dialogue_tracks.append((start_f / FPS, dur_f / FPS, norm_samples, speaker))

    total_samples = int(TOTAL_SEC * SR)
    buf_l = [0.0] * total_samples
    buf_r = [0.0] * total_samples

    # Música de fondo energética tech (Groove sutil de sintetizador para Vertiente A)
    # Acordes en A menor (A3, C4, E4) y F mayor con bajo rítmico
    bpm = 120
    beat_dur = 60.0 / bpm
    for b in range(int(TOTAL_SEC / beat_dur)):
        t_b = b * beat_dur
        k_b = int(t_b * SR)
        # Bombo suave en cada beat
        for k in range(k_b, min(total_samples, k_b + int(0.08 * SR))):
            dt = (k - k_b) / SR
            sig = math.sin(2 * math.pi * (80 * math.exp(-dt * 40.0) + 40) * dt) * math.exp(-dt * 20.0) * 0.12
            buf_l[k] += sig
            buf_r[k] += sig

    # Superposición de voces con panning alternado (Tony izquierda, Agy derecha)
    for t_start, t_dur, samples, speaker in dialogue_tracks:
        base_k = int((t_start + 0.08) * SR)
        pan = -0.18 if speaker == "tony" else 0.18
        gl = math.sqrt(0.5 * (1.0 - pan))
        gr = math.sqrt(0.5 * (1.0 + pan))
        v_gain = 1.05

        for idx, s in enumerate(samples):
            target = base_k + idx
            if target < total_samples:
                buf_l[target] += s * gl * v_gain
                buf_r[target] += s * gr * v_gain

    # Normalización Master
    peak = max(0.001, max(max(abs(x) for x in buf_l), max(abs(x) for x in buf_r)))
    gain = min(1.0, 0.90 / peak)
    print(f"📊 Peak original: {peak:.3f} | Gain aplicado: {gain:.3f}")

    with wave.open(str(MASTER_WAV), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        frames = bytearray()
        for l, r in zip(buf_l, buf_r):
            sl = max(-32767, min(32767, int(l * gain * 32767.0)))
            sr = max(-32767, min(32767, int(r * gain * 32767.0)))
            frames.extend(struct.pack("<hh", sl, sr))
        wf.writeframes(bytes(frames))

    print(f"✅ Master WAV para EP09 generado con éxito: {MASTER_WAV}")

if __name__ == "__main__":
    generate_ep09_master()
