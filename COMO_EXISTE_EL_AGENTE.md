# Cómo existe Captoora en inteligencia artificial

Captoora no es un chatbot suelto ni un GPT con ese nombre.
Captoora, en IA, es **un proyecto con tres archivos + un bot que los obedece**.

## Las tres capas

| Archivo | Pregunta que responde | Se cambia |
| --- | --- | --- |
| `IDENTITY.md` | ¿Quién es esta marca? | Casi nunca |
| `AGENTS.md` | ¿Cómo se trabaja en este repo? | Cuando cambia el mapa o las reglas |
| `CONTEXT.md` | ¿Qué hay que hacer *ahora*? | Cada sesión |

No hace falta un `content.md` aparte. El contenido (captions, bios, reels) sale de Identity + Context. Si un día hay calendario largo, vive en `CALENDARIO_REDES_CAPTOORA.md` que ya existe.

## Dónde “vive” el agente

1. **Esta conversación (Grok)** — estratega. Escribe identity, copies, parches, decide.
2. **Grok Bot en tu PC** — operador. Lee los tres md, lee `apis.txt` local, publica con Browserflow.
3. **El repo** `ponchogf88/captoora` — memoria compartida. Si el Bot y yo leemos lo mismo, somos el mismo agente de Captoora.

No hay un interruptor “Agente Captoora ON” en internet. Lo enciendes cuando le dices al Bot:

> Eres el operador de Captoora. Lee IDENTITY.md, AGENTS.md y CONTEXT.md de este repo antes de hacer nada.

Eso *es* tener el agente. El nombre del agente es el nombre del proyecto. No hace falta un cuarto archivo místico.

## Cómo se lo dices a alguien (o a otro modelo)

Frase útil, honesta:

> Estoy construyendo Captoora, un estudio fotográfico en Monterrey, con un agente de IA que trabaja sobre un repo: identity de marca, reglas de trabajo y un contexto semanal. El humano decide; el bot ejecuta en el escritorio (redes, Google, archivos).

No digas “tengo una IA que es Captoora”. Di “tengo un sistema de agentes *para* Captoora”.

## Orden de lectura (siempre)

```
IDENTITY.md     ← marca
AGENTS.md       ← cómo trabajar
CONTEXT.md      ← ahora
(archivos de estrategia solo si la tarea lo pide)
```

## Plantilla para el próximo proyecto

Vive en local: `_plantilla-proyecto/` (README, IDENTITY, AGENTS, CONTEXT con `{{PLACEHOLDERS}}`).
Se clona. Se rellena el nombre. No se reescribe la filosofía.
