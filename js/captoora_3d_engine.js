/**
 * CAPTOORA STUDIO · ULTRA 8K CINEMATIC CAMERA COMPOSITOR ENGINE
 * Authentic Nikon Z9 Flagship + Nikkor Z 50mm f/1.2 S Lens (Pexels Real High-Resolution Photography)
 * 5-Act Scroll Choreography · Web Audio Shutter Synthesis · 150ms Strobe Flash · Parallax Par Excellence
 */

(function () {
  'use strict';

  window.CaptooraCinematic = {
    // Stage elements
    container: null,
    canvas: null,
    ctx: null,
    layerTop: null,
    layerFront: null,
    layerMacro: null,
    specularSheen: null,
    vfFrame: null,
    afReticleBox: null,
    hudOverlay: null,
    act1Hud: null,
    act2Quote: null,
    act3Quote: null,
    flashScreen: null,
    soundToggleBtn: null,

    // State variables
    soundEnabled: true,
    audioCtx: null,
    hasFlashedAct3: false,
    currentAct: 1,
    actProgress: 0,
    mouseX: 0,
    mouseY: 0,
    targetMouseX: 0,
    targetMouseY: 0,

    // Dust particles system
    particles: [],
    particleCount: 55,

    // Initialize the engine
    init: function () {
      this.container = document.getElementById('webgl-container');
      if (!this.container) return;

      this.canvas = document.getElementById('webgl-canvas');
      this.layerTop = document.getElementById('layer-top-oled');
      this.layerFront = document.getElementById('layer-front-hero');
      this.layerMacro = document.getElementById('layer-macro-shutter');
      this.specularSheen = document.getElementById('specular-sheen');
      this.vfFrame = document.getElementById('camera-vf-frame');
      this.afReticleBox = document.getElementById('af-reticle-box');
      this.hudOverlay = document.querySelector('.hud-overlay');
      this.act1Hud = document.getElementById('act1-hud');
      this.act2Quote = document.getElementById('act2-quote');
      this.act3Quote = document.getElementById('act3-quote');
      this.flashScreen = document.getElementById('flash-screen');
      this.soundToggleBtn = document.getElementById('sound-toggle-btn');

      this.initParticles();
      this.initScrollTrigger();
      this.initInteractions();
      this.renderLoop();

      window.addEventListener('resize', () => this.onResize());
      console.log('⚡ Captoora Cinematic 8K Engine Initialized Successfully');
    },

    // 1. PARTICLES & VOLUMETRIC ATMOSPHERE CANVAS
    initParticles: function () {
      if (!this.canvas) return;
      this.ctx = this.canvas.getContext('2d');
      this.onResize();

      this.particles = [];
      for (let i = 0; i < this.particleCount; i++) {
        this.particles.push({
          x: Math.random() * this.canvas.width,
          y: Math.random() * this.canvas.height,
          radius: Math.random() * 1.8 + 0.4,
          alpha: Math.random() * 0.45 + 0.1,
          speedX: (Math.random() - 0.5) * 0.35,
          speedY: -Math.random() * 0.4 - 0.1,
          pulse: Math.random() * Math.PI * 2,
        });
      }
    },

    onResize: function () {
      if (!this.canvas) return;
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;
    },

    drawParticles: function (time) {
      if (!this.ctx) return;
      const w = this.canvas.width;
      const h = this.canvas.height;
      this.ctx.clearRect(0, 0, w, h);

      for (let i = 0; i < this.particles.length; i++) {
        const p = this.particles[i];
        p.y += p.speedY;
        p.x += p.speedX;
        p.pulse += 0.02;

        if (p.y < 0) p.y = h;
        if (p.x < 0) p.x = w;
        if (p.x > w) p.x = 0;

        const currentAlpha = p.alpha * (0.6 + 0.4 * Math.sin(p.pulse));

        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        this.ctx.fillStyle = `rgba(200, 235, 255, ${currentAlpha})`;
        this.ctx.shadowBlur = 6;
        this.ctx.shadowColor = 'rgba(0, 212, 255, 0.5)';
        this.ctx.fill();
        this.ctx.shadowBlur = 0;
      }
    },

    // 2. SYNTHESIZED NIKON Z9 MECHANICAL DUAL-CURTAIN SHUTTER (WEB AUDIO API)
    playNikonZ9Shutter: function () {
      if (!this.soundEnabled) return;

      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!this.audioCtx) {
          this.audioCtx = new AudioCtx();
        }
        if (this.audioCtx.state === 'suspended') {
          this.audioCtx.resume();
        }

        const now = this.audioCtx.currentTime;

        // Front Curtain Impact: crisp metallic transient
        const osc1 = this.audioCtx.createOscillator();
        const gain1 = this.audioCtx.createGain();
        osc1.type = 'triangle';
        osc1.frequency.setValueAtTime(1250, now);
        osc1.frequency.exponentialRampToValueAtTime(70, now + 0.035);

        gain1.gain.setValueAtTime(1.0, now);
        gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.04);

        osc1.connect(gain1);
        gain1.connect(this.audioCtx.destination);
        osc1.start(now);
        osc1.stop(now + 0.045);

        // Rear Curtain Snap & Electronic Solenoid Click (delay 45ms)
        const osc2 = this.audioCtx.createOscillator();
        const gain2 = this.audioCtx.createGain();
        osc2.type = 'sine';
        osc2.frequency.setValueAtTime(840, now + 0.045);
        osc2.frequency.exponentialRampToValueAtTime(95, now + 0.11);

        gain2.gain.setValueAtTime(0.0, now);
        gain2.gain.setValueAtTime(0.85, now + 0.045);
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.12);

        osc2.connect(gain2);
        gain2.connect(this.audioCtx.destination);
        osc2.start(now + 0.045);
        osc2.stop(now + 0.13);

        // Mechanical high-frequency texture noise
        const bufferSize = this.audioCtx.sampleRate * 0.04;
        const noiseBuffer = this.audioCtx.createBuffer(1, bufferSize, this.audioCtx.sampleRate);
        const output = noiseBuffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          output[i] = Math.random() * 2 - 1;
        }

        const whiteNoise = this.audioCtx.createBufferSource();
        whiteNoise.buffer = noiseBuffer;

        const filter = this.audioCtx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.value = 3200;
        filter.Q.value = 2.5;

        const noiseGain = this.audioCtx.createGain();
        noiseGain.gain.setValueAtTime(0.35, now);
        noiseGain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);

        whiteNoise.connect(filter);
        filter.connect(noiseGain);
        noiseGain.connect(this.audioCtx.destination);
        whiteNoise.start(now);
        whiteNoise.stop(now + 0.045);
      } catch (e) {
        console.warn('Audio Synthesis Warning:', e);
      }
    },

    // 3. GSAP SCROLLTRIGGER 5-ACT ORCHESTRATION
    initScrollTrigger: function () {
      if (!window.gsap || !window.ScrollTrigger) return;
      gsap.registerPlugin(ScrollTrigger);

      // Initialize smooth Lenis scrolling if available
      if (window.Lenis) {
        const lenis = new Lenis({
          duration: 1.25,
          easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
          direction: 'vertical',
          smooth: true,
        });
        function raf(time) {
          lenis.raf(time);
          requestAnimationFrame(raf);
        }
        requestAnimationFrame(raf);
        lenis.on('scroll', ScrollTrigger.update);
        gsap.ticker.add((time) => lenis.raf(time * 1000));
        gsap.ticker.lagSmoothing(0);
      }

      const storyStage = document.getElementById('story-stage');
      if (!storyStage) return;

      ScrollTrigger.create({
        trigger: storyStage,
        start: 'top top',
        end: 'bottom bottom',
        scrub: 1,
        onUpdate: (self) => {
          const progress = self.progress; // 0.00 to 1.00
          this.actProgress = progress;

          // ========================================================
          // ACT 1: THE REVEAL (0.00 -> 0.30)
          // Top macro dial view -> 3D pivot into 3/4 Frontal Flagship
          // ========================================================
          if (progress <= 0.30) {
            this.currentAct = 1;
            const p = progress / 0.30; // 0 to 1

            // Top view layer fades out, front hero rotates in
            if (this.layerTop) {
              this.layerTop.style.opacity = Math.max(0, 1 - p * 1.4);
              this.layerTop.style.transform = `scale(${1.05 - p * 0.1}) rotateX(${10 - p * 15}deg) translateY(${-p * 40}px)`;
            }

            if (this.layerFront) {
              this.layerFront.style.opacity = Math.min(1, p * 1.5);
              const rotY = (1 - p) * -18;
              const rotX = (1 - p) * 8;
              const scale = 0.92 + p * 0.08;
              this.layerFront.style.transform = `scale(${scale}) rotateY(${rotY}deg) rotateX(${rotX}deg)`;
            }

            if (this.layerMacro) {
              this.layerMacro.style.opacity = 0;
            }

            // HUD Badges
            if (this.act1Hud) this.act1Hud.style.opacity = Math.max(0, 1 - p * 1.8);
            if (this.act2Quote) this.act2Quote.style.opacity = 0;
            if (this.act3Quote) this.act3Quote.style.opacity = 0;

            // Reticle in scan mode
            if (this.afReticleBox) this.afReticleBox.classList.remove('locked');

            // Specular sheen sweep
            if (this.specularSheen) {
              this.specularSheen.style.transform = `translateX(${-80 + p * 80}%) rotate(-12deg)`;
            }
          }

          // ========================================================
          // ACT 2: THE FACE OFF (0.30 -> 0.60)
          // Front Lock, Optical Breathing, AF Lock, Quote Fade
          // ========================================================
          else if (progress > 0.30 && progress <= 0.60) {
            this.currentAct = 2;
            const p = (progress - 0.30) / 0.30; // 0 to 1

            if (this.layerTop) this.layerTop.style.opacity = 0;

            if (this.layerFront) {
              this.layerFront.style.opacity = 1;
            }

            if (this.layerMacro) this.layerMacro.style.opacity = 0;

            if (this.act1Hud) this.act1Hud.style.opacity = 0;

            // Quote fades in and stays centered
            if (this.act2Quote) {
              const quoteOpacity = p < 0.2 ? p * 5 : p > 0.8 ? (1 - p) * 5 : 1;
              this.act2Quote.style.opacity = quoteOpacity;
            }

            if (this.act3Quote) this.act3Quote.style.opacity = 0;

            // AF Reticle locks onto the lens
            if (this.afReticleBox) this.afReticleBox.classList.add('locked');

            // Reset flash trigger if scrolled backwards
            if (progress < 0.58) this.hasFlashedAct3 = false;
          }

          // ========================================================
          // ACT 3: THE FLASH (0.60 -> 0.85)
          // Macro Shutter Zoom, Depress, 150ms Flash & Dark Quote
          // ========================================================
          else if (progress > 0.60 && progress <= 0.85) {
            this.currentAct = 3;
            const p = (progress - 0.60) / 0.25; // 0 to 1

            if (this.layerTop) this.layerTop.style.opacity = 0;
            if (this.act2Quote) this.act2Quote.style.opacity = 0;

            // Crossfade into macro shutter view
            if (p < 0.35) {
              const macroFade = p / 0.35;
              if (this.layerFront) this.layerFront.style.opacity = 1 - macroFade;
              if (this.layerMacro) {
                this.layerMacro.style.opacity = macroFade;
                this.layerMacro.style.transform = `scale(${1.0 + macroFade * 0.15})`;
              }
            } else {
              if (this.layerFront) this.layerFront.style.opacity = 0;
              if (this.layerMacro) {
                this.layerMacro.style.opacity = 1;
                this.layerMacro.style.transform = `scale(1.15)`;
              }
            }

            // Trigger Strobe Flash Burst & Shutter Audio at ~68%
            if (progress >= 0.68 && !this.hasFlashedAct3) {
              this.hasFlashedAct3 = true;
              this.playNikonZ9Shutter();

              if (this.flashScreen) {
                this.flashScreen.style.opacity = '1';
                setTimeout(() => {
                  this.flashScreen.style.opacity = '0';
                }, 150);
              }
            }

            // Quote emerges after the flash: "Capturamos lo que el tiempo quiere borrar"
            if (this.act3Quote) {
              if (progress >= 0.70) {
                const quoteP = (progress - 0.70) / 0.15;
                this.act3Quote.style.opacity = Math.min(quoteP * 2, 1);
              } else {
                this.act3Quote.style.opacity = 0;
              }
            }
          }

          // ========================================================
          // ACT 4: THE ABSORPTION (0.85 -> 1.00)
          // Accelerating Zoom directly into f/1.2 Pure Front Glass
          // ========================================================
          else if (progress > 0.85) {
            this.currentAct = 4;
            const p = (progress - 0.85) / 0.15; // 0 to 1

            if (this.layerTop) this.layerTop.style.opacity = 0;
            if (this.layerMacro) this.layerMacro.style.opacity = 0;
            if (this.act2Quote) this.act2Quote.style.opacity = 0;
            if (this.act3Quote) this.act3Quote.style.opacity = Math.max(0, 1 - p * 2);

            // Front hero zooms aggressively directly into lens center
            if (this.layerFront) {
              this.layerFront.style.opacity = 1;
              const zoomScale = 1.0 + Math.pow(p, 2.2) * 5.2; // 1.0 to 6.2
              this.layerFront.style.transform = `scale(${zoomScale})`;
              // Vignette perimeter closes down to pure black
              const vignette = Math.max(0, 1 - p * 1.2);
              this.layerFront.style.filter = `brightness(${vignette})`;
            }

            // HUD & Viewfinder frame fade out
            if (this.hudOverlay) this.hudOverlay.style.opacity = Math.max(0, 1 - p * 2);
            if (this.vfFrame) this.vfFrame.style.opacity = Math.max(0, 1 - p * 2);
          }

          // Restore HUD opacity if scrolling back up from Act 4
          if (progress <= 0.85) {
            if (this.hudOverlay) this.hudOverlay.style.opacity = 1;
            if (this.vfFrame) this.vfFrame.style.opacity = 1;
            if (this.layerFront) this.layerFront.style.filter = 'contrast(1.08) brightness(1.0)';
          }
        },
      });
    },

    // 4. MOUSE PARALLAX & CLICK INTERACTIONS
    initInteractions: function () {
      // Audio toggle button
      if (this.soundToggleBtn) {
        this.soundToggleBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          this.soundEnabled = !this.soundEnabled;
          this.soundToggleBtn.innerHTML = this.soundEnabled
            ? '<span>SONIDO: ON</span> 🔊'
            : '<span>SONIDO: OFF</span> 🔇';
          this.soundToggleBtn.classList.toggle('muted', !this.soundEnabled);
          if (this.soundEnabled) this.playNikonZ9Shutter();
        });
      }

      // Tap / Click anywhere on stage to trigger Shutter & Flash
      if (this.container) {
        this.container.addEventListener('click', () => {
          this.playNikonZ9Shutter();
          if (this.flashScreen) {
            this.flashScreen.style.opacity = '1';
            setTimeout(() => {
              this.flashScreen.style.opacity = '0';
            }, 120);
          }
        });
      }

      // Mouse Parallax coordinates tracker
      window.addEventListener('mousemove', (e) => {
        this.targetMouseX = (e.clientX / window.innerWidth - 0.5) * 2; // -1 to 1
        this.targetMouseY = (e.clientY / window.innerHeight - 0.5) * 2; // -1 to 1
      });
    },

    // 5. ANIMATION LOOP (PARALLAX SMOOTHING, OPTICAL BREATHING, PARTICLES)
    renderLoop: function () {
      requestAnimationFrame(() => this.renderLoop());

      const time = performance.now() * 0.001;

      // Draw volumetric dust particles
      this.drawParticles(time);

      // Smooth mouse interpolation (LERP)
      this.mouseX += (this.targetMouseX - this.mouseX) * 0.06;
      this.mouseY += (this.targetMouseY - this.mouseY) * 0.06;

      // In Act 2: Apply optical focus breathing and mouse parallax tilt
      if (this.currentAct === 2 && this.layerFront) {
        const breathingScale = 1.0 + Math.sin(time * 2.5) * 0.015;
        const tiltY = this.mouseX * 4.5; // -4.5deg to +4.5deg
        const tiltX = -this.mouseY * 3.5; // -3.5deg to +3.5deg
        this.layerFront.style.transform = `scale(${breathingScale}) rotateY(${tiltY}deg) rotateX(${tiltX}deg)`;

        // Specular sheen slides across the glass with mouse
        if (this.specularSheen) {
          const sheenX = -40 + this.mouseX * 30;
          this.specularSheen.style.transform = `translateX(${sheenX}%) rotate(-12deg)`;
        }
      }
    },
  };

  // Auto-init on DOM load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => window.CaptooraCinematic.init());
  } else {
    window.CaptooraCinematic.init();
  }
})();
