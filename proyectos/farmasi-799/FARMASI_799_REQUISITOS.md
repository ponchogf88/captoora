# Farmasi 799 — registro de requisitos

Fecha: 2026-11-03. Fuente: solicitud del usuario en Proyecto FOTOGRAFIA.

| Requisito | Estado | Destino / evidencia pendiente |
|---|---|---|
| Plan de edición de 799 JPG de la sesión del 31 de octubre | implemented | PLAN_FARMASI_799.md |
| Localizar carpeta exacta en Google Drive dentro de Captura | verified | FARMASI_799_SELECCION_JPG, ID 1fnUJljKnCMEuGlozJg8wxVTEDnWAI9lv |
| Confirmar cantidad real y listar archivos | blocked | Depende de acceso a carpeta exacta; 799 es cantidad declarada |
| Eliminar set casero de fotografías de fondo blanco | requested | Ruta blanca del plan; prueba pendiente |
| Resolver también fotografías de fondo negro | requested | Ruta negra del plan; prueba pendiente |
| Usar acabado anterior como referencia | requested | Carpetas anteriores localizadas; comparación visual pendiente |
| Preservar originales y correspondencia de nombres | implemented | Requisito del flujo propuesto; aún no se modifican fotografías |
| Aprobar muestra antes de extender el acabado | requested | Piloto de 9 imágenes propuesto |

Auditoría: plan entregado; cero fotografías inspeccionadas de esta sesión, editadas, aprobadas o subidas. No hay coste ni plazo confirmado.

Actualización autorizada 2026-11-03: el piloto cambia a NUEVE fotografías distintas: 3 individuales de fondo blanco, 3 individuales de fondo negro y 3 grupales. Preparar ediciones cuando estén disponibles y mostrar originales junto a resultados para aprobación. No extender al resto sin aprobación. Ejecución y entrega pendientes.

Primera revisión 2026-11-03 15:04: carpeta localizada https://drive.google.com/drive/folders/1fnUJljKnCMEuGlozJg8wxVTEDnWAI9lv ; 367 JPG únicos durante paginación de subida. Doce originales descargados e inspeccionados en hoja de contacto. Piloto todavía pendiente. Usuario informó 365/799.

Segunda revisión ejecutada a las 15:08 (un minuto después de las 15:07 programadas): 457 imágenes visibles durante la paginación. Subida en curso, total 799 todavía no verificado. Ninguna edición iniciada todavía.

Piloto: 9 solicitudes al editor integrado, 8 resultados PNG guardados aparte y 1 bloqueado por moderación de salida (DSC01197.JPG). Comparativas en entregables/FARMASI_799/piloto/comparacion_{blanco,negro,grupo}.png. Revisión: hay cambios de encuadre, orientación lateral en archivos y diferencias en sujetos/productos en grupos; no se verifica fidelidad suficiente para producción. No aprobados. Ninguna de las demás 790 fotografías editada. Originales preservados con manifiesto SHA256. Selección blanca representativa tomada de archivos accesibles, no certificada como las tres primeras del inventario definitivo.

## Correcciones solicitadas por usuario — 2026-11-03, versión 02
Fuente: mensaje actual del usuario. Autoridad: originales del piloto, no versiones generadas.

| Requisito explícito | Estado | Destino / verificación |
|---|---|---|
| Negro con baño de luz ámbar/anaranjado/amarillo elegante, sin rayo definido | requested | prueba negra v02 |
| Negro con gradación y sombras muy sutiles, sin plano uniforme | requested | prueba negra v02 |
| Blanco con una o dos sombras originales cálidas, profundidad y esquinas algo más oscuras | requested | prueba blanca v02 |
| Conservar alfombra blanca de peluche y sus texturas | requested | blancas y grupal v02 |
| Quitar solo elementos ajenos al set; conservar carácter de estudio | requested | cuatro pruebas v02 |
| Mantener piel natural del acabado que gustó, identidad, pose, ropa y productos | requested | revisión de sujetos v02 |
| Entregar prueba pendiente de mujer de pelo chino DSC01197.JPG | requested | prueba individual v02; antecedente de bloqueo del editor |
| Grupal dreamy con peluche extendido a laterales y bordes suavemente difuminados | requested | prueba grupal v02 |
| Mostrar pruebas antes de continuar resto | requested | cuatro pruebas representativas v02, piloto completo de nueve sigue abierto |

