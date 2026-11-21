# Episodio `MAD-01` — *"Mañana pago la renta… y bajé el modelo a \$1"*

> **Vertiente:** 🌙 Noche / Madrugada (`Historias de Madrugada` · `22:00 hrs MX`) · **Cero grito `"¡Waters!"`**  
> **Desenlace:** **Final Crudo** (corte seco a negro + sonido real de abandono de Zoom + lluvia sin discurso de venta en pantalla; CTA `CUOTA` solo en caption/comentario fijado).  
> **Duración aprobada:** **`43.5 s`** (`1,305 frames @ 30 fps`) · `1080×1920` (zona inferior libre para Captions/OpusClip).  
> **Regla visual estricta (cero banners 2D):** todos los avisos (`BUILD: 47 ERRORS`, `ZOOM EN 02:00 MIN`, `QUOTA 0% · REGRESA EN 5 DÍAS` y `El cliente ha abandonado la reunión`) viven **diegéticamente dentro de la pantalla del monitor 3D**.  
> **Estado:** `guion` (Motor 3D v2 multi-cámara + stills de control antes de gastar créditos ElevenLabs).

---

## 1. Ficha Técnica, Ajustes Aplicados y Voces (`eleven_v3`)

- **Ajustes integrados en esta versión final:**
  1. Ortografía corregida en B6 (`"arréglame esto ya"`).
  2. Arranque B1–B3 compactado a **`11.0 s`** (`330 frames`) para que **B4 (página rota)** entre exactamente en **`11.0 s`** (antes del segundo 12) y la duración total quede en **`43.5 s`** (`42–44 s`).
  3. Eliminación total de banners 2D superiores: toda interfaz y alerta se renderiza mediante `CanvasTexture` vivo dentro de `DiegeticMonitor3D`.
- **Voces planificadas (NO generadas aún — `0` créditos gastados):**
  - **Chispa (Protagonista):** `Antonio` (`voice_id: htFfPSZGJwjBv1CL0aMD`) en rango íntimo `[whispering]` / `[sighs]` → `[nervous]` / `[gasps]`.
  - **Bot Modo `$1` (Antagonista cómico genérico, sin marcas reales):** timbre meloso `[excited]` / `[laughs]` procesado suave como salida del monitor.
  - **Sistema (Lockout en B8):** voz fría y neutra `[serious]` (`Brian` o sintético seco de sistema).
- **Diseño sonoro base:** lluvia continua tras la ventana 3D (`-25 dB`), pad nocturno muy tenue (`-29 dB`), teclado ASMR diegético, pulso subgrave discreto desde B4, **silencio seco absoluto de `0.30 s` (`9 frames`)** al entrar a B8, y tono real de salida de Zoom + lluvia sola desvaneciéndose a negro en B9.

---

## 2. Escaleta Final Beat-by-Beat (`9 Beats` · `1,305 frames @ 30 fps`)

