# Continuidad Total de Conversación y Proyecto Captoora Studio (Mac -> Windows)

> **Rama oficial en GitHub:** `puerto-vallarta-3-zonas-web-gbp-2026` en `https://github.com/ponchogf88/captoora`  
> **Última actualización sincronizada:** `2026-11-20`  
> **Conversación Puerto Vallarta completa:** [HISTORIAL_COMPLETO_SESION_PV_2026_11_18.md](HISTORIAL_COMPLETO_SESION_PV_2026_11_18.md)  
> **Conversación MTY, Contador PFAE 612, 7 Motores, Médico Asesino & Claves:** [HISTORIAL_COMPLETO_SESION_CRECIMIENTO_MTY_2026_11.md](HISTORIAL_COMPLETO_SESION_CRECIMIENTO_MTY_2026_11.md) · [HANDOFF_WINDOWS_MTY_CRECIMIENTO_2026_11.md](HANDOFF_WINDOWS_MTY_CRECIMIENTO_2026_11.md)  
> **Continuidad Biogen 2027 & Omnicanal:** [HANDOFF_WINDOWS_BIOGEN_2027.md](HANDOFF_WINDOWS_BIOGEN_2027.md)

---

## 1. Instrucción Directa para Retomar en tu Computadora de Windows

Cuando abras Antigravity (o Claude / Gemini CLI / Codex) en tu computadora de **Windows**, escribe este prompt exacto:

```text
Lee completos los archivos docs/CONTINUIDAD_CONVERSACION_WINDOWS.md, docs/HANDOFF_WINDOWS_MTY_CRECIMIENTO_2026_11.md, docs/HANDOFF_WINDOWS_BIOGEN_2027.md, docs/HISTORIAL_COMPLETO_SESION_CRECIMIENTO_MTY_2026_11.md, docs/HISTORIAL_COMPLETO_SESION_PV_2026_11_18.md y .agents/skills/captoora-growth-playbook/SKILL.md. Ejecuta `uv sync` y `uv run pytest -v` para confirmar el entorno en Windows y retomemos exactamente donde nos quedamos respetando todas las reglas de marca, copy, PFAE 612 ($0 Ads) y separación por zonas.
```

---

## 2. Pasos de Instalación Rápida en Windows (PowerShell)

1. **Clonar únicamente esta rama actualizada** (descarga rápida, sin mezclar otras ramas viejas ni tocar `main`):
   ```powershell
   git clone -b puerto-vallarta-3-zonas-web-gbp-2026 --single-branch https://github.com/ponchogf88/captoora.git captoora-pv
   cd captoora-pv
   ```
   *(O si usas SSH ya configurado en Windows: `git clone -b puerto-vallarta-3-zonas-web-gbp-2026 --single-branch git@github.com:ponchogf88/captoora.git captoora-pv`)*

2. **Crear `.env` local en Windows** (nunca se sube a GitHub por seguridad):
   Copia `.env.example` a `.env` y llena únicamente tus llaves privadas locales (`APIFY_TOKEN`, `SMTP_PASS`, `WHATSAPP_CLOUD_TOKEN`, etc.).

3. **Instalar dependencias Python con `uv` y validar todas las pruebas:**
   ```powershell
   uv sync
   uv run pytest -v
   ```
   - El soporte de Google Chrome / Edge en Windows ya quedó automatizado en `captoora_agents/mockups.py` (`_find_chrome_binary()`) y `captoora_agents/gmaps_auditor.py`. También puedes definir `CHROME_BIN` en `.env` si instalaste Chrome en otra ruta.

4. **Levantar servidor local interactivo o abrir reportes HTML directamente:**
   ```powershell
   uv run python -m captoora_agents.server
   ```
   - Panel HQ: `http://127.0.0.1:8765/dashboard/index.html`
   - Endpoint Web Demo + Checklist GBP bajo demanda: `http://127.0.0.1:8765/api/small-business/prototype/{slug}`
   - O abre directamente con doble clic los HTML locales en `docs/` (todos usan rutas relativas portables).

---

## 3. Reglas Inquebrantables Acordadas en Esta Conversación

Todo agente y script en este proyecto debe cumplir **sin excepción**:

