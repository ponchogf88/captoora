"""Official Meta WhatsApp Cloud API client for zero-QR, zero-disconnect Captoora outreach."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx
from dotenv import load_dotenv

from .config import ROOT_DIR, append_agent_event, validate_client_copy


@dataclass(frozen=True)
class WhatsAppCloudConfig:
    """Configuration for Meta's official WhatsApp Cloud API (Graph API)."""

    token: str = ""
    phone_number_id: str = ""
    business_account_id: str = ""
    verify_token: str = ""
    api_version: str = "v21.0"
    public_base_url: str = ""

    @property
    def is_configured(self) -> bool:
        return bool(self.token.strip() and self.phone_number_id.strip())

    def missing_env_vars(self) -> list[str]:
        missing: list[str] = []
        if not self.token.strip():
            missing.append("WHATSAPP_CLOUD_TOKEN")
        if not self.phone_number_id.strip():
            missing.append("WHATSAPP_PHONE_NUMBER_ID")
        return missing


def load_cloud_config() -> WhatsAppCloudConfig:
    """Load Meta WhatsApp Cloud API settings from workspace .env and process env."""
    load_dotenv(ROOT_DIR / ".env", override=False)
    return WhatsAppCloudConfig(
        token=os.getenv("WHATSAPP_CLOUD_TOKEN", "").strip(),
        phone_number_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID", "").strip(),
        business_account_id=os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "").strip(),
        verify_token=os.getenv("WHATSAPP_VERIFY_TOKEN", "").strip(),
        api_version=os.getenv("WHATSAPP_API_VERSION", "v21.0").strip() or "v21.0",
        public_base_url=os.getenv("WHATSAPP_PUBLIC_BASE_URL", "").strip().rstrip("/"),
    )


def get_cloud_status() -> dict[str, Any]:
    """Return non-secret connection status for Meta Cloud API vs local fallback."""
    cfg = load_cloud_config()
    return {
        "configured": cfg.is_configured,
        "mode": "meta_cloud_api" if cfg.is_configured else "wa_me_or_desktop_fallback",
        "token_set": bool(cfg.token),
        "phone_number_id_set": bool(cfg.phone_number_id),
        "business_account_id_set": bool(cfg.business_account_id),
        "public_base_url_set": bool(cfg.public_base_url),
        "api_version": cfg.api_version,
        "missing_env": cfg.missing_env_vars(),
    }


def clean_phone_digits(phone: str) -> str:
    """Normalize a phone string into E.164 digits expected by Meta Cloud API."""
    digits = "".join(ch for ch in (phone or "") if ch.isdigit())
    if len(digits) < 10:
        raise ValueError(f"Número WhatsApp inválido (requiere mínimo 10 dígitos con lada): {phone!r}")
    if len(digits) == 10:
        return f"52{digits}"
    return digits


def _ensure_safe_copy(text: str | None) -> None:
    if not text:
        return
    violations = validate_client_copy(text)
    if violations:
        raise ValueError("Texto bloqueado por guardrail: " + " | ".join(violations))


def build_text_payload(to_phone: str, body: str, *, preview_url: bool = True) -> dict[str, Any]:
    """Build a Meta Cloud API plain-text message payload (within 24h session window)."""
    _ensure_safe_copy(body)
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": clean_phone_digits(to_phone),
        "type": "text",
        "text": {"preview_url": preview_url, "body": body},
    }


def build_document_payload(
    to_phone: str,
    document_url: str,
    filename: str,
    *,
    caption: str | None = None,
) -> dict[str, Any]:
    """Build a Meta Cloud API PDF/document payload."""
    _ensure_safe_copy(caption)
    doc_obj: dict[str, Any] = {"link": document_url, "filename": filename}
    if caption:
        doc_obj["caption"] = caption
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": clean_phone_digits(to_phone),
        "type": "document",
        "document": doc_obj,
    }


def build_image_payload(
    to_phone: str,
    image_url: str,
    *,
    caption: str | None = None,
) -> dict[str, Any]:
    """Build a Meta Cloud API image payload."""
    _ensure_safe_copy(caption)
    img_obj: dict[str, Any] = {"link": image_url}
    if caption:
        img_obj["caption"] = caption
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": clean_phone_digits(to_phone),
        "type": "image",
        "image": img_obj,
    }


def build_template_payload(
    to_phone: str,
    template_name: str,
    language_code: str = "es_MX",
    *,
    header_document_url: str | None = None,
    header_document_filename: str | None = None,
    header_image_url: str | None = None,
    body_params: list[str] | None = None,
    button_url_params: list[str] | None = None,
) -> dict[str, Any]:
    """Build an official approved Meta template payload for proactive outbound triggers."""
    if body_params:
        for param in body_params:
            _ensure_safe_copy(param)
    if button_url_params:
        for param in button_url_params:
            _ensure_safe_copy(param)

    components: list[dict[str, Any]] = []
    if header_document_url:
        doc_param: dict[str, Any] = {"link": header_document_url}
        if header_document_filename:
            doc_param["filename"] = header_document_filename
        components.append(
            {
                "type": "header",
                "parameters": [{"type": "document", "document": doc_param}],
            }
        )
    elif header_image_url:
        components.append(
            {
                "type": "header",
                "parameters": [{"type": "image", "image": {"link": header_image_url}}],
            }
        )

    if body_params:
        components.append(
            {
                "type": "body",
                "parameters": [{"type": "text", "text": val} for val in body_params],
            }
        )

    if button_url_params:
        for idx, url_suffix in enumerate(button_url_params):
            components.append(
                {
                    "type": "button",
                    "sub_type": "url",
                    "index": str(idx),
                    "parameters": [{"type": "text", "text": url_suffix}],
                }
            )

    template_obj: dict[str, Any] = {
        "name": template_name,
        "language": {"code": language_code},
    }
    if components:
        template_obj["components"] = components

    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": clean_phone_digits(to_phone),
        "type": "template",
        "template": template_obj,
    }


