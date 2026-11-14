**Piloto de edición paralela (14 nov):** [Motor, prompt y guías por herramienta](piloto-edicion-paralela/README.md).

> **Fórmula de edición actual (5nov):** [proceso exacto, parámetros y scripts](FORMULA_EDICION_ACTUAL.md). Incluye corrección de blancos, restauración original, prompts intermedios y límites; no equivale a aprobación.

# FARMASI 799 — paquete de continuidad para Antigravity y otros editores

**Entrada:** [CONTINUAR.md](CONTINUAR.md). **Prompts reales:** [148 ejecuciones legibles](prompts/EJECUTADOS_EXACTOS.md) y [JSON exacto](prompts/ejecutados_exactos.json). **Métodos actuales:** [RECETAS_VIGENTES.md](prompts/RECETAS_VIGENTES.md).

Este paquete permite entender y continuar el trabajo, no convierte un prompt en un editor ni transfiere permisos de Drive o cuota entre proveedores. Las fotografías quedan en Drive; GitHub contiene texto, scripts, enlaces estables, estados y hashes.

## Estado comprobado

- 799 fuentes JPG inventariadas con ID y enlace de Drive.
- 144 JPG aprobados y verificados en Drive.
- 15 JPG nuevos o anteriores en revisión; no aprobados automáticamente.
- 150 prompts exactos recuperados; incluyen intentos bloqueados sin imagen cuando están identificados así.
- 193 originales inspeccionados con SHA-256; no afirmar que los 799 tengan hash comprobado.
- 3 fuentes bloqueadas por herramienta; no cuentan como producción.
- Lote01 de veinte: rechazado por cabello y contornos. No reutilizar sus máscaras.
- Prioridad e instrucciones actuales en CONTINUAR.md; el calendario nocturno del4nov es historico y no autoriza nuevas activaciones.

El registro distingue originales, aprobadas, pendientes, bloqueadas y rechazadas. Una versión histórica no cuenta como otra fotografía.

## Leer en este orden
1. [CONTINUAR.md](CONTINUAR.md): cola y reglas de ejecución vigentes.
2. [ESTADO_ACTUAL.md](ESTADO_ACTUAL.md) y [fuentes_799.json](registros/fuentes_799.json): qué existe y qué falta.
3. [RECETAS_VIGENTES.md](prompts/RECETAS_VIGENTES.md): cómo reproducir métodos aprobados sin inventar rostros o letras.
4. [EJECUTADOS_EXACTOS.md](prompts/EJECUTADOS_EXACTOS.md): prompts históricos completos, identificados por fuente/ejecución.
5. [BITACORA_FARMASI_799.md](BITACORA_FARMASI_799.md): decisiones, fallos, aprobaciones y cambios de método.
6. [DIRECCION_Y_CALIDAD.md](DIRECCION_Y_CALIDAD.md): referencias, sujetos, texturas y revisión.

Las correcciones locales v03/v04 y las pruebas del bebé no tienen un nuevo prompt generativo: sus recetas y manifiestos describen las operaciones realmente aplicadas. No atribuir GPT Image2 a llamadas cuyo modelo no fue expuesto. No atribuir detalle de sensor a un fondo ampliado.

## Carpetas verificadas
- [Originales de la selección](https://drive.google.com/drive/folders/1fnUJljKnCMEuGlozJg8wxVTEDnWAI9lv).
- [Última aprobada JPG](https://drive.google.com/drive/folders/1O70rKDMLZfC9d_eY-0Ugh7MAl-iZuw11).
- [Última aprobada PNG](https://drive.google.com/drive/folders/1nHp9UEYFBFMngGT6QRldBGlsxKqRzAG-).
- [Historial fuera de entrega](https://drive.google.com/drive/folders/1PyB8uIJMFq0_cP1kLV15EC_ch5ax6PzD).

No hay entrega Pixieset verificada. Ver [SINCRONIZAR_GITHUB.md](SINCRONIZAR_GITHUB.md) para mantener visible la información en la rama principal.
