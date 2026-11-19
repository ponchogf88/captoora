"""Automated tests for Captoora Sports 7-Agent Architecture, Guardrails, and FastAPI Server."""

from __future__ import annotations

import asyncio
import json
import shutil
from datetime import datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from google.antigravity import types

from captoora_agents import config, orchestrator, safety_and_hooks, server, tools


@pytest.fixture()
def isolated_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Copy real JSON workspace files to tmp_path and redirect config.FILES."""
    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    real_data_dir = config.DATA_DIR
    mapping: dict[str, Path] = {}
    for key, src_path in config.FILES.items():
        if src_path.parent == real_data_dir:
            dst = data_dir / src_path.name
            if src_path.exists():
                shutil.copy2(src_path, dst)
            mapping[key] = dst
        else:
            mapping[key] = src_path
    for key, path in mapping.items():
        monkeypatch.setitem(config.FILES, key, path)
    return data_dir


def test_real_json_workspace_integrity():
    """Verify all pre-seeded workspace JSON files follow expected structure and copy rules."""
    roster = config.read_json(config.FILES["roster"])
    assert len(roster["agents"]) == 10
    assert [a["number"] for a in roster["agents"]] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    asana = config.read_json(config.FILES["asana"])
    started = datetime.fromisoformat(asana["sprint"]["started_at"])
    deadline = datetime.fromisoformat(asana["sprint"]["deadline_at"])
    assert deadline > started
    assert deadline.weekday() == 1
    assert deadline.hour == 12
    assert deadline.minute == 0
    assert asana["sprint"].get("target_deals_min") == 1
    assert asana["sprint"].get("target_deals_max") == 3
    assert len(asana["projects"]) == 5
    assert len(asana["tasks"]) >= 10

    approvals = config.read_json(config.FILES["approvals"])
    assert len(approvals["items"]) >= 6
    for item in approvals["items"]:
        if item.get("niche") != "Operación Interna":
            assert config.validate_client_copy(item["draft_text"]) == []

    accounting = config.read_json(config.FILES["accounting"])
    for pkg in accounting["packages_catalog"]:
        assert pkg["margin_pct"] >= 70.0


def test_validate_client_copy_guardrails():
    """Ensure 'IA' / 'presumir' are caught without false positives on Spanish words."""
    assert config.validate_client_copy("Hola club, usamos IA para editar sus fotos.") != []
    assert config.validate_client_copy("Con Inteligencia Artificial entregamos hoy.") != []
    assert config.validate_client_copy("Para presumir en redes sociales el torneo.") != []

    clean_text = (
        "Fotografía deportiva el mismo día para proyectar en redes sociales una imagen profesional "
        "al nivel de excelencia de su club y trofeos en acrílico óptico con luz LED cálida."
    )
    assert config.validate_client_copy(clean_text) == []


def test_financial_and_contract_tools(isolated_workspace: Path):
    """Verify package margin calculations and legal clause red-flag checks."""
    quote_raw = tools.calculate_package_financials("PKG-4", discount_pct=10.0)
    quote = json.loads(quote_raw)
    assert quote["final_price_mxn"] == 11250.0
    assert quote["advance_50_pct_mxn"] == 5625.0
    assert quote["healthy_margin_ok"] is True

    audit_raw = tools.audit_contract_clauses(
        "El club paga a 60 días con cesión total patrimoniales y morales, incluyendo acrílicos LED en 15 min."
    )
    audit = json.loads(audit_raw)
    assert len(audit["red_flags"]) == 3


def test_enqueue_human_trigger_and_hook_blocking(isolated_workspace: Path):
    """Verify enqueue_human_trigger and SDK pre_tool_guardrail enforce Human Approval & copy rules."""
    rejected = tools.enqueue_human_trigger(
        agent_id="ventas_outreach",
        target_name="Club Prueba",
        niche="Pádel & Raqueta",
        channel="WhatsApp Directo",
        draft_text="Usamos inteligencia artificial para que puedan presumir fotos.",
    )
    assert rejected.startswith("RECHAZADO POR GUARDRAIL")

    bad_call = types.ToolCall(
        name="enqueue_human_trigger",
        args={"agent_id": "ventas_outreach", "draft_text": "Fotos con IA para presumir.", "is_client_facing": True},
        id="tc-1",
    )
    hook_block = asyncio.run(safety_and_hooks.pre_tool_guardrail(bad_call))
    assert hook_block.allow is False

    clean_call = types.ToolCall(
        name="enqueue_human_trigger",
        args={
            "agent_id": "ventas_outreach",
            "draft_text": "Entrega el mismo día para proyectar una imagen profesional al nivel de excelencia de su club.",
            "is_client_facing": True,
        },
        id="tc-2",
    )
    hook_ok = asyncio.run(safety_and_hooks.pre_tool_guardrail(clean_call))
    assert hook_ok.allow is True

    ok_raw = tools.enqueue_human_trigger(
        agent_id="ventas_outreach",
        target_name="Club Test NL",
        niche="Pádel & Raqueta",
        channel="WhatsApp Directo",
        phone="52 81 0000 1111",
        draft_text="Hola Club Test NL, entrega el mismo día para proyectar imagen profesional.",
    )
    ok_res = json.loads(ok_raw)
    assert ok_res["status"] == "pending_trigger"
    queue = config.read_json(config.FILES["approvals"])
    assert queue["items"][0]["whatsapp_url"].startswith("https://wa.me/528100001111?text=")


def test_sdk_config_builds_seven_agents_and_blocks_shell():
    """Confirm Chief of Staff config registers all 9 single-job subagents (inc. Marky/Lupe/Conan) and blocks run_command."""
    cfg = orchestrator.build_agent_config("chief_of_staff")
    assert len(cfg.subagents) == 9
    sub_names = {s.name for s in cfg.subagents}
    assert {"marky_marketing", "lupe_social", "conan_content"}.issubset(sub_names)
    assert "run_command" in (cfg.capabilities.disabled_tools or [])
    for sub in cfg.subagents:
        assert "run_command" in (sub.capabilities.disabled_tools or [])


def test_fastapi_endpoints_lifecycle(isolated_workspace: Path):
    """Test FastAPI workspace loading, Sprint UI serving, Asana task creation/update, and Last Trigger decisions."""
    client = TestClient(server.app)

    root_redir = client.get("/", follow_redirects=False)
    assert root_redir.status_code in (302, 307)
    assert root_redir.headers["location"] == "/dashboard/index.html#sprint-martes"

    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    ws = client.get("/api/workspace")
    assert ws.status_code == 200
    body = ws.json()
    assert body["server_online"] is True
    assert "whatsapp_cloud" in body and "mode" in body["whatsapp_cloud"]
    assert len(body["roster"]["agents"]) == 10
    assert "marketing_studio" in body

    dash = client.get("/dashboard/index.html")
    assert dash.status_code == 200
    for marker in ("tab-sprint-martes", "pomoTimeDigits", "visualBedReadyList", "top10LeadsContainer"):
        assert marker in dash.text

    playbook = client.get("/docs/meta_business_ai_agent_playbook.md")
    assert playbook.status_code == 200
    assert "captoora.studio/sports" in playbook.text

    created = client.post(
        "/api/tasks",
        json={
            "project_id": "proj_sprint_padel",
            "title": "Confirmar horario con Cuatro Padel",
            "assigned_agent": "ventas_outreach",
            "priority": "Crítica",
            "due_label": "Hoy",
        },
    )
    assert created.status_code == 200
    new_task_id = created.json()["task"]["id"]

    patched = client.patch(f"/api/tasks/{new_task_id}", json={"status": "done", "deliverable_ref": "Confirmado"})
    assert patched.status_code == 200
    assert patched.json()["task"]["status"] == "done"

    blocked_decision = client.post(
        "/api/approvals/APR-001/decision",
        json={"decision": "approve", "edited_text": "Promo IA para presumir"},
    )
    assert blocked_decision.status_code == 400

    approved = client.post(
        "/api/approvals/APR-001/decision",
        json={"decision": "approve"},
    )
    assert approved.status_code == 200
    assert approved.json()["item"]["status"] == "approved"


def test_mockup_spec_guardrails_and_test_assets():
    """Verify MockupSpec rejects forbidden words/old years and self-test bundle files exist."""
    from captoora_agents import mockups

    with pytest.raises(ValueError, match="2026"):
        mockups.validate_mockup_spec(
            mockups.MockupSpec(
                club_name="Cuatro Padel",
                tournament_name="Torneo del Pavo",
                season_label="NAVIDAD 2024",
                year="2024",
            )
        )

    with pytest.raises(ValueError, match="prohibidos"):
        mockups.validate_mockup_spec(
            mockups.MockupSpec(
                club_name="Cuatro Padel",
                tournament_name="Torneo con IA para presumir 2026",
            )
        )

    clean = mockups.MockupSpec(club_name="Cuatro Padel", tournament_name="Torneo del Pavo")
    mockups.validate_mockup_spec(clean)

    opt_b_html = mockups._build_option_b_html(clean)
    assert "captoora.studio/sports" in opt_b_html
    assert "galeria.captoora.studio" in opt_b_html

    test_dir = config.ROOT_DIR / "assets" / "mockups" / "test"
    for filename in (
        "Mockup_Prueba_OpcA_Navidad2026.png",
        "Mockup_Prueba_OpcB_AccionLED_2026.png",
        "Captoora_Dossier_Prueba_Navidad2026.pdf",
        "Captoora_Email_Oscuro_Navidad2026.html",
        "Captoora_Email_Claro_Navidad2026.html",
        "Captoora_Firma_Horizontal_2026.html",
    ):
        asset_path = test_dir / filename
        assert asset_path.exists()
        assert asset_path.stat().st_size > 2_000

    for html_name in (
        "Captoora_Email_Oscuro_Navidad2026.html",
        "Captoora_Email_Claro_Navidad2026.html",
        "Captoora_Firma_Horizontal_2026.html",
    ):
        html_text = (test_dir / html_name).read_text(encoding="utf-8")
        assert config.validate_client_copy(html_text) == []
        assert "#c6ff00" in html_text.lower()
        assert "chuy@captoora.studio" in html_text
        assert "https://captoora.studio/sports" in html_text
        assert "galeria.captoora.studio" in html_text
        assert "Jesús Gutiérrez" in html_text


def test_whatsapp_cloud_payload_and_mock_dispatch(isolated_workspace):
    """Verify Meta Cloud API payload construction, guardrail enforcement, and zero-QR transport."""
    import httpx
    from captoora_agents import whatsapp_cloud

    with pytest.raises(ValueError, match="guardrail"):
        whatsapp_cloud.build_text_payload("8130516527", "Automatizado con IA para presumir")

    with pytest.raises(ValueError, match="guardrail"):
        whatsapp_cloud.build_interactive_cta_url_payload(
            "8130516527",
            body_text="Editamos con Inteligencia Artificial",
            button_text="Ver portafolio",
            button_url="https://captoora.studio/sports",
        )

    payload = whatsapp_cloud.build_template_payload(
        "81 3051 6527",
        "captoora_navidad_2026",
        header_document_url="https://captoora.studio/dossier.pdf",
        header_document_filename="Captoora_Dossier.pdf",
        body_params=["Cuatro Padel", "Torneo del Pavo"],
        button_url_params=["cuatro-padel-2026"],
    )
    assert payload["to"] == "528130516527"
    assert payload["template"]["name"] == "captoora_navidad_2026"
    assert payload["template"]["components"][0]["parameters"][0]["type"] == "document"
    assert payload["template"]["components"][-1]["type"] == "button"
    assert payload["template"]["components"][-1]["sub_type"] == "url"
    assert payload["template"]["components"][-1]["parameters"][0]["text"] == "cuatro-padel-2026"

    cta_payload = whatsapp_cloud.build_interactive_cta_url_payload(
        "81 3051 6527",
        body_text="Preparamos la vista previa de Cuatro Padel con entrega el mismo día y trofeos LED.",
        button_text="Ver Portafolio",
        button_url="https://captoora.studio/sports",
        header_text="Captoora Sports 2026",
        footer_text="San Jerónimo · Monterrey",
    )
    assert cta_payload["type"] == "interactive"
    assert cta_payload["interactive"]["type"] == "cta_url"
    assert cta_payload["interactive"]["action"]["parameters"]["url"] == "https://captoora.studio/sports"

    seen_requests: list[tuple[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_requests.append((str(request.url), request.headers.get("authorization", "")))
        return httpx.Response(200, json={"messaging_product": "whatsapp", "messages": [{"id": "wamid.TEST123"}]})

    async def _run():
        cfg = whatsapp_cloud.WhatsAppCloudConfig(
            token="test_token",
            phone_number_id="10987654321",
            public_base_url="https://hub.captoora.studio",
        )
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport) as async_client:
            return await whatsapp_cloud.dispatch_approval_via_cloud(
                {
                    "id": "TEST-001",
                    "agent_id": "ventas_outreach",
                    "phone": "528130516527",
                    "draft_text": "Hola 👋, prueba directa Captoora Studio 🎾",
                    "attachments": [
                        {
                            "type": "pdf",
                            "label": "Dossier 1 Hoja",
                            "path": "assets/mockups/test/Captoora_Dossier_Prueba_Navidad2026.pdf",
                        }
                    ],
                },
                config=cfg,
                client=async_client,
            )

    res = asyncio.run(_run())
    assert res["dispatched"] is True
    assert res["mode"] == "meta_cloud_api"
    assert len(res["message_ids"]) == 2
    assert seen_requests[0][0] == "https://graph.facebook.com/v21.0/10987654321/messages"
    assert seen_requests[0][1] == "Bearer test_token"

    api_client = TestClient(server.app)
    wa_status = api_client.get("/api/whatsapp/status")
    assert wa_status.status_code == 200
    assert "mode" in wa_status.json()
    assert (config.ROOT_DIR / ".env.example").exists()


def test_modular_35_biogen_and_smb_pricing(isolated_workspace: Path):
    """Verify -35% seasonal pricing, deferred LED split, Biogen Beta, and Small Business 2027 math."""
    opt1 = json.loads(tools.calculate_package_financials("OPT-DIGITAL", discount_pct=35.0, niche="padel_gym"))
    assert opt1["list_price_mxn"] == 4900.0
    assert opt1["final_price_mxn"] == 3185.0
    assert opt1["healthy_margin_ok"] is True

    opt3 = json.loads(
        tools.calculate_package_financials(
            "OPT-FULL-LED", discount_pct=35.0, split_physical_later=True, niche="padel_gym"
        )
    )
    assert opt3["list_price_mxn"] == 11500.0
    assert opt3["final_price_mxn"] == 7475.0
    assert opt3["split_physical_later"] is True
    assert opt3["phase_1_digital_mxn"] == 3835.0
    assert opt3["phase_2_physical_mxn"] == 3640.0

    biogen_3 = json.loads(tools.calculate_package_financials("BIOGEN-3M", discount_pct=35.0))
    assert biogen_3["monthly_mxn"] == 1267.5
    assert biogen_3["months"] == 3
    assert biogen_3["healthy_margin_ok"] is True

    biogen_60 = json.loads(tools.calculate_package_financials("BIOGEN-60M", discount_pct=35.0))
    assert biogen_60["monthly_mxn"] == 747.5
    assert biogen_60["months"] == 60
    assert biogen_60["healthy_margin_ok"] is True

    smb_total = json.loads(tools.calculate_package_financials("SMB-TOTAL", discount_pct=35.0))
    assert smb_total["list_price_mxn"] == 10600.0
    assert smb_total["final_price_mxn"] == 6890.0
    assert smb_total["healthy_margin_ok"] is True

    smb_2027 = json.loads(tools.calculate_package_financials("SMB-SUITE-2027", discount_pct=35.0, split_physical_later=True))
    assert smb_2027["final_price_mxn"] == 10400.0
    assert smb_2027["phase_1_digital_mxn"] == 6890.0
    assert smb_2027["phase_2_physical_mxn"] == 3510.0


def test_usage_semaphore_and_gmaps_small_business_endpoints(isolated_workspace: Path):
    """Verify /api/usage semaphore controls, Google Maps audit index guardrails, and SMB Before/After PDF generation."""
    from captoora_agents import gmaps_auditor

    client = TestClient(server.app)

    usage = client.get("/api/usage")
    assert usage.status_code == 200
    u_data = usage.json()
    assert u_data["semaphore"] in {"verde", "ambar", "rojo"}
    assert "whatsapp_quota" in u_data

    toggled = client.post("/api/usage/limits", json={"dry_run_preferred": True, "daily_token_budget": 300000})
    assert toggled.status_code == 200
    assert toggled.json()["usage_telemetry"]["limits"]["dry_run_preferred"] is True
    assert toggled.json()["usage_telemetry"]["tokens"]["budget"] == 300000

    audits_res = client.get("/api/gmaps-audits")
    assert audits_res.status_code == 200
    audits_json = audits_res.json()
    assert audits_json["total_leads"] >= 138
    assert audits_json["total_audited"] >= 60
    assert audits_json["deficient_count"] >= 20

    for item in audits_json["audits"][:25]:
        for mode_text in (item.get("outreach_modes") or {}).values():
            assert config.validate_client_copy(mode_text) == []

    # Verify Small Business Before/After + PDF generation and multi-mode queue enqueuing
    sample_slug = audits_json["audits"][0]["slug"]
    gen_res = client.post(
        "/api/small-business/generate-audit",
        json={"slug": sample_slug, "enqueue_mode": "all", "after_hero_variant": "studio"},
    )
    assert gen_res.status_code == 200
    gen_body = gen_res.json()
    assert len(gen_body["enqueued_ids"]) == 3
    ba_abs = config.ROOT_DIR / gen_body["before_after_path"]
    pdf_abs = config.ROOT_DIR / gen_body["dossier_pdf_path"]
    assert ba_abs.exists() and ba_abs.stat().st_size > 10_000
    assert pdf_abs.exists() and pdf_abs.stat().st_size > 10_000

    # Verify dashboard HTML includes Module 9 elements cleanly
    dash = client.get("/dashboard/index.html")
    assert dash.status_code == 200
    for marker in (
        "tab-small-business",
        "tokenUsageBar",
        "parallelTracksSection",
        "modular35MatrixSection",
        "biogenBetaSection",
        "smbAuditDialog",
    ):
        assert marker in dash.text

    # Smoke-check gmaps_auditor Street View detection helper
    sv_check = gmaps_auditor.analyze_business_profile(
        {
            "nombre": "Consultorio Demo StreetView",
            "categoria": "Clínica médica",
            "nicho": "Clínicas & Consultorios",
            "image_url": "https://streetviewpixels-pa.googleapis.com/v1/thumbnail?panoid=abc",
            "images_count": 0,
            "claim_this_business": True,
        }
    )
    assert sv_check["has_streetview_cover"] is True
    assert "CARRITO STREET VIEW" in sv_check["audit_flags"]
    assert "0 FOTOS" in sv_check["audit_flags"]
    assert "SIN RECLAMAR" in sv_check["audit_flags"]


def test_marketing_trio_marky_lupe_conan_zero_grokbot_and_subscriptions(isolated_workspace: Path, monkeypatch: pytest.MonkeyPatch):
    """Verify Marky/Lupe/Conan run with 0 external quotas, guardrails hold, and all Marketing Studio APIs work."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    client = TestClient(server.app)

    # Zero-token execution for Marky, Conan, and Lupe without GEMINI_API_KEY
    res_marky = asyncio.run(orchestrator.run_agent_mission("marky_marketing"))
    assert res_marky["mode"] == "local_zero_token"

    res_conan = asyncio.run(orchestrator.run_agent_mission("conan_content", "Grabar lote OpusClip Pro hoy"))
    assert res_conan["mode"] == "local_zero_token"
    assert res_conan["brief"]["for_agent"] == "lupe_social"

    res_lupe = asyncio.run(orchestrator.run_agent_mission("lupe_social"))
    assert res_lupe["mode"] == "local_zero_token"
    assert res_lupe["enqueued_id"].startswith("LUPE-")

    # Guardrail must block prohibited AI / 'presumir' copy in prepare_lupe_social_post tool & HTTP API
    blocked_tool = tools.prepare_lupe_social_post("TikTok", "Prueba mala", "Hecho con IA para presumir fotos.")
    assert blocked_tool.startswith("RECHAZADO POR GUARDRAIL")

    bad_hook = asyncio.run(
        safety_and_hooks.pre_tool_guardrail(
            types.ToolCall(
                name="prepare_lupe_social_post",
                args={"platform": "TikTok", "draft_text": "Video con inteligencia artificial."},
                id="tc-lupe-bad",
            )
        )
    )
    assert bad_hook.allow is False

    mk_res = client.get("/api/marketing-studio")
    assert mk_res.status_code == 200
    mk = mk_res.json()
    sub_names = " ".join(s["name"] for s in mk["subscriptions_stack"])
    assert "OpusClip Pro" in sub_names
    assert "Google AI Pro #1" in sub_names
    assert "Google AI Pro #2" in sub_names
    assert "Captions App" in sub_names
    assert "Canva" in sub_names
    assert "Aftershoot" in sub_names
    assert "Meta Business Suite" in sub_names
    assert "Grokbot" not in sub_names or "ELIMINADO" in mk["grokbot_status"]

    for post in mk["content_calendar"]:
        assert config.validate_client_copy(f"{post['caption']}\n{post.get('hashtags', '')}") == []
    for dm in mk["lupe_dm_playbook"]:
        assert config.validate_client_copy(dm["reply_text"]) == []

    # HTTP workflow: regenerate plan, enqueue Lupe post, reject bad caption, assign Conan brief, ingest Muse note
    regen = client.post("/api/marketing-studio/generate-plan", json={"focus": "opusclip", "week_label": "Sprint Rescate OpusClip"})
    assert regen.status_code == 200
    assert regen.json()["marketing_studio"]["active_week_label"] == "Sprint Rescate OpusClip"

    bad_http = client.post("/api/marketing-studio/enqueue-post", json={"post_id": "POST-01", "custom_caption": "Hecho con IA"})
    assert bad_http.status_code == 400

    good_http = client.post("/api/marketing-studio/enqueue-post", json={"post_id": "POST-02"})
    assert good_http.status_code == 200
    assert good_http.json()["enqueued_item"]["id"] == "LUPE-02"

    muse_res = client.post(
        "/api/marketing-studio/muse-ingest",
        json={"notes_text": "Grabar clínica Obispado mañana para OpusClip Pro", "target_agent": "conan_content"},
    )
    assert muse_res.status_code == 200
    assert muse_res.json()["task"]["assigned_agent"] == "conan_content"

    dash = client.get("/dashboard/index.html")
    assert dash.status_code == 200
    for marker in ("tab-marketing-hq", "mkhqOpusClipSection", "mkhqGoogleProSyncCard", "mkhqMuseBridgeCard", "mkhqCalendarGrid"):
        assert marker in dash.text


