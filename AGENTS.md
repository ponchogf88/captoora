> **FARMASI799 — continuidad vigente4nov2026:** leer primero [FARMASI_799_CONTINUAR_AQUI.md](FARMASI_799_CONTINUAR_AQUI.md). Incluye148prompts históricos completos, recetas locales realmente utilizadas, bitácora,799fuentes y143aprobadas. No usar los antiguos scripts/horarios del repo como autorización para regenerar caras, etiquetas o relanzar la noche.

# REGLAS MAESTRAS DE TRABAJO - AMDA AGENTIC ENGINE

## 🚀 PROTOCOLO VIGENTE (NOVIEMBRE 2026): SESIÓN 31 OCTUBRE, EMBAJADORAS FARMASI Y CAMPAÑA UNBOXING NAVIDEÑO
Cualquier agente que trabaje en Captoora debe consultar obligatoriamente:
1. **[ESTRATEGIA_VIRAL_UNBOXING_NAVIDENO_CAPTOORA.md](ESTRATEGIA_VIRAL_UNBOXING_NAVIDENO_CAPTOORA.md)**: El modelo de negocio y flywheel de fin de año. Se entregan las galerías digitales con opción de 1 foto gratis por mención en historias de Instagram (`@captoora.studio` y `@ponchogf88`) y venta de paquetes completos vía Stripe. El 25-30% de los ingresos se aparta para producir los cuadros Fine-Art de Montse ("La China") y las embajadoras destacadas, enviándolos a finales de noviembre para que hagan unboxing en Instagram Stories a principios de diciembre y detonen las reservaciones navideñas del estudio.
2. **[PLANTILLAS_MENSAJES_INFLUENCERS_CAPTOORA.md](PLANTILLAS_MENSAJES_INFLUENCERS_CAPTOORA.md)**: Textos aprobados por Poncho con el lente, estrellitas y corazón (`📸✨🤍`), arroba oficial `@captoora.studio`, la frase insignia *"nunca vamos a volver a ser tan jóvenes como en este instante"*, las invitaciones gratuitas al piloto de **Captoora Biométricos**, Gift Cards y los 2 mensajes personalizados exclusivos para Montse "La China" destacando su chispa, las marometas y a su bebé como embajador oficial para capturar su crecimiento junto a su familia.
3. **[GALERIA_CLIENTES_FARMASI.html](GALERIA_CLIENTES_FARMASI.html)**: Interfaz de galería interactiva con validador de Instagram Story y pasarela Stripe.

1. **CERO PASOS INTERMEDIOS PARA EL HUMANO:** Nunca le pidas al usuario ejecutar "paso 3 de 7" ni seguir tutoriales paso a paso. Mientras el usuario suelta ideas a velocidad luz, la IA debe absorber, procesar y construir de principio a fin los entregables.
2. **PROTOCOLO DE DESCARGA LIBRE DE IDEAS:** Cuando el usuario envíe ideas en ráfaga, la IA debe capturarlas inmediatamente, registrarlas en el Banco de Ideas, y delegarlas a los agentes correspondientes sin frenar la conversación.
3. **EJECUCIÓN AUTÓNOMA DE EXTREMO A EXTREMO:** La IA debe encargarse de la generación de código, archivos, guiones, tablas CSV, PDFs y prompts de video de forma autónoma.
4. **DESPACIO QUE LLEVO PRISA:** Calidad y precisión antes que velocidad. No romper nada.
5. **VERIFICA ANTES DE AVISAR:** Jamás dar por terminada una tarea sin abrir y auditar los archivos resultantes.
6. **AL CHILE (CERO COMPLACENCIAS):** Sin filtros ni respuestas complacientes. Directo y funcional.
7. **PROHIBICIÓN ESTRICTA DE PUBLICACIONES DE PURO TEXTO (LEY VISUAL CAPTOORA / GROKBOT / JIRU / ANTIGRAVITY):**
   - **Queda terminantemente prohibido generar o entregar posts/publicaciones que sean láminas de texto sobre fondos oscuros o colores sólidos.** La fotografía es 100% visual; una imagen dice más que mil palabras.
   - **Prohibido ensuciar o tapar la fotografía con bloques de texto:** En cualquier fotografía principal, el texto sobre la imagen debe ser CERO o reducirse exclusivamente a micro-iconografía/firma mínima que jamás tape al sujeto, el altar, la arquitectura o la escena.
   - **Toda historia larga, opinión técnica o crónica va en el Caption/Script o en un slide aparte**, acompañada de fotografías reales e imágenes de referencia que guarden relación directa con el tema.
   - **Prohibido recortar personas (`Zero Crop / 100% Full-Frame`):** Ninguna edición puede amputar brazos, manos, piernas, pies ni cabezas.
