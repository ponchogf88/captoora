# Regla posterior: rostro y producto reales

El usuario rechazo el efecto acuarela en siete rostros y una etiqueta, y autorizo expresamente restauracion local de pixeles desde originales, sin IA generativa. El resto de la fotografia no debe rehacerse. La regla de fidelidad de rostros/textos aplica a toda la produccion; no dar por auditadas las entregas anteriores.

Mapeo de capturas por registro geometrico de la misma imagen: DSC07706, DSC07724, DSC07731, DSC07732, DSC08471, DSC08479, DSC08484 (rostros); DSC07726 (etiqueta). El usuario ya habia seleccionado las personas; este proceso no identifica personas entre fotos distintas.

Metodo: conservar fondo v02, escalarlo tecnicamente al lienzo del original 4128x6192 o6192x4128; registrar la toma original con transformacion de similitud, copiar solo regiones locales, ajustar luz sin sintetizar detalles, guardar mascara y comprobar cero pixeles cambiados fuera de ella respecto a esa base. El fondo escalado no gana detalle optico. No reutilizar la segmentacion Vision rechazada.

La etiqueta de la misma impresion/envase en DSC07722 es una fuente fotografica mas legible para otras tomas de la misma secuencia; conservar fuente, region y transformacion. No transcribir letras adivinadas. DSC08479 conserva desenfoque ya presente en su fuente. El reflejo del envase borra parte de la letra fina; no declarar que quedo totalmente legible.

La entrega final cubre exactamente siete rostros marcados y una etiqueta: ocho fuentes distintas. Las pruebas extendidas de productos en trece fuentes se apartaron como INTERNAS_NO_ENTREGAR; no se avalaron y no deben reutilizarse como resultado. Estas son versiones, no nuevas fotos para el contador nocturno. No aprobarlas automaticamente. Antes de extender el procedimiento a entregas anteriores, presentar estas correcciones segun la puerta de revision por lotes del usuario. El resto de fuentes producidas conserva pendiente la auditoria de fidelidad de textos, aunque tenga aprobacion estetica previa.

Prompts generativos historicos se conservan como evidencia, no como recomendacion vigente para reconstruir caras o letras. Ninguna llamada nueva al generador se uso para estas correcciones locales.


Entrega autorizada para revision: correcciones_rostros_textos_v03/entrega_final. El script restaurar_originales_v03.py contiene pruebas internas; no es una receta general validada. finalizar_correcciones_marcadas.py restringe la entrega a las zonas de las capturas. Las mascaras numericas prueban alcance, no que un detalle ausente en fuente sea recuperable. La fidelidad general de lotes anteriores sigue pendiente; el usuario revisa las versiones concretas primero.

Lectura Drive confirma8JPG y8PNG maestros de entrega. Las13pruebas internas no son una entrega ni cuentan como nuevas. Registro799 conserva29aprobadas/110enrevision; contador nocturno100 sin incremento por estas versiones. Las comparativas visuales estan en Drive/local, no en git.