def test_per_prospect_niche_personalization_and_no_cross_club_leakage(isolated_workspace: Path):
    """Ensure every prospect gets niche-authentic visuals/copy, club logos render cleanly, and no cross-club boilerplate leaks."""
    from captoora_agents import gmaps_auditor, mockups

    summary = gmaps_auditor.sync_audit_index_from_sources()
    assert summary["total_leads"] == 141
    assert summary["total_audited"] == 141

    by_slug = {a["slug"]: a for a in summary["audits"]}

    # 1. Fitness gym gets fitness hero + TotalPass + Biogen + 11:11 logo, NEVER padel court photo
    gym_rec = by_slug["11_11_fitness_top_obispado"]
    gym_spec = mockups.build_small_business_spec_from_record(gym_rec)
    assert gym_spec.after_hero_path.name == "niche_fitness_gym.jpg"
    assert gym_spec.prospect_logo_path and gym_spec.prospect_logo_path.name == "eleven_fitness.png"
    gym_html = mockups._build_before_after_audit_html(gym_spec)
    assert "niche_fitness_gym" not in gym_html  # encoded as data URI, verify pillars/tag instead
    assert "MAPS + TOTALPASS + BIOGEN" in gym_html
    assert "Torneo del Pavo" not in gym_html

    # 2. Kindergarten gets Montessori hero + safe admissions copy, NEVER football/Biogen/TotalPass/Cuatro Padel
    kinder_rec = by_slug["reino_encantado"]
    kinder_spec = mockups.build_small_business_spec_from_record(kinder_rec)
    assert kinder_spec.after_hero_path.name == "niche_kinder_montessori.jpg"
    kinder_html = mockups._build_before_after_audit_html(kinder_spec)
    for forbidden in ("Biogen", "TotalPass", "Cuatro Padel", "Torneo del Pavo"):
        assert forbidden.lower() not in kinder_html.lower()
    assert "CONFIANZA FAMILIAR" in kinder_html

    # 3. Dental clinic gets clinic hero + medical trust pillars, NEVER TotalPass/Biogen/football
    clinic_rec = by_slug["dr_cesar_garza_ponce_consultorio_dental"]
    clinic_spec = mockups.build_small_business_spec_from_record(clinic_rec)
    assert clinic_spec.after_hero_path.name == "niche_clinica_dental.jpg"
    clinic_html = mockups._build_before_after_audit_html(clinic_spec)
    for forbidden in ("Biogen", "TotalPass", "Cuatro Padel"):
        assert forbidden.lower() not in clinic_html.lower()
    assert "CONFIANZA MÉDICA" in clinic_html

    # 4. Dance academy Christmas mockup uses dance acrylic blank + dance stage hero + real logo + White-Glove card
    dance_rec = by_slug["the_movement_dance_project"]
    dance_spec = mockups.build_club_mockup_spec(dance_rec)
    assert dance_spec.plate_style == "dance"
    assert dance_spec.acrylic_base_path == mockups.DANCE_ACRYLIC_BLANK_PATH
    assert dance_spec.hero_photo_path.name == "niche_danza_studio.jpg"
    assert dance_spec.club_logo_path and dance_spec.club_logo_path.name == "the_movement.png"
    assert dance_spec.extra_card and "WHITE-GLOVE" in dance_spec.extra_card[0]
    dance_a_html = mockups._build_option_a_html(dance_spec)
    assert "THE MOVEMENT DANCE PROJECT" in dance_a_html
    assert "CUATRO PADEL" not in dance_a_html.upper()

    # 5. All 141 specs validate cleanly against client copy guardrails and unique slugs
    for rec in summary["audits"]:
        spec = mockups.build_small_business_spec_from_record(rec)
        mockups.validate_smb_spec(spec)
        for mode_txt in (rec.get("outreach_modes") or {}).values():
            assert config.validate_client_copy(mode_txt) == []


