# Auditoría técnica de `assets/media_jpg` · 2026-11-03 04:00 CST

## Alcance y resultado

- Carpeta inspeccionada sin mover, copiar, renombrar ni editar fotografías.
- 57 archivos JPG, 19 MiB en total.
- Todos los archivos abrieron con `sips`; dimensiones entre 359×430 y 4000×5000 px.
- Se calcularon SHA-256 de los 57 archivos. No se encontraron duplicados byte a byte dentro de la carpeta.
- Se identificaron 6 finales 4:5 de alta resolución (`IG_CPT_*`, 3200×4000 o 4000×5000), 10 archivos Farmasi, 40 archivos `pf-*` y un escenario.

## Lectura editorial

- La presencia en `assets/` y un nombre descriptivo no acreditan consentimiento, autoría, release ni permiso comercial.
- Los seis `IG_CPT_*` son técnicamente aptos para publicación 4:5, pero su uso queda condicionado a localizar la sesión y autorización de cada persona.
- Los archivos `pf-*` mezclan retratos, familia y fotografía social; varias imágenes tienen resolución baja para recortes o movimiento. Deben tratarse como candidatos, no como portafolio aprobado.
- Los archivos Farmasi ya están cubiertos por el manifiesto de derechos del 2 de noviembre y siguen condicionados.

## Evidencia reproducible

- Herramientas reales: `find`, `stat`, `du`, `sips`, `shasum` e inspección visual local.
- La salida completa de nombre, dimensiones, bytes y SHA-256 se obtuvo durante este ciclo; no se creó una copia de las fotografías por la ley de custodia visual.
- Espacio disponible al inicio: 398 GiB.

## Decisión

Conservar la biblioteca sin cambios. No incorporar ningún archivo a una publicación ni a un reel hasta enlazarlo con sesión, autoría y consentimiento. Priorizar la acreditación de los seis `IG_CPT_*`, porque ya cumplen formato y resolución 4:5.