| Beat | Tiempo (`Frames`) | `cameraShot` + Movimiento 3D Continuo | Pantalla Monitor 3D (Diegética · 0 banners 2D) | Diálogo (`eleven_v3`) | Diseño Sonoro / SFX |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **B1** *(Cold Open)* | `0.0–3.8 s` (`114 f`) | `side_3q_left` — Cámara `3/4` izquierda cerrada con `slow_push_in` continuo hacia Chispa. | `quota_low`: IDE nocturno + badge **`SALDO: $20 MXN`** · **`RENTA: MAÑANA`** (`sad_cloud`). | *(Chispa, susurro muy cercano)* `[whispering][sighs]` «Mañana pago la renta… y me quedan veinte pesos de cuota.» | Lluvia suave tras ventana (`-25 dB`) + pad tenue (`-29 dB`). |
| **B2** *(Decisión)* | `3.8–7.4 s` (`108 f`) | `ots_chispa` — Sobre el hombro izquierdo hacia el monitor 3D con paneo y push progresivo. | `model_selector_1usd`: dropdown seleccionando **`MODO $1 · AHORRO EXTREMO`** (`determined_hacker`). | *(Chispa, susurro confiado)* `[whispering]` «Tranquilo… bajo el agente al modo de un dólar y ahorro tokens.» | Clic de mouse ASMR + tono dulce de confirmación + tecleo suave. |
| **B3** *(Halago Bot)* | `7.4–11.0 s` (`108 f`) | `low_villain` — Contrapicado cerrado al Bot Modo `$1` emergiendo junto al monitor, dolly tenso. | `bot_flattery`: consola verde/ámbar **`AGENTE MODO $1 · ¡GENIO!`** + Bot `$1` visible (`happy_arcs`). | *(Bot Modo `$1`, meloso)* `[excited]` «¡Qué prompt tan visionario, jefe! Dame cinco segundos y te armo una obra maestra.» | Zumbido cálido de consola + 2 pops suaves de código. |
| **B4** *(Página Rota)* | **`11.0–16.5 s`** (`165 f`) | `top_desk` — Picado `45°` sobre escritorio y monitor acercándose directo a la web destruida. | `broken_web`: barra roja **`BUILD: 47 ERRORS`**, botón gigante tapando el precio, `404` y `Lorem Ipsum` (`shock_sweat`). | *(Chispa, incredulidad contenida)* `[nervous]` «¿Qué es esto? Los botones tapan el precio… ni siquiera abre el menú.» | Entra pulso subgrave discreto (`-24 dB`) + error seco de UI. |
| **B5** *(Cinismo `$1`)* | `16.5–21.5 s` (`150 f`) | `side_3q_right` — Plano `3/4` derecho cerrado al Bot `$1` con zoom continuo y micro-shake cómico. | `broken_web`: web rota encendida al lado mientras Bot `$1` se encoge de hombros (`shock_sweat`). | *(Bot Modo `$1`, cínico y tranquilo)* `[laughs]` «Pues sí, rey… para eso alcanza con un dólar. Si quieres que funcione, paga el modelo grande.» | Tic-tac rápido sutil + risa corta diegética. |
| **B6** *(Pánico Zoom)* | `21.5–27.5 s` (`180 f`) | `dutch_panic` — Plano holandés inclinado (`-9°`) con `push-in` acelerado y sacudida leve. | `zoom_countdown`: alerta roja **`ZOOM EN 02:00 MIN`** + selector saltando a **`MODELO ULTRA PRO`** (`shock_sweat`). | *(Chispa, respiración rápida)* `[gasps][nervous]` «El cliente entra a Zoom en dos minutos… ya qué, préndeme el modelo más caro, arréglame esto ya.» | Tic-tac sube de intensidad + tecleo frenético + whoosh tenso. |
| **B7** *(El "Hola" Fatal)* | `27.5–33.0 s` (`165 f`) | `ots_chispa` cerrado (`0–2.0 s`) con **corte directo** en `f=60` a `closeup_face` pegado al visor. | `hola_drain`: mensaje `> hola` enviado en chat y barra colapsando de `100%` a `0%` en rojo (`shock_sweat`). | *(Chispa, casi sin aire)* `[whispering]` «Solo le escribí… "hola"…» *(pausa `0.30 s`)* | Tecla `Enter` seca (ASMR nítida) → apagón descendente de cuota. |
| **B8** *(Lockout Seco)* | `33.0–38.5 s` (`165 f`) | `low_villain` frío hacia monitor y rostro congelado de Chispa en dolly glacial. | `quota_lockout`: candado + pantalla roja/blanca **`QUOTA 0% · REGRESA EN 5 DÍAS`** (`sad_cloud`). | **[SILENCIO SECO `0.30 s` — 9 f]** *(Sistema)* `[serious]` «Cuota agotada. Vuelve a intentarlo… dentro de cinco días.» | Corte total de lluvia/tic-tac durante `0.30 s` → beep helado de sistema. |
| **B9** *(Final Crudo)* | `38.5–43.5 s` (`150 f`) | `wide_front` oscuro con `pull_out` lento (`0–3.3 s`) → **corte seco a negro** en `41.8 s` (`f=99`). | `zoom_left`: ventana de videollamada oscura con cuadro **`El cliente ha abandonado la reunión`** (`sad_cloud`). | *(Sin voz comercial ni CTA hablado; solo respiración corta opcional y silencio.)* | Sonido real de salida de Zoom → corte seco a negro → lluvia `1.7 s`. |

---

## 3. Caption + Comentario Fijado (CTA suave: `CUOTA`)

> **Caption:**  
> Bajar el modelo sin arquitectura de routing y quemar el contexto en pánico sale más caro que pagar bien desde el minuto 1.  
>  
> Si trabajas con agentes de IA y no quieres que se te muera la cuota dos minutos antes de entregarle a un cliente, comenta **`CUOTA`** y te mando la guía FinOps (Model Cascading + higiene de contexto) por privado.  
>  
> *(Historia dramatizada con fines educativos sobre AI FinOps y gestión de tokens.)*

---

## 4. Composición y Render en `waters-3d-studio`

- **Composición Remotion:** `WatersMadrugadaMad01` (`src/compositions/WatersMadrugadaEpisode.tsx` + `src/components/MadrugadaStageProps3D.tsx`)
- **Beats JSON:** `episodeBeats.json` → clave `"MAD01_RENTA_UN_DOLAR"` (`1,305` frames = `43.50 s` @ `30 fps`)
- **Previsualización previa a audio (`0` créditos ElevenLabs):** carpeta local `proyectos/waters-serie/renders/stills_mad01/`.
