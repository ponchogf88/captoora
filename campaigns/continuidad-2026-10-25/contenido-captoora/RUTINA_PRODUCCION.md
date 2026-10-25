# Rutina ejecutable de producción CAPTOORA

Automatización: producci-n-captoora-likinya, cada hora en este hilo. Esto es un despertador de trabajo del agente, no una integración automática de todas las aplicaciones. Requiere que el entorno programado pueda ejecutar las herramientas y acceder a las cuentas.

## En cada ejecución

1. Leer REQUISITOS.md y reporte.json. Consultar estado de trabajos enviados antes de iniciar otros. No duplicar generación ante respuesta incierta.
2. Actualizar cuotas.json con saldo, unidad, fecha de consulta y reinicio por servicio que permita consulta. Desconocido permanece null, no 0. Nunca convertir créditos a tokens ni mezclar planes web y API.
3. Priorizar cuotas que vencen antes: primero producir una pieza revisable, luego ampliar lotes distintos según saldo y tarifa comprobados. Intentar aprovechar todo el saldo incluido útil; no activar sobreconsumo o compras. Si el proveedor no expone tarifa ni saldo, documentarlo antes de prometer cobertura.
4. Ejecutar `python3 producir_lote.py` desde este directorio para preparar clips de apoyo reales de archivos locales autorizados. El ejecutor no consume cuotas de IA. Puede ejecutarse otra vez sin regenerar archivos ya comprobados. No producir relleno ni estirar videos para aumentar bytes.
5. Continuar las piezas de PRODUCCION_LIKINYA.md: localizar maestros ISO/enfoque, obtener voz ElevenLabs, animar solo apertura/cierre con el avatar identificado, montar y verificar. No cambiar de voz sin resolver elección.
6. Si un login bloquea una herramienta, avanzar dependencias independientes. Registrar exactamente el bloqueo y avisar solo cuando necesite intervención o cambie el estado. No afirmar producción en segundo plano sin proceso o tarea real.
7. Guardar manifest y reporte: archivos nuevos, duración, bytes, IDs de proveedores, cuotas antes/después y límites de medición. Reportar cero consumo cuando sea lo medido, incluso si el usuario pidió agotar cuotas.

## Reportes por reinicio

Cuando haya pasado un reinicio conocido, registrar último saldo medido y saldo nuevo. Solo afirmar cuota utilizada = asignación - saldo si se conoce asignación, no hubo recargas y ambos corresponden al mismo periodo. Si falta medición previa al reinicio, marcar consumo no verificable; no declarar 100%.

## Destino y volumen

Salida inicial: clips/ en este directorio. Mantener al menos 8 GiB libres y detener lotes locales si no hay espacio. Destino Drive verificado: carpeta CAPTOORA 1dTwGiUNZ-8Km3MSb5edYdWHPx6_kGE0R. Capacidad libre de nube no medida: verificar antes de transferencias masivas. No subir material a otra cuenta por suposición.

## Accesos conocidos

HeyGen: conexión consultable, 1051 créditos premium comprobados el 2026-10-21 04:30 UTC; reinicio indicado 2026-10-24T02:48:46Z. Avatar privado mostrado como Photo Avatar, personaje confirmado por usuario; nombre Pharmacy Girl aún sin correspondencia por nombre. ElevenLabs: sesión operativa previamente comprobada; voz Liza - Natural Mexican Creator utilizada en piloto; último saldo 33948, pendiente de consulta nueva. No sustituir voz sin resolver elección. Resto: suscripciones declaradas, no integración ni saldo comprobados. Page Agent, Browser Use, Video Use y Browser Flow fueron solicitados; no se encontraron herramientas expuestas con esos nombres ni binarios page-agent/browser-use/browser-flow en PATH durante revisión. Usar capacidades realmente disponibles; no instalar por suposición.

Evoto/Pixieset conservan papel de fotografía/entrega, sin forzar consumo para videos. No enviar mensajes ni publicar redes automáticamente; usuario autorizó generación y almacenamiento, no una publicación específica.

## Prioridad vigente: organización CSV
Leer PLAN_EPISODIOS_CAPTOORA.csv, PLAN_RECURSOS_CAPTOORA.csv y lote_yare.json. Petición más reciente: planear antes de escalar; no lanzar lotes nuevos durante revisión del plan. Automatización actualizada para conservar esta prioridad. Una imagen Nano Banana descargada (626223 bytes), resto 47 recursos planificados. Saldo Yare posterior a imagen individual aún no recertificado. No confundir saldo 1050 medido tras lote fallido con medición posterior al éxito individual.

## Prioridad vigente: gift cards solicitadas
La petición humana posterior autoriza cuatro gift cards Biometrics (dos hombres y dos mujeres adultos atléticos) y diseños Signature con mujeres maduras elegantes, personales/editoriales. Esta prioridad supera la espera general para este encargo concreto. Consultar gift_cards_estado.json: preparación Canva abierta, sin diseño generado; continuar generación solo tras interacción válida con el widget, sin repetir preparación. No inventar logos, valores, vigencias ni condiciones. La reserva local de 8 GiB no bloquea el diseño en Canva en nube. Mantener la revisión de suscripciones pendiente para el resto del inventario.
