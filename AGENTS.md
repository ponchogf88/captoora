> **FUENTE VIGENTE:** leer primero [`docs/ESTADO_ACTUAL.md`](docs/ESTADO_ACTUAL.md),
> [`docs/DECISIONES_PENDIENTES.md`](docs/DECISIONES_PENDIENTES.md) y
> [`docs/MAPA_REPOSITORIO.md`](docs/MAPA_REPOSITORIO.md). `js/config.js` manda para los
> datos renderizados por el sitio. Las fechas, direcciones y porcentajes posteriores en este
> archivo se conservan como contexto histórico y no deben publicarse.

# Captoora — README para agentes


Este archivo es el mapa del repo. Si llegas nuevo: lee `IDENTITY.md` primero, luego esto.

Repo: https://github.com/ponchogf88/captoora
Pages: https://ponchogf88.github.io/captoora/
Owner GitHub: `ponchogf88`
Marca: **Captoora** (Captura + doble O)

---

## Misión histórica (cerrada: miércoles 23 sep 2026, 19:00)

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
| Calendly | Cuenta del estudio `alfonsogf.88@gmail.com`. Enlace https://calendly.com/captoora/gift-card | Pendiente de autorización. No es el despacho. [Ficha](docs/CALENDLY_CAPTOORA.md) |
| Canva | Conectado | Fuente actual del logo |
| GitHub | ponchogf88/captoora | Este repo |

Si un handle no está confirmado, escríbelo como `TBD`. Nunca publiques un @ inventado.

## Agenda del estudio

Antes de leer reservas o escribir en un calendario, leer [docs/CALENDLY_CAPTOORA.md](docs/CALENDLY_CAPTOORA.md). Jesús Gutiérrez confirmó el 6 de noviembre de 2026 que Calendly Captoora es cuenta propia (`alfonsogf.88@gmail.com`), distinta del despacho (`https://calendly.com/ggconsultores`, correo exacto `l.jagf87@gmail.com`). Esa conexión no se consulta como si fuera el estudio.

---

## Stack creativo que el dueño ya eligió para la web *buena*

El sitio actual es HTML/CSS/JS estático en Pages. El destino que quiere:

- Motion premium en hero (cámara / lente que abre la marca)
- Referencias: Motion, Rive, Remotion
- Paleta: void / negro + lima
- Experiencia: un lente que *es* la O de Captoora, no un stock de Unsplash

No reescribas el esqueleto entero el domingo. Parchea el hero + métricas + inauguración. El rebuild motion va en paralelo *después* de que el link de reserva funcione.

---

## Objetivos históricos

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
9. Antes de leer o modificar Calendly, lee `docs/CALENDLY_CAPTOORA.md`. La cuenta del estudio no es la del despacho.

---

## Contacto del proyecto

Jesús Gutiérrez · WhatsApp estudio +52 81 4005 0088
X: @jagf87 · GitHub: ponchogf88

## Ley visual obligatoria

Antes de producir o entregar cualquier pieza visual comercial, leer y aplicar [docs/LEY_VISUAL_CAPTOORA.md](docs/LEY_VISUAL_CAPTOORA.md). Toda pieza debe incluir fotografía protagonista; quedan prohibidas las entregas exclusivamente tipográficas. Respetar la fuente fotográfica autorizada para cada encargo.


## Producción de contenido: instrucciones acumulativas
Para cualquier encargo de contenido, leer [campañas: entrada para agentes](campaigns/operacion-contenido/README.md), las reglas de producción y los ciclos de cuotas. Los accesos secretos solo se referencian en SECRET_REFERENCES.md, nunca se copian al repositorio. Mantener evidencia y no declarar todos los servicios aprovechados sin comprobarlo.
