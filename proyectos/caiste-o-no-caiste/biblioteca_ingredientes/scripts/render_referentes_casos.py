#!/usr/bin/env python3
"""
Renderiza los 10 Referentes Visuales ilustrados P1..P10 en PNG RGBA transparentes (1080x1080)
usando chrome-headless-shell + referentes_studio.html y valida canal alfa + contraste.
"""
import functools
import http.server
import math
import shutil
import socketserver
import struct
import subprocess
import threading
import zlib
from pathlib import Path

ROOT = Path("/Users/imac/Desktop/Projects/CAPTOORA.STUDIO")
OUT_DIR = ROOT / "proyectos/caiste-o-no-caiste/biblioteca_ingredientes/03_referentes_visuales_casos"
HEADLESS_SHELL = Path(
    "/Users/imac/Library/Caches/ms-playwright/chromium_headless_shell-1200/"
    "chrome-headless-shell-mac-x64/chrome-headless-shell"
)

CASE_IDS = [
    "ref_P1_paquete_retenido_almacen",
    "ref_P2_app_banco_compra_real",
    "ref_P3_netflix_dominio_falso",
    "ref_P4_cfe_recibo_luz_falso",
    "ref_P5_iphone17_premio_falso",
    "ref_P6_google_alerta_real",
    "ref_P7_trabajo_likes_whatsapp",
    "ref_P8_dhl_paquete_aduana",
    "ref_P9_codigo_6_digitos_real",
    "ref_P10_costco_cadena_pantalla",
]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def inspect_rgba_png(path: Path):
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return None
    pos = 8
    width = height = bit_depth = color_type = None
    idat_chunks = []
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        payload = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if ctype == b"IHDR":
            width, height, bit_depth, color_type = struct.unpack(">IIBB", payload[:10])
        elif ctype == b"IDAT":
            idat_chunks.append(payload)
        elif ctype == b"IEND":
            break

    if not width or not height or bit_depth != 8 or color_type != 6:
        return (width, height, color_type, 255, 0.0)

    bpp = 4
    raw = zlib.decompress(b"".join(idat_chunks))
    stride = width * bpp
    samples = []
    corner_alphas = []
    prev_row = bytearray(stride)
    row_step = max(1, height // 64)
    col_step = max(1, width // 64)
    idx = 0
    for y in range(height):
        ftype = raw[idx]
        idx += 1
        row = bytearray(raw[idx:idx + stride])
        idx += stride
        if ftype == 1:
            for x in range(bpp, stride):
                row[x] = (row[x] + row[x - bpp]) & 0xFF
        elif ftype == 2:
            for x in range(stride):
                row[x] = (row[x] + prev_row[x]) & 0xFF
        elif ftype == 3:
            for x in range(stride):
                left = row[x - bpp] if x >= bpp else 0
                row[x] = (row[x] + ((left + prev_row[x]) >> 1)) & 0xFF
        elif ftype == 4:
            for x in range(stride):
                a = row[x - bpp] if x >= bpp else 0
                b = prev_row[x]
                c = prev_row[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                row[x] = (row[x] + pr) & 0xFF
        prev_row = row
        if y in (8, height - 9):
            corner_alphas.append(row[8 * bpp + 3])
            corner_alphas.append(row[(width - 9) * bpp + 3])
        if y % row_step == 0:
            for x in range(0, width, col_step):
                p = x * bpp
                lum = 0.299 * row[p] + 0.587 * row[p + 1] + 0.114 * row[p + 2]
                samples.append(lum)

    mean = sum(samples) / len(samples)
    std = math.sqrt(sum((v - mean) ** 2 for v in samples) / len(samples))
    max_corner_alpha = max(corner_alphas) if corner_alphas else 255
    return (width, height, color_type, max_corner_alpha, std)


def render_one(port: int, case_id: str) -> None:
    out_path = OUT_DIR / f"{case_id}.png"
    profile = Path(f"/tmp/chrome_ref_{case_id}")
    shutil.rmtree(profile, ignore_errors=True)
    profile.mkdir(parents=True, exist_ok=True)
    out_path.unlink(missing_ok=True)

    url = (
        f"http://127.0.0.1:{port}/proyectos/caiste-o-no-caiste/"
        f"biblioteca_ingredientes/scripts/referentes_studio.html?id={case_id}"
    )
    cmd = [
        str(HEADLESS_SHELL),
        "--headless",
        f"--user-data-dir={profile}",
        "--window-size=1080,1080",
        "--force-device-scale-factor=1",
        "--hide-scrollbars",
        "--default-background-color=00000000",
        f"--screenshot={out_path}",
        url,
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20, check=True)
    finally:
        shutil.rmtree(profile, ignore_errors=True)

    info = inspect_rgba_png(out_path)
    if not info:
        raise RuntimeError(f"PNG inválido: {out_path}")
    w, h, ctype, corner_a, std = info
    if w != 1080 or h != 1080 or ctype != 6:
        raise RuntimeError(f"{case_id}: formato inesperado {w}x{h} ctype={ctype}")
    if corner_a != 0:
        raise RuntimeError(f"{case_id}: esquinas no transparentes (alpha={corner_a})")
    if std < 12.0:
        raise RuntimeError(f"{case_id}: baja varianza (stddev={std:.2f})")
    print(f"OK {out_path.name} ({out_path.stat().st_size} B, RGBA corner_alpha=0, stddev={std:.1f})")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        for cid in CASE_IDS:
            render_one(port, cid)
    finally:
        httpd.shutdown()
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
