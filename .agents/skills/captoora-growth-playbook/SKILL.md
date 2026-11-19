---
name: captoora-growth-playbook
description: Executes and replicates Captoora's end-to-end weekly client acquisition engine across any new niche or territory: Apify Google Maps scraping, Chrome CDP visual proof auditing, personalized Antes/Después and LED offer PDFs, Embudo Invisible Pull+Push omnichannel campaigns (20-30 clips/week + SEO #1 + safe Zoho/WhatsApp sequences), human-trigger governance, and executive visual deck export. Use when launching a weekly campaign, entering a new niche, scaling prospection to another zone/city, or running an Embudo Invisible sprint.
---

# Captoora Growth Playbook · Campañas High-Impact & Embudo Invisible

Este skill estandariza el flujo completo construido en **Captoora Studio (Monterrey / San Pedro Garza García)** desde la inteligencia competitiva inicial (*Capitanes CDMX / Arena CDMX* y *10 rivales de Nuevo León*) hasta la máquina replicable semanal de captación cliente-por-cliente (**Push Quirúrgico + Pull Embudo Invisible**).

## Arquitectura Central · El Motor Dual (`Push + Pull`)

En lugar de vender fotografía en frío (lo cual activa reactancia psicológica), combinamos **dos carriles sincronizados** que hacen que el prospecto sienta *"lo necesito, lo quiero ya"*:

1. **Carril A · Push Quirúrgico (Evidencia en Espejo, Cero Spam Destructivo):**
   - Extraemos prospectos reales con **Apify** (`compass~crawler-google-places`).
   - Auditamos cada ficha con **Chrome CDP** capturando evidencia visual real (*portada Street View*, *<=5 o 0 fotos*, *ficha sin reclamar*, *falta de reporte para patrocinadores*).
   - Fabricamos automáticamente un **"Regalo de Estatus / Espejo Visual"** personalizado con su marca/logo (*Antes vs. Después 2027* + PDF de 1 página o Mockup de Trofeo Acrílico LED).
   - Enviamos secuencia controlada por lotes seguros (**Zoho Mail `chuy@captoora.studio` + WhatsApp Business + Seguimiento 48h/72h**), protegiendo siempre reputación de dominio y cuenta Meta/WhatsApp.

2. **Carril B · Pull Omnicanal ("Embudo Invisible"):**
   - Mientras el prospecto abre tu correo o WhatsApp, ve tus piezas diarias en su feed:
     - **20–30 clips verticales/semana** grabados en `OBS` + `Captions App` y multiplicados en `OpusClip Pro` (Reels IG, Facebook, TikTok, YouTube Shorts).
     - **Carruseles B2B 4:5 en LinkedIn** (`Canva`) con casos institucionales (*Coca-Cola FEMSA, Tecate/Heineken, Poder Judicial NL, Borregos, Tigres*).
     - **Posicionamiento SEO Local #1 + Portal 3D** (`captoora.studio/sports`) + **Bucle viral del producto físico**: trofeos de acrílico óptico con base de nogal LED y placas QR compartidos en Instagram Stories generan demanda *inbound* directa.

---

## Flujo Semanal Replicable en 6 Fases

Para clonar esta campaña en cualquier nuevo nicho o ciudad (ej. *clínicas estéticas Valle Oriente, inmobiliarias San Pedro, restaurantes Barrio Antiguo, ligas juveniles*), ejecuta estas 6 fases en orden:

### Fase 1 · Selección de Nicho, Dolor y Oferta Autofinanciable
- Consulta [references/niche-adaptation-checklist.md](references/niche-adaptation-checklist.md).
- Define el **dolor visual en 3 segundos** (portada Street View, falta de evidencia a patrocinadores, baja confianza médica/escolar).
- Estructura **3 Opciones Modulares (-35% Temporada / Lanzamiento)** y separa siempre el **Pago/Entrega Digital Mismo Día o 48–72h** de la **Manufactura Física LED/Marcos en taller local (3–5 días hábiles)** con opción de diferir el pago físico a un 2do momento.

