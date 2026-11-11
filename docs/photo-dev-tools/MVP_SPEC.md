# CAPTOORA Photo Dev Tools — MVP v0.1
Fecha: 2026-11-11
Estado: propuesta para validación, no funcionalidad ya implementada

## Definición en una frase
Una aplicación web móvil que guía a un fotógrafo principiante a mejorar una foto de producto con el equipo que ya tiene, mediante instrucciones claras, una toma de prueba y una iteración de mejora.

## Usuario inicial
Fotógrafos principiantes, creadores y pequeños vendedores que necesitan fotografías de producto para redes y se frustran con parámetros técnicos o compras innecesarias.

## Problema principal
«Sé qué aspecto quiero, pero no sé configurar cámara, lente, luz ni fondo para conseguirlo, y temo gastar dinero en equipo incompatible».

## Propuesta de valor
«Logra la foto que imaginas con el equipo que ya tienes». Un asistente comprensible y contextual, no un manual genérico ni una lista de accesorios para vender.

## Flujo mínimo completo (happy path)
1. Usuario abre la PWA en teléfono o computadora.
2. Indica cámara o celular, lente, luz, accesorios y presupuesto (permitir 'no sé').
3. Describe qué quiere fotografiar y el aspecto esperado (ej. producto de lujo sobre fondo oscuro).
4. Recibe 3–5 pasos accionables usando primero su equipo, con ajustes sugeridos y explicación breve.
5. Toma una fotografía con su cámara/celular y la carga voluntariamente.
6. Recibe análisis con incertidumbre explícita y un cambio prioritario para probar.
7. Compara las tomas y califica utilidad, tiempo y resultado.

## Funciones incluidas en MVP
- Web responsiva/PWA, sin dependencia de integración directa a cámara.
- Perfil simple de equipo y presupuesto, editable y con opciones 'desconocido'.
- Guía por intención visual, cámara/accesorios y nivel de experiencia.
- Orientación técnica: exposición, apertura, ISO, velocidad, distancia, luz y fondos, según equipo.
- Carga opcional de fotografía ficticia o propia autorizada; análisis y una mejora por iteración.
- Aviso sobre límites y posibilidad de errores de IA.
- Consentimiento y privacidad; control de retención y eliminación.
- Retroalimentación del usuario sobre utilidad y resultado.

## No incluido inicialmente
- Cambio de firmware o interfaz interna de cámara.
- Control remoto universal por API/USB; solo cuando se verifique compatibilidad específica.
- Tienda, afiliados, comparador de precios en vivo ni pagos.
- Reconocimiento automático y certero de todas las cámaras y lentes.
- Plataforma general de poses, video, edición, redes y cursos.
- Uso de fotografías de clientes sin autorizaciones verificadas.

## GearCheck (siguiente módulo piloto)
Evaluar compra de accesorios por SKU y compatibilidad con fuentes oficiales. Puede probarse manualmente durante beta, antes de automatizarse. Ejemplo: distinguir disparadores Godox X2T-N y X2T-C; probar funciones específicas, no solo si 'dispara'.

## Métricas de validación
- Al menos 5–10 fotógrafos entrevistados para comprensión de problema, sin presuponer demanda.
- 5 usuarios beta capaces de completar flujo de foto de producto con fotos propias/consentidas.
- Registrar tiempo hasta obtener un resultado aceptado por cada usuario.
- Encuesta: ¿logró una foto mejor? ¿entendió qué cambiar? ¿evitó alguna compra? ¿volvería a usarlo?
- Revisar fallos de técnica, alucinaciones e instrucciones inseguras antes de escalar.
Las cifras son metas de experimento, no resultados existentes.

## Criterios de aceptación v0.1
- Se completa el recorrido sin instalar app nativa ni comprar accesorios.
- Guía brinda instrucciones ajustadas al equipo declarado, o admite explícitamente que desconoce una característica.
- La imagen solo se analiza tras carga voluntaria y consentimiento.
- Ningún usuario ve fotos ni perfiles de otro.
- No se registran secretos ni fotos sin necesidad.
- Los usuarios pueden reportar instrucciones equivocadas.

## Desarrollo y gestión
1. Validar hipótesis y recorrido con comunidad.
2. Diseñar wireframe, criterios de aceptación y evaluación.
3. Implementar prototipo aislado de producción CAPTOORA.
4. Probar con datos de ejemplo y controles de seguridad en sandbox.
5. Beta cerrada; medir, corregir y decidir si se amplía o pivota.
6. Mantener futuras funcionalidades en backlog, no en el MVP.

## Regla central
Un deploy no demuestra ajuste producto-mercado. Un MVP demuestra que un grupo de usuarios puede resolver un problema relevante con una solución mínima y medible.
