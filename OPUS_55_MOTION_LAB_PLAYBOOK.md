# 🎬 PLAYBOOK OFICIAL: OPUS 5.5 MOTION LAB (@flxrnc Architecture) — CAPTOORA STUDIO

## 1. Filosofía Central: "The Harness Over The Prompt"
El prompt crudo es solo el 10% del resultado; el **90% es el Harness Técnico**:
- **Prohibido pedir subjetividades** (*"haz que se vea fluido"* o *"ponle una animación bonita"*).
- **Todo movimiento se define con física matemática exacta:** Frecuencia natural ($f$ en $\text{Hz}$) y coeficiente de amortiguamiento ($\zeta$, zeta).
  - Rebote táctil mecánico / 3D Keycap / UI Card: $\zeta = 0.42$, $f = 9.0\text{ Hz}$
  - Entrada editorial de lujo (Glassmorphism Card): $\zeta = 0.78$, $f = 4.5\text{ Hz}$
  - Cámara cinematográfica / Parallax lunar: $\zeta = 0.92$, $f = 2.2\text{ Hz}$

## 2. Arquitectura de Renderizado Determinista `seek(t)`
En lugar de depender de timelapses estocásticos, toda pieza de Motion Design se programa alrededor de una función pura `seek(t)`:
```javascript
// Fórmula de resorte sub-amortiguado de Opus 5.5 Motion Lab
function spring(t, zeta = 0.42, freq = 9.0) {
  if (t <= 0) return 0;
  const omega = 2 * Math.PI * freq;
  const omegaD = omega * Math.sqrt(1 - zeta * zeta);
  return 1 - Math.exp(-zeta * omega * t) * (
    Math.cos(omegaD * t) + (zeta * omega / omegaD) * Math.sin(omegaD * t)
  );
}
```
Cada cuadro $k \in [0, N]$ se evalúa en $t = k / 60.0$ segundos y se codifica directamente en `ffmpeg` a **60fps (`libx264`, `crf 16`, `pix_fmt yuv420p`)**.

## 3. Ciclo Agéntico Obligatorio de 6 Pasos
1. **`generate`**: Escribir el motor `seek(t)` con capas Glassmorphism, iluminación especular y tipografía editorial.
2. **`preview`**: Renderizar los keyframes críticos ($t = 0.2\text{s}, 0.8\text{s}, 1.5\text{s}, 3.0\text{s}$).
3. **`inspect`**: Abrir los keyframes con `view_file`.
4. **`critique`**: Evaluar márgenes, legibilidad, física del movimiento y que **jamás se recorte a ninguna persona o producto**.
5. **`revise`**: Ajustar coordenadas y curvas de amortiguamiento ($\zeta$).
6. **`render`**: Exportar MP4 a 60fps + Preview animada lista para ver directamente en Composer.
