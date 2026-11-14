# Marcos de fotos vivos

**Proyecto:** Captoora  
**Fecha de la idea:** 13 de noviembre de 2026 (llamada con Jesús Gutiérrez, hora de Monterrey)  
**Estado:** idea en exploración. **No está aprobada para producción.**  
**Precios:** [POR CONFIRMAR]

Este documento reúne la idea de negocio que Jesús dictó en la llamada del 13 de noviembre de 2026: restaurar fotos antiguas, animarlas y entregarlas en un marco físico con pantallita, como un álbum vivo.

---

## 1. Concepto

La propuesta es devolverle vida a las fotos que la gente guarda en cajones, monederos o álbumes viejos.

El servicio tendría tres pasos:

1. **Restaurar** la foto antigua con inteligencia artificial.
2. **Animarla con un clic**, para que el retrato se mueva unos segundos en bucle, como si las personas estuvieran conviviendo en ese momento.
3. **Entregarla** en una pantallita empotrada en un marco físico personalizado: madera, impresión 3D, acrílico o cristal, con la opción de luces LED cálidas.

El resultado sería un **álbum vivo**, al estilo de los retratos de Harry Potter: no una pantalla suelta, sino un objeto que se puede colgar o poner en una mesa, y que parece que el momento sigue ocurriendo dentro del marco.

Para animar la foto, el camino más simple hoy es un solo clic, sin escribir un prompt:

- **Grok Imagine:** “Animar foto”.
- **Google Fotos:** “Foto a video”.

Encaja de forma natural con la línea de **restauración de fotos viejas** de Studio: primero se cuida la imagen, y después esa misma foto puede “revivir” en el marco. También se siente como un regalo de Navidad o de ocasión especial.

---

## 2. Opciones de pantalla

La investigación de proveedores se hizo el 13 de noviembre de 2026. Fue solo investigación: no se compró nada ni se contactó a vendedores. Los precios que aparecen abajo son **aproximados** a esa fecha y quedan **[POR CONFIRMAR]** (pueden cambiar por tipo de cambio, envío e IVA de importación a México). Varias fichas no se pudieron abrir por completo, así que hay que verificar precio y compatibilidad antes de cotizar.

En todos los casos de video, la arquitectura práctica es la misma:

**panel + placa HDMI compatible (casi siempre 5 V por USB-C o 12 V) + un reproductor pequeño que repita el clip en bucle.**

Un panel suelto (MIPI o eDP) no enciende por sí solo con un reproductor HDMI: la placa tiene que ser compatible con ese modelo concreto.

### IPS rígida (la favorita para el prototipo)

Es la opción más recomendable para las fotos vivas: se ve nítida de cerca, reproduce video con fluidez y es más sencilla de integrar en un marco a medida.

**Favorita:** Sharp **LQ079L1SX01**, de **7.9 pulgadas**, **1536×2048**, **325 PPI**, proporción **3:4**, tipo iPad mini. Es el mejor formato para un retrato clásico. La placa de este panel tiene que generar tres voltajes distintos (incluye rieles positivos y negativos).

Otras alternativas revisadas:

| Panel | Tamaño y resolución | Notas de precio (13 nov 2026, por confirmar) |
|---|---|---|
| **BOE TV080WUM-NL0** | 8", 1200×1920 | El panel suelto se vio en unos **USD 52** (USD 51.72 en ENLCD, ficha abierta). |
| **JDI LT070ME05000** | 7", 1200×1920 | Es el kit HDMI más común. Se indexó alrededor de **USD 70** (USD 69–75); *no verificado en la ficha del vendedor*. |
| **Sharp LS060R1SX01** | 6", 1440×2560 | Muy nítido, para un marco chico. Se indexó un kit alrededor de **EUR 50**; *precio no verificado en el detalle*. |
| **10.1" (p. ej. Sharp LQ101R1SX01)** | 10.1", 2560×1600 | Tamaño más cercano a una línea Signature. El kit se indexó en unos **USD 100**; *ficha no verificada*. |
| **LG LP133UD1-SPA1** | 13.3", 4K (3840×2160) | Pieza de lujo. El conjunto de panel más placa queda en unos **USD 330** (panel USD 199.99 + controladora USD 129.99, vistos en lcdparts.net el 13 nov 2026). |