def test_zoho_smtp_status_and_dry_run_guardrail(isolated_workspace: Path, monkeypatch: pytest.MonkeyPatch):
    """Verify chuy@captoora.studio Zoho SMTP config reporting, dry-run bundle packing, and copy guardrail."""
    from captoora_agents import email_sender

    monkeypatch.setenv("SMTP_PASS", "")
    client = TestClient(server.app)

    status_res = client.get("/api/email/status")
    assert status_res.status_code == 200
    sdata = status_res.json()
    assert sdata["provider"] == "zoho_smtp"
    assert sdata["sender"] == "chuy@captoora.studio"
    assert sdata["host"] == "smtp.zoho.com"

    dry_res = client.post("/api/email/send-test", json={"to_email": "ponchogf88@me.com", "dry_run": True})
    assert dry_res.status_code == 200
    ddata = dry_res.json()
    assert ddata["mode"] == "dry_run"
    assert ddata["from"] == "chuy@captoora.studio"
    assert "Captoora_Dossier_Prueba_Navidad2026.pdf" in ddata["attachments"]

    with pytest.raises(ValueError, match="guardrail"):
        email_sender.send_email_via_zoho(
            to_email="ponchogf88@me.com",
            subject="Prueba con IA para presumir fotos",
            html_body="<p>Contenido bloqueado</p>",
            dry_run=True,
        )


