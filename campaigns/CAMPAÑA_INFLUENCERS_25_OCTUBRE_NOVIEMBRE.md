# 🍂 CAPTOORA STUDIO — MASTER PLAN: CAMPAÑA 25 INFLUENCERS
## Temporada: Pumpkin Patch, Halloween, Día de Muertos y Grabación UGC
**Fecha de lanzamiento:** 20 de Octubre de 2026  
**Lugar:** Captoora Studio (Amapola Eventos, Monterrey)  
**Objetivo:** Disparar la visibilidad de la marca, saturar las redes con contenido visual de alto nivel y posicionar a Captoora como el estudio fotográfico de referencia para creadores de contenido.

---

### 1. MODELO DE INTERCAMBIO (CREATIVE BARTER AGREEMENT)

Para garantizar un retorno de inversión (ROI) masivo y profesionalismo mutuo:

| Captoora Entrega | La Creadora / Influencer Entrega |
| :--- | :--- |
| **Sesión de 45 minutos** en set temático profesional con dirección de poses. | **1 Post en Colaboración (Collab Post)** en feed de Instagram (carrusel de 3 a 5 fotos). |
| **5 Fotografías Finales en Alta Resolución** (Master Retouch, piel radiante, ciclorama o set limpio). | **1 Reel / TikTok de Behind The Scenes** mostrando la experiencia y etiquetando @captoora. |
| **Acceso el mismo día a Galería Digital** para previsualización y selección guiada. | **Mínimo 3 Stories en vivo** durante la sesión y 2 Stories al recibir la entrega final. |
| **Clips de video crudo 4K (9:16)** para que creen sus propios videos dinámicos. | Compromiso de mención explícita: *"Fotografía por @captoora"*. |

---

### 2. LOS 4 SETS Y TEMÁTICAS VISUALES

```
                          ┌───────────────────────────┐
                          │   TEMPORADA OTOÑO 2026    │
                          └─────────────┬─────────────┘
                                        │
      ┌──────────────────┬──────────────┴──────────────┬──────────────────┐
      ▼                  ▼                             ▼                  ▼
1. PUMPKIN PATCH   2. HALLOWEEN FASHION       3. DÍA DE MUERTOS     4. UGC / GRABACIÓN
• Fardos de paja   • Fondos oscuros / Gel     • Flores Cempasúchil  • Micro-vlogs BTS
• Variedad calabaza• Iluminación teatral      • Velas led y copal   • Audios virales
• Tonos cálidos/suave• Moda editorial         • Maquillaje Catrina  • Contenido dinámico
```

#### A. Set 1: Pumpkin Patch & Cozy Autumn
- **Estética:** Otoñal cálido, madera, fardos de heno, calabazas de distintos tamaños, cobijas de lana tejida, suéteres en tonos mostaza, terracota y verde oliva.
- **Iluminación:** Luz suave envolvente tipo ventana grande (Softbox octogonal de 120cm) + luz de contra cálida (Rim light a 3200K) para brillo en cabello.
- **Preset de Revelado sugerido:** `final_calido` (+14 Temp, +0.18 EV, +20 Sombras).

#### B. Set 2: Halloween Creative & Costume Fashion
- **Estética:** Retrato editorial de alta costura con disfraces trabajados. Nada de disfraces desechables; enfoque en glamour, vampiros modernos, cine clásico o fantasía.
- **Iluminación:** Esquema dramático tipo Rembrandt o Clamshell con geles de color (rojo carmín, magenta o ámbar profundo).
- **Preset de Revelado sugerido:** `transicion_equilibrada` o contraste medio-alto.

#### C. Set 3: Día de Muertos (Tradición y Elegancia)
- **Estética:** Altares contemporáneos, alfombra de pétalos de cempasúchil, elementos de barro negro, coronas florales artesanales y maquillaje editorial de Catrina.
- **Iluminación:** Luz cálida inspirada en la llama de las velas, fondo limpio para aislar la riqueza textil y el tocado.
- **Preset de Revelado sugerido:** `final_calido` con altas luces controladas para respetar el maquillaje blanco.

#### D. Set 4: Behind The Scenes (Grabación Continua)
- **Cámara fija Eufy:** Registro 24/7 en plano cenital / angular para alimentar el motor de Daily Vlogs.
- **Grabación móvil en estabilizador:** Tomas de 3 a 5 segundos de la interacción con el fotógrafo, risas, detalles de cámara y reacciones de las chicas.

---

### 3. CRONOGRAMA DE SLOTS (25 CREADORAS)

Se agendan bloques de 1 hora (45 min de disparo efectivo + 15 min de sanitización y cambio de set):

- **Viernes 23 de Octubre (Tarde):** 5 slots (2:00 PM a 7:00 PM) -> *Pumpkin Patch focus*
- **Sábado 24 de Octubre (Día completo):** 8 slots (10:00 AM a 7:00 PM) -> *Halloween & Fashion*
- **Domingo 25 de Octubre (Día completo):** 8 slots (10:00 AM a 7:00 PM) -> *Día de Muertos & Tradición*
- **Lunes 26 de Octubre (Tarde):** 4 slots (3:00 PM a 7:00 PM) -> *Sesiones VIP / Reagendadas*

---

### 4. PIPELINE DE PRODUCCIÓN ULTRA-RÁPIDO

1. **Disparo en Tethering con Nikon D3500:**
   Las fotos entran directamente a la computadora de control en el estudio.
2. **Curaduría Inmediata con `dev_event_curator`:**
   En 5 minutos tras finalizar la sesión, se cargan las 150 fotos del disparo en el servidor local `http://127.0.0.1:8855`. Se filtran parpadeos, se revisan expresiones espontáneas y la influencer pre-selecciona sus 5 favoritas con las teclas `1` y `2`.
3. **Revelado Batch en 3 Minutos:**
   Se aplica la receta tonal correspondiente (`inicio_fresco`, `transicion_equilibrada` o `final_calido`) y se exportan copias maestras en alta resolución.
4. **Entrega Digital el Mismo Día:**
   Las 5 fotos aprobadas se suben a la galería del cliente para descarga inmediata en su smartphone.
