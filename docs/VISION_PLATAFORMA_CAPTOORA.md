# Captoora — visión de plataforma

**Estado:** idea en planeación; no es un PRD aprobado ni una orden para programar.
**Fecha de captura:** 2026-10-20
**Fuente canónica:** `docs/VISION_PLATAFORMA_CAPTOORA.md` en el repositorio privado `ponchogf88/captoora`.
**Trazabilidad:** requisitos y estado en [`PRODUCT_VISION_REQUIREMENTS_LEDGER.md`](PRODUCT_VISION_REQUIREMENTS_LEDGER.md).

## Intención del fundador

Captoora podría evolucionar de estudio y sitio fotográfico a una plataforma especializada que ayude a operar el negocio, entregar fotografías, aprender fotografía y, a largo plazo, conectar clientes, fotógrafos y espacios. Pixieset serviría durante la transición como herramienta práctica para galerías y entregas; la plataforma propia se diseñaría con tiempo y una estructura clara.

La intención expresada es evitar una plataforma saturada, reducir gastos repetidos y cuotas por imagen cuando exista una alternativa local adecuada, y ofrecer algo que combine operación fotográfica con recursos que Pixieset no prioriza. La estimación de “menos de un mes” se conserva como expectativa informal, no como plazo prometido.

## Líneas Captoora mencionadas

Los nombres y límites son provisionales; confirmar antes de convertirlos en arquitectura o comunicación comercial.

- **Captoora Studio:** fotografía editorial y sesiones regulares de estudio.
- **Captoora Signature:** bodas, quince años y experiencias de alta producción.
- **Captoora Pop:** Smash Cake, fiestas infantiles y conceptos lúdicos/estacionales.
- **Captoora Corporation:** retrato profesional, LinkedIn y fotografía empresarial.
- **Captoora Biometrics:** concepto relacionado con salud y registros de progreso corporal; requiere diseño separado de privacidad, consentimiento y tratamiento de datos sensibles.
- **Temporadas:** Navidad podría activar ofertas de Studio, Signature, Pop y quizá Corporation según el contexto de cada servicio; no se limita a una sola línea.

## Capacidades que se quieren explorar

### Operación fotográfica y edición

- Ingesta, organización y selección asistida de fotos.
- Edición consistente y exportación por lote con perfiles reutilizables.
- Prioridad a un motor local para ajustes fotográficos y control de costos; evaluar por separado cualquier función que requiera IA externa o cobro por uso.
- Galerías privadas para clientes, favoritos/comentarios y descargas individuales o por colección.
- Administración de sesiones, clientes, reservas de estudio y entregas.
- Integración con Pixieset durante una transición gradual, sin interrumpir las entregas actuales.

### Biblioteca educativa y apoyo en sesión

- Guías prácticas de poses, lentes, iluminación y tethering.
- Referencias para consultar durante una sesión cuando se necesite inspiración o una indicación de pose.
- Posibles enlaces a referencias externas como Pinterest; no copiar imágenes o guías ajenas sin permiso y revisar las condiciones de uso de cualquier integración.
- Recursos para conectar cámara y computadora en tiempo real.

### Documentos y permisos de locación

- Plantillas y flujo de contratos, autorizaciones y permisos de uso de imagen.
- Orientación para consultar permisos de fotografía por locación (por ejemplo, parques o recintos de Monterrey).
- Generación, revisión, control de versiones, renovación y archivo de documentos.
- Toda guía legal deberá indicar jurisdicción, fecha y fuente verificable; no prometer certeza jurídica sin revisión vigente.

### Comunidad y marketplace — horizonte posterior

- Explorar una micro-SaaS que conecte clientes con fotógrafos disponibles y espacios de estudio en renta.
- Permitir que el cliente programe una sesión desde el teléfono; no se promete atención inmediata estilo transporte por aplicación.
- Evaluar perfiles, disponibilidad, calidad, pagos, cancelaciones, seguridad, seguros y responsabilidades antes de abrir el marketplace.
- Explorar comunidad de fotógrafos y acceso a herramientas o equipo, sujeto a un modelo operativo y económico viable.

### IA Bar / IA Coffee Studio — concepto físico futuro

