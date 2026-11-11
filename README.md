# Capitanes CDMX & Men's Basketball Intelligence Hub 🏀📸

> Repositorio de inteligencia deportiva, prospección comercial, alianzas de agencias y planeación de cobertura fotográfica en duela para **Capitanes de la Ciudad de México** (NBA G League) y el ecosistema de **básquetbol varonil** (México y EE.UU.).

---

## 📌 Visión del Proyecto y Metas de Colaboración

Este repositorio está diseñado para operar de forma colaborativa entre **agentes de IA y colaboradores humanos** dentro de tu entorno de GitHub, con el objetivo de:
1. **Lograr acreditaciones y contratos de fotografía de duela (*courtside*)** con Capitanes de la Ciudad de México en la Arena CDMX.
2. **Infiltrarse a través de las agencias colaboradoras** (como **Imago7**, **Zignia Live** o agencias BTL de patrocinadores) para realizar **prácticas profesionales, shadowing o asistencia técnica** a ras de cancha.
3. **Mapear puertas alternativas de básquetbol varonil**: Si Capitanes tiene cupos llenos, tener identificados los equipos varoniles con acceso inmediato para practicar (Diablos Rojos Basquetbol Varonil, Ángeles CDMX Varonil en CIBACOPA, y la Liga Universitaria ABE Varonil).
4. **Anticiparse al calendario**: Monitorear fechas límites de solicitud (T - 5 días) y saber con quién dirigirse con nombre, apellido y correo verificado.

---

## ⚡ Dashboard Interactivo de Operaciones

El proyecto incluye un **Dashboard Web interactivo** moderno y responsivo, listo para ser visualizado en cualquier navegador:

📍 **Ruta del Dashboard:** [`dashboard/index.html`](file:///Users/imac/Documents/antigravity/epic-bohr/dashboard/index.html)

### Módulos del Dashboard:
* **📅 Agenda de Partidos & Ventanas de Anticipación:** Listado completo de juegos de Capitanes CDMX en la NBA G League (Tip-Off Tournament y Temporada Regular), diferenciando partidos locales en la Arena CDMX vs visitas en EE.UU., con fecha límite de anticipación de acreditación y contactos asignados.
* **🤝 Agencias con las que Colaboran & Prácticas:** Fichas de Imago7, Getty Images / NBA Photos, Zignia Live (Arena CDMX) y agencias BTL de patrocinadores (ADO, Caliente.mx), con teléfonos directos, canales de contacto y guiones de prácticas/shadowing.
* **🏀 Equipos Rivales y Alternativos (Solo Hombres):**
  * *Rivales de la G League que visitan la Arena CDMX* (Austin Spurs, Texas Legends, RGV Vipers, Birmingham Squadron, Osceola Magic, South Bay Lakers) que contratan stringers locales.
  * *Equipos Profesionales Varoniles en CDMX* (Diablos Rojos del México Basquetbol en LNBP y Ángeles CDMX en CIBACOPA, ambos en el Gimnasio Juan de la Barrera).
  * *Liga ABE División 1 Varonil* (Borregos Tec de Monterrey CCM y Pumas UNAM en CU) para práctica técnica inmediata sin trabas burocráticas.
* **📇 Directorio & Decisores de Presupuesto:** Contactos verificados del Front Office (Carlos Tostado, Orlando Méndez, Nuño Pérez-Pla, Daniela Rivero, Área de Comunicación y Área de Alianzas).
* **🚀 Pipeline de Agentes:** Registro de seguimiento de misiones de prospección.
* **✅ Checklist Pre-Partido:** Cronograma de verificación técnica y operativa (T-5 días, T-24h, Día de Juego en Arena CDMX y Post-Partido).

---

## 📂 Estructura del Repositorio

```text
.
├── README.md                                  # Visión general y guía del repositorio
├── dashboard/
│   ├── index.html                             # Dashboard interactivo para navegador
│   └── data/
│       ├── schedule.json                      # Calendario oficial de juegos y deadlines
│       ├── agencies.json                      # Agencias, contactos y vías de prácticas
│       ├── alternative_teams.json             # Rivales y alternativas varoniles exclusivas
│       ├── contacts.json                      # Directorio de decisores y directivos
│       └── outreach.json                      # Pipeline y bitácora de prospección
├── docs/
│   ├── agencias_y_practicas.md                # Investigación a fondo de Imago7, Zignia y Getty
│   ├── equipos_alternativos_y_rivales_varonil.md # Mapeo de básquetbol varonil (G League, LNBP, ABE)
│   ├── guia_agentes.md                        # Protocolo operativo para agentes de IA
│   └── manual_tecnico_courtside.md            # Parámetros técnicos de cámara y normas NBA
└── templates/
    ├── solicitud_practicas_imago7.md          # Carta formal para pedir prácticas a Imago7
    ├── solicitud_acreditacion_capitanes.md    # Plantilla de Media Pass para Capitanes CDMX
    └── propuesta_equipos_visitantes_gleague.md # Script para rivales de la G League en CDMX
```

---

## 🤖 Protocolo para Agentes de IA en GitHub

Si eres un agente de IA que interactúa con este repositorio:
1. **Regla de Alcance:** Todo el contenido debe permanecer **estrictamente enfocado en Básquetbol Varonil (Men's Basketball)**.
2. **Actualización de Datos:** Al realizar una nueva gestión o descubrir un nuevo contacto o fecha, actualiza los archivos JSON en `dashboard/data/` y el archivo `docs/guia_agentes.md`.
3. **Ventana de Anticipación:** El gatillo de contacto para partidos locales debe activarse con **mínimo 5 días hábiles de anticipación** (`anticipation_deadline` en `schedule.json`).
