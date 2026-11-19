#!/usr/bin/env python3
"""Research, screenshot, and public Apify profile scout for Captoora Influencers Regios."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[4]
CHROME_BIN = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


def normalize_instagram_handle(raw: str) -> str:
    """Extract clean Instagram username from @handle or profile URL."""
    val = (raw or "").strip()
    if "instagram.com/" in val.lower():
        parsed = urllib.parse.urlparse(val if "://" in val else f"https://{val}")
        parts = [p for p in parsed.path.split("/") if p]
        if parts:
            val = parts[0]
    val = val.lstrip("@").strip().strip("/")
    if not re.match(r"^[A-Za-z0-9._]{1,64}$", val):
        raise ValueError(f"Usuario de Instagram inválido: {raw!r}")
    return val


def load_apify_token() -> str:
    """Resolve APIFY_TOKEN from env or workspace .env without hardcoding secrets."""
    token = os.getenv("APIFY_TOKEN", "").strip()
    if token:
        return token
    env_path = ROOT_DIR / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("APIFY_TOKEN="):
                return s.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def fetch_apify_profile(handle: str, token: str) -> dict:
    """Run Apify apify~instagram-profile-scraper synchronously for a single public handle."""
    if not token:
        return {"source": "apify", "ok": False, "reason": "APIFY_TOKEN vacío en entorno/.env"}

    endpoint = (
        "https://api.apify.com/v2/acts/apify~instagram-profile-scraper/"
        f"run-sync-get-dataset-items?token={urllib.parse.quote(token)}&timeout=90"
    )
    payload = json.dumps({"usernames": [handle]}).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=95) as resp:
            items = json.loads(resp.read().decode("utf-8"))
        if isinstance(items, list) and items:
            item = items[0]
            return {
                "source": "apify",
                "ok": True,
                "username": item.get("username") or handle,
                "full_name": item.get("fullName"),
                "biography": item.get("biography"),
                "external_url": item.get("externalUrl"),
                "followers_count": item.get("followersCount"),
                "follows_count": item.get("followsCount"),
                "posts_count": item.get("postsCount"),
                "verified": item.get("verified"),
                "is_business_account": item.get("isBusinessAccount"),
                "business_category": item.get("businessCategoryName"),
                "profile_pic_url": item.get("profilePicUrlHD") or item.get("profilePicUrl"),
                "latest_posts_sample": [
                    {
                        "type": p.get("type"),
                        "caption": (p.get("caption") or "")[:220],
                        "likes": p.get("likesCount"),
                        "comments": p.get("commentsCount"),
                        "timestamp": p.get("timestamp"),
                        "url": p.get("url"),
                    }
                    for p in (item.get("latestPosts") or [])[:6]
                ],
            }
        return {"source": "apify", "ok": False, "reason": "Perfil sin datos públicos devueltos."}
    except urllib.error.HTTPError as exc:
        return {"source": "apify", "ok": False, "reason": f"HTTP {exc.code}: {exc.reason}"}
    except Exception as exc:
        return {"source": "apify", "ok": False, "reason": str(exc)}


def capture_profile_screenshot(handle: str, out_png: Path) -> dict:
    """Capture visual screenshot of public Instagram URL via Chrome headless without bypassing auth gates."""
    if not CHROME_BIN.exists():
        return {"ok": False, "reason": "Google Chrome no encontrado en ruta estándar macOS."}
    out_png.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://www.instagram.com/{handle}/"
    cmd = [
        str(CHROME_BIN),
        "--headless=new",
        "--disable-gpu",
        "--window-size=1280,960",
        "--virtual-time-budget=6000",
        f"--screenshot={out_png}",
        url,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0 or not out_png.exists():
        return {"ok": False, "reason": res.stderr.strip()[:220] or "No se pudo capturar pantalla."}
    return {"ok": True, "screenshot_path": str(out_png), "bytes": out_png.stat().st_size, "url": url}


def main() -> None:
    parser = argparse.ArgumentParser(description="Investiga y captura perfil público de Instagram para Captoora Influencers.")
    parser.add_argument("target", help="Usuario @handle o URL completa de Instagram.")
    parser.add_argument("--skip-apify", action="store_true", help="Omitir llamada Apify y solo tomar captura pública.")
    args = parser.parse_args()

    handle = normalize_instagram_handle(args.target)
    slug = re.sub(r"[^a-z0-9_]+", "_", handle.lower()).strip("_")
    out_dir = ROOT_DIR / "assets" / "influencers" / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    apify_data = {"source": "apify", "ok": False, "reason": "Omitido por bandera --skip-apify"}
    if not args.skip_apify:
        apify_data = fetch_apify_profile(handle, load_apify_token())

    shot_data = capture_profile_screenshot(handle, out_dir / "ig_profile.png")
    report = {
        "handle": f"@{handle}",
        "slug": slug,
        "instagram_url": f"https://www.instagram.com/{handle}/",
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "apify_profile": apify_data,
        "screenshot": shot_data,
    }
    report_path = out_dir / "scout_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report_path": str(report_path), **report}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
