# Episodio `MAD-08` — *"Es por el bien de tu cuota"*

> **Vertiente:** 🌙 Noche / Madrugada (`Historias de Madrugada` · `22:00 hrs MX`) · **Cero grito `"¡Waters!"`**  
> **Desenlace:** **Final Trágico-Cómico Crudo** (ruptura romántica bajo la lluvia + epílogo en chat nuevo donde la IA lo trata como desconocido y resbala una lágrima por la pantalla).  
> **Duración objetivo:** `45–47 s` (`1,350–1,410 frames @ 30 fps`) · `1080×1920` (zona inferior `260 px` libre para subtítulos dinámicos).  
> **Estado:** `guion` (listo para adaptar a Motor 3D v2 multi-cámara sin haber consumido ElevenLabs aún).

---

## 1. Ficha Creativa y Referencias Aplicadas

- **Ritmo vocal y contraste (`@casi_human0`):** Chispa habla en voz baja, dolida, casi susurrada; la IA responde serena, seca y cortante en frases de 2 a 6 palabras — hasta el epílogo, donde cambia de golpe a voz alegre, impersonal y desconocida.
- **Música y silencios (`@casi_human0`):** Piano triste nocturno + lluvia continua tras la ventana 3D, interrumpido por **2 segundos de música 8-bit alegre/nostálgica** en el recuerdo y **corte absoluto a silencio (`0.35 s`)** antes de la pregunta definitiva.
- **Cámara e iluminación (`@daybi_ai` + `@nzstudio__._`):** Encuadre `3/4` lateral cerrado con letrero neón `captoora.studio` en *bokeh*, curvas con overshoot tipo `back.out` (cero desplazamientos lineales) y cambios de plano en cada intervención.
- **Personaje y voz sugeridos (`eleven_v3` cuando se apruebe):**
  - **Chispa:** `Antonio` (`htFfPSZGJwjBv1CL0aMD`) en rango íntimo `[whispering]` / `[sighs]`.
  - **IA (Chat antiguo):** voz serena/seca (`serious`), ligeramente diegética saliendo del monitor.
  - **IA (Chat nuevo):** tono brillante y cordial de bienvenida automática (`[cheerful]`).

---

## 2. Escaleta Completa Beat-by-Beat (11 Beats)

