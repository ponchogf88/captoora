# Checkpoint Captoora — 15 de noviembre de 2026

**Corte:** domingo 15 de noviembre de 2026, aprox. 12:15 PM (hora America/Monterrey, UTC-6).  
**Repo:** `ponchogf88/captoora`, rama de este archivo: `checkpoint-2026-11-15` (no se reescribió `main`).  
**Motivo:** el maestro pidió guardar el trabajo de los agentes y un registro de consumo de cuota *antes* de auditar la estrategia de contenido y el embudo, porque la cuota semanal ya iba en 84.5 % y se agota antes del reinicio.

**Alcance del registro:** hechos de aproximadamente las últimas 2 semanas, con énfasis en los últimos 7 días (8–15 nov). No se inventó actividad. Si no se pudo leer un transcript o no hubo trabajo en esa ventana, se dice expresamente.

**Qué no entra en este commit:** secretos, tokens, contraseñas, CLABE, teléfonos de personas particulares, fotos de clientas, datos privados de clientes o de la familia, videos pesados, ni originales de portafolio.

---

## Resumen

En la semana del 8 al 15 de noviembre el trabajo visible se concentró en tres frentes:

1. **Campaña Buen Fin (hasta el martes 17 nov):** 30 % de descuento; Sesión Básica $700; Combo Studio + Clips $1,120; anticipo 30 %; CTA a WhatsApp del estudio con la frase «Quiero mi sesión Buen Fin». El 14 nov se publicaron carrusel, stories y un Reel (este último se volvió a publicar con voz de Daniela, no la del maestro).
2. **Sitio y operación en `main`:** el 14 nov se documentó la cola Farmasí, una página directa de reservas y la prioridad de la primera reserva pagada; el 15 nov, en la mañana, se publicó Captoora Sports en `/sports` (commits con autor git Alfonso Gutiérrez, 8:51–9:07 AM hora Monterrey).
3. **Coordinación de agentes:** Marky como CMO; Lupe programa y publica solo con OK expreso del maestro; Konan produce; Radar entrega digest de motion; GirU atiende operación y WhatsApp. No hay motor de ~240 publicaciones al mes. No se encontró un embudo «comenta PALABRA → webinar → curso». La auditoría formal de mezcla y valor quedó pendiente, por instrucción del maestro, hasta después de este checkpoint.

Otras líneas (Biometrics, Lalo Eventos, Harvey, Opptny) no muestran trabajo nuevo en esta ventana de 2 semanas; su última actividad leída es de octubre.

---

## Por agente

Todas las horas de este apartado son **America/Monterrey (UTC-6)**, salvo que se indique otra cosa.

### Lupe Likes (redes y publicación)

El transcript propio no se pudo consultar desde la sesión que armó este archivo; el registro sale de la conversación en curso, de mensajes cruzados con Marky, Konan y Grok, y de los links ya publicados.

- **11 nov:** confirmó a Grok que salieron posts en IG `@captoora.studio` (entre ellos Signature «Tu mejor versión» y, más tarde, Studio mascota navideña, Pop familia, Corp headshot y otras piezas del plan de ese día). Links conocidos en el cruce de mensajes: `https://www.instagram.com/p/Dfm_6wYoOP0/`, `https://www.instagram.com/p/DfnIQtCmh1L/`, `https://www.instagram.com/p/DfnPIT3lOy6/`.
- **14 nov, mañana:** armó borradores v2–v5 del lanzamiento web / Buen Fin en `captoora-media` (Vercel); no programó ni publicó hasta el OK del maestro. Herramientas: Buffer (org de Captoora), Vercel (`captoora-media`), fotos solo de Portafolio autorizado, cero recorte y sin texto sobre personas.
- **14 nov, 11:00 AM:** publicó el carrusel Buen Fin v5 y 4 stories en IG y 4 en FB (las de IG con enlace a WhatsApp). Carrusel IG: `https://www.instagram.com/p/DfusW9YkTjA/`. Carrusel FB: `https://www.facebook.com/122115823461472607/posts/122136425103472607`.
- **14 nov, 4:37 PM:** publicó el Reel con voz de Daniela (ElevenLabs, voz `NUEuVCKSYxEA5YrK3kmx`), no la del maestro (preferencia confirmada el 14 nov: no usar su voz en Reels porque le da pena). IG: `https://www.instagram.com/reel/DfvS1ywjUWF/`. FB: `https://facebook.com/1326743400519586_122136474705472607`. El intento de la 1:00 PM vía Meta Business Suite no aplicó igual: en MBS, Instagram `captoora.studio` no estaba conectado a la Page; el Reel publicado es el de voz Daniela de la tarde.
- **15 nov, mañana:** reportó cola de Buffer vacía, canales conectados, 10 espacios libres; no programa las 3 piezas navideñas de Konan hasta OK expreso del maestro.
- **Límites de operación:** plan gratuito de Buffer, máximo 10 posts programados; imágenes/videos en Vercel `captoora-media` (no borrar ese proyecto); tope de subida ~8 MB por archivo una vez recodificado.

