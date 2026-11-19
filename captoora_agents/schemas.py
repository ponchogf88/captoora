"""Pydantic data models for Asana tracking, Human Trigger approvals, Geo Routes, Accountant, and Growth Suite."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


TaskStatus = Literal["backlog", "in_progress", "waiting_trigger", "done"]
ApprovalStatus = Literal["pending_trigger", "approved", "rejected"]
DecisionAction = Literal["approve", "reject"]


class CreateTaskRequest(BaseModel):
    project_id: str
    title: str = Field(min_length=4, max_length=240)
    assigned_agent: str
    priority: str = "Alta"
    due_label: str = "Sprint 72h"
    deliverable_ref: str = "Pendiente"


class TaskStatusUpdateRequest(BaseModel):
    status: TaskStatus
    deliverable_ref: str | None = None


class ApprovalDecisionRequest(BaseModel):
    decision: DecisionAction
    edited_text: str | None = None


class AgentRunRequest(BaseModel):
    instruction: str | None = None


class UsageLimitsUpdateRequest(BaseModel):
    daily_token_budget: int = Field(ge=5000, le=50_000_000, default=500_000)
    monthly_whatsapp_limit: int = Field(ge=50, le=100_000, default=1000)
    daily_usd_limit: float = Field(ge=0.25, le=500.0, default=5.0)
    dry_run_preferred: bool = False


class GmapsCaptureRequest(BaseModel):
    limit: int = Field(ge=1, le=30, default=5)
    slug: str | None = None
    overwrite: bool = False


class SmbGenerateAuditRequest(BaseModel):
    slug: str = Field(min_length=2, max_length=120)
    enqueue_mode: Literal["none", "all", "mode_a", "mode_b", "mode_c"] = "none"
    after_hero_variant: Literal["auto", "sports", "studio"] = "auto"


class MarketingPlanGenerateRequest(BaseModel):
    focus: str = Field(default="all", max_length=80)
    week_label: str = Field(default="Semana Sprint Nov 2026 (-35%)", max_length=120)


class LupeEnqueuePostRequest(BaseModel):
    post_id: str = Field(min_length=2, max_length=60)
    custom_caption: str | None = None
    platform_override: str | None = None


class ConanBriefRequest(BaseModel):
    title: str = Field(min_length=4, max_length=200)
    tool_stack: str = Field(default="OpusClip Pro + CapCut", max_length=120)
    output_format: str = Field(default="Reel 9:16", max_length=80)
    target_channel: str = Field(default="IG Reels + TikTok + LinkedIn", max_length=120)
    notes: str = Field(default="", max_length=600)


class MuseIngestRequest(BaseModel):
    notes_text: str = Field(min_length=4, max_length=2000)
    target_agent: str = Field(default="marky_marketing", max_length=60)


class EmailSendTestRequest(BaseModel):
    to_email: str = Field(default="ponchogf88@me.com", min_length=5, max_length=160)
    dry_run: bool = False


# --- Monterrey Geo-Radar & Routes ---
class GeoRouteOptimizeRequest(BaseModel):
    slugs: list[str] = Field(min_length=1, max_length=25)
    origin_lat: float | None = None
    origin_lng: float | None = None
    origin_name: str | None = None


class GeoRouteSaveRequest(GeoRouteOptimizeRequest):
    title: str = Field(default="Ruta Confirmada Monterrey", min_length=3, max_length=140)
    scheduled_date: str = ""
    notes: str = ""


# --- Accountant, Fiscal SAT 612 & Growth Suite ---
class AccountantSaleRequest(BaseModel):
    client_name: str = Field(min_length=2, max_length=140)
    package_ref: str = Field(default="SMB-TOTAL", max_length=120)
    amount_collected_mxn: float = Field(gt=0.0, le=5_000_000.0)
    direct_cost_mxn: float = Field(ge=0.0, le=2_000_000.0, default=0.0)
    includes_iva: bool = True
    client_is_persona_moral: bool = False
    payment_phase: str = "Anticipo 50%"


class AccountantExpenseRequest(BaseModel):
    concept: str = Field(min_length=2, max_length=180)
    amount_mxn: float = Field(gt=0.0, le=1_000_000.0)
    category: str = "Taller / Producción"
    has_cfdi_iva: bool = True


class FiscalConfigRequest(BaseModel):
    isr_reserve_pct: float | None = Field(default=None, ge=0.0, le=45.0)
    ads_reinvestment_pct: float | None = Field(default=None, ge=0.0, le=50.0)


class ContractAuditRequest(BaseModel):
    contract_text: str = Field(min_length=10, max_length=8000)


class CeoPlanRequest(BaseModel):
    custom_focus: str | None = None


class Clips20Request(BaseModel):
    topic: str = Field(default="Auditoría Google Maps + Alta Velocidad 1/2000s", min_length=3, max_length=180)


class GrowthMailRequest(BaseModel):
    to_email: str = Field(min_length=5, max_length=160)
    prospect_name: str = Field(min_length=2, max_length=140)
    offer_track: Literal["small_business", "navidad_led", "biogen"] = "small_business"
    attach_slug: str = ""
    dry_run: bool = True


class CalendlyLinkRequest(BaseModel):
    prospect_name: str = Field(min_length=2, max_length=140)
    slug: str = ""
    event_type_id: str = "maps_audit_15"


class CalendlyBaseRequest(BaseModel):
    base_url: str = Field(min_length=8, max_length=240)


class TomorrowReminderRequest(BaseModel):
    send_email_to: str = ""
    dry_run: bool = True


class CrmKycUpsertRequest(BaseModel):
    slug: str = ""
    nombre: str = Field(min_length=2, max_length=140)
    stage: str = "Nuevo"
    decisor_name: str = ""
    email: str = ""
    phone: str = ""
    rfc: str = ""
    razon_social: str = ""
    confirmed_yes_today: bool = False
    notes: str = ""
    sync_ghl: bool = False


class WhatsappMarkSentRequest(BaseModel):
    slug: str
    nombre: str
    phone: str
    notes: str = ""


class ApifySweepRequest(BaseModel):
    zones: list[str] = Field(min_length=1)
    niches: list[str] = Field(min_length=1)
    dry_run: bool = True


class SchedulerToggleRequest(BaseModel):
    enabled: bool


class SchedulerRunSlotRequest(BaseModel):
    slot_id: str


class InboundWebhookRequest(BaseModel):
    source: str = Field(default="ghl_or_calendly", max_length=80)
    event_type: str = Field(default="lead_update", max_length=80)
    payload: dict[str, Any] = Field(default_factory=dict)


class AgentMissionOutput(BaseModel):
    """Structured final report returned by Google Antigravity agents."""

    agent_id: str
    summary: str
    actions_taken: list[str]
    asana_task_updates: list[str]
    enqueued_approval_ids: list[str]
    next_recommendation: str