8. **LAS FOTOS DE SESIÓN NO TOCAN EL DISCO INTERNO** (Ley Captoora, 23 de octubre de 2026; texto vigente en https://github.com/ponchogf88/captoora/blob/main/docs/LEY_VISUAL_CAPTOORA.md):
   - Prohibido guardar rollos, RAW, pruebas, correcciones o carpetas de entrega en el SSD, el Escritorio, Descargas o este folder.
   - El camino es SD → nube. La edición se hace con el archivo que ya está en la nube.
   - Si una copia cae en un disco local, se borra cuando el peso en la nube coincida.
   - Solo se conservan dos archivos, ambos en la nube: la original cruda en Drive (`lic.jagf87@gmail.com`) y la edición final en Pixieset.
   - No instalar Google Drive de escritorio: replica otra vez los archivos en la computadora.
9. **POLÍTICA INQUEBRANTABLE DE CERO ELIMINACIÓN (`ZERO DELETE POLICY`):**
   - **Jamás borrar ni eliminar archivos del proyecto.** Si cualquier script, reporte, CSV, prototipo o activo se retira para limpiar u ordenar el repositorio o la nube, se debe mover íntegro a **`historico_y_archivos/`** y registrarse en `historico_y_archivos/INDICE_ARCHIVO_HISTORICO.md`.
10. **ARQUITECTURA MULTI-EQUIPO (`MacBook Pro 256GB` ↔ `iMac 2015`):**
   - **MacBook Pro (`/Users/user` · 256 GB):** Consola ligera y web (`captoora.studio`).
   - **iMac 2015 (`/Users/imac` · SSD Externo + HDD Interno):** Estación de carga pesada + extracción diaria de video vía ADB (`Xiaomi Redmi Note 8` `160305c5` + Artemis + Cámara **Eufy S350** 24/7).
   - Todos los scripts deben usar `scripts/captoora_paths.py` (nunca rutas fijas a `/Users/user` ni `/Users/imac`).

---

> Continuidad actualizada 25 oct 2026: leer primero [CONTINUAR_EN_OTRA_COMPUTADORA.md](CONTINUAR_EN_OTRA_COMPUTADORA.md). Las fechas y direcciones de inauguración que siguen son históricas; consultar el expediente y js/config.js para el estado vigente.


# Captoora — README para agentes


Este archivo es el mapa del repo. Si llegas nuevo: lee `IDENTITY.md` primero, luego esto.

Repo: https://github.com/ponchogf88/captoora
Pages: https://ponchogf88.github.io/captoora/
Owner GitHub: `ponchogf88`
Marca: **Captoora** (Captura + doble O)

---

## Misión inmediata (hoy → miércoles 23 sep 2026, 19:00)

Inaugurar el estudio físico en Colinas de San Jerónimo 11 con presencia digital *creíble*, no con un growth engine inflado.

Prioridad real (en este orden):

1. Nombre y logo consistentes (Captoora, monograma no recortado).
2. Google Business Profile con pin, fotos del local real, WhatsApp.
3. Instagram / Facebook con bio + link de reserva.
4. Hero del sitio: inauguración + CTA WhatsApp. Quitar métricas inventadas.
5. Dominio decente apuntando a Pages (o a un rebuild).
6. Recién entonces: motion premium (Rive / Remotion / Motion).

No empieces por el lente 3D del hero si el miércoles alguien no encuentra la dirección.

---

## Qué hay hoy en el repo (inventario honesto)

### Sitio (esqueleto, no producto final)

| Ruta | Qué es | Nota para agentes |
| --- | --- | --- |
| `index.html` | Home monolítica (~87 KB) | Demasiadas secciones. Nav saturado. Métricas +500 / 5.0 no verificadas. |
| `css/style.css` | Estilos dark + lima | Conservar paleta. Limpiar desktop nav. Arreglar crop del logo en móvil. |
| `js/main.js` | Interacciones, cotizador, WA | Confirmar que el wa.me apunte a `528140050088`, no al placeholder `5218100000000`. |
| `assets/logo.png` | Logo Canva provisional | Vectorizar. No recortar. |
| `assets/banner.png` | Portada Facebook | Usable como OG temporal. |
| `assets/*.MP4` | Video de muestra | Peso alto para Pages. Comprimir. |
| `lead_magnets/` | Guía LinkedIn + Lookbook Pumpkin Patch | Vivos. Bonus $300. No son la inauguración. |

### Documentos de estrategia (existen; no son el sitio)

| Archivo | Qué representa | Hueco |
| --- | --- | --- |
| `TABLERO_DE_AVANCE.md` | Declara el proyecto al 100% | Falso para launch. Tratarlo como checklist, no como verdad. |
| `GUIA_ESTRATEGICA_CAPTOORA.md` | Posicionamiento + precios + scripts WA | Buena base comercial. Precios sugeridos, no grabados en piedra. |
| `PRD_CAPTOORA_GROWTH_ENGINE.md` | Funnels, CAC/LTV, outreach | Útil post-inauguración. No bloquea el miércoles. |
| `CALENDARIO_REDES_CAPTOORA.md` | Calendario de contenido | Revisar que hable de inauguración 23 sep, no de un mes genérico. |
| `ESTRATEGIA_CAMPANAS_GRATUITAS_Y_SEO.md` | SEO / campañas free | Google Business primero. |
| `ESTRATEGIA_AIRBNB_EXPERIENCES_2026.md` | Canal Airbnb | Fuera de scope esta semana. |
| `CONTRATOS_POLITICAS_Y_TERMINOS.md` | Legal | Revisar con ojo de Legal Engineer antes de publicarlo en footer. |
| `outreach_tracker.csv` | Pipeline B2B 5 toques | Vacío o semilla. No fingir clientes. |
| `agente_prospeccion.py` | Script de research | Herramienta interna. No es producto de cliente. |
| `*.bat` | Lanzadores Windows / yt-dlp | Solo máquina local del dueño. |

---

## Canales (llenar handles reales; no inventar)

| Canal | Dato | Estado |
| --- | --- | --- |
| WhatsApp Business | +52 81 4005 0088 | Conectado en tablero |
| Sitio oficial | https://captoora.studio | Vivo (Porkbun DNS) |
| Galerías Pixieset | https://galeria.captoora.studio | Vivo |
| Sitio staging | https://ponchogf88.github.io/captoora/ | Respaldo GitHub Pages |
| Instagram | `@captoora.studio` | Oficial activo |
| Facebook Page | TBD | Pendiente |
| Google Business | TBD | Crítico esta semana |
| TikTok / Reels | Mismo handle que IG | Después del miércoles si no está |
| Calendly | Conectado a la cuenta Grok del dueño | Usar para “Agendar sesión” cuando el event type exista |
| Canva | Conectado | Fuente actual del logo |
| GitHub | ponchogf88/captoora | Este repo |

Si un handle no está confirmado, escríbelo como `TBD`. Nunca publiques un @ inventado.

---

## Stack creativo que el dueño ya eligió para la web *buena*

El sitio actual es HTML/CSS/JS estático en Pages. El destino que quiere:

- Motion premium en hero (cámara / lente que abre la marca)
- Referencias: Motion, Rive, Remotion
- Paleta: void / negro + lima
- Experiencia: un lente que *es* la O de Captoora, no un stock de Unsplash

No reescribas el esqueleto entero el domingo. Parchea el hero + métricas + inauguración. El rebuild motion va en paralelo *después* de que el link de reserva funcione.

---

## Objetivos

### Semana 0 (19–23 sep 2026)
- [ ] Identity sheet y este README vivos en el repo
- [ ] Hero sin cifras falsas
- [ ] Bloque de inauguración (fecha, hora, dirección, mapa, WA)
- [ ] Logo sin crop en móvil
- [ ] Google Business creado
- [ ] Bio IG lista
- [ ] Dominio comprado o al menos decidido

### Mes 1
- [ ] 15 reseñas Google reales
- [ ] Portafolio con fotos *del set de Colinas*, no stock
- [ ] Rebuild motion del hero
- [ ] URL final en todas las bios

### No-objetivos esta semana
Airbnb Experiences, agente de prospección autónomo, “growth engine”, 12 verticales en el hero, 3D del logo.

---

## Reglas para cualquier agente que edite este repo

1. Lee `IDENTITY.md`. El nombre es Captoora.
2. Lee `docs/LEY_VISUAL_CAPTOORA.md` antes de tocar una foto, una entrega o una publicación. Esa ley manda. Las fotos de sesión no tocan el disco interno.
3. No inventes reseñas, conteos ni handles.
4. No borres `index.html` sin dejar una home que reserve por WhatsApp.
5. Commits en español o inglés, pero mensajes concretos: `fix: quitar métrica +500 del hero`.
6. Imágenes nuevas del sitio van a `assets/` con nombres sin espacios. Los rollos de sesión no entran a este repo ni al disco interno: SD → nube. Se conservan solo el crudo en Drive y la final en Pixieset.
7. Si tocas precios, contrasta con `GUIA_ESTRATEGICA_CAPTOORA.md`.
8. Pregunta antes de cambiar el logo.

---

## Contacto del proyecto

Jesús Gutiérrez · WhatsApp estudio +52 81 4005 0088
X: @jagf87 · GitHub: ponchogf88

## Ley visual obligatoria

Antes de producir o entregar cualquier pieza visual comercial, leer y aplicar [docs/LEY_VISUAL_CAPTOORA.md](docs/LEY_VISUAL_CAPTOORA.md). Toda pieza debe incluir fotografía protagonista; quedan prohibidas las entregas exclusivamente tipográficas. Respetar la fuente fotográfica autorizada para cada encargo.


## Producción de contenido: instrucciones acumulativas
Para cualquier encargo de contenido, leer [campañas: entrada para agentes](campaigns/operacion-contenido/README.md), las reglas de producción y los ciclos de cuotas. Los accesos secretos solo se referencian en SECRET_REFERENCES.md, nunca se copian al repositorio. Mantener evidencia y no declarar todos los servicios aprovechados sin comprobarlo.
