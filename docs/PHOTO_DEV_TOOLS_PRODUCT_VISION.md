# CAPTOORA — Photo Dev Tools: visión y descubrimiento del producto

> Documento de exploración, 11 de noviembre de 2026. Hipótesis pendientes de validar con fotógrafos reales. No implica desarrollo implementado ni decisiones definitivas de marca.

## Visión
Crear un asistente de IA especializado para fotógrafos principiantes, aficionados y creadores de contenido que traduzca su intención creativa a acciones prácticas. Debe reducir tres fricciones: problemas técnicos, tiempo perdido y compras equivocadas o innecesarias.

## Problemas observados por el fundador
- Barrera técnica entre imaginar una fotografía y conseguirla: ISO, apertura, velocidad, iluminación y enfoque.
- Manuales extensos, tutoriales desactualizados, heterogeneidad de cámaras y marcas.
- Compatibilidad confusa de cámaras, lentes, disparadores y flashes (ejemplo Godox X2T-N vs X2T-C).
- Costos de softboxes, fondos de papel, cicloramas y equipo profesional; alternativas accesibles, de segunda mano y bricolaje seguro.
- Necesidad de orientación en la tienda sobre telas, textura, reflejos, absorción de luz, costo por metro y resultado visual.
- Fotografía de producto y contenido comercial para pequeñas empresas con presupuestos reducidos.
- Dificultad de dirigir poses y asegurar estabilidad física de soportes y luces.
- Chats genéricos fragmentados que no conservan inventario ni contexto fotográfico.

## Propuesta de producto
Nombre de trabajo: CAPTOORA (nombre comercial y denominación de app por validar). Proyecto técnico: Photo Dev Tools. Nombres de módulos, también provisionales: PhotoPilot (guía creativa/técnica) y GearCheck (compatibilidad/compras).

### Modo 1 — Quiero lograr esta foto
El usuario describe verbalmente el resultado o comparte una fotografía de referencia. El asistente pregunta lo mínimo indispensable, conoce el inventario y presupuesto, propone una receta contextual de cámara, lente, fondo, iluminación y pasos, y ajusta iterativamente según la foto capturada. Distinguir entre análisis de imágenes, inferencia y ajustes realmente comprobados.

### Modo 2 — Antes de comprar, pregúntame
Comparación de compatibilidad según modelo exacto y versión; funciones soportadas/perdidas; precios, alternativas usadas o económicas; estimación de costo total; advertencias sobre ofertas, devoluciones y seguridad física. No afirmar compatibilidades sin evidencia técnica verificable.

### Fases posteriores
- Manual conversacional basado en documentación oficial con citas por modelo/firmware.
- Asistente de voz manos libres y guía visual paso a paso.
- Dirección de poses, iluminación y fotografía de producto.
- Controles de cámara/tethering por APIs o SDKs compatibles, sin prometer modificaciones del firmware o la pantalla interna.
- Seguridad de API, autorización por cliente/sesión, protección de fotografías y pruebas en laboratorio aislado.

## MVP recomendado
**Primera experiencia:** fotografía de producto para redes con el equipo que el usuario ya tiene, incluyendo smartphone. Usuario describe estilo, luz, presupuesto y equipo; el asistente entrega configuración, secuencia de pruebas, revisión de resultado y solo recomienda compras cuando sean necesarias.

**Primera plataforma:** web móvil adaptable (PWA) para facilitar pruebas en Android, iPhone, Mac y Windows sin mantener varias aplicaciones nativas. Evaluar apps nativas después de validar experiencia y necesidades de integraciones.

**Arquitectura inicial propuesta:** interfaz web; perfil de inventario con consentimiento; motor conversacional; catálogo de compatibilidad con fuentes y nivel de confianza; captura/carga opcional de fotografías; analítica privada y control de costos. No cargar fotografías reales de clientes sin permiso y políticas de retención claras.

## Beta y validación
Invitar a fotógrafos de confianza. Medir:
1. Porcentaje que logra un resultado fotográfico satisfactorio.
2. Minutos necesarios para obtener la fotografía deseada.
3. Compras erróneas evitadas y ahorro verificable.
4. Utilidad, claridad, precisión y confianza en recomendaciones.
5. Repetición de uso, testimonios consentidos y disposición real a pagar.

Los testimonios y métricas deben provenir de pruebas reales; no fabricar cifras de mercado ni declarar éxito comercial sin evidencia.

## Posicionamiento
No vender IA por sus funciones. Mensaje central: **«Logra la foto que imaginas con el equipo que ya tienes»**. La comunicación debe demostrar problemas resueltos, tiempo y dinero ahorrados, casos antes/después y testimonios auténticos.

## Próximos pasos para Gemini / Antigravity
1. Revisar el estado actual de la rama `photodev-tools` sin reemplazar trabajo existente.
2. Separar el módulo de producto del código de producción de CAPTOORA.
3. Diseñar un prototipo de la primera receta de fotografía de producto y un flujo de compras.
4. Elaborar matriz de compatibilidad verificable y riesgos.
5. Preparar beta cerrada, criterios de aceptación, privacidad y medición.
6. No desplegar, publicar, comprar, modificar producción ni manipular datos de clientes sin revisión y autorización.
