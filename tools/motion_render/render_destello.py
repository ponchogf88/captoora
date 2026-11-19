#!/usr/bin/env python3
"""Render determinista de "El Destello" (Captoora Signature) a MP4.

Mismo principio que Remotion: la escena es una función pura seek(t); Chrome headless
pinta cada fotograma y ffmpeg lo codifica. Aquí no hay Node, así que se usa Chrome
por DevTools Protocol desde Python.

Uso (entorno aislado fuera de iCloud):
  ~/.venvs/captoora-motion/bin/python tools/motion_render/render_destello.py
  ~/.venvs/captoora-motion/bin/python tools/motion_render/render_destello.py --stills 1.0,3.6,8.1 --qa-dir /tmp/qa
"""
from __future__ import annotations

import argparse
import base64
import json
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
import wave
from pathlib import Path

import imageio_ffmpeg
import numpy as np
import websocket

ROOT = Path(__file__).resolve().parents[2]
SCENE_DIR = ROOT / "docs/motion_lab/destello_signature"
SCENE = SCENE_DIR / "index.html"
OUT_DIR = SCENE_DIR / "render"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H, FPS, DUR = 1080, 1920, 60, 10.0
NF = int(FPS * DUR)
SR = 48000


# ----------------------------------------------------------------- audio
def _env(n, attack, tau):
    t = np.arange(n) / SR
    e = np.exp(-np.maximum(t - attack, 0) / tau)
    if attack > 0:
        e = np.where(t < attack, t / attack, e)
    return e


def _band(x, lo, hi):
    f = np.fft.rfft(x)
    fr = np.fft.rfftfreq(len(x), 1 / SR)
    f[(fr < lo) | (fr > hi)] = 0
    return np.fft.irfft(f, len(x))


