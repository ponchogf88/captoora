# PHOTODEV TOOLS — PLAN COMERCIAL & ARQUITECTURA DE PRODUCTO
**Ecosistema Inteligente de Control de Cámara y Asistencia Fotográfica con IA**
*Fecha de Formulación: Noviembre 2026 | Rama Oficial: `photodev-tools`*

---

## 1. El Diagnóstico del Mercado: ¿Qué existe y dónde está el dolor?

El mercado del software fotográfico está roto y fragmentado en 4 mundos que no se comunican entre sí:

| Categoría | Jugadores Actuales | Precio | Qué Hacen Bien | Dónde Fallan Críticamente |
|---|---|---|---|---|
| **Tethering Tradicional** | Capture One, Lightroom Classic, Smart Shooter 4 | $24–$30 USD/mes o $299 USD licencia | Conexión cableada estable, perfiles de color | **Cero IA en vivo**. Interfaz saturada con 300 botones. No controlan la cámara por intención humana ni voz. Curva de aprendizaje empinadísima. |
| **Retoque IA Post-Toma** | Evoto AI, Imagen AI, Aftershoot | $0.05–$0.10 USD / crédito o $35–$50/mes | Suavizado de piel, recorte, ojos | **Llegan demasiado tarde**. Trabajan después de que la foto ya se tomó. Si la foto salió movida, fuera de foco o mal iluminada, el crédito se desperdicia. No operan la cámara. |
| **Hardware "Asistente"** | Arsenal 2, CamRanger 2 | $200–$350 USD (dispositivo físico) | Transmisión Wi-Fi, time-lapses automáticos | Mala recepción en estudio, apps móviles lentas, no tienen dirección de arte, ni voz continua, ni resuelven fotografía comercial/volumen. |
| **Fotografía Escolar / Volumen** | GotPhoto, PhotoDay | 10% comisión por venta o $40 USD/mes | Tiendas en línea para padres de familia | La captura en set sigue siendo manual, engorrosa y desconectada del control de cámara inteligente. |

### 💥 La Oportunidad de Oro (El Océano Azul)
Ninguno de los competidores ofrece un **Asistente de Cámara Conversacional en Vivo**. 
Existe una barrera brutal: **el 80% de los fotógrafos amateurs avanzados, creadores y fotógrafos de estudio independientes se sienten abrumados por los menús arcaicos de sus cámaras (Canon, Nikon, Sony)** y no tienen para pagar a un segundo fotógrafo o asistente de iluminación que les cante los errores en el set.

---

## 2. La Propuesta de Valor: "No una navaja suiza saturada, sino un Director IA"

Para evitar el **síndrome de la navaja suiza** (pantallas saturadas que abruman al usuario), la arquitectura de **PhotoDev Tools** se basa en el patrón **AI Intent Router (Enrutador de Intenciones)**:

```
                  ┌────────────────────────────────────────┐
                  │          ENTRADA DEL USUARIO           │
                  │   (Voz en Vivo, Chat, o Botón Simple)  │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │       PHOTODEV AI AGENT ROUTER         │
                  │  (Entiende cámaras, lentes y técnica)  │
                  └───────────────────┬────────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         │                            │                            │
         ▼                            ▼                            ▼
┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
│ MOD 1: PILOTO   │          │ MOD 2: DIRECTOR │          │ MOD 3: VOLUMEN  │
│ CERO-MENÚS      │          │ ÓPTICO EN VIVO  │          │ & SESIONES      │
│ (ISO/f/Shutter) │          │ (Foco/Luz/Pose) │          │ (QR/Colegios)   │
└─────────────────┘          └─────────────────┘          └─────────────────┘
```

El usuario nunca ve menús de 4 niveles. Solo tiene una pantalla limpia estilo **Apple Liquid Glass** con un visor central. Cuando dice o escribe:
* *"Quiero fondo borroso"* ➔ El Router activa el módulo de diafragma y abre a `f/2.0` vía USB/Wi-Fi.
* *"¿Cómo salió la luz?"* ➔ El Router activa la telemetría óptica y canta el ratio Key-to-Fill y recorte de altas luces.
* *"Siguiente alumno: Carlos Pérez"* ➔ El Router etiqueta la foto con el ID escolar mediante el módulo de volumen.

---

## 3. Modelo de Negocio y Monetización a Corto Plazo