Para una sola muestra conviene buscar en AliExpress. Para mayoreo, las fábricas de Shenzhen en Alibaba suelen pedir pedidos mínimos (en la investigación se vieron rangos de 50 a 100 piezas, según el vendedor).

### OLED flexible

Sí reproduce video y se puede curvar o integrar en formas menos convencionales.

Hay que tener en cuenta dos limitaciones:

- **Riesgo de quemado (burn-in)** si el mismo video se repite durante muchas horas.
- Brilla, así que no se parece tanto a una foto impresa.

El rango de precio visto en la investigación es de **USD 75 a 500**, también **[POR CONFIRMAR]**.

### Tinta electrónica (Spectra 6 / E Ink)

Es la que más se parece a **papel fotográfico**: no brilla como una pantalla de video.

No sirve para fotos vivas en movimiento, porque **no reproduce video**. Solo puede ir cambiando de foto cada tanto. Quedaría mejor como una línea aparte: un retrato que cambia de imagen, no un momento animado.

### Cómo leer estos precios

Son referencias de componentes al 13 de noviembre de 2026, no precios de venta al público ni costos finales del marco armado. El precio del producto terminado lo arma Marky y queda **[POR CONFIRMAR]** hasta que Jesús lo apruebe.

---

## 3. Alternativas

Además de la pantallita empotrada, en la llamada se exploraron dos caminos complementarios:

1. **Proyector de tiro corto (o ultra corto)** que proyecta **por detrás** sobre un acrílico colocado dentro del marco. La imagen aparecería en la superficie del marco, sin que se vea una pantalla convencional. Es una idea prometedora, pero pide prototipo físico: hay que revisar brillo en interiores, si la resolución es 1080p de verdad, el calor, el ruido y si el acrílico queda plano y uniforme.
2. **Film electrocrómico (smart film) táctil para ventanas.** Permitiría mostrar o ocultar la imagen sobre un cristal o una ventana. Queda como exploración, no como el camino principal del primer prototipo.

Estas alternativas no sustituyen, por ahora, al kit de IPS rígida para armar la primera muestra.

---

## 4. Flujo de trabajo

El recorrido que se imagina para el cliente es sencillo:

1. La persona **manda su foto por WhatsApp** al **81 4005 0088**.
2. En Captoora se **restaura** con Picsart, cuidando el rostro y los bordes.
3. Se **anima con un clic**, en Grok Imagine (“Animar foto”) o en Google Fotos (“Foto a video”).
4. Se **entrega el clip** (el retrato vivo en bucle) **junto con el marco** físico personalizado, ya con la pantallita empotrada y el video cargado.

Mientras el producto no esté aprobado, este flujo es solo una propuesta de operación. Nada se vende ni se publica sin el OK de Jesús.

---

## 5. La historia detrás

Esta idea no nació solo de una pantalla o de un truco de magia. Nació de algo más íntimo.

Jesús encontró el monedero de su papá fallecido, y adentro había fotos viejas. Esa costumbre —llevar cerca a las personas que queremos, en un retrato que cabe en la mano o en la cartera— es la que quiere devolverle a la gente, ahora con tecnología en lugar de papel.

El marco vivo sería eso: un objeto cotidiano y cariñoso, para que los seres queridos no se queden guardados en una caja, sino cerca, como si el momento todavía estuviera ocurriendo.

---

## 6. Estado y próximos pasos

**Estado actual:** idea en exploración. **No está aprobada para producción.** No se debe publicar, vender ni encargar piezas en serie hasta que Jesús lo autorice.

**Precios de venta y de kits:** [POR CONFIRMAR].

Próximos pasos sugeridos, si Jesús da luz verde a una prueba:

1. Armar **una muestra de un solo marco** (preferente: kit IPS de 7.9" Sharp LQ079L1SX01, o el kit HDMI de 7" u 8" si resulta más fácil de conseguir).
2. **Cotizar kits** concretos (panel + placa HDMI + reproductor en bucle), confirmando precio, voltaje, interfaz y envío a México.
3. Hacer una **prueba de animación** con una foto de dominio público o de stock —nunca del portafolio de Jesús—, en Grok Imagine y, si está disponible en México, en Google Fotos “Foto a video”.
4. **Revisar precios con Marky** (costo del marco, del servicio de restauración y animación, y posibles niveles Pop/Studio, Signature y lujo) antes de subir cualquier cifra a la web.

Hasta entonces, este archivo es solo memoria de la idea.