No se ha localizado referencia anterior exacta de luz naranja; interpretación inicial basada en descripción actual. No afirmar coincidencia comprobada.

V02 ejecutada con editor integrado: cuatro PNG guardados e inspeccionados (negra DSC00001; blanca DSC01863; pelo chino DSC01197; grupal DSC02415). Sombras, alfombra y calidez implementadas como pruebas visuales. Originales intactos. Primera blanca bloqueada por filtro automático; corrección posterior sobre v01 y referencia original sí generada. Etiqueta del frasco individual requirió corrección separada. Persisten límites de fidelidad generativa en microtexto, productos grupales e identidad; muestras para dirección visual, no archivos finales aprobados ni autorización del lote. La comparación exacta con referencia naranja anterior sigue pendiente por falta de referencia accesible. Piloto completo de nueve sigue abierto.

## Aprobación y ajuste — nueva instrucción del usuario
Fuente: mensaje posterior a las cuatro pruebas v02.
- verified: usuario aprueba el estilo de blancas y grupales v02. Aprobación estética no confirma microtexto/productos ni todos los archivos del lote.
- requested: continuar únicamente pruebas de fondos negros en esta etapa.
- requested: reducir intensidad de luz ámbar 35–40%; aplicar 40% de reducción respecto a v02.
- requested: conservar rostro e identidad original; sin perfilado, embellecimiento, afinamiento, cambio de facciones o remodelado.
- requested: generar más pruebas negras; usar tres originales DSC00001, DSC00002 y DSC00003 del piloto, sin extender al lote.
- requested: conservar sombras y profundidad sutiles del negro aprobado.
Destino: piloto/negros_v03; originales como autoridad para rasgos, luz v02 como referencia estética únicamente.

Negros v03: tres pruebas generadas y revisadas visualmente, guardadas aparte. Ámbar visiblemente más tenue; reducción 40% es objetivo visual solicitado, no porcentaje medido. Persisten diferencias generativas en rostro/encuadre y pastel; conservación idéntica de rasgos no verificada. No afirmar que rostro está intacto. Pendiente revisión del usuario y método que preserve píxeles si no satisface identidad. Blancos y grupales aprobados estéticamente se mantienen sin cambios.

## Nueva corrección explícita: tres personas diferentes
Fuente: último mensaje usuario. Sustituye selección de tres poses de misma modelo. Solicita tres originales negros de tres personas distintas. Rostro/facciones/pose/cuerpo sin modificación alguna, solo fondo/luz/sombra. Verificar protección del sujeto antes de entregar. Selección y producción pendientes.

## Continuación: negros v04 con protección de píxeles
Selección visual: DSC00001.JPG (mujer pastel), DSC02003.JPG (mujer vestido claro tatuaje), DSC02116.JPG (hombre camisa vino), tres personas distintas. Autoridad: originales completos. Se producirá fondo vacío con editor integrado y composición local con máscara conservadora del sujeto. No se enviará persona a regeneración. Proteger rostro/cuerpo/pose y objetos originales. Verificar igualdad numérica en región protegida. Luz ámbar tenue y sombra/fondo con profundidad. Ninguna programación nueva. Estados: solicitado, implementación pendiente.

Negros v04 implementados y verificados: DSC00001, DSC02003 y DSC02116, tres personas diferentes. Fondo vacío generado una sola vez, luz incorporada localmente sin regenerar sujetos. PNG 4128x6192, pose/encuadre conservados con giro 90 grados. Validación tras reabrir PNG: cero píxeles diferentes en zona protegida de las tres imágenes. Rostros y luz original sobre piel retenidos. Texturas/sombras originales del set retenidas; no se reclama limpieza completa de todo borde del cuarto. Vistas reducidas para presentación; archivos maestros y máscaras aparte. Aprobación de estas tres pruebas pendiente.

## Corrección de fondos completos v05
Fuente: usuario señala que v04 conservó piso/pared; solicita corregir y mostrar tres aquí. Mantener tres personas distintas y rostros/poses sin regeneración. Quitar piso, pared y bordes del set, reemplazar con fondo negro ámbar tenue ya generado. Usar máscaras de primer plano refinadas en lugar de ajuste aditivo sobre set original. Revisión visual completa y comprobación numérica de caras obligatorias antes de entrega. Estado: solicitado, v04 no cumple eliminación del set.

