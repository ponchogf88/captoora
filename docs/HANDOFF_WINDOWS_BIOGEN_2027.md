# Handoff Windows · Captoora Biogen 2027 & Omnicanal

> Guía rápida para retomar exactamente este hilo en tu computadora de **Windows** (rama `puerto-vallarta-3-zonas-web-gbp-2026` en `github.com:ponchogf88/captoora.git`).

---

## 1. Qué ya quedó listo y guardado en este repositorio
1. **Modelo de Negocio Quíntuple 2027:** [`docs/MODELO_NEGOCIO_BIOGEN_2027.md`](MODELO_NEGOCIO_BIOGEN_2027.md)
   - 5 aliados: **Captoora Studio**, **Nutrióloga Karen** (consultas + Ficha Nutricional + fotos de consultorio + imagen del programa), **Cocinas Saludables emergentes** (Power Foods como referencia + sesión Día 1 de platillos), **Gimnasios** (**TotalPass** Plan A / **Captoora Biogen Club** Plan B), y **Farmasi · Nutriplus** (comisiones por venta para influencers + equipo para Karen).
   - 2 carriles: **Influencers** (escalera Starter 5K–15K / Pro 15K–50K / Elite 50K+) y **Público General de paga** (arranque **2 de enero 2027**).
   - Fase 2: **Agencia Captoora Talent**.
2. **Propuestas PDF listas (ya revisadas visualmente y validadas):**
   - [`Propuesta_Captoora_Biogen_TotalPass.pdf`](Propuesta_Captoora_Biogen_TotalPass.pdf) (8 slides 16:9 con portafolio y logos)
   - [`Propuesta_Captoora_Biogen_Cocina_Aliada.pdf`](Propuesta_Captoora_Biogen_Cocina_Aliada.pdf) (2 págs)
   - [`Propuesta_Captoora_Biogen_Gimnasio_Club.pdf`](Propuesta_Captoora_Biogen_Gimnasio_Club.pdf) (2 págs)
   - [`Propuesta_Captoora_Biogen_Medico_Asesino.pdf`](Propuesta_Captoora_Biogen_Medico_Asesino.pdf)
3. **Scraping real de Monterrey (67 leads filtrados + capturas Chrome CDP):**
   - [`docs/DIRECTORIO_COCINAS_Y_GIMNASIOS_MTY_2027.md`](DIRECTORIO_COCINAS_Y_GIMNASIOS_MTY_2027.md) y [`dashboard/data/alianzas_biogen_mty.json`](../dashboard/data/alianzas_biogen_mty.json)
   - Script reutilizable: [`scripts/scrape_biogen_alianzas_mty.py`](../scripts/scrape_biogen_alianzas_mty.py)
4. **Estrategia LinkedIn B2B & 10 Canales Omnicanal ("Go Everywhere, Everything"):**
   - [`docs/ESTRATEGIA_OMNICANAL_Y_LINKEDIN_BIOGEN_2027.md`](ESTRATEGIA_OMNICANAL_Y_LINKEDIN_BIOGEN_2027.md) (incluye TotalPass, Wellhub, RH FEMSA/Heineken/CEMEX/Arca/Banorte, Birdman/You Matter/B Life, agencias deportivas/talento, HYROX/Running Clubs y clínicas de fisioterapia/pádel ya en el repo)
   - [`docs/DIRECTORIO_CONTACTOS_ALIANZA_BIOGEN_2027.md`](DIRECTORIO_CONTACTOS_ALIANZA_BIOGEN_2027.md)
   - Guiones WhatsApp / IG / LinkedIn: [`docs/GUIONES_CONTACTO_ALIANZA_BIOGEN_2027.md`](GUIONES_CONTACTO_ALIANZA_BIOGEN_2027.md)
5. **Skill actualizada:** [`.agents/skills/captoora-influencers-regios/SKILL.md`](../.agents/skills/captoora-influencers-regios/SKILL.md)
6. **MCP Browser Config + Chrome Remote Debugging:** [`.agents/mcp_config.json`](../.agents/mcp_config.json) y [`docs/CONEXION_CHROME_REMOTE_DEBUGGING_Y_MCP.md`](CONEXION_CHROME_REMOTE_DEBUGGING_Y_MCP.md)
   - En Windows, para puerto `9222` en Chrome: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%LOCALAPPDATA%\captoora-chrome-9222"` (o activar `chrome://inspect/#remote-debugging` en Chrome 144+ para `--autoConnect`).
7. **Respaldo de esta conversación completa (redactado sin secretos):**
   - [`.antigravity_state/brain/e3211432-3b08-4b69-976e-d7a1f46999b9/`](../.antigravity_state/brain/e3211432-3b08-4b69-976e-d7a1f46999b9/)

---

## 2. Cómo abrir en Windows
```powershell
git clone -b puerto-vallarta-3-zonas-web-gbp-2026 git@github.com:ponchogf88/captoora.git
cd captoora
# (si ya lo clonaste antes: git pull origin puerto-vallarta-3-zonas-web-gbp-2026)
uv sync
```
*(Copia tu `.env` aparte por seguridad — nunca se sube a GitHub).*

---

## 3. Pendientes inmediatos para seguir en Windows
1. Pasar nombre de tu hermana y `@` de Instagram de la Nutrióloga Karen para cerrar su mensaje y el anexo de contrato.
2. Confirmar `@` exactos de la cohorte inicial (El Médico Asesino, Joel Isaí, Ángel Leal, Mauricio, `@soytrev2`, etc.) y aplicar la skill `captoora-influencers-regios` a cada uno.
3. Dar luz verde ("Aprobado") para disparar los primeros mensajes en LinkedIn (TotalPass / Wellhub / RH FEMSA & Heineken), WhatsApp a Karen y DM a las cocinas/gimnasios top de Monterrey.