1. **Separación Estricta de Territorios (`0` mezclas, `0` traslapes `place_id`):**
   - **Puerto Vallarta (Solo PV, Jalisco):** dividido estrictamente en **3 zonas aisladas**:
     1. `zona_romantica` (Emiliano Zapata, Olas Altas, Basilio Badillo, Playa Los Muertos)
     2. `zona_hotelera` (Zona Hotelera Norte, Las Glorias, Versalles/Fluvial, Marina Vallarta, Zona Hotelera Sur / Conchas Chinas)
     3. `centro_y_bahia` (Centro Histórico 48300, Malecón & Paseo Díaz Ordaz, Isla Río Cuale, Gringo Gulch, Col. 5 de Diciembre / Playa Camarones)
   - **Excluidos del perímetro PV:** Riviera Nayarit, Nuevo Vallarta, VidantaWorld, Punta Mita, Bucerías, Tepic, El Pitillal (`48290`), Las Juntas.
   - **Nuevo León intacto:** Los `141` leads y archivos en `dashboard/data/gmaps_audits.json` permanecen separados y sin alterarse al operar Puerto Vallarta.
2. **Cero referencias de origen en entregables de Puerto Vallarta:**
   - **Prohibido** mencionar `Colinas de San Jerónimo`, `San Jerónimo`, `#SanJeronimo`, `Monterrey`, `MTY`, `SPGG` o `San Pedro Garza` en copy, prototipos web o guiones orientados a clientes de PV. Liderar siempre con **portafolio, resultados visuales, estilo editorial y técnica fotográfica**.
3. **Playbook Captoora (`captoora-growth-playbook/SKILL.md` & `captoora_agents/config.py`):**
   - **`0%` menciones a `IA` / `Inteligencia Artificial` / `Claude` / `prompts`** en todo texto orientado a cliente (`validate_client_copy`).
   - **Prohibido** el verbo `presumir` (usar *"proyectar una imagen profesional de alto nivel"*).
   - Director comercial siempre firmado como **`Jesús Gutiérrez`** (`chuy@captoora.studio`, `+52 81 4005 0088`, `https://captoora.studio/sports`).
   - Esquema modular **`-35%`** sin paquete único obligatorio: Small Business / Hospitalidad / Comercios en **`$3,900` / `$6,890` / `$10,400 MXN`**; Eventos/Deportes en **`$3,185` / `$5,135` / `$7,475 MXN`**.
   - Separar siempre entrega digital (**mismo día en eventos / 48–72h en sesiones SMB + Web Express + GBP**) de fabricación artesanal de placas acrílicas LED QR / marcos (**3–5 días hábiles**, diferible a un 2do momento).

---

## 4. Mapa Completo de Entregables Actuales Listos en el Repositorio

### A. Fase 1 + Fase 3: Mapeado Google Maps (`167/167` Capturas CDP) + Web Express Demos + Checklists GBP

| Zona / Territorio | Prospectos | Sin Web / Solo Red Social | Capturas Chrome CDP | Hub Interactivo (HTML) | Reporte Tabular (MD) | Carpeta Prototipos Web |
| :--- | ---: | ---: | ---: | :--- | :--- | :--- |
| **Zona Romántica** | `54` | `16` | `54/54` | [puerto_vallarta_zona_romantica.html](puerto_vallarta_zona_romantica.html) | [MAPEADO_PV_ZONA_ROMANTICA.md](MAPEADO_PV_ZONA_ROMANTICA.md) | `docs/demos_pv/zona_romantica/` |
| **Zona Hotelera** | `73` | `31` | `73/73` | [puerto_vallarta_zona_hotelera.html](puerto_vallarta_zona_hotelera.html) | [MAPEADO_PV_ZONA_HOTELERA.md](MAPEADO_PV_ZONA_HOTELERA.md) | `docs/demos_pv/zona_hotelera/` |
| **Centro / Bahía** | `40` | `18` | `40/40` | [puerto_vallarta_centro_bahia.html](puerto_vallarta_centro_bahia.html) | [MAPEADO_PV_CENTRO_Y_BAHIA.md](MAPEADO_PV_CENTRO_Y_BAHIA.md) | `docs/demos_pv/centro_y_bahia/` |
| **Resumen Maestro PV** | **`167`** | **`65`** | **`167/167`** | Resumen JSON: `dashboard/data/puerto_vallarta/territorio_resumen.json` | — | `167` HTML listos |

### B. Fase 2: Cartelera de Eventos (Nov 2026 – Ene 2027), Influencers & Proveedores Confiables PV

