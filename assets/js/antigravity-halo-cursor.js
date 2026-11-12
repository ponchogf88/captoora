/**
 * ANTIGRAVITY HALO CURSOR & AMBIENT REACTIVE GLOW
 * Captoora Ultra-Premium Experience Engine
 * Ethereal fluid lighting, dynamic spring physics & luminous interaction
 */

(function () {
  'use strict';

  // Check if user prefers reduced motion or is touch only
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReduced) return;

  class AntigravityHalo {
    constructor() {
      this.mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
      this.halo = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
      this.dot = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
      this.targetScale = 1;
      this.currentScale = 1;
      this.isHovering = false;
      this.isVisible = false;
      this.particles = [];
      this.particleCount = 18;

      this.initDOMElements();
      this.initEvents();
      this.render();
    }

    initDOMElements() {
      // 1. Halo Glow Element (Large soft aura)
      this.haloEl = document.createElement('div');
      this.haloEl.className = 'ag-halo-aura';
      Object.assign(this.haloEl.style, {
        position: 'fixed',
        top: '0',
        left: '0',
        width: '460px',
        height: '460px',
        borderRadius: '50%',
        pointerEvents: 'none',
        zIndex: '1',
        transform: 'translate(-50%, -50%)',
        background: 'radial-gradient(circle, rgba(0, 240, 255, 0.12) 0%, rgba(204, 255, 0, 0.04) 40%, transparent 70%)',
        filter: 'blur(32px)',
        transition: 'opacity 0.4s ease, transform 0.12s ease-out',
        opacity: '0',
        willChange: 'transform, opacity'
      });

      // 2. Focused Specular Dot (Sharp point)
      this.dotEl = document.createElement('div');
      this.dotEl.className = 'ag-cursor-dot';
      Object.assign(this.dotEl.style, {
        position: 'fixed',
        top: '0',
        left: '0',
        width: '8px',
        height: '8px',
        borderRadius: '50%',
        pointerEvents: 'none',
        zIndex: '9999',
        transform: 'translate(-50%, -50%)',
        background: '#00f0ff',
        boxShadow: '0 0 14px #00f0ff, 0 0 28px rgba(204, 255, 0, 0.8)',
        opacity: '0',
        transition: 'opacity 0.25s ease, width 0.2s, height 0.2s, background 0.2s',
        willChange: 'transform'
      });

      document.body.appendChild(this.haloEl);
      document.body.appendChild(this.dotEl);
    }

    initEvents() {
      window.addEventListener('mousemove', (e) => {
        this.mouse.x = e.clientX;
        this.mouse.y = e.clientY;

        if (!this.isVisible) {
          this.isVisible = true;
          this.haloEl.style.opacity = '1';
          this.dotEl.style.opacity = '1';
        }
      }, { passive: true });

      document.addEventListener('mouseleave', () => {
        this.isVisible = false;
        this.haloEl.style.opacity = '0';
        this.dotEl.style.opacity = '0';
      });

      // Interactive hover targets
      const updateHoverTargets = () => {
        const interactive = document.querySelectorAll('a, button, .interactive-card, [data-halo-interactive]');
        interactive.forEach((el) => {
          el.addEventListener('mouseenter', () => {
            this.targetScale = 2.4;
            this.haloEl.style.background = 'radial-gradient(circle, rgba(204, 255, 0, 0.2) 0%, rgba(0, 240, 255, 0.08) 50%, transparent 75%)';
            this.dotEl.style.background = '#CCFF00';
            this.dotEl.style.boxShadow = '0 0 20px #CCFF00, 0 0 40px rgba(0, 240, 255, 0.9)';
          });
          el.addEventListener('mouseleave', () => {
            this.targetScale = 1;
            this.haloEl.style.background = 'radial-gradient(circle, rgba(0, 240, 255, 0.12) 0%, rgba(204, 255, 0, 0.04) 40%, transparent 70%)';
            this.dotEl.style.background = '#00f0ff';
            this.dotEl.style.boxShadow = '0 0 14px #00f0ff, 0 0 28px rgba(204, 255, 0, 0.8)';
          });
        });
      };

      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', updateHoverTargets);
      } else {
        updateHoverTargets();
      }
    }

    render() {
      // Smooth lerp (linear interpolation)
      this.halo.x += (this.mouse.x - this.halo.x) * 0.1;
      this.halo.y += (this.mouse.y - this.halo.y) * 0.1;

      this.dot.x += (this.mouse.x - this.dot.x) * 0.35;
      this.dot.y += (this.mouse.y - this.dot.y) * 0.35;

      this.currentScale += (this.targetScale - this.currentScale) * 0.15;

      if (this.isVisible) {
        this.haloEl.style.transform = `translate3d(${this.halo.x}px, ${this.halo.y}px, 0) translate(-50%, -50%) scale(${this.currentScale})`;
        this.dotEl.style.transform = `translate3d(${this.dot.x}px, ${this.dot.y}px, 0) translate(-50%, -50%)`;
      }

      requestAnimationFrame(() => this.render());
    }
  }

  // Initialize on window load
  window.AntigravityHaloCursor = AntigravityHalo;
  if (typeof document !== 'undefined') {
    new AntigravityHalo();
  }
})();
