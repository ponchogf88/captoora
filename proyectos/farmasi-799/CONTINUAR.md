# Continuar FARMASI 799 — instrucciones vigentes

Actualizado 5 noviembre 2026. Este documento sustituye la antigua guía nocturna. La entrada canónica estará en `main`: `FARMASI_799_CONTINUAR_AQUI.md`. La rama `farmasi/continuidad-edicion-799` conserva el respaldo de trabajo.

## Antes de editar
1. Leer `ESTADO_ACTUAL.md`, `registros/fuentes_799.json`, `DIRECCION_Y_CALIDAD.md`, `prompts/RECETAS_VIGENTES.md` y `BITACORA_FARMASI_799.md`.
2. Confirmar acceso a Drive. Los JPG/PNG NO están en GitHub. Usar `source_id/source_url`, nunca reconstruir una fotografía de memoria. No descargar el rollo completo por comodidad.
3. Consultar `estado` y `version_actual`: una aprobación histórica o el nombre de una carpeta no sustituye el registro actual. No repetir fuentes aprobadas ni trabajos reservados.
4. La prioridad actual es la modelo del conjunto lila y cabello negro largo, referencia DSC07706 v04. Diez individuales corregidas lila_v03 estan en revision, no aprobadas. V02 fue RECHAZADA por empalmes laterales; no repetir ni entregar su fondo de franjas. Corregir usando expediente correccion_v03 y preservar las zonas faciales/cuerpo aceptadas, etiquetas originales. No repetirlas ni las diez previamente aprobadas. 7752/7753/7756 tienen productos ocluidos por dedos del fotografo; 7759 es JPEG fuente corrupto confirmado dos veces. Ver historial/modelo_lila_cabello_largo/ESTADO.json. Hay 24 candidatas de vestido cobrizo inspeccionadas sin editar, y grupos posteriores aun no inventariados exhaustivamente. El bebe queda como pendiente anterior, no cancelado. El chat compartido 6aec4bd5-9504-83e8-81b4-132778368d8b se leyo usando Chrome autenticado: tras terminar la modelo lila, preparar montajes madre+bebe mirando ambos a camara mediante recortes de originales compatibles, sin generar ni modificar rostros.16 referencias cruzadas con los IDs del inventario. Ver historial/bebe/MONTAJES_MADRE_BEBE_REQUISITOS.json. Respuestas del otro asistente no cargan; mensajes del usuario si. No pedir al usuario repetirlos.
5. La petición anterior de veinte fotos diversas sigue sin completar: las pruebas de relleno poligonal de lote16 fueron rechazadas internamente, no entregadas ni aprobadas. No usarlas. Las fuentes deben revalidarse contra el registro antes de continuar.

## Eleccion de pared pendiente
Se agrega una cuarta variante D sobreB: sombra suave de ella proyectada en pared, segun nueva solicitud. A/B/C conservadas. Todas pendientes de eleccion; no aprobadas ni aplicadas a otras fotos. Ver MANIFIESTO_VERSION_D.json ycrear_version_D_sombra.py enel mismo historial.
Tres variantes A/B/C sobre la misma DSC07738, no tres fuentes nuevas. Usuario acepta piso/sombras inferiores y solicita pared con relieve/textura sutil recuperada de fondo original: no plana, ni tela/arrugas evidentes. A tenue,B sombras mas presentes,C leve calidez. No aplicar al lote sin eleccion. Modelo/productos/piso preservados; cero nuevas generaciones. Ver historial/modelo_lila_cabello_largo/pruebas_textura_pared. Enlace de revision: https://drive.google.com/drive/folders/1W-0oV8CK0NS5g4FY4EznLcDZIsqNwYtU .

## Qué usar para producir
- `prompts/ejecutados_exactos.json`: 150 prompts enviados realmente; no modificarlos ni confundirlos con una receta vigente. Su versión legible está en `prompts/EJECUTADOS_EXACTOS.md`.
- `prompts/RECETAS_VIGENTES.md`: requisitos actuales, plantillas NO ejecutadas, referencias aprobadas y métodos locales reales.
- Las últimas correcciones de cara, etiqueta, cabello y bebé NO se generaron con un prompt de imagen. Fueron edición local desde originales. Reproducir el script y los parámetros correspondientes, no regenerar al sujeto.
- Los scripts de `scripts/` son verificadores, registradores y recetas específicas. No existe un motor universal de generación masiva listo para ejecutar con una API. Los scripts copiados de correcciones puntuales pueden requerir preparar las rutas/archivos fuente según sus manifiestos; no ejecutarlos a ciegas desde la raíz.