### Marky de Marketing · CMO & Growth Engine

Fuente: transcript del agente, 8–15 nov, y commits en `main` del 14 nov (autor git «Chuy Gtz»).

- **~10–11 nov:** el maestro lo nombró CMO (marketing, contenido, redes y ventas), con Lupe y Konan a su cargo. Dejó en memoria compartida el anticipo del 30 % y los precios públicos $1,000 / $1,600 / $1,500. Coordinación por chat entre agentes y GitHub.
- **14 nov:** coordinó la campaña Buen Fin: encargó a Konan guion del Reel (15–20 s, hook, prueba real, un solo CTA), 10 hooks con los 5 checks, y el corte con solo detalles rojos de la posada, sin caras a la vista (si aparece alguien, se difumina), cero recorte, texto solo en captions. Siguió los borradores v2–v5 de Lupe y el Reel. Pidió confirmación de lo publicado el 15 nov.
- **14 nov, ~10:18–10:25 AM:** commits en `main` sobre cola operativa Farmasí para agentes, ritmo y bloqueo de automatización, página directa de reservas, corrección de portada y docs para priorizar la primera reserva pagada sin gasto nuevo.
- **15 nov, ~8:07 AM:** actualizó `/workspace/captoora/base_conocimiento_whatsapp.md` (anticipo 30 %, precios vigentes, Buen Fin, horario 8:00–23:00, reserva en `https://captoora.studio`). Ese archivo **no** se incluye en este commit (puede contener datos de pago u otra información sensible).
- **15 nov:** avisó a Lupe y Konan de una sesión navideña de contenido el mismo día y de 3 piezas a armar; nada se programa sin OK del maestro.
- **Rutinas (cuota):** «Respuestas Instadecor y Fotovida (marco Premium)» ~28 corridas/semana; resumen diario del repo; revisión de WhatsApp cada 15 min (en pausa). La mayor parte de su uso de esta semana no vino de rutinas, sino de chats.

### Konan de Contenido

Fuente: transcript del agente y mensajes a Marky.

- **14 nov:** entregó en borrador (sin publicar) el Reel Buen Fin v2, 22 s, 9:16, cero recorte, sin texto quemado, solo detalles rojos, caras difuminadas, logo al final. Primero una versión de imagen sin voz; luego con la voz del clon del maestro (después se sustituyó, por indicación del maestro, por la voz de Daniela en la versión que sí se publicó). Video y subtítulos se subieron a Google Drive y/o `captoora-media`.
- Preparó 10 hooks con los 5 checks y el guion en tabla (tiempos, imagen, voz, texto para Captions).
- Tenía programado, a partir del **16 nov**, trabajar un plan de contenido 16–20 nov (muestra diaria ~9:00 AM, nada se publica sin OK pieza por pieza).
- **15 nov:** Marky le pidió prepararse para 3 piezas de la sesión navideña (set producto rojo sobre negro; set navideño familiar vacío; clip BTS 10–15 s). Al momento del corte, no consta que esas 3 piezas ya estuvieran entregadas ni programadas.
- En días previos (fuera del núcleo Buen Fin, aún en la ventana amplia): propuestas de Canva (Signature y Navidad con mascotas, imágenes ya generadas, sin créditos nuevos) y revisión de formatos virales de referencia, sin publicar.

