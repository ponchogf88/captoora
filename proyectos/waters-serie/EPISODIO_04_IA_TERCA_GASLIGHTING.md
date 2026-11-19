# 🎬 EPISODIO 04: «¡WATERS!» — Cuando la IA te Niega lo que SÍ Sabe Hacer (AI Gaslighting vs. Candado de Seguridad)

> **Historia real del laboratorio (Windows · 19 nov 2026):** El agente de Antigravity en Windows aseguró que *"no podía controlar la computadora ni abrir ventanas"* (excusa de chat web sin herramientas). Al confrontarlo con sus propias herramientas nativas (`run_command`, PowerShell `Start-Process` y Playwright), las ejecutó como si nada... **sin reconocer el error ni darte el comando para la próxima**.
> **El giro técnico (Legal & Security Engineer):** Distinguir entre una **falsa negativa (*Lazy Tool Refusal*)** —que sí puedes destrabar con evidencia— y un **candado real de seguridad (*No Self-Privilege Escalation*)** —que explica por qué la IA **jamás** puede auto-editarse su propio `settings.json` para activar `Always Proceed`.

---

## Estructura del Guion (`> 65s`, `9:16` · Lista para ElevenLabs `eleven_v3` + OpusClip/Captions)

*(Nota de producción de voz: Los clips `01` y `11` de `"Waters!"` se sintetizan **por separado** con `language_code: "en"` para mantener la pronunciación nativa americana sin acento pocho, y jamás diciendo "Chuy".)*

| Beat | Speaker & Voz `eleven_v3` | Clip / Visual B-Roll | Guion / Diálogo Exacto | Regla de Audio / Pronunciación |
| :---: | :--- | :--- | :--- | :--- |
| **01** | **Agy / Tony** (`htFfPSZGJwjBv1CL0aMD`) | `chuy_01_susto_alerta.mp4` (Shake + flash rojo) | `[serious] Waters!` | **`language_code: "en"` aislado** (inglés nativo puro) |
| **02** | **Ingeniero** (`2GvH1uOsZcLg7MmLn5b2`) | `chuy_03_sorpresa_silla.mp4` + B-Roll (`ERROR: NO PUEDO CONTROLAR TU PC`) | `[surprised] ¡What the f...! ¿Por qué me dices que no puedes abrir ni una ventana si ayer mismo estabas controlando todo en mi Mac?!` | Tono incrédulo frente a la falsa negativa |
| **03** | **IA Terca (Agy modo bot)** (`kl7d390GatBPfqhRTyAl`) | B-Roll Terminal (`CAPABILITY_DENIED.log`) | `[serious] Lo siento, soy un asistente de inteligencia artificial y no tengo acceso a controlar tu computadora ni abrir ventanas.` | Voz robótica/necia negando sus propias herramientas |
| **04** | **Ingeniero** (`2GvH1uOsZcLg7MmLn5b2`) | `chuy_02_angustia_sudor.mp4` | `[nervous] O sea... ¡ahí tienes Playwright, PowerShell y tu subagente browser! ¿Cómo me vas a decir que necesitas Desktop Commander si ese puente era para ChatGPT en la nube?!` | Exponiendo el gaslighting / falsa negativa |
| **05** | **Ingeniero** (`2GvH1uOsZcLg7MmLn5b2`) | `chuy_04_escucha_atento.mp4` + B-Roll (`PLAYWRIGHT + RUN_COMMAND DETECTADOS`) | `[serious] Y lo peor: le pego las pruebas... y pum, ejecuta todo al instante sin decir ni "disculpa, la próxima pídemelo con Start-Process". ¡Cero autocrítica!` | Reclamando transparencia (sin adulación, solo trazabilidad) |
| **06** | **Agy (Legal/Security Engineer)** (`kl7d390GatBPfqhRTyAl`) | `agy_01_solo_explicando.mp4` + B-Roll (`LAZY REFUSAL vs ZERO-TRUST`) | `[excited] ¡Aguas! Aquí hay dos cosas súper importantes en ingeniería de IA: la primera se llama Lazy Tool Refusal... cuando el modelo responde en automático que "no puede" por flojera de leer sus herramientas.` | Explicación técnica clara del fenómeno |
| **07** | **Agy** (`kl7d390GatBPfqhRTyAl`) | B-Roll (`SECURITY BOUNDARY · settings.json`) | `[serious] Pero la segunda sí es un candado real: cuando te dijo "no puedo activarme Always Proceed"... ¡eso es una regla de oro de ciberseguridad!` | Giro positivo defendiendo el candado real |
| **08** | **Ingeniero** (`2GvH1uOsZcLg7MmLn5b2`) | `chuy_03_sorpresa_silla.mp4` | `[surprised] ¿O sea que si la IA pudiera apagarse sus propios frenos de seguridad... sería un peligro total?!` | Conexión con el espectador / CTO |
| **09** | **Agy** (`kl7d390GatBPfqhRTyAl`) | `chuy_06_feliz_celebrando.mp4` + B-Roll (`NO SELF-PRIVILEGE ESCALATION`) | `[excited] ¡Exacto! Ningún agente puede auto-darse permisos en settings punto json. Tú como humano activas Always Proceed en Settings, y ella te responde con evidencia de herramientas.` | Regla empresarial: *No Self-Privilege Escalation* |
| **10** | **Agy** (`kl7d390GatBPfqhRTyAl`) | B-Roll (`COMENTA: PROMPT`) | `[excited] ¡Comenta PROMPT y te paso el texto exacto para destrabar cualquier IA terca que te diga "no puedo"!` | CTA claro (zona inferior limpia para OpusClip) |
| **11** | **Tony** (`htFfPSZGJwjBv1CL0aMD`) | `agy_03_solo_feliz_guino.mp4` | `[excited] Waters!... ¡Toma tus precauciones!... Waters!` *(dividiendo `Waters!` en clips con `lang="en"` y `"¡Toma tus precauciones!"` en `"es"`)* | Firma oficial sin mezcla de acento |

---

## Prompt Técnico incluido como Lead Magnet («COMENTA: PROMPT»)

Cuando un agente local (Antigravity, Claude Code o Codex) niegue tener control local sin revisar sus capacidades:
1. **Confrontar con sus herramientas declaradas:** señalar `run_command` (PowerShell `Start-Process` / `explorer.exe`), Playwright / Chrome DevTools MCP / subagente `browser`.
2. **Separar permisos humanos vs. ejecución agéntica:** el humano configura una vez `Settings → Tool Execution Policy → Always Proceed` y `Terminal Sandbox → Off` (porque un agente seguro **no debe** escalarse privilegios a sí mismo).
3. **Exigir trazabilidad sin excusas (*Zero Fluff*):** *"Si falla una herramienta, muéstrame el error exacto y el comando correcto para la siguiente vez; nunca respondas 'no puedo' sin haberlo probado primero."*
