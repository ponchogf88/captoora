# 🌊 Biblioteca de Curvas y Físicas Spring (Efecto Rebote Delicioso)

Valores de configuración física optimizados para lograr el rebote sedoso característico de interfaces y presentaciones de alta gama (Apple, Linear, Stripe).

---

## 1. Presets de Resorte (Spring Configurations)

### A. "Apple Bouncy" (Rebote Elástico Notorio)
Ideal para: Elementos que entran a cuadro (tarjetas, botones, logos, stickers de planos).
```javascript
// Framer Motion / Remotion spring
const springBouncy = {
  type: "spring",
  stiffness: 300,
  damping: 18,
  mass: 0.8
};
```
* **Sensación:** Rápido, enérgico, con 1 o 2 micro-rebotes antes de asentarse.

---

### B. "Linear Smooth" (Inercia Suave y Elegante)
Ideal para: Textos que suben, apertura de diafragma, transiciones de fotos.
```javascript
const springSmooth = {
  type: "spring",
  stiffness: 120,
  damping: 24,
  mass: 1.0
};
```
* **Sensación:** Peso consistente, desaceleración cremosa sin rebote brusco.

---

### C. "Snap & Settle" (Impacto Rápido de Flash)
Ideal para: Simulación del disparo del obturador, destellos de flash.
```javascript
const springSnap = {
  type: "spring",
  stiffness: 500,
  damping: 30,
  mass: 0.5
};
```
* **Sensación:** Instantáneo como un disparo mecánico, frena en seco sin oscilación.

---

## 2. Curvas Cubic-Bezier para CSS Puro

Si se anima directamente en CSS o Webflow sin librerías de JS:

```css
/* Curva Apple Suave (Out-Quart modificado) */
--ease-apple: cubic-bezier(0.16, 1, 0.3, 1);

/* Curva con Anticipación (Toma impulso antes de avanzar) */
--ease-anticipate: cubic-bezier(0.34, 1.56, 0.64, 1);

/* Curva Cinemática de Profundidad */
--ease-cinema: cubic-bezier(0.25, 0.1, 0.25, 1);
```
