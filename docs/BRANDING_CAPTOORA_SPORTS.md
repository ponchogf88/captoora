# Manual de Marca & Business DNA — Captoora Sports (`captoora.studio`)

> **Documento Maestro de Identidad, Posicionamiento, Sistema Visual y Guardrails de Comunicación**  
> Sede: Av. Paseo de los Álamos 165, Colinas de San Jerónimo, Monterrey, N.L. · Director: Jesús Gutiérrez (`chuy@captoora.studio` · WhatsApp `+52 81 4005 0088`)

---

## 1. Esencia y Posicionamiento de Marca

### Identidad Nominal
- **Nombre Comercial Principal:** **Captoora Sports** / **Captoora Studio** / **Captoora**
- **Lockup Editorial (Navbar):** `CAPTOORA` / `ESTUDIO FOTOGRÁFICO // SPORTS`
- **Dominio y Canales:** `https://captoora.studio/sports` · `https://galeria.captoora.studio` · `@captoora.studio`

### Taglines y Declaraciones Oficiales
- **Tagline Web / Meta:** *"Fotografía deportiva a 1/2000s, entrega el mismo día, Túnel 3D interactivo y trofeos en acrílico LED · Monterrey y SPGG."*
- **Declaración Editorial (Hero):** *"Desde San Jerónimo, Monterrey hasta la duela de Arena CDMX. Cada disparo lleva la velocidad quirúrgica y la historia que no se ve desde las gradas."*
- **Manifiesto:** *"Quiero que nos recuerden por más que un clic de cámara — congelamos el alma y la velocidad del atleta de élite."*
- **Cierre / Finale:** *"RECORDS WERE MADE TO BE BROKEN"*

### Posicionamiento Estratégico
Captoora **no se posiciona como fotógrafo social, amateur ni "freelance"**. Se posiciona como una **firma de ingeniería visual de élite deportiva** (estándar NFL / NBA / NCAA), combinando:
1. **Captura quirúrgica de alta velocidad:** Global Shutter (`Sony A9 III`, `1/1250s–1/2000s`), ópticas `f/2.8` y flash HSS (`1/8000s`) con cero desenfoque de movimiento.
2. **Entrega digital inmediata (*Halftime Blitz*):** 10–15 fotos calibradas en `9:16` entregadas en 15 minutos al medio tiempo y galería completa el mismo día (`< 2h` post-partido en duela; `48–72h` en sesiones completas Small Business).
3. **Plataforma Web 3D Interactiva (`captoora.studio`):** Túnel 3D (*Scrolltide*) y tarjetas holográficas interactivas en lugar de carpetas planas de Google Drive o Pixieset.
4. **Productos físicos de lujo autofinanciables:** Trofeos en acrílico óptico grabado con láser sobre base de nogal LED (y marcos de madera sólida *El Marco San Pedro*), producidos localmente en `3–5 días hábiles` en taller de Monterrey/SPGG.

### Filosofía Comercial ("Embudo Invisible")
Nadie se despierta queriendo pagar a un fotógrafo; los tomadores de decisión compran **estatus y validación de comunidad, prueba de ROI para patrocinadores, cero carga operativa y autofinanciamiento a riesgo cero**. La demanda se atrae mediante pruebas visuales (*Antes vs. Después*, portal 3D, piezas físicas LED) antes de hablar de precio.

---

## 2. Sistema Visual (Paleta, Tipografía y Activos)

### A. Paleta de Color Oficial

#### 1) Ecosistema Público Flagship (`captoora_sports.html`) — *Dark Athletic Editorial + Cyber Cyan/Lime*
| Token | Hex / Valor | Uso Principal |
| :--- | :--- | :--- |
| `--color-ink-deep` | `#060509` | Fondo maestro profundo (también `#020307` en escenario 3D y `#080c14` en marcos del túnel) |
| `--color-ink` | `#0c0b11` | Fondo de secciones principales |
| `--color-ink-card` | `#13121b` | Superficie de tarjetas y módulos |
| `--color-bone` | `#f7f4ef` | Tipografía principal y contraste editorial (`rgba(247,244,239,0.65)` muted / `0.14` subtle) |
| `--cyan` | `#00f0ff` | Acento tecnológico / telemetría |
| `--lime` | `#CCFF00` | Acento de alto impacto / CTAs deportivos |
| `--gold` | `#d4af37` | Acento de prestigio / campeonato |