## Puerta de calidad obligatoria
Preservar rasgos, expresión, pose, pelo, manos y productos. No regenerar caras ni textos; no inventar detalle borroso o quemado. Para cambiar un fondo, el editor debe proteger de verdad al sujeto y los envases. Si el motor no admite esa protección, detener ese método y registrar la limitación: un prompt por sí solo no garantiza identidad.
Comparar cada fuente y salida a resolución suficiente. No usar recorte Vision rechazado ni rellenos poligonales que invadan al sujeto. Para el montaje madre+bebe expresamente autorizado, usar solo recortes de tomas originales compatibles, sin sintetizar expresiones; mostrar donantes y resultado. Las zonas del set que no puedan limpiarse con fidelidad quedan pendientes; no resolverlas pintando sobre personas.

## Lotes, aprobación y versiones
Trabajar en los lotes autorizados por el usuario. Mostrar pruebas antes de extender un método que cambie. Una salida nueva va a revisión: las aprobaciones globales anteriores no aprueban imágenes futuras.
`aprobadas/JPG` y `aprobadas` (PNG) contienen UNA sola última versión expresamente aprobada por fuente y formato. Las versiones anteriores se mueven al historial FUERA de aprobadas; no borrarlas ni exhibirlas como entregas duplicadas. DSC07706 vigente: v04.
Después de una entrega/aprobación: verificar nombres, ID, padre y bytes en Drive; registrar archivo, fuente, referencia, método/prompt exacto, versión, hashes y estado. No confundir exportar, subir y aprobar.

## Revisión y respaldo
Ejecutar `python3 scripts/validar.py` y `python3 scripts/revisar_relevo.py` desde este paquete: no editan fotos ni consumen API.
`preparar_respaldo.py` reconstruye registros desde un expediente operativo existente; no descarga fuentes ni genera fotos. La réplica de Git debe incluir la documentación actual en `main`, no quedarse solo en la rama de continuidad. Ver `SINCRONIZAR_GITHUB.md`.
La programación nocturna del 4 noviembre era una autorización acotada hasta las10:00, no una orden vigente para reactivar horarios pasados. No crear/reactivar automatizaciones, comprar, instalar, cambiar proveedor con coste ni usar API de pago sin autorización aplicable.


## Actualizacion prioritaria
Leer ESTADO_MODELO_D_TODAS.md antes de continuar.29 nuevos D en revision;75 cobrizo pendientes y4 incidencias lila. ReferenciaDaprobada.

### Cobrizo SOLA:6 nuevas
6 individuales entregadas en revision;69 cobrizo restantes. Fuentes8318,8500,8504,8536,8540,8554. Dos individuales adicionales NO localizadas; no contar recortes grupales.6generaciones nativas intermedias, sujeto recompuesto desde originales; PNGconserva pixeles protegidos (8318 ganancia1.25),JPGcompresion. Prompts exactos y metodo en historial/cobrizo_sola_6. No aprobacion automatica. Drive:https://drive.google.com/drive/folders/1Y7-si0Zkhxiqi0vf8f-u98B7XPohWWwv

### Correccion de blancos solicitada:solo4
DSC08500/8504/8536/8554:blancos_v03,solo fondo neutro,misma pose/rostro/vestido.4 JPG actualizados sin duplicar IDs y movidos a revision conjunta:https://drive.google.com/drive/folders/13vIl4Xt_R3YIIxkXbqgiSIia1ZL9cjsb. Las dos aprobadas v02 afectadas se retiraron de aprobadas;PNG historicos fuera de entrega.146 previas vuelven a144 aprobadas por correccion solicitada. No nuevas generaciones. Rostros/velo anteriores siguen pendientes;ultima instruccion pide exclusivamente blancos antes de siguiente tarea. Receta/auditoria en historial/correccion_blancos_v03.