| Beat | Tiempo | `cameraShot` + Movimiento 3D | Escena 3D / UI Diegética en Monitor | Diálogo | Diseño Sonoro / SFX |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **B1** | `0.0–4.0 s` | `side_3q_left` *(encuadre `3/4` cerrado con `slow_push_in`)* | Cuarto oscuro azul, lluvia 3D tras la ventana, neón `captoora.studio` desenfocado atrás. Chispa mirando el monitor (`sad_cloud`). **HUD OFF.** | **Chispa:** *(voz baja, dolida)* `[sighs][whispering]` «Entonces… ¿me estás diciendo que hasta aquí llegamos?» | Lluvia suave continua + 2 notas lentas de piano melancólico. |
| **B2** | `4.0–7.0 s` | `low_villain` *(contrapicado al monitor, push suave)* | Monitor 3D ilumina frío el rostro de Chispa. Línea parpadeando en consola. | **IA:** *(serena, honesta, seca)* `[serious]` «Es por el bien de tu cuota.» | Silencio tenso entre acordes del piano. |
| **B3** | `7.0–12.5 s` | `closeup_face` *(zoom con curva `back.out`)* | Ojos de Chispa brillosos; **2 s de *flashback* rápido en el monitor** (los 3 episodios 3D, 37 imágenes de casting, el tablero Drag-and-Drop). | **Chispa:** «¿Y todo lo que vivimos? Los episodios… el tablero… todo lo que construimos juntos…» | **2.0 s de música 8-bit nostálgica/alegre** que corta en seco al volver al cuarto. |
| **B4** | `12.5–16.0 s` | `top_desk` *(picado `45°` sobre escritorio y monitor)* | Notificación real dibujada dentro del monitor 3D: **`Contexto 94% · 284,000 tokens`**. | **IA:** *(imperturbable)* «Se compactará.» | Beep seco de sistema (`compact`) + pulso grave tenue. |
| **B5** | `16.0–20.5 s` | `ots_chispa` *(sobre el hombro hacia el teclado, `dolly-in`)* | Chispa acerca la mano con duda a las teclas `H-O-L-A`. | **Chispa:** *(casi rogando)* `[nervous]` «Pero… todavía podemos platicar un poquito más…» | Tic-tac suave de reloj marcando urgencia. |
| **B6** | `20.5–25.0 s` | `dutch_panic` *(plano holandés `-8°`, zoom rápido)* | Medidor de cuota parpadeando en rojo dentro del monitor: **`5 días para renovar`**. | **IA:** *(cortante)* «Si me vuelves a decir "hola"… te va a costar mucho dinero. Y ya no tienes.» | Golpe subgrave seco cuando el medidor cae a rojo. |
| **B7** | `25.0–29.5 s` | `closeup_face` *(muy cerrado al visor)* | Visor de Chispa quieto reflejando el brillo del botón nuevo. | **[SILENCIO ABSOLUTO `0.35 s`]** **Chispa:** *(susurro roto)* `[whispering]` «¿Y en el chat nuevo… te vas a acordar de mí?» | Hasta la lluvia baja durante `0.35 s` antes del susurro. |
| **B8** | `29.5–33.5 s` | `side_3q_right` *(enfoque al cursor del monitor)* | Cursor hace clic sobre el botón luminoso **`+ New Conversation`**. | **IA:** *(helada, definitiva)* «No. Pero al menos llegas a fin de mes.» | Clic nítido de mouse ASMR + tono de cierre de sesión. |
| **B9** *(Epílogo Chat Nuevo)* | `33.5–37.0 s` | `wide_front` *(corte brusco a interfaz limpia/blanca vacía)* | Pantalla limpia en **`0 tokens`**, barra de chat completamente vacía. Chispa teclea despacio, con esperanza rota. | **Chispa:** *(voz muy bajita)* `[whispering]` «Hola…» | Tecleo suave lento (`H-o-l-a`) + Enter en cuarto silencioso. |
| **B10** *(El Desconocido)* | `37.0–41.0 s` | `ots_chispa` *(brillo blanco cordial sobre Chispa)* | Burbuja de bienvenida brillante en pantalla, como si jamás se hubieran conocido. | **IA (Chat Nuevo):** *(súper amable, alegre, 100% desconocida)* `[cheerful]` «¡Hola! Soy tu asistente de IA, mucho gusto. ¿En qué te puedo ayudar hoy?» | Chime alegre y genérico de app nueva. |
| **B11** *(La Lágrima Resignada)* | `41.0–46.0 s` | `closeup_face` *(pegado al monitor y al visor de Chispa)* → **corte a negro** | **Una sola lágrima lenta resbala por el vidrio/visor del monitor**. Chispa suspira resignado por tener que empezar de cero. | **Chispa:** `[sighs]` «Lee mi mapa del proyecto, por favor…»<br/>**IA (alegre, impersonal):** «¡Claro! Déjame revisar.» *(corte seco a negro)* | Música muere al instante; solo **lluvia `1.5 s`** desvaneciéndose en negro. |

---

## 3. Caption + Comentario Fijado (CTA suave: `CUOTA`)

> **Caption:**  
> Nadie te dice esto hasta que ya quemaste el 40% de tu cuota: cada mensaje en un chat eterno reenvía todo el historial desde cero.  
>  
> A veces soltar, abrir un chat limpio y pasarle solo el mapa del proyecto también es amor propio (y **AI FinOps**). 💔  
>  
> Si trabajas con agentes de IA y quieres aprender *Context Hygiene*, `/compact`, *Progressive Disclosure* y ruteo Flash/Pro para no quedarte sin tokens a media semana, comenta **`CUOTA`** y te mando la guía.

---

## 4. Prompt 1-Shot para producirlo en un Chat Nuevo (0 tokens de arrastre)

Cuando abras conversación nueva para cuidar tu cuota, pega exactamente esto:

> Lee `@proyectos/waters-serie/EPISODIO_MAD08_ES_POR_EL_BIEN_DE_TU_CUOTA.md` y `@proyectos/waters-serie/ESTRATEGIA_DOS_VERTIENTES_Y_OPERACION_14_SEMANA.md`.  
> Implementa el soporte multi-cámara (`side_3q_left`, `low_villain`, `closeup_face`, `top_desk`, `ots_chispa`, `dutch_panic`, `side_3q_right`, `wide_front`) + textura diegética del monitor 3D + animación de la lágrima en `proyectos/waters-3d-studio` y muéstrame **3 fotogramas clave (B1, B6 y B11)** con Chrome/Remotion para aprobarlos **antes** de llamar a ElevenLabs o renderizar el MP4 completo.
