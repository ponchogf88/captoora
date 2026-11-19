# 🎬 Biblioteca de Clips Reciclables — Serie ¡WATERS! (Chuy + Agy)

> **Principio clave:** Todos los clips base se generan **sin texto quemado** y **sin audio hablado** (`no spoken dialogue audio`). Así se reciclan en los 100 episodios cambiando únicamente la voz en español, las pantallas B-Roll en Remotion y los subtítulos en Captions.

## 📂 Estructura de la Biblioteca
- `chuy_reacciones/` — Planos de Chuy reaccionando, preguntando, sudando o sorprendiéndose.
- `agy_explicando/` — Planos cerrados del **puro monito Agy** sobre el escritorio junto al monitor (estilo ping-pong).

---

## Inventario de Clips Base

### 1. Reacciones de Chuy (`chuy_reacciones/`)
| Archivo | Emoción / Uso | Origen |
| :--- | :--- | :--- |
| `chuy_01_susto_alerta.mp4` | Susto inicial `0:00` (`¡WATERS!`) + lluvia nocturna | Flow (`pose_01_susto.jpg`) |
| `chuy_02_angustia_sudor.mp4` | Preocupación cerrando ojos + gota de sudor | Flow (`pose_01_susto.jpg`) |
| `chuy_03_sorpresa_silla.mp4` | Asombro total levantándose de la silla | Flow (`pose_02_experto_mascotita.jpg`) |
| `chuy_04_escucha_atento.mp4` | Escucha y asiente mientras Agy explica | Flow (`pose_02_experto_mascotita.jpg`) |
| `chuy_05_cierre_sonrisa.mp4` | Sonrisa cálida señalando abajo al CTA | Flow (`pose_03_cta_mascotita.jpg`) |
| `chuy_06_feliz_celebrando.mp4` | **¡GOZANDO!** Chuy riéndose, festejando con los brazos arriba / puño de victoria | Flow (`pose_03_cta_mascotita.jpg`) |
| `chuy_07_alivio_cafe.mp4` | **¡ALIVIO!** Suspiro de alivio, sonrisa relajada recargado en la silla | Flow (`pose_02_experto_mascotita.jpg`) |

### 2. Planos del Puro Monito Agy (`agy_explicando/`)
| Archivo | Emoción / Uso | Cómo generarlo |
| :--- | :--- | :--- |
| `agy_01_solo_explicando.mp4` | Agy solo sobre escritorio frente al monitor explicando con manos y lente cian | Flow (Imagen 9:16 -> Video) |
| `agy_02_solo_alerta_roja.mp4` | Agy solo frente al monitor señalando alerta roja urgente | Flow (Imagen 9:16 -> Video) |
| `agy_03_solo_feliz_guino.mp4` | Agy solo saltando feliz con lente dorado + guiño final | Flow (Imagen 9:16 -> Video) |

---

## Flujo Estándar de Producción (Empanizar → Guisar → Sazonar)
1. **Empanizar (Google Flow):** Generar clips limpios (`9:16`, sin texto, sin diálogo). Guardar en `biblioteca_clips/`.
2. **Guisar (Remotion):** Ensamblar cortes Ping-Pong (`1s–6s`), silenciar audio original de Flow, montar voz en español + SFX + monitores dinámicos del episodio.
3. **Sazonar (Captions):** Exportar `.mp4` de Remotion y aplicar subtítulos dinámicos sobre la voz en español.