- **Eventos Zona Romántica (`83`):** [puerto_vallarta_eventos_zona_romantica.html](puerto_vallarta_eventos_zona_romantica.html) · [EVENTOS_PV_ZONA_ROMANTICA.md](EVENTOS_PV_ZONA_ROMANTICA.md)
- **Eventos Zona Hotelera (`17`):** [puerto_vallarta_eventos_zona_hotelera.html](puerto_vallarta_eventos_zona_hotelera.html) · [EVENTOS_PV_ZONA_HOTELERA.md](EVENTOS_PV_ZONA_HOTELERA.md)
- **Eventos Centro / Bahía (`18`):** [puerto_vallarta_eventos_centro_bahia.html](puerto_vallarta_eventos_centro_bahia.html) · [EVENTOS_PV_CENTRO_Y_BAHIA.md](EVENTOS_PV_CENTRO_Y_BAHIA.md)
- **Influencers, VIPs, Chefs & Brechas Fotográficas (`6` grupos, `8` bloques VIP, `13` chefs FGI, `5` fotógrafos prensa detectados):** [puerto_vallarta_influencers_y_cobertura.html](puerto_vallarta_influencers_y_cobertura.html) · [INFLUENCERS_Y_COBERTURA_PV.md](INFLUENCERS_Y_COBERTURA_PV.md)
- **Proveedores Locales Confiables para Taller & Recuerdos en PV (`39` auditados, `25/39` Chrome CDP + checklist anti-informalidad):** [puerto_vallarta_proveedores_taller.html](puerto_vallarta_proveedores_taller.html) · [PROVEEDORES_TALLER_PUERTO_VALLARTA.md](PROVEEDORES_TALLER_PUERTO_VALLARTA.md)

### C. Código Principal Agregado / Actualizado

- [captoora_agents/mockups.py](../captoora_agents/mockups.py): Perfiles `Hoteles, Resorts & Beach Clubs` / `Tiendas, Boutiques & Comercios`, `_find_chrome_binary()` Windows+Mac, `build_gbp_optimization_checklist()` y `build_smb_landing_prototype_html()` + imágenes editoriales costeras (`assets/niche_heroes/pv_hospitality_resort.jpg`, `assets/niche_heroes/pv_gastronomy_terrace.jpg`).
- [captoora_agents/gmaps_auditor.py](../captoora_agents/gmaps_auditor.py): `sync_audit_index_from_sources` y `capture_flagged_places` parametrizados, mensajes origin-neutral para PV y resolución multiplataforma Chrome.
- [captoora_agents/server.py](../captoora_agents/server.py): Nuevo endpoint `GET /api/small-business/prototype/{slug}` para vista Web Express / checklist GBP en vivo.
- [scripts/scrape_puerto_vallarta.py](../scripts/scrape_puerto_vallarta.py): Scraper Apify + auditor Chrome CDP separado por 3 zonas PV.
- [scripts/scrape_pv_events_and_influencers.py](../scripts/scrape_pv_events_and_influencers.py) & [scripts/scrape_pv_suppliers.py](../scripts/scrape_pv_suppliers.py) & [scripts/build_pv_events_and_suppliers_hub.py](../scripts/build_pv_events_and_suppliers_hub.py) & [scripts/build_pv_zone_maps.py](../scripts/build_pv_zone_maps.py).
- [tests/test_captoora_agents.py](../tests/test_captoora_agents.py): **16/16 pruebas automatizadas** cubriendo NL, PV 3 zonas, Web Express + GBP, guardrails y FastAPI.

---

## 5. Pendientes / Siguientes Pasos Naturales al Retomar en Windows

1. Seleccionar los primeros **15–20 prospectos prioritarios** por zona dentro del filtro **`Sin Sitio Web / Solo Red Social`** (`65` detectados en total across ZR/ZH/Centro) y enviar sus links reales de **Web Demo + Guión Modo D** por WhatsApp (`Jesús Gutiérrez`).
2. Ejecutar visita física y auditoría presencial a los **Top Proveedores Tier A** en Versalles / Fluvial / El Coapinole ([PROVEEDORES_TALLER_PUERTO_VALLARTA.md](PROVEEDORES_TALLER_PUERTO_VALLARTA.md)) para cotizar muestra de base acrílica LED + grabado láser sin sobrecosto turístico ni souvenirs genéricos.
3. Hacer outreach directo a organizadores/influencers con brecha de cobertura visual detectada en [puerto_vallarta_influencers_y_cobertura.html](puerto_vallarta_influencers_y_cobertura.html) rumbo a **Vallarta Nayarit Gastronómica, Padel 233, Torneo de Pesca y Posadas Dic 2026**.
4. Si en algún momento deseas publicar los `167` demos `docs/demos_pv/` bajo dominio web (`captoora.studio/demos_pv/...`) para mandar URLs `https://` limpias por WhatsApp, desplegar la carpeta `docs/` + `assets/` en tu hosting / Vercel / GitHub Pages de forma que los links en WhatsApp abran directo desde el celular del dueño del negocio.