def test_puerto_vallarta_zone_separation_and_origin_neutral_copy(tmp_path: Path, isolated_workspace: Path):
    """Ensure PV Zona Romántica and Zona Hotelera separate cleanly, use hospitality/retail profiles, and strip MTY/San Jerónimo copy."""
    from captoora_agents import gmaps_auditor, mockups
    from scripts.scrape_puerto_vallarta import classify_pv_zone

    rom_item = {
        "title": "Beach Club Olas Demo",
        "categoryName": "Beach club",
        "address": "Malecón / Olas Altas 169, Zona Romántica, Emiliano Zapata, 48380 Puerto Vallarta, Jal., México",
        "location": {"lat": 20.6001, "lng": -105.2385},
        "imagesCount": 3,
        "claimThisBusiness": True,
        "placeId": "pid_pv_rom_1",
    }
    hot_item = {
        "title": "Resort Las Glorias Demo",
        "categoryName": "Hotel resort",
        "address": "Blvd. Francisco Medina Ascencio Km 2.5, Zona Hotelera Norte, Las Glorias, 48333 Puerto Vallarta, Jal., México",
        "location": {"lat": 20.6378, "lng": -105.2321},
        "imageUrl": "https://streetviewpixels-pa.googleapis.com/v1/thumbnail?panoid=pv1",
        "imagesCount": 0,
        "placeId": "pid_pv_hot_1",
    }
    out_item = {
        "title": "Hotel Nuevo Vallarta Fuera",
        "categoryName": "Hotel",
        "address": "Paseo de los Cocoteros 50, Nuevo Vallarta, Nayarit, México",
        "location": {"lat": 20.7010, "lng": -105.2950},
    }

    assert classify_pv_zone(rom_item)[0] == "zona_romantica"
    assert classify_pv_zone(hot_item)[0] == "zona_hotelera"
    assert classify_pv_zone(out_item)[0] is None

    # Parameterized sync on PV temp dirs must leave Nuevo León's 141 leads completely untouched
    rom_raw = tmp_path / "rom_raw.json"
    rom_leads = tmp_path / "rom_leads.json"
    rom_audits = tmp_path / "rom_audits.json"
    rom_shots = tmp_path / "rom_shots"
    rom_raw.write_text(json.dumps([rom_item], ensure_ascii=False), encoding="utf-8")

    pv_summary = gmaps_auditor.sync_audit_index_from_sources(
        raw_path=rom_raw,
        leads_path=rom_leads,
        audits_path=rom_audits,
        screenshots_dir=rom_shots,
        screenshots_rel_prefix="assets/gmaps_audits/puerto_vallarta/zona_romantica",
    )
    assert pv_summary["total_leads"] == 1
    rec = pv_summary["audits"][0]
    assert rec["municipio"] == "Puerto Vallarta"
    assert rec["zona"] == "Zona Romántica"
    assert rec["nicho"] == "Hoteles, Resorts & Beach Clubs"

    spec = mockups.build_small_business_spec_from_record(rec)
    mockups.validate_smb_spec(spec)
    forbidden = ("san jerónimo", "san jeronimo", "monterrey", "mty", "spgg")
    for text in [spec.address_line, spec.sla_footer_note, spec.hero_intro, *rec["outreach_modes"].values()]:
        assert config.validate_client_copy(text) == []
        for term in forbidden:
            assert term not in text.lower()

    retail_profile = mockups.resolve_niche_profile("Tiendas, Boutiques & Comercios", name="Boutique Olas", category="Tienda de ropa")
    assert retail_profile.niche_key == "Tiendas, Boutiques & Comercios"

    # Confirm Nuevo León remains at 141 leads
    nl_summary = gmaps_auditor.sync_audit_index_from_sources()
    assert nl_summary["total_leads"] == 141


