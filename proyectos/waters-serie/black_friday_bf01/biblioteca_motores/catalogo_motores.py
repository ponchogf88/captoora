#!/usr/bin/env python3
"""
Escanea todas las carpetas de motores en biblioteca_motores/ (.mp4/.mov/.jpg/.png),
extrae duración y resolución vía ffprobe/ffmpeg cuando aplica, y genera
biblioteca_data.js (window.BF01_BIBLIOTECA) compatible con file://.
"""
import json
import subprocess
import shutil
from pathlib import Path
from typing import Any, Dict, List

HERE = Path(__file__).resolve().parent
FFPROBE = shutil.which("ffprobe") or "/opt/homebrew/bin/ffprobe"

SCENES = [
    {"idx": 1, "slug": "01_hook", "titulo": "01 · Hook Black Friday", "angulo": "Close-Up frontal alerta"},
    {"idx": 2, "slug": "02_bucle", "titulo": "02 · El Bucle en AI Box", "angulo": "3/4 izquierda mirando derecha"},
    {"idx": 3, "slug": "03_grafica", "titulo": "03 · Gráfica $2,000 USD", "angulo": "Plano medio contrapicado"},
    {"idx": 4, "slug": "04_dilema", "titulo": "04 · Dilema Puertas 3D", "angulo": "3/4 derecha (2 dedos)"},
    {"idx": 5, "slug": "05_candados", "titulo": "05 · 3 Candados Checklist", "angulo": "Plano pecho contando 1-2-3"},
    {"idx": 6, "slug": "06_cta", "titulo": "06 · Cierre CTA Presupuesto", "angulo": "Close-Up eye-level"},
]

ENGINES = [
    {"id": "06_angulos_base_img", "label": "Ángulos Base 16:9", "kind": "image"},
    {"id": "01_gemini_veo", "label": "Google Flow / Veo (Web)", "kind": "video"},
    {"id": "07_gemini_api_omni", "label": "Gemini API · Omni 1.1 Flash", "kind": "video"},
    {"id": "02_grok", "label": "Grok Imagine (Web/xAI)", "kind": "video"},
    {"id": "03_sora_gpt", "label": "ChatGPT / OpenAI API", "kind": "video"},
    {"id": "04_meta_ai", "label": "Meta AI", "kind": "video"},
    {"id": "05_picsart", "label": "Picsart (Seedance 2.5)", "kind": "video"},
    {"id": "08_wan_alibaba", "label": "Wan Video (Alibaba)", "kind": "video"},
    {"id": "09_kling_ai", "label": "Kling AI (China)", "kind": "video"},
    {"id": "10_hailuo_minimax", "label": "Hailuo / MiniMax (China)", "kind": "video"},
]


def probe_media(path: Path) -> Dict[str, Any]:
    ext = path.suffix.lower()
    if ext in (".mp4", ".mov", ".webm", ".mkv"):
        try:
            out = subprocess.check_output(
                [
                    FFPROBE, "-v", "error", "-select_streams", "v:0",
                    "-show_entries", "stream=width,height:format=duration",
                    "-of", "json", str(path),
                ],
                text=True,
            )
            data = json.loads(out)
            st = (data.get("streams") or [{}])[0]
            fmt = data.get("format") or {}
            return {
                "type": "video",
                "width": int(st.get("width") or 0),
                "height": int(st.get("height") or 0),
                "duration": round(float(fmt.get("duration") or 0), 2),
                "size_mb": round(path.stat().st_size / (1024 * 1024), 2),
            }
        except Exception:
            return {"type": "video", "width": 0, "height": 0, "duration": 0, "size_mb": round(path.stat().st_size / (1024 * 1024), 2)}
    return {
        "type": "image",
        "size_kb": round(path.stat().st_size / 1024, 1),
    }


def find_scene_files(folder: Path, scene_idx: int) -> List[Path]:
    if not folder.exists():
        return []
    prefixes = (f"{scene_idx:02d}", f"s{scene_idx:02d}", f"escena_{scene_idx:02d}", f"scene_{scene_idx:02d}", f"{scene_idx}_", f"{scene_idx}.")
    hits = []
    for p in sorted(folder.iterdir()):
        if not p.is_file() or p.name.startswith("."):
            continue
        if p.suffix.lower() not in (".mp4", ".mov", ".webm", ".jpg", ".jpeg", ".png", ".webp"):
            continue
        low = p.name.lower()
        if any(low.startswith(pref) for pref in prefixes):
            hits.append(p)
    return hits


def main() -> int:
    rows = []
    for sc in SCENES:
        idx = sc["idx"]
        cells: Dict[str, Any] = {}
        for eng in ENGINES:
            folder = HERE / eng["id"]
            matches = find_scene_files(folder, idx)
            items = []
            for m in matches:
                info = probe_media(m)
                info["rel_path"] = f"{eng['id']}/{m.name}"
                info["name"] = m.name
                items.append(info)
            cells[eng["id"]] = items
        rows.append({**sc, "cells": cells})

    payload = {
        "generated_at": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"),
        "ref_img": "00_referencia_maestra/avatar_ref.jpg",
        "engines": ENGINES,
        "rows": rows,
    }
    js_out = HERE / "biblioteca_data.js"
    js_out.write_text(
        "window.BF01_BIBLIOTECA = " + json.dumps(payload, indent=2, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    print(f"OK -> {js_out} ({len(rows)} escenas x {len(ENGINES)} columnas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
