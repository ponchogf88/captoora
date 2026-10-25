# Contrato operativo de producción · CAPTOORA

Fecha: 20 de octubre de 2026, Monterrey. Versión 1.

Este documento establece el encargo y los criterios de cumplimiento del agente de IA. Es un acuerdo operativo de trabajo, no un contrato laboral firmado ni una garantía de operación independiente de los accesos y del entorno.

## Encargo

Producir contenido útil y revisable para CAPTOORA: guiones, narración, apariciones breves de Likinya, demostraciones, montaje, subtítulos y derivados. Mantener una línea separada del fundador, cuyo nuevo clon espera sus fotos y grabación. Integrar el servicio de clon digital en CAPTOORA Biometrics, respetando el alcance comercial documentado.

## Obligaciones y comprobantes

| Obligación | Acción exigible al agente | Evidencia para considerarla cumplida |
|---|---|---|
| Continuidad | Leer requisitos y checkpoint antes de actuar; conservar encargos anteriores | REQUISITOS.md actualizado |
| Accesos | Probar cada herramienta necesaria; separar conector, sesión, permiso y cuota | Cuenta consultada y fecha; desconocido donde no haya prueba |
| Aprovechamiento | Priorizar reinicios comprobados y contenido útil | Saldo anterior/nuevo, unidad, fecha e ID de generación |
| Producción | Avanzar piezas completas; los insumos no cuentan como reel final | Audio, escenas, MP4 y ficha de revisión |
| Identidad | Usar personaje y voz correctos | avatar/look ID y voice ID; sin sustitución silenciosa |
| Calidad | Revisar imagen, sonido, sincronía, subtítulos y exactitud | Registro de revisión; rechazar fallos aunque el archivo decodifique |
| Reutilización | Localizar maestros ISO/enfoque y originales antes de rehacer | Ruta de origen y versión |
| Almacenamiento | Conservar originales y comprobar espacio/destino | Manifest con rutas, tamaño y hash; permisos antes de transferir |
| Automatización | Ejecutar la cola cuando despierte la tarea; no limitarse a repetir el plan | Historial de ejecución y dependencia resuelta o archivos nuevos |
| Reportes | Informar producción y consumo reales, incluidos ceros | Reporte por ejecución; balance al reinicio cuando sea medible |
| Publicación | Distinguir render, revisión, programación y publicación | URL/ID de publicación cuando exista autorización y ejecución |
| Recuperación | Consultar estado antes de repetir generación incierta | ID del trabajo y resultado; sin duplicados pagados |

## Límites y autorizaciones actuales

- El usuario autoriza crear contenido, rutinas, guardar en GitHub e incorporar clonación en el sitio.
- El usuario expresó aceptación de cargos adicionales; no hay monto máximo semanal definido. No existe una compra nueva ejecutada ni obligación de gastar por gastar. La automatización actual sigue limitada a cuotas incluidas hasta conciliar su política con el presupuesto y las condiciones de cada herramienta.
- No publicar en redes, mandar DMs ni contratar servicios nuevos por inferencia.
- No prometer cuota 100% consumida, ventas que cubran costos, terabytes de material o funcionamiento permanente sin medición y capacidad comprobadas.
- Una suscripción web no acredita acceso API. Abrir una pestaña no acredita sesión ni derecho de uso. No guardar claves o contraseñas en este documento.

## Automatización existente y responsabilidad horaria

Nombre: **Producción CAPTOORA · Likinya**. ID: `producci-n-captoora-likinya`. Estado guardado: ACTIVE. Frecuencia: cada hora, en este hilo. Archivo de configuración: /Users/user/.codex/automations/producci-n-captoora-likinya/automation.toml.

Ya se recibieron despertares y ejecutaron comprobaciones. Eso acredita el disparador, no que las quince herramientas estén integradas. Requiere que la aplicación, la máquina y los accesos permitan trabajar; no es un servidor de generación 24/7 garantizado.

Al despertar: leer cola → consultar estados/saldos → producir siguiente etapa viable → revisar → guardar evidencia → informar resultado. Si un paso está bloqueado, resolver otra dependencia real. No volver a renderizar material rechazado ni crear duplicados por llenar la cuota. Si no existe avance ejecutable, registrar un bloqueo concreto y la intervención necesaria.

Rutina detallada: RUTINA_PRODUCCION.md. Ejecutor local: producir_lote.py. Evidencia: manifest.json, cuotas.json, ejecuciones.jsonl y reporte.json. Este ejecutor solo recorta una fuente local; no integra ElevenLabs, HeyGen ni los demás proveedores.

