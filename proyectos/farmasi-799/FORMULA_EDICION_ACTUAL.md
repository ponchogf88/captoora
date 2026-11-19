# Fórmula real de edición FARMASI

Actualización: 5 de noviembre de 2026. Documento de continuidad solicitado por el usuario. Describe lo ejecutado, no garantiza aprobación estética ni autoriza producción nueva.

## Entradas y orden de trabajo

1. Localizar la fotografía original mediante `registros/fuentes_799.json`. Identificar versión y orientación antes de editar. Mantener el original intacto.
2. Abrir la referencia de estilo aprobada de la misma sesión. Para el acabado blanco D: `DSC07738_pared_D_sombra_v05`. Conservar textura tenue, sombras suaves y piso de peluche real; no convertir el fondo en blanco plano de catálogo.
3. Registrar las zonas autorizadas. Rostro, expresión, cabello, dimensiones, pose, manos, ropa, productos y letras deben conservar la información original. No inventar detalle ausente ni sustituir etiquetas por texto sintetizado.
4. Si se necesita limpiar el set con generación, usar el resultado como material intermedio del entorno. Un prompt de preservación no garantiza que el motor respete la identidad. Recuperar los sujetos desde el original y comparar a tamaño completo.
5. Revisar la unión del fondo. Las primeras composiciones del cobrizo dejaron diferencias frías y claras alrededor del cuerpo; ese defecto motivó la corrección `blancos_v03` descrita abajo. No copiar ese defecto al siguiente lote.
6. Exportar PNG para comprobación de píxeles y JPG para revisión. Registrar fuente, versión, hash, bytes, destino y estado. Subida o corrección no equivalen a aprobación.

## Mapa de recetas y prompts ejecutados

| Etapa | Archivo de referencia en este paquete | Alcance real |
| --- | --- | --- |
| Prompts históricos | [Biblioteca JSON](prompts/ejecutados_exactos.json) | Historial; incluye intentos identificados sin salida. No ejecutar en bloque como receta actual. |
| Limpieza nativa del cobrizo | [Seis prompts exactos](historial/cobrizo_sola_6/PROMPTS_EJECUTADOS.json) | Seis generaciones intermedias, una por fuente. No atribuir modelo específico no expuesto por la herramienta. |
| Recuperación del sujeto original | [Script ejecutado](historial/cobrizo_sola_6/restaurar_sujeto.py) | Alineación del fondo y composición con píxeles originales. Máscaras específicas, no universales. Produjo las bases v02 con el defecto de blancos después señalado. |
| Acabado D sobre bases existentes | [Script D](historial/modelo_D_todas/produccion_acabado_D.py) | Textura de fondo real y sombras suaves. No es el método para corregir los halos de cobrizo. |
| Unión de blancos v03 | [Código exacto ejecutado](historial/correccion_blancos_v03/corregir.py) | Corrección local no generativa de cuatro fondos. |
| Auditoría de blancos | [Manifiesto](historial/correccion_blancos_v03/MANIFIESTO.json) y [Drive](historial/correccion_blancos_v03/DRIVE_VERIFICADO.json) | Hashes, bytes, versión y metadatos comprobados. |

No hay un único prompt que produzca todo el acabado. El trabajo combina material de entorno, composición desde originales y correcciones locales. Las últimas cuatro correcciones de blancos no consumieron una nueva generación. El coste de las seis generaciones anteriores no fue medido por una herramienta de facturación; no declararlo cero.

## Recuperación del sujeto: parámetros efectivamente usados

El script `restaurar_sujeto.py` documenta las seis fuentes: DSC08318, DSC08500, DSC08504, DSC08536, DSC08540 y DSC08554.

- Orientar el original con EXIF y la orientación registrada; conservar sus dimensiones.
- Trabajar para la medición con altura de 1500 píxeles y ancho proporcional.
- SIFT con hasta 6000 características; correspondencias con razón menor que 0.72.
- `estimateAffinePartial2D`, RANSAC y tolerancia de 4 píxeles. Se alinea el material generado hacia el original, no se deforma el original para ajustarlo a la generación.
- Máscaras cromáticas, regiones por imagen, soporte del cabello y transición por distancia están escritos literalmente en el código. No reutilizar las cajas en otra pose ni tratarlas como segmentación verificada de toda la persona.
- En el núcleo protegido, copiar los píxeles del original. Las zonas periféricas se mezclan. La aserción verifica el núcleo calculado: no demuestra por sí sola que todos los cabellos, zonas transparentes o bordes humanos estén correctamente incluidos.
- Solo DSC08318 recibió después una ganancia fotométrica de 1.25. El usuario pidió igualar aún más su iluminación y revisar el rostro; ese pendiente no se resuelve con la corrección de blancos de las otras cuatro.

