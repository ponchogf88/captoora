# Guía de Operación: Equipo Digital de 7 Agentes Captoora Sports (NL)

Arquitectura multi-agente **"One Job Per Bot"** construida con **Google Antigravity SDK** (Python 3.12 + `uv`) e integrada en tiempo real con el Dashboard Liquid Glass (`http://127.0.0.1:8765/dashboard/index.html`).

---

## 1. Principio Central: 7 Bots de Responsabilidad Única + Tu Último Trigger

Cada agente tiene un único rol acotado y sus propias herramientas. Ningún agente tiene permiso de enviar mensajes por WhatsApp, mandar correos de Pixieset, publicar en Instagram/LinkedIn ni comprometer gastos por su cuenta.

| # | ID (`agent_id`) | Nombre en Estudio HQ | Única Responsabilidad | Herramientas |
|---:|---|---|---|---|
| 1 | `chief_of_staff` | Director de Orquesta (Chief of Staff) | Priorizar la meta del primer **"Sí"** en el Sprint de 72 horas, delegar a subagentes `2..7`, gestionar Asana y consolidar tu Bandeja de Último Trigger. | `list_asana_tasks`, `create_asana_task`, `update_asana_task_status`, `read_verified_leads`, `calculate_package_financials`, `enqueue_human_trigger` |
| 2 | `scouting_radar` | Scouting & Radar NL | Inspeccionar `apify_scraped_leads.json` y priorizar clubes de Pádel (Torneo del Pavo / Posadas) y academias de Danza (Galas Navideñas) en San Pedro y MTY. | `read_verified_leads`, `list_asana_tasks`, `update_asana_task_status` |
| 3 | `embudo_marketing` | Marketing & Embudo Invisible | Convertir objeciones de gasto en ofertas autofinanciables (patrocinadores / preventa White-Glove) sin imposición comercial. | `read_verified_leads`, `calculate_package_financials`, `enqueue_human_trigger`, `list_asana_tasks` |
| 4 | `social_content` | Redes Sociales & Marca (`@captoora`) | Redactar guiones 9:16 y captions destacando entrega mismo día y reconocimientos en acrílico óptico iluminados con luz LED cálida. | `get_portfolio_highlights`, `enqueue_human_trigger`, `list_asana_tasks` |
| 5 | `ventas_outreach` | Ventas B2B & Cierre 3 Días | Redactar mensajes diagnósticos hiper-personalizados (WhatsApp / Pixieset) para leads verificados y dejarlos en `pending_trigger`. | `read_verified_leads`, `calculate_package_financials`, `enqueue_human_trigger`, `list_asana_tasks`, `update_asana_task_status` |
| 6 | `contabilidad_finanzas` | Contabilidad, Cotizaciones & Margen | Auditar márgenes (`>=70%`), validar anticipo **50% reserva / 50% entrega**, costos de taller y control de suscripciones / CFDI. | `calculate_package_financials`, `list_asana_tasks`, `update_asana_task_status` |
| 7 | `ops_talleres_legal` | Operaciones, Talleres LED & Legal | Proteger SLAs (entrega digital 15 min / mismo día vs **3 a 5 días hábiles** en Foco Lab / El Marco San Pedro / Promocionales MTY) y detectar focos rojos contractuales. | `audit_contract_clauses`, `list_asana_tasks`, `update_asana_task_status`, `enqueue_human_trigger` |

---

## 2. Guardrails Inquebrantables de Marca y Seguridad

1. **Bloqueo por defecto (`deny_all`) + cero shell autónomo:** `build_security_policies()` aplica `policy.deny_all()`, bloquea explícitamente `run_command`, `create_file` y `edit_file`, y únicamente autoriza (`policy.allow`) las herramientas de dominio Captoora (`read_verified_leads`, `list_asana_tasks`, `update_asana_task_status`, `create_asana_task`, `calculate_package_financials`, `audit_contract_clauses`, `get_portfolio_highlights`, `enqueue_human_trigger`, `invoke_subagent`, `search_web`, `finish`). Además, `disabled_tools` desactiva herramientas peligrosas tanto en el Director como en los 6 subagentes especialistas.
2. **Último Trigger Humano Obligatorio:** El hook `@hooks.pre_tool_call_decide` (`pre_tool_guardrail`) y la función `enqueue_human_trigger()` estacionan toda propuesta saliente en `dashboard/data/approval_queue.json` con estado `pending_trigger`. Solo tú apruebas/editas o rechazas desde el Dashboard antes de abrir WhatsApp o enviar.
3. **Filtro automático de estilo Captoora (`validate_client_copy`):**
   - **Prohibido** mencionar `IA` / `Inteligencia Artificial` en textos orientados al cliente.
   - **Prohibido** usar la palabra `presumir` (sustituir por *"proyectar en redes sociales una imagen profesional al nivel de excelencia de su club"*).
   - **Distinción obligatoria de SLA:** Fotografía digital el mismo día (Halftime Blitz / entrega 15 min bajo tu control) vs **3 a 5 días hábiles** para reconocimientos en acrílico óptico con base LED o marcos Fine Art en taller local.

---

## 3. Cómo Iniciar y Usar el Sistema Local

### Levantar el Servidor de Control y Visualización en Vivo
Ejecuta el servidor **dentro de la carpeta del proyecto** (o pasando `--directory` si tu terminal abrió en `~`):
```bash
cd /Users/imac/Documents/antigravity/epic-bohr
uv run python -m captoora_agents.server
```
O en una sola línea desde cualquier carpeta (por ejemplo `~`):
```bash
uv run --directory /Users/imac/Documents/antigravity/epic-bohr python -m captoora_agents.server
```
Abre tu navegador en:
- **Vista Videojuego (Estudio HQ 2D) & Empresa:** `http://127.0.0.1:8765/dashboard/index.html#agentes-ia`
- **Asana & Tu Último Trigger:** `http://127.0.0.1:8765/dashboard/index.html#proyectos-asana`

El encabezado muestra en todo momento el **Countdown regresivo del Sprint de 72 horas** hacia el primer `"Sí"` firmado + 50% de anticipo.

### Ejecutar un Agente desde Terminal (Modo Dry-Run o En Vivo con Gemini)
```bash
# Verificación local sin consumo de API:
uv run python -m captoora_agents.orchestrator --agent chief_of_staff --dry-run

# Ejecutar una misión real (requiere GEMINI_API_KEY en el entorno):
uv run python -m captoora_agents.orchestrator --agent scouting_radar
uv run python -m captoora_agents.orchestrator --agent ventas_outreach --instruction "Prepara 1 borrador Caballo de Troya para un club de pádel sin Trigger pendiente."
```

---

## 4. Pruebas Automatizadas

```bash
uv run pytest -v
```
Valida la integridad de los JSON compartidos en `dashboard/data/`, las reglas de estilo `validate_client_copy()`, el encolado en `enqueue_human_trigger()`, los hooks del SDK y los endpoints HTTP de FastAPI (`GET /api/health`, `GET /api/workspace`, `POST /api/tasks`, `PATCH /api/tasks/{id}`, `POST /api/approvals/{id}/decision`).