## Inventario de herramientas y cuentas

| Herramienta | Función | Estado comprobado o límite |
|---|---|---|
| HeyGen | Avatar y clon del fundador | Conector operativo; saldo actual consultado 1055 premium; reinicio 23 oct 20:48 Monterrey. Photo Avatar y Alfonso localizados; Pharmacy Girl sin correspondencia por nombre |
| ElevenLabs | Voz maestra | En un turno anterior se vio sesión y 34280 créditos. En esta auditoría no hay pestaña accesible y reapertura agotó espera; saldo actual no recertificado; voz femenina pendiente |
| Canva Business | Portadas, fichas y carruseles | Consulta real de kits rechazada por sesión: requiere reconectar Canva. Plan/equipo no acreditados |
| CapCut | Montaje | Plugin disponible en sesión; autenticación, plan, saldo y cuenta de renovación pendientes |
| Captions | Montaje alternativo | Aplicación instalada, no ejecutándose en inventario; sesión y plan no comprobados |
| OpusClip | Derivados de material largo | Suscripción declarada; acceso y material largo pendientes |
| PicsArt Pro | Retoque puntual | Suscripción declarada; acceso no verificado |
| InVideo | Producción alternativa | Suscripción declarada; acceso no verificado |
| Edits de Instagram | Edición móvil | Declarada; no control móvil verificado |
| Google Photos | Biblioteca | Declarada; no sesión o inventario comprobados |
| Fotos de Apple | Biblioteca local | App encontrada; no estaba ejecutándose; biblioteca no inventariada |
| Google AI Pro / Nano Banana / Flow | Imágenes y escenas | Cuentas adicionales declaradas por usuario; accesos, límites y reinicios no comprobados |
| Pippit AI | Variantes comerciales | Declarada; acceso no verificado |
| Evoto | Trabajo fotográfico | App ejecutándose según inventario; 65 créditos declarados por usuario, no saldo consultado |
| Pixieset | Galerías y entrega | Declarada; acceso y galería no verificados |
| GitHub | Fuente y respaldo de producción | Escrituras y lecturas remotas verificadas en ponchogf88/captoora |
| Page Agent / Browser Use / Video Use / Browser Flow | Automatización solicitada | No se han verificado conectores operativos con esos nombres. Sí existe CUA para navegador/apps; no equivale a tener todas estas herramientas instaladas |

No están todas las cuentas abiertas ni operativas. Este inventario lo declara para impedir informes falsos.

## Resultado acumulado comprobado

- Doce guiones borrador y calendario relativo guardados en GitHub.
- Tres recortes locales, 3122026 bytes; rechazados para piloto educativo por marca incrustada y contenido inadecuado. Cero reels finales a partir de ese lote.
- Cero audios nuevos de ElevenLabs y cero clips nuevos de avatar generados en esta conversación hasta este checkpoint.
- Tarjeta de clon digital y FAQ en js/config.js; ficha en CAPTOORA_BIOMETRICS/CLON_DIGITAL.md. Código remoto comprobado. GitHub Pages devolvió 404; publicación pública no acreditada.
- Una imagen de disposición de set creada y mostrada al usuario.

## Prioridad de ejecución siguiente

1. Recuperar sesión de ElevenLabs y voz femenina; dejar de tratarla como bloqueada por login si la sesión vuelve a estar accesible.
2. Resolver look de Likinya/Pharmacy Girl con evidencia y generar solo apertura y cierre del piloto usando el mismo audio maestro.
3. Seleccionar demostraciones propias limpias; finalizar un reel educativo con subtítulos y revisión.
4. Una vez revisado el piloto, ampliar lotes distintos y producir derivados en Canva.
5. Identificar destino nube y auditar restantes servicios; no esperar que todas las cuentas estén conectadas para usar las operativas.

## Reporte que debe recibir el usuario

Piezas terminadas y enlace; insumos separados; cuota antes/después y unidad; fallos/costos comprobados; bloqueos y siguiente acción. Un documento o recordatorio por sí solo no cuenta como contenido terminado.

## Aceptación expresa del usuario

20 octubre 2026, Monterrey. El usuario manifestó «Acepto el contrato» y «My acceptance. My signature. My voice signature, of course.» en esta conversación. Se registra aceptación del acuerdo operativo y autorización de continuidad dentro de su alcance. Evidencia disponible: mensaje recibido; no se verificó ni archivó un audio original o certificado. No se certifica una firma ni se sustituye el consentimiento de HeyGen. Presupuesto adicional y publicaciones conservan los límites documentados. Idiomas declarados: español e inglés; grabación inicial del clon propuesta en español.
