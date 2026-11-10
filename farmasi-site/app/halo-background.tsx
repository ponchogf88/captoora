"use client";

import { useEffect, useRef } from "react";

const colors = ["255,156,106", "247,207,169", "224,222,237"];

export default function HaloBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    if (!canvas || !ctx) return;
    const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
    const pointer = { x: 0, y: 0, lastMoved: -Infinity, active: false };
    const dust = Array.from({ length: 92 }, (_, index) => ({
      x: Math.random(), y: Math.random(), offsetX: 0, offsetY: 0,
      phase: Math.random() * Math.PI * 2, size: .75 + Math.random() * 1.5,
      alpha: .16 + Math.random() * .36, color: colors[index % colors.length],
    }));
    let width = 0, height = 0, raf = 0, strength = 0, lastFrame = 0;
    let haloX = 0, haloY = 0;

    function render(now: number) {
      if (!ctx) return;
      raf = 0;
      const step = lastFrame ? Math.min((now - lastFrame) / 16.67, 2) : 1;
      lastFrame = now;
      const moving = pointer.active && now - pointer.lastMoved < 420 && !motion.matches;
      strength += ((moving ? 1 : 0) - strength) * (1 - Math.pow(.86, step));
      haloX += (pointer.x - haloX) * (1 - Math.pow(.8, step));
      haloY += (pointer.y - haloY) * (1 - Math.pow(.8, step));
      ctx.clearRect(0, 0, width, height);

      if (strength > .015) {
        const glow = ctx.createRadialGradient(haloX, haloY, 1, haloX, haloY, 158);
        glow.addColorStop(0, `rgba(255,140,82,${.29 * strength})`);
        glow.addColorStop(.34, `rgba(255,125,71,${.16 * strength})`);
        glow.addColorStop(1, "rgba(255,125,71,0)");
        ctx.fillStyle = glow;
        ctx.fillRect(haloX - 158, haloY - 158, 316, 316);
      }

      for (const p of dust) {
        const x = p.x * width, y = p.y * height;
        const dx = x - haloX, dy = y - haloY;
        const influence = Math.max(0, 1 - Math.hypot(dx, dy) / 220) * strength;
        const orbit = now / 385 + p.phase;
        const ease = 1 - Math.pow(.89, step);
        p.offsetX += ((-.6 * dx - .34 * dy + Math.cos(orbit) * 37) * influence - p.offsetX) * ease;
        p.offsetY += ((-.6 * dy + .34 * dx + Math.sin(orbit) * 37) * influence - p.offsetY) * ease;
        ctx.beginPath();
        ctx.fillStyle = `rgba(${p.color},${Math.min(.95, p.alpha + influence * .51)})`;
        ctx.arc(x + p.offsetX, y + p.offsetY, p.size + influence * 1.4, 0, 2 * Math.PI);
        ctx.fill();
      }
      if (moving || strength > .002 || dust.some((p) => Math.abs(p.offsetX) + Math.abs(p.offsetY) > .08)) {
        raf = requestAnimationFrame(render);
      } else {
        lastFrame = 0;
      }
    }

    function redraw() {
      if (!raf) raf = requestAnimationFrame(render);
    }

    function resize() {
      if (!canvas || !ctx) return;
      width = window.innerWidth;
      height = window.innerHeight;
      const scale = Math.min(window.devicePixelRatio || 1, 1.5);
      canvas.width = Math.round(width * scale);
      canvas.height = Math.round(height * scale);
      ctx.setTransform(scale, 0, 0, scale, 0, 0);
      redraw();
    }

    function move(event: PointerEvent) {
      if (event.pointerType === "touch" || motion.matches) return;
      if (!pointer.active || strength < .015) {
        haloX = event.clientX;
        haloY = event.clientY;
      }
      pointer.x = event.clientX;
      pointer.y = event.clientY;
      pointer.lastMoved = performance.now();
      pointer.active = true;
      redraw();
    }

    function release() {
      pointer.active = false;
    }

    function resetMotion() {
      release();
      strength = 0;
      for (const p of dust) p.offsetX = p.offsetY = 0;
      redraw();
    }

    resize();
    window.addEventListener("resize", resize, { passive: true });
    window.addEventListener("pointermove", move, { passive: true });
    document.documentElement.addEventListener("pointerleave", release);
    window.addEventListener("blur", release);
    motion.addEventListener("change", resetMotion);
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
      window.removeEventListener("pointermove", move);
      document.documentElement.removeEventListener("pointerleave", release);
      window.removeEventListener("blur", release);
      motion.removeEventListener("change", resetMotion);
    };
  }, []);

  return <canvas ref={canvasRef} className="halo-background" aria-hidden="true" />;
}
