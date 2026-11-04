# FARMASI · continuidad de edición de 799 fotografías

Respaldo privado del proyecto de sesión del 31 de octubre. Fecha de corte de este paquete: 4 de noviembre de 2026, hora Ciudad de México. No es publicación ni entrega al cliente.

## Empezar aquí

1. Leer [CONTINUAR.md](CONTINUAR.md), [DIRECCION_Y_CALIDAD.md](DIRECCION_Y_CALIDAD.md) y el registro de requisitos.
2. Consultar `registros/fuentes_799.json`, `registros/artefactos.json` y `prompts/ejecutados_exactos.json`.
3. Abrir las referencias aceptadas en Drive antes de editar. El prompt solo no sustituye la referencia visual.

## Estado comprobado

- 799 fuentes JPG inventariadas con ID y enlace de Drive.
- 29 JPG aprobados y verificados en Drive.
- 50 JPG nuevos o anteriores en revisión; no aprobados automáticamente.
- 83 prompts exactos recuperados; incluyen intentos bloqueados sin imagen cuando están identificados así.
- 117 originales inspeccionados con SHA-256; no afirmar que los 799 tengan hash comprobado.
- 3 fuentes bloqueadas por herramienta; no cuentan como producción.
- Lote01 de veinte: rechazado por cabello y contornos. No reutilizar sus máscaras.
- Ver `operacion_nocturna/PLAN_NOCTURNO.json` para el contador de hasta200 nuevas, calendario y reservas activas.

El registro distingue fuente, versión, aceptación y archivo verificado. Los campos históricos de rechazo no invalidan una versión posterior aprobada. `historial/` conserva fotografías documentales de registros anteriores; no es la cola vigente.

## Archivos fotográficos en la nube

- [Originales 799](https://drive.google.com/drive/folders/1fnUJljKnCMEuGlozJg8wxVTEDnWAI9lv).
- [Aprobadas JPG](https://drive.google.com/drive/folders/1O70rKDMLZfC9d_eY-0Ugh7MAl-iZuw11).
- [Aprobadas PNG / referencias](https://drive.google.com/drive/folders/1nHp9UEYFBFMngGT6QRldBGlsxKqRzAG-).
- [Lote05: siete en revisión](https://drive.google.com/drive/folders/1hvuKsanvCMWXAG99H8-HSP1SI7OOqoEq).
- [Diez grupales nocturnas en revisión](https://drive.google.com/drive/folders/1rcBPhUIC6Ha4QontlUBxk4r6dwlZ_hEl).
- [Diez individuales nocturnas en revisión](https://drive.google.com/drive/folders/1VkBJUZkKarh55p0LZfI8I5JCirArnZsI).
- [Lote04 en revisión](https://drive.google.com/drive/folders/1RmnlaNjOJt8HFcZ0sSvx1ca-eprV-T66).

GitHub respalda instrucciones, recetas, enlaces, hashes y decisiones. No contiene los JPG/PNG ni los 799 originales, conforme a la custodia del repositorio. Drive requiere acceso a la cuenta autorizada. No contiene claves ni enlaces temporales de descarga. No hay entrega Pixieset verificada para este proyecto.

## Qué produce la calidad

Edición sobre la foto exacta; bloqueo de identidad, pose y escala; instrucciones locales de limpieza; profundidad y sombras conservadas; contraluz natural en el cabello; elección visual del usuario; revisión contra la fuente y control de versiones. No existe un ajuste secreto ni una garantía de reproducción idéntica.

Las llamadas actuales usan `image_gen` integrado. El identificador del modelo no se expone: no se atribuye GPT Image 2 a estas salidas. No hay seed, máscara generativa ni parámetros de fidelidad registrados que puedan inventarse. Las salidas recientes son de resolución generada, frecuentemente 1024×1536; no equivalen al archivo de sensor de 24 MP. Otro proveedor puede producir cambios de identidad o microtexto incluso con el mismo prompt.

## Actualización

Después de cada lote o aprobación, actualizar manifiestos, prompts exactos y lectura de Drive; ejecutar el validador y crear un nuevo commit. No hay programación automática ni llamadas de generación al abrir este paquete. El usuario canceló las automatizaciones para ahorrar cuota.

`scripts/preparar_respaldo.py --source /ruta/FARMASI_799 --dest /ruta/de/este/paquete` reconstruye los registros desde el expediente operativo; no edita imágenes, no cobra y no sube archivos. La sincronización git es una acción separada y verificable. Ver [CONTINUAR.md](CONTINUAR.md).
