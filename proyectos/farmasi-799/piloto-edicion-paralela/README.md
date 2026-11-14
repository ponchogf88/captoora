# CAPTOORA · Edición de una foto en paralelo

## Una foto, una orden

```bash
node piloto.mjs foto /ruta/retrato.jpg blanco+grupo
```

Usa `oscuro`, `blanco`, `grupo`, `producto` o una combinación aplicable. Omite la receta para el revelado base. La guía [CAPTOORA Photo Editing](skill-captoora-photo-editing.md) explica cómo elegir la receta mirando la foto y cuándo proponer otra pasada. El comando de Terminal recibe esa decisión como argumento. Dos ejecuciones directas con el mismo archivo y prompt comparten la carpeta de resultados. Si quieres usar el CSV, agrega la columna opcional `receta` y asigna un ID nuevo al cambiar la receta de una toma que ya tiene resultados.

El comando directo usa todos los motores activos en `CAPTOORA_MOTORES` (si no está definido, usa `motores.json`). Cada variante de modelo puede tener su propia clave, por ejemplo `gemini-nano-banana`, con los campos `url`, `modelo` y `pasos`. Confirma el modelo seleccionado durante la calibración y usa `activo: false` para excluir una entrada del disparo general. Las ramas ejecutadas por Playwright empiezan en paralelo. Una rama sin calibrar o pendiente de verificación devuelve su propio error mientras las demás siguen.

Para completar el disparo único con extensiones, cada flujo necesita recibir el archivo y el prompt y devolver la descarga con su ID de motor. El comando actual ejecuta los pasos de Playwright. Las rutas Browserflow, Page Agent, extensiones nativas, Obscura, APIs y Artemis conservan sus propios requisitos de calibración. Meta, Dola AI, One y Google Fotos aparecen en la ficha como rutas previstas. Confirma la identidad de One y la compatibilidad de cada ruta con foto de referencia antes de habilitarla. El piloto usa las cuentas y cupos que ya tienes configurados. Conserva la revisión y aprobación humana antes de cualquier entrega a Pixieset.

Prepara una carpeta de trabajo en el SSD externo. Define `CAPTOORA_WORK_DIR` con su ruta absoluta y copia allí `cola.ejemplo.csv` como `cola.csv`. Selecciona un JPG del álbum en Google Fotos, identifica la fuente correspondiente en `../registros/fuentes_799.json` y descarga esa foto al SSD externo. En `cola.csv` escribe su ID único y la ruta relativa a la carpeta de trabajo. Usa el mismo archivo y `prompt.txt` para cada motor. Cada motor recibe el original. La foto sale por cuatro ramas independientes: Picsart, Grok, Gemini y ChatGPT. Meta queda disponible como quinta prueba. La decisión editorial y la entrega en Pixieset las haces tú.

```csv
foto_id,archivo
FARMASI-PRUEBA,entradas/prueba.jpg
```

`node piloto.mjs ficha FARMASI-PRUEBA` muestra la ruta absoluta, un destino por motor, el estado local y el prompt íntegro. La ficha sirve también para las rutas sin código. Conserva el encuadre completo y revisa a tamaño completo. Guarda cada imagen como `borradores/FARMASI-PRUEBA/MOTOR.ext` con el nombre de motor en minúsculas. Crea la carpeta si aún no existe. Para una corrección manual conserva el original y elige un nombre como `gemini-r02.jpg`. Compara facciones, piel, manos, ropa, encuadre y productos. Lleva solo el archivo elegido a Pixieset. Si las cuatro variantes fallan, la foto sigue pendiente.

## Browserflow en tu Chrome de escritorio

1. Abre el perfil donde Browserflow ya aparece instalado. En el editor de Browserflow crea un flujo por motor. Usa el modo de grabación y recorre manualmente una edición con un JPG de prueba.
2. Abre el editor o chat de imágenes del motor. Para adjuntar, registra el control de archivo y usa **Upload File** con la ruta absoluta que muestra la ficha. La documentación de Browserflow exige **Allow access to file URLs** para ese comando. Si el control de archivo está dentro de un iframe, usa la ruta Playwright o adjunta manualmente.
3. Graba escribir el prompt, verificar la miniatura de la foto, iniciar la edición, esperar el resultado y descargar la imagen nueva. Verifica que apuntes a la descarga del resultado y que el flujo pueda registrar la ruta descargada. En Picsart elige la función de edición con IA que acepte la foto base.
4. Para probar concurrencia, deja un motor en la pestaña activa de cada una de cuatro ventanas y arranca los cuatro flujos. Browserflow requiere una pestaña activa por ventana. Si al iniciar uno el panel detiene el otro, esa instalación debe ejecutarlos de forma escalonada. Para varias filas, importa el CSV a una hoja de Google Sheets y usa **Loop Spreadsheet Rows** como fuente del ID y la ruta. Reutiliza el prompt como variable del flujo.

Docs: https://docs.browserflow.app/guides/running-a-flow
https://docs.browserflow.app/reference/browserflow-commands/interact-with-page/upload-file

## Page Agent Ext en otra ventana o perfil de Chrome

