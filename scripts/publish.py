#!/usr/bin/env python3
"""Captoora Publora publisher. Never prints API keys. Never uses Likinya handles."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

BASE = "https://api.publora.com/api/v1"
ROOT = Path(__file__).resolve().parents[1]
LIKINYA_BLOCKLIST = {"likinhya", "likinya8062", "celestialssh"}


def load_env() -> None:
    for env_path in (ROOT / ".env", Path("/Users/imac/likinya/.env")):
        if not env_path.exists():
            continue
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def key() -> str:
    load_env()
    k = os.environ.get("PUBLORA_API_KEY", "").strip()
    if not k:
        print("BLOCKED: falta PUBLORA_API_KEY en .env (no la pegues en el chat).", file=sys.stderr)
        sys.exit(2)
    return k


def api(method: str, path: str, body: dict | None = None) -> dict:
    url = f"{BASE}{path}"
    cmd = [
        "curl", "-sS", "-X", method, url,
        "-H", f"x-publora-key: {key()}",
        "-H", "Accept: application/json",
    ]
    if body is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(body)]
    raw = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, timeout=90)
    try:
        return json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        print(raw, file=sys.stderr)
        sys.exit(1)


def connections() -> list[dict]:
    data = api("GET", "/platform-connections")
    return data.get("connections") or []


def is_likinya(c: dict) -> bool:
    user = (c.get("username") or "").lower().lstrip("@")
    return user in LIKINYA_BLOCKLIST


def studio_platforms() -> list[dict]:
    load_env()
    wanted = []
    for envk in (
        "CAPTOORA_IG_PLATFORM_ID",
        "CAPTOORA_FB_PLATFORM_ID",
        "CAPTOORA_TT_PLATFORM_ID",
        "CAPTOORA_X_PLATFORM_ID",
    ):
        v = os.environ.get(envk, "").strip()
        if v:
            wanted.append(v)
    if wanted:
        return wanted
    return [
        c["platformId"]
        for c in connections()
        if not is_likinya(c) and c.get("tokenStatus") == "valid"
    ]


def cmd_list(_: argparse.Namespace) -> None:
    conns = connections()
    studio = [c for c in conns if not is_likinya(c)]
    likinya = [c for c in conns if is_likinya(c)]
    print("# Cuentas de ESTE estudio")
    if not studio:
        print("NINGUNA. Publora solo tiene Likinya. Connect IG/FB/TT del estudio y di: ya.")
    for c in studio:
        print(f"  {c.get('platformId')}  @{c.get('username')}  ({c.get('tokenStatus')})")
    print("\n# Likinya (NO usar para Captoora)")
    for c in likinya:
        print(f"  @{c.get('username')}  ({c.get('tokenStatus')})")
    ids = studio_platforms()
    print("\n# platformIds que usaría un post ahora:")
    print("  " + (", ".join(ids) if ids else "(vacío — BLOCKED)"))


def cmd_post(args: argparse.Namespace) -> None:
    platforms = [p.strip() for p in args.platforms.split(",") if p.strip()] if args.platforms else studio_platforms()
    if not platforms:
        print(
            "BLOCKED: Publora no tiene las cuentas de este estudio. "
            "Connect IG/FB/TT del estudio en el dashboard. Di: ya. No pegues password.",
            file=sys.stderr,
        )
        sys.exit(2)
    # Safety: refuse Likinya ids even if passed by hand
    conns = {c.get("platformId"): c for c in connections()}
    for pid in platforms:
        c = conns.get(pid) or {}
        if is_likinya(c):
            print(f"BLOCKED: {pid} es Likinya (@{c.get('username')}). No se publica ahí.", file=sys.stderr)
            sys.exit(2)
    text = args.text or ""
    if args.template:
        text = (f"[plantilla {args.template:02d}] " + text).strip()
    body: dict = {"content": text, "platforms": platforms}
    if args.when:
        body["scheduledTime"] = args.when
    if args.media:
        body["mediaUrls"] = [u.strip() for u in args.media.split(",") if u.strip()]
    print("create-post →", platforms)
    res = api("POST", "/create-post", body)
    print(json.dumps(res, indent=2, ensure_ascii=False))


def main() -> None:
    p = argparse.ArgumentParser(description="Captoora Publora publisher")
    sub = p.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("list")
    s1.set_defaults(func=cmd_list)
    s2 = sub.add_parser("post")
    s2.add_argument("--text", default="")
    s2.add_argument("--template", type=int, default=None)
    s2.add_argument("--platforms", default=None)
    s2.add_argument("--when", default=None)
    s2.add_argument("--media", default=None)
    s2.set_defaults(func=cmd_post)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
