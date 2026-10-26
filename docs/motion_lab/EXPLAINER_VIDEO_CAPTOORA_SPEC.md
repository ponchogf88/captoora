# 🎬 EXPLAINER VIDEO CAPTOORA STUDIO — ESPECIFICACIÓN MAESTRA OPUS 5.5

> **Objetivo:** Video explicativo de alto impacto (25 a 30 segundos) estilo Linear / Duolingo / Apple que presenta Captoora Studio en Colinas de San Jerónimo, su filosofía de iluminación, los 3 sets físicos y la Academia de Foto + IA.

---

## 1. Guión Técnico y Storyboard Beat por Beat (25 Segundos)

| Beat | Tiempo | Escena Visual (60 FPS) | Locución en Off (Voiceover) | Audio SFX & Háptica |
| :--- | :--- | :--- | :--- | :--- |
| **01** | `00:00 - 00:05` | **La Penumbra:** Fondo *Dark Void* absoluto. Una partícula de luz vibra en el centro y se expande en bokeh sutil. Tipografía gigante entra con fade elástico. | *"Para ser el amo y señor de la luz... primero tienes que dominar la oscuridad."* | Frecuencia grave sub-bass (50 Hz) que sube progresivamente. |
| **02** | `00:05 - 00:10` | **El Diafragma Mecánico:** Aparece el monograma de Captoora; la 'O' se transforma en un diafragma de 6 palas que gira 45° y abre su apertura en resorte ($\zeta = 0.45$). | *"Captoora Studio. No es otra sesión de fotos aburrida. Es el carácter que tu marca merece."* | Click mecánico de obturador de cámara analógica (1200 Hz). |
| **03** | `00:10 - 00:15` | **El Espacio Físico:** Transición a vista de los 3 sets en San Jerónimo + el parque contiguo. Tarjetas de vidrio ahumado (*glassmorphism*) flotando en 3D. | *"Tres escenarios profesionales y luz natural exterior en Colinas de San Jerónimo. Dos atmósferas, cero traslados."* | Sonido sutil de aire / swish de lente en movimiento. |
| **04** | `00:15 - 00:20` | **La Oferta Dual:** Dos tarjetas táctiles con rebote de keycap. Izquierda: Combo Studio + Clips ($1,600). Derecha: Academia Foto & IA (Taller $500). | *"Ven a vivir tu sesión guiada o aprende en nuestro taller a fotografiar tus propios productos con tu celular."* | Dos clicks táctiles en sincronía con la aparición de tarjetas. |
| **05** | `00:20 - 00:25` | **Cierre & Acción:** Botón verde lima eléctrico que pulsa suavemente. Logo completo de Captoora y WhatsApp `81 4005 0088`. | *"Momentos que permanecen. Escríbenos por WhatsApp y agenda tu fecha hoy."* | Chime armónico de confirmación y obturador final. |

---

## 2. Sistema de Diseño Visual (Dark Void + Lima Captoora)

* **Fondo Principal:** `#030407` (Negro obsidiana con viñeteado sutil).
* **Color de Acento:** `#C6F135` (Verde lima eléctrico de alto contraste).
* **Superficies:** `rgba(255, 255, 255, 0.04)` con `backdrop-filter: blur(16px)` y bordes de `1px solid rgba(255,255,255,0.08)`.
* **Tipografía:** SF Pro Display / Inter Bold para jerarquía cinematográfica.
* **Física de Movimiento:** Oscilador armónico amortiguado con frecuencia de $8.5\text{ Hz}$ y $\zeta = 0.45$ para respuesta táctil inmediata.

---

## 3. Mockup Interactivo Local (Pruébalo en tu Mac)

Ya tienes el storyboard interactivo y funcional corriendo en tu máquina:
👉 **[captoora_explainer_mockup.html](file:///Users/imac/Library/Mobile%20Documents/com~apple~CloudDocs/Desktop/Projects/CAPTOORA.STUDIO/docs/motion_lab/captoora_explainer_mockup.html)**

* Trae los 5 beats navegables en tiempo real.
* Sintetizador de audio Web Audio API que reproduce el click de cámara real.
* Apertura de diafragma mecánico interactiva.

---

## 4. Prompt Maestro para Claude Opus 5.5 (Listo para Copiar y Pegar)

Pega el siguiente prompt íntegro en Claude Opus 5.5 para que te genere el código de renderizado determinista a 60 FPS:

```markdown
ROLE: Lead Creative Technologist & Motion Engineer (@skunzu / @flxrnc pipeline).
GOAL: Write the deterministic 60 FPS animation code for the Captoora Studio Explainer Video (25s) using Remotion / React Three Fiber / Framer Motion.

SPECIFICATIONS:
1. ARCHITECTURE: Pure seek(t) function evaluation. No wall-clock timestamps.
2. DESIGN SYSTEM: Captoora Dark Void:
   - Background: #030407 (deep obsidian void)
   - Primary Accent: #C6F135 (electric lime)
   - Glass Cards: rgba(255,255,255,0.04) with border: 1px solid rgba(255,255,255,0.08) and backdrop blur.
   - Brand Rule: Zero crop on human subjects and products (Ley Visual Captoora).

3. BEAT TIMELINE:
   - Beat 01 (0.0s - 5.0s): Dark void expansion, central light seed pulsing, quote "Para ser el amo y señor de la luz... primero tienes que dominar la oscuridad."
   - Beat 02 (5.0s - 10.0s): Camera aperture iris rotation (6 blades, scale 1.0 -> 1.15, rotation 45deg, spring zeta=0.45, f=8.0Hz). Logo reveal: Captoora Studio.
   - Beat 03 (10.0s - 15.0s): 3D Parallax floating location card: "Colinas de San Jerónimo 165", 3 studio sets + outdoor park badge.
   - Beat 04 (15.0s - 20.0s): Dual tactical cards bounce into frame (Combo Clips $1,600 / Academia Foto + IA $500).
   - Beat 05 (20.0s - 25.0s): Outro spring lock. CTA button "Agendar por WhatsApp (81 4005 0088)", acoustic shutter tick SFX at t=21.0s.

DELIVERABLE: Complete production-ready TypeScript component and Remotion composition exporting at 1080x1920 (9:16 Reels) and 1920x1080 (16:9 Web) at 60 FPS with ffmpeg libx264 settings.
```
