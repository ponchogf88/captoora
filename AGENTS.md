> **Pertenencia:** repo [ponchogf88/captoora](https://github.com/ponchogf88/captoora) · Drive [POR CONFIRMAR] · WhatsApp +52 81 4005 0088 · Calendly [POR CONFIRMAR]
> **YLOSABES.md:** [POR CONFIRMAR]. No está en el repositorio en este corte (1 nov 2026). No se redacta un sustituto.

# REGLAS MAESTRAS DE TRABAJO - AMDA AGENTIC ENGINE

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

---

# Captoora — mapa para agentes (noviembre 2026)

Este archivo es el mapa del repo. Si llegas nuevo, respeta esta jerarquía y no la reordenes:

1. `IDENTITY.md`
2. `SOUL.md`
3. `AGENTS.md`
4. `PROJECT.md`
5. `CONTEXT.md`
6. `USER.md`

`START_HERE.md` conserva otro párrafo de arranque. No se reescribió en este corte.

Repo: https://github.com/ponchogf88/captoora
Pages: https://ponchogf88.github.io/captoora/
Owner GitHub: `ponchogf88`
Marca: **Captoora** (Captura + doble O)
Fundador: el maestro Jesús Gutiérrez

El encargo de inauguración del 23 de septiembre de 2026 es historial. Vivía en este archivo como si siguiera siendo la misión. Ya no lo es. El corte vigente está en `CONTEXT.md`. Los logs de esas semanas están en `docs/archivo/`.

## Qué hacer ahora

1. Landings motion por marca. Guías: `docs/motion/`.
2. Dejar corriendo en la iMac un stack mínimo Three.js + GSAP + Remotion. Inventario: `STACK.md`.
3. El agente Radar Motion Trends está activo. Su ubicación en el repo: [POR CONFIRMAR].
4. El explainer de Biometrics ya está en `CAPTOORA_BIOMETRICS/biometrics_motion_explainer.html`.

Antes de producir una pieza: `PROHIBIDO.md` y `docs/LEY_VISUAL_CAPTOORA.md`.

El PR #3 (rama `cursor/motion-stack-demo-ad76`, demo de movimiento Signature) está fusionado. No se toca desde un corte de limpieza.

## Qué hay en el repo

### Sitio

| Ruta | Qué es | Nota para agentes |
| --- | --- | --- |
| `index.html` | Home | Carga Three.js y GSAP por CDN. Los `wa.me` revisados en este corte apuntan a `528140050088`. |
| `js/config.js` | Datos de la home | Dirección Álamos 165, paquetes, portafolio GlowTours y Chipinque. `reviews.googleUrl` vacío. |
| `js/main.js` | Interacciones y WhatsApp | Mismo número `528140050088`. |
| `css/style.css` | Estilos | Paleta del esqueleto. No es la paleta de las cinco marcas. |
| `captoora_signature.html`, `captoora_biometrics.html`, `captoora_studio.html`, `captoora_pop.html`, `captoora_corp.html` | Prototipos de marca | No son la landing motion cerrada. Ver `docs/motion/`. |
| `CAPTOORA_BIOMETRICS/` | Biometrics | README propio y explainer HTML. |
| `assets/logo.png` | Logo Canva provisional | No es el lockup definitivo (`IDENTITY.md`). No recortar. Preguntar antes de cambiar el logo. |
| `lead_magnets/` | Guía LinkedIn y lookbook | Existen. No son el trabajo de noviembre. |

### Documentos que sí mandan en noviembre

| Archivo | Qué es |
| --- | --- |
| `STACK.md` | Hardware, flash, software, regla de `apis.txt` |
| `PROHIBIDO.md` | Sesión que el maestro detesta (aún sin describir) y portafolio sin autorización |
| `docs/motion/*_MOTION.md` | Mood de cada marca |
| `docs/LEY_VISUAL_CAPTOORA.md` | Ley visual. No se reescribe |
| `docs/archivo/LEEME.md` | Dónde quedaron bitácoras y calendarios de octubre |
| `CONTEXT.md` | Prioridades de este mes |
| `GUIA_ESTRATEGICA_CAPTOORA.md` | Precios y scripts. Contrastar antes de publicarlos. No están grabados en piedra |
| `CALENDARIO_REDES_CAPTOORA.md` | Calendario de redes que se quedó en la raíz. No es el plan de noviembre |

`TABLERO_DE_AVANCE.md` es un corte del 18 oct, no un porcentaje actual.

## Canales

| Canal | Dato en el repo | Estado en este corte |
| --- | --- | --- |
| WhatsApp Business | +52 81 4005 0088 | Escrito en `js/config.js`, `index.html` y `js/main.js` |
| Sitio staging | https://ponchogf88.github.io/captoora/ | URL de Pages escrita en el README |
| Dominio final | — | [POR CONFIRMAR] |
| Instagram | `@Captoora.studio` en `js/config.js` y `USER.md` | Perfil en vivo: [POR CONFIRMAR] |
| TikTok | `@captoora.studio` | La nota del 26 oct dice que el perfil público no se verificó. Sigue [POR CONFIRMAR] |
| X | `@captoora_studio` | Perfil en vivo: [POR CONFIRMAR] |
| Facebook Page | — | [POR CONFIRMAR] |
| Google Business | `reviews.googleUrl` vacío | [POR CONFIRMAR] |
| Calendly | Sin URL en el repo | [POR CONFIRMAR] |
| GitHub | `ponchogf88/captoora` | Este repo |

Si un handle no está en `js/config.js` o en `USER.md`, se escribe [POR CONFIRMAR]. No se publica un @ nuevo.

## Stack

El detalle está en `STACK.md`. Resumen: iMac 2015, Intel i5, 24 GB, HDD → SSD en curso, Rolling TV por HDMI, iPhone con el atajo «Hey Grok», Godox TT600 en manual con X2T y softbox, Nikon D3500 en M a 1/160, f/5.6, ISO 100. Las llaves solo en `apis.txt` local de Desktop/Projects.

## Reglas para cualquier agente que edite este repo

1. Lee `IDENTITY.md`. El nombre es Captoora.
2. Lee `docs/LEY_VISUAL_CAPTOORA.md` antes de tocar una foto, una entrega o una publicación. Esa ley manda. Las fotos de sesión no tocan el disco interno.
3. Lee `PROHIBIDO.md`. Hay unas 30 sesiones sin consentimiento. El tipo de sesión que el maestro detesta está en [POR CONFIRMAR: el maestro la describirá] y no se produce.
4. No inventes reseñas, conteos ni handles.
5. No borres `index.html` sin dejar una home que reserve por WhatsApp.
6. Commits en español o inglés, con mensaje concreto.
7. Imágenes nuevas del sitio van a `assets/` con nombres sin espacios. Los rollos de sesión no entran a este repo ni al disco interno: SD → nube. Se conservan solo el crudo en Drive y la final en Pixieset.
8. Si tocas precios, contrasta con `GUIA_ESTRATEGICA_CAPTOORA.md` y con `js/config.js`. Si chocan, no elijas una cifra: márcala [POR CONFIRMAR].
9. Pregunta antes de cambiar el logo.
10. No toques `.env.example` para «ordenar» secretos. No commitees `apis.txt`.

## Contacto del proyecto

Jesús Gutiérrez, el maestro. WhatsApp del estudio +52 81 4005 0088.
X personal escrito en `USER.md`: @jagf87. GitHub: ponchogf88.
Las cuentas personales no se usan para publicar Captoora salvo que él lo diga.

## Ley visual obligatoria

Antes de producir o entregar cualquier pieza visual comercial, leer y aplicar [docs/LEY_VISUAL_CAPTOORA.md](docs/LEY_VISUAL_CAPTOORA.md). Toda pieza debe incluir fotografía protagonista; quedan prohibidas las entregas exclusivamente tipográficas. Respetar la fuente fotográfica autorizada para cada encargo.

## Producción de contenido: instrucciones acumulativas

Para cualquier encargo de contenido, leer [campañas: entrada para agentes](campaigns/operacion-contenido/README.md), las reglas de producción y los ciclos de cuotas. Los accesos secretos solo se referencian en SECRET_REFERENCES.md, nunca se copian al repositorio. Mantener evidencia y no declarar todos los servicios aprovechados sin comprobarlo.
