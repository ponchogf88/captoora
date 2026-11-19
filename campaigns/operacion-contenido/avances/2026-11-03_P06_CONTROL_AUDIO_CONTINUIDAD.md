# P06 · Control técnico de audio y continuidad

Fecha/hora: 2026-11-03 08:00 CST  
Archivo: `VIDEO_VIRAL_01_COMO_FUNCIONA_CAPTOORA.mp4`

## Pruebas ejecutadas

- `ffprobe`: 48.921 s, H.264 1080 × 1920 a 30 fps; AAC estéreo 44.1 kHz; 49,996,320 bytes.
- `ffmpeg` con `astats`: pico -3.01 dBFS, RMS -19.94 dBFS, piso de ruido aproximado -65.26 dBFS; sin NaN, infinitos ni muestras desnormalizadas.
- `silencedetect` a -35 dB y 0.4 s: pausas de 0.522 s y 0.630 s alrededor de 28.33–28.85 s y 29.93–30.56 s. Son pausas breves, no evidencia por sí mismas de un defecto.
- `blackdetect` a 0.3 s: no reportó segmentos negros prolongados.
- SHA-256 conservado: `fcfe011459cb8be089e47e2e934c165813c5edd44cfc173bdeb5175c090e1354`.

## Decisión editorial

El archivo es técnicamente reproducible y no presenta clipping digital evidente ni huecos negros prolongados. Este control no valida la locución palabra por palabra, música, licencias, promesas comerciales ni el subtítulo inglés detectado anteriormente. P06 permanece en **revisión** y no se cuenta como pieza terminada.

## Siguiente acción

Escuchar el reel completo con monitoreo humano, cotejar texto y CTA con la oferta vigente, acreditar cada clip y corregir el subtítulo inglés en Canva, Captions, OpusClip o CapCut.

## Herramientas y consumo

`ffprobe` y `ffmpeg` locales. Servicios externos no utilizados; créditos consumidos: 0.
