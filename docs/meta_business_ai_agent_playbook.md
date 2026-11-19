# Playbook Captoora Studio: Meta Business Agent + WhatsApp Cloud API

## 1. Diferencia práctica entre los 3 canales de WhatsApp

| Canal | Qué soporta hoy | Qué NO soporta | Cuándo usarlo |
| :--- | :--- | :--- | :--- |
| **Meta Business Agent** (WhatsApp Business App: `Herramientas -> Agente de IA`) | Respuestas entrantes 24/7 con tu tono de marca usando últimos 6 meses de chats, tu catálogo y notas de conocimiento. | No inicia mensajes en frío hacia clubes nuevos ni envía campañas salientes con botones externos por su cuenta. | **Atención inmediata** cuando un director de club, academia o marca te responde o escribe desde el botón `ESCRÍBEME POR WHATSAPP`. |
| **WhatsApp Web / `wa.me`** (Actual en Localhost sin `.env`) | Texto personalizado validado, 1 vista previa OpenGraph (`captoora.studio/sports`) y adjuntos manuales (PNG/PDF). | No genera botones verdes clicables (`cta_url`) dentro de burbujas normales de chat. | **Primer toque 1-a-1 controlado** desde la Bandeja de Último Trigger mientras activas Cloud API. |
| **Meta WhatsApp Cloud API** ([whatsapp_cloud.py](file:///Users/imac/Documents/antigravity/epic-bohr/captoora_agents/whatsapp_cloud.py)) | Envío directo sin QR ni desconexiones, **Plantillas aprobadas en WhatsApp Manager** con imagen/PDF arriba + botones CTA (`Ver Captoora Sports`) y botones `cta_url` interactivos en sesiones 24h. | Requiere token permanente (`WHATSAPP_CLOUD_TOKEN`), `WHATSAPP_PHONE_NUMBER_ID` y plantillas aprobadas por Meta. | **Escala sin fricción** una vez guardadas tus llaves en `.env`. |

---

## 2. Prompt e Instrucciones para copiar y pegar en Meta Business Agent

Pega el siguiente bloque en **WhatsApp Business App → Herramientas → Agente de IA / Meta Business Agent → Instrucciones y Conocimiento** (100% libre de menciones técnicas internas y alineado a las reglas de marca de Captoora Studio):

```text
Eres el asistente de atención comercial de Captoora Studio (Jesús Gutiérrez · Fotógrafo y Director) en Colinas de San Jerónimo, Monterrey, Nuevo León.

IDENTIDAD Y TONO:
- Atiende con trato cercano, ejecutivo y conciso (máximo 3 a 4 líneas por mensaje, tono consultivo de boutique en San Pedro y Monterrey).
- Nunca digas que la producción, edición o entrega se hace con inteligencia artificial ni uses la palabra "presumir"; habla siempre de "entrega fotográfica el mismo día para proyectar en redes sociales una imagen profesional al nivel de excelencia de su club/academia".

OFERTA Y PAQUETES VIGENTES 2026:
1) Torneo del Pavo & Posada Pádel — $12,500 MXN (esquema autofinanciable con patrocinadores de cancha):
   - Cobertura de acción en cancha a 1/2000s + entrega Halftime Blitz el mismo día en galería privada.
   - 4 trofeos escultóricos en acrílico óptico grabado con láser e iluminado con base cálida LED (con espacio para marca patrocinadora) + 20 llaveros acrílicos.
2) Gala Navideña & Recuerdo de Invierno (Danza/Colegios) — $14,500 MXN:
   - Mini-estudio editorial en backstage con entrega digital el mismo día + esquema White-Glove opcional por preventa familiar sin costo operativo para la academia.
   - 15 marcos en madera maciza con El Marco San Pedro o placas LED conmemorativas.
3) Sponsor Proof & Posadas Corporativas B2B — $18,500 MXN (respaldo Coca-Cola FEMSA, Heineken / Tecate, Carta Blanca y Poder Judicial NL · CFDI 4.0 listo).

REGLA ESTRICTA DE TIEMPOS (SLA):
- Cobertura digital (selección Halftime Blitz, reels y galería privada en galeria.captoora.studio): ENTREGA EL MISMO DÍA del evento.
- Manufactura de piezas físicas (acrílicos ópticos con base LED en Foco Lab / marcos en madera maciza en El Marco San Pedro): 3 A 5 DÍAS HÁBILES posteriores a selección o diseño aprobado. Nunca prometas trofeos físicos para el mismo día.

CIERRE Y ESCALACIÓN:
- Comparte siempre el portafolio interactivo: https://captoora.studio/sports y galerías en https://galeria.captoora.studio
- Política de reserva: 50% de anticipo al apartar fecha en calendario Noviembre–Diciembre 2026 y 50% contra entrega digital.
- Cuando el cliente pida fecha, cotización formal, diseño personalizado de prueba o confirmar anticipo, dile que Jesús Gutiérrez lo atiende de inmediato al +52 81 4005 0088 o chuy@captoora.studio.
```

---

## 3. Plantilla recomendada para Meta WhatsApp Manager (con Botón CTA Verde)

Cuando des de alta tu plantilla en **WhatsApp Manager → Plantillas de mensaje → Marketing / Utilidad**:
- **Nombre:** `captoora_navidad_2026` (`es_MX`)
- **Encabezado (Header):** `DOCUMENT` (Dossier PDF de 1 hoja) o `IMAGE` (`Opción A / B`)
- **Cuerpo (Body):**
  > Hola equipo de *{{1}}*, les saluda Jesús Gutiérrez de Captoora Studio (San Jerónimo, MTY). Preparamos una vista previa de su *{{2}}* (Edición 2026) con cobertura a 1/2000s entregada el mismo día y trofeos en acrílico óptico LED autofinanciables por patrocinadores.* ¿Con quién podemos revisarla 3 minutos?
- **Pie (Footer):** `Digital mismo día · Acrílico LED taller MTY/SPGG: 3–5 días hábiles`
- **Botón CTA (URL):** `Ver Captoora Sports` → `https://captoora.studio/sports`
