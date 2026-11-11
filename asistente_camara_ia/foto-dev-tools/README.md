# Foto Dev Tools — Captoora

Proyecto de herramientas de desarrollador para fotografía, dentro de `asistente_camara_ia/`. No es solo Canon: cubre Nikon, Canon y hardware externo con IA.

## Lo que ya existe
- `asistente_camara_ia/servidor_tether_ia.py`: tether por USB con gphoto2 / digiCamControl / WIA PTP. Controla ISO, apertura y velocidad en Canon EOS 7D Mark II y detecta Nikon/Canon/Sony por PTP.
- `asistente_camara_ia/index.html`: interfaz "Modo Tether" / "Directo USB (gphoto2)".
- Lanzadores `ABRIR_ASISTENTE_CAMARA_MAC.command` y `ABRIR_ASISTENTE_CAMARA_WIN.bat`.
- Manual `MANUAL_NIKON_D3500_EVENTO_EN_VIVO.pdf` en la raíz.

## 1. Nikon + GPhoto2
- Cámara: Nikon D3500. Sin Wi-Fi, solo SnapBridge (Bluetooth). Muchos bloqueos.
- Con GPhoto2 (ingeniería inversa) ya se puede manipular desde la computadora y hacer tether por USB.
- Idea: documentar los comandos que ya funcionan y qué no funciona por los bloqueos de la D3500.

## 2. Canon + CCAPI / EDSDK
- Cuenta Canon Developer Community: lic.jagf87@gmail.com, usuario ponchogf88, empresa Captoora. Registro enviado el 11 nov 2026. Pendiente: crear la contraseña desde el correo "Welcome to the Canon Developer Community".
- CCAPI: API REST por HTTP sobre Wi-Fi, independiente de plataforma. Sirve para disparo remoto, ajustes, live view y transferencia.
- EDSDK: control por USB, Windows y Mac.
- Pendiente: solicitar acceso a CCAPI en SDK | API | Downloads > EOS & PowerShot Cameras, y luego la herramienta de activación CCAPI por USB.
- Nota: CCAPI es solo para cámaras Canon, no controla la Nikon.

## 3. Raspberry Pi en la zapata (Nikon)
- Idea en desarrollo: un módulo externo en la zapata de la Nikon D3500 con Raspberry Pi e IA, porque la cámara no tiene internet.
- Pendiente: definir modelo de Raspberry Pi, alimentación, conexión con la cámara (USB/PTP/gphoto2) y qué hace la IA (por ejemplo, asistir en ajustes, disparo o interfaz).

## 4. Vibe hacking / interfaces con IA
- Idea: cambiar la interfaz de un aparato con IA, como ya se hace con refrigeradores y televisiones (quitar publicidad, cambiar menús).
- Ejemplo: elegir Netflix o YouTube como si fuera Pokémon; entrar a una casa para Netflix, a un gimnasio para Amazon Prime.
- Aplicación a fotografía: una interfaz de cámara más visual y divertida, sin copiar marcas ni interfaces de terceros tal cual.

## Criterio de cámaras
- No es cambiarse de marca. Retrato: Canon. Paisaje: Nikon.
- Objetivo: detectar qué cámara usar para cada situación.

## Reglas
- No publicar ni cambiar nada en main sin aprobación.
- Antes de producir/entregar cualquier pieza visual comercial, leer y aplicar docs/LEY_VISUAL_CAPTOORA.md; toda pieza debe incluir fotografía protagonista, prohibidas entregas solo tipográficas.
- No guardar contraseñas, códigos ni datos bancarios en el repo.

## Dirección comercial
- Objetivo: monetizar este programa con una oferta comercial para el nicho de fotógrafos.
- Primero investigar a la competencia: qué programas similares existen y qué soluciones reales ofrecen.
- Ofrecer programas que combinen una serie de herramientas, sin saturar al usuario.
- La IA no es una navaja suiza que lo haga todo: es el puente/conector que dirige cada instrucción a la herramienta correcta, para evitar un cuello de botella.