### Fase 2 · Scraping Apify + Auditoría Visual Chrome CDP
- Ejecuta el actor `compass~crawler-google-places` filtrado por municipio/colonia y categoría.
- Captura pantallas reales de Google Maps vía Chrome CDP y calcula banderas (`has_streetview_cover`, `images_count`, `claim_this_business`, `audit_score`).
- Prioriza prospectos con dolor visual verificable y teléfono/sitio web activo.

### Fase 3 · Fábrica de Activos Personalizados (`mockups.py` + `WeasyPrint`)
- Genera imágenes comparativas **Antes vs. Después** (`PNG 1600x1200`) y **PDFs de 1 página** o mockups **Acrílico LED** con el nombre y logotipo real de cada prospecto.
- **Regla estricta de calidad:** verifica visualmente los renders antes de encolar y garantiza que ningún cliente reciba archivos genéricos o de otro negocio.

### Fase 4 · Producción Semanal Pull (20–30 Clips + SEO #1)
- Explota el stack de suscripciones (`2x Google AI Pro [$395 + $99]`, `OpusClip Pro`, `Captions`, `Canva`, `Aftershoot`, `Evoto`, `CapCut`, `OBS`, `Meta Muse`) con `$0` dependencia de bots externos.
- Graba **3 videos pilar cortos (8–12 min c/u)** -> exporta **20–30 clips 9:16** -> programa con **Lupe** en Meta Business Suite + TikTok + LinkedIn (`2–3 piezas diarias`).
- Inyecta palabras clave locales en títulos, captions, portal web y descripciones de Google Maps para dominar búsquedas locales.

### Fase 5 · Secuencia Multicanal Segura + Último Trigger Humano
- Carga todos los borradores en la **Cola de Aprobación (`dashboard/data/approval_queue.json`)** — ningún agente envía dinero o mensajes masivos sin autorización humana (`Último Trigger`).
- Respeta los **límites anti-ban** definidos en [references/weekly-embudo-schedule.md](references/weekly-embudo-schedule.md):
  - **Zoho Mail (`chuy@captoora.studio`):** `20–30` correos personalizados diarios máx. por buzón en calentamiento.
  - **WhatsApp Business:** `15–20` contactos nuevos diarios máx. con imagen personalizada adjunta (cambiando redacción y horario).
  - **Seguimiento:** Día 2 (`24–48h`) con hallazgo puntual + Día 4 (`72h`) con enlace **Calendly 15 min** o cierre `50% anticipo / 50% entrega`.

### Fase 6 · Reporte CEO Semanal & Exportación Visual
- Cada **Viernes 16:00–18:00 CST**, consolida métricas reales (*tasa de respuesta WA/Mail, demos Calendly agendadas, clips con mayor retención, anticipos cobrados*) y ajusta ganchos del siguiente Lunes.
- Actualiza el deck visual infográfico (`docs/presentacion_captoora.html` -> `docs/CAPTOORA_Presentacion_Flujo_Visual_2026.pdf`) con nuevos casos de éxito reales para reforzar prueba social.

---

## Reglas Inquebrantables de Marca y Seguridad

- **Cero menciones a IA frente al cliente final:** Todo entregable frente al cliente se presenta como producción editorial y consultoría humana de **Captoora Studio / Jesús Gutiérrez**.
- **SLA transparente:** Nunca prometas acrílicos LED o marcos físicos el mismo día; comunica *entrega digital inmediata / 48–72h* y *taller artesanal MTY/SPGG en 3–5 días hábiles*.
- **Protección de secretos:** Las claves reales (`SMTP_PASS`, `APIFY_TOKEN`, `GHL_WEBHOOK_URL`, `WHATSAPP_CLOUD_TOKEN`, `CALENDLY_BASE_URL`) viven exclusivamente en `.env` (ignorado por `.gitignore`) y jamás se exponen en HTML, JSON del dashboard ni presentaciones.
- **Sin promesas falsas ni métricas inventadas:** Toda proyección de respuesta se presenta como estimación operativa vinculada al cumplimiento diario de envíos y piezas Pull.

## Recursos de Referencia
- Horario semanal por hora, plan de arranque y proyecciones: [references/weekly-embudo-schedule.md](references/weekly-embudo-schedule.md)
- Guía de adaptación rápida a nuevos nichos y checklists pre-vuelo: [references/niche-adaptation-checklist.md](references/niche-adaptation-checklist.md)
