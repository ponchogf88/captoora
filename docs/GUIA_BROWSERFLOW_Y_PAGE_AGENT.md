# Guía: BrowserFlow, Page Agent, NexLev y Control Nativo de Chrome

## 1. Estado actual en esta sesión (por qué no tomé tu pestaña abierta)
- En esta sesión de Antigravity solo están cargados los servidores MCP de documentación/notebooks (`dak-notebook`, `dak-viz`, `gemini-api-docs`). El servidor **`chrome-devtools` MCP** no está activo en esta sesión.
- Tu navegador Google Chrome abierto tampoco se inició con `--remote-debugging-port`.
- Por eso el scraping en vivo de cocinas y gimnasios se ejecutó con **Apify + Chrome CDP WebSocket nativo** (`scripts/scrape_biogen_alianzas_mty.py`), sin usar Playwright.

---

## 2. Cómo habilitar control nativo de extensiones Chrome en futuras sesiones
Según la documentación del plugin `chrome-devtools`, agrega esto en `~/.gemini/config/mcp_config.json` (o en Antigravity → `... → MCP Servers`) y reinicia la sesión:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest", "--categoryExtensions"]
    }
  }
}
```

Con `--categoryExtensions` se habilitan herramientas como `list_extensions`, `trigger_extension_action`, `take_snapshot` y `evaluate_script` dentro del navegador.

---

## 3. Prueba rápida en tu pestaña abierta de BrowserFlow (Google Maps)
Si quieres probar **BrowserFlow** directo en Chrome (útil para extraer manualmente perfiles de Instagram o listas sin gastar créditos):
1. Abre la extensión **BrowserFlow** en Chrome y entra a **Gallery → Google Maps**.
2. Selecciona la plantilla **"Scrape List of Places from Google Maps"** o crea un flujo:
   - **Visit:** `https://www.google.com/maps`
   - **Type:** `meal prep comida saludable Monterrey` (o `gimnasio independiente Guadalupe Nuevo Leon`) en el buscador y presiona Enter.
   - **Loop / Scroll:** desplazar el panel lateral de resultados hasta cargar 20–40 fichas.
   - **Extract:** guardar Título y URL de cada ficha en Google Sheets.
3. Enlaza la segunda plantilla (**"Scrape Place Details from Google Maps"**) leyendo esas URLs desde Google Sheets para extraer teléfono, web, dirección y horario.

---

## 4. Page Agent y NexLev (para qué sirve cada uno)
- **Page Agent (`alibaba.github.io/page-agent/`):** agente GUI en lenguaje natural. La extensión de Chrome permite tareas multipestaña (`window.PAGE_AGENT_EXT` con token del panel lateral) para navegar entre Google Maps e Instagram sin escribir código.
- **NexLev (`docs.nexlev.io`):** orientado a **YouTube** (analítica de canales, nichos, transcripciones y conexión por API/MCP a n8n). Útil cuando captemos creadores de YouTube o Shorts, no para Google Maps ni Instagram.
