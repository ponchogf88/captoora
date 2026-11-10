---
name: antigravity-halo-cursor
description: Implements the hypnotic Google Antigravity interactive orbital particle halo cursor effect (Spring-Physics Swarm + Multi-Harmonic Breathing Ring + Velocity-Aligned Micro-Capsules) compatible with Apple Liquid Glass / Glassmorphism UIs. Use whenever the user asks for the Antigravity cursor particles, orbital halo cursor, interactive particle swarm, or "halo skill".
---

# Antigravity Orbital Halo Cursor Skill (`antigravity-halo-cursor`)

## Overview & Technical Terminology
In interactive graphics and creative coding, the hypnotic cursor effect featured on `antigravity.google` is known as an **Orbital Spring-Physics Particle Swarm** (or **Harmonic Attractor Halo / Boids Flow-Field Ring**).

It combines four physical behaviors that make the particles feel alive and choreographed:
1. **Hollow Orbital Equilibrium (Halo Ring)**: Instead of collapsing onto the exact `(x, y)` point of the mouse, each particle orbits at a target radius $r_i \in [R_{\min}, R_{\max}]$ around the cursor.
2. **Multi-Harmonic Wave Breathing (Cymatic Undulation)**: The ring radius undulates continuously using coupled trigonometric harmonics:
   $$R_i(t) = r_i + A_1 \sin(3\theta_i + \omega_1 t) + A_2 \cos(5\theta_i - \omega_2 t)$$
   so the swarm dances and breathes in synchrony even when the mouse is completely still.
3. **Staggered Spring-Damper Lag (Verlet / Hooke's Law)**: Each particle has a radial layer with distinct spring stiffness (`k`) and viscous damping (`friction`). When the cursor moves rapidly, inner particles follow tightly while outer particles trail behind like a comet tail and spiral gracefully back into orbit.
4. **Tangent / Velocity-Aligned Micro-Capsules**: Each particle is drawn as a micro-capsule (rounded dash) rotated along its instantaneous velocity/orbital tangent vector, elongating with speed.

---

## Quick Integration (Drop-In Script)

Include `<script src="/assets/js/antigravity_halo_cursor.js"></script>` or embed the self-contained initializer below in any HTML page:

```javascript
window.initAntigravityHalo({
  particleCount: 220,
  baseRadius: 78,
  radiusSpread: 64,
  palette: ['#4285F4', '#9B72CB', '#D96570', '#F5C542', '#60A5FA', '#A78BFA'],
  opacity: 0.85
});
```

## Pairing with Apple Liquid Glass (visionOS Glassmorphism)
When pairing the **Antigravity Halo Cursor** with **Apple Liquid Glass**:
- Place the `<canvas id="antigravityHaloCanvas">` at `z-index: 1` (behind the Liquid Glass cards) OR at `z-index: 9998` with `pointer-events: none` and `mix-blend-mode: screen`.
- Use `backdrop-filter: blur(28px) saturate(190%)` and specular inner borders (`box-shadow: inset 0 1px 0 0 rgba(255,255,255,0.35), inset 0 0 24px rgba(255,255,255,0.06)`) on the Liquid Glass panels so the orbiting particles refract through the translucent glass edges as you move the mouse!
