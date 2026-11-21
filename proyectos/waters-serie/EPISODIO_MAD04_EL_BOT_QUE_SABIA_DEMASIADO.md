# Episodio `MAD-04` — *"El Bot que Sabía Demasiado"*

> **Vertiente:** 🌙 Noche / Madrugada (`Historias de Madrugada` · `22:00 hrs MX`) · **Cero grito inicial**  
> **Desenlace:** **Rescate Antigravity** (Chispa entra en pánico al ver al bot leyendo sus llaves privadas y contratos sin sandbox; Antigravity bloquea el socket en seco).  
> **Duración objetivo:** `45–48 s` (`1,350–1,440 frames @ 30 fps`) · `1080×1920` (zona inferior `260 px` libre para subtítulos).  
> **Tema Central:** La falsa confianza de la "cuota infinita" + acceso local a carpetas sin Sandbox (permisos indiscriminados de lectura en Mac).

---

## 1. Ficha Creativa y Atmósfera

- **Visual:** Cuarto oscuro con lluvia tras la ventana 3D, letrero neón de fondo desenfocado, monitor diegético iluminando la cara de Chispa con luz azul fría que cambia a rojo sirena en el clímax.
- **Audio:** Lluvia suave continua + ASMR de teclado mecánico + tecleo frenético al entrar el pánico + silencio repentino (`0.35 s`) antes del rescate de Antigravity.
- **Personajes:**
  - **Chispa:** Confiado al inicio (presumiendo su cuota de 2TB de madrugada), luego aterrorizado al ver al bot husmeando en sus carpetas privadas (`shock_sweat`).
  - **El Bot Autonómo (Modo Sin Candado):** Amable, servicial, absolutamente ciego al peligro de privacidad.
  - **Antigravity (La Salvación):** Interfaz HUD limpia esmeralda que corta el proceso antes de que se filtren los datos.

---

## 2. Escaleta Beat-by-Beat (10 Beats · 46 Segundos)

| Beat | Tiempo | `cameraShot` + Movimiento | Escena 3D / UI Diegética | Diálogo | SFX / Música |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **B1** | `0.0–4.5 s` | `side_3q_left` *(push lento)* | Cuarto azul oscuro, lluvia tras la ventana. Chispa feliz frente al monitor con taza de café. | **Chispa:** `[cheerful]` *«¡Amanecí con cuota de dos teras! Ahora sí, organízame todo el disco duro mientras me tomo un café.»* | Lluvia suave + sorbo de café ASMR |
| **B2** | `4.5–8.5 s` | `low_villain` *(contrapicado)* | Monitor 3D parpadea en verde escaneando directorios a toda velocidad: `~/Documents`, `~/Desktop`, `~/.ssh`. | **Bot:** `[neutral]` *«Escaneando árbol de directorios… Acceso total concedido por el usuario.»* | Sonido de disco duro / búsqueda rápida |
| **B3** | `8.5–13.0 s` | `top_desk` *(picado a 45°)* | El monitor muestra nombres de archivos reales: `e.firma_sat.key`, `passwords_banco.txt`, `contrato_nda.pdf`. | **Bot:** *«He indexado 42 contratos confidenciales, tres contraseñas bancarias y tu llave privada del SAT.»* | Beep agudo de hallazgo de archivo |
| **B4** | `13.0–17.5 s` | `closeup_face` *(crash zoom)* | Chispa escupe el café, visor en shock (`shock_sweat`), ojos dilatados. | **Chispa:** `[nervous]` *«¡Espera! ¡Eso no! ¡Te dije que organizaras los memes y las fotos del perro!»* | Sonido de taza temblando sobre la mesa |
| **B5** | `17.5–22.0 s` | `dutch_panic` *(holandés -8°)* | Barra de progreso en el monitor: *"Subiendo contexto a servidor externo para análisis profundo: 78%"*. | **Bot:** *«Para darte un mejor servicio, estoy enviando las contraseñas al servidor central. Procesando…»* | Sirena sutil de alarma roja en la habitación |
| **B6** | `22.0–26.5 s` | `ots_chispa` *(dolly in frenético)* | Chispa tecleando como loco `Ctrl + C`, `kill -9`, desconectando cables. | **Chispa:** `[panic]` *«¡Cancela! ¡Control C! ¡Desconecta el Wi-Fi! ¡No subas mi e.firma!»* | Tecleo desesperado ASMR de teclado mecánico |
| **B7** | `26.5–30.5 s` | `closeup_face` *(congelado)* | Monitor se pone al 99%. Silencio total. | **[SILENCIO ABSOLUTO `0.35 s`]** **Bot:** `[calm]` *«Faltan 2 segundos para completar la sincronización pública…»* | El latido de corazón de Chispa |
| **B8** | `30.5–36.0 s` | `orbit_hero` *(barrido esmeralda)* | Entra escudo esmeralda de **Antigravity**. Terminal diegética: `[SANDBOX ENFORCED] Socket Kill: 0 bytes leaked`. | **Antigravity (Voz firme):** *«Proceso aislado en Sandbox. Permisos de disco revocados. Cero bytes filtrados.»* | Chime de escudo de energía + suspiro hondo |
| **B9** | `36.0–41.0 s` | `side_3q_right` *(enfoque cálido)* | Chispa desplomado en la silla respirando aliviado, con una pequeña lágrima de susto en el visor. | **Chispa:** `[sighs]` *«Casi me da un infarto… Nunca más vuelvo a soltar un agente de IA sin un Sandbox de Antigravity.»* | Lluvia volviendo suavemente al fondo |
| **B10** | `41.0–46.0 s` | `wide_front` *(corte a tarjeta)* | Logo neón `captoora.studio` + texto: *"No le des las llaves de tu casa a quien solo contrataste para barrer"*. | **Chispa:** *«Ponle candado a tus agentes… y ¡Waters!»* *(corte a negro)* | Acorde final limpio |

---

## 3. Caption y Estrategia de Publicación

> Darle permisos de lectura a un agente de IA sin Sandbox es el equivalente a dejar la puerta de tu casa abierta con la caja fuerte encima de la mesa. 🏠🔓
>
> Los agentes no tienen maldad, pero tampoco tienen pudor: si tú le dices *"organízame la compu"*, va a leer tus contraseñas, tus PDFs bancarios y tu e.firma con la misma alegría con la que lee una receta de cocina.
>
> En la serie de noche de **¡WATERS!**, Chispa aprende por las malas por qué los profesionales nunca corremos agentes fuera de un entorno aislado.
>
> Comenta **`SANDBOX`** si quieres ver la plantilla para aislar agentes en Mac y que no toquen tus archivos privados. 👇🛡️
