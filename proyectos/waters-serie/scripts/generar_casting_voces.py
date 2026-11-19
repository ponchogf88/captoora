#!/usr/bin/env python3
"""
Genera 8 muestras cortas de Casting de Voces & Ritmos en ElevenLabs
probando eleven_v3 (Expressive Mode con respiraciones/emociones) y ritmos variados,
y construye un reproductor HTML local para escucharlas con 1 clic.
"""
import json
import os
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
ENV_FILE = ROOT / ".env"
OUT_DIR = ROOT / "proyectos/waters-serie/renders/casting_voces"


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


SAMPLES = [
    {
        "id": "01_chuy_clon_v3_dramatico",
        "title": "01 · Tu Voz Clonada (chuy) — v3 Dramático + Suspiro",
        "role": "CHUY",
        "voice_id": "2GvH1uOsZcLg7MmLn5b2",
        "model_id": "eleven_v3",
        "stability": 0.30,
        "text": "[gasps] ¡Waters gamers! O sea... ¿si bajo un link falso de GTA seis, pierdo mi cuenta?! [nervous] No manches...",
    },
    {
        "id": "02_cristian_v3_intriga",
        "title": "02 · Cristian Medina — v3 Intriga + Susurro",
        "role": "CHUY",
        "voice_id": "6hfb8itl0CXl6ZA7WVIA",
        "model_id": "eleven_v3",
        "stability": 0.35,
        "text": "[sighs] Escucha esto... hoy salió GTA seis y ya lleva millones de vistas. [whispering] Pero aguas, porque hay una trampa.",
    },
    {
        "id": "03_diego_v3_ritmo_tiktok",
        "title": "03 · Diego — v3 Ritmo Ágil TikTok",
        "role": "CHUY",
        "voice_id": "J3JSkWXJwqClE1dIxQM9",
        "model_id": "eleven_v3",
        "stability": 0.30,
        "text": "[excited] ¡Aguas! Si te llegó un crack gratis de GTA seis... [serious] no lo abras, te vacían la cuenta en segundos.",
    },
    {
        "id": "04_antonio_v3_cercano",
        "title": "04 · Antonio — v3 Cercano + Risa Alivio",
        "role": "CHUY",
        "voice_id": "htFfPSZGJwjBv1CL0aMD",
        "model_id": "eleven_v3",
        "stability": 0.35,
        "text": "[sighs] Qué coraje perder años de progreso... [laughs] ¡pero por fin quedó blindada al cien!",
    },
    {
        "id": "05_agy_liam_v3_orion",
        "title": "05 · Agy (Liam) — v3 Estilo Gemini Orion Tech",
        "role": "AGY",
        "voice_id": "TX3LPaxmHKxFdv7VOQHJ",
        "model_id": "eleven_v3",
        "stability": 0.35,
        "text": "[serious] Chuy, escucha bien. Hackers usan inteligencia artificial para hacer Vibe Hacking. [excited] ¡Pero Gemini cuatro Neon te protege!",
    },
    {
        "id": "06_agy_charlie_v3_hyped",
        "title": "06 · Agy (Charlie) — v3 Rápido & Energético",
        "role": "AGY",
        "voice_id": "IKne3meq5aSn9XLyUdCD",
        "model_id": "eleven_v3",
        "stability": 0.28,
        "text": "[excited] ¡Exacto! Esos links traen Infostealers... ¡Activa dos FA ya mismo y comenta Neon para la guía!",
    },
    {
        "id": "07_agy_brian_v3_profundo",
        "title": "07 · Agy (Brian) — v3 Profundo Cinematográfico",
        "role": "AGY",
        "voice_id": "nPczCjzI2devNBz1zQrb",
        "model_id": "eleven_v3",
        "stability": 0.40,
        "text": "[sighs] Tranquilo, Chuy. Con Antigravity y Gemini cuatro Neon, tus contraseñas quedan blindadas en segundos.",
    },
    {
        "id": "08_liza_v3_mexicana",
        "title": "08 · Liza (Mexicana Natural) — v3 Social Media",
        "role": "ALTERNATIVA",
        "voice_id": "kl7d390GatBPfqhRTyAl",
        "model_id": "eleven_v3",
        "stability": 0.30,
        "text": "[gasps] ¡Oye, aguas! ¿Ya viste lo que está pasando con las cuentas bloqueadas? [excited] ¡Te enseño cómo recuperarla!",
    },
]


