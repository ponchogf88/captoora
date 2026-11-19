"""Local FastAPI server linking the Liquid Glass Dashboard / Game Studio HQ with the 10 Python Agents."""

from __future__ import annotations

import asyncio
import contextlib
import os
import urllib.parse
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles

from . import ROOT_DIR
from .config import FILES, append_agent_event, now_iso, read_json, validate_client_copy, write_json
from .email_sender import get_smtp_status, send_self_test_email
from .geo_radar import get_enriched_geo_map, optimize_visit_route, save_confirmed_route
from .gmaps_auditor import capture_flagged_places, sync_audit_index_from_sources
from .growth_suite import (
    NICHE_PRESETS,
    ZONE_PRESETS,
    audit_contract_financial_and_tax,
    compute_accountant_snapshot,
    compute_weekly_report,
    enrich_emails_from_websites,
    generate_20_clips_plan,
    generate_calendly_client_link,
    get_or_init_growth_state,
    get_seo_aeo_status,
    get_whatsapp_web_supervisor_queue,
    mark_whatsapp_web_sent,
    record_accountant_expense,
    record_accountant_sale,
    refresh_ceo_weekly_plan,
    run_apify_zone_sweep,
    send_growth_mail_campaign,
    trigger_tomorrow_reminder,
    update_calendly_base_url,
    update_fiscal_config,
    upsert_crm_kyc,
)
from .marketing_hub import (
    enqueue_lupe_calendar_post,
    get_or_init_marketing_state,
    ingest_muse_mobile_notes,
    regenerate_marketing_plan,
    register_conan_creative_brief,
)
from .mockups import (
    PADEL_ACTION_PATH,
    SmallBusinessSpec,
    build_gbp_optimization_checklist,
    build_small_business_spec_from_record,
    build_smb_landing_prototype_html,
    generate_self_test_bundle,
    render_before_after_audit_png,
    render_small_business_dossier_pdf,
)
from .orchestrator import run_agent_mission
from .scheduler import (
    execute_scheduler_slot,
    get_scheduler_status,
    process_inbound_webhook,
    scheduler_background_loop,
    toggle_scheduler,
)
from .schemas import (
    AccountantExpenseRequest,
    AccountantSaleRequest,
    AgentRunRequest,
    ApifySweepRequest,
    ApprovalDecisionRequest,
    CalendlyBaseRequest,
    CalendlyLinkRequest,
    CeoPlanRequest,
    Clips20Request,
    ConanBriefRequest,
    ContractAuditRequest,
    CreateTaskRequest,
    CrmKycUpsertRequest,
    EmailSendTestRequest,
    FiscalConfigRequest,
    GeoRouteOptimizeRequest,
    GeoRouteSaveRequest,
    GmapsCaptureRequest,
    GrowthMailRequest,
    InboundWebhookRequest,
    LupeEnqueuePostRequest,
    MarketingPlanGenerateRequest,
    MuseIngestRequest,
    SchedulerRunSlotRequest,
    SchedulerToggleRequest,
    SmbGenerateAuditRequest,
    TaskStatusUpdateRequest,
    TomorrowReminderRequest,
    UsageLimitsUpdateRequest,
    WhatsappMarkSentRequest,
)
from .usage_tracker import get_usage_summary, update_usage_limits
from .whatsapp_cloud import clean_phone_digits, dispatch_approval_via_cloud, get_cloud_status


@asynccontextmanager
async def _lifespan(_app: FastAPI):
    disable_bg = os.getenv("CAPTOORA_DISABLE_BG_SCHEDULER") == "1" or bool(os.getenv("PYTEST_CURRENT_TEST"))
    stop_event = asyncio.Event()
    task = None
    if not disable_bg:
        task = asyncio.create_task(scheduler_background_loop(stop_event))
    try:
        yield
    finally:
        stop_event.set()
        if task is not None:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task


app = FastAPI(title="Captoora Sports Multi-Agent Control Server", version="0.3.0", lifespan=_lifespan)

