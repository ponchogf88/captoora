# 📱 CAPTOORA STUDIO — GUÍA TÉCNICA E INTEGRACIÓN: WHATSAPP BUSINESS API & OPEN SOURCE

**Fecha:** 20 de Octubre de 2026  
**Ecosistema:** Captoora Studio & Captoora Biometrics  
**Objetivo:** Conectar WhatsApp con modelos de razonamiento (Grokbot, Antigravity, Codex o modelos locales) para atención de clientes, prospección y agendamiento de influencers.

---

## 1. Estado del Arte: ¿Cuál es el repositorio viral en X / GitHub?

En las últimas semanas, la comunidad de IA y automatización en X (Twitter) ha destacado principalmente dos soluciones libres para WhatsApp:

### A. **Evolution API v2 (`EvolutionAPI/evolution-api`) — LA RECOMENDADA #1**
- **Qué es:** Microservicio open-source en Node.js/TypeScript que convierte cualquier número de WhatsApp en una API REST moderna.
- **Bajo el capó:** Utiliza la librería **Baileys**, conectándose directo por WebSockets al protocolo multi-dispositivo de WhatsApp. **No usa Puppeteer ni Chrome**, lo que consume apenas ~150 MB de RAM (ideal para Mac M1).
- **Ventajas:**
  - Viene con interfaz web (Manager), documentación Swagger interactiva y soporte multi-instancia (puedes conectar varios números a la vez).
  - Webhooks nativos para recibir mensajes en tiempo real y enviarlos a Python, FastAPI, n8n, LangChain o agentes locales.
  - Soporta texto, audios con PTT (Push-To-Talk), imágenes, catálogos, botones y documentos.
- **Repositorio:** `https://github.com/EvolutionAPI/evolution-api`

### B. **Baileys (`whiskeysockets/baileys`)**
- **Qué es:** La biblioteca fundamental y más depurada de ingeniería inversa del protocolo WebSocket de WhatsApp.
- **Ventajas:** Máxima ligereza y control total en código.
- **Desventaja:** Requiere construir el servidor REST y la base de datos de sesiones manualmente (Evolution API ya lo resolvió por completo).

### C. **WhatsApp Cloud API (Meta Oficial)**
- **Qué es:** La API oficial de Meta para desarrolladores (`graph.facebook.com/v21.0/`).
- **Ventajas:** **Cero riesgo de baneo.** Primeras 1,000 conversaciones de servicio al mes son 100% gratis.
- **Desventaja:** Requiere verificación de empresa en Meta Business Suite para escalar y plantillas pre-aprobadas para iniciar conversaciones.

---

## 2. Despliegue en 1 Clic con Docker (Evolution API)

Para tener WhatsApp Business API corriendo en tu Mac M1 o en un VPS económico (DigitalOcean/Hetzner):

Crea un archivo `docker-compose.yml`:

```yaml
version: '3.8'

services:
  evolution-api:
    image: atendai/evolution-api:v2.1.1
    container_name: evolution_api
    restart: always
    ports:
      - "8080:8080"
    environment:
      - SERVER_URL=http://localhost:8080
      - AUTHENTICATION_API_KEY=captoora_secret_api_key_2026
      - DATABASE_PROVIDER=local
      - CACHE_REDIS_ENABLED=false
      - WEBHOOK_GLOBAL_ENABLED=true
      - WEBHOOK_GLOBAL_URL=http://host.docker.internal:5000/webhook/whatsapp
    volumes:
      - ./evolution_instances:/evolution/instances
      - ./evolution_store:/evolution/store
```

Ejecución:
```bash
docker compose up -d
```
Luego abres `http://localhost:8080/manager` y escaneas el código QR desde tu app de WhatsApp en el celular (WhatsApp Business o normal). ¡Listo! Tu WhatsApp ya tiene API REST completa.

---

## 3. Protocolo Anti-Baneo (Reglas de Oro)

1. **Jitter y Retardos Humanos:** Nunca respondas en 0.1 segundos. Simula un delay de 3 a 8 segundos antes de enviar texto.
2. **Envío de estado `composing`:** Muestra "Escribiendo..." (`/chat/sendPresence`) durante 2 a 4 segundos antes de mandar el mensaje.
3. **Calentamiento de Número (Warm-up):**
   - Días 1 a 3: Máximo 20 conversaciones diarias.
   - Días 4 a 7: Máximo 50 conversaciones diarias.
   - Semana 2+: Respuestas ilimitadas a mensajes entrantes (Inbound), pero nunca hagas spam masivo no solicitado a números que no te tienen guardado.

---

## 4. Arquitectura de Conexión con Modelos de Razonamiento

```
WhatsApp Usuario (Cliente/Influencer)
              │
              ▼
    Evolution API / Meta API (Puerto 8080)
              │ (Webhook HTTP POST)
              ▼
   Agente Captoora Python (FastAPI / `whatsapp_client.py`)
              │
              ├── Memoria de Conversación (Historial de sesión)
              ├── Consulta de Calendario (Slots disponibles para 25 chicas)
              └── Inferencia con LLM (Prompt de Negociación y Cierre)
              │
              ▼
   Respuesta formateada -> Evolution API -> WhatsApp Usuario
```