V05: tres PNG compuestos con reemplazo completo del fondo de escena; piso y bordes del set retirados visualmente de DSC00001 y fondos unificados en DSC02003/DSC02116. Fondo ámbar existente reutilizado sin nueva generación. Personas, poses y objetos originales sin regeneración; recorte alfa en contornos. Resguardo facial desde originales con transición exterior. Verificación después de abrir PNG en negros_v05/verificacion.json. Resultados pendientes de aprobación visual del usuario; no aplicados al lote.

## Producción por lotes de 20 — instrucción actual
- verified: usuario aprueba las tres pruebas negras v05. Blancas/grupales v02 conservan aprobación estética previa.
- requested: crear carpeta aprobadas, conservar allí muestras aceptadas; no incluir lote nuevo sin aprobación explícita.
- requested: entregar ahora primer lote de 20 fotografías distintas editadas para revisión, con numeración estable y nombres originales.
- requested: usuario decide aceptadas/rechazadas; registrar decisiones por foto. Continuar por lotes de 20 tras revisión.
- verified: inventario Drive actualizado de carpeta fuente tiene exactamente 799 imágenes. No 891.
- requested: empezar lote 01 de fondos negros por contexto activo; no mezclar ediciones previas como nuevas.
- requested: preservar rostros/cuerpo/poses/productos originales; reemplazar set completo, negro con ámbar tenue.
- requested: entregar aquí 20 vistas y carpeta aparte de aprobadas; originales intactos, sin programaciones.
Destino: entregables/FARMASI_799/produccion y carpeta Drive de edición separada de originales. Lote 01 solicitado, selección/edición pendientes.

Lote 01 implementado y verificado: 20 fotografías nuevas de fondo negro, numeradas 01–20, PNG de resolución original. Auditoría reabriendo PNG: cero píxeles alterados en todos los rectángulos faciales y en interiores protegidos. Revisadas visualmente las veinte en cuatro hojas. Drive lectura posterior confirmó 20 PNG en Lote_01_en_revision y 6 muestras en aprobadas. URLs y IDs registrados en produccion/verificacion_drive.json y REGISTRO_EDICION.json. Estados: 6 aprobadas, 20 en revisión, 773 pendientes; suma799. La exigencia anterior de completar piloto9 queda sustituida por indicación del usuario de que las muestras actuales son suficientes y comenzar producción20. Ninguna foto nueva se movió a aprobadas. No iniciar lote02 hasta revisión de este lote. No se crearon programaciones ni nuevas generaciones de imagen; fondo vacío existente reutilizado.

## Rechazo total lote01 y reconstrucción v02
Usuario rechaza expresamente las 20 por cabello/contornos artificiales. Quedan rechazadas, ninguna aprobada. Conserva las 6 muestras previamente aceptadas. Solicita rehacer todo con atención clínica al cabello, cuerpo, proporciones, dimensiones y rasgos. Pide GPT Image 2; herramienta integrada no expone modelo verificable, no atribuirlo sin evidencia y no activar API/servicios de pago sin aprobación de cargo. Usar edición nativa de imágenes sobre originales, sin composición de máscaras locales rechazada. Primero prueba técnica interna de una toma compleja, luego resto del lote si cumple calidad; mostrar los 20 rehechos. Revisión visual ampliada y comparación con fuente antes de entregar. Confirmado por registro de ejecución: lote01 rechazado usó fondo previo y máscaras locales; no hubo20 generaciones de imagen para ese lote. No se conoce consumo global de cuota.

## Direccion elegante: peluche negro y luces visibles selectivas
Solicitado por usuario: suelo visible de peluche negro elegante, con textura y sombras de apoyo; fondo negro con profundidad y ambar muy discreto. En algunas tomas conservar los paneles LED reales y las manos del asistente apuntando a cabello y copa como detras de camaras editorial. Preservar contraluz en rizos, cabello natural completo, rostro, pose y dimensiones sin alteracion. La nueva prueba parte de DSC00108 original; no sustituye la obligacion de rehacer las 20. Estado: solicitado; prueba en ejecucion, no verificado ni aprobado.

