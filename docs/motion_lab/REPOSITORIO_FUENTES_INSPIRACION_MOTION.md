# 🛸 REPOSITORIO MAESTRO DE INSPIRACIÓN & MOTION DESIGN — CAPTOORA STUDIO

Catálogo curado de plataformas, estudios de animación, sistemas de diseño, bibliotecas de componentes y benchmarks visuales para la producción de animaciones con física de resortes (*spring physics*), estética Dark Void / Glassmorphism y motion interactivo estilo Duolingo, Linear y Apple.

---

## 1. Plataformas de Inspiración & Benchmarks de Clase Mundial

### A. Referencias de Motion & Micro-interacciones
* **Mobbin (Motion & Transitions):** [mobbin.com](https://mobbin.com) — La biblioteca más grande de grabaciones de pantalla de micro-animaciones en iOS y Android (onboardings, transiciones de tarjetas, menús y checkout).
* **Godly Website Design:** [godly.website](https://godly.website) — Curaduría diaria de los mejores sitios web del mundo con animaciones webGL, scroll interactivo y estética de lujo.
* **Awwwards (Animation & WebGL):** [awwwards.com/websites/animation](https://www.awwwards.com/websites/animation/) — Ganadores de sitio del día con foco en transiciones cinematográficas y shaders 3D.
* **Httpster:** [httpster.net](https://httpster.net) — Muestrario tipográfico y de transiciones minimalistas.
* **Siteinspire:** [siteinspire.com](https://www.siteinspire.com) — Filtrado por tipo de interacción (hover, paginación, transiciones de pantalla completa).

### B. Estudios de Animación de Referencia (Gold Standard)
* **Ordinary Folk:** [ordinaryfolk.co](https://ordinaryfolk.co) — Maestros del motion design narrativo, timing elástico y transiciones orgánicas fluidas.
* **Cuberto:** [cuberto.com](https://cuberto.com) — Creadores de la tendencia de cursores magnéticos, distorsiones líquidas y navegación elástica en móvil y desktop.
* **Illo:** [illo.tv](https://illo.tv) — Estudio italiano creador de estilos visuales limpios, paletas de color con carácter y animaciones explicativas geométricas.
* **Buck Design:** [buck.co](https://buck.co) — Referencia global en animación de personajes e identidades de marca en movimiento.
* **Giant Ant:** [giantant.ca](https://giantant.ca) — Storytelling visual y transiciones de cámara suaves sin cortes duros.

### C. Benchmarks de Marcas Tecnológicas
* **Duolingo Design (Motion & Characters):** [design.duolingo.com](https://design.duolingo.com) — El estándar de micro-animaciones de recompensa, rebote táctil en botones (Keycaps 3D con física) y videos explicativos ultra-dinámicos.
* **Linear.app:** [linear.app](https://linear.app) — La referencia suprema de la estética Dark Void: negros profundos, bordes de 1px con gradiente sutil, velocidad instantánea y física de resorte rápida sin retraso.
* **Apple Interactive Displays:** [apple.com](https://apple.com) — Parallax sutil de hardware, lentes de cámara que se ensamblan en 3D al hacer scroll y tipografía gigante que revela fotos.
* **Raycast:** [raycast.com](https://raycast.com) — Animaciones de teclado, atajos, desenfoque de fondo (*backdrop-filter*) e iconografía flotante.

---

## 2. Bibliotecas de Código, Motores & Toolkits de Animación

* **Motion.dev (antes Framer Motion):** [motion.dev](https://motion.dev) — La librería estándar de animaciones declarativas y spring physics para React y JavaScript moderno.
* **Remotion:** [remotion.dev](https://remotion.dev) — Motor programático para renderizar videos MP4 reales a 60fps usando código React y Tailwind.
* **Rive:** [rive.app](https://rive.app) — Animaciones interactivas ligeras con máquinas de estado que responden al cursor y a eventos en tiempo real (reemplazo moderno de Lottie).
* **LottieFiles:** [lottiefiles.com](https://lottiefiles.com) — Animaciones vectoriales JSON exportadas desde After Effects lista para web y apps.
* **Three.js Journey / React Three Fiber:** [threejs.org](https://threejs.org) / [docs.pmnd.rs](https://docs.pmnd.rs) — 3D en el navegador: diafragmas mecánicos, cristales, partículas y reflejos de lentes fotográficos.
* **GSAP (GreenSock):** [gsap.com](https://gsap.com) — El motor de animación web más rápido y robusto para timelines complejos y scrollTrigger.

---

## 3. Cuentas y Canales Clave de Motion & Shaders (Inspiración Diaria)

* **Instagram & X / Twitter:**
  * `@flxrnc` (Florian) — Creador de la arquitectura Opus 5.5 Motion Lab, renders deterministas `seek(t)` y físicas matemáticas puras.
  * `@cmaboratory` (CMA) — Shaders interactivos, cristales y deformaciones ópticas en WebGL.
  * `@lusionltd` (Lusion) — Experiencias visuales inmersivas en 3D para marcas de lujo.
  * `@emilkowalski_` (Emil Kowalski) — Micro-interacciones, animaciones de gestos táctiles y diseño de componentes fluidos.
  * `@pablocubico` (Pablo Stanley) — Ilustración dinámica y motion narrativo.

---

## 4. Clasificación de Estilos para Captoora

| Estilo Visual | Sensación | Fórmulas / Parámetros | Caso de Uso en Captoora |
| :--- | :--- | :--- | :--- |
| **Dark Void / Obsidian** | Lujo, misterio, alta fidelidad | Fondo `#000000`, bordes `rgba(255,255,255,0.08)`, resorte $\zeta = 0.92, f = 2.2\text{ Hz}$ | Portadas de videos, Hero web, branding corporativo |
| **Glassmorphism / Frosted** | Elegancia táctil, profundidad Z | `backdrop-filter: blur(20px)`, resorte $\zeta = 0.78, f = 4.5\text{ Hz}$ | Tarjetas de precios, carruseles de fotos, badges |
| **Tactile Keycap / Duolingo** | Satisfacción física, dinamismo | Rebote mecánico elástico $\zeta = 0.42, f = 9.0\text{ Hz}$ | Botones de WhatsApp, CTAs, stickers de poses |
| **Cámara EFI / Parallax Óptico** | Cinematográfico, apertura de lente | Diafragma 6-8 palas, rotación `ease-out`, zoom z $1.0 \rightarrow 1.15$ | Intros de reels, transiciones de sesión fotográfica |

---

## 5. Plataformas Clave Adicionales (Curaduría de la Comunidad X)

* **`60fps.design`:** El catálogo definitivo de animaciones fluidas a 60 FPS para estudiar timing y aceleración.
* **`scrolltide.co`:** Más de 600 prompts y código fuente de experiencias 3D y scroll-driven design.
* **`detail.design`:** Colección de micro-interacciones y detalles de producto que marcan la diferencia.
* **`collectui.com` & `recent.design`:** Ideas diarias de interfaz y micro-layouts listos para maquetar.
* **`theinternetdesigns.com` & `bestdesignsonx.com`:** Los diseños más destacados compartidos por la comunidad global de X.
* **`navbar.gallery` & `footer.design`:** Referencias especializadas para cabeceras y cierres de página.
* **`VoiceStudio` (`github.com/debpalash/VoiceStudio`):** Clonación y doblaje de voz en local para locuciones de reels.
* **`REA` (`github.com/morluto/rea`):** Ingeniería inversa limpia para desarmar micro-interacciones de apps virales.
