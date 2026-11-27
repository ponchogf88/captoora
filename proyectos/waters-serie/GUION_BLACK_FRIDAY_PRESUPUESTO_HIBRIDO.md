# Guion Híbrido Black Friday · `WATERS_013` (`PRESUPUESTO`)

- **Composición Remotion:** `HybridBlackFridayBF01` (`1920×1080` · `30 fps` · `92.0 s` · **Master limpio 16:9 SIN subtítulos quemados abajo**, diseñado para meter directo a **OpusClip** + **Captions**).
- **Objetivo social:** Evitar que empresarios, desarrolladores y abogados amanezcan con cargos sorpresa de `$2,000 USD` (`~$40,000 MXN`) por activar pruebas gratis y APIs de IA en Black Friday sin topes de gasto.
- **Palabra clave CTA:** `PRESUPUESTO`

---

## Estructura en 5 Actos (optimizada para 3–4 clips en OpusClip)

| Acto | Tiempo | Visual en Pantalla | Qué dices tú (Guion) |
| --- | --- | --- | --- |
| **1. Hook Black Friday** | `0:00 – 0:12` | **Tú a pantalla completa** + Alerta Roja superior (`NO METAS TU TARJETA ASÍ · -$40,000 MXN EN 1 NOCHE`) + flecha `AUTO-RECHARGE ON` | *"Hoy es Black Friday y media ciudad está metiendo su tarjeta en pruebas gratis y APIs de IA... pero un solo botón apagado te puede despertar mañana con 40,000 pesos cobrados en el banco."* |
| **2. La Cajita en Bucle** | `0:12 – 0:32` | **Tú a la izquierda** + **Cajita interactiva Gemini/Claude/ChatGPT** escribiéndose en vivo a la derecha (`Attempt #10,000 · Auto-Recharge ON`) | *"Dejas corriendo tu primer agente o automatización en la noche con la tarjeta de tu negocio. Un error tonto de programación mete al bot en bucle infinito: se reintenta 10,000 veces en cuatro horas mientras duermes."* |
| **3. La Gráfica Mortal** | `0:32 – 0:54` | `32–44s`: **Tú a la izquierda + Gráfica `$0 → $2,000 USD`** con flechas animadas (`2 AM $420 → 4 AM $1,250 → 6 AM $2,000`).<br>`44–54s`: **Toy-Prop 3D (`SemiGauge3D` + sirena roja)** + **Tú en esquina PiP arriba-derecha** | *"Así sube el cobro: a las 2 de la mañana van 420 dólares, a las 4 ya cruzaste 1,250, y a las 6 amaneces con 2,000 dólares quemados porque el Auto-Recharge siguió cobrando sin pedirte permiso."* |
| **4. Dilema 3D** | `0:54 – 1:12` | **Toy-Prop 3D (`BinaryDoors3D`)**: Puerta `1 TARJETA DIRECTA` vs Puerta `2 TOPE + VIRTUAL` + **Tú en esquina PiP** | *"Hoy en Black Friday tienes dos puertas: meter tu tarjeta principal directo y rezar que nada falle, o blindarte en 3 minutos antes de dar clic."* |
| **5. Los 3 Candados + CTA** | `1:12 – 1:32` | `72–84s`: **Toy-Prop 3D (`GiantClipboard3D`)** palomeando 3 candados + **Tú en PiP**.<br>`84–92s`: **Corte final a ti Fullscreen** + badge `COMENTA: PRESUPUESTO` | *"1: activa Hard Monthly Limit en tu consola de Gemini, Anthropic u OpenAI. 2: usa tarjeta virtual topada. 3: exige aprobación humana arriba de 10 ejecuciones. Comenta PRESUPUESTO y te paso la guía exacta."* |

---

## 4 Micro-Clips para tu Rama de Gemini (copiar y pegar tal cual)

Genera clips cortos (`8–10 s` cada uno) manteniendo tu **rama oficial (muro concreto oscuro + polo negra)** para extraer los `4–6 s` donde mejor se muevan manos y labios:

| Clip | Archivo destino en repo | Prompt exacto en tu rama de Gemini | Tramo limpio a recortar |
| --- | --- | --- | --- |
| **Clip 1 (Hook)** | `public/avatar/bf01_hook.mp4` | Same character, black polo, dark concrete studio wall, slight lean forward with urgent warning hand gesture, mouth speaking clearly: *"Hoy es Black Friday y un solo botón te puede despertar con cuarenta mil pesos cobrados en el banco."* Camera static 16:9, crisp lighting. | `1.0s → 8.5s` |
| **Clip 2 (Cajita / Gráfica)** | `public/avatar/bf01_bucle.mp4` | Same character, black polo, dark concrete wall, explaining while glancing slightly toward screen-right to point at floating charts: *"Un error mete tu bot en bucle infinito y se reintenta diez mil veces mientras duermes."* Calm authoritative expression, camera static 16:9. | `1.5s → 7.5s` |
| **Clip 3 (Reacción PiP)** | `public/avatar/bf01_reaccion.mp4` | Same character, black polo, dark concrete wall, subtle nodding and concerned eyebrows reacting while explaining AI billing traps, looking directly into lens. Camera static 16:9. | `1.0s → 9.0s` |
| **Clip 4 (Cierre CTA)** | `public/avatar/bf01_cta.mp4` | Same character, black polo, dark concrete wall, confident smile pointing down-right cleanly at end: *"Activa tu límite duro hoy. Comenta PRESUPUESTO y te paso la guía exacta."* Camera static 16:9. | `1.5s → 8.5s` |

> **Nota rápida:** Mientras sacas esos clips (o incluso antes de sacarlos), `HybridBlackFridayBF01` ya corre usando `master_ref.mp4` en bucle limpio por acto. En cuanto los guardes en `proyectos/waters-3d-studio/public/avatar/`, solo apuntamos `avatarClips` y re-renderizamos.