1. Abre el perfil donde Page Agent Ext ya aparece instalado y las cuatro páginas de edición. Configura en el panel el modelo que ya usas y abre una conversación nueva en cada motor.
2. Adjunta el mismo JPG en las cuatro páginas. Si el diálogo nativo de archivos no resulta accesible al agente, resuelve esa selección manualmente. Dale al panel la ficha y esta instrucción: «En cada una de las cuatro pestañas, confirma visualmente que ya está adjunta la foto de prueba. Pega el prompt tal cual y dispara una generación por pestaña. Inicia los cuatro envíos antes de esperar las respuestas. Si un motor pide una acción de cuenta, reporta el nombre y el paso. Descarga cada imagen resultante y reporta el motor y el archivo».
3. Comprueba cada descarga y colócala con el nombre de la ficha. Esta ruta permite agrupar el trabajo entre pestañas. La subida desde el diálogo nativo y la descarga con nombre final requieren comprobación en tu instalación.

Docs: https://github.com/alibaba/page-agent/blob/main/packages/extension/docs/extension_api.md

## Control de navegador por agente

Conecta el agente al perfil de Chrome que tiene abiertas tus sesiones. Abre las cuatro páginas oficiales y dale la ficha de la foto. El agente comprueba el archivo adjunto en cada pestaña, escribe el prompt, inicia cada edición y luego vuelve a las pestañas para guardar los resultados. En una conexión que no exponga el selector de archivos de la Mac, adjunta el JPG desde tu navegador y deja al agente continuar en esas pestañas. Si el agente puede realizar varias acciones a la vez, úsalo para preparar pestañas independientes. Lo que se paraleliza sin depender de un solo cursor es la generación en los cuatro servidores, una vez enviados los encargos. Usa perfiles y sesiones de la Mac disponibles para esa conexión.

## Playwright en la MacBook

1. Abre Terminal dentro de esta carpeta y corre `npm ci`. Ejecuta `node piloto.mjs sesion` y entra tú a tus cuentas en el Chrome que abre. Pulsa Enter al terminar. El perfil se reutiliza en los siguientes lanzamientos.
2. Ejecuta `node piloto.mjs calibrar grok`, y luego Gemini, ChatGPT y Picsart. El Inspector permite elegir selectores. En cada sitio identifica los controles de adjuntar, escribir, generar y descargar. Usa selectores únicos y cercanos a la respuesta nueva. En Picsart también puede haber pasos de aplicar o exportar.
3. Copia `motores.json` a `motores.local.json`, define `CAPTOORA_MOTORES` con esa ruta y escribe ahí los pasos de cada motor. Este ejemplo es ilustrativo y los selectores deben salir del Inspector.

```json
"pasos": [
  {"accion":"foto","selector":"input[type=file]"},
  {"accion":"prompt","selector":"[role=textbox]"},
  {"accion":"clic","selector":"button[aria-label=Enviar]"},
  {"accion":"descarga","selector":"button[aria-label=Descargar]"}
]
```

Usa `elegir_foto` con el selector del botón si este abre un selector de archivos. Puedes insertar `clic` para abrir un menú o entrar a Imágenes. El último botón debe disparar una descarga directa de la imagen. Si un editor muestra un diálogo de exportación, registra sus clics intermedios.

4. Ejecuta `node piloto.mjs ejecutar FARMASI-PRUEBA`. Dispara las cuatro ramas en paralelo. Guarda un resultado por motor. Si un sitio falla conserva los demás archivos. El marcador `.pendiente` de esa rama indica que debes comprobar qué sucedió en el sitio antes de retirarlo para reintentar. Un resultado ya guardado se omite al repetir.
5. Consulta el estado con `node piloto.mjs ficha FARMASI-PRUEBA`.

Docs: https://playwright.dev/docs/input
https://playwright.dev/docs/api/class-browsertype

## Extensiones de imagen y Meta Automation

1. Haz la prueba en modo **Editar** o **Image to Image**, primero con una foto propia o de prueba. Adjunta el JPG junto al prompt. Un resultado correcto tiene que conservar la composición, la persona y los productos reconocibles.
2. Confirma si la importación admite **una referencia por fila**. Si admite un identificador local de recurso, enlaza en la fila el original importado y usa el formato CSV del fabricante. Si importa solo prompts o usa una referencia global, ejecuta una foto por cola con el original seleccionado.
3. Tu extensión instalada **Meta Automation - Auto Meta on Meta.ai** anuncia lotes de texto y descarga automática. Comprueba en el panel si tu versión admite imagen de entrada en cada trabajo. Kbach Studio anuncia referencias y flujos para Grok, Gemini y ChatGPT. Verifica la referencia en cada motor y si tu versión realmente inicia varios trabajos a la vez. Deja Picsart en su rama de Browserflow o Playwright. Guarda la salida de Meta como `meta.ext` cuando quieras compararla como extra.

Fichas: https://chromewebstore.google.com/detail/meta-automation-auto-meta/pcmcomcmgpmnpdmkdgjnipeipchbfchf
https://chromewebstore.google.com/detail/kbach-studio-ai-image-vid/jifhkmfnccgnpngdfchfhebdbmcnkldc

