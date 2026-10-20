#!/usr/bin/env python3
"""
Captoora Studio - Local Event Photo Curator Server
100% Offline, Local HTTP Server con REST API y GUI Web.
Optimizado para Mac M1 (8GB RAM).
"""

import os
import sys
import json
import glob
import urllib.parse
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import cv2

# Importar motor local
from curator_engine import (
    PRESETS,
    load_image_normalized,
    apply_color_grading,
    generate_preview_and_metrics,
    export_curated_batch,
    hamming_distance
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
RECIPES_DIR = os.path.join(BASE_DIR, "recipes")
CACHE_DIR = os.path.join(BASE_DIR, ".cache_thumbs")
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(RECIPES_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

# Estado de la sesión actual en memoria
SESSION = {
    "input_folder": "",
    "output_folder": "",
    "client_tag": "EVENTO",
    "active_recipe": dict(PRESETS["transicion_equilibrada"]),
    "items": []
}

class CuratorRequestHandler(BaseHTTPRequestHandler):
    def end_headers_with_cors(self, content_type="application/json"):
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers_with_cors()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # 1. Servir archivos estáticos del frontend
        if path == "/" or path == "/index.html":
            self.serve_file(os.path.join(STATIC_DIR, "index.html"), "text/html; charset=utf-8")
            return
        elif path.startswith("/static/"):
            rel_path = path[len("/static/"):]
            file_path = os.path.join(STATIC_DIR, rel_path)
            ext = os.path.splitext(file_path)[1].lower()
            mime = {
                ".html": "text/html; charset=utf-8",
                ".css": "text/css; charset=utf-8",
                ".js": "application/javascript; charset=utf-8",
                ".svg": "image/svg+xml",
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg"
            }.get(ext, "application/octet-stream")
            self.serve_file(file_path, mime)
            return

        # 2. Servir miniaturas de imágenes cacheadas
        elif path == "/api/thumb":
            thumb_path = query.get("path", [""])[0]
            if os.path.exists(thumb_path):
                self.serve_file(thumb_path, "image/jpeg")
            else:
                self.send_error(404, "Thumbnail no encontrado")
            return

        # 3. Estado de la sesión
        elif path == "/api/status":
            self.send_response(200)
            self.end_headers_with_cors("application/json")
            resp = {
                "input_folder": SESSION["input_folder"],
                "output_folder": SESSION["output_folder"],
                "client_tag": SESSION["client_tag"],
                "active_recipe": SESSION["active_recipe"],
                "total_items": len(SESSION["items"]),
                "presets": PRESETS
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        # 4. Obtener items escaneados
        elif path == "/api/items":
            self.send_response(200)
            self.end_headers_with_cors("application/json")
            self.wfile.write(json.dumps({"items": SESSION["items"]}).encode("utf-8"))
            return

        # 5. Listar recetas guardadas
        elif path == "/api/recipes":
            self.send_response(200)
            self.end_headers_with_cors("application/json")
            recipe_files = glob.glob(os.path.join(RECIPES_DIR, "*.json"))
            recipes = []
            for rf in recipe_files:
                try:
                    with open(rf, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        recipes.append({"filename": os.path.basename(rf), "data": data})
                except Exception:
                    pass
            self.wfile.write(json.dumps({"recipes": recipes}).encode("utf-8"))
            return

        self.send_error(404, "Ruta no encontrada")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b""
        payload = json.loads(body.decode("utf-8")) if body else {}

        # 1. Escanear carpeta de entrada
        if path == "/api/scan":
            in_dir = payload.get("input_folder", "").strip()
            out_dir = payload.get("output_folder", "").strip()
            client_tag = payload.get("client_tag", "EVENTO").strip()

            if not os.path.exists(in_dir):
                self.send_response(400)
                self.end_headers_with_cors("application/json")
                self.wfile.write(json.dumps({"error": f"La carpeta de entrada no existe: {in_dir}"}).encode("utf-8"))
                return

            SESSION["input_folder"] = in_dir
            SESSION["output_folder"] = out_dir or os.path.join(in_dir, "00_CURATED_DELIVERY")
            SESSION["client_tag"] = client_tag

            # Buscar fotos
            exts = ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG", "*.webp", "*.WEBP")
            found_paths = []
            for ext in exts:
                found_paths.extend(glob.glob(os.path.join(in_dir, ext)))
            found_paths = sorted(list(set(found_paths)))

            # Procesar miniaturas y métricas
            items = []
            for idx, p in enumerate(found_paths):
                info = generate_preview_and_metrics(p, CACHE_DIR, SESSION["active_recipe"])
                info["index"] = idx
                items.append(info)

            # Detección consultiva de ráfagas continuas / duplicados
            for i in range(len(items)):
                is_burst = False
                burst_group = None
                # Comparar con la anterior y la siguiente
                if i > 0:
                    dist_prev = hamming_distance(items[i]["dhash"], items[i-1]["dhash"])
                    if dist_prev <= 10:
                        is_burst = True
                        burst_group = f"Ráfaga {i}"
                if i < len(items) - 1:
                    dist_next = hamming_distance(items[i]["dhash"], items[i+1]["dhash"])
                    if dist_next <= 10:
                        is_burst = True
                        burst_group = burst_group or f"Ráfaga {i+1}"
                items[i]["is_burst_duplicate"] = is_burst
                items[i]["burst_group"] = burst_group

            SESSION["items"] = items

            self.send_response(200)
            self.end_headers_with_cors("application/json")
            self.wfile.write(json.dumps({
                "status": "ok",
                "total": len(items),
                "items": items,
                "input_folder": in_dir,
                "output_folder": SESSION["output_folder"]
            }).encode("utf-8"))
            return

        # 2. Actualizar decisión de foto (Sí / Revisar / No)
        elif path == "/api/decision":
            index = payload.get("index")
            decision = payload.get("decision", "pending")  # "yes", "review", "no", "pending"
            if index is not None and 0 <= index < len(SESSION["items"]):
                SESSION["items"][index]["decision"] = decision
                self.send_response(200)
                self.end_headers_with_cors("application/json")
                self.wfile.write(json.dumps({"status": "ok", "index": index, "decision": decision}).encode("utf-8"))
            else:
                self.send_response(400)
                self.end_headers_with_cors("application/json")
                self.wfile.write(json.dumps({"error": "Índice fuera de rango"}).encode("utf-8"))
            return

        # 3. Actualizar receta activa o previsualización de una foto
        elif path == "/api/update_recipe":
            new_settings = payload.get("settings", {})
            apply_to_all = payload.get("apply_to_all", False)
            target_index = payload.get("target_index", None)

            SESSION["active_recipe"].update(new_settings)

            # Re-renderizar previsualización para el target o para todos
            if target_index is not None and 0 <= target_index < len(SESSION["items"]):
                item = SESSION["items"][target_index]
                # Reaplicar color grading en la miniatura de preview
                _, bgr_raw = load_image_normalized(item["path"], max_dim=1200)
                bgr_graded = apply_color_grading(bgr_raw, SESSION["active_recipe"])
                cv2.imwrite(item["graded_thumb"], bgr_graded, [cv2.IMWRITE_JPEG_QUALITY, 85])

            if apply_to_all:
                for item in SESSION["items"]:
                    _, bgr_raw = load_image_normalized(item["path"], max_dim=1200)
                    bgr_graded = apply_color_grading(bgr_raw, SESSION["active_recipe"])
                    cv2.imwrite(item["graded_thumb"], bgr_graded, [cv2.IMWRITE_JPEG_QUALITY, 85])

            self.send_response(200)
            self.end_headers_with_cors("application/json")
            self.wfile.write(json.dumps({"status": "ok", "active_recipe": SESSION["active_recipe"]}).encode("utf-8"))
            return

        # 4. Guardar receta JSON
        elif path == "/api/save_recipe":
            name = payload.get("name", "receta_personalizada").strip()
            clean_name = "".join(c for c in name if c.isalnum() or c in ("_", "-")).rstrip()
            if not clean_name:
                clean_name = "receta_evento"
            file_path = os.path.join(RECIPES_DIR, f"{clean_name}.json")
            data = {
                "name": name,
                "settings": SESSION["active_recipe"]
            }
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self.send_response(200)
            self.end_headers_with_cors("application/json")
            self.wfile.write(json.dumps({"status": "ok", "saved_file": file_path}).encode("utf-8"))
            return

        # 5. Exportar lote seleccionado
        elif path == "/api/export":
            out_dir = payload.get("output_folder", SESSION["output_folder"]).strip()
            client_tag = payload.get("client_tag", SESSION["client_tag"]).strip()

            if not out_dir:
                self.send_response(400)
                self.end_headers_with_cors("application/json")
                self.wfile.write(json.dumps({"error": "Carpeta de destino no especificada"}).encode("utf-8"))
                return

            report = export_curated_batch(
                SESSION["items"],
                out_dir,
                SESSION["active_recipe"],
                client_tag=client_tag
            )

            self.send_response(200)
            self.end_headers_with_cors("application/json")
            self.wfile.write(json.dumps({"status": "ok", "report": report}).encode("utf-8"))
            return

        self.send_error(404, "Ruta no encontrada")

    def serve_file(self, file_path, mime_type):
        if not os.path.exists(file_path):
            self.send_error(404, "Archivo no encontrado")
            return
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.end_headers_with_cors(mime_type)
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error leyendo archivo: {e}")

    def log_message(self, format, *args):
        # Silenciar logs ruidosos de HTTP para mantener la terminal limpia
        return

def run_server(port=8855):
    server = ThreadingHTTPServer(("127.0.0.1", port), CuratorRequestHandler)
    print(f"==========================================================")
    print(f"  CAPTOORA STUDIO - CURADOR Y REVELADOR LOCAL DE EVENTOS")
    print(f"  100% Offline | Cero APIs externas | Mac M1 8GB Optimized")
    print(f"  Disponible localmente en: http://127.0.0.1:{port}")
    print(f"==========================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido por el usuario.")
        server.server_close()

if __name__ == "__main__":
    port = 8855
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)