# Strictly bound for local desktop use; permits null origin if HTML is opened directly via file://
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8765",
        "http://localhost:8765",
        "null",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type", "X-Captoora-Secret"],
)


def _assemble_workspace() -> dict:
    roster = read_json(FILES["roster"], default={"agents": []})
    asana = read_json(FILES["asana"], default={"sprint": {}, "projects": [], "tasks": []})
    approvals = read_json(FILES["approvals"], default={"items": []})
    accounting = read_json(FILES["accounting"], default={})
    events = read_json(FILES["events"], default={"events": []})
    gmaps_audits = read_json(FILES["gmaps_audits"], default={"audits": []})
    marketing_studio = get_or_init_marketing_state()
    return {
        "server_online": True,
        "server_time": now_iso(),
        "whatsapp_cloud": get_cloud_status(),
        "smtp_status": get_smtp_status(),
        "usage_telemetry": get_usage_summary(),
        "roster": roster,
        "asana": asana,
        "approvals": approvals,
        "accounting": accounting,
        "accountant_snapshot": compute_accountant_snapshot(),
        "scheduler_status": get_scheduler_status(),
        "seo_status": get_seo_aeo_status(),
        "events": events,
        "gmaps_audits": gmaps_audits,
        "marketing_studio": marketing_studio,
    }


@app.get("/")
async def root_redirect():
    return RedirectResponse(url="/dashboard/index.html#sprint-martes")


@app.get("/captoora_sports.html")
@app.get("/portal-3d")
async def serve_portal_3d():
    portal_path = ROOT_DIR / "captoora_sports.html"
    if not portal_path.exists():
        raise HTTPException(status_code=404, detail="captoora_sports.html no encontrado.")
    return FileResponse(portal_path, media_type="text/html; charset=utf-8")


@app.get("/api/health")
async def health():
    return {"status": "ok", "server_time": now_iso(), "workspace": str(ROOT_DIR)}


@app.get("/api/workspace")
async def get_workspace():
    return _assemble_workspace()


@app.get("/api/usage")
async def get_usage():
    return get_usage_summary()


@app.post("/api/usage/limits")
async def post_usage_limits(req: UsageLimitsUpdateRequest):
    summary = update_usage_limits(
        daily_token_budget=req.daily_token_budget,
        monthly_whatsapp_limit=req.monthly_whatsapp_limit,
        daily_usd_limit=req.daily_usd_limit,
        dry_run_preferred=req.dry_run_preferred,
    )
    append_agent_event(
        "contabilidad_finanzas",
        "Actualizó Tope API",
        f"Tope diario: {req.daily_token_budget:,} tokens · US${req.daily_usd_limit:.2f} · Dry-Run={req.dry_run_preferred}",
        zone="boveda_finanzas",
        source="human_ui",
    )
    return {"usage_telemetry": summary, "workspace": _assemble_workspace()}


@app.get("/api/events")
async def get_events():
    return read_json(FILES["events"], default={"events": []})


@app.post("/api/tasks")
async def create_task(req: CreateTaskRequest):
    asana = read_json(FILES["asana"], default={"sprint": {}, "projects": [], "tasks": []})
    tasks = asana.get("tasks", [])
    existing_nums = [int(t["id"].split("-")[1]) for t in tasks if t.get("id", "").startswith("TASK-") and t["id"].split("-")[1].isdigit()]
    new_id = f"TASK-{max(existing_nums, default=600) + 1}"
    task = {
        "id": new_id,
        "project_id": req.project_id,
        "title": req.title,
        "assigned_agent": req.assigned_agent,
        "status": "in_progress",
        "priority": req.priority,
        "due_label": req.due_label,
        "depends_on": [],
        "deliverable_ref": req.deliverable_ref,
    }
    tasks.append(task)
    asana["tasks"] = tasks
    write_json(FILES["asana"], asana)
    append_agent_event(
        "chief_of_staff",
        f"Nueva Tarea {new_id}",
        f"Asignada a {req.assigned_agent}: {req.title}",
        target_agent=req.assigned_agent,
        source="human_ui",
    )
    return {"task": task, "workspace": _assemble_workspace()}