def build_interactive_cta_url_payload(
    to_phone: str,
    body_text: str,
    button_text: str,
    button_url: str,
    *,
    header_text: str | None = None,
    footer_text: str | None = None,
) -> dict[str, Any]:
    """Build an interactive WhatsApp Cloud API CTA URL message (for active 24h conversations)."""
    for chunk in (body_text, button_text, header_text, footer_text):
        _ensure_safe_copy(chunk)

    interactive: dict[str, Any] = {
        "type": "cta_url",
        "body": {"text": body_text},
        "action": {
            "name": "cta_url",
            "parameters": {
                "display_text": button_text[:20],
                "url": button_url,
            },
        },
    }
    if header_text:
        interactive["header"] = {"type": "text", "text": header_text[:60]}
    if footer_text:
        interactive["footer"] = {"text": footer_text[:60]}

    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": clean_phone_digits(to_phone),
        "type": "interactive",
        "interactive": interactive,
    }


async def send_cloud_message(
    payload: dict[str, Any],
    *,
    config: WhatsAppCloudConfig | None = None,
    client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Send a validated payload to Meta Graph API without QR codes or phone tethering."""
    cfg = config or load_cloud_config()
    if not cfg.is_configured:
        missing = ", ".join(cfg.missing_env_vars())
        raise RuntimeError(f"WhatsApp Cloud API no configurado en .env (falta: {missing}).")

    endpoint = f"https://graph.facebook.com/{cfg.api_version}/{cfg.phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {cfg.token}",
        "Content-Type": "application/json",
    }

    owns_client = client is None
    active_client = client or httpx.AsyncClient(timeout=20.0)
    try:
        resp = await active_client.post(endpoint, headers=headers, json=payload)
        if resp.status_code >= 400:
            raise RuntimeError(f"Meta Graph API HTTP {resp.status_code}: {resp.text[:400]}")
        return resp.json()
    finally:
        if owns_client:
            await active_client.aclose()


async def dispatch_approval_via_cloud(
    item: dict[str, Any],
    *,
    config: WhatsAppCloudConfig | None = None,
    client: httpx.AsyncClient | None = None,
) -> dict[str, Any]:
    """Attempt live Meta Cloud API dispatch for an approved trigger item, or return clean fallback info."""
    cfg = config or load_cloud_config()
    draft_text = item.get("draft_text", "")
    phone = item.get("phone", "")
    _ensure_safe_copy(draft_text)

    if not phone:
        return {"dispatched": False, "mode": "no_phone", "reason": "item_missing_phone"}

    text_payload = build_text_payload(phone, draft_text, preview_url=True)
    if not cfg.is_configured:
        return {
            "dispatched": False,
            "mode": "wa_me_fallback",
            "reason": "missing_meta_cloud_credentials",
            "missing_env": cfg.missing_env_vars(),
            "ready_payload": text_payload,
            "wa_me_url": item.get("whatsapp_url", ""),
        }

    responses: list[dict[str, Any]] = []
    message_ids: list[str] = []

    res = await send_cloud_message(text_payload, config=cfg, client=client)
    responses.append(res)
    for msg in res.get("messages", []):
        if msg.get("id"):
            message_ids.append(msg["id"])

    if cfg.public_base_url:
        for att in item.get("attachments", []) or []:
            rel_path = str(att.get("path", "")).lstrip("/")
            if not rel_path:
                continue
            public_url = f"{cfg.public_base_url}/{rel_path}"
            att_type = att.get("type")
            label = att.get("label", "Captoora Studio")
            if att_type == "pdf":
                media_payload = build_document_payload(
                    phone,
                    public_url,
                    rel_path.split("/")[-1],
                    caption=label,
                )
            elif att_type == "image":
                media_payload = build_image_payload(phone, public_url, caption=label)
            else:
                continue
            media_res = await send_cloud_message(media_payload, config=cfg, client=client)
            responses.append(media_res)
            for msg in media_res.get("messages", []):
                if msg.get("id"):
                    message_ids.append(msg["id"])

    from .usage_tracker import record_whatsapp_dispatch

    record_whatsapp_dispatch(len(message_ids) or 1, mode="meta_cloud_api")

    append_agent_event(
        item.get("agent_id", "ventas_outreach"),
        f"Enviado por WhatsApp Cloud API: {item.get('id', 'MSG')}",
        f"Destino +{clean_phone_digits(phone)} · IDs: {', '.join(message_ids) or 'ok'}",
        target_agent=item.get("agent_id"),
        zone="trigger_gate",
        source="whatsapp_cloud_api",
    )
    return {
        "dispatched": True,
        "mode": "meta_cloud_api",
        "message_ids": message_ids,
        "responses": responses,
    }
