---
name: captoora-influencers-regios
description: End-to-end Captoora "Influencers Captoora / Influencers Regios" & Captoora Biogen 2027 5-Way Ecosystem workflow. Triggered whenever the user passes an Instagram username/URL (e.g. "aplica la skill Captoora influencer a @usuario"): automatically researches & scrapes the public Instagram profile, captures visual screenshots, generates an intelligence report, drafts a personalized 2-page PDF proposal (Capitanes 3D portfolio at https://captoora.studio/sports + Nutrióloga Karen + cocinas saludables + TotalPass/Biogen Club + Farmasi Nutriplus affiliate commissions + @soytrev2 cohorte), drafts formal/easy-read agreements & Instagram DM scripts by tier, and MANDATORILY presents everything to the user for feedback/edits BEFORE any contact or send occurs.
---

# Captoora Influencers Regios · Playbook Piloto Captoora Biogen 2027

Esta skill permite abrir **una conversación limpia en Antigravity** donde el usuario solo escribe algo como:
> *"Aplica el skill Captoora Influencers Regios a este usuario de Instagram: `@usuario`"*

Y el agente ejecuta de manera automática el ciclo completo de investigación, captura, informe, borrador de propuesta PDF y guion DM — **deteniéndose obligatoriamente ante el usuario para revisión y cambios ANTES de entrar en contacto con el influencer**.

---

## Ecosistema Quíntuple Biogen 2027 & Escalera por Resultados
Todo prospecto se evalúa e integra dentro del ecosistema completo (`docs/MODELO_NEGOCIO_BIOGEN_2027.md`):
1. **Captoora Studio:** Sesiones semanales o quincenales (`1/2000s`, luz escultural) + clips `9:16` + coordinación hacia futura agencia **Captoora Talent**.
2. **Nutrióloga Karen:** Consulta en línea/presencial, plan de alimentación y **Ficha Nutricional** (macros + alergias/restricciones).
3. **Cocinas Saludables Aliadas:** `@powerfoodsmty` como referencia y marcas emergentes locales (`dashboard/data/alianzas_biogen_mty.json`).
4. **Gimnasios Aliados:** Red **TotalPass** o sedes independientes **Captoora Biogen Club**.
5. **Farmasi · Nutriplus (Monetización del Influencer):** Alta como afiliado/distribuidor (vía equipo de Karen / directora Farmasi) para generar comisiones vendiendo proteína, creatina, preentreno y suplementos a su audiencia.

**Escalera por resultados (definida por Insights y ventas reales):**
- **Starter (`5K–15K`):** sesión quincenal, consulta, descuento en comidas, alta Farmasi.
- **Pro (`15K–50K`):** sesión semanal, consulta, comida del plan, gimnasio y alta Farmasi.
- **Elite (`50K+`):** todo Pro + bono/pago ajustado a métricas y ventas comprobadas.

---

## Flujo Automático en 5 Fases (Con Candado Obligatorio Pre-Envío)

### Fase 1 · Investigación, Scraping y Captura Visual Automática
Apenas recibas un `@usuario` o URL de Instagram:
1. Ejecuta el script local de reconocimiento del skill desde la raíz del repositorio:
   ```bash
   .venv/bin/python .agents/skills/captoora-influencers-regios/scripts/scout_instagram_profile.py "<@usuario_o_url>"
   ```
   - Esto intenta extraer datos públicos con Apify (`apify~instagram-profile-scraper` si `APIFY_TOKEN` está en `.env`/entorno) y captura `assets/influencers/<slug>/ig_profile.png` + `scout_report.json`.
   - **Integridad de acceso:** Si Instagram muestra muro de inicio de sesión o el perfil es privado, **NUNCA intentes evadir logins ni captchas**; reporta claramente el bloqueo en el informe para que el usuario te comparta una captura abierta desde su sesión o el dato directo.
2. Inspecciona `assets/influencers/<slug>/ig_profile.png` con `view_file` para ver estéticamente su perfil, paleta, bio y feed real.
3. Complementa con búsqueda web (`search_web`) sobre el nombre público del creador/atleta (disciplina, promotoras/ligas, marcas que ya lo patrocinan, agencia o correo de booking público, redes paralelas como TikTok/YouTube).

### Fase 2 · Informe Ejecutivo de Investigación (`docs/informe_influencer_<slug>.md`)
Antes de diseñar la propuesta, genera un informe breve y accionable para el usuario con datos 100% verificados (*cero números inventados*):
- **Perfil y Nivel Sugerido:** Nombre, `@usuario`, disciplina, seguidores/actividad observada, ¿tiene agencia o contacto público? Nivel recomendado (**Starter / Pro / Elite**).
- **Diagnóstico Visual:** Calidad actual de su foto, iluminación, consistencia de Reels/Historias y qué hueco resuelve Captoora Biogen.
- **Fit con Alianzas (Ecosistema Quíntuple):** Cómo encaja con **Nutrióloga Karen**, **Cocinas Aliadas** (`@powerfoodsmty` o cocina de su zona), **Gimnasio**, **Farmasi · Nutriplus** (potencial de ventas con su audiencia) y cohorte **`@soytrev2`**.
- **Horario Recomendado de Publicación:** Estimación inicial o recordatorio de pedir captura de *Insights* para fijar la hora pico en el Anexo A.

### Fase 3 · Generación de Borradores (Propuesta PDF + Convenio + Guion DM)
Construye los 4 borradores listos para revisión usando las plantillas del skill (`assets/` y `references/`):
1. **Propuesta PDF Personalizada (`docs/propuesta_biogen_<slug>.html` -> `docs/Propuesta_Captoora_Biogen_<Slug>.pdf`):**
   - Parte de [assets/propuesta_biogen_template.html](assets/propuesta_biogen_template.html) (2 páginas dark-luxury: Pág. 1 Invitación Piloto + Portafolio Capitanes `https://captoora.studio/sports`; Pág. 2 Flow completo Karen + Cocinas + Gimnasio + Farmasi Nutriplus + Cohorte `@soytrev2` + Pregunta de Agencia vs. Decisión Directa).
   - Exporta con Chrome headless (`--headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf`).
2. **Guion de Contacto por Instagram DM** basado en [references/instagram-dm-and-alliance-slots.md](references/instagram-dm-and-alliance-slots.md).
3. **Convenio Fácil Lectura (`1 pág PDF`) y Contrato Formal (`.md`)** listos para cuando responda positivo ([references/contract-and-easy-read-clauses.md](references/contract-and-easy-read-clauses.md)).
4. **Auditoría Guardrail Previa:** Corre `validate_client_copy()` de `captoora_agents/config.py` (`0` menciones `IA`, `0` verbo `"presumir"`, **`0` menciones de colonia/ubicación como gancho comercial**), e inspecciona visualmente cada página del PDF con `view_file`.

### Fase 4 · CANDADO OBLIGATORIO DE REVISIÓN HUMANA (STOP ANTES DE CONTACTAR)
> **REGLA INQUEBRANTABLE:** Jamás envíes el DM, correo o propuesta por tu cuenta tras el primer comando del usuario.

Presenta ordenadamente al usuario:
1. Captura + **Informe de Investigación** del influencer (`Fase 2`).
2. Vista/enlace del **PDF de Propuesta generado** + **Texto exacto de Instagram DM propuesto** (`Fase 3`).
3. Pídele explícitamente su revisión: *"¿Qué ajustamos de la propuesta o del mensaje antes de contactarlo?"* y aplica todas las correcciones que indique regenerando el PDF hasta obtener su **"Aprobado / Mándaselo"**.

### Fase 5 · Despacho Final (Solo Con Luz Verde Explícita)
Una vez aprobado el borrador final, entrega los textos limpios listos para copiar o ejecuta el envío autorizado, registrando el seguimiento (`Mensaje 1` -> `Agencia o Decisión` -> `Envío PDF` -> `Convenio Fácil Lectura` + `Alta Farmasi` + `Insights`).

---

## Referencias y Activos Integrados
- Modelo de negocio maestro 2027: [docs/MODELO_NEGOCIO_BIOGEN_2027.md](../../../docs/MODELO_NEGOCIO_BIOGEN_2027.md)
- Directorio de cocinas y gimnasios MTY: `dashboard/data/alianzas_biogen_mty.json`
- Script de reconocimiento y captura IG: [scripts/scout_instagram_profile.py](scripts/scout_instagram_profile.py)
- Guiones DM, slots Karen / Cocinas / Gimnasio / Farmasi / `@soytrev2` y guía *Insights*: [references/instagram-dm-and-alliance-slots.md](references/instagram-dm-and-alliance-slots.md)
- Obligaciones semanales/diarias y cláusulas formales: [references/contract-and-easy-read-clauses.md](references/contract-and-easy-read-clauses.md)
- Plantillas HTML base: [assets/propuesta_biogen_template.html](assets/propuesta_biogen_template.html) y [assets/convenio_facil_lectura_template.html](assets/convenio_facil_lectura_template.html)