@app.patch("/api/tasks/{task_id}")
async def update_task_status(task_id: str, req: TaskStatusUpdateRequest):
    asana = read_json(FILES["asana"], default={"sprint": {}, "projects": [], "tasks": []})
    for task in asana.get("tasks", []):
        if task.get("id") == task_id:
            task["status"] = req.status
            if req.deliverable_ref is not None:
                task["deliverable_ref"] = req.deliverable_ref
            write_json(FILES["asana"], asana)
            append_agent_event(
                task.get("assigned_agent", "chief_of_staff"),
                f"Estado {task_id} -> {req.status}",
                task.get("title", ""),
                source="human_ui",
            )
            return {"task": task, "workspace": _assemble_workspace()}
    raise HTTPException(status_code=404, detail=f"Tarea '{task_id}' no encontrada.")


@app.get("/api/whatsapp/status")
async def whatsapp_status():
    return get_cloud_status()


@app.post("/api/approvals/{item_id}/decision")
async def decide_approval(item_id: str, req: ApprovalDecisionRequest):
    queue = read_json(FILES["approvals"], default={"items": []})
    asana = read_json(FILES["asana"], default={"projects": [], "tasks": []})
    target_item = None
    for item in queue.get("items", []):
        if item.get("id") == item_id:
            target_item = item
            break
    if not target_item:
        raise HTTPException(status_code=404, detail=f"Elemento '{item_id}' no encontrado en cola.")

    if req.edited_text is not None:
        violations = validate_client_copy(req.edited_text)
        if req.decision == "approve" and target_item.get("niche") != "Operación Interna" and violations:
            raise HTTPException(status_code=400, detail="Texto bloqueado por guardrail: " + " | ".join(violations))
        target_item["draft_text"] = req.edited_text
        if target_item.get("phone"):
            target_item["whatsapp_url"] = (
                f"https://wa.me/{target_item['phone']}?text={urllib.parse.quote(req.edited_text)}"
            )

    target_item["status"] = "approved" if req.decision == "approve" else "rejected"
    target_item["decided_at"] = now_iso()
    write_json(FILES["approvals"], queue)

    linked_task_id = target_item.get("task_id")
    if linked_task_id:
        for task in asana.get("tasks", []):
            if task.get("id") == linked_task_id:
                task["status"] = "done" if req.decision == "approve" else "backlog"
        write_json(FILES["asana"], asana)

    append_agent_event(
        target_item.get("agent_id", "ventas_outreach"),
        f"Trigger {'APROBADO' if req.decision == 'approve' else 'RECHAZADO'}: {item_id}",
        f"{target_item.get('target_name')} ({target_item.get('channel')})",
        target_agent=target_item.get("agent_id"),
        zone="trigger_gate",
        source="human_trigger",
    )

    whatsapp_delivery = {"dispatched": False, "mode": "skipped"}
    if req.decision == "approve" and target_item.get("phone"):
        try:
            whatsapp_delivery = await dispatch_approval_via_cloud(target_item)
        except Exception as exc:
            whatsapp_delivery = {"dispatched": False, "mode": "meta_cloud_error", "error": str(exc)}

    return {
        "item": target_item,
        "whatsapp_delivery": whatsapp_delivery,
        "workspace": _assemble_workspace(),
    }


@app.post("/api/agents/{agent_id}/run")
async def run_agent_endpoint(agent_id: str, req: AgentRunRequest | None = None):
    instruction = req.instruction if req else None
    try:
        result = await asyncio.wait_for(run_agent_mission(agent_id, instruction), timeout=240.0)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"result": result, "workspace": _assemble_workspace()}


@app.get("/api/gmaps-audits")
async def get_gmaps_audits(refresh: bool = False):
    index = read_json(FILES["gmaps_audits"], default=None)
    if refresh or not index or not index.get("audits"):
        index = sync_audit_index_from_sources()
    return index


