# 🎬 Recetas de Transiciones Fotográficas (Captoora Style)

Efectos específicos diseñados para videos cortos (Reels / TikTok / Shorts) y carruseles animados de fotografía.

---

## 1. El "Dolly Zoom In" (De Gran Plano General a Plano Detalle)

* **Concepto:** La cámara avanza velozmente hacia el sujeto en 3D mientras el fondo se desenfoca orgánicamente.
* **Estructura de Animación (Remotion / Framer Motion):**
  1. **Fotograma 0 a 15:** Escala inicial `scale(1)`, desenfoque `blur(0px)`.
  2. **Fotograma 16 a 40:** Aceleración con curva `--ease-anticipate`. La escala vuela de `1` a `3.5` apuntando al rostro/ojo.
  3. **Fotograma 41 a 55:** Breve flash blanco translúcido (`opacity: 0.8` $\rightarrow$ `0`) simulando el destello del flash de estudio.
  4. **Fotograma 56:** Corte al Primerísimo Primer Plano con micro-rebote `springBouncy`.

---

## 2. El "Aperture Iris Shutter" (El Lente que Abre y Cierra)

* **Concepto:** 6 a 8 hojas de diafragma metálicas giran en espiral en 3D mientras cambia la foto.
* **Valores Clave:**
  * Rotación: `rotate(45deg)` a `rotate(0deg)`.
  * Apertura: De `F1.8` (grande) a `F16` (cerrado).
  * Reflejo anamórfico: Un haz de luz horizontal azulado/cian recorre el lente durante el cierre.

---

## 3. La Tarjeta de Cristal Flotante (SOUL Glass Card Reveal)

* **Concepto:** Las tarjetas con tips o datos fotográficos entran flotando sobre la imagen con efecto de cristal esmerilado.
* **CSS de Efecto Vidrio Ahumado:**
```css
.captoora-glass-card {
  background: rgba(10, 10, 15, 0.45);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border-radius: 16px;
}
```