Para generar ingresos inmediatos y flujo de efectivo sin fricción, se estructura en 3 niveles de monetización:

### Nivel 1: PhotoDev Starter (Gratis / Freemium — Gancho de Adopción)
* **Objetivo:** Adquisición masiva y viralidad en redes (TikTok, YouTube, comunidades fotográficas).
* **Incluye:**
  * Tethering USB básico con visor en pantalla completa.
  * El **Antimanual Interactivo de Cámaras** (Canon, Nikon, Sony) para aprender qué hace cada botón físico viendo ejemplos reales.
  * 15 disparos por voz al día.

### Nivel 2: PhotoDev Pro Creator ($19 USD / mes o $149 USD / año)
* **Público:** Fotógrafos de retrato, bodas, creadores de contenido, fotógrafos de estudio individuales.
* **Incluye:**
  * **Disparos por Voz LIVE Ilimitados** (manos libres en el set).
  * **Piloto Automático Cero-Menús**: traducción de intenciones a comandos PTP/CCAPI (ajuste automático de ISO, apertura, velocidad y balance de blancos).
  * **Director Óptico con IA Multimodal**: diagnóstico en tiempo real de foco en ojos, ratio de iluminación, clipping de luces altas y advertencias de trepidación.
  * Guías dinámicas de encuadre (Zero-Crop 4:5 para Instagram, 16:9, portadas).

### Nivel 3: PhotoDev Studio & Volume ($49 USD / mes o $399 USD / año)
* **Público:** Estudios comerciales, agencias de modelaje, fotografía escolar (colegios/graduaciones) y eventos masivos.
* **Incluye:**
  * Todo lo del plan Pro.
  * **Workflow Escolar y de Eventos con QR/Códigos de Barra**: escaneo previo a la toma que vincula automáticamente los RAWs y JPGs al nombre y matrícula del alumno.
  * **Multi-Cámara Tethering**: soporte para hasta 3 cámaras conectadas en paralelo (ej. plano entero + plano cerrado).
  * **Live Proofing / Galería de Selección Instantánea** para clientes en iPad/tablet en el set mientras se dispara.

---

## 4. Estrategia de Comunicación: "Cero Mención de IA — Solo Óptica y Tecnología de Punta"

> [!IMPORTANT]
> **REGLA DE ORO DE CAPTOORA / PHOTODEV TOOLS:**
> En fotografía profesional, la palabra "Inteligencia Artificial" (IA) está satanizada porque abarata la percepción del trabajo ("si es IA, lo hace un filtro y no vale nada").
> **JAMÁS** usamos el término "IA" de cara al cliente final (colegios, familias, clientes comerciales).
> **Tampoco atacamos errores ajenos** (no hablamos de fotógrafos que se equivocan).
> **Siempre comunicamos en positivo, resaltando tecnología de punta, fidelidad óptica real y entregas récord:**

1. **La Propuesta de Valor para Colegios / Familias (B2B Local):**
   > *"En Captoora contamos con una arquitectura de captura digital de alta velocidad y fidelidad óptica calibrada: cada alumno cuenta con su propia galería digital privada en alta resolución protegida con acceso individual, asegurando tiempos de entrega récord en menos de 48 horas sin retrasar las actividades del colegio."*

2. **La Oferta para Fotógrafos / Creadores (SaaS B2B):**
   > *"PhotoDev Tools: Conecta tu cámara réflex o mirrorless (Canon, Nikon, Sony) y toma el control total en tiempo real sin perder tiempo en menús. Disparo con manos libres, calibración lumínica instantánea y visualización de ultra-definición directo en tu monitor."*

---

## 5. Hoja de Ruta de Implementación en la Rama `photodev-tools`

- [x] **Fase 0: Creación de la rama `photodev-tools`** en Git.
- [ ] **Fase 1: Motor Universal Multi-Cámara** (Abstracción limpia para Canon PTP, Nikon PTP y Canon CCAPI Wi-Fi).
- [ ] **Fase 2: Arquitectura de Micro-Módulos con AI Router** (Desacoplar la UI para que sea minimalista estilo Apple Liquid Glass con el Halo Cursor de Antigravity).
- [ ] **Fase 3: Módulo de Fotografía Escolar/Volumen** (Lector QR/Código de barras por webcam o escáner USB + roster CSV).
- [x] **Fase 4: Landing Page Comercial de PhotoDev Tools** con demo interactiva y pasarela de pago (Stripe).
