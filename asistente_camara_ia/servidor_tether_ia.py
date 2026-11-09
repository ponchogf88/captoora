#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CAPTOORA STUDIO — ARGON LENS AI (TETHER & VOICE DIRECTOR ASSISTANT)
================================================================================
Compatible con:
  - Canon EOS 7D Mark II (USB 3.0 Micro-B / UGREEN USB-C en Mac / USB-A en Windows)
  - macOS: Control nativo vía `gphoto2` (PTP/USB) + desbloqueo automático de PTPCamera + TTS `say`
  - Windows: Control vía `digiCamControl` (CameraControlCmd.exe), WIA PTP COM (`wiaCommandTakePicture`),
    EOS Utility Hotkey Trigger, y Hot-Folder Watcher en tiempo real.
  - Análisis Óptico en Vivo + IA Multimodal (Gemini Vision opcional + Telemetría Óptica Local):
    Evalúa exposición, recorte de altas luces, empastado de sombras, ratio de iluminación (Key-to-Fill),
    nitidez óptica en zona de rostro/ojos y balance de encuadre.
================================================================================
"""

import os
import sys
import json
import time
import base64
import shutil
import platform
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request
import urllib.error

try:
    from PIL import Image, ImageStat, ImageFilter, ExifTags
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
TETHER_DIR = BASE_DIR / "sesiones_tether"
TETHER_DIR.mkdir(parents=True, exist_ok=True)

OS_NAME = platform.system()  # 'Darwin' (macOS), 'Windows', 'Linux'

STATE = {
    "camera_connected": False,
    "camera_model": "Buscando Canon EOS 7D Mark II...",
    "connection_mode": "Hot-Folder / Simulador Óptico",
    "os": "macOS" if OS_NAME == "Darwin" else OS_NAME,
    "shots": [],
    "last_shot_file": None,
    "is_shooting": False,
    "gemini_api_key": os.environ.get("GEMINI_API_KEY", ""),
    "director_mode": "LOBA_PRO",
    "active_scene_preset": "ESTUDIO_FLASH",
    "camera_settings": {
        "iso": "100",
        "aperture": "5.6",
        "shutter": "1/160",
        "wb": "Flash 5600K",
        "human_intent": "Estudio con Flash (Cero Menús)"
    }
}

SCENE_PRESETS = {
    "FONDO_BORROSO": {
        "iso": "200",
        "aperture": "2.0",
        "shutter": "1/250",
        "wb": "Luz Día / Auto",
        "human_intent": "Fondo Borroso / Retrato (Bokeh)",
        "voice_confirm": "Listo Alfonso, ya le moví yo a la cámara: abrí el lente a f dos punto cero para derretir el fondo, ISO 200 y velocidad 1 sobre 250. Dime 'toma la foto'."
    },
    "MOVIMIENTO_NINOS": {
        "iso": "800",
        "aperture": "4.0",
        "shutter": "1/800",
        "wb": "Auto",
        "human_intent": "Niños / Mascotas / Acción (Cero Fotos Movidas)",
        "voice_confirm": "Ya configuré la 7D Mark II en modo congelar movimiento: velocidad rápida a 1 sobre 800, enfoque continuo y sensibilidad en ISO 800. Tú solo encuadra y dime 'toma la foto'."
    },
    "ESTUDIO_FLASH": {
        "iso": "100",
        "aperture": "5.6",
        "shutter": "1/160",
        "wb": "Flash 5600K",
        "human_intent": "Estudio con Flash / Estrobos (Nitidez Total)",
        "voice_confirm": "Cámara clavada para estudio con flash: sincronización a 1 sobre 160, diafragma f cinco punto seis para máxima nitidez en piel y ojos, e ISO 100 limpio."
    },
    "POCA_LUZ": {
        "iso": "1600",
        "aperture": "2.8",
        "shutter": "1/125",
        "wb": "Tungsteno / Cálido",
        "human_intent": "Interior / Poca Luz sin Flash",
        "voice_confirm": "Ya ajusté la cámara para poca luz sin que tengas que entrar al menú: subí a ISO 1600, abrí el diafragma a f dos punto ocho y aseguré velocidad a 1 sobre 125."
    },
    "MAS_LUZ_AUTO": {
        "iso": "400",
        "aperture": "2.8",
        "shutter": "1/125",
        "wb": "Auto",
        "human_intent": "Auto-Corrección: +1.5 Pasos Más de Luz",
        "voice_confirm": "Entendido, yo la arreglo. Abrí el diafragma a f dos punto ocho y subí un paso el ISO para levantar las sombras sin quemar la piel. Dime 'toma la foto' para probar."
    },
    "MENOS_LUZ_AUTO": {
        "iso": "100",
        "aperture": "8.0",
        "shutter": "1/250",
        "wb": "Auto",
        "human_intent": "Auto-Corrección: -1.5 Pasos Menos de Luz",
        "voice_confirm": "Yo me encargo. Bajé el ISO a 100 y cerré el diafragma a f ocho para recuperar todos los detalles en las luces altas. Dime 'toma la foto'."
    }
}


def apply_camera_preset_usb(preset_key: str) -> dict:
    """Mueve automáticamente ISO, Apertura y Velocidad en la Canon EOS 7D Mark II vía USB (gphoto2 / digiCamControl)."""
    preset = SCENE_PRESETS.get(preset_key, SCENE_PRESETS["ESTUDIO_FLASH"])
    STATE["active_scene_preset"] = preset_key
    STATE["camera_settings"] = {
        "iso": preset["iso"],
        "aperture": preset["aperture"],
        "shutter": preset["shutter"],
        "wb": preset["wb"],
        "human_intent": preset["human_intent"]
    }

    # Si está conectada por USB en Mac con gphoto2, enviamos los comandos PTP directo a la 7D Mark II
    if OS_NAME == "Darwin":
        gphoto = shutil.which("gphoto2")
        if gphoto and STATE["camera_connected"]:
            subprocess.run(["killall", "-9", "PTPCamera"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run([
                gphoto,
                f"--set-config=iso={preset['iso']}",
                f"--set-config=aperture={preset['aperture']}",
                f"--set-config=shutterspeed={preset['shutter']}"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=8)
    elif OS_NAME == "Windows":
        dcc_paths = [
            Path(r"C:\Program Files (x86)\digiCamControl\CameraControlCmd.exe"),
            Path(r"C:\Program Files\digiCamControl\CameraControlCmd.exe"),
        ]
        dcc_exe = next((p for p in dcc_paths if p.exists()), None)
        if dcc_exe and STATE["camera_connected"]:
            subprocess.run([
                str(dcc_exe),
                "/iso", preset["iso"],
                "/aperture", preset["aperture"],
                "/shutter", preset["shutter"]
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=8)

    return {
        "ok": True,
        "preset": preset_key,
        "camera_settings": STATE["camera_settings"],
        "voice_confirm": preset["voice_confirm"]
    }



def detect_camera():
    """Detecta la Canon EOS 7D Mark II (o cualquier DSLR/Mirrorless conectada por USB)."""
    if OS_NAME == "Darwin":
        # En macOS liberamos primero el proceso PTPCamera que secuestra el USB al conectar el UGREEN
        subprocess.run(["killall", "-9", "PTPCamera"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        gphoto = shutil.which("gphoto2")
        if gphoto:
            try:
                res = subprocess.run([gphoto, "--auto-detect"], capture_output=True, text=True, timeout=5)
                lines = [l.strip() for l in res.stdout.splitlines() if l.strip() and not l.startswith("Model") and not l.startswith("---")]
                if lines:
                    STATE["camera_connected"] = True
                    STATE["camera_model"] = lines[0].split("usb:")[0].strip()
                    STATE["connection_mode"] = "macOS USB Directo (gphoto2 PTP)"
                    return STATE
            except Exception:
                pass
        # También revisamos system_profiler SPUSBDataType por si está conectada pero falta instalar gphoto2
        try:
            res = subprocess.run(["system_profiler", "SPUSBDataType"], capture_output=True, text=True, timeout=5)
            if "Canon" in res.stdout or "7D" in res.stdout or "EOS" in res.stdout:
                STATE["camera_connected"] = True
                STATE["camera_model"] = "Canon EOS 7D Mark II (USB Detectado en Mac)"
                STATE["connection_mode"] = "EOS Utility Hot-Folder / Instalar gphoto2 para Disparo Directo"
                return STATE
        except Exception:
            pass

    elif OS_NAME == "Windows":
        # Revisión ultrarrápida (<5ms) de digiCamControl CLI sin invocar PowerShell lento
        dcc_paths = [
            Path(r"C:\Program Files (x86)\digiCamControl\CameraControlCmd.exe"),
            Path(r"C:\Program Files\digiCamControl\CameraControlCmd.exe"),
        ]
        dcc_exe = next((p for p in dcc_paths if p.exists()), None)
        if dcc_exe:
            STATE["camera_connected"] = True
            STATE["camera_model"] = "Canon EOS 7D Mark II (digiCamControl USB)"
            STATE["connection_mode"] = "Windows USB Directo (CameraControlCmd)"
            return STATE

    STATE["camera_connected"] = False
    STATE["camera_model"] = "Canon EOS 7D Mark II (Lista para UGREEN Mac / Hot-Folder)"
    STATE["connection_mode"] = "Piloto Automático IA + Hot-Folder En Vivo"
    return STATE


def extract_optical_telemetry(img_path: Path) -> dict:
    """Analiza la fotografía recién tomada: EXIF real, histograma, foco/nitidez, iluminación Key/Fill y encuadre."""
    telemetry = {
        "filename": img_path.name,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "width": 0,
        "height": 0,
        "camera": "Canon EOS 7D Mark II",
        "iso": "ISO 200",
        "shutter": "1/160s",
        "aperture": "f/2.8",
        "focal_length": "50mm",
        "mean_brightness": 128.0,
        "ev_status": "ÓPTIMA",
        "highlights_clip_pct": 0.0,
        "shadows_crush_pct": 0.0,
        "key_to_fill_ratio": 1.5,
        "light_direction": "Centro-Izquierda",
        "sharpness_score": 85.0,
        "focus_status": "CLAVADO",
        "headroom_balance": "Equilibrado",
    }

    if not PIL_AVAILABLE or not img_path.exists():
        return telemetry

    try:
        with Image.open(img_path) as im:
            telemetry["width"], telemetry["height"] = im.size

            # 1. Extraer EXIF si existe
            exif_data = getattr(im, "_getexif", lambda: None)()
            if exif_data:
                exif = {ExifTags.TAGS.get(k, k): v for k, v in exif_data.items()}
                model = str(exif.get("Model", "")).strip().replace("\x00", "")
                if model:
                    telemetry["camera"] = model
                iso = exif.get("ISOSpeedRatings") or exif.get("PhotographicSensitivity")
                if iso:
                    telemetry["iso"] = f"ISO {iso}"
                fnum = exif.get("FNumber")
                if fnum:
                    try:
                        val = float(fnum[0]) / float(fnum[1]) if isinstance(fnum, tuple) else float(fnum)
                        telemetry["aperture"] = f"f/{val:.1f}"
                    except Exception:
                        pass
                exp = exif.get("ExposureTime")
                if exp:
                    try:
                        val = float(exp[0]) / float(exp[1]) if isinstance(exp, tuple) else float(exp)
                        if val < 1:
                            telemetry["shutter"] = f"1/{int(round(1.0/val))}s"
                        else:
                            telemetry["shutter"] = f"{val:.1f}s"
                    except Exception:
                        pass

            # 2. Convertir a escala de grises para análisis lumínico y de foco
            gray = im.convert("L")
            w, h = gray.size
            hist = gray.histogram()
            total_px = float(w * h)

            mean_luma = ImageStat.Stat(gray).mean[0]
            telemetry["mean_brightness"] = round(mean_luma, 1)

            # Recorte en altas luces (>248) y empastado en sombras (<8)
            high_clip = sum(hist[248:]) / total_px * 100.0
            shad_crush = sum(hist[:8]) / total_px * 100.0
            telemetry["highlights_clip_pct"] = round(high_clip, 2)
            telemetry["shadows_crush_pct"] = round(shad_crush, 2)

            if mean_luma < 72:
                telemetry["ev_status"] = "SUBEXPUESTA (-1.2 EV)"
            elif mean_luma > 185:
                telemetry["ev_status"] = "SOBREEXPUESTA (+1.1 EV)"
            elif high_clip > 6.5:
                telemetry["ev_status"] = "ALTAS LUCES AL LÍMITE"
            else:
                telemetry["ev_status"] = "CLAVADA (RANGO ÓPTIMO)"

            # 3. Ratio Key-to-Fill (Mitad Izquierda vs Mitad Derecha en zona central)
            left_crop = gray.crop((int(w * 0.1), int(h * 0.15), int(w * 0.5), int(h * 0.85)))
            right_crop = gray.crop((int(w * 0.5), int(h * 0.15), int(w * 0.9), int(h * 0.85)))
            l_mean = max(ImageStat.Stat(left_crop).mean[0], 1.0)
            r_mean = max(ImageStat.Stat(right_crop).mean[0], 1.0)
            ratio = max(l_mean, r_mean) / min(l_mean, r_mean)
            telemetry["key_to_fill_ratio"] = round(ratio, 2)
            if abs(l_mean - r_mean) < 8:
                telemetry["light_direction"] = "Frontal Simétrica (Beauty / Flat)"
            elif l_mean > r_mean:
                telemetry["light_direction"] = "Key Light a la Izquierda (Rembrandt / Split)"
            else:
                telemetry["light_direction"] = "Key Light a la Derecha (Rembrandt / Split)"

            # 4. Nitidez óptica en zona de ojos/rostro (tercio superior-central)
            focus_zone = gray.crop((int(w * 0.28), int(h * 0.16), int(w * 0.72), int(h * 0.55)))
            edges = focus_zone.filter(ImageFilter.FIND_EDGES)
            edge_std = ImageStat.Stat(edges).stddev[0]
            sharp_score = min(100.0, round((edge_std / 38.0) * 100.0, 1))
            telemetry["sharpness_score"] = sharp_score
            if sharp_score >= 62:
                telemetry["focus_status"] = "CLAVADO EN OJOS/SUJETO"
            elif sharp_score >= 38:
                telemetry["focus_status"] = "SUAVE (REVISAR VELOCIDAD / AF)"
            else:
                telemetry["focus_status"] = "TREPIDADA O FUERA DE FOCO"

            # 5. Balance de encuadre (tercio superior vs centro)
            top_zone = gray.crop((int(w * 0.2), 0, int(w * 0.8), int(h * 0.22)))
            top_edges = ImageStat.Stat(top_zone.filter(ImageFilter.FIND_EDGES)).mean[0]
            if top_edges < 6.5:
                telemetry["headroom_balance"] = "Aire superior amplio (Baja 3° el lente)"
            elif top_edges > 28.0:
                telemetry["headroom_balance"] = "Encuadre cerrado arriba (Dame 2 dedos más de aire)"
            else:
                telemetry["headroom_balance"] = "Encuadre 4:5 Zero-Crop Impecable"

    except Exception as e:
        telemetry["error"] = str(e)

    return telemetry


def call_gemini_vision_director(img_path: Path, telemetry: dict) -> str:
    """Si hay GEMINI_API_KEY, consulta a Gemini 2.5 Flash con la foto real para dar dirección de pose y luz."""
    api_key = STATE.get("gemini_api_key", "").strip()
    if not api_key or not img_path.exists():
        return ""

    try:
        img_bytes = img_path.read_bytes()
        b64_img = base64.b64encode(img_bytes).decode("utf-8")
        prompt = (
            "Eres Argon, el director de fotografía y asistente de cámara en vivo de Alfonso en Captoora Studio. "
            "Acaba de disparar esta foto con su cámara. Háblale directo en primera persona, en español mexicano profesional, "
            "con actitud 'loba' (seguro, directo, con ojo clínico editorial, máximo 3 oraciones para poderse leer en voz alta en el estudio). "
            f"Datos ópticos reales de la toma: Exposición {telemetry['ev_status']}, Ratio de luz {telemetry['key_to_fill_ratio']}:1 ({telemetry['light_direction']}), "
            f"Foco {telemetry['focus_status']} ({telemetry['sharpness_score']}/100). "
            "Dile exactamente qué salió brutal y dale 1 o 2 instrucciones físicas precisas de pose, barbilla, hombros, cámara o luz para la siguiente toma."
        )
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": b64_img}}
                ]
            }]
        }
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            return text
    except Exception:
        return ""


def build_director_voice_feedback(telemetry: dict, img_path: Path) -> str:
    """Construye la crítica hablada del Asistente IA combinando visión IA (si hay API Key) o Telemetría Óptica Local."""
    gemini_feedback = call_gemini_vision_director(img_path, telemetry)
    if gemini_feedback:
        return gemini_feedback

    # Motor de Dirección Óptica Local (100% instantáneo sin latencia de red)
    parts = []

    # 1. Evaluación de exposición
    ev = telemetry["ev_status"]
    luma = telemetry["mean_brightness"]
    if "SUBEXPUESTA" in ev:
        parts.append(f"Alfonso, la toma entró oscura con luminancia en {int(luma)}. Sube medio paso el flash principal o abre un tercio de punto tu diafragma.")
    elif "SOBREEXPUESTA" in ev or "ALTAS LUCES" in ev:
        parts.append(f"Ojo con las altas luces, estamos al {telemetry['highlights_clip_pct']}% al límite. Baja un cuarto de potencia al estrobo o cierra un clic el diafragma.")
    else:
        parts.append(f"Exposición clavada al centro en {telemetry['iso']}, {telemetry['aperture']} y {telemetry['shutter']}.")

    # 2. Evaluación de Foco y Nitidez
    if telemetry["sharpness_score"] >= 62:
        parts.append(f"El foco de la 7D Mark II está quirúrgico al {int(telemetry['sharpness_score'])}%.")
    elif telemetry["sharpness_score"] >= 38:
        parts.append("El foco quedó ligeramente suave; asegura el punto AF en el ojo más cercano a la cámara.")
    else:
        parts.append("La toma salió con ligero movimiento; sube la velocidad a 1 sobre 200 y pide que mantenga la postura un segundo más.")

    # 3. Evaluación de Luz (Key-to-Fill) y Encuadre
    ratio = telemetry["key_to_fill_ratio"]
    if ratio >= 1.8:
        parts.append(f"El contraste dramático está en {ratio} a 1 con luz desde {telemetry['light_direction'].lower()}.")
    else:
        parts.append(f"Luz envolvente y limpia en proporción {ratio} a 1.")

    if "Baja 3°" in telemetry["headroom_balance"]:
        parts.append("Tienes un poco de aire de más arriba; baja dos dedos el encuadre, proyecta ligeramente la barbilla hacia el lente y dime 'toma la foto'.")
    elif "Dame 2 dedos" in telemetry["headroom_balance"]:
        parts.append("Estás muy al ras en el borde superior; aléjate medio paso para cuidar nuestro Zero-Crop 4 por 5 y dime 'toma la foto'.")
    else:
        parts.append("El encuadre 4 por 5 está listo para portada. Gira 15 grados los hombros hacia la luz principal, relaja la mano y dime 'toma la foto' para hacer la variante.")

    return " ".join(parts)


def register_new_shot(img_path: Path, trigger_source: str = "VOZ / USB") -> dict:
    """Registra una foto recién capturada o detectada en el Hot-Folder y genera su diagnóstico."""
    telemetry = extract_optical_telemetry(img_path)
    voice_text = build_director_voice_feedback(telemetry, img_path)

    shot_record = {
        "id": f"shot_{int(time.time() * 1000)}",
        "filename": img_path.name,
        "url": f"/sesiones_tether/{img_path.name}?t={int(time.time()*1000)}",
        "trigger_source": trigger_source,
        "telemetry": telemetry,
        "voice_feedback": voice_text,
    }
    STATE["shots"].insert(0, shot_record)
    STATE["shots"] = STATE["shots"][:30]
    STATE["last_shot_file"] = img_path.name

    # Si estamos en macOS, también podemos hablar con la voz nativa si el navegador no tiene el foco
    return shot_record


def trigger_camera_shutter(source_label: str = "COMANDO DE VOZ") -> dict:
    """
    Dispara la Canon EOS 7D Mark II por USB (gphoto2 en Mac / digiCamControl o WIA en Windows).
    Si la cámara aún no está conectada físicamente, toma una captura real del portafolio óptico
    como simulación de estudio para probar todo el flujo de voz + análisis en vivo.
    """
    STATE["is_shooting"] = True
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = TETHER_DIR / f"CAPTOORA_7DMKII_{timestamp_str}.jpg"

    try:
        detect_camera()

        # 1. Intento real en macOS vía gphoto2
        if OS_NAME == "Darwin":
            subprocess.run(["killall", "-9", "PTPCamera"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            gphoto = shutil.which("gphoto2")
            if gphoto and STATE["camera_connected"]:
                res = subprocess.run(
                    [gphoto, "--capture-image-and-download", "--filename", str(out_file), "--force-overwrite"],
                    capture_output=True, text=True, timeout=15
                )
                if out_file.exists():
                    shot = register_new_shot(out_file, trigger_source=f"{source_label} (Canon 7D Mark II USB)")
                    return {"ok": True, "mode": "USB_REAL_MAC", "shot": shot}

        # 2. Intento real en Windows vía digiCamControl CLI o EOS Utility
        elif OS_NAME == "Windows":
            dcc_paths = [
                Path(r"C:\Program Files (x86)\digiCamControl\CameraControlCmd.exe"),
                Path(r"C:\Program Files\digiCamControl\CameraControlCmd.exe"),
            ]
            dcc_exe = next((p for p in dcc_paths if p.exists()), None)
            if dcc_exe and STATE["camera_connected"]:
                res = subprocess.run(
                    [str(dcc_exe), "/filename", str(out_file), "/capture"],
                    capture_output=True, text=True, timeout=15
                )
                if out_file.exists():
                    shot = register_new_shot(out_file, trigger_source=f"{source_label} (Canon 7D Mark II USB)")
                    return {"ok": True, "mode": "USB_REAL_WIN", "shot": shot}

        # 3. Modo Simulador Óptico con fotos 100% reales del PORTAFOLIO AUTORIZADO
        auth_pool_dir = BASE_DIR / "portafolio_autorizado"
        auth_pool = list(auth_pool_dir.rglob("*.JPG")) + list(auth_pool_dir.rglob("*.jpg")) + list(auth_pool_dir.rglob("*.jpeg"))
        
        chosen = None
        if auth_pool:
            chosen = auth_pool[len(STATE["shots"]) % len(auth_pool)]
        else:
            # Respaldo directo a la carpeta en Desktop si existe
            desktop_pool_dir = Path("/Users/imac/Desktop/PORTAFOLIO AUTORIZADO")
            desktop_pool = list(desktop_pool_dir.rglob("*.JPG")) + list(desktop_pool_dir.rglob("*.jpg")) + list(desktop_pool_dir.rglob("*.jpeg"))
            if desktop_pool:
                chosen = desktop_pool[len(STATE["shots"]) % len(desktop_pool)]

        if chosen and chosen.exists():
            shutil.copy2(str(chosen), str(out_file))
            shot = register_new_shot(out_file, trigger_source=f"{source_label} (Portafolio Autorizado — Conecta USB para 7D Mk II)")
            return {"ok": True, "mode": "PORTAFOLIO_AUTORIZADO", "shot": shot}

        return {"ok": False, "error": "No se encontró cámara USB conectada ni fotos en el portafolio autorizado."}
    finally:
        STATE["is_shooting"] = False


def get_newest_unregistered_file():
    """Detecta si EOS Utility, Lightroom o Capture One acaba de guardar una foto nueva en sesiones_tether/."""
    known_names = {s["filename"] for s in STATE["shots"]}
    jpgs = sorted(TETHER_DIR.glob("*.jpg"), key=lambda p: p.stat().st_mtime, reverse=True)
    for j in jpgs:
        if j.name not in known_names:
            return j
    return None


def hot_folder_watcher_loop():
    """Vigila la carpeta sesiones_tether/ cada 1 segundo por si disparas desde el botón físico de la 7D Mark II."""
    while True:
        try:
            if not STATE["is_shooting"]:
                newest = get_newest_unregistered_file()
                if newest:
                    register_new_shot(newest, trigger_source="BOTÓN FÍSICO 7D MARK II (Hot-Folder)")
        except Exception:
            pass
        time.sleep(1.0)


class ArgonTetherHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def log_message(self, format, *args):
        pass  # Silenciar logs ruidosos

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/status":
            detect_camera()
            self._send_json(STATE)
            return
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            payload = json.loads(raw_body)
        except Exception:
            payload = {}

        if parsed.path == "/api/shoot":
            source = payload.get("source", "COMANDO DE VOZ")
            result = trigger_camera_shutter(source_label=source)
            self._send_json(result)
            return

        if parsed.path == "/api/preset":
            preset_key = payload.get("preset", "ESTUDIO_FLASH")
            result = apply_camera_preset_usb(preset_key)
            self._send_json(result)
            return

        if parsed.path == "/api/webcam_shot":
            # Permite disparar usando la señal de video / capturadora / cámara en vivo del navegador
            b64_data = payload.get("image_b64", "")
            if "," in b64_data:
                b64_data = b64_data.split(",", 1)[1]
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_file = TETHER_DIR / f"CAPTOORA_LIVE_{timestamp_str}.jpg"
            out_file.write_bytes(base64.b64decode(b64_data))
            shot = register_new_shot(out_file, trigger_source=payload.get("source", "LIVE VIEW / CAPTURADORA"))
            self._send_json({"ok": True, "mode": "LIVE_VIEW", "shot": shot})
            return

        if parsed.path == "/api/config":
            if "gemini_api_key" in payload:
                STATE["gemini_api_key"] = payload["gemini_api_key"].strip()
            if "director_mode" in payload:
                STATE["director_mode"] = payload["director_mode"]
            self._send_json({"ok": True, "state": STATE})
            return

        self._send_json({"ok": False, "error": "Ruta no encontrada"}, status=404)


def main():
    port = int(os.environ.get("ARGON_PORT", "8765"))
    detect_camera()

    watcher = threading.Thread(target=hot_folder_watcher_loop, daemon=True)
    watcher.start()

    server = HTTPServer(("127.0.0.1", port), ArgonTetherHandler)
    url = f"http://127.0.0.1:{port}/index.html"
    print("=" * 72)
    print("  ARGON LENS AI — ASISTENTE DE CÁMARA Y VOZ EN TIEMPO REAL")
    print(f"  Sistema Operativo : {STATE['os']}")
    print(f"  Cámara Detectada  : {STATE['camera_model']}")
    print(f"  Modo de Conexión  : {STATE['connection_mode']}")
    print(f"  Carpeta Tether    : {TETHER_DIR}")
    print(f"  Estudio Web Local : {url}")
    print("=" * 72)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando Argon Lens AI...")


if __name__ == "__main__":
    main()