def synth_audio(path: Path) -> None:
    n = int(SR * DUR)
    out = np.zeros((n, 2))
    rng = np.random.default_rng(20261026)

    def add(sig, t0, gain=1.0, pan=0.0):
        i = int(t0 * SR)
        if i >= n:
            return
        sig = sig[: n - i] * gain
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        out[i : i + len(sig), 0] += sig * l * 1.41
        out[i : i + len(sig), 1] += sig * r * 1.41

    def tone(freq, dur, attack, tau, f_end=None):
        m = int(dur * SR)
        t = np.arange(m) / SR
        if f_end is None:
            ph = 2 * np.pi * freq * t
        else:  # barrido exponencial
            k = np.log(f_end / freq) / dur
            ph = 2 * np.pi * freq * (np.exp(k * t) - 1) / k
        return np.sin(ph) * _env(m, attack, tau)

    def noise(dur, lo, hi, attack, tau):
        m = int(dur * SR)
        return _band(rng.standard_normal(m), lo, hi) * _env(m, attack, tau) * 0.35

    def shutter(t0, gain):
        add(noise(0.03, 1500, 9000, 0.0005, 0.004), t0, gain)
        add(tone(1200, 0.02, 0.0005, 0.003), t0, gain * 0.5)
        add(tone(180, 0.05, 0.001, 0.012), t0, gain * 0.5)
        add(noise(0.03, 1000, 6000, 0.0005, 0.004), t0 + 0.045, gain * 0.6)
        add(tone(800, 0.02, 0.0005, 0.003), t0 + 0.045, gain * 0.3)

    # Beat 1 · flash
    shutter(0.30, 0.9)
    sub = tone(45, 2.6, 0.9, 0.9) + 0.3 * tone(90, 2.6, 0.9, 0.7)
    add(sub, 0.30, 0.35)
    add(noise(1.2, 200, 4000, 0.01, 0.35), 0.30, 0.5)
    sw = noise(0.7, 300, 5000, 0.5, 0.08)
    add(sw, 1.80, 0.35, -0.3)
    # Beat 2 · catchlight
    shutter(2.50, 0.7)
    add(tone(70, 0.3, 0.002, 0.07), 2.50, 0.6)
    whine = tone(1800, 1.7, 0.05, 0.9, f_end=5200)
    add(whine, 2.55, 0.035, 0.2)
    add(tone(55, 0.3, 0.004, 0.06), 3.25, 0.45)
    add(tone(55, 0.3, 0.004, 0.06), 3.52, 0.3)
    for tw in (3.45, 4.15, 4.75):
        add(tone(3520, 0.25, 0.003, 0.06), tw, 0.03, 0.4)
    # Beat 3 · visión: bip de enfoque + arpegio cristalino
    add(tone(2730, 0.05, 0.002, 0.03), 5.12, 0.12)
    add(tone(2730, 0.05, 0.002, 0.03), 5.24, 0.12)
    notes = [880.0, 987.8, 1108.7, 1318.5, 1480.0, 1760.0, 1975.5, 2217.5, 2637.0, 2960.0, 3520.0, 2637.0]
    for i, f in enumerate(notes):
        bell = tone(f, 0.9, 0.004, 0.35) + 0.25 * tone(f * 2.01, 0.9, 0.004, 0.2)
        add(bell, 5.45 + i * 0.16, 0.06, -0.6 if i % 2 else 0.6)
    # Beat 4 · subida, impacto, campana
    m = int(0.6 * SR)
    riser = _band(rng.standard_normal(m), 400, 7000) * np.linspace(0, 1, m) ** 2.5 * 0.35
    add(riser, 7.40, 0.5)
    add(tone(200, 0.6, 0.3, 0.3, f_end=800) * np.linspace(0, 1, int(0.6 * SR)), 7.40, 0.08)
    add(tone(80, 0.6, 0.002, 0.16, f_end=40), 8.00, 0.9)
    add(noise(0.7, 40, 900, 0.002, 0.18), 8.00, 0.6)
    shutter(8.00, 0.6)
    bell = sum(a * tone(1318.5 * p, 2.0, 0.003, 0.7 / (1 + k * 0.6))
               for k, (p, a) in enumerate([(1, 1), (2.76, 0.5), (5.40, 0.25), (8.93, 0.12)]))
    add(bell, 8.04, 0.12)
    add(tone(659.25, 2.0, 0.01, 0.8), 8.04, 0.06)
    add(tone(2637, 0.3, 0.003, 0.07) + tone(3520, 0.3, 0.003, 0.05), 8.43, 0.05, 0.5)
    shutter(9.70, 0.25)

    peak = np.max(np.abs(out)) or 1.0
    out = out / peak * 0.89
    fade = int(0.03 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)[:, None]
    pcm = (np.clip(out, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


# ------------------------------------------------------------- chrome cdp
class CDP:
    def __init__(self, url: str):
        self.ws = websocket.create_connection(url, timeout=120, suppress_origin=True)
        self.i = 0

    def call(self, method: str, **params):
        self.i += 1
        mid = self.i
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def eval(self, expr: str, await_promise: bool = False):
        r = self.call("Runtime.evaluate", expression=expr, awaitPromise=await_promise, returnByValue=True)
        if "exceptionDetails" in r:
            raise RuntimeError(f"JS: {r['exceptionDetails']}")
        return r.get("result", {}).get("value")


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def open_scene():
    port = free_port()
    profile = tempfile.mkdtemp(prefix="captoora-chrome-")
    proc = subprocess.Popen(
        [CHROME, "--headless=new", f"--remote-debugging-port={port}", f"--user-data-dir={profile}",
         "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "--mute-audio",
         "--allow-file-access-from-files", "--force-device-scale-factor=1", f"--window-size={W},{H}",
         "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    targets = None
    for _ in range(100):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=1) as r:
                targets = [t for t in json.load(r) if t.get("type") == "page"]
            if targets:
                break
        except OSError:
            pass
        time.sleep(0.2)
    if not targets:
        proc.kill()
        raise SystemExit("BLOCKED: Chrome headless no respondió.")
    cdp = CDP(targets[0]["webSocketDebuggerUrl"])
    cdp.call("Page.enable")
    cdp.call("Runtime.enable")
    cdp.call("Emulation.setDeviceMetricsOverride", width=W, height=H, deviceScaleFactor=1, mobile=False)
    cdp.call("Page.navigate", url=SCENE.as_uri() + "?render=1")
    for _ in range(300):
        time.sleep(0.1)
        try:
            if cdp.eval("window.__error || ''"):
                raise SystemExit("Error en escena: " + cdp.eval("window.__error"))
            if cdp.eval("window.__ready === true"):
                break
        except RuntimeError:
            pass
    else:
        raise SystemExit("BLOCKED: la escena no terminó de cargar (¿rutas de assets?).")
    return proc, profile, cdp


def shot(cdp: CDP, t: float) -> bytes:
    cdp.eval(f"window.seekAndWait({t:.6f})", await_promise=True)
    r = cdp.call("Page.captureScreenshot", format="png",
                 clip={"x": 0, "y": 0, "width": W, "height": H, "scale": 1})
    return base64.b64decode(r["data"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stills", default="", help="tiempos en segundos separados por coma (QA)")
    ap.add_argument("--qa-dir", default="", help="carpeta para los stills de QA")
    ap.add_argument("--name", default="captoora_signature_destello_10s_1080x1920")
    args = ap.parse_args()

    ff = imageio_ffmpeg.get_ffmpeg_exe()
    proc, profile, cdp = open_scene()
    try:
        if args.stills:
            qa = Path(args.qa_dir or tempfile.mkdtemp(prefix="destello-qa-"))
            qa.mkdir(parents=True, exist_ok=True)
            for t in [float(x) for x in args.stills.split(",") if x.strip()]:
                p = qa / f"still_{t:05.2f}s.png"
                p.write_bytes(shot(cdp, t))
                print(p)
            return

        OUT_DIR.mkdir(parents=True, exist_ok=True)
        tmp = Path(tempfile.mkdtemp(prefix="destello-audio-"))
        wav = tmp / "sfx.wav"
        synth_audio(wav)
        # audio para el preview del HTML
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(wav), "-c:a", "aac", "-b:a", "160k",
                        str(SCENE_DIR / "destello_sfx.m4a")], check=True)

        out = OUT_DIR / f"{args.name}.mp4"
        enc = subprocess.Popen(
            [ff, "-y", "-loglevel", "error",
             "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
             "-i", str(wav),
             "-map", "0:v", "-map", "1:a",
             "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
             "-profile:v", "high", "-level", "4.2", "-r", str(FPS),
             "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)],
            stdin=subprocess.PIPE)
        t0 = time.time()
        for f in range(NF):
            enc.stdin.write(shot(cdp, f / FPS))
            if f % 60 == 0:
                print(f"frame {f:03d}/{NF}  {time.time() - t0:5.1f}s", flush=True)
        enc.stdin.close()
        if enc.wait() != 0:
            raise SystemExit("ffmpeg falló")
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"OK {out}  ({out.stat().st_size / 1e6:.1f} MB, {time.time() - t0:.0f}s)")
    finally:
        try:
            cdp.ws.close()
        except Exception:
            pass
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        shutil.rmtree(profile, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
