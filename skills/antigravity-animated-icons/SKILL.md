---
name: antigravity-animated-icons
description: Implements Google Antigravity IDE-style interactive floating docks, micro-animated SVG vector icons, frosted disc highlights, 3D spring-physics hover states, dark-glass floating tooltips, and Spotlight command search palettes (⌘K). Use whenever the user asks for Antigravity dock icons, animated SVG micro-interactions, 3D icon flips, checkmark drawing animations, morphing geometric shapes, or IDE-like icon rail navigation.
---

# Antigravity Animated Icons & Interactive Dock Skill (`antigravity-animated-icons`)

## Overview & Visual Language
This skill encapsulates the signature micro-interaction design system seen in the **Google Antigravity IDE sidebar dock**:
1. **Frosted Luminous Backplate:** When an icon is hovered, a soft translucent circular pill disc (`rgba(255, 255, 255, 0.09)`) lights up with a subtle radial glow and smooth spring scale (`1.08`).
2. **Dynamic Vector Micro-Animations (SVG):**
   - **☑️ Checkbox / Objetivos:** The square frame executes an elastic 3D perspective tilt (`rotateY(20deg) rotateX(-10deg)`) while the checkmark dynamically draws in with `stroke-dashoffset` animation.
   - **🔍 Buscar (⌘K):** The magnifying glass tilts (`rotate(-18deg) scale(1.15)`) with an internal animated optical glint in the lens.
   - **💡 Ideas / Sol:** The bulb filament switches on in bright amber (`#fbbf24`), casting a soft neon drop-shadow and pulsing radiating aura rays.
   - **📚 Biblioteca (◇ △ ○ □):** The 4 geometric shapes tumble and morph from a 2x2 cluster into a clean vertical alignment with staggered easing.
   - **➕ Crear un espacio:** Rounded square container with a plus icon that performs an elastic 90-degree twist (`rotate(90deg)`).
   - **💬 Conversación:** Speech bubble with 3 interior dots that jump sequentially in an undulating wave.
   - **🧬 Biometrics / Iris:** Precision optical aperture with an inner dashed ring that rotates 180 degrees and flashes a cyan target reticle.
3. **Floating Dark-Glass Tooltips:**
   - Positioned to the right (or top on mobile) with pointer arrow.
   - Deep obsidian glass (`rgba(24, 25, 29, 0.94)` + `backdrop-filter: blur(18px)`).
   - Keycap shortcut chips (`⌘K`, `⌘J`, `⌘B`, `ESC`).
4. **Haptic Optic Shutter Sound:** Zero-dependency audio feedback generated in real time using the browser's Web Audio API.
5. **Spotlight Command Palette (`⌘K`):** Integrated modal overlay for instant search, fuzzy filtering, and smooth navigation.

---

## 1. Quick Integration

### A. Minimal HTML Structure

```html
<!-- ANTIGRAVITY FLOATING DOCK -->
<aside class="agy-floating-dock" id="agy-floating-dock" aria-label="Navegación Rápida">
  <!-- Conversación -->
  <button type="button" class="agy-dock-btn icon-chat" onclick="openAgyChat()">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
      <circle class="chat-dot dot-1" cx="8.5" cy="11.5" r="1.1" fill="currentColor"/>
      <circle class="chat-dot dot-2" cx="12" cy="11.5" r="1.1" fill="currentColor"/>
      <circle class="chat-dot dot-3" cx="15.5" cy="11.5" r="1.1" fill="currentColor"/>
    </svg>
    <span class="agy-tooltip">Conversación <span class="agy-shortcut-key">⌘J</span></span>
  </button>

  <!-- Buscar -->
  <button type="button" class="agy-dock-btn icon-search" onclick="toggleAgySearch()">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="11" cy="11" r="7"/>
      <line x1="16.5" y1="16.5" x2="21.5" y2="21.5"/>
      <circle class="lens-glint" cx="9" cy="9" r="2.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
    </svg>
    <span class="agy-tooltip">Buscar <span class="agy-shortcut-key">⌘K</span></span>
  </button>

  <!-- Biblioteca (4 Formas Morphing) -->
  <button type="button" class="agy-dock-btn icon-library" onclick="scrollToAgySection('portfolio-section')">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <polygon class="shape-diamond" points="6.5,3.5 10,7 6.5,10.5 3,7"/>
      <polygon class="shape-triangle" points="17.5,3.5 21.5,10.5 13.5,10.5"/>
      <circle class="shape-circle" cx="6.5" cy="17.5" r="3.5"/>
      <rect class="shape-square" x="14" y="14" width="7" height="7" rx="1.8"/>
    </svg>
    <span class="agy-tooltip">Biblioteca</span>
  </button>

  <!-- Ideas (Foco Filamento Activo) -->
  <button type="button" class="agy-dock-btn icon-ideas" onclick="scrollToAgySection('ideas-section')">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path class="bulb-outline" d="M9 18h6m-4 3h2M12 2a7 7 0 0 0-7 7c0 2.38 1.19 4.47 3 5.74V17a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-2.26c1.81-1.27 3-3.36 3-5.74a7 7 0 0 0-7-7z"/>
      <path class="filament-path" d="M10 9a2 2 0 0 1 4 0c0 1.2-1.5 2-2 3v1" stroke-width="1.5"/>
      <g class="bulb-rays">
        <line x1="12" y1="0.5" x2="12" y2="2" stroke="#f59e0b" stroke-width="1.6"/>
        <line x1="4.5" y1="4.5" x2="5.8" y2="5.8" stroke="#f59e0b" stroke-width="1.6"/>
        <line x1="19.5" y1="4.5" x2="18.2" y2="5.8" stroke="#f59e0b" stroke-width="1.6"/>
      </g>
    </svg>
    <span class="agy-tooltip">Ideas</span>
  </button>

  <!-- Objetivos (Checkbox 3D con dibujo animado) -->
  <button type="button" class="agy-dock-btn icon-tasks" onclick="scrollToAgySection('pricing-section')">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
      <rect class="task-box" x="3" y="3" width="18" height="18" rx="5"/>
      <path class="task-check" d="M7.5 12l3.2 3.2 6.3-6.4"/>
    </svg>
    <span class="agy-tooltip">Objetivos</span>
  </button>

  <div class="agy-dock-divider"></div>

  <!-- Crear un espacio (+) -->
  <button type="button" class="agy-dock-btn icon-plus" onclick="openAgyCreate()">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
      <rect x="3" y="3" width="18" height="18" rx="5"/>
      <g class="plus-cross">
        <line x1="12" y1="8" x2="12" y2="16"/>
        <line x1="8" y1="12" x2="16" y2="12"/>
      </g>
    </svg>
    <span class="agy-tooltip">Crear un espacio <span class="agy-shortcut-key">⌘B</span></span>
  </button>
</aside>
```

