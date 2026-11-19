/**
 * ANTIGRAVITY HALO CURSOR & DANCING CONSTELLATION PARTICLES (ATG Engine)
 * Captoora Ultra-Premium Experience Engine
 * Ethereal fluid lighting, dancing quantum particles & interactive constellation threads
 */

(function () {
  'use strict';

  // Respect accessibility preferences
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  class AntigravityDancingHalo {
    constructor() {
      this.mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
      this.halo = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
      this.prevMouse = { x: this.mouse.x, y: this.mouse.y };
      this.velocity = 0;
      this.isHovering = false;
      this.isVisible = true;

      // Particle system parameters
      this.particleCount = 42;
      this.particles = [];
      this.connectionDistance = 90;

      this.initCanvas();
      this.initParticles();
      this.initEvents();
      this.render();
    }

    initCanvas() {
      this.canvas = document.createElement('canvas');
      this.canvas.id = 'ag-halo-canvas';
      Object.assign(this.canvas.style, {
        position: 'fixed',
        top: '0',
        left: '0',
        width: '100vw',
        height: '100vh',
        pointerEvents: 'none',
        zIndex: '1',
        opacity: '0.9',
        willChange: 'transform'
      });
      document.body.prepend(this.canvas);
      this.ctx = this.canvas.getContext('2d');
      this.onResize();

      // Sharp central specular dot
      this.dot = document.createElement('div');
      this.dot.className = 'ag-specular-dot';
      Object.assign(this.dot.style, {
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
        boxShadow: '0 0 16px #00f0ff, 0 0 32px #CCFF00',
        transition: 'background 0.25s, transform 0.1s, box-shadow 0.25s',
        willChange: 'transform'
      });
      document.body.appendChild(this.dot);
    }

    onResize() {
      this.width = this.canvas.width = window.innerWidth;
      this.height = this.canvas.height = window.innerHeight;
    }

    initParticles() {
      this.particles = [];
      const colors = ['#00f0ff', '#CCFF00', '#ffffff', '#38bdf8', '#a3e635'];

      for (let i = 0; i < this.particleCount; i++) {
        const angle = Math.random() * Math.PI * 2;
        const dist = Math.random() * 160 + 20;

        this.particles.push({
          x: this.mouse.x + Math.cos(angle) * dist,
          y: this.mouse.y + Math.sin(angle) * dist,
          originX: this.mouse.x,
          originY: this.mouse.y,
          vx: (Math.random() - 0.5) * 1.5,
          vy: (Math.random() - 0.5) * 1.5,
          radius: Math.random() * 2.4 + 1.2,
          color: colors[Math.floor(Math.random() * colors.length)],
          alpha: Math.random() * 0.7 + 0.3,
          orbitSpeed: (Math.random() * 0.02 + 0.008) * (Math.random() > 0.5 ? 1 : -1),
          orbitRadius: dist,
          orbitAngle: angle,
          pulseSpeed: Math.random() * 0.04 + 0.02,
          pulseVal: Math.random() * Math.PI
        });
      }
    }

    initEvents() {
      window.addEventListener('resize', () => this.onResize(), { passive: true });

      window.addEventListener('mousemove', (e) => {
        this.mouse.x = e.clientX;
        this.mouse.y = e.clientY;

        const dx = this.mouse.x - this.prevMouse.x;
        const dy = this.mouse.y - this.prevMouse.y;
        this.velocity = Math.sqrt(dx * dx + dy * dy);

        this.prevMouse.x = this.mouse.x;
        this.prevMouse.y = this.mouse.y;
      }, { passive: true });

      // Interactive hover hooks
      const setHoverState = (hovering) => {
        this.isHovering = hovering;
        this.dot.style.background = hovering ? '#CCFF00' : '#00f0ff';
        this.dot.style.boxShadow = hovering 
          ? '0 0 25px #CCFF00, 0 0 50px rgba(0, 240, 255, 0.9)' 
          : '0 0 16px #00f0ff, 0 0 32px #CCFF00';
      };

      document.addEventListener('mouseover', (e) => {
        if (e.target.closest('a, button, .sport-card, .fan-card, .filter-btn, [data-interactive]')) {
          setHoverState(true);
        }
      });

      document.addEventListener('mouseout', (e) => {
        if (e.target.closest('a, button, .sport-card, .fan-card, .filter-btn, [data-interactive]')) {
          setHoverState(false);
        }
      });
    }

    render() {
      // 1. Clear with subtle trail
      this.ctx.clearRect(0, 0, this.width, this.height);

      // 2. Halo Spring Physics
      this.halo.x += (this.mouse.x - this.halo.x) * 0.12;
      this.halo.y += (this.mouse.y - this.halo.y) * 0.12;

      // Update dot position
      this.dot.style.transform = `translate3d(${this.mouse.x}px, ${this.mouse.y}px, 0) translate(-50%, -50%)`;

      // 3. Draw Ethereal Radial Halo Glow
      const haloRadius = this.isHovering ? 260 : 190;
      const gradient = this.ctx.createRadialGradient(
        this.halo.x, this.halo.y, 0,
        this.halo.x, this.halo.y, haloRadius
      );

      if (this.isHovering) {
        gradient.addColorStop(0, 'rgba(204, 255, 0, 0.18)');
        gradient.addColorStop(0.35, 'rgba(0, 240, 255, 0.09)');
        gradient.addColorStop(0.7, 'rgba(0, 240, 255, 0.02)');
        gradient.addColorStop(1, 'transparent');
      } else {
        gradient.addColorStop(0, 'rgba(0, 240, 255, 0.14)');
        gradient.addColorStop(0.4, 'rgba(204, 255, 0, 0.05)');
        gradient.addColorStop(0.8, 'rgba(0, 119, 255, 0.02)');
        gradient.addColorStop(1, 'transparent');
      }

      this.ctx.fillStyle = gradient;
      this.ctx.beginPath();
      this.ctx.arc(this.halo.x, this.halo.y, haloRadius, 0, Math.PI * 2);
      this.ctx.fill();

      // 4. Update and Draw Dancing Swarm Particles
      const targetRadiusMultiplier = this.isHovering ? 1.6 : 1;

      for (let i = 0; i < this.particles.length; i++) {
        const p = this.particles[i];

        // Orbital dance angle
        p.orbitAngle += p.orbitSpeed * (1 + this.velocity * 0.02);
        p.pulseVal += p.pulseSpeed;

        // Target position based on halo center + orbit
        const targetX = this.halo.x + Math.cos(p.orbitAngle) * (p.orbitRadius * targetRadiusMultiplier);
        const targetY = this.halo.y + Math.sin(p.orbitAngle) * (p.orbitRadius * targetRadiusMultiplier);

        // Spring towards orbital target
        p.vx += (targetX - p.x) * 0.04;
        p.vy += (targetY - p.y) * 0.04;
        p.vx *= 0.88;
        p.vy *= 0.88;

        p.x += p.vx;
        p.y += p.vy;

        // Breathing pulse size
        const currentRadius = p.radius + Math.sin(p.pulseVal) * 0.6;
        const currentAlpha = Math.max(0.1, p.alpha + Math.sin(p.pulseVal) * 0.25);

        // Draw particle glow
        this.ctx.save();
        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, currentRadius, 0, Math.PI * 2);
        this.ctx.fillStyle = p.color;
        this.ctx.globalAlpha = currentAlpha;
        this.ctx.shadowBlur = 10;
        this.ctx.shadowColor = p.color;
        this.ctx.fill();
        this.ctx.restore();

        // 5. Connect particles that dance close to each other (Constellation Threads)
        for (let j = i + 1; j < this.particles.length; j++) {
          const p2 = this.particles[j];
          const dist = Math.hypot(p.x - p2.x, p.y - p2.y);

          if (dist < this.connectionDistance) {
            const threadAlpha = (1 - dist / this.connectionDistance) * 0.32;
            this.ctx.save();
            this.ctx.beginPath();
            this.ctx.moveTo(p.x, p.y);
            this.ctx.lineTo(p2.x, p2.y);
            this.ctx.strokeStyle = '#00f0ff';
            this.ctx.globalAlpha = threadAlpha;
            this.ctx.lineWidth = 0.8;
            this.ctx.stroke();
            this.ctx.restore();
          }
        }
      }

      // Dampen velocity smoothly
      this.velocity *= 0.92;

      requestAnimationFrame(() => this.render());
    }
  }

  // Auto initialize on DOM ready
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => new AntigravityDancingHalo());
    } else {
      new AntigravityDancingHalo();
    }
  }
})();
