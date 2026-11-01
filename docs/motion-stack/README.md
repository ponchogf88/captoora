# Stack mínimo de movimiento — Captoora Signature

Demo aislada en `demos/signature-motion/`. No se publica a producción desde aquí y no modifica la página actual del estudio.

Fecha de la revisión de licencias: 1 de noviembre de 2026, contra el registro de npm y las páginas de cada proyecto.

## Las tres

| Biblioteca | Versión | Licencia | Qué hace en la demo |
| --- | --- | --- | --- |
| [Zdog](https://zzz.dog) | 1.1.3 | MIT | El diafragma. Lienzo 2D con volumen falso. Gira solo y también se arrastra. |
| [glfx.js](https://github.com/evanw/glfx.js) | 0.0.4 | MIT | El retrato. Un solo contexto WebGL1, textura tope de 800 px de ancho. Viñeta, brillo y un sepia corto, en el tiempo. |
| [VFX-JS](https://github.com/fand/vfx-js) (`@vfx-js/core`) | 1.1.0 | MIT | El título respira en un shader (la opacidad de las letras). Si WebGL2 no existe, o si el cuadro se queda por debajo de unos 11 fps de forma sostenida, la placa vuelve a HTML. |

Los textos MIT están en `demos/signature-motion/LICENCIAS.md`.

## Por qué Signature, y por qué estas tres

Signature es la línea de bodas, quince años y producciones que piden más tiempo (`docs/VISION_PLATAFORMA_CAPTOORA.md`). El golpe visual que le queda es óptico y lento: un instrumento, un retrato, un barrido de luz. Biometrics pediría cuerpo, medidas o un modelo de visión. Eso empuja a MediaPipe, que esta máquina no debe cargar, y empujaría a inventar datos de salud. Pop se resolvería con confeti y fuegos, que en Signature se ven de otra marca.

En un iMac de 2015 (Intel i5, GPU integrada vieja: HD 6000 en el 21.5 básico, Iris Pro 6200 en el 27, a veces una Radeon en configuraciones altas) el presupuesto es un lienzo chico y, como mucho, dos contextos WebGL con el pixel ratio a raya.

1. **Zdog** no toca la GPU. El diafragma cabe en un canvas de 220 px. Sirve igual como anillo de medición si un día se hace Biometrics, o como juguete si se hace Pop, sin cambiar de motor.
2. **glfx.js** es el revelado, que es el producto. WebGL1 llega a esa Mac desde hace años. La textura va comprimida antes de subirla. No se usan los filtros caros de la misma librería (denoise, tilt-shift, desenfoque de lente): son bucles de muchos samples.
3. **VFX-JS** da el acento que alguien esperaría de Three.js o de Vanta, en un shader de una sola lectura de textura: el título late, sin deformar las letras. El lienzo de VFX-JS cubre el viewport y se limpia cada cuadro, así que aquí el `pixelRatio` queda en 1, y en 0.75 si el área CSS pasa de 2 megapíxeles (un 5K en modo 2560×1440 entra en ese caso). El apagado automático espera unos 4 segundos y solo corta si el promedio de 45 cuadros pasa de 90 ms. Un tropiezo breve no lo mata.

## GSAP, confirmado y dejado fuera

GSAP es gratis, plugins incluidos. Webflow lo anunció el 30 de abril de 2025 y el paquete `gsap@3.15.0` (13 de abril de 2026) sigue en esa condición. La licencia vigente es la [Standard “No Charge” License](https://gsap.com/standard-license/), no MIT y no una licencia abierta de la OSI.

Qué sí cubre: sitios, aplicaciones web e interfaces, uso comercial, y código generado por una IA. Qué no cubre: meter GSAP dentro de una herramienta visual para armar animaciones que compita con el builder de Webflow. Webflow puede retirar la licencia si se incumple.

Para animar el DOM de Captoora sería una buena pieza, y es ligera. No entra en este trío porque el encargo pide código abierto MIT o igual de permisivo. “Gratis” y “permisivo” no son la misma cosa.

## Qué no instalar en ese iMac

| Candidato | Licencia que vimos | Por qué se queda fuera de esta máquina |
| --- | --- | --- |
| Remotion, y sobre todo su render | Propietaria, código visible. Gratis para una persona o un equipo de hasta 3. De ahí en adelante hay licencia de empresa. | No es MIT. El render abre Chrome sin cabeza, come RAM y escribe video. En un i5 de 2015 es un horno, y el estudio puede crecer de tamaño y salir del tramo gratis. |
| MediaPipe | Apache-2.0 | Los modelos pesan y corren en WASM más GPU. En la integrada el cuadro se cae y el equipo se calienta. Es la tentación de Biometrics y justo la que hay que rechazar aquí. |
| GaussianSplats3D (`@mkkellogg/gaussian-splats-3d`, MIT en npm) | MIT | Nubes de puntos 3D, mucho ancho de banda de textura. La integrada no tiene ese presupuesto. |
| Rapier (`@dimforge/rapier3d-compat`, Apache-2.0) | Apache-2.0 | Física en WASM. No pone el retrato ni el diafragma, y el i5 paga el arranque del módulo para un efecto que la landing no necesita. |
| FFmpeg en local, pipelines largos | LGPL 2.1 o GPL, según cómo se compile. No es una librería de página. | Transcodificar en ese CPU es lento. La landing no tiene que producir video en la Mac. |
| Three.js + Drei + three-nebula, juntos | Los tres MIT | Drei arrastra React y React Three Fiber. three-nebula llena la vista de partículas encima de otra escena WebGL. El combo es el que se siente en el ventilador. Three.js solo, una malla y `pixelRatio` 1, podría vivir otro día. No hace falta para esta demo. |
| Vanta | MIT | El fondo animado carga Three.js o p5 y pinta el viewport entero. Es el mismo costo de un lienzo grande, con menos control que el shader chico de VFX-JS. |
| PixiJS Filters | MIT (Pixi y `pixi-filters`) | Otro renderer WebGL completo para un trabajo que glfx.js ya hace con un canvas. |
| Excalidraw | MIT | Pizarra. No anima la landing y pesa como aplicación. |
| Penpot | MPL-2.0 | Herramienta de diseño, copyleft por archivo, no un runtime de la página. |
| canvas-confetti | ISC | Muy ligera y permisiva. El gesto es de fiesta: le queda a Pop, no a Signature. |
| fireworks-js | MIT | También es de Pop. Con muchas partículas el canvas 2D sube el CPU del i5. |

## Cómo abrirla en la iMac

Sistema de partida: macOS Monterey 12 (el máximo oficial del iMac 2015). Navegador: Safari de ese sistema. Node: 20, por nvm, porque es LTS y sigue publicando binario Intel (`darwin-x64`).

Si nvm no está instalado, el instalador oficial es el de https://github.com/nvm-sh/nvm. Después, cierra y abre la terminal.

```bash
nvm install 20
nvm use 20
node -v

cd demos/signature-motion
npm install
npm start
```

En el navegador: http://127.0.0.1:4173/

`npm install` baja Zdog, glfx.js, VFX-JS y esbuild. esbuild trae un binario nativo; hace falta red esa primera vez. `npm start` compila `src/main.js` hacia `dist/demo.js` (destino ES2017, para el Safari de Monterey) y levanta un servidor de Node sin más dependencias, atado a `127.0.0.1:4173`.

Para parar el servidor: Ctrl+C en esa terminal.

### Reservas de sistema y de navegador

- El techo oficial de hardware es macOS Monterey 12.7. Con OpenCore se puede ir más lejos; esta demo no se probó ahí y no lo pide.
- El Capitan, Sierra y High Sierra se quedan cortos para Node 20 y para el JavaScript de VFX-JS, aunque el bundle baje a ES2017.
- Safari 15 y posteriores en Monterey tienen WebGL 1 y WebGL 2. Si WebGL 2 falta, el barrido no entra y el resto de la página sí.
- Chrome para Monterey dejó de actualizarse en algún punto de la vida de ese sistema. Si el instalador de Chrome se niega, usa Safari.
- No abras `index.html` con doble clic. El origen `file://` mancha el lienzo y glfx.js no puede leer la foto. Tiene que ser el servidor local.
- La pantalla Retina 5K reporta muchos pixeles CSS. Por eso la foto no se sube a resolución nativa y el shader baja a 0.75 cuando el viewport es grande. Quitar ese tope es lo que haría tronar la integrada.
- `prefers-reduced-motion: reduce` arranca la página en pausa. El botón “Reanudar movimiento” la echa a andar.
- Si el promedio se queda por debajo de unos 11 fps, el latido de VFX-JS se desmonta y el título vuelve a HTML. Zdog y glfx.js se quedan. El texto de estado lo dice en la página.
- Conviene cerrar Final Cut, Chrome con muchas pestañas y cualquier visor 3D antes de abrirla. El i5 comparte la integrada con el escritorio.
- Python no hace falta. Monterey no trae un `python3` garantizado y este servidor es el de Node.

## Qué se ve, y qué no se afirma

La fotografía es de Pietro Henricky en Pexels, cuadro completo, 1400×2100. Ficha y licencia en `demos/signature-motion/assets/FUENTE.md`. No es una sesión de Captoora y la página lo dice.

El precio de Signature y lo que incluye la línea van como **[POR CONFIRMAR]**. La dirección (Av. Paseo de los Álamos 165, Colinas de San Jerónimo) y el WhatsApp 81 4005 0088 salen de `js/config.js`, que es el dato vigente del sitio, no un dato inventado para esta demo.

El enlace abre `https://wa.me/528140050088`.

Nada de esta carpeta está enlazado desde `index.html`. El sitio actual sigue igual.
