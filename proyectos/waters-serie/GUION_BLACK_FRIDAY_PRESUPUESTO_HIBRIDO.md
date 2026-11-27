# Guion Híbrido Black Friday (Multi-Ángulo · 6 Escenas Separadas) · `WATERS_013` (`PRESUPUESTO`)

- **Regla de Oro:** **1 escena = 1 clip real independiente (`5–8 s`) con ángulo de cámara distinto + su propio audio con lip-sync real.** Ver [REGLAS_PRODUCCION_HIBRIDA.md](REGLAS_PRODUCCION_HIBRIDA.md).
- **Entregables que genera [armar_escenas_bf01.py](scripts/armar_escenas_bf01.py):**
  1. `proyectos/waters-serie/black_friday_bf01/escenas/01_hook.mp4` .. `06_cta.mp4` (cada escena individual con sus overlays/3D + su audio real).
  2. `proyectos/waters-serie/black_friday_bf01/BF01_COMPLETO_UNIDO.mp4` + copia en `cola_programacion_semana/listos_para_arrastrar/00_BLACK_FRIDAY_PRESUPUESTO_OPUS_CLEAN.mp4`.
  3. **Sin subtítulos quemados abajo** (`220 px` libres) para pasar limpio por **OpusClip** y **Captions**.

---

## 6 Escenas Separadas · Prompts Multi-Ángulo (Rama Oficial de Gemini / Nano Banana)

> **Cómo guardarlos:** guárdalos como `01.mp4` .. `06.mp4` en `proyectos/waters-serie/black_friday_bf01/clips_raw/` (o déjalos en `Descargas` en orden `1 → 6` y corre `python3 proyectos/waters-serie/scripts/armar_escenas_bf01.py --from-downloads`).

| Escena | Duración | Ángulo y Encuadre | Overlay / 3D que entra encima | Prompt exacto (pegar en tu rama de Gemini) |
| --- | --- | --- | --- | --- |
| **01 · Hook** | `5–7 s` | **Close-Up frontal**, ligera inclinación hacia adelante, energía de alerta | Barra `BLACK FRIDAY · ALERTA IA` + badge `-$40,000 MXN` + flecha | `Same character from reference, black polo, dark concrete wall, CLOSE-UP chest-to-head frontal camera angle, urgent concerned expression leaning slightly forward with warning hand gesture, speaking clearly in Spanish: "Hoy es Black Friday y un solo botón apagado en tu IA te puede despertar mañana con cuarenta mil pesos cobrados." Static 16:9 studio lighting.` |
| **02 · El Bucle** | `6–8 s` | **Ángulo 3/4 desde la izquierda** (`left-side frame`), personaje mirando levemente a su derecha | **Cajita interactiva Gemini/Claude/ChatGPT** escribiendo + contador `10,000x` | `Same character from reference, black polo, dark concrete wall, MEDIUM SHOT filmed from a subtle 3/4 left camera angle, character positioned slightly left glancing toward empty dark wall on screen-right while explaining in Spanish: "Dejas corriendo tu agente en la noche con tu tarjeta y un error lo mete en bucle: diez mil reintentos mientras duermes." Static 16:9 camera.` |
| **03 · La Gráfica** | `6–8 s` | **Plano medio amplio contrapicado suave** (`low-angle waist-up`), señalando hacia la derecha | **Gráfica `$80 → $420 → $1,250 → $2,000 USD`** + flecha curva neón | `Same character from reference, black polo, dark concrete wall, WAIST-UP MEDIUM WIDE shot with slight low-angle cinematic camera, calm serious tone pointing toward open dark space on screen-right, speaking clearly in Spanish: "Mira la gráfica: a las dos van cuatrocientos veinte dólares, a las cuatro mil doscientos cincuenta, y a las seis dos mil dólares quemados." Static 16:9.` |
| **04 · Dilema 3D** | `5–7 s` | **Ángulo 3/4 desde la derecha** (`right-side 3/4`), levantando 2 dedos | Entra **`BinaryDoors3D` (`1 SIN LÍMITE` vs `2 HARD LIMIT`)** + tú en PiP arriba-derecha | `Same character from reference, black polo, dark concrete wall, TIGHT CHEST-UP shot from a 3/4 right camera angle, raising two fingers cleanly to contrast two options, speaking clearly in Spanish: "Hoy tienes dos puertas: meter tu tarjeta directa sin freno, o blindarte en tres minutos antes de dar clic." Crisp 16:9.` |
| **05 · Los 3 Candados** | `6–8 s` | **Plano medio-corto (`chest-up`)**, contando `1 · 2 · 3` con los dedos | Entra **`GiantClipboard3D`** palomeando los 3 candados + tú en PiP | `Same character from reference, black polo, dark concrete wall, CHEST-UP eye-level angle slightly rotated left, clearly counting one, two, three with fingers while speaking in Spanish: "Uno: Hard Monthly Limit de veinte dólares. Dos: tarjeta virtual topada. Tres: aprobación humana arriba de diez corridas." Crisp 16:9.` |
| **06 · Cierre CTA** | `5–6 s` | **Close-Up frontal `eye-level`** seguro y cercano, sonrisa confiada al cierre | Card flotante esmeralda **`COMENTA: PRESUPUESTO`** | `Same character from reference, black polo, dark concrete wall, CRISP EYE-LEVEL CLOSE-UP centered framing, warm confident smile nodding cleanly at end, speaking clearly in Spanish: "Que tu automatización no se vuelva tu bancarrota. Comenta PRESUPUESTO y te paso la guía exacta." Static 16:9.` |

---

## Cómo re-hacer solo 1 escena si no te gustó
```bash
# 1. Reemplaza únicamente clips_raw/03.mp4 (por ejemplo)
# 2. Re-renderiza solo esa escena y vuelve a pegar todo en ~15 segundos:
python3 proyectos/waters-serie/scripts/armar_escenas_bf01.py --scene 3
```