def test_pv_events_suppliers_three_zones_and_copy_guardrails(isolated_workspace: Path):
    """Verify strict 3-zone PV event separation (ZR / ZH / Centro-Bahía), Nayarit/Vidanta exclusion, supplier scoring, and copy guardrails."""
    from captoora_agents import gmaps_auditor
    from scripts.scrape_pv_events_and_influencers import (
        FORBIDDEN_ORIGIN_TERMS,
        _build_event_outreach_script,
        _build_influencers_intelligence,
        classify_event_zone,
    )
    from scripts.scrape_pv_suppliers import classify_pv_corridor, process_suppliers

    # 1. Strict 3-zone event routing inside PV & Vidanta/Nayarit rejection
    assert classify_event_zone("Brawny Bear Weekend", "Mantamar Beach Club, Zona Romántica")[0] == "zona_romantica"
    assert classify_event_zone("Torneo 233", "Padel 233, Guadalupe Victoria, Fluvial")[0] == "zona_hotelera"
    assert classify_event_zone("Candlelight Navideño", "Teatro Vallarta, Col. 5 de Diciembre")[0] == "centro_y_bahia"
    assert classify_event_zone("Majahuitas Beach Party", "Playa Majahuitas, Bahía de Banderas salida PV")[0] == "centro_y_bahia"
    assert classify_event_zone("LUDÕ Cirque", "VidantaWorld Nuevo Vallarta, Nayarit")[0] is None
    assert classify_event_zone("Picnic Bajo las Parotas", "Tepic, Nayarit")[0] is None

    # 2. Supplier street collision guard + Nayarit exclusion
    assert classify_pv_corridor("Emiliano Zapata 326, Valentín Gómez Farías, 48320 Puerto Vallarta, Jal.", lat=20.6294) != "Zona Romántica"
    assert classify_pv_corridor("Olas Altas 500, Zona Romántica, 48380 Puerto Vallarta, Jal.", lat=20.598) == "Zona Romántica"

    sample_raw = [
        {
            "title": "Taller Láser Demo PV",
            "categoryName": "Servicio de corte láser",
            "address": "Av. Francisco Villa 1200, Versalles, 48310 Puerto Vallarta, Jal.",
            "phone": "+52 322 100 2000",
            "website": "https://tallerlaserdemo.com",
            "reviewsCount": 65,
            "totalScore": 4.8,
            "imagesCount": 24,
            "claimThisBusiness": False,
            "placeId": "sup_pv_1",
            "location": {"lat": 20.635, "lng": -105.225},
        },
        {
            "title": "Taller Bucerías Fuera",
            "categoryName": "Carpintero",
            "address": "Carretera Tepic 100, Bucerías, Nayarit",
            "placeId": "sup_nay_1",
        },
    ]
    sup_res = process_suppliers(sample_raw)
    assert sup_res["total_suppliers"] == 1
    assert sup_res["tier_a_count"] == 1
    assert len(sup_res["excluded_out_of_pv"]) == 1

    # 3. Validate all outreach scripts (event + influencer DM) for zero origin & zero IA/presumir leaks
    script = _build_event_outreach_script(
        titulo="Torneo 233",
        recinto="Padel 233",
        fecha="03 – 06 Dic 2026",
        zona_label="Zona Hotelera",
        categoria="Deportes / Torneo de Pádel",
        invitados=["Jugadores PV"],
        cobertura_status="Abierta / Nicho Core Captoora",
    )
    assert config.validate_client_copy(script) == []
    for term in FORBIDDEN_ORIGIN_TERMS:
        assert term not in script.lower()

    inf_pack = _build_influencers_intelligence([])
    for inf in inf_pack["influencers_y_creadores_pv"]:
        dm = inf["guion_dm_captoora"]
        assert config.validate_client_copy(dm) == []
        for term in FORBIDDEN_ORIGIN_TERMS:
            assert term not in dm.lower()

    # 4. Validate real PV Phase 2 JSON deliverables generated in workspace root
    pv_real_root = Path(__file__).resolve().parent.parent / "dashboard" / "data" / "puerto_vallarta"
    for zfile in ("eventos_zona_romantica.json", "eventos_zona_hotelera.json", "eventos_centro_y_bahia.json"):
        zdata = json.loads((pv_real_root / zfile).read_text(encoding="utf-8"))
        assert zdata["total_events"] >= 10
        for ev in zdata["events"]:
            g = ev["guion_acercamiento_captoora"]
            assert config.validate_client_copy(g) == []
            for term in FORBIDDEN_ORIGIN_TERMS:
                assert term not in g.lower()

    # Confirm Nuevo León stays untouched at 141 leads
    assert gmaps_auditor.sync_audit_index_from_sources()["total_leads"] == 141