## Fórmula de corrección de blancos v03

Fuentes afectadas exclusivamente: **DSC08500, DSC08504, DSC08536 y DSC08554**. Entrada: PNG de composición v02; referencia de entorno: la generación correspondiente alineada mediante la matriz ya registrada. No se generaron caras, prendas ni fondos nuevos en esta etapa.

Sea `A` la composición v02, `B` el fondo de referencia alineado y `G32` un desenfoque gaussiano de sigma 32. Los cálculos siguientes se hacen en RGB de 8 bits convertido a float, a altura 1500; no es un ajuste de exposición en espacio lineal.

### Protección y muestras

- Proteger píxeles cálidos: `(R-G > 7) AND (R-B > 12)`.
- Proteger también píxeles oscuros: `min(R,G,B) < 125`.
- `S` es la unión de esas protecciones.
- **No dilatar S.** Un ensayo con dilatación 9×9 produjo un contorno blanco y se retiró antes de la entrega.
- Una muestra de fondo `W=1` requiere: fuera de S; mínimo de A mayor que 125; rango de canales de A menor que 45; mínimo de B mayor que 150; rango de canales de B menor que 45. En otro caso W=0.

### Campo de corrección

Para cada canal `c`:

```text
D[c] = G32((B[c] - A[c]) * W) / max(G32(W), 0.001)
D[c] = limitar(D[c], -28, +28)
T = G1(1 - S)
T[S] = 0
```

Subir `D` y `T` a las dimensiones originales mediante interpolación. Subir S con vecino más próximo.

```text
salida = limitar(redondear(original_v02 + D * T), 0, 255)
salida[S] = original_v02[S]
```

Así se corrige el cambio amplio de color y luminosidad del fondo sin desenfocar directamente la imagen. Se conserva el detalle de alta frecuencia; la luminosidad de las sombras amplias puede variar. Comparar visualmente las sombras, no afirmar que todo el fondo quedó idéntico.

### Exportación y comprobación

- PNG a dimensiones de la base; comprobar igualdad exacta dentro de la máscara protegida.
- JPG con calidad 97 y submuestreo 0. La compresión JPG puede modificar píxeles; la prueba de igualdad corresponde al PNG previo, no al JPG.
- Previsualización máxima 700×1050, calidad 95. No usarla como nueva fuente.
- Registrar SHA-256 de la base y del JPG, tamaño en bytes y metadatos de Drive.
- Las cuatro entregas actualizaron los mismos IDs de JPG en Drive, con nombre `*_blancos_v03.jpg`, para evitar archivos repetidos.

## Reproducibilidad y límites

Los scripts históricos esperan la estructura de trabajo y manifiestos usados en la sesión. **No son ejecutables autónomos desde un clon vacío.** `GENERACIONES.json`, originales y PNG base son entradas de trabajo; GitHub contiene las recetas y registros, no las fotografías. Preparar las entradas autorizadas en el entorno de edición y adaptar las rutas de forma explícita antes de ejecutar. No volver a generar una referencia faltante como si fuera la original.

La protección por color funciona como heurística para este vestido cobrizo y estas imágenes; no garantiza protección en prendas blancas, piel quemada, transparencias o nuevos fondos. Si se cambia de sujeto o vestuario, preparar y revisar una máscara nueva. Comprobar rostro, cabello, dedos, contornos, cola y etiquetas frente al original antes de ampliar la producción.

La prueba de cero cambios protegidos NO equivale a «cero cambios en cada píxel del sujeto» fuera de esa máscara. No prometer recuperación de detalle que la fuente perdió por desenfoque, movimiento o exposición.

## Estado al guardar esta fórmula

Las cuatro correcciones de blancos están **en revisión**, no aprobadas automáticamente: [carpeta Drive](https://drive.google.com/drive/folders/13vIl4Xt_R3YIIxkXbqgiSIia1ZL9cjsb).

Siguen pendientes independientes, sin declararlos resueltos por este ajuste:

- DSC08318: revisión de rostro e igualar iluminación/color con las demás.
- DSC08500: revisión de rostro.
- DSC08536 y DSC08540: vuelo natural del velo.
- Resto de producción y montajes madre/bebé: conservar los requisitos anteriores y su orden; esta solicitud solo pide documentar la fórmula.

Los registros `registros/fuentes_799.json` y `registros/artefactos.json` son la autoridad de inventario. Las cifras antiguas en notas históricas no son un estado actual.