## Comparativa solicitada: con y sin paneles
Correccion vigente: sin manos ni brazos de asistente en ninguna version. Entregar dos versiones DSC00108 con la misma composicion: A paneles discretos parcialmente fuera del encuadre; B sin paneles. Conservar peluche negro y contraluz de rizos. Preservar rostro, pose, cuerpo y cabello. Estado solicitado, pendiente de generacion y revision. Sustituye permiso previo de manos visibles.

## Comparativa de pisos solicitada
Usuario elige paneles discretos sin manos y aprueba direccion del fondo y brillo de rizos. Solicita dos nuevas pruebas sobre A: peluche negro mas corto y menos abundante; piso negro lustroso tipo agua quieta con reflejo elegante. Cambiar solo piso, conservar composicion y sujeto. Aprobacion estetica no resuelve desviacion de escala respecto al original. Estado solicitado; pendiente generacion y revision.

## Produccion de cinco en cinco
Usuario aprueba C peluche ligero y solicita reducir mas su presencia; paneles discretos sin manos, fondo y contraluz definidos. Guardar versiones expresamente aprobadas en aprobadas. El lote rechazado no se aprueba retroactivamente. Continuar por nombre, grupos de cinco sujetos a revision: DSC00002, DSC00003, DSC00004, DSC00007, DSC00009. Preservar originales y registrar fuente/version. Estado solicitado.

## Aprobacion de cinco y ampliacion siguiente a diez
DSC00002, DSC00003, DSC00004, DSC00007 y DSC00009 aprobadas expresamente; pasar a aprobadas en Drive tambien como JPG. Siguiente entrega diez consecutivas por nombre despues de DSC00009; conservar todos los requisitos visuales, originales y versiones, sin aprobar automaticamente el siguiente lote.

Verificado: las cinco DSC00002/3/4/7/9 movidas como PNG a aprobadas y JPG subidos a aprobadas/JPG; total JPG aprobados comprobado 12. Lote03: diez JPG generados por editor nativo, comparados visualmente con fuentes, guardados localmente y diez nombres comprobados en Drive, pendientes de aprobacion. Se conservan PNG y originales. No afirmar igualdad pixel a pixel de sujetos ni resolucion de sensor: salidas generadas 1024x1536.

## Lote04 con diversidad de personas
Usuario aprueba diez JPG del lote03 y ordena moverlos a aprobadas/JPG de Drive. Siguiente lote diez fotografias de otras personas, evitar las dos mujeres de los lotes recientes, mantener orden ascendente por nombre dentro de seleccion diversa y registrar saltos como pendientes, no borrar ni aprobar fotos omitidas. Preservar todos los requisitos de identidad, cabello, fondos y paneles sin manos. Estado solicitado.

Verificado lote04: diez JPG en Drive, edicion nativa de diez fuentes inspeccionadas y salidas revisadas; fuentes y PNG conservados. Orden numerico preservado dentro de la seleccion; saltos registrados en pendientes_omitidas_por_diversidad.json. Anteriores diez movidas a aprobadas/JPG y conteo22 comprobado. Lote04 sigue en revision del usuario, no aprobado. Las salidas generativas no garantizan identidad pixel a pixel ni microtexto exacto de etiquetas; se conserva fuente de comparacion.

## Respaldo GitHub autorizado
Usuario solicita depositar proyecto, prompts exactos, proceso y detalles de calidad en GitHub para relevo de modelo al agotarse cuota. Destino verificado privado ponchogf88/captoora, rama farmasi/continuidad-edicion-799; solo carpeta proyectos/farmasi-799. Fotos permanecen en Drive conforme regla de custodia del repositorio; GitHub contiene enlaces/versiones/hash, no rollos. Recuperados 33 prompts exactos de ejecucion; faltantes historicos declarados como no recuperados, no inventados. Incluir proceso, fallos y limitaciones, registro799,22 aprobadas,10 en revision, plantillas separadas de prompts reales, guia de relevo y script idempotente de actualizacion sin generacion ni cobros. Estado solicitado, paquete en preparacion.