def test_pv_phase3_centro_bahia_web_prototypes_gbp_checklist_and_server(isolated_workspace: Path):
    """Verify 3-zone PV separation (ZR/ZH/Centro-Bahía), GBP checklists, Web Express HTML prototypes, and API preview."""
    from captoora_agents import gmaps_auditor, mockups
    from scripts.build_pv_zone_maps import FORBIDDEN_ORIGIN_TERMS
    from scripts.scrape_puerto_vallarta import classify_pv_zone

    # 1. Geographic boundary check between Zona Romántica, Centro/Bahía, and Zona Hotelera
    centro_item = {
        "title": "Bar Océano Demo",
        "categoryName": "Bar",
        "address": "Paseo Díaz Ordaz 538, Centro, 48300 Puerto Vallarta, Jal., México",
        "location": {"lat": 20.6114, "lng": -105.2345},
    }
    pitillal_out = {
        "title": "Negocio Pitillal Fuera",
        "categoryName": "Tienda",
        "address": "Centro Pitillal, 48290 Puerto Vallarta, Jal., México",
        "location": {"lat": 20.648, "lng": -105.211},
    }
    assert classify_pv_zone(centro_item)[0] == "centro_y_bahia"
    assert classify_pv_zone(pitillal_out)[0] is None

    # 2. Verify all 3 separated real PV datasets have zero place_id overlaps & 100% CDP captures
    repo_root = Path(__file__).resolve().parent.parent
    pv_root = repo_root / "dashboard" / "data" / "puerto_vallarta"
    zone_ids: dict[str, set[str]] = {}
    all_records: list[tuple[str, dict]] = []
    for zkey in ("zona_romantica", "zona_hotelera", "centro_y_bahia"):
        idx = json.loads((pv_root / zkey / "gmaps_audits.json").read_text(encoding="utf-8"))
        audits = idx["audits"]
        assert len(audits) >= 40
        assert idx["captured_count"] == len(audits)
        zone_ids[zkey] = {a["place_id"] for a in audits if a.get("place_id")}
        all_records.extend((zkey, a) for a in audits)

    assert zone_ids["zona_romantica"].isdisjoint(zone_ids["zona_hotelera"])
    assert zone_ids["zona_romantica"].isdisjoint(zone_ids["centro_y_bahia"])
    assert zone_ids["zona_hotelera"].isdisjoint(zone_ids["centro_y_bahia"])

    # 3. Verify niche-diverse Web Express prototypes + tailored GBP checklist + zero origin/copy leaks
    hotel_rec = {
        "slug": "hotel_olas_demo",
        "nombre": "Hotel Olas Demo",
        "categoria": "Hotel",
        "nicho": "Hoteles, Resorts & Beach Clubs",
        "municipio": "Puerto Vallarta",
        "zona": "Zona Hotelera",
        "subzona": "Las Glorias",
        "direccion": "Av. Francisco Medina Ascencio 200, Las Glorias, 48333 Puerto Vallarta, Jal.",
        "telefono": "+52 322 200 1122",
        "sitio_web": "",
        "audit_flags": ["SIN RECLAMAR", "SIN SITIO WEB", "CARRITO STREET VIEW"],
        "audit_score": 78,
        "rating": 4.4,
        "resenas": 32,
        "images_count": 3,
    }
    hotel_chk = mockups.build_gbp_optimization_checklist(hotel_rec)
    assert hotel_chk["website_status"] == "sin_web"
    assert hotel_chk["priority_level"] == "Crítica"
    assert hotel_chk["urgent_count"] >= 3
    hotel_html = mockups.build_smb_landing_prototype_html(hotel_rec, gbp_checklist=hotel_chk)
    assert "pv_hospitality_resort.jpg" in hotel_html
    assert "Jesús Gutiérrez" in hotel_html
    assert "$3,900 MXN" in hotel_html
    assert config.validate_client_copy(mockups._strip_data_uris(hotel_html)) == []
    for term in FORBIDDEN_ORIGIN_TERMS:
        assert term not in hotel_html.lower()

    cafe_rec = {
        **hotel_rec,
        "slug": "cafe_malecon_demo",
        "nombre": "Café Malecón Demo",
        "categoria": "Cafetería",
        "nicho": "Restaurantes & Cafés Boutique",
        "sitio_web": "https://www.instagram.com/cafemaleconpv",
        "audit_flags": ["RED PERSONAL EN RIESGO"],
        "audit_score": 25,
    }
    cafe_chk = mockups.build_gbp_optimization_checklist(cafe_rec)
    assert cafe_chk["website_status"] == "solo_red_social"
    cafe_html = mockups.build_smb_landing_prototype_html(cafe_rec, gbp_checklist=cafe_chk)
    assert "pv_gastronomy_terrace.jpg" in cafe_html
    assert "niche_cafe_restaurante" not in cafe_html

    # 4. Verify generated static 3-zone HTML hubs & demo files exist and have no raw syntax issues
    docs_root = repo_root / "docs"
    for zkey, fname in (
        ("zona_romantica", "puerto_vallarta_zona_romantica.html"),
        ("zona_hotelera", "puerto_vallarta_zona_hotelera.html"),
        ("centro_y_bahia", "puerto_vallarta_centro_bahia.html"),
    ):
        hub_text = (docs_root / fname).read_text(encoding="utf-8")
        assert "demos_pv/" in hub_text
        assert "Checklist GBP" in hub_text
        assert ".join('\n')" not in hub_text

    for zkey, rec in all_records:
        demo_file = docs_root / "demos_pv" / zkey / f"{rec['slug']}.html"
        assert demo_file.exists(), f"Falta prototipo web: {demo_file}"

    # 5. Verify FastAPI GET /api/small-business/prototype/{slug} endpoint
    client = TestClient(server.app)
    api_json = client.get("/api/small-business/prototype/11_11_fitness_top_obispado?output=json")
    assert api_json.status_code == 200
    assert api_json.json()["gbp_checklist"]["business_name"]
    api_html = client.get("/api/small-business/prototype/11_11_fitness_top_obispado")
    assert api_html.status_code == 200
    assert "Jesús Gutiérrez" in api_html.text

    # 6. Confirm Nuevo León stays untouched at 141 leads
    assert gmaps_auditor.sync_audit_index_from_sources()["total_leads"] == 141


