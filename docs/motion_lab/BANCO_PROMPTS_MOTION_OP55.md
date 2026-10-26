# 🧠 BANCO DE PROMPTS Y METODOLOGÍA: OPUS 5.5 MOTION LAB & REA
> **Arquitectura:** Pipeline Determinista 60 FPS (@skunzu / @flxrnc) + Protocolo Clean Room REA (`morluto/rea`).

---

## 1. El Pipeline de 4 Fases para Motion Design (@skunzu)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    STAGE 01     │ ──> │    STAGE 02     │ ──> │    STAGE 03     │ ──> │    STAGE 04     │
│     AST GEN     │     │     PHYSICS     │     │     RASTER      │     │   WASM TRANS    │
│  (Opus 5.5 LLM) │     │  (Motion + R3F) │     │   (Canvas/GL)   │     │  (ffmpeg.wasm)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

> **Axioma Central:**  
> *"La IA escribe la escena y los keyframes matemáticos (`seek(t)`); las librerías resuelven la física del resorte y la luz de estudio; la GPU y ffmpeg hacen el resto a 60 FPS limpios."*

---

## 2. Los 10 Repositorios Núcleo del Ecosistema

1. **`threejs/three.js` (116.3k ⭐):** Motor 3D WebGL para óptica de cámara, orbit controls y shaders de diafragma mecánico.
2. **`motion-division/motion` (34.0k ⭐):** Motor de físicas elásticas de resortes (*spring physics*), masa y amortiguación sin bloqueo del DOM.
3. **`fabricjs/fabric.js` (31.4k ⭐):** Canvas 2D vectorial interactivo para composición de tarjetas y overlays fotográficos a 60 FPS.
4. **`ffmpegwasm/ffmpeg.wasm` (17.8k ⭐):** Transcodificación y unión de video/audio en el cliente sin servidores externos.
5. **`pmndrs/drei` (9.9k ⭐):** Iluminación de estudio fotográfico HDR, sombreado suave y controles orbitales amortiguados en Three.js.
6. **`rive-app/rive-runtime` (1.2k ⭐):** Máquinas de estado vectoriales interactivas ultra-ligeras corriendo a 120 FPS.
7. **`shuding/cobe` (5.9k ⭐):** Globo 3D WebGL interactivo en menos de 5KB.
8. **`canvas-confetti` (12.7k ⭐):** Física de partículas ligeras para dinámicas de celebración o confeti en reels.
9. **`twgl.js` (3.0k ⭐):** Helpers minimalistas para compilar fragment shaders GLSL sin sobrecarga.
10. **`morluto/rea` (65k ⭐):** Protocolo de ingeniería inversa Clean Room para desarmar animaciones virales y reconstruirlas nativas.

---

## 3. Protocolo REA (Reverse Engineer Anything) — Plantilla Maestra

Usa este prompt estructurado cuando quieras replicar la física de cualquier video de referencia (como el video de Duolingo o interfaces virales de X):

```markdown
<prompt>
<goal>
Analizar la animación y micro-interacciones de {{FEATURE}} en {{VIDEO_O_REFERENCIA}} para comprender su física matemática, timing y transiciones exactas, y generar la especificación determinista pura en SPEC.md para reproducirla en Captoora Motion Lab.
</goal>

<clean_room>
Regla de oro:
- Estudiar el comportamiento visual y los fotogramas clave.
- Registrar la física (frecuencia Hz, coeficiente de amortiguamiento zeta, velocidad inicial).
- Nunca copiar código propietario ni activos ajenos; construir una versión 100% nativa con la identidad Dark Void / Lente de Captoora Studio.
</clean_room>

<pipeline_check>
- Motor de render: Función seek(t) evaluada a 60 cuadros por segundo.
- Física de resorte:
  • Rebote táctil / botón: zeta = 0.42, freq = 9.0 Hz
  • Tarjeta flotante / cristal: zeta = 0.78, freq = 4.5 Hz
  • Cámara de cine / parallax: zeta = 0.92, freq = 2.2 Hz
- Salida: ffmpeg libx264 crf 16 pix_fmt yuv420p a 60fps.
</pipeline_check>

<report>
Entregar:
1. Tabla de keyframes críticos (t = 0.0s, 0.3s, 0.8s, 1.5s, 3.0s).
2. Código TypeScript / React con Framer Motion o Remotion.
3. Verificación de que ninguna persona o producto resulte recortado (Ley Visual Captoora Zero Crop).
</report>
</prompt>
```

---

## 4. Banco de Sitios de Referencia Curados para Estudio Fotográfico

* **`60fps.design`:** La mayor colección de animaciones fluidas a 60 cuadros por segundo para estudiar velocidad y rebote.
* **`scrolltide.co`:** Más de 600 prompts y código fuente de experiencias 3D y desplazamiento impulsado (*scroll-driven*).
* **`motion-primitives.com`:** Componentes animados de texto progresivo, revelado de imagen y botones de cristal.
* **`reactbits.dev`:** Fondos estelares, mallas cósmicas y efectos ópticos sin peso de video.
* **`detail.design`:** Estudio de micro-detalles de interfaz premium.
