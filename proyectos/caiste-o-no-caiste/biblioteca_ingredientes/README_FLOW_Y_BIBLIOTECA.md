# Workflow Oficial (`iMac + CapCut Pro` en Redmi Note 8) y `Biblioteca de Ingredientes` — `¿Caíste o no caíste?`

> **Estado actual del proyecto (`🧪 EN PRUEBA / HIPÓTESIS`):** Ya tienes tu primer Short V2 dinámico **completamente renderizado y sin tocar** en el teléfono ([`CAISTE_SHORT_01_P4_CFE_V2_DYNAMIC.mp4`](../renders/CAISTE_SHORT_01_P4_CFE_V2_DYNAMIC.mp4)) + esta primera caja de **Ingredientes Reutilizables** lista para que tú lo decores y pruebes retención real antes de escalar los 30 videos.

---

## 1. ¿En qué paso exacto vamos del Workflow? (Mapa de 2 Estaciones y 6 Pasos)

Tu flujo original (`soul-youtube` + tu compra de **CapCut Pro $30 MXN**) ahora queda dividido limpio en **dos estaciones sin trabajo duplicado**:

| Paso | Estación | Qué ocurre exactamente | Estado hoy en `P4 CFE` |
| --- | --- | --- | --- |
| **1. Guion + Candados** | 🖥️ iMac | Guion humano (`7 trampas + 3 reales`, tiempos `5/7/9s`, tip **Segundo Robado** en P4 y P8). | ✅ **LISTO** (`piloto_01_nivel_facil.json`) |
| **2. Mundo 3D Vivo** | 🖥️ iMac | Escena `Three.js + HyperFrames` con `Antigravity` caminando por los rieles ascendentes + cámara viva + `Grok` robando el `2` en 3D. | ✅ **LISTO** (`hf_v2_p4/`) |
| **3. Audio Maestro** | 🖥️ iMac | Locución ElevenLabs + reloj + chime + cama marimba en pista WAV verificada (`short_P4_cfe_master.wav`). | ✅ **LISTO** (`audio/`) |
| **4. Render Base Dinámico + Ingredientes** | 🖥️ iMac | MP4 vertical `1080×1920 @ 30fps` limpio + tu **Biblioteca de Ingredientes** (SFX teclado, Halos Gemini/Antigravity, stickers PNG referentes). | ✅ **LISTO** (`V2` + Pack #1) |
| **👉 5. Condimentos (`CapCut Pro` absorbio a `Captions`)** | 📱 **Redmi Note 8** | **TÚ ESTÁS AQUÍ.** En CapCut Pro pones: **(a)** subtítulos dinámicos tipo máquina + **(b)** SFX de teclado mecánico cremoso + **(c)** sticker referente visual del caso (ej. paquete aduana/CFE) + **(d)** Halo de fondo por nivel o blanco hueso final. | 🟡 **LISTO PARA TI EN EL TELÉFONO** |
| **6. Escalar Video Largo (`10 min`) → `Opus Clip`** | 🖥️ iMac + 🌐 Opus Clip → 📱 CapCut | **DESPUÉS (no aplica hoy en este Short):** cuando grabemos los episodios largos `16:9` de 10 min, **`Opus Clip`** parte el video largo en 10 Shorts con **captions apagadas** (`motion/zooms ON`), y luego cada Short baja a **CapCut Pro** para sus subtítulos y condimentos. | ⏳ **DESPUÉS de validar retención** |

### Respuesta directa sobre `Captions` y `Opus Clip`
- **¿Cuándo entra la app `Captions`?** **YA NO la necesitas pagar aparte:** **CapCut Pro** hace los subtítulos dinámicos animados + fuente gruesa + efectos de máquina de escribir mucho mejor por `$30 MXN/mes`.
- **¿Cuándo entra `Opus Clip`?** **Hasta que hagamos el Video Largo horizontal de 10 min.** Para Shorts hechos uno por uno en vertical (`9:16`) como este `P4 V2`, **te brincas Opus Clip** y entras directo a **CapCut Pro** (Paso 5).

---

## 2. ¿Qué quedó resuelto de tu "80% que ya teníamos vs 20% faltante"?

Sí quedó registrado y auditado completo en [`proyectos/waters-serie/INVENTARIO_ARSENAL_Y_PIPELINE_PRODUCCION.md`](../../waters-serie/INVENTARIO_ARSENAL_Y_PIPELINE_PRODUCCION.md):

- **Tu ~80% ya instalado y funcionando en esta iMac:** `HyperFrames` (`v0.8.223`), `Remotion + Three.js + @react-three/fiber` (`waters-3d-studio`), motor de voces/SFX (`waters_audio_engine.py`), `FFmpeg` + `ffprobe`, `adb` + `scrcpy` directo a tu Redmi Note 8 + CapCut Pro, y **`GSAP`** + planos continuos tipo **`onetake`** (**ya activos** dentro de este V2).
- **Tu ~20% pendiente para siguientes iteraciones:**
  1. **`WhisperX`** (alineación exacta palabra-por-palabra cuando automatices subtítulos en Mac).
  2. **`react-postprocessing + Theatre.js`** (cuando pasemos a renders 3D pesados de Remotion para episodios largos).
  3. **`Lemo-Opuscar / Impeccable`** (presets de color y acabado visual adicionales).

---

## 3. Catálogo de Tu Pack #1 (`Biblioteca de Ingredientes`)

Todos los archivos están aquí y ya copiados en tu Redmi Note 8 en `/sdcard/Movies/Captoora_CapCut/03_BIBLIOTECA_INGREDIENTES/`:

1. **`01_sfx_teclado_mecanico/`** (`.mp3` para CapCut y `.wav` 48 kHz para HyperFrames/macOS)
   - `sfx_teclado_creamy_rafaga_3s` · ráfaga cremosa de `3 s` rematada con golpe grave `Enter` (para títulos).
   - `sfx_teclado_creamy_rafaga_6s` · ráfaga natural de `6 s` con micro-pausas entre palabras (para mensajes SMS/WhatsApp).
   - `sfx_teclado_tecla_suelta_01..03` · 3 variaciones de tecla suelta PBT.
   - `sfx_teclado_enter_thock` · golpe grave Enter/Spacebar para remate de tarjeta.
   - `sfx_pop_burbuja_ui`, `sfx_whoosh_suave_tarjeta`, `sfx_guardrail_dorado_chime`.
2. **`02_halos_dinamicos_por_nivel/`** (`MP4 1080×1920 @ 30fps · Loop perfecto 8.0 s`)
   - `halo_00_blanco_hueso_final.mp4` — **Blanco hueso cálido (`#FDF6EA`)** con brillo oro miel suave (cierre + Guardrail).
   - `halo_01_facil_gemini_pastel.mp4` — **Nivel Fácil (`ChatGPT`)**: gradiente cambiante estilo Gemini en azul cielo, menta y crema.
   - `halo_02_medio_terracota_ambar.mp4` — **Nivel Medio (`Claude`)**: terracota, ámbar y lavanda cálida.
   - `halo_03_dificil_antigravity_halo.mp4` — **Nivel Difícil (`Grok` / Halo Antigravity)**: violeta, cian y rosa sobre ciruela (funciona de fondo o en `Mezclar → Pantalla` en CapCut Pro).
3. **`03_referentes_visuales_casos/`** (`PNG 1080×1080 RGBA con fondo transparente`)
   - Los 10 stickers ilustrados del Piloto 01 (`ref_P1` a `ref_P10`), incluyendo **`ref_P8_dhl_paquete_aduana.png`** (paquete detenido en barrera aduana + `$350` + sin guía oficial) y **`ref_P4_cfe_recibo_luz_falso.png`**.
4. **`04_plantilla_texto_dinamico_teclado/`**
   - `typewriter_mecanico_overlay.html`: plantilla lista en HyperFrames con texto dinámico letra por letra + SFX cremoso.

---

## 4. Receta Rápida en CapCut Pro (Redmi Note 8 · 4 Pasos)

1. **Importa base:** abre proyecto nuevo en CapCut Pro con `01_CAISTE_SHORTS/CAISTE_SHORT_01_P4_CFE_V2_DYNAMIC.mp4`.
2. **Subtítulos dinámicos + Teclado cremoso:** activa `Texto → Subtítulos automáticos` con plantilla animada palabra por palabra, y coloca en la pista de audio `sfx_teclado_creamy_rafaga_6s.mp3` cuando sale el mensaje + `sfx_teclado_enter_thock.mp3` al golpe de `¡ES TRAMPA!`.
3. **Referente visual (`Superposición`):** agrega `ref_P4_cfe_recibo_luz_falso.png` como sticker flotante (`Escala` con rebote + `sfx_whoosh_suave_tarjeta.mp3`) para reforzar visualmente el caso sin cubrir la cara de `Antigravity`.
4. **Halo de nivel opcional (`Superposición → Mezclar`):** si quieres probar fondo/halo vivo, añade `halo_01_facil_gemini_pastel.mp4` o `halo_00_blanco_hueso_final.mp4` con opacidad suave (`15–25%` o recorte de fondo) y exporta para subir a TikTok / Shorts / Reels.
