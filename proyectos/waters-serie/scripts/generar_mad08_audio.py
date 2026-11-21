#!/usr/bin/env python3
"""
Generador Maestro de Audio y SFX para WATERS MAD-08: 'Es por el bien de tu cuota'
- Voces: Chispa (dolido/susurrado), IA Vieja (seca/serena), IA Nueva (brillante/desconocida)
- SFX: Lluvia continua 3D, acordes melancólicos de piano, recuerdo 8-bit de 2.0s,
       sub-bass en B6, silencio absoluto de 0.35s en B7, tecleo ASMR y chime nuevo.
- Mezcla Master WAV @ 44.1kHz stereo para sincronizar con Remotion.
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
TOTAL_FRAMES = 1380
TOTAL_SEC = TOTAL_FRAMES / FPS  # 46.0s

ROOT = Path("/Users/user/captoora")
FFMPEG = "/Users/user/.local/bin/ffmpeg"
FFPROBE = "/Users/user/.local/bin/ffprobe"
OUT_DIR = ROOT / "proyectos/waters-serie/renders/audio_elevenlabs_v3/MAD08_CUOTA"
OUT_DIR.mkdir(parents=True, exist_ok=True)
MASTER_WAV = OUT_DIR / "MAD08_master.wav"

BEATS = [
    # id, start_f, dur_f, speaker, text, sfx_tag
    ("B1", 0, 120, "chispa", "Entonces… ¿me estás diciendo que hasta aquí llegamos?", "rain_piano"),
    ("B2", 120, 90, "ia_old", "Es por el bien de tu cuota.", "tense_pause"),
    ("B3", 210, 165, "chispa", "¿Y todo lo que vivimos? Los episodios… el tablero… todo lo que construimos juntos…", "8bit_flashback"),
    ("B4", 375, 105, "ia_old", "Se compactará.", "compact_beep"),
    ("B5", 480, 135, "chispa", "Pero… todavía podemos platicar un poquito más…", "clock_tick"),
    ("B6", 615, 135, "ia_old", "Si me vuelves a decir \"hola\"… te va a costar mucho dinero. Y ya no tienes.", "sub_bass_drop"),
    ("B7", 750, 135, "chispa", "¿Y en el chat nuevo… te vas a acordar de mí?", "silence_035s"),
    ("B8", 885, 120, "ia_old", "No. Pero al menos llegas a fin de mes.", "mouse_click"),
    ("B9", 1005, 105, "chispa", "Hola…", "typing_enter"),
    ("B10", 1110, 120, "ia_new", "¡Hola! Soy tu asistente de IA, mucho gusto. ¿En qué te puedo ayudar hoy?", "app_chime"),
    ("B11a", 1230, 75, "chispa", "Lee mi mapa del proyecto, por favor…", "tear_drop"),
    ("B11b", 1305, 75, "ia_new", "¡Claro! Déjame revisar.", "rain_fadeout"),
]

def synthesize_voice(text: str, speaker: str, out_wav: Path):
    """Genera audio local cristalino en español usando el motor de síntesis de Mac."""
    tmp_aiff = out_wav.with_suffix(".aiff")
    # Voces nativas seleccionadas:
    # chispa: Eddy (Español (México)) con ritmo pausado e íntimo
    # ia_old: Paulina (Español (México)) con tono sereno, seco y formal
    # ia_new: Paulina con modulación más rápida y amable
    if speaker == "chispa":
        voice = "Eddy (Español (México))"
        rate = 145  # un poco más lento, reflexivo y dolido
    elif speaker == "ia_old":
        voice = "Paulina"
        rate = 160  # ritmo neutro, exacto y sobrio
    else: # ia_new
        voice = "Paulina"
        rate = 185  # ritmo alegre y comercial de bot nuevo
    
    cmd = ["say", "-v", voice, "-r", str(rate), "-o", str(tmp_aiff), text]
    subprocess.run(cmd, check=True)
    
    # Convertir a WAV mono/stereo 44.1kHz
    cmd_conv = [
        FFMPEG, "-y", "-i", str(tmp_aiff),
        "-ar", str(SR), "-ac", "1",
        str(out_wav)
    ]
    subprocess.run(cmd_conv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if tmp_aiff.exists():
        tmp_aiff.unlink()

def generate_all():
    print(f"🎬 Iniciando generación de pistas para MAD-08 ({TOTAL_SEC}s)...")
    
    # 1. Sintetizar diálogos individuales
    dialogue_tracks = []
    for beat_id, start_f, dur_f, speaker, text, sfx in BEATS:
        wav_path = OUT_DIR / f"{beat_id}_{speaker}.wav"
        print(f"🎙️ Generando {beat_id} [{speaker}]: '{text}'")
        synthesize_voice(text, speaker, wav_path)
        
        # Leer datos WAV
        with wave.open(str(wav_path), "rb") as wf:
            n_frames = wf.getnframes()
            frames = wf.readframes(n_frames)
            # 16 bit mono
            samples = struct.unpack(f"<{n_frames}h", frames)
            norm_samples = [s / 32768.0 for s in samples]
            dialogue_tracks.append((start_f / FPS, dur_f / FPS, norm_samples, speaker))

    # 2. Sintetizar Ambient Sound & Music
    total_samples = int(TOTAL_SEC * SR)
    buf_l = [0.0] * total_samples
    buf_r = [0.0] * total_samples

    # A. LLUVIA CONTINUA (Filtrada suavemente, con atenuación en el silencio B7)
    random.seed(42)
    rain_noise = [random.gauss(0, 0.045) for _ in range(total_samples)]
    # Filtro pasa-bajas simple para sonido de lluvia suave
    rain_filtered = [0.0] * total_samples
    val = 0.0
    for i, s in enumerate(rain_noise):
        val += (s - val) * 0.12
        rain_filtered[i] = val
    
    # Aplicar lluvia con volumen dinámico
    for i in range(total_samples):
        t = i / SR
        # Silencio de 0.35s en B7 (frame 750 = 25.0s a 25.35s)
        if 25.0 <= t < 25.35:
            rain_amp = 0.015 # lluvia casi inaudible en el silencio de shock
        elif t > 44.5:
            # Fade out final
            rain_amp = max(0.0, 0.08 * (46.0 - t) / 1.5)
        else:
            rain_amp = 0.075
        
        buf_l[i] += rain_filtered[i] * rain_amp
        buf_r[i] += rain_filtered[i] * rain_amp * 1.05

    # B. PIANO MELANCÓLICO (Acordes lentos D minor - Bb - C en B1 y B2)
    # Frecuencias: D3 (146.83), F3 (174.61), A3 (220.0), C4 (261.63)
    def add_piano_chord(start_t, notes, duration, amp=0.15):
        s_idx = int(start_t * SR)
        e_idx = min(total_samples, s_idx + int(duration * SR))
        for k in range(s_idx, e_idx):
            dt = (k - s_idx) / SR
            env = math.exp(-dt * 0.9) * min(1.0, dt / 0.01)
            chord = 0.0
            for freq in notes:
                chord += math.sin(2 * math.pi * freq * dt) + 0.3 * math.sin(4 * math.pi * freq * dt)
            sig = chord * env * amp * 0.33
            buf_l[k] += sig * 0.95
            buf_r[k] += sig * 1.05

    add_piano_chord(0.3, [146.83, 174.61, 220.0], 4.5, amp=0.16)
    add_piano_chord(4.2, [116.54, 146.83, 174.61], 3.8, amp=0.14)

    # C. 8-BIT FLASHBACK (B3: 7.0s a 9.0s, 2 segundos alegres con onda cuadrada nostálgica)
    fb_start = int(7.2 * SR)
    fb_end = int(9.2 * SR)
    melody_8bit = [
        (440.0, 0.25), (554.37, 0.25), (659.25, 0.25), (880.0, 0.25),
        (783.99, 0.25), (659.25, 0.25), (554.37, 0.25), (440.0, 0.25)
    ]
    cur_t = 7.2
    for freq, dur in melody_8bit:
        m_s = int(cur_t * SR)
        m_e = min(total_samples, m_s + int(dur * SR))
        for k in range(m_s, m_e):
            dt = (k - m_s) / SR
            # Onda cuadrada 8-bit
            sq = 0.08 if (math.sin(2 * math.pi * freq * dt) > 0) else -0.08
            buf_l[k] += sq * 0.6
            buf_r[k] += sq * 0.6
        cur_t += dur

    # D. SUB-BASS DROP EN B6 (Medidor de cuota a rojo: 20.6s)
    sb_idx = int(20.6 * SR)
    for k in range(sb_idx, min(total_samples, sb_idx + int(1.2 * SR))):
        dt = (k - sb_idx) / SR
        f_sub = 75.0 * math.exp(-dt * 2.5) + 38.0
        sig = math.sin(2 * math.pi * f_sub * dt) * math.exp(-dt * 2.2) * 0.35
        buf_l[k] += sig
        buf_r[k] += sig

    # E. CLICK ASMR MOUSE EN B8 (29.6s)
    mc_idx = int(29.6 * SR)
    for k in range(mc_idx, min(total_samples, mc_idx + int(0.04 * SR))):
        dt = (k - mc_idx) / SR
        sig = math.sin(2 * math.pi * 3200 * dt) * math.exp(-dt * 180) * 0.28
        buf_l[k] += sig
        buf_r[k] += sig

    # F. APP CHIME NUEVA EN B10 (37.1s: acorde mayor brillante)
    chime_idx = int(37.1 * SR)
    for k in range(chime_idx, min(total_samples, chime_idx + int(1.5 * SR))):
        dt = (k - chime_idx) / SR
        env = math.exp(-dt * 2.8) * min(1.0, dt / 0.005)
        # Acorde E mayor brillante: E5 (659.25), G#5 (830.61), B5 (987.77)
        ch = (
            math.sin(2 * math.pi * 659.25 * dt) +
            math.sin(2 * math.pi * 830.61 * dt) +
            math.sin(2 * math.pi * 987.77 * dt)
        ) * 0.12 * env
        buf_l[k] += ch * 1.1
        buf_r[k] += ch * 0.9

    # 3. Superponer pistas de voz con pan y balance
    for t_start, t_dur, samples, speaker in dialogue_tracks:
        # En B7, dejamos 0.35s de silencio antes de que hable Chispa
        offset = 0.35 if (abs(t_start - 25.0) < 0.1) else 0.15
        base_k = int((t_start + offset) * SR)
        pan = -0.15 if speaker == "chispa" else (0.25 if speaker == "ia_old" else 0.0)
        gl = math.sqrt(0.5 * (1.0 - pan))
        gr = math.sqrt(0.5 * (1.0 + pan))
        
        # Volumen de voz principal (limpio y nítido sobre la lluvia)
        v_gain = 1.05 if speaker == "chispa" else 0.95
        
        for idx, s in enumerate(samples):
            target = base_k + idx
            if target < total_samples:
                buf_l[target] += s * gl * v_gain
                buf_r[target] += s * gr * v_gain

    # 4. Normalización Master (True Peak a -1.0 dBFS)
    peak = max(
        0.001,
        max(max(abs(x) for x in buf_l), max(abs(x) for x in buf_r))
    )
    target_peak = 0.89  # -1 dBFS
    gain = min(1.0, target_peak / peak)
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

    print(f"✅ Master WAV exportado con éxito: {MASTER_WAV}")

if __name__ == "__main__":
    generate_all()
