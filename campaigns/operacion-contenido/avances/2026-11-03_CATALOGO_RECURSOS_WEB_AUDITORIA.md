# Auditoría del catálogo de recursos web · 2026-11-03 02:00 CST

## Archivo

- `LISTA_MAESTRA_RECURSOS_DISENO_PAGINAS.pdf`
- 12 páginas · 707,950 bytes · SHA-256 `b3ac126f6f2c1b70923cca12e82b1e23b7f1fe782125c89cbb9b505ef554fc71`.
- El documento declara 76 recursos en siete categorías y “100% cotejado”. Esa declaración pertenece al documento y no fue demostrada por esta revisión.

## Revisión realizada

Se extrajo y leyó el texto completo de las 12 páginas. El catálogo mezcla bibliotecas de interfaz, motores 3D/video, galerías de inspiración, infraestructura de negocio y herramientas de IA. También contiene datos que pueden cambiar —precios, estrellas, rendimiento, licencias, disponibilidad y capacidades— y propuestas comerciales no autorizadas, por ejemplo tarifas y pagos.

## Selección útil para la web CAPTOORA

Prioridad de prueba, sujeta a licencia y rendimiento real:

1. Motion/Framer Motion para microinteracciones y transiciones accesibles.
2. GSAP + ScrollTrigger o Lenis, solo si el prototipo demuestra beneficio y respeta reducción de movimiento.
3. Three.js/React Three Fiber para un único hero o módulo 3D medido, no para decorar toda la página.
4. Plausible para analítica, previa revisión de privacidad, alojamiento y coste.
5. Cal.com para agenda, sin habilitar pagos ni publicar flujos hasta validar oferta y permisos.

Recursos de inspiración como Godly, Scrolltide, 60fps.design y galerías similares se consideran referencia; no acreditan derecho a copiar diseños, código, imágenes o prompts.

## Riesgos y correcciones necesarias

- Verificar cada URL, licencia, mantenimiento y compatibilidad antes de instalar.
- No adoptar cifras de estrellas, FPS, carga GPU, tamaños o capacidades sin fuente viva fechada.
- No usar tarifas, anticipos, promociones, testimonios ni promesas que no estén autorizadas.
- No desplegar audio automático; cualquier sonido debe ser opcional y accesible.
- Probar en iPhone y en los equipos disponibles, con `prefers-reduced-motion`, carga lenta y fallback sin WebGL.
- Evitar integrar simultáneamente varias bibliotecas que resuelven el mismo efecto.

## Decisión editorial

Conservar como mapa de investigación, no como especificación aprobada ni prueba de capacidad. No se instaló, contrató ni ejecutó ningún servicio externo en este ciclo.

## Siguiente acción

Convertir la selección prioritaria en una matriz de verificación viva —URL, licencia, coste, mantenimiento, peso, accesibilidad y caso de uso— antes de modificar la web.

## Herramientas ejecutadas

`pdfinfo`, extracción local con `pypdf`, lectura, `stat` y SHA-256. Créditos consumidos: 0.
