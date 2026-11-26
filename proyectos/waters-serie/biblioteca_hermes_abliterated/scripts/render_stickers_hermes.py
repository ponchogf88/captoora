#!/usr/bin/env python3
"""
Renderiza los 6 stickers PNG RGBA transparentes (1080x1080) del paquete Black Canvas Coloreado
para la biblioteca Hermes Agent + Abliterated.
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
OUT_DIR = ROOT / "proyectos/waters-serie/biblioteca_hermes_abliterated/01_stickers_black_canvas"
HEADLESS_SHELL = Path(
    "/Users/imac/Library/Caches/ms-playwright/chromium_headless_shell-1200/"
    "chrome-headless-shell-mac-x64/chrome-headless-shell"
)

STICKER_IDS = [
    "stk_01_abliteration_vector",
    "stk_02_hermes_loop",
    "stk_03_filtros_vs_auditoria",
    "stk_04_docker_sandbox_escudo",
    "stk_05_vps_gpu_finops",
    "stk_06_alerta_prompt_injection",
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
    if color_type != 6 or not idat_chunks:
        return (width, height, color_type, 255, 0.0)

    raw = zlib.decompress(b"".join(idat_chunks))
    stride = width * 4
    rows = []
    idx = 0
    prev = bytearray(stride)
    for _ in range(height):
        filt = raw[idx]
        idx += 1
        row = bytearray(raw[idx:idx + stride])
        idx += stride
        if filt == 1:
            for i in range(4, stride):
                row[i] = (row[i] + row[i - 4]) & 0xFF
        elif filt == 2:
            for i in range(stride):
                row[i] = (row[i] + prev[i]) & 0xFF
        elif filt == 3:
            for i in range(stride):
                left = row[i - 4] if i >= 4 else 0
                row[i] = (row[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif filt == 4:
            for i in range(stride):
                a = row[i - 4] if i >= 4 else 0
                b = prev[i]
                c = prev[i - 4] if i >= 4 else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                row[i] = (row[i] + pr) & 0xFF
        rows.append(row)
        prev = row

    corners = [(2, 2), (width - 3, 2), (2, height - 3), (width - 3, height - 3)]
    corner_alphas = [rows[y][x * 4 + 3] for x, y in corners]
    samples = []
    for y in range(0, height, 24):
        row = rows[y]
        for x in range(0, width, 24):
            p = x * 4
            if row[p + 3] > 20:
                samples.append(0.299 * row[p] + 0.587 * row[p + 1] + 0.114 * row[p + 2])
    mean = sum(samples) / len(samples) if samples else 0.0
    std = math.sqrt(sum((v - mean) ** 2 for v in samples) / len(samples)) if samples else 0.0
    return (width, height, color_type, max(corner_alphas), std)


def render_one(port: int, sticker_id: str) -> None:
    out_path = OUT_DIR / f"{sticker_id}.png"
    profile = Path(f"/tmp/chrome_hermes_{sticker_id}")
    shutil.rmtree(profile, ignore_errors=True)
    profile.mkdir(parents=True, exist_ok=True)
    out_path.unlink(missing_ok=True)

    url = (
        f"http://127.0.0.1:{port}/proyectos/waters-serie/"
        f"biblioteca_hermes_abliterated/scripts/black_canvas_stickers.html?id={sticker_id}"
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
    if w != 1080 or h != 1080 or ctype != 6 or corner_a != 0:
        raise RuntimeError(f"{sticker_id}: {w}x{h} ctype={ctype} corner_a={corner_a}")
    print(f"OK {out_path.name} ({out_path.stat().st_size} B, RGBA corner_alpha=0, std={std:.1f})")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        for sid in STICKER_IDS:
            render_one(port, sid)
    finally:
        httpd.shutdown()
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