#### 2) Playbook & Presentaciones Ejecutivas (`docs/presentacion_captoora.html`) — *Obsidian, Gold & Volt*
| Token | Hex | Uso |
| :--- | :--- | :--- |
| `--bg` / `--surface` / `--surface-2` | `#050608` / `#0b0e14` / `#111622` | Fondos y tarjetas ejecutivas |
| `--gold` / `--gold-bright` | `#c9a23f` / `#ecd28a` | Acentos de lujo y bordes (`rgba(201,162,63,0.34)`) |
| `--volt` | `#c6ff00` | Energía deportiva y métricas clave |
| `--cyan` / `--coral` / `--emerald` | `#38bdf8` / `#fb7185` / `#34d399` | Indicadores de estado y canales |
| `--text` / `--muted` | `#f5f4ef` / `#98a2b3` | Texto principal y secundario |

#### 3) Dossiers PDF para Clientes & Dashboard Interno
- **PDFs / Mockups (`captoora_agents/mockups.py`):** Negro absoluto `#000000`, Hueso `#f4efe6`, Oro `#c9a23f`, Volt `#c6ff00`, Oro cálido `#d4b483` / `#ded7ca`.
- **Dashboard Interno (`dashboard/index.html`):** Estilo *Liquid Glass Luxury Atelier* (sin neón): `#08090c` (`--canvas-dark`), `#0e1015` (`--canvas-surface`), `#c5a880` (`--champagne`), `#dfcbb5` (`--champagne-light`), `#d2d5de` (`--platinum`), `#f5f4ef` (`--bone-white`).

### B. Tipografía
| Rol | Familia | Pesos | Uso |
| :--- | :--- | :--- | :--- |
| **Display / Títulos** | `Cinzel` (serif) | 400, 500, 600, 700 | Títulos hero, encabezados de prestigio, marca |
| **Editorial / Citas** | `Cormorant Garamond` (serif) | 300–600, italic 400 | Manifiesto, citas de marca, acentos de lujo |
| **Cuerpo / UI** | `Plus Jakarta Sans` (o `Inter`) | 300–700 | Lectura general, descripciones y tarjetas |
| **Técnico / Telemetría** | `JetBrains Mono` (monospace) | 300–600 | Eyebrows, especificaciones (`1/2000s`), CTAs, datos |
| **Print / PDF** | `Didot` / `Bodoni 72` + `Avenir Next` | — | Dossiers impresos/PDF y documentos formales |

### C. Activos Gráficos y Logotipos (`assets/`)
- **Logos principales:**
  - `assets/CAPTOORA_LOGO_TRANSPARENT.png` (logotipo principal para portadas, PDFs y encabezados)
  - `assets/CAPTOORA_FAVICON_512x512.png` (emblema/favicon y loader)
  - `assets/CAPTOORA_WOLF_CLEAN_TRANSPARENT.png` y `assets/CAPTOORA_WOLF_PURE_TRANSPARENT.png` (isotipo lobo)
  - `assets/CAPTOORA_SIGNATURE_LOGO.png` (firma de marca)
- **Imagen insignia:** `assets/hero-portrait.png` (retrato de atleta con visor blanco y jersey rojo `#11`).
- **Portafolio autorizado:** 78 fotografías en `assets/portfolio/` (`toros`, `tec`, `soccer`, `nidos`, `football`, `sports`, `cheer`) + 14 momentos insignia en `assets/signature_moments/` + 7 héroes de nicho en `assets/niche_heroes/`.

---

## 3. Tono de Voz y Reglas Estrictas de Copy (Guardrails)

### Personalidad Verbal
- **Español mexicano (`es-MX`)** editorial, consultivo, seguro y cercano-profesional (hospitalidad *White-Glove* combinada con precisión técnica).
- Vocabulario clave: *ingeniería visual, congelar el alma y la velocidad, entrega el mismo día, estándar de élite, calibración óptica, piezas escultóricas de colección, riesgo cero*.

