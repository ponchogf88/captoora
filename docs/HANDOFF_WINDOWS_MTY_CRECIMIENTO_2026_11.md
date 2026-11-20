# Handoff Windows · Captoora MTY, Contador PFAE 612, 7 Motores, Médico Asesino & Claves

> **Rama sincronizada en GitHub:** `puerto-vallarta-3-zonas-web-gbp-2026` en `git@github.com:ponchogf88/captoora.git`  
> **Conversación completa exportada (142 intervenciones, sanitizada sin secretos):** [HISTORIAL_COMPLETO_SESION_CRECIMIENTO_MTY_2026_11.md](HISTORIAL_COMPLETO_SESION_CRECIMIENTO_MTY_2026_11.md)  
> **Índice general Windows + instalación:** [CONTINUIDAD_CONVERSACION_WINDOWS.md](CONTINUIDAD_CONVERSACION_WINDOWS.md)

---

## 1. Todo lo Construido y Verificado en Esta Sesión

### A. Campaña Influencer El Médico Asesino · Captoora Biogen + Skill Replicable
- **Propuesta comercial + Flujo completo (`PowerFoods MTY` + Nutriólogo + `@soytrev2`):**
  - HTML fuente: [`docs/propuesta_biogen_medico_asesino.html`](propuesta_biogen_medico_asesino.html) → PDF listo: [`docs/Propuesta_Captoora_Biogen_Medico_Asesino.pdf`](Propuesta_Captoora_Biogen_Medico_Asesino.pdf)
- **Convenio Fácil Lectura + Contrato Formal Piloto Influencer (con horarios por alcance, 4+ historias/semana, clips comida 15s + entrenamientos):**
  - HTML + PDF fácil lectura: [`docs/RESUMEN_FACIL_LECTURA_COLABORACION_BIOGEN.html`](RESUMEN_FACIL_LECTURA_COLABORACION_BIOGEN.html) → [`docs/Convenio_Facil_Lectura_Captoora_Biogen_2026.pdf`](Convenio_Facil_Lectura_Captoora_Biogen_2026.pdf)
  - Contrato formal: [`docs/CONTRATO_FORMAL_PILOTO_INFLUENCER_CAPTOORA_BIOGEN.md`](CONTRATO_FORMAL_PILOTO_INFLUENCER_CAPTOORA_BIOGEN.md)
  - Guión DM Instagram: [`docs/ESTRATEGIA_DM_MEDICO_ASESINO_BIOGEN.md`](ESTRATEGIA_DM_MEDICO_ASESINO_BIOGEN.md)
- **Skill instalada para replicar con cualquier `@usuario` de Instagram:**
  - [`.agents/skills/captoora-influencers-regios/SKILL.md`](../.agents/skills/captoora-influencers-regios/SKILL.md) (incluye `scripts/scout_instagram_profile.py`, plantillas HTML y cláusulas contractuales).

### B. Contador SAT PFAE Régimen 612 (`GUFJ870801NA6`) + Regla Cero Deuda (`$0` Ads)
- **Perfil fiscal persistido en [`dashboard/data/accounting_ledger.json`](../dashboard/data/accounting_ledger.json):**
  - Régimen **612** (*Persona Física con Actividades Empresariales y Profesionales*), **RFC `GUFJ870801NA6`**, IVA 16%, provisión ISR 20%, retenciones Persona Moral (10% ISR + 10.67% IVA) y **candado estricto de `$0 MXN` en pauta pagada** hasta registrar cobros reales en caja (`20%` configurable de utilidad libre neta).
  - Auditor fiscal de contratos PFAE 612 implementado en [`captoora_agents/growth_suite.py`](../captoora_agents/growth_suite.py).