## Obscura

Esta ruta se refiere al navegador headless de obscura.sh. Levanta una sesión propia o usa un endpoint CDP autorizado de Obscura. Ejecuta el mismo piloto con `CAPTOORA_CDP_URL` en el entorno. Primero valida con una imagen de prueba que el navegador abre cada motor, mantiene una sesión propia autenticada, adjunta el archivo y entrega una descarga. Prueba cada uno de esos pasos, porque el soporte CDP por sí solo no garantiza que funcionen el selector de archivos, la descarga o las sesiones de estas aplicaciones. La alternativa para un motor incompatible es usar la rama en Chrome de escritorio. El endpoint debe tratarse como credencial. Si Obscura se ejecuta fuera de tu Mac, verifica también dónde recibirá el archivo.

Docs: https://www.obscura.sh/
https://playwright.dev/docs/api/class-browsertype#browser-type-connect-over-cdp

## Google Fotos en Chrome

Google Fotos sí permite edición en computadora. Permite aplicar sugerencias, corregir luz y color, usar filtros y recortar. La disponibilidad de herramientas varía. Para FARMASI conserva el cuadro completo. Usa una copia de trabajo separada del original si la interfaz web solo ofrece Guardar. Registra qué ajustes de luz y color aplicaste y guarda la exportación como `google-fotos-web.ext`. Los sliders convencionales sirven para comparar color y exposición sin mandar la foto a otro proveedor. En Chrome puedes grabar la receta con Browserflow o describírsela a Page Agent.

Docs: https://support.google.com/photos/answer/6128850?co=GENIE.Platform%3DDesktop&hl=es

## Artemis con Android y Google Fotos

1. Abre Artemis en el equipo donde está conectado tu Android. Desde Artemis o su integración en Antigravity, abre la app Google Fotos. Localiza la toma exacta con ID o nombre de archivo y comprueba la miniatura.
2. Toca **Editar**. Para la ruta por texto, busca **Preguntar** / **Ask**, pega `prompt.txt` y genera. Si la opción no aparece en esa cuenta, usa **Ajustar** con cambios suaves de luz, sombras y balance de blancos. Conserva el encuadre. Guarda con **Guardar como copia**. Si la acción solo ofrece cambiar una foto original, abre una copia separada para el piloto.
3. Pasa el resultado al SSD externo y guárdalo como `google-fotos-android.ext`. Identifica si la salida provino de Ask, Editor Mágico o ajustes convencionales. Artemis también puede seguir una receta en Chrome para Android, o abrir otro motor en su app o sitio. Deja las cuatro ramas web generando en la Mac y usa Android para esta variante adicional.
4. Para el control de cuota, registra lo que muestre el dispositivo al guardar. Google anunció 10 guardados mensuales de Editor Mágico para Android/iOS compatibles y más con Pixel o Google One Premium de 2 TB o superior. El cupo anunciado para Editor Mágico no determina la cuota de Ask Fotos o Gemini. Ask depende de elegibilidad, cuenta personal, región y configuración. Pendiente verificar lo que muestra la cuenta concreta.

Docs: https://github.com/google/artemis
https://support.google.com/photos/answer/6128850?co=GENIE.Platform%3DAndroid&hl=en
https://blog.google/products-and-platforms/products/photos/google-photos-editing-features-availability/

## iPhone

1. En Atajos crea **Enviar a CAPTOORA**, activa «Mostrar en hoja para compartir», acepta imágenes y agrega **Guardar archivo** en una carpeta accesible desde tu Mac. Desde Google Fotos comparte el JPG al atajo.
2. En la Mac asigna la ruta de ese JPG a la fila del CSV y dispara el piloto. Si quieres editar una variante en el iPhone, abre la app de ese motor, adjunta el JPG y pega `prompt.txt`. Guarda el resultado con el nombre de esa rama. El atajo hace la entrega del archivo al piloto. La navegación de las cuatro apps en paralelo corre en la Mac.

Docs: https://support.apple.com/guide/shortcuts/apd163eb9f95/ios

## Mezclar rutas

Asigna una herramienta por motor y una ejecución por par foto/motor. Un ejemplo es Browserflow para Picsart, Playwright para Grok, Page Agent para Gemini, y Playwright para ChatGPT. Ejecuta solo las ramas de Playwright así: `node piloto.mjs ejecutar FARMASI-PRUEBA grok chatgpt`. Usa la ficha para guardar las otras dos. Las salidas coinciden por ID aunque lleguen en momentos diferentes. Confirma el consumo visible de la primera edición antes de escalar. El motor entrega borradores y no se conecta a Pixieset.

## Estado de la prueba

El motor de Playwright se prueba con páginas simuladas. Los selectores de los cuatro editores comerciales quedan pendientes de calibrar en las sesiones autorizadas. Las rutas de extensiones y móvil son recetas de trabajo que se validan con una foto de prueba. El inventario de FARMASI y los archivos de revisión siguen siendo la referencia para reconciliar los pendientes y Pixieset.