@app.post("/api/gmaps-audits/capture")
async def post_gmaps_capture(req: GmapsCaptureRequest | None = None):
    payload = req or GmapsCaptureRequest()
    try:
        res = await asyncio.wait_for(
            capture_flagged_places(
                limit=payload.limit,
                slugs=[payload.slug] if payload.slug else None,
                only_deficient=not bool(payload.slug),
                overwrite=payload.overwrite,
            ),
            timeout=240.0,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {
        "batch_results": res["batch_results"],
        "summary": res["summary"],
        "workspace": _assemble_workspace(),
    }


@app.post("/api/small-business/generate-audit")
async def post_small_business_generate_audit(req: SmbGenerateAuditRequest):
    index = read_json(FILES["gmaps_audits"], default=None)
    if not index or not index.get("audits"):
        index = sync_audit_index_from_sources()

    target = next((a for a in index.get("audits", []) if a.get("slug") == req.slug), None)
    if not target:
        raise HTTPException(status_code=404, detail=f"Ficha '{req.slug}' no encontrada en auditoría Google Maps.")

    shot_rel = target.get("screenshot_path") or ""
    shot_abs = (ROOT_DIR / shot_rel) if shot_rel else None
    if shot_abs is not None and not shot_abs.exists():
        shot_abs = None

    spec = build_small_business_spec_from_record(
        target,
        hero_override=req.after_hero_variant,
        screenshot_override=shot_abs,
    )

    out_dir = ROOT_DIR / "assets" / "mockups" / "small_biz"
    ba_rel = f"assets/mockups/small_biz/{req.slug}_AntesDespues_2027.png"
    pdf_rel = f"assets/mockups/small_biz/{req.slug}_Dossier_SMB_2027.pdf"
    ba_abs = ROOT_DIR / ba_rel
    pdf_abs = ROOT_DIR / pdf_rel

    try:
        await asyncio.to_thread(render_before_after_audit_png, spec, ba_abs)
        await asyncio.to_thread(render_small_business_dossier_pdf, spec, pdf_abs, before_after_png_path=ba_abs)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error al renderizar lámina/dossier Small Business: {exc}") from exc

    # Patch gmaps_audits.json record cleanly without blocking full resync
    for item in index.get("audits", []):
        if item.get("slug") == req.slug:
            item["before_after_path"] = ba_rel
            item["dossier_pdf_path"] = pdf_rel
            break
    index["updated_at"] = now_iso()
    write_json(FILES["gmaps_audits"], index)

    enqueued_ids: list[str] = []
    if req.enqueue_mode != "none":
        variants = target.get("outreach_modes") or {}
        niche_low = str(target.get("nicho") or "").lower()
        mode_c_label = (
            "Modo C · Híbrido Web + -35% + Biogen Beta"
            if any(k in niche_low for k in ("fitness", "crossfit", "gym"))
            else "Modo C · Híbrido Portal 3D + -35%"
        )
        mode_map = {
            "mode_a": ("Modo A · Directo Visual Antes/Después + PDF (-35%)", variants.get("mode_a_directo", "")),
            "mode_b": ("Modo B · Diagnóstico Corto 2 Pasos (-35%)", variants.get("mode_b_diagnostico", "")),
            "mode_c": (mode_c_label, variants.get("mode_c_hibrido", "")),
        }
        selected_keys = ["mode_a", "mode_b", "mode_c"] if req.enqueue_mode == "all" else [req.enqueue_mode]

        raw_phone = str(target.get("telefono") or "").strip()
        try:
            phone_digits = clean_phone_digits(raw_phone) if raw_phone else ""
        except ValueError:
            phone_digits = ""

        queue = read_json(FILES["approvals"], default={"policy": "HUMAN_APPROVAL_REQUIRED", "items": []})
        items_list = queue.get("items", [])

        for mkey in selected_keys:
            label, draft_text = mode_map.get(mkey, ("", ""))
            if not draft_text:
                continue
            violations = validate_client_copy(draft_text)
            if violations:
                raise HTTPException(status_code=400, detail=f"Guardrail bloqueó {mkey}: {violations}")

            mode_suffix = mkey.upper().replace("_", "")
            item_id = f"SMB-{req.slug[:12].upper()}-{mode_suffix}"
            items_list = [existing for existing in items_list if existing.get("id") != item_id]
            new_item = {
                "id": item_id,
                "agent_id": "ventas_outreach",
                "task_id": "TASK-601",
                "target_name": f"{target.get('nombre')} ({label})",
                "niche": target.get("nicho") or "Small Business & Comercios",
                "channel": f"WhatsApp Directo ({raw_phone})" if raw_phone else "WhatsApp / Visita Local MTY",
                "phone": phone_digits,
                "package_ref": "SMB-TOTAL Suite Small Business 2027 ($6,890 MXN · -35%)",
                "financial_impact_mxn": 6890,
                "estimated_margin_pct": 84.0,
                "compliance_flags": [
                    "0% mención IA",
                    "Sin palabra 'presumir'",
                    "-35% Descuento Temporada",
                    "3 Pilares + Meta Portfolio",
                ],
                "attachments": [
                    {
                        "type": "image",
                        "label": "Comparativa Antes vs Después 2027 (PNG)",
                        "path": ba_rel,
                    },
                    {
                        "type": "pdf",
                        "label": "Dossier Small Business 2027 (PDF)",
                        "path": pdf_rel,
                    },
                ],
                "draft_text": draft_text,
                "status": "pending_trigger",
                "created_at": now_iso(),
                "decided_at": None,
            }
            if phone_digits:
                new_item["whatsapp_url"] = f"https://wa.me/{phone_digits}?text={urllib.parse.quote(draft_text)}"
            items_list.insert(0, new_item)
            enqueued_ids.append(item_id)

        queue["items"] = items_list
        write_json(FILES["approvals"], queue)

    append_agent_event(
        "embudo_marketing",
        "Auditoría Small Business 2027",
        f"Generó Antes/Después + PDF para {target.get('nombre')}"
        + (f" y encoló {', '.join(enqueued_ids)}" if enqueued_ids else ""),
        target_agent="ventas_outreach",
        zone="trigger_gate" if enqueued_ids else "atelier_embudo",
        source="human_ui",
    )

    return {
        "slug": req.slug,
        "before_after_path": ba_rel,
        "dossier_pdf_path": pdf_rel,
        "enqueued_ids": enqueued_ids,
        "workspace": _assemble_workspace(),
    }


def _find_smb_audit_record(slug: str, zone: str | None = None) -> tuple[dict, str]:
    pv_root = ROOT_DIR / "dashboard" / "data" / "puerto_vallarta"
    zone_map = {
        "zona_romantica": pv_root / "zona_romantica" / "gmaps_audits.json",
        "zona_hotelera": pv_root / "zona_hotelera" / "gmaps_audits.json",
        "centro_y_bahia": pv_root / "centro_y_bahia" / "gmaps_audits.json",
    }
    if zone and zone in zone_map:
        idx = read_json(zone_map[zone], default={"audits": []})
        hit = next((a for a in idx.get("audits", []) if a.get("slug") == slug), None)
        if hit:
            return hit, zone

    nl_idx = read_json(FILES["gmaps_audits"], default={"audits": []})
    nl_hit = next((a for a in nl_idx.get("audits", []) if a.get("slug") == slug), None)
    if nl_hit:
        return nl_hit, "nuevo_leon"

    for zkey, zpath in zone_map.items():
        idx = read_json(zpath, default={"audits": []})
        hit = next((a for a in idx.get("audits", []) if a.get("slug") == slug), None)
        if hit:
            return hit, zkey

    raise HTTPException(status_code=404, detail=f"Ficha '{slug}' no encontrada.")


@app.get("/api/small-business/prototype/{slug}")
async def get_small_business_prototype(slug: str, zone: str | None = None, output: str = "html"):
    """Render bespoke Web Express HTML prototype or Google Business Profile optimization JSON on demand."""
    target, resolved_zone = _find_smb_audit_record(slug, zone=zone)
    checklist = build_gbp_optimization_checklist(target)
    if output == "json":
        return {"slug": slug, "zone": resolved_zone, "gbp_checklist": checklist}
    html_doc = build_smb_landing_prototype_html(
        target,
        assets_prefix="/assets",
        gbp_checklist=checklist,
    )
    return HTMLResponse(content=html_doc)


@app.post("/api/self-test/generate")
async def post_generate_self_test():
    try:
        bundle = await asyncio.to_thread(generate_self_test_bundle)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {
        "bundle": {k: str(v.relative_to(ROOT_DIR)) for k, v in bundle.items()},
        "workspace": _assemble_workspace(),
    }


@app.get("/api/marketing-studio")
async def get_marketing_studio():
    return get_or_init_marketing_state()


@app.post("/api/marketing-studio/generate-plan")
async def post_marketing_generate_plan(req: MarketingPlanGenerateRequest | None = None):
    payload = req or MarketingPlanGenerateRequest()
    state = regenerate_marketing_plan(focus=payload.focus, week_label=payload.week_label)
    return {"marketing_studio": state, "workspace": _assemble_workspace()}


@app.post("/api/marketing-studio/enqueue-post")
async def post_marketing_enqueue_post(req: LupeEnqueuePostRequest):
    try:
        res = enqueue_lupe_calendar_post(
            req.post_id,
            custom_caption=req.custom_caption,
            platform_override=req.platform_override,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {**res, "workspace": _assemble_workspace()}


@app.post("/api/marketing-studio/conan-brief")
async def post_marketing_conan_brief(req: ConanBriefRequest):
    res = register_conan_creative_brief(
        title=req.title,
        tool_stack=req.tool_stack,
        output_format=req.output_format,
        target_channel=req.target_channel,
        notes=req.notes,
    )
    return {**res, "workspace": _assemble_workspace()}


@app.post("/api/marketing-studio/muse-ingest")
async def post_marketing_muse_ingest(req: MuseIngestRequest):
    try:
        res = ingest_muse_mobile_notes(req.notes_text, target_agent=req.target_agent)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {**res, "workspace": _assemble_workspace()}


@app.get("/api/email/status")
async def email_status():
    return get_smtp_status()


@app.post("/api/email/send-test")
async def post_email_send_test(req: EmailSendTestRequest | None = None):
    payload = req or EmailSendTestRequest()
    try:
        res = await asyncio.to_thread(
            send_self_test_email,
            to_email=payload.to_email,
            dry_run=payload.dry_run,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error al enviar correo SMTP: {exc}") from exc
    return {**res, "workspace": _assemble_workspace()}


# --- Technical SEO & AEO Root Files ---
@app.get("/sitemap.xml")
async def serve_sitemap():
    p = ROOT_DIR / "sitemap.xml"
    if not p.exists():
        raise HTTPException(status_code=404, detail="sitemap.xml no encontrado")
    return Response(content=p.read_text(encoding="utf-8"), media_type="application/xml")


@app.get("/robots.txt", response_class=PlainTextResponse)
async def serve_robots():
    p = ROOT_DIR / "robots.txt"
    return p.read_text(encoding="utf-8") if p.exists() else "User-agent: *\nAllow: /\n"


@app.get("/llms.txt", response_class=PlainTextResponse)
async def serve_llms_txt():
    p = ROOT_DIR / "llms.txt"
    return p.read_text(encoding="utf-8") if p.exists() else "# Captoora Studio\n"


# --- Monterrey Geo-Radar & Multi-Stop Route Optimizer ---
@app.get("/api/geo/leads")
async def get_geo_leads():
    return get_enriched_geo_map()


@app.post("/api/geo/routes/optimize")
async def post_geo_route_optimize(req: GeoRouteOptimizeRequest):
    try:
        return optimize_visit_route(
            req.slugs,
            origin_lat=req.origin_lat,
            origin_lng=req.origin_lng,
            origin_name=req.origin_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/geo/routes/save")
async def post_geo_route_save(req: GeoRouteSaveRequest):
    try:
        entry = save_confirmed_route(
            title=req.title,
            slugs=req.slugs,
            scheduled_date=req.scheduled_date,
            notes=req.notes,
            origin_lat=req.origin_lat,
            origin_lng=req.origin_lng,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"route": entry, "geo": get_enriched_geo_map(), "workspace": _assemble_workspace()}


# --- Accountant PFAE 612 (GUFJ870801NA6) & 7 Executive Growth Engines ---
@app.get("/api/growth/state")
async def get_growth_suite_state():
    return {
        "growth_suite": get_or_init_growth_state(),
        "accountant": compute_accountant_snapshot(),
        "weekly_report": compute_weekly_report(),
        "seo_status": get_seo_aeo_status(),
        "scheduler": get_scheduler_status(),
        "whatsapp_web_supervisor": get_whatsapp_web_supervisor_queue(),
        "presets": {"zones": ZONE_PRESETS, "niches": NICHE_PRESETS},
    }


@app.get("/api/growth/tracking-ids")
async def get_growth_tracking_ids():
    return get_or_init_growth_state().get("tracking_ids", {})


@app.get("/api/growth/accountant/summary")
async def get_accountant_summary():
    return compute_accountant_snapshot()


@app.post("/api/growth/accountant/record-sale")
async def post_accountant_sale(req: AccountantSaleRequest):
    res = record_accountant_sale(
        client_name=req.client_name,
        package_ref=req.package_ref,
        amount_collected_mxn=req.amount_collected_mxn,
        direct_cost_mxn=req.direct_cost_mxn,
        includes_iva=req.includes_iva,
        client_is_persona_moral=req.client_is_persona_moral,
        payment_phase=req.payment_phase,
    )
    return {**res, "workspace": _assemble_workspace()}


@app.post("/api/growth/accountant/record-expense")
async def post_accountant_expense(req: AccountantExpenseRequest):
    res = record_accountant_expense(
        concept=req.concept,
        amount_mxn=req.amount_mxn,
        category=req.category,
        has_cfdi_iva=req.has_cfdi_iva,
    )
    return {**res, "workspace": _assemble_workspace()}


@app.post("/api/growth/accountant/config")
async def post_accountant_config(req: FiscalConfigRequest):
    snap = update_fiscal_config(
        isr_reserve_pct=req.isr_reserve_pct,
        ads_reinvestment_pct=req.ads_reinvestment_pct,
    )
    return {"accountant": snap, "workspace": _assemble_workspace()}


@app.post("/api/growth/accountant/audit-contract")
async def post_accountant_audit_contract(req: ContractAuditRequest):
    return audit_contract_financial_and_tax(req.contract_text)


@app.post("/api/growth/ceo/plan")
async def post_growth_ceo_plan(req: CeoPlanRequest | None = None):
    payload = req or CeoPlanRequest()
    plan = refresh_ceo_weekly_plan(payload.custom_focus)
    return {"ceo_plan": plan, "workspace": _assemble_workspace()}


@app.post("/api/growth/content/20-clips")
async def post_growth_20_clips(req: Clips20Request):
    try:
        res = generate_20_clips_plan(req.topic)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"seo_and_clips": res, "workspace": _assemble_workspace()}


@app.get("/api/growth/reports/weekly")
async def get_growth_weekly_report():
    return compute_weekly_report()


@app.post("/api/growth/crm/enrich-emails")
async def post_growth_enrich_emails():
    res = await asyncio.to_thread(enrich_emails_from_websites, 12)
    return {**res, "growth_suite": get_or_init_growth_state(), "workspace": _assemble_workspace()}


@app.post("/api/growth/crm/upsert")
async def post_growth_crm_upsert(req: CrmKycUpsertRequest):
    res = upsert_crm_kyc(req.model_dump())
    return {**res, "growth_suite": get_or_init_growth_state(), "workspace": _assemble_workspace()}


@app.post("/api/growth/mail/send")
async def post_growth_mail_send(req: GrowthMailRequest):
    try:
        res = await asyncio.to_thread(
            send_growth_mail_campaign,
            to_email=req.to_email,
            prospect_name=req.prospect_name,
            offer_track=req.offer_track,
            attach_slug=req.attach_slug,
            dry_run=req.dry_run,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {**res, "workspace": _assemble_workspace()}


@app.post("/api/growth/agenda/remind-tomorrow")
async def post_growth_remind_tomorrow(req: TomorrowReminderRequest | None = None):
    payload = req or TomorrowReminderRequest()
    try:
        res = trigger_tomorrow_reminder(send_email_to=payload.send_email_to, dry_run=payload.dry_run)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"reminder": res, "workspace": _assemble_workspace()}


@app.post("/api/growth/calendly/base-url")
async def post_growth_calendly_base(req: CalendlyBaseRequest):
    cal = update_calendly_base_url(req.base_url)
    return {"calendly": cal, "workspace": _assemble_workspace()}


@app.post("/api/growth/calendly/link")
async def post_growth_calendly_link(req: CalendlyLinkRequest):
    try:
        rec = generate_calendly_client_link(
            prospect_name=req.prospect_name,
            slug=req.slug,
            event_type_id=req.event_type_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"link": rec, "growth_suite": get_or_init_growth_state(), "workspace": _assemble_workspace()}


@app.post("/api/growth/apify/sweep")
async def post_growth_apify_sweep(req: ApifySweepRequest):
    try:
        rec = run_apify_zone_sweep(req.zones, req.niches, dry_run=req.dry_run)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"sweep": rec, "growth_suite": get_or_init_growth_state(), "workspace": _assemble_workspace()}


# --- WhatsApp Web Safe 1-Click Supervisor ---
@app.get("/api/whatsapp/web-queue")
async def get_whatsapp_web_queue():
    return get_whatsapp_web_supervisor_queue()


@app.post("/api/whatsapp/web-mark-sent")
async def post_whatsapp_web_mark_sent(req: WhatsappMarkSentRequest):
    res = mark_whatsapp_web_sent(
        slug=req.slug,
        nombre=req.nombre,
        phone=req.phone,
        notes=req.notes,
    )
    return {**res, "workspace": _assemble_workspace()}


# --- 24/7 Awakening Scheduler & Inbound Webhook ---
@app.get("/api/scheduler/status")
async def scheduler_status():
    return get_scheduler_status()


@app.post("/api/scheduler/toggle")
async def post_scheduler_toggle(req: SchedulerToggleRequest):
    return {"scheduler": toggle_scheduler(req.enabled), "workspace": _assemble_workspace()}


@app.post("/api/scheduler/run-slot")
async def post_scheduler_run_slot(req: SchedulerRunSlotRequest):
    try:
        executed = execute_scheduler_slot(req.slot_id, manual=True)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"executed": executed, "scheduler": get_scheduler_status(), "workspace": _assemble_workspace()}


@app.post("/api/webhooks/inbound")
async def post_inbound_webhook(
    req: InboundWebhookRequest,
    x_captoora_secret: str | None = Header(default=None, alias="X-Captoora-Secret"),
):
    try:
        res = process_inbound_webhook(
            source_name=req.source,
            event_type=req.event_type,
            payload=req.payload,
            provided_secret=x_captoora_secret,
        )
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    return res


# Mount static directories cleanly without shadowing /api routes
for folder in ("dashboard", "assets", "docs", "captoora"):
    path: Path = ROOT_DIR / folder
    if path.exists():
        app.mount(f"/{folder}", StaticFiles(directory=str(path), html=True), name=folder)


def main() -> None:
    import uvicorn

    uvicorn.run("captoora_agents.server:app", host="127.0.0.1", port=8765, reload=False)


if __name__ == "__main__":
    main()
