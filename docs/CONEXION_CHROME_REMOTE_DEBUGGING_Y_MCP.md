# Conexión entre Antigravity y Google Chrome (Remote Debugging + MCP + Playwright)

## 1. Lo que sí podemos automatizar y los límites de seguridad
- **No se eliminan candados de seguridad ni advertencias anti-bot:** por diseño de Chrome y del entorno de Antigravity, no es posible saltarse el aviso de autorización de Chrome al conectar depuración remota, ni evadir CAPTCHAs, muros de login o controles anti-automatización de sitios externos.
- **Cómo reducir interrupciones de forma oficial:** dentro de Antigravity puedes elegir el nivel de permisos que prefieras en su configuración oficial (ver sección 4).

---

## 2. Qué ya quedó configurado en este workspace
Se creó [`.agents/mcp_config.json`](../.agents/mcp_config.json) con dos servidores MCP oficiales listos:
1. **`chrome-devtools`** (`chrome-devtools-mcp@latest --autoConnect --categoryExtensions`): pensado para conectarse a tu **Google Chrome 150** actual (conservando tus extensiones como BrowserFlow, Page Agent y NexLev).
2. **`playwright`** (`@playwright/mcp@latest --cdp-endpoint http://127.0.0.1:9222`): pensado para conectarse por puerto `9222` a una instancia lanzada con Remote Debugging Port.

Si quieres que estos servidores estén disponibles en **todos** tus proyectos (no solo en este repositorio), copia el mismo JSON a `~/.gemini/config/mcp_config.json` o agrégalos desde **Antigravity App → `Customizations` → `Installed` → `MCP Servers` → `Add MCP Server (+)`** (o **Antigravity IDE → `…` → `MCP Servers` → `Manage MCP Servers` → `View raw config`**) y reinicia la sesión.

---

## 3. Dos formas oficiales de abrir el canal con Google Chrome

### Opción A · Conectar a tu Chrome actual (`--autoConnect`, sin perder tus extensiones)
Recomendada para **Chrome DevTools MCP** y `/browser` en Antigravity IDE:
1. En tu Google Chrome actual (versión 150.x), abre una pestaña nueva y entra a:
   `chrome://inspect/#remote-debugging`
2. Activa la casilla **"Allow remote debugging for this browser instance"**.
3. Reinicia tu sesión de Antigravity para que cargue [`.agents/mcp_config.json`](../.agents/mcp_config.json) (o `~/.gemini/config/mcp_config.json`).
4. Cuando el agente llame por primera vez a Chrome (por ejemplo con `/browser` en el IDE), Chrome mostrará una ventana pidiendo confirmación: haz clic en **"Allow"** dentro de los **60 segundos**.

### Opción B · Puerto explícito `9222` (`--remote-debugging-port=9222`, para Playwright MCP)
Desde Chrome 136+, Google Chrome exige un directorio `--user-data-dir` separado del perfil por defecto para abrir el puerto `9222`.
1. Ejecuta en tu terminal:
   ```bash
   ./scripts/launch_chrome_debug_9222.sh
   ```
2. Verifica que el puerto esté escuchando abriendo `http://127.0.0.1:9222/json/version`.
3. En esa ventana inicia sesión o instala las extensiones que quieras usar en segundo plano; **`playwright` (`@playwright/mcp`)** se conectará directo a `http://127.0.0.1:9222`.

> **Nota sobre Antigravity App (2.0):** si usas Antigravity App `v2.30.0+` con cuenta personal de Google, incluye un navegador integrado en el panel lateral sin necesidad de configurar puerto remoto; en Antigravity IDE el navegador local siempre se invoca con `/browser <tarea>`.

---

## 4. Configuración oficial de permisos en Antigravity (sin modificar archivos internos a mano)
- **Antigravity App (2.0):** `Settings` → `General` → `Global Permissions` → `Permission Preset` (`Request Review`, `Default`, `Auto`, `Turbo`). Puedes ajustarlo globalmente o solo para este proyecto.
- **Antigravity IDE (`Browser`):** barra de estado `Antigravity` → `Open Settings` → `Browser` para definir `Enable Browser Tools`, `Browser Javascript Execution Policy` (`Request Review` / `Always Proceed` / `Disabled`) y `Browser Actuation Rules`.
