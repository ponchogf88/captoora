# Recetas vigentes y biblioteca de prompts

## No confundir tres cosas
1. `ejecutados_exactos.json` contiene148 prompts históricos reales e inalterados, incluidos intentos bloqueados identificados así. Conserva su texto, fuente, ID y proveedor/modelo cuando fue expuesto. El estado histórico de una ejecución no sustituye `fuentes_799.json`.
2. Las plantillas siguientes son instrucciones NUEVAS de relevo, NO prompts ejecutados históricamente.
3. Las últimas restauraciones no usaron generación: se reproducen con píxeles de los originales, regiones, matrices y curvas registradas. No existe un «prompt secreto» que explique por sí solo todos los resultados.

## Preparación por imagen
Localizar la fuente por ID/URL del inventario. Abrirla y orientarla visualmente. Abrir una referencia aprobada del mismo tipo. Conservar archivo y hash originales. Anotar exactamente qué se permite cambiar. No usar como fuente una previsualización, screenshot o edición que ya alteró identidad.

## Fondo blanco y grupal — plantilla no ejecutada
Usar SOLO con una máscara verificada que excluya sujeto completo, cabello, transparencias, manos y todos los envases/etiquetas. Si no se puede protegerlos, no lanzar generación masiva.

```text
Edit ONLY the explicitly supplied background selection of ORIGINAL_SOURCE.
Preserve every unselected original pixel: all people, facial features, expression,
gaze, natural skin texture, hair and curls, body scale, pose, hands, clothes,
products, labels, logos and text. Do not redraw or beautify any subject.
Keep the original framing, camera angle, dimensions and perspective.
Remove domestic room edges, unwanted stands/cables/mirrors and baseboards only
inside the allowed selection. Continue an off-white professional studio backdrop,
retaining the existing soft warm cast shadows and subtle corner falloff.
Where floor already exists, continue the original fine white plush texture and
contact shadows, with very soft distant edges. Dreamy applies to the environment,
not to faces, hair or product print. Do not flatten onto pure catalogue white.
No new people, text, watermark, accessories or invented product print.
```
Referencias: DSC02415_v02 (grupal), DSC01197_v02 (individual) y sus URLs vigentes en `registros/artefactos.json`. Las limitaciones generativas de microtexto de estas referencias siguen documentadas: no copiarlas como fuente de letras.

## Fondo negro — plantilla no ejecutada
Misma protección obligatoria de sujeto y productos. La plantilla NO garantiza por sí sola que el motor la respete.

```text
Edit ONLY the verified background selection of ORIGINAL_SOURCE.
Keep the entire original person and every product untouched and registered to
its original position. Preserve face, expression, real skin texture, all hair,
curls and flyaways, body proportions, pose, hands, clothes and exact printed text.
Create a dimensional deep charcoal studio environment with restrained diffuse
warm amber glow, approximately35-40 percent less prominent than the initial
strong amber reference. No literal beam or bright orange wash.
Retain the real hair rim light without drawing new strands or hard halos.
If floor is already visible, use almost-flat black micro-pile/velvet texture,
subtle contact shadows and minimal pile height. Do not invent floor by zooming out.
A small discreet LED panel sliver may remain near an extreme edge, without
assistant hands or arms. No dominant panels, extra props, people, logos or text.
```
Referencia de estilo aceptada: DSC00108_C_peluche_ligero_APROBADA. Versión vigente y enlaces en `registros/artefactos.json`. El piso lustroso/reflejante fue alternativa, no la elección actual. No reutilizar las máscaras Vision rechazadas del lote01.

## Restauración local de rostro, etiqueta y cabello — método ejecutado
- Ocho correcciones v03: siete rostros y una etiqueta. Leer `CORRECCION_LOCAL_V03.md`, `scripts/finalizar_correcciones_marcadas.py` y metadatos de `historial/correcciones_rostros_textos_v03/entrega_final/`.
- La autoridad de textura/identidad es el original. Registrar la toma sobre la edición con la matriz documentada; copiar solo la región aprobada y ajustar luz. Mantener fuera de máscara idéntico a la base PNG de la misma resolución. Una ampliación del fondo no crea detalle óptico.
- Etiqueta: usar la impresión real del envase fotografiado. Donante real DSC07722 donde corresponde; nunca cambiar a una versión de catálogo con otro idioma/diseño ni inventar letra quemada por reflejo.
- Cabello DSC07706v04: `scripts/restaurar_cabello_v04.py` y `historial/correccion_cabello_DSC07706_v04/AUDITORIA_CABELLO.json`. Se recuperó textura original en regiones de cabello, sin tocar el rostro aprobado. Regiones auditadas: cero cambios fuera de máscara y en cara protegida.
- `restaurar_originales_v03.py` incluye ensayos internos rechazados. NO es un motor genérico ni receta avalada para cualquier producto. Tampoco usar las pruebas locales de relleno lote16.
- Usar las rutas/donantes/matrices del manifiesto correspondiente, no asumir que un script de una foto aplica a otras. Preparar únicamente las fuentes autorizadas en el entorno de edición; GitHub no trae las fotos.

## Bebé — receta exacta ejecutada, sin prompt generativo
Fuentes aprobadas: DSC08258.JPG, DSC08290 2.JPG, DSC08295.JPG. Ver `scripts/editar_pruebas_bebe.py` y `historial/bebe/pruebas_v01/MANIFIESTO.json`.
1. Orientación EXIF y giro90grados antihorario registrado.
2. Ganancias RGB sRGB `[1.035,1.0,0.974]`, con acotación0–255.
3. Para cada canal resultante `v`: `v + 2.5*sin(pi*v/255) - 8*(v/255)**6`; redondear y acotar0–255.
4. Sin regeneración, suavizado, enfoque artificial ni sustitución entre fotografías. Se conservaron foco y texturas reales de captura; no se recuperó detalle óptico perdido.
5. Dos fotos tienen recorte lateral registrado de2.2% para retirar borde del cuarto; la primera conserva todo el cuadro. Es una decisión específica de estas versiones aceptadas, no licencia para amputar personas ni receta general de recorte.
6. PNG maestro y JPG calidad97, subsampling0. Comparar rasgos y etiquetas, verificar hash y bytes en nube.

Las tomas08261/08284 presentan movimiento o suavidad; no reemplazar ojos/expresiones por los de otra toma. Una composición multiframe requeriría compatibilidad real y revisión específica; NO se hizo ni se promete.

## Control antes de extender un lote
Validar cara, pelo, contorno, pose, manos, cantidad de productos, tipografía y sombras contra la fuente, no solo en contacto pequeño. Usar ampliaciones reales, no «mejorar» el screenshot. Si hay error, corregir antes de entregar y registrar el ensayo como interno; no contarlo como producción ni aprobación.
Registrar prompt REAL o versión/hash del script, fuentes y referencias, regiones, parámetros, archivo y hash, proveedor/modelo expuesto, coste reportado si existe, decisión y enlace estable. Si no se conoce cuota o coste, no inventarlo. La autorización de una suscripción no autoriza API de pago ni cambio de servicio con fotos privadas.
