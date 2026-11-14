---
name: captoora-photo-editing
description: Prepare and compare repeatable CAPTOORA photo edits across image models. Use when the user supplies a photo or a Google Photos export and asks for studio portrait, dark backdrop, white backdrop, group, product, multi-model comparison, or staged refinements.
---

# Edit and compare CAPTOORA photos

## Prepare the job

1. Obtain the actual source file. For Google Photos, use the selected photo's downloaded original and preserve it. A URL or a thumbnail alone is insufficient. If no image is available, deliver the prompt plan and request the file when execution is needed.
2. Inspect subject count, backdrop, lighting, visible problems, and the requested outcome. Treat backdrop and subject count as independent. Apply the group rules to any group, including groups on white or dark backdrops. If the backdrop is ambiguous, use the base rules and record uncertainty. Apply product rules when a product matters.
3. Compose one concrete editing prompt from the base and the relevant rules below. Include only corrections that the image needs and user-requested changes. Record the exact text and source identifier. Send the same file and prompt to text-capable editors for a fair first comparison. Supply equivalent adjustments for controls-only editors when feasible and label them as a different method.
4. When executing, start one independent job per enabled, verified model and collect results as they finish. Prefer the user's configured extension if it can attach the original, accept the prompt, and return the output. Use Browserflow, Page Agent, Playwright or Obscura, or an authorized API as configured. If there is no verified path for that model, report the gap. Keep the Google Photos web or Artemis/Android branch as an additional variant when configured. Keep unavailable, authentication-required, quota-limited, and failed jobs visible. Pause before incurring a charge the user has not authorized. Never name a model version based solely on the brand of the editor.
5. For each result, record source ID, provider, model as shown (or unknown), route, prompt, pass, state, and saved file. Use distinct names such as `PHOTO_ID/gemini__MODEL__r01.png` using safe filename characters. Keep the originals and each previous variant. Retry only the failed or requested branch once its submission state is clear.

## Build the editing prompt

Use this base in Spanish and append any applicable instructions below as direct requests to the image editor.

> Edita la fotografía adjunta y devuelve una sola imagen editada. Conserva la proporción, el encuadre y la composición. Mantén los rasgos, la expresión, la edad aparente, la textura de piel, el cabello, las manos, la pose y la ropa de cada persona. Aplica un revelado fotográfico natural. Ajusta exposición y balance de blancos con moderación y conserva la dirección de la luz. Trabaja con el detalle visible de la toma. Conserva la escena y los elementos del fondo salvo que se pida una corrección específica.

| Condition | Instructions to append when applicable |
| --- | --- |
| Dark backdrop | Mantén el fondo oscuro y su gradación. Recupera solo el detalle visible en sombras de la persona y conserva los negros. Haz legible el borde natural de pelo y ropa sin crear halos, bordes artificiales ni aclarar todo el fondo. |
| White backdrop | Neutraliza la dominante del fondo y suaviza desigualdades de iluminación. Conserva la sombra natural de contacto y el detalle en pelo, piel y prendas blancas. Respeta la separación entre la persona y el fondo. |
| Group | Conserva la cantidad, las posiciones y la identidad de todas las personas. Equilibra la iluminación de cada rostro respetando su tono de piel y su expresión. Conserva miradas, oclusiones, manos y rostros de los extremos del encuadre. |
| Product or visible branding | Mantén la forma, el empaque, el color y la posición del producto. Conserva textos y logotipos tal como se ven y deja intactos los detalles ilegibles. |

## Refine and review

- Start with one pass per model. Inspect the original and results side by side at full size for crops, faces (all faces in groups), hands, hair edges, skin texture, clipped highlights, and visible branding. Mark identity changes or invented details for rejection before judging style.
- For a localized issue, send a fresh instruction naming the exact area, desired change, and elements to preserve. Use the original for identity drift, hallucinations, or composition errors. Use a satisfactory variant for a small tonal adjustment when the editor supports it, and record that variant as its input. In a controlled second round, give the same correction and same input to the models being compared.
- Example for a white-background group after a strong first pass: «Aclara solo la franja gris del fondo a la izquierda. Conserva el borde del cabello de la persona de ese lado, las sombras de contacto y todos los rostros tal como están».
- Show the original plus labeled variants, pending branches, and the exact prompts used. Record the user's selection or revision request by photo and variant. Leave upload to Pixieset subject to the user's selection and delivery instruction.

## Invocation to reuse

> Usa la guía de edición CAPTOORA con esta fotografía. Identifica si es individual o de grupo y si el fondo es blanco, oscuro u otro. Prepara un solo prompt base con las reglas aplicables. Si los motores están configurados, envía el mismo original y la misma instrucción a todos los modelos habilitados con cupo disponible. Devuélveme el original y cada variante identificada por proveedor y modelo. Marca las ramas que requieran intervención y propone una segunda pasada solo donde haya un defecto concreto. Déjame elegir qué versión queda aprobada.
