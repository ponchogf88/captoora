# Dirección visual y control de calidad

## Invariantes

Conservar rostro, facciones, expresión, mirada, piel real, cabello completo, pose, proporciones, dimensiones, manos, dedos, ropa, accesorios, tatuajes, productos y encuadre de la fuente. No perfilar caras, adelgazar, embellecer anatomía ni inventar extremidades fuera de cuadro. No prometer igualdad de píxeles de un resultado generativo.

## Fondos negros

- Estudio elegante negro/carbón con profundidad, pequeñas sombras y luz ámbar difusa muy discreta; el usuario pidió reducir la intensidad inicial aproximadamente 35–40%. Es dirección visual relativa, no valor de exposición medido.
- Conservar el contraluz real que ilumina rizos y mechones. No dibujar contornos duros ni inventar volumen capilar.
- Paneles LED discretos, parcialmente fuera de cuadro, sin manos o brazos del asistente. No convertirlos en rectángulos dominantes. La decisión anterior de conservar manos quedó sustituida.
- Suelo de peluche negro muy corto, casi terciopelo/microfibra; reducir protagonismo y volumen. Nada de montículos de pelo largo. Solo donde la toma original muestra suelo: no alejar cámara para inventarlo.
- El piso negro lustroso fue una alternativa mostrada, no la elegida. La versión C de peluche ligero de DSC00108 fue aceptada; un ajuste posterior aún más corto permanece separado.

## Fondos blancos y grupos

Mantener textura y sombras originales, incluso leves tonos cálidos y esquinas ligeramente oscuras; no producir un recorte blanco plano de catálogo. Suelo de peluche blanco continuo; extenderlo donde termina el set y difuminarlo suavemente hacia esquinas lejanas. No tapar sombras de apoyo ni convertir toda la escena en beige intenso. Dreamy pertenece al fondo y a la textura, no a borrar piel, caras o productos.

## Flujo real

1. Inventario Drive y fuente exacta por ID; orientar visualmente. EXIF puede no indicar giro: comprobar ojos/cabeza arriba. DSC01909 es horizontal y debe seguir horizontal.
2. Cargar la fuente y verla antes de editar. Usar una llamada de editor por imagen, no una generación de collage para diez fotos.
3. Prompt: alcance local del cambio + invariantes + fondo + textura/luz + objetos que deben permanecer + prohibiciones. Los prompts enviados se guardan completos en inglés en `prompts/ejecutados_exactos.json`.
4. Guardar PNG de salida y exportar JPG de calidad 97 sin submuestreo cromático cuando se usa Pillow. Esa conversión cambia formato, no demuestra aumento de resolución ni mejora la fuente.
5. Revisar cada salida contra original, además de la hoja de contacto. Numerar con nombre fuente. Guardar JPG en revisión y leer la carpeta para verificar existencia.
6. Solo la aprobación expresa mueve una versión a aprobadas; la aprobación del concepto no aprueba todas las fotos futuras. Guardar fecha/decisión/enlace y actualizar GitHub.

## Revisión ampliada obligatoria

| Zona | Qué observar | Motivo de rechazo |
|---|---|---|
| Cara y cuerpo | Geometría y escala respecto a fuente, expresión y pose | Cara distinta, cintura afinada, sujeto desplazado o reducido |
| Cabello | Rizos, puntas, transparencia y contraluz naturales | Halos, bloques, recorte erosionado, pelo inventado |
| Manos y objetos | Dedos, contacto, copa transparente y reflejos | Dedos extra, copa deformada, mano eliminada por error |
| Producto | Cantidad, posición, forma, etiquetas y texto | Envase nuevo, marca o texto cambiado |
| Suelo | Perspectiva, textura discreta, sombra de apoyo | Sujeto flotando, pelo exagerado, suelo fuera de encuadre inventado |
| Equipo | Panel mínimo sin ayudante | Brazos/manos, luz flotante excesiva o dominante |

## Fallos que no se repiten

El lote01 se hizo con Vision/máscaras locales y un fondo generado antes. Fue rechazado por bordes/cabello, aunque los interiores de cara coincidieran numéricamente. No hubo veinte generaciones nuevas para ese lote; el consumo global de cuota no se pudo determinar. Se abandonó esa composición como método del nuevo lote.

Las primeras generaciones de DSC00108 cambiaron escala y encuadre pese al prompt; fueron señaladas como pruebas, no como fidelidad garantizada. Las versiones posteriores recibieron aprobación estética. Mantener ese límite documentado y comparar siempre con el original, no solo contra una edición ya alterada.

Los primeros seis aprobados tienen métodos mixtos: tres negros v05 compuestos localmente y tres blancos/grupal v02 generativos. Su aceptación no significa que ese algoritmo local vuelva a ser el recomendado para nuevos lotes.


Actualizacion posterior obligatoria: leer CORRECCION_LOCAL_V03.md. No continuar con generacion integral de caras o letras. Restauracion local desde originales expresamente autorizada; originales y versiones previas intactos, regiones y auditoria requeridas. No confundir aprobacion estetica previa con auditoria global de fidelidad de textos.