### C. Mapa Estratégico Monterrey & SPGG (`141` Pines) + Optimizador de Rutas TSP + 7 Motores + Despertador 24/7
- **Mapa interactivo (`#mapa-rutas`):** [`captoora_agents/geo_radar.py`](../captoora_agents/geo_radar.py), [`dashboard/data/leads_geo.json`](../dashboard/data/leads_geo.json) (`96` Apify exactos + `29` OSM geocodificados + `16` zona), [`dashboard/growth_command.js`](../dashboard/growth_command.js) con Leaflet 1.9.4 local (`dashboard/vendor/leaflet/`) y filtro editorial oscuro sobre OpenStreetMap (sin claves ni marcas de agua).
- **Centro Ejecutivo (`#centro-ejecutivo`):** Contador 612, Supervisor Seguro WhatsApp Web 1-Clic (tope `20/día`), Despertador 24/7 CST cada 60s ([`captoora_agents/scheduler.py`](../captoora_agents/scheduler.py)), SEO/AEO ([`robots.txt`](../robots.txt), [`sitemap.xml`](../sitemap.xml), [`llms.txt`](../llms.txt), `JSON-LD` en [`captoora_sports.html`](../captoora_sports.html)), Matriz 20 Clips 9:16, CEO Personal, Zoho Mail (`chuy@captoora.studio`), Scanner de correos web, Generador Calendly y CRM/KYC.
- **Guardrail reforzado en [`captoora_agents/config.py`](../captoora_agents/config.py):** `0% IA`, sin palabra `"presumir"`, y prohibido destacar colonia propia (`Colinas de San Jerónimo / #SanJeronimo`) en copy comercial al cliente.

---

## 2. Hallazgo Importante de Cuentas / Claves Pendientes (Mac → Windows)

Al revisar las otras ramas del repositorio en GitHub (`ponchogf88/captoora`) se detectó documentación previa verificada:
1. **Calendly del estudio YA identificado en la rama `cursor/calendly-captoora-cuenta-ae48` (`docs/CALENDLY_CAPTOORA.md`):**
   - Cuenta del estudio: **`alfonsogf.88@gmail.com`**
   - Enlace conocido: **`https://calendly.com/captoora`** / `https://calendly.com/captoora/gift-card`
   - **Nota crítica:** NO mezclar con `https://calendly.com/ggconsultores` (`l.jagf87@gmail.com`), que pertenece al despacho. El API token de Calendly (`CALENDLY_API_TOKEN`) sigue pendiente de autorizarse desde la cuenta `alfonsogf.88@gmail.com`.
2. **Lo único opcional pendiente de llenar en `.env` local en Windows** (copiando `.env.example` → `.env`, nunca subiendo `.env` a Git):
   - **`SMTP_PASS`**: App Password de Zoho Mail para `chuy@captoora.studio` (`https://accounts.zoho.com/home#security/app_password`). *(Todo lo demás de WhatsApp Web 1-Clic, Mapa TSP, PDFs y Contabilidad 612 ya opera hoy sin contraseñas).*
   - **`CAPTOORA_WEBHOOK_SECRET`**: se genera localmente (ej. con Python o `openssl rand -hex 24`) si luego conectas webhooks entrantes.
   - **`GA4_MEASUREMENT_ID` / `META_PIXEL_ID` / `GHL_WEBHOOK_URL`**: opcionales; no bloquean ventas hoy (regla `$0 Ads`).

---

## 3. Prompt Directo para Pegar en Antigravity al Abrir en Windows

```text
Acabo de clonar/actualizar el repo de GitHub (rama puerto-vallarta-3-zonas-web-gbp-2026).
Lee docs/CONTINUIDAD_CONVERSACION_WINDOWS.md, docs/HANDOFF_WINDOWS_MTY_CRECIMIENTO_2026_11.md y docs/HANDOFF_WINDOWS_BIOGEN_2027.md.
Ejecuta `uv sync` y `uv run pytest -v` para confirmar el entorno en Windows, levanta `uv run python -m captoora_agents.server` en :8765, y dime qué quieres que hagamos primero (conectar Zoho/Calendly en `.env` local o empezar a mandar WhatsApps/DMs de hoy).
```
