# Respaldo Íntegro de Conversación — Campaña Navideña, Inbound SPGG, Tablero ManyChat y `notebooklm-py`

- **Rama en GitHub:** `docs/conversacion-navidad-manychat-nov-2026`
- **ID de conversación original (Antigravity):** `f71b5fab-a0c2-40f3-aa5e-05a09b19ab67`
- **Equipo de origen:** `iMac 2015` (`/Users/imac/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Projects/CAPTOORA.STUDIO`)
- **Rango temporal de la conversación:** `2026-11-02 06:14` a `2026-11-11 11:50` (`America/Monterrey`)
- **Exportado al commit base:** `HEAD` al momento del respaldo (`397` pasos capturados)

---

## 🧭 Cómo continuar esta conversación en otro equipo (MacBook Pro / otra estación)

1. Asegúrate de tener el repo actualizado (`git fetch origin` o traer esta rama `git checkout docs/conversacion-navidad-manychat-nov-2026` o leer los archivos desde GitHub/carpeta local).
2. Abre un nuevo chat con tu agente en el repositorio `CAPTOORA.STUDIO` (en `main`) y pega este prompt:

```text
Lee completa la conversación respaldada en la rama origin/docs/conversacion-navidad-manychat-nov-2026 (específicamente docs/conversaciones/2026-11-11_f71b5fab_campana_navidad_manychat/README.md y CONVERSACION_DIALOGO_LITERAL.md). Sincroniza tu contexto con todo lo acordado en esa cadena, verifica el estado vigente en main y continuamos desde ahí.
```

> **Tip Git si ya estás trabajando en `main` en el otro equipo y solo quieres traerte esta carpeta para leerla sin cambiar de rama:**
> ```bash
> git fetch origin docs/conversacion-navidad-manychat-nov-2026
> git show origin/docs/conversacion-navidad-manychat-nov-2026:docs/conversaciones/2026-11-11_f71b5fab_campana_navidad_manychat/CONVERSACION_DIALOGO_LITERAL.md | less
> ```

---

## 📂 Qué contiene este respaldo

| Archivo | Contenido | Cuándo usarlo |
| --- | --- | --- |
| [`CONVERSACION_DIALOGO_LITERAL.md`](./CONVERSACION_DIALOGO_LITERAL.md) | Copia **100% literal, palabra por palabra**, de todos los mensajes del usuario y todas las respuestas del agente (~45 KB). | Para que otro agente o tú lean toda la charla íntegra rápidamente. |
| [`CONVERSACION_BITACORA_TECNICA_COMPLETA.md`](./CONVERSACION_BITACORA_TECNICA_COMPLETA.md) | Bitácora técnica paso a paso con llamadas a herramientas, comandos ejecutados, rutas y extractos de salida. | Para auditar qué archivos, scripts o comandos se corrieron en cada turno. |
| [`raw/transcript_full.jsonl`](./raw/transcript_full.jsonl) | Registro crudo oficial completo de Antigravity sin truncar (`JSONL`). | Fuente primaria exacta / respaldo forense completo de la sesión. |
| [`raw/transcript.jsonl`](./raw/transcript.jsonl) | Índice compacto oficial de Antigravity (`JSONL`). | Referencia estructural nativa de Antigravity. |

*(Nota: Los turnos finales donde el agente ejecuta y confirma el `git push` de esta misma rama ocurren inmediatamente después de escribir estos archivos).*

---

## 🧩 Estado de entregables producidos durante esta conversación (ya integrados en `main`)

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
4. **`notebooklm-py` (solo en máquina local, excluido en `.gitignore`):**
   - En la iMac se clonó `https://github.com/teng-lin/notebooklm-py` en `notebooklm-py/` con `uv` (`[browser,markdown,headless]`) y Chromium Playwright, enlazado en `~/.local/bin/notebooklm`.
   - Como `notebooklm-py/` está en `.gitignore`, no viaja por Git al otro equipo; si lo necesitas allá, clónalo y corre `uv sync --extra browser --extra markdown --extra headless && .venv/bin/playwright install chromium && notebooklm login`.
