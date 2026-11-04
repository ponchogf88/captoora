# Relevo a otro modelo

## Contrato de continuidad

No recrear las 799 fotos ni empezar desde cero. Leer primero la cola y las aprobaciones; preservar originales. No preguntar de nuevo por decisiones que ya están documentadas. El siguiente lote solicitado prioriza a la mujer de cabello largo, lacio y negro descrita por el usuario: confirmar visualmente la selección antes de gastar generación. El lote04 aún no se aprobó.

## Reanudar

1. Verificar acceso autenticado a las carpetas de Drive. Descargar/materializar únicamente la fuente que se editará si la herramienta lo requiere; respetar custodia de nube del repositorio.
2. Seleccionar archivos por nombre dentro de la persona/categoría elegida. Registrar los saltos como pendientes. No cambiar los nombres de las fuentes ni perder el orden maestro.
3. Usar el original como objetivo y una referencia aprobada como guía estética. Una prueba generada que cambió escala no sustituye al original de identidad.
4. Leer el prompt exacto de una toma comparable. Registrar el prompt adaptado realmente enviado, proveedor/modelo que el sistema sí exponga, fuente, referencias, fecha, salida y decisión. No etiquetar una plantilla reconstruida como ejecución histórica.
5. Editar una prueba y revisar cabello, cara, manos, productos, sombras y geometría a escala completa. Solo extender la producción cuando no haya fallos detectados; no pedir aprobación extra para pasos ya autorizados.
6. Producir el tamaño de lote autorizado; ahora diez. Mostrar salidas numeradas. Mantener `en_revision` hasta aceptación del usuario. Guardar en `aprobadas/JPG` solo después de aceptación expresa y verificar por lectura de Drive.
7. Actualizar este respaldo y comprobar el commit remoto. Un archivo local o un push iniciado no demuestra respaldo remoto.

## Cambiar de motor sin gastar a ciegas

Las suscripciones de ChatGPT, API y otros proveedores no son una cuota intercambiable. Este paquete no instala nada, no compra créditos, no activa API ni configura cargos. Elegir una herramienta disponible en la cuenta del usuario, leer su costo y límites reales y solicitar aprobación si exige un cargo. No transferir fotos a otro servicio sin autorización aplicable.

Capacidades necesarias: edición con imagen de entrada, conservación de sujeto y encuadre, idealmente máscara del fondo/protección del sujeto. Si se requieren píxeles idénticos de la persona, una generación libre no lo garantiza: usar un editor con selección protegida y verificarlo, sin volver al recorte automático defectuoso del lote01.

Hacer comparación fuente/salida alineada: rostro, proporciones, pose y pelo completos. Revisar frascos y letras legibles. Si el modelo altera identidad, cambiar la edición o declarar el bloqueo; nunca presentar variaciones como identidad preservada al 100%.

## Actualizar el respaldo

```sh
python3 scripts/preparar_respaldo.py --source /ruta/FARMASI_799 --dest .
python3 scripts/validar.py
```

El expediente fuente debe tener `produccion/REGISTRO_EDICION.json`, lectura de Drive actual y `PROMPTS_EJECUTADOS_RECUPERADOS.json`. Registrar primero los nuevos prompts; el script no los obtiene mágicamente de otra conversación. No conserva credenciales ni cuotas en caché. Confirmar diff y publicar solo la carpeta de este proyecto en la rama `farmasi/continuidad-edicion-799`; no modificar la web ni fusionar cambios ajenos.

Para ver las fuentes y descargar fotografías se requieren permisos de Drive, aunque el código se pueda leer. Un relevo sin acceso a los archivos está bloqueado: no reconstruir fotografías de memoria.
