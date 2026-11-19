#!/usr/bin/env python3
"""
CAPTOORA STUDIO — OPUS CLIP 4.0 PRO PIPELINE & WATCHER
Dirección Ejecutiva: Agente Eddy💫 (Director de Operaciones & Estrategia Viral)

Monitorea drops de video BTS, ensambla masters de formato largo (>10-30 min)
y genera la especificación de ganchos virales, subtítulos y reframing 9:16
para exprimir al 100% la membresía Pro de Opus Clip 4.0 (opus.pro).
"""

import os
import sys
import time
import glob
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# CONFIGURACIÓN DE RUTAS MAESTRAS
HOME = os.path.expanduser("~")
DESKTOP = os.path.join(HOME, "Desktop")
CAPTOORA_DIR = os.path.join(HOME, "captoora")
EXTERNAL_DATA = "/Volumes/Macintosh HD - Data/VIDEOS_BTS_CAMARITA"

INPUT_DIRS = [
    os.path.join(DESKTOP, "CAPTOORA_DAILY_VIDEOS", "03_OPUS_CLIP_MASTER_INPUT"),
    EXTERNAL_DATA,
    os.path.join(DESKTOP, "BTS"),
    os.path.join(DESKTOP, "Capturas_y_Grabaciones_Pantalla")
]

OUTPUT_DIR = os.path.join(DESKTOP, "CAPTOORA_DAILY_VIDEOS", "04_OPUS_CLIP_PRO_EXPORTADOS")
MANIFEST_PATH = os.path.join(CAPTOORA_DIR, "OPUS_CLIP_4_PRO_MANIFEST.json")
DASHBOARD_PATH = os.path.join(CAPTOORA_DIR, "OPUS_CLIP_DASHBOARD.html")
STATUS_PATH = os.path.join(CAPTOORA_DIR, "logs", "opus_clip_status.json")
GUIDE_PATH = os.path.join(CAPTOORA_DIR, "docs", "OPUS_CLIP_4_PRO_ESTRATEGIA_EDDY.md")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(CAPTOORA_DIR, "logs"), exist_ok=True)
os.makedirs(os.path.join(CAPTOORA_DIR, "docs"), exist_ok=True)

# AGENTE EDDY💫 — HOOKS Y PROMPTS VIRALES PRECONFIGURADOS
EDDY_VIRAL_HOOKS = [
    {
        "id": "HOOK_01_CEO_BEAUTY",
        "tema": "Cómo posar como CEO de Belleza",
        "gancho": "Cómo posar como Directora Ejecutiva en 3 segundos sin verte tiesa 📸💄",
        "cta": "Comenta FOTO si quieres la guía de poses comerciales de Captoora.",
        "keywords": ["Farmasi", "Beauty CEO", "Poses de Estudio", "Monterrey"]
    },
    {
        "id": "HOOK_02_BTS_CAOS_ORDENADO",
        "tema": "Detrás de Cámaras Real",
        "gancho": "¿Qué pasa realmente cuando juntas a 25 líderes en un ciclorama? 🥂✨",
        "cta": "Síguenos para ver la sesión completa con mimosas y alta costura.",
        "keywords": ["BTS", "Captoora Studio", "Fotografía Comercial", "Vibra"]
    },
    {
        "id": "HOOK_03_ZERO_CROP_SECRETO",
        "tema": "Técnica de Fotografía Zero Crop",
        "gancho": "La razón exacta por la que jamás recortamos una foto en Captoora Studio 📐🎞️",
        "cta": "Guarda este video si eres creador de contenido o fotógrafo.",
        "keywords": ["Zero Crop", "Full Frame", "Dirección de Arte", "Iluminación"]
    },
    {
        "id": "HOOK_04_TESTIMONIOS_PING_PONG",
        "tema": "Testimonios Dinámicos de Marca",
        "gancho": "Le preguntamos a 5 directoras qué sintieron al verse en ciclorama puro... 😲✨",
        "cta": "Visita nuestro perfil para agendar tu fecha comercial.",
        "keywords": ["Testimonios", "Transformación", "Autoestima", "Marca Personal"]
    }
]