## Lote05 prioridad cabello negro largo
Usuario solicita diez de mujer descrita de piel clara, cabello largo lacio negro y sonrisa; candidata visual localizada en vestido blanco DSC01532 y DSC01663. Seleccionar diez de esa secuencia en orden y verificar cada sujeto antes de editar. Lote04 permanece en revision. GitHub respaldo inicial subido rama farmasi/continuidad-edicion-799; pendiente lectura remota y actualizacion de lote05.

Lote05 verificado parcial: siete JPG generados, revisados y comprobados en Drive. DSC01532, DSC01536 y DSC01540 bloqueadas por filtro de salida de image_gen; codigo moderation_blocked. No se recibieron tres imagenes, no declarar lote de diez terminado ni reintentar para eludir filtro. Quedan pendientes. Total22 aprobadas,17 en revision y3 bloqueadas. Diez nuevos prompts exactos (7 con salida y3 bloqueados) anadidos al respaldo; total43.

## Produccion nocturna autorizada 4 noviembre
Usuario aprueba siete entregadas lote05; mover solo esas siete a aprobadas/JPG. Solicita diez grupales, luego diez de otra chica y continuar produccion nocturna. Aclaracion expresa: hasta200 a las10:00 America/Mexico_City, ritmo40 cada2horas (objetivos02=40,04=80,06=120,08=160,10=200). Esta autorizacion revoca cancelacion anterior solo para esta programacion. No aprobar automaticamente nuevas fotos, no instalar/comprar/autorizar cargos ni intentar eludir filtros; conservar bloqueadas pendientes; generar con herramienta integrada y verificar Drive/GitHub. Limite200 salidas nuevas; primeros20 actuales forman parte del limite, no se suman dos veces.

Programacion verificada activa farmasi-producci-n-nocturna-hasta-200-4-nov: primera revision01:00,luego03/05/07/09,bloques40hasta200,10:00solo cierre. Sustituye horarios02/04/06/08/10 previos para dejar ultimo bloque antes del corte. Siete lote05 movidas a aprobadas/JPG;29aprobadas, no contar como nuevas nocturnas.

Verificado: lote06 diez grupales y lote07 diez individuales nuevos, todosJPG en Drive revisados visualmente y comprobados por lectura. Veinte de200 nocturnas, quedan180;29anteriores aprobadas en carpetaJPG. Programacion activa01/03/05/07/09 y10solo cierre, contar primeros20sin duplicacion. Sesionactual reserva liberada. GitHub requiere sincronizacion de63prompts y estado actualizado.

Heartbeat01:00del4nov:20nuevasya verificadas, faltan20para objetivo40. Reserva20fuentes distintas para lotes08grupalesy09otrapersona; ninguna aceptada automaticamente. Estado solicitado/enproduccion.

Heartbeat01:00 completado: veinte nuevas fuentes (10grupales lote08y10de otra persona lote09) generadas con editor integrado, inspeccionadas y JPG guardados/verificados en Drive por nombre y peso. Contador40/200, pendientes160. Se conserva29aprobadas;50enrevision. Sin filtros ni cargos adicionales autorizados en este bloque. Reserva liberada para proxima activacion03:00, objetivo acumulado80. Prompts exactos83yregistros a sincronizar GitHub.

## Activacion03:00 4nov: solicitado40 nuevas
Fuente heartbeat03:06; acumulado verificado40de200. Reservadas40 fuentes pendientes distintas en SELECCION_0300.json, cuatro sublotes10: grupales, rizos blanco y dos personas distintas; inspeccionar categorias/orientacion antes de editar. Conservar identidad, cabello, pose y objetos, estilo aprobado; destinos revision Drive, nunca aprobadas. Registrar prompts exactos y respaldo GitHub. Estado solicitado/preparando, ninguna nueva contada aun.

Verificado activacion03:00: 40 nuevas JPG distintas en cuatro carpetas Drive,10porcarpeta, nombres y bytes comprobados por lectura posterior; acumulado nocturno80/200, ninguna nueva aprobada. Revisadas fuentes orientadas y40 salidas, cinco correcciones internas de objetos personales residuales en grupales conservadas como historial. Prompts exactos128, incluyendo cinco versiones internas corregidas. Distribucion de esta activacion:10grupales blancas,21individuales blancas y9individuales negras. Originales intactos; limitaciones generativas de identidad/microtexto y resolucion declaradas. Respaldo GitHub en preparacion.

