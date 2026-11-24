#!/usr/bin/env python3
"""
Renderiza localmente con chrome-headless-shell (o Google Chrome for Testing como respaldo)
y Three.js (voxel_studio.html) los 4 personajes y 3 escenarios PNG de ¿Caíste o no caíste?
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
PROJECT = ROOT / "proyectos/caiste-o-no-caiste"
HEADLESS_SHELL = Path(
    "/Users/imac/Library/Caches/ms-playwright/chromium_headless_shell-1200/"
    "chrome-headless-shell-mac-x64/chrome-headless-shell"
)
CHROME_FOR_TESTING = Path(
    "/Users/imac/Library/Caches/ms-playwright/chromium-1200/"
    "chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
)

ASSETS = [
    ("guardrails_antigravity", PROJECT / "assets/personajes/guardrails_antigravity.png", (1080, 1080)),
    ("chatgpt_facil", PROJECT / "assets/personajes/chatgpt_facil.png", (1080, 1080)),
    ("claude_medio", PROJECT / "assets/personajes/claude_medio.png", (1080, 1080)),
    ("grok_dificil", PROJECT / "assets/personajes/grok_dificil.png", (1080, 1080)),
    ("escenario_01_facil_casa", PROJECT / "assets/escenarios/escenario_01_facil_casa.png", (1920, 1080)),
    ("escenario_02_medio_oficina", PROJECT / "assets/escenarios/escenario_02_medio_oficina.png", (1920, 1080)),
    ("escenario_03_dificil_cima_rieles", PROJECT / "assets/escenarios/escenario_03_dificil_cima_rieles.png", (1920, 1080)),
]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def inspect_png_variance(path: Path):
    """Decodifica cabeceras e IDAT de un PNG RGBA/RGB para verificar tamaño y contraste no plano."""
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

    if not width or not height or bit_depth != 8 or color_type not in (2, 6):
        return (width, height, 0.0)

    bpp = 3 if color_type == 2 else 4
    raw = zlib.decompress(b"".join(idat_chunks))
    stride = width * bpp
    samples = []
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
        if y % row_step == 0:
            for x in range(0, width, col_step):
                p = x * bpp
                lum = 0.299 * row[p] + 0.587 * row[p + 1] + 0.114 * row[p + 2]
                samples.append(lum)

    mean = sum(samples) / len(samples)
    std = math.sqrt(sum((v - mean) ** 2 for v in samples) / len(samples))
    return (width, height, std)


def render_one(
    browser: Path,
    url: str,
    out_path: Path,
    size: tuple[int, int],
    is_cft: bool = False,
) -> tuple[bool, str]:
    w, h = size
    profile_dir = Path(f"/tmp/chrome_voxel_prof_{w}_{h}_{int(is_cft)}")
    if profile_dir.exists():
        shutil.rmtree(profile_dir)
    profile_dir.mkdir(parents=True, exist_ok=True)
    out_path.unlink(missing_ok=True)

    cmd = [
        str(browser),
        "--headless=new" if is_cft else "--headless",
    ]
    if is_cft:
        cmd.extend(["--no-first-run", "--no-default-browser-check"])
    cmd.extend([
        f"--user-data-dir={profile_dir}",
        f"--window-size={w},{h}",
        "--force-device-scale-factor=1",
        "--hide-scrollbars",
        "--virtual-time-budget=2500",
        "--enable-webgl",
        "--ignore-gpu-blocklist",
        "--use-gl=angle",
        "--use-angle=swiftshader",
        "--enable-unsafe-swiftshader",
        f"--screenshot={out_path}",
        url,
    ])

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    except subprocess.TimeoutExpired:
        return False, "timeout (30s)"
    finally:
        shutil.rmtree(profile_dir, ignore_errors=True)

    if res.returncode != 0 or not out_path.exists():
        err = res.stderr.decode("utf-8", errors="replace")[-350:]
        return False, f"rc={res.returncode}: {err}"

    info = inspect_png_variance(out_path)
    if not info:
        return False, "PNG inválido"
    pw, ph, std = info
    if pw != w or ph != h:
        return False, f"dimensiones {pw}x{ph} != {w}x{h}"
    if std < 8.0:
        return False, f"render plano/vacío (stddev={std:.2f})"
    return True, f"{pw}x{ph} bytes={out_path.stat().st_size} stddev={std:.2f}"


def main() -> int:
    engines = []
    if HEADLESS_SHELL.exists():
        engines.append(("chrome-headless-shell", HEADLESS_SHELL, False))
    if CHROME_FOR_TESTING.exists():
        engines.append(("chrome-for-testing", CHROME_FOR_TESTING, True))
    if not engines:
        print("ERROR: no se encontró chrome-headless-shell ni Google Chrome for Testing")
        return 1

    (PROJECT / "assets/personajes").mkdir(parents=True, exist_ok=True)
    (PROJECT / "assets/escenarios").mkdir(parents=True, exist_ok=True)

    handler = functools.partial(QuietHandler, directory=str(ROOT))
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    try:
        print(f"Servidor local temporal en http://127.0.0.1:{port}/")
        for scene_id, out_path, size in ASSETS:
            url = f"http://127.0.0.1:{port}/proyectos/caiste-o-no-caiste/voxel_studio.html?scene={scene_id}"
            rendered = False
            last_msg = ""
            for label, browser, is_cft in engines:
                ok, msg = render_one(browser, url, out_path, size, is_cft=is_cft)
                if ok:
                    print(f"OK [{label}] {scene_id} -> {out_path.relative_to(ROOT)} ({msg})")
                    rendered = True
                    break
                last_msg = f"[{label}] {msg}"
                print(f"[retry fallback] {scene_id}: {last_msg}")
            if not rendered:
                print(f"FAIL {scene_id}: {last_msg}")
                return 2
    finally:
        httpd.shutdown()
        httpd.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