def get_video_telemetry(file_path):
    """Extrae duración, resolución, códec y bitrate usando ffprobe."""
    try:
        cmd = [
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_format", "-show_streams", file_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            return None
        data = json.loads(res.stdout)
        fmt = data.get("format", {})
        duration_sec = float(fmt.get("duration", 0))
        size_mb = float(fmt.get("size", 0)) / (1024 * 1024)
        
        # Streams de video
        v_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
        width = v_stream.get("width", 0)
        height = v_stream.get("height", 0)
        codec = v_stream.get("codec_name", "unknown")

        return {
            "path": file_path,
            "filename": os.path.basename(file_path),
            "duration_sec": round(duration_sec, 2),
            "duration_human": f"{int(duration_sec // 60)}m {int(duration_sec % 60)}s",
            "size_mb": round(size_mb, 2),
            "resolution": f"{width}x{height}",
            "codec": codec,
            "estimated_opus_shorts": max(3, int(duration_sec // 60) * 1) # ~1 viral short per minute
        }
    except Exception as e:
        print(f"[Error ffprobe] {e}")
        return None

def scan_master_videos():
    """Escanea las carpetas monitoreadas buscando videos MP4/MOV."""
    found = []
    seen_paths = set()
    for d in INPUT_DIRS:
        if not os.path.exists(d):
            continue
        for ext in ("*.mp4", "*.MP4", "*.mov", "*.MOV"):
            for f in glob.glob(os.path.join(d, ext)):
                real_p = os.path.realpath(f)
                if real_p in seen_paths:
                    continue
                seen_paths.add(real_p)
                t = get_video_telemetry(real_p)
                if t and t["duration_sec"] > 15: # Ignorar clips miniatura < 15s
                    found.append(t)
    return found

def generate_manifest(master_videos):
    """Crea el manifiesto JSON para Opus Clip 4.0 Pro."""
    manifest = {
        "sistema": "Captoora Studio — Opus Clip 4.0 Pro Pipeline",
        "director_ejecutivo": "Agente Eddy💫 (Director de Operaciones)",
        "fecha_actualizacion": datetime.now().isoformat(),
        "suscripcion": {
            "tipo": "Opus Clip Pro (Membresía Activa 1 Mes)",
            "version_engine": "Opus Clip 4.0 (Latest Release)",
            "plataforma": "https://www.opus.pro",
            "objetivo": "Maximizar créditos generando lotes de 15 a 30 videos verticales por master"
        },
        "configuracion_render_opus_4": {
            "aspect_ratio": "9:16 (Vertical Fullscreen)",
            "auto_reframe": "Smart Speaker + Face Focus (Centrado en Poncho y Modelos)",
            "subtitulos": {
                "estilo": "Viral Modern Karaoke (Hormozi Style)",
                "color_base": "#FFFFFF",
                "color_resaltado": "#DFB15B (Gold Captoora)",
                "emojis_automaticos": True,
                "posicion": "Centro-inferior (Safe Zone TikTok/Reels)"
            },
            "duracion_clips_preferida": "30s a 60s (Alta Retención)",
            "umbral_virality_score": 75,
            "eliminacion_silencios": True
        },
        "videos_maestros_disponibles": master_videos,
        "ganchos_y_prompts_eddy": EDDY_VIRAL_HOOKS
    }

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    return manifest

def generate_dashboard(manifest):
    """Genera un dashboard HTML ejecutivo para que Poncho visualice el pipeline."""
    v_rows = ""
    for v in manifest["videos_maestros_disponibles"]:
        v_rows += f"""
        <tr>
          <td><strong>{v['filename']}</strong><br><small style="color:#8e95a5;">{v['path']}</small></td>
          <td><span class="badge duration">{v['duration_human']}</span></td>
          <td>{v['resolution']} ({v['codec']})</td>
          <td>{v['size_mb']} MB</td>
          <td><span class="badge clips">~{v['estimated_opus_shorts']} Clips Virales</span></td>
          <td>
            <a href="file://{v['path']}" class="btn-action">Ver Archivo</a>
          </td>
        </tr>
        """

    hooks_cards = ""
    for h in manifest["ganchos_y_prompts_eddy"]:
        hooks_cards += f"""
        <div class="hook-card">
          <div class="hook-badge">{h['id']} · {h['tema']}</div>
          <h4>"{h['gancho']}"</h4>
          <p class="hook-cta"><strong>CTA:</strong> {h['cta']}</p>
          <div class="hook-tags">{' '.join([f'<span>#{kw}</span>' for kw in h['keywords']])}</div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>CAPTOORA STUDIO — Panel de Control Opus Clip 4.0 Pro</title>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;800&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #090a0f;
      --card-bg: rgba(255, 255, 255, 0.04);
      --border: rgba(255, 255, 255, 0.08);
      --gold: #dfb15b;
      --gold-glow: rgba(223, 177, 91, 0.25);
      --text: #f0f2f8;
      --text-muted: #8e95a5;
      --success: #10b981;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', sans-serif;
      padding: 40px 24px;
      line-height: 1.5;
    }}
    .container {{ max-width: 1200px; margin: 0 auto; }}
    header {{
      margin-bottom: 30px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}
    h1 {{
      font-family: 'Cinzel', serif;
      font-size: 28px;
      color: #fff;
    }}
    h1 span {{ color: var(--gold); }}
    .badge-sub {{
      background: rgba(223, 177, 91, 0.15);
      border: 1px solid var(--gold);
      color: var(--gold);
      padding: 6px 16px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
    }}
    .grid-summary {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 20px;
      margin-bottom: 30px;
    }}
    .stat-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 22px;
    }}
    .stat-card h3 {{
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: var(--text-muted);
      margin-bottom: 8px;
    }}
    .stat-card .val {{
      font-size: 26px;
      font-weight: 800;
      color: var(--gold);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--card-bg);
      border-radius: 16px;
      overflow: hidden;
      margin-bottom: 40px;
      border: 1px solid var(--border);
    }}
    th, td {{
      padding: 16px 20px;
      text-align: left;
      font-size: 13px;
      border-bottom: 1px solid var(--border);
    }}
    th {{
      background: rgba(255, 255, 255, 0.02);
      color: var(--gold);
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 1.5px;
    }}
    .badge {{
      display: inline-block;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
    }}
    .badge.duration {{ background: rgba(255,255,255,0.08); color: #fff; }}
    .badge.clips {{ background: rgba(16, 185, 129, 0.15); color: var(--success); border: 1px solid var(--success); }}
    .btn-action {{
      background: var(--gold);
      color: #000;
      text-decoration: none;
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
    }}
    .hooks-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 20px;
    }}
    .hook-card {{
      background: rgba(223, 177, 91, 0.04);
      border: 1px solid rgba(223, 177, 91, 0.2);
      border-radius: 16px;
      padding: 22px;
    }}
    .hook-badge {{
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 1.5px;
      color: var(--gold);
      text-transform: uppercase;
      margin-bottom: 8px;
    }}
    .hook-card h4 {{
      font-size: 15px;
      color: #fff;
      margin-bottom: 10px;
    }}
    .hook-cta {{ font-size: 12px; color: var(--text-muted); margin-bottom: 12px; }}
    .hook-tags span {{
      display: inline-block;
      background: rgba(255,255,255,0.06);
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      color: var(--gold);
      margin-right: 6px;
    }}
    .opus-cta-box {{
      background: linear-gradient(135deg, rgba(99, 91, 255, 0.15) 0%, rgba(223, 177, 91, 0.15) 100%);
      border: 1px solid var(--gold);
      border-radius: 18px;
      padding: 26px;
      margin-top: 35px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
    }}
    .opus-btn {{
      background: linear-gradient(135deg, var(--gold) 0%, #b88628 100%);
      color: #000;
      font-size: 15px;
      font-weight: 800;
      padding: 14px 28px;
      border-radius: 12px;
      text-decoration: none;
      box-shadow: 0 4px 18px var(--gold-glow);
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div>
        <h1>CAPTOORA STUDIO · <span>OPUS CLIP 4.0 PRO</span></h1>
        <p style="color:var(--text-muted); font-size:14px; margin-top:4px;">
          Centro de Ingesta & Optimización Viral · Dirección Ejecutiva: Agente Eddy💫
        </p>
      </div>
      <div class="badge-sub">Membresía Pro Activa (1 Mes) · Versión 4.0</div>
    </header>

    <div class="grid-summary">
      <div class="stat-card">
        <h3>Videos Maestros Listos</h3>
        <div class="val">{len(manifest['videos_maestros_disponibles'])} Videos</div>
      </div>
      <div class="stat-card">
        <h3>Minutos de Ingesta</h3>
        <div class="val">{sum(v['duration_sec'] for v in manifest['videos_maestros_disponibles']) / 60:.1f} Minutos</div>
      </div>
      <div class="stat-card">
        <h3>Potencial de Clips Virales</h3>
        <div class="val">~{sum(v['estimated_opus_shorts'] for v in manifest['videos_maestros_disponibles'])} Shorts / Reels</div>
      </div>
      <div class="stat-card">
        <h3>Formato de Salida</h3>
        <div class="val" style="font-size:18px;">9:16 Vertical + Karaoke</div>
      </div>
    </div>

    <h2 style="font-family:'Cinzel',serif; font-size:18px; margin-bottom:16px; color:#fff;">
      📁 Inventario de Videos Maestros para Opus Clip
    </h2>
    <table>
      <thead>
        <tr>
          <th>Archivo Maestro</th>
          <th>Duración</th>
          <th>Resolución</th>
          <th>Tamaño</th>
          <th>Rendimiento Estimado</th>
          <th>Acción</th>
        </tr>
      </thead>
      <tbody>
        {v_rows}
      </tbody>
    </table>

    <h2 style="font-family:'Cinzel',serif; font-size:18px; margin-bottom:16px; color:#fff;">
      🎯 Ganchos Virales Diseñados por Agente Eddy💫
    </h2>
    <div class="hooks-grid">
      {hooks_cards}
    </div>

    <div class="opus-cta-box">
      <div>
        <h3 style="font-size:18px; color:#fff; margin-bottom:4px;">🚀 Listo para Subir a Opus Clip 4.0 Pro</h3>
        <p style="font-size:13px; color:var(--text-muted);">
          Sube el archivo maestro <strong>CAPTOORA_FARMASI_31_OCT_BTS_MASTER_LONG.mp4</strong> a tu cuenta de opus.pro con un solo clic.
        </p>
      </div>
      <a href="https://www.opus.pro" target="_blank" class="opus-btn">
        Abrir Opus Clip Pro (opus.pro) ➔
      </a>
    </div>
  </div>
</body>
</html>
"""
    with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
        f.write(html)

def generate_markdown_guide(manifest):
    """Genera la guía ejecutiva en Markdown para Poncho."""
    content = f"""# GUÍA EJECUTIVA: ESTRATEGIA OPUS CLIP 4.0 PRO
**Captoora Studio · Operación Monterrey 2026**  
**Dirección:** Agente Eddy💫 (Director de Operaciones & Estrategia Viral)  
**Fecha:** {datetime.now().strftime("%Y-%m-%d %H:%M")}  
**Suscripción:** Opus Clip Pro (1 Mes de Acceso Total — Versión 4.0)

---

## 1. El Objetivo de Eddy💫
Aprovechar al 100% el mes de suscripción Pro de **Opus Clip 4.0** transformando el material detrás de cámaras (BTS) y los testimonios de la sesión Farmasi del 31 de octubre en una **fábrica ininterrumpida de contenido vertical (TikTok, Instagram Reels, YouTube Shorts)**.

---

## 2. Archivo Maestro Listo para Carga
Ya consolidamos y verificamos el video maestro de alta duración:
- **Archivo:** `CAPTOORA_FARMASI_31_OCT_BTS_MASTER_LONG.mp4`
- **Ubicación en Mac:** `/Volumes/Macintosh HD - Data/VIDEOS_BTS_CAMARITA/CAPTOORA_FARMASI_31_OCT_BTS_MASTER_LONG.mp4`
- **Acceso Directo en Escritorio:** `/Users/imac/Desktop/CAPTOORA_DAILY_VIDEOS/03_OPUS_CLIP_MASTER_INPUT/CAPTOORA_FARMASI_31_OCT_BTS_MASTER_LONG.mp4`
- **Duración:** 20 minutos con 43 segundos (15 tomas continuas de ciclorama, iluminación y dirección).
- **Rendimiento Estimado en Opus Clip:** **18 a 25 clips virales individuales**.

---

## 3. Configuración Óptima en Opus Clip 4.0 Pro
Al subir el archivo a [opus.pro](https://www.opus.pro), selecciona los siguientes parámetros recomendados por Eddy💫:

| Parámetro | Configuración Recomendada | Razón Estratégica |
|---|---|---|
| **Aspect Ratio** | `9:16 (Vertical)` | Ocupa toda la pantalla del teléfono en TikTok y Reels. |
| **Auto Reframe** | `Smart Multi-Face Tracker` | Mantiene a Poncho dirigiendo o a la modelo centrada. |
| **Subtitles Template** | `Modern Karaoke / Hormozi` | Fuente bold con salto dinámico y palabras resaltadas. |
| **Color Primario** | `#FFFFFF` (Blanco Puro) | Máxima legibilidad sobre fondos oscuros o ciclorama. |
| **Color Resaltado** | `#DFB15B` (Oro Captoora) | Refuerza la identidad visual premium del estudio. |
| **Auto Emojis** | `Activado (High Frequency)` | Eleva la retención de audiencia en los primeros 3 segundos. |
| **Target Length** | `30s a 60s` | Mejor tasa de finalización y compartidos en Instagram. |
| **Silence Removal** | `Activo (Auto-Trim)` | Elimina pausas muertas entre instrucciones de pose. |

---

## 4. Los 4 Ganchos de Oro de Eddy💫 para Copys y Títulos
1. **El Secreto Beauty CEO:**  
   *"Cómo posar como Directora Ejecutiva en 3 segundos sin verte tiesa 📸💄"*
2. **El Detrás de Cámaras:**  
   *"¿Qué pasa realmente cuando juntas a 25 líderes en un ciclorama? 🥂✨"*
3. **La Filosofía Zero Crop:**  
   *"La razón exacta por la que jamás recortamos una foto en Captoora Studio 📐🎞️"*
4. **Prueba Social en Ping-Pong:**  
   *"Le preguntamos a 5 directoras qué sintieron al verse en ciclorama puro... 😲✨"*

---

## 5. Dashboard y Manifiesto en Tiempo Real
- **Dashboard Visual:** [OPUS_CLIP_DASHBOARD.html](file://{DASHBOARD_PATH})
- **Manifiesto Técnico:** [OPUS_CLIP_4_PRO_MANIFEST.json](file://{MANIFEST_PATH})
- **Watcher Automático:** Ejecutable mediante `python3 scripts/opus_clip_pipeline_watcher.py --watch`
"""
    with open(GUIDE_PATH, "w", encoding="utf-8") as f:
        f.write(content)

def run_once():
    """Ejecuta una ronda completa de escaneo y generación."""
    print("=" * 70)
    print("🎬 [Agente Eddy💫] Escaneando material para Opus Clip 4.0 Pro...")
    videos = scan_master_videos()
    print(f"✅ Se encontraron {len(videos)} videos maestros candidatos.")
    for v in videos:
        print(f"   • {v['filename']} ({v['duration_human']} | {v['size_mb']} MB | ~{v['estimated_opus_shorts']} clips)")
    
    manifest = generate_manifest(videos)
    generate_dashboard(manifest)
    generate_markdown_guide(manifest)
    print(f"📄 Manifiesto actualizado: {MANIFEST_PATH}")
    print(f"📊 Dashboard interactivo generado: {DASHBOARD_PATH}")
    print(f"📖 Guía de Eddy lista: {GUIDE_PATH}")
    print("=" * 70)

def watch_loop():
    """Bucle continuo para modo daemon."""
    print("👀 [Agente Eddy💫] Modo Watcher activo. Monitoreando drops de video cada 30 segundos...")
    last_count = -1
    while True:
        try:
            videos = scan_master_videos()
            if len(videos) != last_count:
                last_count = len(videos)
                manifest = generate_manifest(videos)
                generate_dashboard(manifest)
                generate_markdown_guide(manifest)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔄 Cambio detectado: {last_count} videos maestros registrados.")
            time.sleep(30)
        except KeyboardInterrupt:
            print("\n🛑 Watcher detenido por el usuario.")
            break
        except Exception as e:
            print(f"[Watcher Error] {e}")
            time.sleep(30)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        watch_loop()
    else:
        run_once()