def test_phase4_growth_geo_accountant_and_scheduler(isolated_workspace: Path, monkeypatch: pytest.MonkeyPatch):
    """Verify SEO/AEO root assets, zero neighborhood brag, 141-pin Monterrey map + TSP, PFAE 612 accountant $0-debt gate, and 24/7 scheduler."""
    from captoora_agents import geo_radar, growth_suite, scheduler

    repo_root = Path(__file__).resolve().parent.parent

    # 1. SEO & AEO technical assets + zero San Jerónimo brag in client copy
    for seo_file in ("robots.txt", "sitemap.xml", "llms.txt"):
        assert (repo_root / seo_file).exists(), f"Falta archivo SEO/AEO: {seo_file}"
    portal_html = (repo_root / "captoora_sports.html").read_text(encoding="utf-8")
    assert "application/ld+json" in portal_html
    assert '"ProfessionalService"' in portal_html
    assert '"FAQPage"' in portal_html
    assert "Colinas de San Jerónimo" not in portal_html[:1400]

    bad_copy = config.validate_client_copy("Estudio aquí en Colinas de San Jerónimo Monterrey #SanJeronimo")
    assert len(bad_copy) == 1
    assert config.validate_client_copy("Congelamiento 1/2000s Global Shutter y Halftime Blitz 15m en tu sede") == []

    # Verify gmaps_auditor & marketing_hub live generation stay free of neighborhood brag
    from captoora_agents import gmaps_auditor, marketing_hub

    audits_idx = gmaps_auditor.sync_audit_index_from_sources()
    sample_audit = audits_idx["audits"][0]
    for mode_val in sample_audit["outreach_modes"].values():
        assert config.validate_client_copy(mode_val) == []
    mk_state = marketing_hub.build_initial_marketing_state()
    for p in mk_state["content_calendar"]:
        assert config.validate_client_copy(f"{p['caption']} {p.get('hashtags','')}") == []
    for dm in mk_state["lupe_dm_playbook"]:
        assert config.validate_client_copy(dm["reply_text"]) == []

    client = TestClient(server.app)

    # 2. Geo-Radar 141 pins + TSP Multi-Stop Route Optimizer + Save
    geo_res = client.get("/api/geo/leads")
    assert geo_res.status_code == 200
    geo_data = geo_res.json()
    assert geo_data["total_pins"] == 141
    slugs = [p["slug"] for p in geo_data["pins"][:4]]

    opt_res = client.post("/api/geo/routes/optimize", json={"slugs": slugs})
    assert opt_res.status_code == 200
    opt_data = opt_res.json()
    assert opt_data["stops_count"] == 4
    assert opt_data["total_distance_km"] > 0
    assert "google.com/maps/dir/" in opt_data["google_maps_route_url"]
    assert [s["stop_number"] for s in opt_data["stops"]] == [1, 2, 3, 4]

    save_res = client.post("/api/geo/routes/save", json={"title": "Ruta Demo Colegios", "slugs": slugs[:3]})
    assert save_res.status_code == 200
    assert save_res.json()["route"]["id"] == "RUTA-001"

    # 3. Accountant PFAE 612 (GUFJ870801NA6) & Zero-Debt $0 Ads Gate
    acct_initial = client.get("/api/growth/accountant/summary").json()
    assert acct_initial["fiscal_profile"]["regime_code"] == "612"
    assert acct_initial["fiscal_profile"]["rfc"] == "GUFJ870801NA6"
    assert acct_initial["summary"]["paid_sales_count"] == 0
    assert acct_initial["summary"]["ads_unlocked"] is False
    assert acct_initial["summary"]["authorized_ads_budget_mxn"] == 0.0
    assert all(p["authorized_mxn"] == 0.0 for p in acct_initial["platform_allocations"])

    sale_res = client.post(
        "/api/growth/accountant/record-sale",
        json={
            "client_name": "Clínica Demo Obispado",
            "package_ref": "Maps Visual 2027",
            "amount_collected_mxn": 3900.0,
            "direct_cost_mxn": 0.0,
            "includes_iva": True,
            "client_is_persona_moral": False,
        },
    )
    assert sale_res.status_code == 200
    after_sale = sale_res.json()["accountant"]["summary"]
    assert after_sale["paid_sales_count"] == 1
    assert after_sale["iva_payable_sat_mxn"] > 0
    assert after_sale["isr_estimated_reserve_mxn"] > 0
    assert after_sale["free_net_profit_mxn"] > 0
    assert after_sale["ads_unlocked"] is True
    assert after_sale["authorized_ads_budget_mxn"] > 0

    audit_contract = client.post(
        "/api/growth/accountant/audit-contract",
        json={"contract_text": "Pago a 90 días a Persona Moral S.A. de C.V. con cesión total patrimonial."},
    )
    assert audit_contract.status_code == 200
    alerts_joined = " ".join(audit_contract.json()["alerts"])
    assert "FLUJO" in alerts_joined
    assert "612" in alerts_joined

    # 4. 7 Executive Engines + WhatsApp Web 1-Click + 24/7 Scheduler & Webhook auth
    clips_res = client.post("/api/growth/content/20-clips", json={"topic": "Clínicas con Street View en MTY"})
    assert clips_res.status_code == 200
    assert len(clips_res.json()["seo_and_clips"]["clips_20"]) == 20

    mail_res = client.post(
        "/api/growth/mail/send",
        json={"to_email": "demo@example.com", "prospect_name": "Clínica Demo", "dry_run": True},
    )
    assert mail_res.status_code == 200
    assert mail_res.json()["mode"] == "dry_run"
    assert mail_res.json()["sent"] is False

    cal_res = client.post(
        "/api/growth/calendly/link",
        json={"prospect_name": "Dra. Ana Demo", "event_type_id": "maps_audit_15"},
    )
    assert cal_res.status_code == 200
    assert "utm_source=captoora" in cal_res.json()["link"]["url"]

    wa_res = client.post(
        "/api/whatsapp/web-mark-sent",
        json={"slug": "clinica_demo", "nombre": "Clínica Demo", "phone": "528112345678"},
    )
    assert wa_res.status_code == 200
    assert wa_res.json()["supervisor"]["sent_today"] == 1

    # 24/7 Scheduler idempotent slot trigger (08:35 CST Friday -> runs 08_30_ceo once)
    test_dt = datetime(2026, 11, 20, 8, 35, tzinfo=config.MONTERREY_TZ)
    tick1 = scheduler.tick_scheduler(now_dt=test_dt)
    assert len(tick1["executed"]) == 1
    assert tick1["executed"][0]["slot_id"] == "08_30_ceo"
    tick2 = scheduler.tick_scheduler(now_dt=test_dt)
    assert tick2["executed"] == []

    monkeypatch.setenv("CAPTOORA_WEBHOOK_SECRET", "top_secret_captoora")
    bad_wh = client.post("/api/webhooks/inbound", json={"source": "calendly", "event_type": "invitee.created", "payload": {"name": "Lead"}})
    assert bad_wh.status_code == 401
    ok_wh = client.post(
        "/api/webhooks/inbound",
        json={"source": "calendly", "event_type": "invitee.created", "payload": {"name": "Lead OK"}},
        headers={"X-Captoora-Secret": "top_secret_captoora"},
    )
    assert ok_wh.status_code == 200
    assert ok_wh.json()["accepted"] is True

    # 5. Dashboard integration check + SEO HTTP routes
    dash_html = (repo_root / "dashboard" / "index.html").read_text(encoding="utf-8")
    for marker in ("vendor/leaflet/leaflet.js", "growth_command.js", "tab-mapa-rutas", "tab-centro-ejecutivo"):
        assert marker in dash_html
    assert client.get("/robots.txt").status_code == 200
    assert client.get("/sitemap.xml").status_code == 200
    assert client.get("/llms.txt").status_code == 200









