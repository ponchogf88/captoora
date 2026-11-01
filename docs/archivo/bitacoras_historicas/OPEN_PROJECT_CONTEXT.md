# Contexto para retomar el proyecto

Fecha: 2026-09-20

## Objetivo actual

Automatizar la creación de seis canciones con Gemini/Lyria y descargar los archivos, usando Google Sheets como fuente de prompts. Después se podrán adaptar y publicar en redes sociales.

## Plan recomendado

1. Google Sheets con una fila por canción: `id`, `titulo`, `prompt`, `genero`, `voz`, `duracion`, `estado`, `archivo`.
2. Preferir Gemini API + Lyria 3.5 para generar MP3 de forma estable y repetible.
3. Guardar los MP3 en `/Users/imac/Music/GeminiSongs/`.
4. Usar Browserflow/Browser Use solo para tareas web posteriores o si se decide automatizar la interfaz de Gemini. El inicio de sesión y cualquier CAPTCHA deben hacerse manualmente.

## Herramientas y proyectos instalados

- Browser Use: `/Users/imac/browser-use`
- OpenCut oficial: `/Users/imac/opencut`
- Dependencias web de OpenCut: `/Users/imac/opencut/apps/web/node_modules`
- OpenCut compila correctamente con `bun run build` desde `/Users/imac/opencut/apps/web`.

## Limitación de OpenCut

El iMac es `iMac17,1` con macOS 12.7.6. El runtime de Cloudflare usado por el editor local exige macOS 13.5 o superior, y Apple indica que este modelo llega oficialmente hasta Monterey. La versión web funcional puede usarse en https://opencut.app.

## Grok

- CLI `grok` conservado.
- Grok Bot oficial instalado en `/Applications/Grok Bot.app`.

## Seguridad

No guardar aquí contraseñas, tokens ni claves API. Durante una prueba anterior algunas variables de entorno con claves quedaron visibles en una salida de diagnóstico; deben revocarse y regenerarse antes de usarlas de nuevo.

## Próximo paso al volver

Confirmar si se usará Gemini API o Browserflow local. Si se elige API, crear la plantilla de Google Sheets y el script de generación/descarga con reintentos, nombres únicos y actualización de estado.