## Prioridad usuario chica DSC07722,4nov04:50
Solicitud20 de la chica de cabello largo negro/conjunto lila estampado, sola y grupo. Referencia capturaDSC07722.JPG. Seleccionar10individuales y10grupales por inspeccion visual; verificar misma chica aunque vestuario distinto. Originales intactos, mismos criterios aprobados de identidad/cabello/pose/productos, blanco con sombras y peluche suave; enviar20a revision Drive, sin aprobar automaticamente. Contar dentro200 nocturnas para no duplicar; reserva prioritaria en PLAN_NOCTURNO. Registrar prompts y sincronizar GitHub. Estado solicitado, seleccion preliminar pendiente inspeccion final.

Confirmacion explicita usuario: enDSC08454 la chica del vestido cobrizo a derecha es la solicitada; incluir esas grupales. Seleccion10individualesDSC07706a07734 y10grupalesDSC08454a08484 verificada por vestuario/secuencia y seleccion del usuario, no identificacion facial automatica.

Verificado prioridadDSC07722:20JPG nuevas en Drive,10individuales lote14 y10grupales lote15 con seleccion del usuario. Todas inspeccionadas contra originales orientados; fondo blanco dimensional/sombras y alfombra extendidos, set retirado. Conteo10porcarpeta y bytes comprobados por lectura Drive; contador100/200, ninguna nueva aprobada automaticamente. Prompts exactos148; PNG fuente y JPG derivados aparte. Vistas numeradas01a20 en CONTACTO_FINAL.png. Preservacion generativa revisada visualmente, no prometer igualdad pixel a pixel ni microtexto exacto. Reserva liberada, pendientes20para objetivo05:00=120, sin duplicar esta tanda.

## Correccion clinica rostros y textos,4nov
Usuario marca7rostros y1etiqueta en8capturas: restaurar SOLO zonas marcadas, no rehacer foto completa. Nueva regla general para TODAproduccion: conservar rostros reales sin acuarela/suavizado/deformacion y textos/logotipos de producto exactos desde fuente; solo ajustes de luz/exposicion recuperable, nunca inventar detalle quemado o texto ilegible. Usuario autoriza expresamente edicion local de pixeles copiando originales, sin IA generativa. Mantener cuerpos/poses/cabello/vestuario/fondos y zonas no marcadas; no reusar mascaras Vision rechazadas. Identificar fotos exactas por registro de imagen, registrar regiones y verificar cambios fuera mascara=0 contra base de misma resolucion. Preparar versionv03 separada, no sobrescribirv02 ni aprobar automaticamente. Para resolver reduccion generativa de resolucion, evaluar master de resolucion original con fondo aprobado escalado tecnicamente, zonas fuente restauradas; declarar la base usada en auditoria. Auditoria de textos global solicitada, estado pendiente hasta verificar cada foto; no afirmar cumplimiento global con un parche de muestra. Produccion nueva retenida por puerta de calidad.

Correccion localv03: entrega estricta8fuentes (7rostros marcados +etiquetaDSC07726), restauradas desde originales en lienzo6192x4128/4128x6192 con fondo previo escalado solo tecnicamente. PNG maestro comprueba0pixeles cambiados fuera de regiones contra base de igual resolucion. Sin nuevas llamadas generativas ni nuevos cargos. Pruebas extendidas de productos en13fuentes son INTERNAS_NO_ENTREGAR; no avaladas y apartadas, no afirmar correccion general de10individuales. La entrega final esta en correcciones_rostros_textos_v03/entrega_final. DSC08479 conserva desenfoque de origen; parte de letra fina del envase no recuperable por reflejo con estas fuentes. Catalogop134 muestra otra impresion (CompleteBlend/espanol), no reemplazar etiqueta inglesa/francesa fotografiada. Estado: versiones parciales para revision; falta fuente nitida misma etiqueta para precision completa. Regla general de conservar caras/textos reales registrada; auditoria retrospectiva deotrasfuentes sigue solicitada, sin declarar cumplimiento global. Revisar esta tanda antes de extender correcciones. Nuevas generaciones integrales de sujetos/textos no permitidas.