- Experiencia futura de aprendizaje y uso de herramientas de IA e internet, conectada con fotografía y estudio.
- La expansión física del espacio (incluida construcción sobre la terraza) es una dependencia; no se considera parte del lanzamiento de software.
- Mantener separado el concepto digital de la decisión futura sobre abrir o construir un local.

## Principios de diseño propuestos

1. **Menos opciones por tarea:** presentar primero el flujo que el fotógrafo necesita y dejar controles avanzados bajo demanda.
2. **Originales intactos:** conservar originales y crear salidas derivadas con trazabilidad.
3. **Humano decide:** selección y diagnósticos orientan; no descartan ni alteran momentos importantes sin revisión.
4. **Realismo fotográfico:** las herramientas de edición deben respetar identidades, expresiones, cuerpos, productos y locación.
5. **Privacidad primero:** priorizar procesamiento local cuando sea razonable; pedir consentimiento claro para cualquier procesamiento externo.
6. **Modularidad:** compartir componentes cuando convenga, manteniendo diferencias entre líneas de servicio.
7. **Legal verificable:** contratos, permisos y recomendaciones locales muestran fuente y vigencia, y distinguen plantillas informativas de asesoría profesional.
8. **Transición sin interrupciones:** usar Pixieset y los procesos actuales hasta validar cada capacidad propia con sesiones reales.

## Mapa inicial de módulos para planear

| Módulo | Problema que podría resolver | Estado |
|---|---|---|
| Photo Desk | Organizar, seleccionar, revelar y exportar sesiones con bajo costo por foto. | Idea; revisar prototipos existentes antes de definir requisitos. |
| Client Gallery | Presentar, proteger y entregar galerías con descargas y selección de favoritas. | Referencia de Pixieset; requerimientos propios por definir. |
| Studio CRM | Contactos, prospectos, sesiones, agenda, contratos, cotizaciones y pagos. | Idea; definir alcance y servicios de pago por país. |
| Learning Library | Guías y recursos para poses, lentes, luz, tethering y operación. | Idea; identificar fuentes y derechos. |
| Location & Legal Desk | Consultar permisos y gestionar contratos/consentimientos con trazabilidad. | Idea; requiere validación jurídica por jurisdicción. |
| Marketplace | Descubrimiento y reserva de fotógrafos y espacios. | Horizonte posterior; validar oferta, demanda y responsabilidades. |
| IA Bar / Coffee Studio | Espacio educativo y de experimentación con IA e internet. | Concepto físico futuro; depende de espacio e inversión. |

## Secuencia para continuar la planeación

1. Completar el mapa de líneas y servicios de Captoora con el fundador.
2. Auditar los prototipos existentes de selección, desenfoque y retoque, sin modificarlos.
3. Comparar necesidades con Pixieset y documentar qué se queda temporalmente en Pixieset.
4. Priorizar un flujo inicial pequeño y comprobar calidad, privacidad, costo operativo y facilidad de uso.
5. Definir arquitectura, datos, respaldo, permisos, pruebas y criterios de aceptación.
6. Solo después de cerrar la planeación, el fundador decidirá cuándo autorizar construcción.

## Benchmark Pixieset

Revisado en fuentes oficiales el 2026-10-20. Pixieset agrupa galerías, sitios web, gestión de estudio, tienda y una herramienta de edición/selección de fotos. Sirve de referencia funcional, no implica que Captoora deba copiar su interfaz o sus procesos.

- [Client Gallery](https://website-help.pixieset.com/en/articles/5129147-getting-started-with-client-gallery)
- [Studio Manager](https://pixieset.com/studio-manager/)
- [Planes Pixieset](https://pixieset.com/pricing-website/?currency=USD)
- [Pixieset Photo Editor](https://blog.pixieset.com/blog/photo-editor/)

Disponibilidad, precios y métodos de pago varían por plan y país; verificarlos de nuevo antes de cualquier decisión comercial.

## Estado de ejecución

- **Documentado:** la visión inicial y las ideas mencionadas en conversación.
- **No decidido:** requisitos de producto, secuencia final, modelo de negocio, arquitectura y fecha de lanzamiento.
- **No iniciado:** desarrollo de esta plataforma. La documentación no autoriza código, despliegue, publicación ni gasto.