def tts_generate(sample: dict, out_path: Path, api_key: str) -> str:
    models_to_try = [sample["model_id"], "eleven_multilingual_v2"]
    for mid in models_to_try:
        # Clean v3 tags if falling back to v2
        txt = sample["text"]
        if mid != "eleven_v3":
            import re
            txt = re.sub(r"\[[^\]]+\]\s*", "", txt)
        payload = json.dumps({
            "text": txt,
            "model_id": mid,
            "voice_settings": {
                "stability": sample["stability"],
                "similarity_boost": 0.78,
                "style": 0.45 if mid != "eleven_v3" else 0.0,
                "use_speaker_boost": True,
            },
        }).encode("utf-8")
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{sample['voice_id']}",
            data=payload,
            headers={
                "xi-api-key": api_key,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                out_path.write_bytes(r.read())
                return mid
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="ignore")
            print(f"  Model {mid} error {e.code}: {body[:160]}")
            continue
    raise RuntimeError(f"Failed all models for {sample['id']}")


def main():
    api_key = load_api_key()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cards = []
    for s in SAMPLES:
        mp3 = OUT_DIR / f"{s['id']}.mp3"
        used_model = s["model_id"]
        if not mp3.exists():
            print(f"Generando {s['id']}...")
            used_model = tts_generate(s, mp3, api_key)
        cards.append({**s, "file": mp3.name, "used_model": used_model})

    html = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8" />
<title>Casting de Voces & Ritmos — ¡WATERS!</title>
<style>
  body { background:#070B14; color:#F8FAFC; font-family:system-ui,-apple-system,sans-serif; margin:0; padding:32px; }
  h1 { color:#DFB15B; margin-bottom:6px; }
  p.sub { color:#94A3B8; margin-top:0; margin-bottom:28px; }
  .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(340px,1fr)); gap:18px; }
  .card { background:#0F172A; border:1px solid #1E293B; border-radius:16px; padding:18px; }
  .badge { display:inline-block; font-size:11px; font-weight:800; padding:4px 10px; border-radius:999px; background:#1E293B; color:#38BDF8; margin-bottom:8px; }
  .badge.chuy { color:#DFB15B; }
  .title { font-weight:800; font-size:16px; margin-bottom:8px; }
  .txt { font-size:13px; color:#CBD5E1; line-height:1.45; margin-bottom:12px; background:#060913; padding:10px; border-radius:10px; }
  audio { width:100%; }
</style>
</head>
<body>
  <h1>🎙️ Casting de Voces & Ritmos (8 Variaciones)</h1>
  <p class="sub">Escucha las 8 pruebas con respiraciones, suspiros y ritmo dinámico. Dime qué número quieres para <b>Chuy</b> y qué número para <b>Agy</b>.</p>
  <div class="grid">
"""
    for c in cards:
        cls = "chuy" if c["role"] == "CHUY" else ""
        html += f"""    <div class="card">
      <span class="badge {cls}">{c['role']} · {c['used_model']}</span>
      <div class="title">{c['title']}</div>
      <div class="txt">{c['text']}</div>
      <audio controls src="{c['file']}"></audio>
    </div>\n"""
    html += "  </div>\n</body>\n</html>\n"
    html_path = OUT_DIR / "casting_voces.html"
    html_path.write_text(html, encoding="utf-8")
    print(f"✅ Casting listo: {html_path}")


if __name__ == "__main__":
    main()