## Aprobacion v03 y correccion localizada cabello DSC07706
Usuario aprueba explicitamente las8correcciones v03. Pasar sus JPG/PNG maestros a aprobadas, sin aprobar v04 anticipadamente. Solicita SOLOcabello de DSC07706: eliminar apariencia ondulada/acuarela, recuperar hebra definida desde original, caida lisa natural con movimiento, sin planchado rigido. Rostro aprobado, piel, manos, ropa, pose, productos y fondo intactos. Reutilizar autorizacion vigente de restauracion local de pixeles; no generacion completa ni cambios de rasgos. Entregar nueva versionv04 aparte para revision, comparativa ampliada y verificar0cambios fuera de mascara y rostro. Registrar fuente, mascara, ajustes, Drive y GitHub. Estado solicitado.

### Entrega cabello v04 verificada
Ocho v03 aprobadas por usuario, JPG y PNG movidos y verificados en Drive. DSC07706 v04 candidata aparte: textura real de cabello restaurada, rostro y exterior de mascara con cero pixeles modificados. PNG y JPG subidos y bytes verificados; pendiente aprobacion visual. No generacion ni incremento de fuentes nocturnas.

## Lote16 solicitado:20fuentes nuevas con variedad de modelos
Usuario aprueba DSC07706v04 explicitamente; moverla a aprobadas conservandohistorial. Seleccionar20fuentes pendientes diversas, verificar orientacion, limpiar solo set sin alterar rostros/cabellos/cuerpos/productos/rotulos. Conservar alfombra y sombras reales, no repetir fotos ni aprobar nuevas automaticamente. Fuentes en lote_16_variedad20/SELECCION_20.json, estado solicitado. Priorizar fidelidad original mediante edicion local; nuevas versiones a revision Drive y trazabilidad GitHub.

Control de calidad lote16: primer metodo local de relleno rechazado internamente por bordes artificiales y una invasion de region de rostro. NOsubido aDrive, NOentregado, NOcontado, NOaprobado. Veintefuentes seleccionadas siguen pendientes, no sustituirlas por pruebas fallidas. Aprobacionv04 deDSC07706 registrada y archivos movidos aaprobadas enDrive, nombres ypadres verificados.

## Auditoria de aprobadas solicitada
Usuario solicita comprobar TODASlasaprobadas y recuperar faltantes del modelo camiseta blanca/shortnegro, identidad descriptiva confirmada por usuario. Cruzar DriveJPG, maestrosPNG y aprobaciones historicas; no incluir originales ni borradores rechazados. Primera lectura:37fuentes aprobadas,38JPGincluida versionhistoricaDSC07706,21PNG: faltan17maestrosPNG. DSC02748pilotov01 existe localmente y corresponde al modelo confirmado, pero no estaba registradaenaprobadas. Recuperar esta version historica con giro90sinretoque y registrar aclaracionactual delusuario como autoridad. No usar nueva prueba fallida lote16. Otras fotos sin edicion/aprobacion verificable siguen pendientes.

Auditoriaaprobadas verificada:38fuentes aprobadas,39JPGy39PNGincluida versionhistoricaDSC07706; cero faltantes contra registro actualizado y todoslosbytesconcuerdan. DSC02748piloto recuperada solo giro90, JPG/PNG enDriveaprobadas.17PNGfaltantesincorporados. Otras fotos del modelo sin edicion entregada ni aprobacion individual no se etiquetan comoaprobadas. La fuenteDSC02748 se excluye de seleccionlote16 pendiente de reemplazo para no contar foto antigua como nueva. Informe en produccion/auditoria_aprobadas_2026-11-04/INFORME.md.

## Aprobacion total de todas las entregas en revision
Usuario aprueba expresamente TODASlasfotos actualmente enrevision, incluidos lote09 y modelo conperiodico/geles y maquillajelabial. Transferir102fuentes pendientesdeaprobacion aaprobadas JPGyPNG, verificar Driveconpaginacion ybytes, conservar originales e historial. No incluir12versionesrechazadas ni3bloqueadas ni pruebasinternas rechazadas lote16. Objetivo140fuentes aprobadas, sin generar imagenes nuevas. Estado solicitado, autoridadmensajeactual.

