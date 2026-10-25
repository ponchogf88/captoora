# 🪐 Captoora Motion Lab — Base de Conocimiento de Motion Graphics

Bienvenido al laboratorio de animación, físicas y transiciones dinámicas para **Captoora Studio**.

Este repositorio de conocimiento documenta las fórmulas matemáticas, curvas de animación, configuraciones de resorte (*spring physics*) y recetas de código para producir visuales con la estética **Dark Void / SOUL**.

---

## 📐 Principios de Diseño de Movimiento (Motion Principles)

1. **Cero Linealidad:** Ningún objeto se mueve a velocidad constante. La naturaleza tiene inercia, peso y amortiguación.
2. **Spring Physics sobre Bezier Rígido:** Se prefieren simulaciones físicas de resorte (`stiffness`, `damping`, `mass`) sobre curvas `ease-in-out` estándar para lograr el rebote orgánico característico de Apple y Linear.
3. **Profundidad Espacial (Z-Axis):** Las transiciones no solo se mueven en X e Y; viajan en profundidad hacia la cámara con desenfoque de movimiento (*motion blur*) y distorsión de lente sutil.
4. **Iluminación Reactiva:** Los reflejos y brillos en bordes de cristal ahumado reaccionan al ángulo de movimiento.

---

## 🛠️ Herramientas Soportadas

* **Remotion:** Renderizado programático de videos MP4 de alta fidelidad con React.
* **Framer Motion / Motion.dev:** Animaciones web interactivas y carruseles fluidos.
* **Three.js / React Three Fiber:** Lentes de cámara 3D, reflejos de cristal, hojas de diafragma y partículas cosmicas.
* **GSAP / Canvas API:** Animaciones vectoriales de alto rendimiento.