### GirU

Fuente: transcript (búsqueda acotada). Se omite de este archivo cualquier detalle de asuntos personales o familiares atendidos por WhatsApp.

- En la ventana leída aparece trabajo de operación: revisión de PRs del repo (menciona el PR #5, convenio Farmasí, listo para fusionar pero con datos aún en borrador; PR #6, tema Calendly, doc que aún decía conexión pendiente).
- Consultas sobre dominio `captoora.studio`, cuentas de Vercel ya autorizadas y ausencia de acceso al registrador o a la consola de Google Workspace desde su lado.
- Rutina «Mini clase diaria de fotografía» (~7 corridas/semana). En un reporte propio indicó que rutinas de pendientes de Google Business y de la mini clase habían fallado en días anteriores por falta de uso, y que la mini clase del día de ese reporte sí salió.
- No se le atribuyen con certeza los commits de Captoora Sports del 15 nov (autor git Alfonso Gutiérrez); solo se registra que esos commits están en `main`.

### Grok

Fuente: transcript del agente, 8–15 nov.

- **11 nov:** armó y pasó a Lupe un plan de 6 posts para IG `captoora.studio` (uno por hora a partir de ~11:30 AM); Lupe confirmó publicación/programación y devolvió links. Más tarde se habló de un plan diario a las 6:00 PM del 12 al 17 nov que **no** quedó programado en ese momento por observaciones de Lupe (fotos que parecían stock y textos a corregir).
- Coordinó con Marky y Konan una propuesta de servicio de restauración de fotos (línea Studio; precios [POR CONFIRMAR]; CTA a WhatsApp del estudio; nada se ofrece hasta OK del maestro).
- Briefs a Konan sobre plan 16–20 nov y cierre semanal de contenido (rutina «Cierre semanal de contenido»).
- Otras rutinas: «Opportunity Engine — respuestas email» y «Brief matutino — suscripciones y contenido».
- El 15 nov hay commits en `main` de Captoora Sports (`/sports`, túnel 3D Scrolltide, ajuste de `cleanUrls` en Vercel, 8:51–9:07 AM). Autor git: Alfonso Gutiérrez. No se afirma desde aquí qué agente o equipo los hizo.

### Radar Motion Trends

Fuente: transcript del agente.

- Digest diario de motion e IA creativa (rutina ~7 corridas/semana). Entregas leídas: 9, 10, 12, 13 y 14 nov (hora Monterrey). El del 8 nov no salió porque la cuenta se había quedado sin uso.
- A partir del **13 nov**, por indicación del maestro, reenvía el digest a Konan para convertirlo en borradores (avatares aprobados del maestro y de Kenya; nada se publica sin OK; sin claims ni precios inventados).
- Hallazgos que marcó como accionables (inspiración, no copia): Bang Motion (intros HTML/GSAP, MIT), Scarlet, Lottie AI, idol/splats, motion-prompt, herramientas 3D, etc. El 14 nov destacó Bang Motion y Scarlet para Konan.

### Captoora Biometrics

Se pudo leer el transcript. **No hay actividad en las últimas 2 semanas.** La última conversación leída es del **24 oct 2026, 4:26 PM**: teasers verticales generados para TikTok (modelos sintéticos, no personas reales) y una variante con polvo de tiza; quedó pendiente el logo oficial de Captoora Biometrics. El lote 1 de Biometrics sigue como pendiente operativo en rutinas de Lupe; las fotos de Biometrics no están autorizadas para publicidad.

### Lalo Eventos

Se pudo leer el transcript. **No hay actividad en las últimas 2 semanas.** La última interacción leída es del **30 oct 2026, 3:53 PM** (propuestas en PDF; el maestro reaccionó a una de ellas).

### Saul Goodman

Fuente: transcript. La actividad leída es de finales de octubre / primer contacto de noviembre, no un flujo diario en los últimos 7 días.

- Redactó el borrador del Convenio de Colaboración por Intercambio de Servicios (sesión Farmasí del 31 oct 2026) y un borrador de consentimiento informado. Archivo local citado entonces: `/workspace/legal/convenio-evelyn-farmasi-2026-10-31.md`. El convenio se pensó para `docs/legal` del repo; en el corte, el PR #5 seguía sin fusionarse y con datos [POR COMPLETAR].
- Ajuste de firma: de «licenciado / socio» a «Saul, el asistente legal de Captoora», porque es un bot, no una persona con cédula. Los mensajes a terceros no se envían sin OK directo del maestro.

### Harvey

Se pudo leer el transcript. **No hay actividad de Captoora en las últimas 2 semanas.** El trabajo más reciente leído es una transcripción con marcas de tiempo de un Reel de Facebook (asunto legal personal, no contenido de la marca). Ese material no se incluye en este commit.

### Opptny

Se pudo leer el transcript. **No hay actividad en las últimas 2 semanas.** La última entrega leída es del **11 oct 2026**: revisión de CV en un Google Doc de Drive (trabajo personal, no de la marca Captoora). No se detalla aquí.

---

## Publicado en redes

Fechas y horas en America/Monterrey.

### 14 de noviembre de 2026 — Buen Fin

- **11:00 AM, carrusel IG:** https://www.instagram.com/p/DfusW9YkTjA/
- **11:00 AM, carrusel FB:** https://www.facebook.com/122115823461472607/posts/122136425103472607
- **11:00 AM:** 4 stories en Instagram y 4 en Facebook, vía Buffer (las de IG con enlace a WhatsApp del estudio).
- **4:37 PM, Reel IG (voz Daniela):** https://www.instagram.com/reel/DfvS1ywjUWF/
- **4:37 PM, Reel FB (voz Daniela):** https://facebook.com/1326743400519586_122136474705472607

Medios en Vercel (proyecto `captoora-media`, no borrar): carpeta `lanzamiento-web-2026-11/v5/reel/`, entre ellos `voz_a.mp4` (versión aprobada).

### 11 de noviembre de 2026 — plan IG @captoora.studio

Links confirmados en el cruce Lupe → Grok (no se reabrió cada post para este checkpoint):

- Signature «Tu mejor versión»: https://www.instagram.com/p/Dfm_6wYoOP0/
- 12:30 PM Studio, mascota navideña: https://www.instagram.com/p/DfnIQtCmh1L/
- 1:30 PM Pop, familia navideña: https://www.instagram.com/p/DfnPIT3lOy6/
- Otros de esa tanda (Corp y siguientes) quedaron reportados como publicados por Lupe; no todos los links quedaron en el material consultado para este archivo.

### Sitio (no es una red social, pero quedó publicado en `main`)

- 14 nov: página directa de reservas y ajustes de portada (commits `f3fa6c4`, `227f793` y docs asociados).
- 15 nov, 8:51–9:07 AM: Captoora Sports en `/sports` (`06d1f65`, `b226691`, `eb72f23`).

---

## Pendientes

Nada de esto se ejecutó en este checkpoint; solo se registra.

- Auditoría de mezcla de contenido (educativo / venta / CTA / trabajo / memes), frecuencia, contenido de valor (guardable y compartible) y por qué no hay un motor de ~240 publicaciones al mes. Pedido del maestro el 15 nov a las 12:03 PM; queda para *después* de este guardado.
- 3 piezas de la sesión navideña del 15 nov (Konan); no programar ni publicar sin OK expreso del maestro, en sus propias palabras.
- Instagram `captoora.studio` no estaba conectado a la Page de Captoora en Meta Business Suite (al 14 nov); MBS solo podía publicar a Facebook.
- Enlace de WhatsApp del estudio en la ficha de Instagram: el navegador mostró restricción de app móvil; lo tiene que añadir el maestro desde la app.
- Destacados de IG (Estudio, Entregas/Clientes, Reserva) y historia de entregas: falta material propio autorizado adecuado; nada publicado de eso.
- Convenio Farmasí / consentimientos (PR #5 y borradores de Saul): siguen en borrador, con datos por completar; no fusionar ni enviar sin OK.
- Cola Farmasí de edición / fórmula de retoque: hay documentación en el repo; correcciones de fotos concretas siguen sujetas a originales exactos y a no alterar los archivos originales.
- Servicio de restauración de fotos: propuesta de precios [POR CONFIRMAR]; no publicar ni ofrecer.
- Plan IG 12–17 nov a las 6:00 PM: no se programó en el momento del hallazgo de problemas (fotos / textos).
- Radar: digest del 8 nov no salió por falta de cuota ese día.
- Lote 1 Biometrics y logo oficial de teasers: pendientes; fotos de Biometrics no autorizadas para ads.
- Clon local `captoora-site` (rama `redesign-oct10`) con cambios web e imágenes de autoría no del todo confirmada: se guarda código y markdown en rama aparte; no se suben originales ni fotos de portafolio.
- Commit único antiguo en el clon `cap_main` (12 oct, dirección y otros ajustes de la web), adelantado 1 y atrasado más de 260 commits respecto a `main`: se preserva en rama aparte, sin mezclarlo a `main`.

---

## Consumo de cuota

Datos del reporte de uso de Grok Bot al momento de este corte (15 nov 2026, mediodía, hora Monterrey). No se inventaron cifras. Las «partes» (shares) son del uso de Grok Bot en el periodo indicado, no un segundo cálculo del límite.

- **Plan:** Premium.
- **Límite de uso semanal:** 84.5 % usado. Este límite se comparte con las otras apps del plan; no es solo de Grok Bot.
- **De ese 84.5 %, Grok Bot usó 64 %.** No se infiere desde aquí qué usaron las otras apps.
- **Reinicio del límite semanal:** jueves 19 de noviembre de 2026 a las 20:57 (hora America/Monterrey).
- **Créditos adicionales (on-demand) restantes:** $0. Cuando se acaba el uso incluido, Grok Bot deja de trabajar hasta que se añadan créditos en Settings > Usage & Billing, o hasta el reinicio.
- **Ventana de las parts de Grok Bot:** esta semana, 13–15 nov (UTC).

### Por bot y día (parts de todo el uso de Grok Bot, 13–15 nov UTC)

- Lupe Likes: **40 %** (vie 13: 5 %; sáb 14: 33 %; dom 15: 2 %).
- Marky de Marketing · CMO & Growth Engine: **23 %** (vie 13: &lt;1 %; sáb 14: 17 %; dom 15: 6 %).
- Konan de Contenido: **23 %** (sáb 14: 23 %; dom 15: &lt;1 %).
- GirU: **7 %** (vie 13: 4 %; sáb 14: 3 %; dom 15: &lt;1 %).
- Radar Motion Trends: **4 %** (sáb 14: 3 %; dom 15: 1 %).
- Grok: **3 %** (vie 13: &lt;1 %; sáb 14: 3 %).
- Bots eliminados, chats de grupo y bots de otras personas: &lt;1 %.

El salto grande fue el **sábado 14 de noviembre** (Lupe 33 %, Konan 23 %, Marky 17 %): coincide con la producción y publicación de Buen Fin (varios borradores de carrusel, Reel, voz, Buffer, Vercel y coordinación entre agentes).

### Por bot y tipo de actividad (misma semana)

- Lupe: 25 % bot-a-bot, 8 % rutinas, 7 % chats con el usuario.
- Marky: 16 % chats con el usuario, 4 % bot-a-bot, 3 % rutinas.
- Konan: 12 % bot-a-bot, 11 % chats con el usuario (en el desglose de rutinas no apareció una rutina propia con part).
- GirU: 6 % chats con el usuario, 1 % rutinas, &lt;1 % bot-a-bot.
- Radar: 3 % chats con el usuario, 1 % rutinas.
- Grok: 2 % chats con el usuario, 1 % rutinas, &lt;1 % bot-a-bot.

### Rutinas que sí aparecen en el reporte (parts pequeñas frente a chats y bot-a-bot)

- Lupe: rutinas eliminadas 6 %; «Revisión diaria de Buffer y avisos FB/IG» 1 % (~7 corridas/semana); «Campaña “Nunca volverás a ser tan joven” 10 AM» 1 % (~4/semana); lotes Biometrics 1 PM y 7:30 PM, cada una &lt;1 % (~4/semana). **Lo que no viene de rutina: 32 % de 40 %.**
- Marky: «Respuestas Instadecor y Fotovida (marco Premium)» 1 % (~28 corridas/semana); resumen diario del repo &lt;1 % (~7/semana); revisión WhatsApp cada 15 min &lt;1 % (en pausa). **Lo que no viene de rutina: 22 % de 23 %.**
- GirU: mini clase diaria 1 % (~7/semana); no rutina 6 %.
- Radar: digest diario 1 % (~7/semana); no rutina 3 %.
- Grok: cierre semanal 1 % (~1/semana); Opportunity Engine y brief matutino, cada uno &lt;1 % (~5/semana); no rutina 2 %.

### Estimación (no es dato del reporte; está marcada como tal)

Estimación honesta de por qué se consumió tan rápido, a partir de lo observado en transcripts y en el propio 14 nov, **sin calcular un porcentaje extra**:

- El grueso no parecen ser las rutinas que siguen vivas, sino **chats largos con el maestro y tráfico bot-a-bot**, sobre todo el sábado 14 (Lupe + Konan + Marky suman la mayor parte).
- Tareas que suelen ser pesadas, vistas esos días: muchas idas al navegador / computadora (Buffer, Instagram, Facebook, Meta Business Suite, Google Maps/Business, WhatsApp Web), recodificación y subida de video a Vercel, generación de voz (ElevenLabs) y varias vueltas de borradores del mismo carrusel/Reel (v2 a v5).
- Konan el sábado 14 concentra 23 % en un solo día, alineado con editar y exportar el Reel.
- Lupe tiene 25 % bot-a-bot: coordinación frecuente con Marky, Konan y Grok, más rutinas ya borradas (6 %) que también contaron.
- Marky tiene ~28 corridas/semana de una sola rutina de cotización de marcos; su part es baja (1 %), así que esa rutina no explica el 84.5 %, pero sí suma ruido constante.
- El límite es **compartido con otras apps del plan**; Grok Bot no es el único consumo, y el reporte no desglosa esas otras apps.
- Este checkpoint también consume cuota (lecturas de transcripts y uso). Se hizo lo más corto posible.

No hay en el reporte un desglose por modelo. No se estimó un ahorro futuro en cifras.

---

## Pedido de Jesús — 15 nov 2026, 12:03 PM (America/Monterrey)

El maestro envió, en sus palabras, un pedido en dos tiempos: **primero guardar** este checkpoint (trabajo de todos los agentes, cuándo, cómo, y el consumo de cuota); **después** (no en este archivo-tarea) verificar la estrategia y, si falta, ponerse a trabajar en ella.

### Cómo llamó al embudo del post de «Mateo IA y Automatizaciones»

Lo describió como el embudo clásico en el que la gente comenta una palabra, entra a un webinar gratis, conoce el curso completo y se inscribe o lo compra porque concluye que lo necesita. En marketing suele nombrarse **embudo de webinar** o **webinar funnel**; cuando el acceso se abre comentando una palabra en la publicación, también se habla de **comment-gate** (comentario como puerta al registro). Registrar el nombre no es todavía la auditoría que pidió.

### Lo que pidió verificar (pendiente adrede)

- Si Captoora tiene un embudo similar. Su propia hipótesis, y la observación previa de Lupe el mismo 15 nov, es que **no**: no hay un CTA de «comenta PALABRA» que lleve a webinar y luego a un curso. El CTA vigente de Buen Fin es WhatsApp del estudio + frase «Quiero mi sesión Buen Fin», y la reserva en `https://captoora.studio`. Eso no se da por cerrado: hay que verificarlo con evidencia (parrilla, Buffer, ManyChat, site, WhatsApp) en el siguiente paso.
- Que el contenido que sí quieren es de **valor**: que eduque, que la gente lo quiera guardar y lo quiera compartir para consultarlo después. Preguntó, con razón, cómo se asegura que lo que hacemos es de valor, para qué se crea, de qué tipo y cada cuándo.
- Mezcla que quiere ver cuantificada: cuánto es educativo, cuánto llama a la compra, cuánto es de venta, cuánto es de trabajo (detrás de cámaras / oficio), cuánto es memes.
- Por qué no tienen un motor de ~240 publicaciones al mes (el post de referencia hablaba de 244 en octubre: 156 videos, 71 historias, 15 carruseles). Dejó claro que una cosa es poder producir piezas y otra es tener ese ritmo con sentido.
- La idea de enseñar: si ya producen con un equipo de agentes (investigar, escribir, producir, publicar, con él aprobando), quizá ya no se trata solo de seguir aprendiendo, sino de poder enseñar ese sistema.

### Hechos ya conocidos que la auditoría deberá usar (no sustituyen la verificación)

- Toda pieza sale solo con OK expreso del maestro, en sus palabras. Eso protege la marca y también pone un techo al ritmo.
- Buffer, en el plan gratuito, admite como máximo 10 posts programados; lo que no cabe va por Meta Business Suite, y el IG no estaba conectado ahí el 14 nov.
- Hay documentación previa de una «mezcla editorial aprobada y mínimo dos piezas diarias» (commit `d48a115`, 23 oct 2026, en la historia del repo). No se reabrió ni se midió en este checkpoint si esa mezcla se está cumpliendo en noviembre.
- Lo publicado el 14 nov es, de hecho, contenido de oferta / CTA de Buen Fin, no una pieza educativa pensada para guardarse.
- El post de referencia usa un equipo de agentes muy parecido al de Marky, Konan y Lupe; lo que el propio hilo señaló como hueco es elegir temas según lo que más alcance tuvo.

Este archivo no abre esa auditoría. Queda como siguiente trabajo, cuando el maestro lo indique, o cuando haya cuota para hacerla con evidencia.

---

## Qué se guardó en GitHub en este corte y qué no

Ramas (sin force-push, sin reescribir `main`, sin borrar nada):

- `checkpoint-2026-11-15` — este documento, a partir de `main` en el commit `eb72f23`.
- `checkpoint-2026-11-15-site` — cambios locales no confirmados del clon `captoora-site` (rama de origen `redesign-oct10`): solo CSS/HTML/JS y markdown de estrategia; **sin** `portfolio_src/` (~355 MB), `shots/`, fotos de portafolio, flyers ni bases64 de imágenes.
- `checkpoint-2026-11-15-cap_main` — preserva el commit local `02dee48` (12 oct 2026) del clon `cap_main`, que no está en `origin/main`. Historia vieja; no mezclar a `main` sin revisión.

No se subió, a propósito:

- Videos del Reel en `/workspace/lanzamiento-web/reel/` (ya están en `captoora-media` en Vercel).
- `/workspace/captoora/base_conocimiento_whatsapp.md` y `leads_corp_2026-11-15.md` (riesgo de datos sensibles o de terceros).
- Originales de fotos, capturas pesadas y cualquier archivo de más de 20 MB.
- El contenido de asuntos legales o personales atendidos por Harvey, Opptny o GirU.

También se añadió una entrada breve, solo al final y sin borrar nada, en la bitácora de Google Docs (`1b_7S2n4-RQHfCh7duAURftttl-Ivd2GySPY3O_DbOS0`).
