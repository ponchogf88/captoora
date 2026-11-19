# Respaldo Íntegro de Conversación — Campaña Navideña, Inbound SPGG, Tablero ManyChat, `notebooklm-py` y Sync Windows

- **Disponible en GitHub (`main` y rama dedicada):** `main` y `docs/conversacion-navidad-manychat-nov-2026`
- **ID de conversación original (Antigravity):** `f71b5fab-a0c2-40f3-aa5e-05a09b19ab67`
- **Equipo de origen:** `iMac 2015` (`/Users/imac/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Projects/CAPTOORA.STUDIO`)
- **Equipo destino:** Computadora con **Windows**
- **Rango temporal de la conversación:** `2026-11-02 06:14:47` a `2026-11-19 08:37:59` (`America/Monterrey`)
- **Pasos capturados en `raw/transcript_full.jsonl`:** `494`

---

## 🪟 Cómo continuar esta conversación en tu computadora con Windows

1. En Windows (PowerShell o Git Bash), clona o actualiza `main`:
   ```powershell
   git clone https://github.com/ponchogf88/captoora.git
   cd captoora
   git pull origin main
   ```
   *(O si usas SSH: `git clone git@github.com:ponchogf88/captoora.git`)*
2. Abre la carpeta `captoora` en Antigravity (o Cursor / Codex) en Windows y pega este prompt exacto:

```text
Lee completa la conversación respaldada en docs/conversaciones/2026-11-11_f71b5fab_campana_navidad_manychat/README.md y CONVERSACION_DIALOGO_LITERAL.md. Sincroniza tu contexto con todo lo hablado y acordado en esa sesión (Campaña Navideña 2026, embudo orgánico $0 ads SPGG/embajadoras Oct 31, tablero hora por hora ManyChat, notebooklm-py, Prompt Maestro Muse y estado del repo), verifica el estado actual en main y continuamos desde aquí en Windows.
```

> **Si también quieres revisar la rama paralela específica de esta charla:**
> ```powershell
> git fetch origin docs/conversacion-navidad-manychat-nov-2026
> git checkout docs/conversacion-navidad-manychat-nov-2026
> ```

---

## 📂 Qué contiene este respaldo

| Archivo | Contenido | Cuándo usarlo |
| --- | --- | --- |
| [`CONVERSACION_DIALOGO_LITERAL.md`](./CONVERSACION_DIALOGO_LITERAL.md) | Copia **100% literal, palabra por palabra**, de todos los mensajes del usuario y todas las respuestas del agente. | Para que otro agente o tú lean toda la charla íntegra rápidamente. |
| [`CONVERSACION_BITACORA_TECNICA_COMPLETA.md`](./CONVERSACION_BITACORA_TECNICA_COMPLETA.md) | Bitácora técnica paso a paso con llamadas a herramientas, comandos ejecutados, rutas y extractos de salida. | Para auditar qué archivos, scripts o comandos se corrieron en cada turno. |
| [`raw/transcript_full.jsonl`](./raw/transcript_full.jsonl) | Registro crudo oficial completo de Antigravity sin truncar (`JSONL`). | Fuente primaria exacta / respaldo forense completo de la sesión. |
| [`raw/transcript.jsonl`](./raw/transcript.jsonl) | Índice compacto oficial de Antigravity (`JSONL`). | Referencia estructural nativa de Antigravity. |

*(Nota de última vuelta: Los archivos crudos se exportan justo antes de confirmar el `git push` final de cierre; el resultado y hash de commit quedan reportados en la respuesta final de la conversación y en el historial de Git).*

---

## 🧩 Estado de entregables producidos o sincronizados en esta sesión (en `main`)

1. **Command Center Campaña Navideña 2026 & Embudo Orgánico ($0 Ads):**
   - `campana_navidad_2026.html`
   - `captoora_hub.html`
   - `campaigns/campana-navidad-2026/EMBUDO_INBOUND_VIRAL_SPGG_TESTIMONIOS.md`
   - `campaigns/campana-navidad-2026/MATRIZ_MAESTRA_40_POSTS.csv`
   - `campaigns/campana-navidad-2026/8_POSTS_LANZAMIENTO_Y_MONTAJE.md`
   - `campaigns/campana-navidad-2026/GUIONES_REELS_MONTAJE_15S.md`
2. **Tablero Operativo Semanal Hora por Hora (Estilo ManyChat) & Benchmark SPGG:**
   - `tablero_operativo_navidad_manychat.html`
   - `campaigns/campana-navidad-2026/TABLERO_SEMANAL_HORA_POR_HORA_MANYCHAT.md`
   - Disparadores clave: `NAVIDAD`, `BEBE`, `CHINA`, `LUJO`
   - Commit de integración en `main`: `4bb7c9c`
3. **Estrategia Unboxing & Plantillas Embajadoras (Montse "La China", Janet, 25+ líderes oct 31):**
   - `ESTRATEGIA_VIRAL_UNBOXING_NAVIDENO_CAPTOORA.md`
   - `PLANTILLAS_MENSAJES_INFLUENCERS_CAPTOORA.md`
   - `GALERIA_CLIENTES_FARMASI.html`
   - `.agents/skills/captoora-studio-retouch/SKILL.md`
4. **Avances locales rescatados y subidos a `main` en el corte del 19 de noviembre de 2026:**
   - `PROMPT_MAESTRO_AGENTE_MUSE_META_CAPTOORA.md`
   - `preview-captoora-fusion-antigravity.html` y `preview-captoora-fusion-nikon.html` (`css/fusion-pro.css`, `js/fusion-pro.js`)
   - `historico_y_archivos/previews_descartados_2026-11-12/` (9 archivos de prototipos previos preservados bajo Zero Delete Policy)
5. **`notebooklm-py` (solo en máquina local, excluido en `.gitignore`):**
   - En la iMac se clonó `https://github.com/teng-lin/notebooklm-py` en `notebooklm-py/` con `uv` (`[browser,markdown,headless]`) y Chromium Playwright, enlazado en `~/.local/bin/notebooklm`.
   - Como `notebooklm-py/` está en `.gitignore`, no viaja por Git al equipo Windows; si lo ocupas en Windows, clónalo allá (`git clone https://github.com/teng-lin/notebooklm-py.git`) e instala con `uv sync --extra browser --extra markdown --extra headless` + `playwright install chromium` + `notebooklm login`.
