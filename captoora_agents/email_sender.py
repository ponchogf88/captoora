"""Zoho Mail SMTP sender for Captoora Studio (chuy@captoora.studio) with copy guardrails."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import smtplib
import ssl
from dataclasses import dataclass
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from . import ROOT_DIR
from .config import append_agent_event, validate_client_copy


@dataclass(frozen=True)
class ZohoSmtpConfig:
    """SMTP configuration loaded cleanly from environment / .env."""

    host: str
    port: int
    username: str
    password: str
    from_name: str

    @property
    def is_configured(self) -> bool:
        return bool(self.host and self.port and self.username and self.password)

    def missing_env_vars(self) -> list[str]:
        missing: list[str] = []
        if not self.username:
            missing.append("SMTP_USER")
        if not self.password:
            missing.append("SMTP_PASS")
        return missing


def load_smtp_config() -> ZohoSmtpConfig:
    """Load current Zoho SMTP environment settings, reloading .env if present."""
    env_file = ROOT_DIR / ".env"
    if env_file.exists():
        load_dotenv(env_file, override=True)
    raw_port = (os.getenv("SMTP_PORT") or "465").strip()
    try:
        port = int(raw_port)
    except ValueError:
        port = 465
    return ZohoSmtpConfig(
        host=(os.getenv("SMTP_HOST") or "smtp.zoho.com").strip(),
        port=port,
        username=(os.getenv("SMTP_USER") or "chuy@captoora.studio").strip(),
        password=(os.getenv("SMTP_PASS") or "").strip(),
        from_name=(os.getenv("SMTP_FROM_NAME") or "Jesús Gutiérrez · Captoora Studio").strip(),
    )


def get_smtp_status() -> dict[str, Any]:
    """Return non-secret Zoho Mail SMTP readiness status for Dashboard / CLI."""
    cfg = load_smtp_config()
    return {
        "configured": cfg.is_configured,
        "provider": "zoho_smtp",
        "host": cfg.host,
        "port": cfg.port,
        "sender": cfg.username,
        "from_name": cfg.from_name,
        "env_exists": (ROOT_DIR / ".env").exists(),
        "missing_env": cfg.missing_env_vars(),
    }


def _strip_html(html_text: str) -> str:
    no_tags = re.sub(r"<style[^>]*>.*?</style>", " ", html_text, flags=re.IGNORECASE | re.DOTALL)
    no_tags = re.sub(r"<[^>]+>", " ", no_tags)
    return re.sub(r"\s+", " ", no_tags).strip()


def send_email_via_zoho(
    *,
    to_email: str,
    subject: str,
    html_body: str,
    plain_text: str | None = None,
    attachments: list[Path] | None = None,
    config: ZohoSmtpConfig | None = None,
    dry_run: bool = False,
    save_eml_path: Path | None = None,
) -> dict[str, Any]:
    """Build and optionally transmit a client-safe HTML+attachment email from chuy@captoora.studio."""
    cfg = config or load_smtp_config()
    plain = plain_text.strip() if plain_text else _strip_html(html_body)
    for chunk in (subject, plain):
        violations = validate_client_copy(chunk)
        if violations:
            raise ValueError(f"Email bloqueado por guardrail: {'; '.join(violations)}")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr((cfg.from_name, cfg.username))
    msg["To"] = to_email.strip()
    msg["Reply-To"] = cfg.username
    msg.set_content(plain or subject)
    msg.add_alternative(html_body, subtype="html")

    attached_names: list[str] = []
    for att_path in attachments or []:
        if not att_path.exists():
            raise FileNotFoundError(f"Adjunto no encontrado: {att_path}")
        ctype, _ = mimetypes.guess_type(str(att_path))
        maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
        msg.add_attachment(
            att_path.read_bytes(),
            maintype=maintype,
            subtype=subtype,
            filename=att_path.name,
        )
        attached_names.append(att_path.name)

    eml_saved: str | None = None
    if save_eml_path is not None:
        save_eml_path.parent.mkdir(parents=True, exist_ok=True)
        save_eml_path.write_bytes(msg.as_bytes())
        eml_saved = str(save_eml_path)

    if dry_run or not cfg.is_configured:
        return {
            "sent": False,
            "mode": "dry_run" if dry_run else "missing_credentials",
            "from": cfg.username,
            "to": to_email.strip(),
            "subject": subject,
            "attachments": attached_names,
            "eml_path": eml_saved,
            "missing_env": [] if dry_run else cfg.missing_env_vars(),
        }

    ctx = ssl.create_default_context()
    if cfg.port == 465:
        with smtplib.SMTP_SSL(cfg.host, cfg.port, timeout=30, context=ctx) as server:
            server.login(cfg.username, cfg.password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(cfg.host, cfg.port, timeout=30) as server:
            server.starttls(context=ctx)
            server.login(cfg.username, cfg.password)
            server.send_message(msg)

    append_agent_event(
        "ventas_outreach",
        f"Correo enviado desde {cfg.username}",
        f"Para {to_email.strip()} · {len(attached_names)} adjuntos ({subject[:80]})",
        target_agent="ventas_outreach",
        zone="trigger_gate",
        source="zoho_smtp",
    )
    return {
        "sent": True,
        "mode": "zoho_smtp",
        "from": cfg.username,
        "to": to_email.strip(),
        "subject": subject,
        "attachments": attached_names,
    }


def send_self_test_email(
    to_email: str = "ponchogf88@me.com",
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Transmit the TEST-003 self-test dossier + visual mockups from chuy@captoora.studio."""
    test_dir = ROOT_DIR / "assets" / "mockups" / "test"
    html_path = test_dir / "Captoora_Email_Oscuro_Navidad2026.html"
    if not html_path.exists():
        raise FileNotFoundError("Ejecuta primero mockups --test para generar las plantillas HTML.")

    attachments = [
        test_dir / "Captoora_Dossier_Prueba_Navidad2026.pdf",
        test_dir / "Captoora_SmallBusiness_Dossier_2027.pdf",
        test_dir / "Captoora_SmallBusiness_AntesDespues_2027.png",
        test_dir / "Mockup_Prueba_OpcA_Navidad2026.png",
        test_dir / "Mockup_Prueba_OpcB_AccionLED_2026.png",
    ]
    existing_atts = [p for p in attachments if p.exists()]
    return send_email_via_zoho(
        to_email=to_email,
        subject="Captoora Studio · Autoprueba Navidad 2026 (-35%) + Dossier Small Business 2027",
        html_body=html_path.read_text(encoding="utf-8"),
        attachments=existing_atts,
        dry_run=dry_run,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Cliente SMTP Zoho Mail para chuy@captoora.studio")
    parser.add_argument("--status", action="store_true", help="Verifica estado de credenciales Zoho SMTP.")
    parser.add_argument("--send-test", action="store_true", help="Envía la autoprueba TEST-003 desde chuy@captoora.studio.")
    parser.add_argument("--to", default="ponchogf88@me.com", help="Correo destinatario de prueba.")
    parser.add_argument("--dry-run", action="store_true", help="Simula armado sin enviar por SMTP.")
    args = parser.parse_args()

    if args.status:
        print(json.dumps(get_smtp_status(), indent=2, ensure_ascii=False))
    elif args.send_test:
        print(json.dumps(send_self_test_email(to_email=args.to, dry_run=args.dry_run), indent=2, ensure_ascii=False))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