Aprobacion total ejecutada y verificada:102fuentes antesenrevision pasan aaprobadas;140fuentes aprobadas total.149JPGy149PNG enDrive incluidos9historicos.11carpetasrevision vacias porlectura, ceroestadoenrevision. Todosnombres,padres,bytes yhashescopiaslocalescomprobados. Los12rechazadosy3bloqueados quedan separados; pruebasinternasfallidas lote16no se aprueban. Desgloseyenlaces en produccion/aprobacion_total_revision_2026-11-04/INFORME_APROBACION_TOTAL.md. No cuenta como fuentes nuevas nocturnas.

## Correccion de duplicados en aprobadas
Usuario exige SOLOultima versionaprobada porfuente enaprobadas, JPGyPNG. Sustituye instruccionoperativa previa dehistorial dentrodeaprobadas. Conservar140fuentes una vezporformato; archivar18archivos de9versionesanteriores fuera deaprobadas sineliminar originales nihistorico. ParaDSC07706 conservarv04, archivav02yv03. Elegirversionporapproved_jpg_drive delregistro, no porfechadesubida. Estado solicitado,seleccionverificada depuracion_ultima_aprobada_2026-11-04/CONSERVAR.json yARCHIVAR.json.

Depuracionverificada:18archivos obsoletos (9versiones JPGyPNG) movidos fuera deaprobadas aHISTORIAL_VERSIONES_ANTERIORES_NO_ENTREGA.140JPGy140PNG,140fuentes unicasporformato, cero duplicados. DSC07706solov04. MismosIDsconservados, padresynombresybytes comprobados, localesconcuerdan. Regla permanente: aprobadas contieneuna sola ultima version aprobada, historicosiempreaparte.

## Prioridad retratos del bebe
Usuario solicita localizar y corregir fotos delbebe, incluidas movidas/borrosas; comparar secuencias yrecuperar detalle REALde tomas cercanas solo con compatibilidadde pose/expresion/perspectiva, nuncainventar ojos/facciones/expresion ni pielplastificada. Conservaroriginales, seleccionar tecnicamente antes de retocar, mejorar luz/color y setmanteniendo delicadeza y texturareal. Primeraspruebas aparte pararevision, no aprobarautomaticamente. Una ultima version aprobada porfuente. Localizacion e inspeccion pendientes.

Bebe:11tomas verificadas porconsulta actualenDrive y porcontactovisual, nombresenONCE_PRIORITARIAS.json; secuenciaampliada contiene19tomas conbebe, noafirmar11comototalexhaustivo. Tres pruebaslocales de luz/color sinreconstruccionfacial:DSC08258,DSC08290 2,DSC08295. DSC08284descartadainternamente comoprueba deentrega porfaltadefoco. Nosemezclanexpresiones nifacciones entreframes, semantiene rug ysombras reales. Nuevaspruebasquedan enrevision, nopasan aaprobadasautomaticamente.

Bebe: tres primeraspruebas DSC08258/DSC08290 2/DSC08295 revisadas aescala general y detalle, JPGyPNGsubidosaDrive ybytesverificados. Color/luzsobreoriginal, texturayrasgos originales conservados sinregeneracion;franjalateralrecortada2.2porcientoen2fuentes, registrado. No afirmar recuperaciondedetalleperdidoniediciondetodaslas11. Tresenrevision pendientesdeaprobacion,140anterioresaprobadasintactas. Fuente08261y08284conmovimientodescartadasdelasprimeraspruebas. Metodoexacto enbebe/editar_pruebas_bebe.py.

## Relevo GitHub para Antigravity solicitado
Usuario reclama falta de prompts/instrucciones accesibles para continuar produccionmasiva y reiterabitacora. Auditar rama remota,148prompts exactos yguias; corregir documentos deentrada obsoletos; publicar paquete textual enrama principal y dejarindice raiz/bitacora/ruta agentes. No subir fotos, secretos, links temporales ni cambiarwebsite. Distinguir prompts historicos de instrucciones vigentes sin regenerar caras/etiquetas; documentar metodo local exacto bebe yrestauracion, versionunicaaprobada, estado actualizado, colas/fallos/filtros, verificacionesypuertasdelote. Nuevas pruebasbebe gustadas y aceptadas porusuario en mensajeactual; registrar aprobacion3sinconfundirla con el resto de secuencia pendiente. Estado solicitado.
