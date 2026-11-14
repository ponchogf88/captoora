# Extensiones de Trường Nguyễn para el piloto FARMASI

Revisión del 14 de noviembre de 2026. [Catálogo del desarrollador](https://kylenguyen.me/).

| Extensión | Edición con foto base | Evidencia |
|---|---|---|
| [Grok](https://chromewebstore.google.com/detail/grok-automation-grokcom-a/kpeloeongamilgpjaibcdmldenfmdngp) | Imagen a imagen | El manual permite adjuntar el original y usarlo para editar. |
| [Veo / Flow](https://chromewebstore.google.com/detail/veo-automation-google-flo/fnmijgmnjpealnnadjpjilaanhhambeb) | Imagen a imagen | El manual lista Nano Banana 2 Lite, Pro y 2 en Flow. Veo es la rama de video. |
| [Muse](https://chromewebstore.google.com/detail/muse-automation-auto-muse/jjcigbgkfmobiegbfipoaolediphpljp) | Imagen a imagen | La ficha describe importación CSV de prompts, concurrencia y edición por etapas. |
| [Seedance / Dreamina o Jimeng](https://chromewebstore.google.com/detail/seedance-automation-auto/cniciedfdaehibebgdeeiobndignobnb) | Imagen a imagen | Seedream para imágenes. Seedance para video. |
| [Dola](https://chromewebstore.google.com/detail/dola-automation-auto-dola/plhanhmohieglgmgmohpncemiinnfobn) | Imagen a imagen | Seedream 4.5 y 5.0 Pro; carga de originales y encadenamiento opcional. |
| [Meta AI](https://chromewebstore.google.com/detail/meta-automation-auto-meta/pcmcomcmgpmnpdmkdgjnipeipchbfchf) | Modo presente en 2.3.0.0 | Se inspeccionó el código instalado en la MacBook. Incluye el formulario de imagen a imagen; falta verificar ejecución y descarga reales. |
| [Vids](https://chromewebstore.google.com/detail/vids-automation-auto-veo/caiompjhmpmodfbfdbihlkbbeijgpial) | Texto a imagen documentado | Adjuntar imágenes está descrito para video. Falta confirmar que devuelva una foto editada. |
| [Higgsfield](https://chromewebstore.google.com/detail/higgsfield-automation-aut/nfokangfiojilfhfelhhbmbdibdndndp) | Imagen a imagen | La ficha describe transformación de imágenes por lotes. |
| [Gemini](https://chromewebstore.google.com/detail/gemini-automation-auto-ge/jlhacppkbcmonaanlkbgipimelfbjgpb) | Imagen a imagen | Usar la ficha enlazada por el desarrollador. Registrar la etiqueta del modelo visible. |
| [ChatGPT](https://chromewebstore.google.com/detail/chatgpt-automation-auto-c/nocgcjgldlpeffhdhfjejhcgjbgcmpgb) | Imagen a imagen | La ficha describe edición por lotes y reutilización opcional de la última salida. |
| [Qwen](https://chromewebstore.google.com/detail/qwen-automation-auto-qwen/gfolnjohlchemjcllgjgbfhaafdpkenk) | Texto a imagen documentado | Falta confirmar edición de un JPG de entrada en la extensión. |
| [Vibes](https://chromewebstore.google.com/detail/vibes-automation-auto-met/mikmoieklgpbgikeemkfffncmcmnhhab) | Texto a imagen documentado | Falta confirmar edición de un JPG de entrada en la extensión. |
| [Canva](https://chromewebstore.google.com/detail/canva-automation-auto-can/henpgladfodcidlnpdadgdlamegalije) | Imagen a imagen | La ficha describe edición por lotes y encadenamiento. |

El catálogo también enlaza [AI Image Upscaler](https://upscale.kylenguyen.me) como herramienta de terceros o de la comunidad. En Chrome Web Store aparecen fichas adicionales del mismo editor para [Gemini](https://chromewebstore.google.com/detail/gemini-automation-auto-ge/kjifccceihodcbogiddghemljmeamijg) y [VEO](https://chromewebstore.google.com/detail/veo-automation-auto-veo-n/hnncdbmjgdcnibomfgiiochojgjfbphg) / [Automation for Google VEO](https://chromewebstore.google.com/detail/automation-for-google-veo/mlbkhhifblaffpihabicadigmfoembdk). La comparación registra el proveedor y modelo visible para evitar contar fichas alternativas como modelos distintos. No se encontró en el catálogo una extensión dedicada a DALL·E ni un panel único que dispare todos los proveedores.

## Cuota y prueba

El desarrollador documenta un tope diario de **prompts** en su plan gratuito y que Max amplía los límites. Quedan por comprobar el valor de **10**, si el contador gratuito es compartido o por extensión y la cuota del servicio de destino. El manual de Flow distingue cantidad de salidas por prompt de cantidad de prompts. [Cuota y problemas de Dola](https://github.com/trgkyle/dola-automation-user-guide#-troubleshooting) · [Plan y salidas por prompt en Flow](https://github.com/trgkyle/veo-automation-user-guide).

Para probar la compatibilidad, usar una sola imagen de prueba con el [prompt común](prompt.txt), seleccionar imagen a imagen, solicitar una salida y comprobar que el archivo original aparece adjunto. Registrar modelo visible, archivo descargado, si el contador del panel cambia y qué límite muestra el proveedor. Para comparar en paralelo, cada extensión parte del mismo original. Para encadenar retoques, partir de la variante elegida. Mantener la revisión y aprobación en manos del fotógrafo antes de Pixieset.

Los manuales describen flujos dentro de cada servicio. La activación con una sola orden a través de todos los paneles queda pendiente de integrar y validar. La inspección local de Meta fue de solo lectura y el catálogo documenta capacidades anunciadas. No se ejecutaron generaciones con fotografías de la sesión.

[Guía del piloto](README.md) · [Grok](https://github.com/trgkyle/grok-automation-user-guide) · [Gemini](https://github.com/trgkyle/gemini-automation-user-guide) · [Dola](https://github.com/trgkyle/dola-automation-user-guide).
