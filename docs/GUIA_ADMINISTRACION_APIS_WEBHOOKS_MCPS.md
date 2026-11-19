# Guía de Administración: APIs, Contraseñas, Webhooks y MCPs (`Captoora 7 Agentes`)

Archivo maestro para configurar tus accesos antes o durante el despliegue de los **7 Agentes Ejecutivos**.

> **Regla de Oro de Seguridad:** Nunca pegues contraseñas o tokens directamente en el chat si puedes guardarlos en [`.env`](file:///Users/imac/Documents/antigravity/epic-bohr/.env) o `~/.gemini/config/mcp_config.json`. Tu archivo `.env` está protegido en `.gitignore` y nunca se sube a Git.

---

## 1. Archivo donde pegar todas tus APIs y Contraseñas

Abre directamente: **[`.env`](file:///Users/imac/Documents/antigravity/epic-bohr/.env)** en este proyecto. Ahí ya están creados todos los espacios con comentarios claros.

### Qué significa cada campo (por orden de prioridad)

| Prioridad | Variable en `.env` | Para qué sirve | Dónde la sacas |
|---|---|---|---|
| **1 · Hoy** | `SMTP_PASS` | Enviar correos HTML + PDF desde **`chuy@captoora.studio`** | Zoho Security → App Passwords (`https://accounts.zoho.com/home#security/app_password`) |
| **1 · Hoy** | `CALENDLY_BASE_URL` | Crear enlaces de Calendly personalizados por cliente | Tu link principal de Calendly (ej. `https://calendly.com/tu-usuario`) |
| **2 · Pronto** | `CALENDLY_API_TOKEN` | Leer citas confirmadas automáticamente desde Calendly | Calendly → Integrations → API & Webhooks → Personal Access Token |
| **2 · Pronto** | `GHL_WEBHOOK_URL` | Enviar leads, estatus KYC y citas directo a **GoHighLevel** | GoHighLevel → Automation → Workflows → Trigger `Inbound Webhook` (copiar URL) |
| **2 · Pronto** | `GHL_API_KEY` / `GHL_LOCATION_ID` | Sincronía directa con tu subcuenta GoHighLevel (CRM / Pipelines) | GoHighLevel → Settings → Business Profile / Private Integrations |
| **2 · Pronto** | `MAILERFIND_API_KEY` | Enriquecer correos B2B con MailerFind | Tu panel de MailerFind → API / Integrations |
| **3 · Auto WA** | `WHATSAPP_CLOUD_TOKEN` + `WHATSAPP_PHONE_NUMBER_ID` | Enviar WhatsApp + PDFs automático sin abrir `wa.me` | Meta for Developers → Tu App → WhatsApp → API Setup |
| **Ya activo** | `APIFY_TOKEN` | Peinar zonas de NL con el Buscador Apify | Apify Console → Settings → Integrations (ya existe token respaldo en `run_apify_production.py`) |
| **Opcional** | `GEMINI_API_KEY` | Usar SDK en la nube (si queda vacío corre nuestro motor local **$0 tokens**) | Google AI Studio (`aistudio.google.com`) |
| **Opcional** | `GMAIL_USER` / `GMAIL_APP_PASSWORD` | Envío respaldo desde cuenta Gmail | Cuenta Google → Seguridad → Verificación en 2 pasos → Contraseñas de aplicaciones |
| **Opcional** | `GDRIVE_FOLDER_ID` + `GOOGLE_OAUTH_*` | Respaldar reportes PDF / dossiers en Google Drive | Google Cloud Console → APIs & Services → Credenciales OAuth |

---

## 2. Los 2 Webhooks (Cómo conectar GoHighLevel / Calendly / WhatsApp en tiempo real)

Para que el sistema funcione en **dos vías** (que mande datos y también registre solo cuando un cliente contesta o agenda cita):

1. **Webhook #1 (Saliente: Captoora ➜ GoHighLevel / Zapier / Make):**
   - Pega en `.env`: `GHL_WEBHOOK_URL=https://services.leadconnectorhq.com/hooks/...`
   - Cada vez que un lead cambia de etapa en tu CRM/KYC o pide enlace Calendly, nuestro backend envía un JSON automático hacia GoHighLevel.

2. **Webhook #2 (Entrante: Calendly / WhatsApp / GHL ➜ Captoora `:8765`):**
   - Si quieres que **Calendly**, **Meta WhatsApp** o **GoHighLevel** actualicen automáticamente en tu tablero quién **"Contestó"** o **"Agendó cita"** sin que tú lo marques a mano, necesitas exponer temporalmente el puerto local `:8765` a internet con un túnel gratuito (ej. `cloudflared tunnel --url http://127.0.0.1:8765`).
   - Las rutas receptoras quedarán en `/api/webhooks/...` protegidas por `CAPTOORA_WEBHOOK_SECRET`.
   - *(Si todavía no quieres abrir túnel ni usar APIs, no te detiene: el tablero CRM incluirá botones de 1 clic para registrar "Enviado / Contestó / Cita" manualmente desde tu pantalla).*

---

## 3. Cómo agregar tus MCPs (MailerFind, Gmail, Google Drive) en Antigravity

Ahorita Antigravity solo tiene montados los MCPs de documentación y notebooks (`gemini-api-docs`, `dak-notebook`, `dak-viz`). Para darnos acceso a **MailerFind MCP**, **Gmail MCP** y **Google Drive MCP** aquí en tu Mac:

### Archivo oficial de configuración MCP en Antigravity
Edita o crea el archivo global en tu Mac:
`~/.gemini/config/mcp_config.json`

*(También puedes abrirlo en la interfaz de Antigravity entrando a **`...` (Additional Options) → `MCP Servers`**).*

### Estructura estándar (`Stdio` local o `SSE` remoto)
```json
{
  "mcpServers": {
    "mailerfind": {
      "serverUrl": "PEGA_AQUI_TU_URL_SSE_DE_MAILERFIND_SI_TE_DAN_LINK_REMOTO"
    },
    "gmail": {
      "command": "npx",
      "args": ["-y", "@gongrzhe/server-gmail-autoauth-mcp"],
      "env": {}
    },
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"],
      "env": {
        "GDRIVE_CREDENTIALS_PATH": "/Users/imac/.gemini/gdrive-credentials.json"
      }
    }
  }
}
```
> **Importante:** En cuanto pegues la configuración de cualquier MCP en `~/.gemini/config/mcp_config.json` y reinicies/recargues el cliente MCP en `... → MCP Servers`, aparecerán sus herramientas disponibles automáticamente en la siguiente sesión o recarga.
> **Nota sobre Google Cloud / Gmail / Drive:** Si quieres que hagamos primero la credencial OAuth de Google (`client_secret.json`) sin complicarte, solo dime y revisamos si ya tienes proyecto en Google Cloud (`gcloud`) o prefieres usar primero **Zoho Mail (`chuy@captoora.studio`) + Extractor Propio de Correos**.

---

## 4. Qué hacer ahorita para avanzar rápido
1. Abre **[`.env`](file:///Users/imac/Documents/antigravity/epic-bohr/.env)** y pega lo que ya tengas a la mano (con solo **`SMTP_PASS` de Zoho** y tu **`CALENDLY_BASE_URL`** ya podemos operar al 100% desde el primer día).
2. Dime cuando hayas guardado `.env` (sin pegarme las contraseñas en el chat si prefieres mantenerlas privadas) **o** dime cuáles integraciones prefieres conectar después, y arrancamos de inmediato con la construcción de los **7 Agentes Ejecutivos**.
