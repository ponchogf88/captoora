# 🎬 ESPECIFICACIÓN MAESTRA DE PRODUCCIÓN: MOTION 10S "EL DESTELLO" (CAPTO*RA SIGNATURE)

> **Destino:** Renderizado en Claude Opus 5.5 mediante Remotion / Three.js / React Spring a 60 FPS determinista puro.

---

## 1. Ficha Técnica

* **Nombre de la Pieza:** *The Flash & The Catchlight* (Capto*ra Signature Reveal).
* **Duración:** 10.0 segundos exactos (600 frames a 60 FPS).
* **Resolución:** 1080 × 1920 px (9:16 Vertical) y 1920 × 1080 px (16:9 Master).
* **Paleta:**
  * Background: `#030407` (Obsidian Void).
  * Spark / Flash: `#C6F135` (Lima Eléctrico) y `#FFFFFF` (Blanco Puro 6500K).
  * Typography: `#FFFFFF` (Primary), `rgba(255,255,255,0.4)` (Secondary).
  * Glass: `rgba(255,255,255,0.03)` con `backdrop-filter: blur(20px)`.

---

## 2. Timeline de Fotogramas Clave (60 FPS / 600 Frames)

| Frame | Tiempo | Fase | Acción Visual | Física / Parámetros |
| :--- | :--- | :--- | :--- | :--- |
| `000 - 150` | `0.0s - 2.5s` | **01. El Flash** | Pantalla negra $\rightarrow$ Explosión de estrella 4 puntas (`✦`) con dispersión de partículas de luz. | Escala $0 \rightarrow 1.8 \rightarrow 1.0$, resorte $\zeta = 0.50, f = 7.0\text{ Hz}$. |
| `150 - 300` | `2.5s - 5.0s` | **02. El Catchlight** | Zoom in macro al centro de la estrella; se integra al iris humano como reflejo pupilar. | Contracción de pupila $\zeta = 0.55, f = 6.0\text{ Hz}$. |
| `300 - 450` | `5.0s - 7.5s` | **03. La Chispa IA** | La estrella se desprende, muta a 8 puntas (`✶`), rota 360° con mallas vectoriales y retícula áurea. | Rotación continua `ease-in-out`, condensación de energía verde lima. |
| `450 - 600` | `7.5s - 10.0s` | **04. El Ensamble** | Aparece `CAPTO [ ] RA`. La estrella vuela y encaja en el hueco formando `CAPTO*RA`. Desliza `SIGNATURE`. | Impacto elástico en hueco $\zeta = 0.42, f = 9.0\text{ Hz}$. Fade in de *SIGNATURE*. |

---

## 3. Audio & SFX Design

* `t = 0.0s`: Click seco de obturador mecánico (1200 Hz, 8ms) + sub-bass 45 Hz en fade-in.
* `t = 2.5s`: Zumbido ascendente de capacitor de flash recargando (*flash recharge whine*).
* `t = 5.0s`: Glissando cristalino digital (frecuencias altas 4kHz - 8kHz).
* `t = 7.8s`: Impacto seco de resorte táctil (*thud* a 80 Hz) al encajar la estrella en el hueco + campana de cristal armónica.