---

## 2. CSS Micro-Interactions Core

```css
.agy-floating-dock {
  position: fixed;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 9995;
  background: rgba(14, 16, 21, 0.88);
  backdrop-filter: blur(28px);
  -webkit-backdrop-filter: blur(28px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 26px;
  padding: 12px 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  box-shadow: 0 20px 48px -6px rgba(0, 0, 0, 0.7), 0 0 1px 1px rgba(255, 255, 255, 0.06);
}

.agy-dock-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: transparent;
  border: none;
  outline: none;
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: background 0.22s ease, color 0.22s ease, transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.22s ease;
}

.agy-dock-btn:hover {
  background: rgba(255, 255, 255, 0.09);
  color: #ffffff;
  transform: scale(1.08);
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.09);
}

.agy-dock-btn:active {
  transform: scale(0.92);
}

/* Tooltip */
.agy-tooltip {
  position: absolute;
  left: calc(100% + 14px);
  top: 50%;
  transform: translateY(-50%) translateX(-8px);
  background: rgba(24, 25, 29, 0.94);
  backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 8px;
  padding: 6px 12px;
  color: #f8fafc;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  pointer-events: none;
  opacity: 0;
  visibility: hidden;
  box-shadow: 0 12px 30px -4px rgba(0, 0, 0, 0.75);
  transition: opacity 0.2s cubic-bezier(0.16, 1, 0.3, 1), transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 10005;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.agy-dock-btn:hover .agy-tooltip {
  opacity: 1;
  visibility: visible;
  transform: translateY(-50%) translateX(0);
}

/* 3D Checkbox Check Draw */
.icon-tasks { perspective: 400px; }
.icon-tasks svg { transition: transform 0.38s cubic-bezier(0.16, 1, 0.3, 1); }
.agy-dock-btn:hover.icon-tasks svg { transform: rotateY(20deg) rotateX(-10deg) scale(1.1); }
.icon-tasks .task-check {
  stroke-dasharray: 24;
  stroke-dashoffset: 0;
}
.agy-dock-btn:hover.icon-tasks .task-check {
  animation: agyCheckDraw 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  stroke: #38bdf8;
}
@keyframes agyCheckDraw {
  0% { stroke-dashoffset: 24; }
  100% { stroke-dashoffset: 0; }
}

/* Morphing Geometric Shapes */
.agy-dock-btn:hover.icon-library .shape-diamond { transform: translate(2.5px, 3px) rotate(45deg); stroke: #a5b4fc; }
.agy-dock-btn:hover.icon-library .shape-triangle { transform: translate(-3.5px, 3px) scale(0.95); stroke: #38bdf8; }
.agy-dock-btn:hover.icon-library .shape-circle { transform: translate(2.5px, -3px) scale(1.1); stroke: #a7f3d0; }
.agy-dock-btn:hover.icon-library .shape-square { transform: translate(-3.5px, -3px) rotate(90deg); stroke: #fde047; }
```

---

## 3. Web Audio API Optic Shutter Synthesis

```javascript
function playAgyOpticClick() {
  try {
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(1400, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(320, audioCtx.currentTime + 0.045);
    gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.045);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.05);
  } catch(e) {}
}
```

---

## 4. Mobile Responsive Alignment
On screens $\le 768\text{px}$, the dock automatically repositions to the bottom-center of the screen as an iOS/visionOS glass bar:
- `left: 50%; bottom: 16px; top: auto; transform: translateX(-50%);`
- `flex-direction: row; border-radius: 999px;`
- Tooltips re-anchor to the top of each icon (`bottom: calc(100% + 12px)`).