### Reglas Prohibidas (Hard Guardrails)
1. **Cero menciones a "IA" o "Inteligencia Artificial" frente al cliente:** Nunca atribuir el trabajo a IA. Si se describe el proceso técnico, usar: **"Pipeline Neuronal de Calibración Óptica y Reducción Cromática en Tiempo Real"**.
2. **Nunca usar el verbo "presumir"** (ni sus conjugaciones): Sustituir siempre por **"proyectar imagen profesional / al nivel de excelencia"**.
3. **Separación estricta de tiempos de entrega (SLA):**
   - **Entrega digital:** Medio tiempo (`15 min`) / mismo día (`< 2h` en eventos deportivos); `48–72h` en sesiones completas Small Business.
   - **Entrega física:** Trofeos acrílicos LED y marcos de madera sólida en `3–5 días hábiles` (taller local MTY/SPGG), con opción de diferir el pago físico a un **2.º momento**.

---

## 4. Públicos Objetivo (ICP) y Oferta Comercial

### Segmentos Prioritarios
1. **Clubes de Pádel, Raqueta y Ligas Deportivas (MTY / SPGG):** Torneos con patrocinadores (`$20k–$60k MXN`), necesidad de *Sponsor Proof* y trofeos LED.
2. **Academias de Danza, Colegios Privados y Kinders (SPGG):** Galas y admisiones bajo modelo *White-Glove* (preventa voluntaria de marcos `$1,200–$1,500 MXN` por familia; 10–12 familias cubren el 100% del evento a costo `$0` para la institución).
3. **Gimnasios, CrossFit, Hyrox, Clínicas y Negocios Boutique (Small Business 2027):** Optimización de Google Maps, Reels `9:16`, Meta Business Portfolio unificado y placa QR LED para reseñas de 5 estrellas.
4. **Básquetbol Profesional y Deporte Colegial/Juvenil (MTY y CDMX):** Capitanes CDMX / G League, LNBP, Borregos Tec, Tigres UANL, MFL (paquetes de juego único `$6,500–$9,500 MXN`, series `$12,000–$16,000 MXN`, Sponsor Proof `$8,500–$14,000 MXN` y residencias `$25,000–$45,000 MXN/mes`).

### Paquetes Estacionales y Small Business (-35%)
- **Clubes y Academias:** Solo Digital `$3,185 MXN` · Foto + Marcos/Impresión `$5,135 MXN` · Suite Full + 4 Trofeos LED + 20 Llaveros `$7,475 MXN` (y paquete torneo patrocinado llave en mano `$12,500 MXN`).
- **Small Business 2027:** Impulso Google Maps `$3,900 MXN` · Suite Total `$6,890 MXN` · Posicionamiento + Placa QR LED `$10,400 MXN`.
- **Captoora Biogen (Beta):** Seguimiento físico escultórico en estudio desde `$1,268 MXN/mes` (3 meses) hasta `$748 MXN/mes` (60 meses).

---

## 5. Bloque "Business DNA" listo para copiar en Google Pomelli

- **Brand Name:** Captoora Sports (`captoora.studio`)
- **Industry / Category:** Elite Sports & Commercial Visual Engineering Studio (Monterrey & San Pedro Garza García, Mexico)
- **Website:** `https://captoora.studio/sports`
- **Primary Colors:** `#060509` (Obsidian Black), `#f7f4ef` (Bone White), `#d4af37` / `#c9a23f` (Championship Gold), `#CCFF00` / `#c6ff00` (Athletic Volt), `#00f0ff` (Telemetry Cyan)
- **Fonts:** `Cinzel` (Display), `Cormorant Garamond` (Editorial), `Plus Jakarta Sans` (Body), `JetBrains Mono` (Technical)
- **Brand Voice:** Authoritative, luxury-editorial, high-energy athletic precision, warm Mexican Spanish (`es-MX`), zero mention of "AI", never use the word "presumir".
- **Core Hook:** `1/2000s` Global Shutter freeze-action + same-day 3D gallery delivery + illuminated LED optical acrylic trophies & Google Maps visual transformation.
