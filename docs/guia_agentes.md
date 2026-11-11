# Guía Operativa para Agentes de IA (Multi-Agent Protocol)

Este repositorio está preparado para que **múltiples agentes de IA** y colaboradores humanos puedan cooperar de manera autónoma o asistida para lograr alianzas comerciales, acreditaciones de prensa y prácticas fotográficas con **Capitanes CDMX** y el ecosistema de **Básquetbol Varonil** en México y EE.UU.

---

## 1. Estructura de Datos del Proyecto

Los agentes deben leer y actualizar los archivos ubicados en `dashboard/data/`:

| Archivo | Propósito | Reglas de Actualización para Agentes |
| :--- | :--- | :--- |
| `schedule.json` | Calendario oficial de partidos varoniles y plazos de anticipación. | Verificar fechas, sedes, estados y alertas de vencimiento de acreditación (T-5 días). |
| `agencies.json` | Directorio de agencias (Imago7, Zignia, Getty, Patrocinadores). | Agregar nuevos contactos, fotógrafos identificados o notas de llamadas. |
| `alternative_teams.json` | Equipos varoniles alternativos (G League visitantes, Diablos, Ángeles, Liga ABE). | **Estricto: Mantener únicamente equipos y competencias varoniles (Men's Hoops).** |
| `contacts.json` | Directorio de directivos y decisores de presupuesto. | Registrar nuevos correos, números de WhatsApp y perfiles de LinkedIn. |
| `outreach.json` | Pipeline de prospección y estado de misiones. | Cambiar estados de `Ready to Contact` a `In Contact`, `Follow-up` o `Approved`. |

---

## 2. Roles Sugeridos para Agentes

1. **Scouting & Intelligence Agent:**
   * Monitorea anuncios oficiales en [capitanes.mx](https://capitanes.mx/) y [gleague.nba.com](https://gleague.nba.com/).
   * Detecta cambios de horario o partidos reprogramados en la Arena CDMX.
   * Identifica los jugadores asignados de la NBA (Two-Way contracts) del equipo rival que visitará la CDMX.
2. **Outreach & Communication Agent:**
   * Redacta y personaliza las propuestas de acreditación o cartas de solicitud de prácticas profesionales para Imago7 o Capitanes.
   * Actualiza `dashboard/data/outreach.json` con la bitácora de mensajes enviados.
3. **Field & Operations Agent:**
   * Gestiona el Checklist Pre-Partido (T-5 días, T-24h, Día de Juego).
   * Prepara los metadatos IPTC y las especificaciones de entrega de fotos.

---

## 3. Protocolo de Anticipación (Alerta T - 5 Días)

Cuando la fecha del sistema (`current_time`) esté a **5 días hábiles** de un partido de local en la Arena CDMX:
1. El agente debe emitir una alerta prioritaria en la bitácora de prospección.
2. Ejecutar la acción de contacto con `comunicacion@capitanes.mx` adjuntando la carta de acreditación estandarizada en `templates/solicitud_acreditacion_capitanes.md`.
3. Notificar al usuario para dar seguimiento directo a través de los canales de WhatsApp o teléfono de la agencia asignada.
