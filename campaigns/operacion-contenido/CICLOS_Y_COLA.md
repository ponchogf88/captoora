# Ciclos de cinco horas y operación por cuotas

## Estado real
Existe un heartbeat horario `producci-n-captoora-likinya` en este hilo. Despierta al agente; no garantiza cinco horas de ejecución continua, máquina despierta ni conectores disponibles. Esta guía define la cola; no instala un daemon ni declara una integración que no existe.

## Ventana de trabajo propuesta de cinco horas
- Inicio: consultar cola y trabajos ya enviados; validar cuenta, saldo, reinicio, espacio y fuentes. Reservar tareas útiles para la cuota que vence primero.
- Hora 0–1: cerrar guiones y selección, voz maestra, primeros recursos; comenzar con piloto revisable y solicitudes pequeñas.
- Hora 1–3: seguir generaciones verificadas; mientras esperan, editar, seleccionar, investigar o preparar derivados independientes. No quedarse solo registrando saldos si hay trabajo autorizado viable.
- Hora 3–4: montaje y subtítulos, revisión de errores y recursos faltantes; ajustar volumen por éxitos/fallos reales.
- Hora 4–5: revisar, descargar y respaldar resultados; reconciliar créditos y dejar siguiente cola lista. No iniciar volumen que no se pueda revisar/recuperar.
- Reinicio: medir saldo anterior/nuevo; reactivar trabajos pendientes solo si hay autorización vigente y acceso. Las ventanas de 5 h, semana y mes pertenecen a cada proveedor y no se sincronizan por suposición.

## Programador de prioridades
1. Ejecutables sin bloqueo, con resultado útil y fuente válida.
2. Cuota incluida con vencimiento más cercano; estimación disponible y coste real medido.
3. Dependencias que desbloquean varias publicaciones (maestro voz, referencias, plantilla, selección de álbum).
4. Calidad y entrega: no sacrificar por llenar terabytes o consumir tokens.

### Guardia obligatoria antes de utilizar Flow

- No generar imágenes estáticas en Flow.
- Seleccionar primero una imagen autorizada de biblioteca propia, Canva o Pexels. Pinterest
  requiere verificación de derechos para utilizarse como fuente; de otro modo es referencia.
- Flow solo anima una imagen aprobada mediante movimiento real definido en el brief.
- No gastar cuota por vencimiento si el recurso no tiene uso editorial concreto.
- Un zoom sobre una imagen no cuenta como video y se rechaza antes del montaje.
- Títulos y subtítulos dinámicos se terminan en Canva, Captions, OpusClip o CapCut; FFmpeg no
  sustituye ese acabado.

Si una cuenta queda bloqueada, pasar a otra dependencia autorizada; no repetir login ni notificar cada hora lo mismo. No consumir cuotas de cuenta distinta de la solicitada. No cambiar voz/identidad.

## Ficha mínima de cola
ID, pilar, tema, módulo/pieza, referencia, originalidad, cuenta, modelo, duración/formato, prompt/guion, dependencias, coste cotizado, estado, ID proveedor, archivo/hash/bytes, revisión, saldo antes/después, reinicio, fecha y URL de publicación solo si ocurre. Desconocido = null.

## Capacidad y metas
100 piezas semanales es una meta a medir. Estimar con tres trabajos válidos por familia y tiempo activo/espera/revisión diferenciados. Capacidad final limitada por el cuello de botella de guion, acceso, generación, edición o revisión; no inferir piezas terminadas a partir de saldo de imágenes. Informar insumos y piezas finales separados.

## Referencias operativas
- ../likinya/consolidado-2026-10-23/README.md
- ../likinya/consolidado-2026-10-23/reporte.json y cuotas.json: snapshot histórico, no saldo vivo.
- ../likinya/consolidado-2026-10-23/plan-9-dias/: ejemplo de 90 publicaciones, ampliable.
- ../likinya/consolidado-2026-10-23/consolidado-repositorio/PLAN_ACCION_OTONO_INVIERNO_2026_2027.md
- SECRET_REFERENCES.md: ubicación declarada de secretos, sin valores.

## Bloqueos actuales preservados
Espera de lista de suscripciones; falta de espacio local; CapCut devolvió planes después de dos aprobaciones sin render; inventario Andrea incompleto; cinco nombres de marcas y álbumes por cotejar. No borrar estos bloqueos porque existe esta guía.
