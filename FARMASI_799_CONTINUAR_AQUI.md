# FARMASI799 — empezar aquí (Antigravity / cualquier modelo)

**Rama canónica: main. Carpeta: proyectos/farmasi-799. Actualizado5noviembre2026.**

El paquete antes estaba únicamente en la rama farmasi/continuidad-edicion-799; main no lo contenía. Esta entrada corrige el problema de descubrimiento y sustituye instrucciones de producción nocturna vencidas.

0. [FÓRMULA ACTUAL: proceso, parámetros, código y límites](proyectos/farmasi-799/FORMULA_EDICION_ACTUAL.md).
1. [CONTINUAR: instrucciones operativas actuales](proyectos/farmasi-799/CONTINUAR.md).
2. [Biblioteca de prompts históricos completos](proyectos/farmasi-799/prompts/EJECUTADOS_EXACTOS.md) — [JSON original](proyectos/farmasi-799/prompts/ejecutados_exactos.json).
3. [Recetas vigentes, parámetros y plantillas separadas](proyectos/farmasi-799/prompts/RECETAS_VIGENTES.md).
4. [Bitácora de decisiones, errores y aprobaciones](proyectos/farmasi-799/BITACORA_FARMASI_799.md).
5. [Estado verificado](proyectos/farmasi-799/ESTADO_ACTUAL.md) y [799fuentes/estados](proyectos/farmasi-799/registros/fuentes_799.json).

Estado registrado al5noviembre:144fuentes aprobadas,625pendientes,12rechazadas,3bloqueadas y15en revisión. Hay candidatos de reemplazo registrados por separado; no contarlos como nuevas fuentes ni como aprobados. Consultar los JSON de estado para cambios posteriores.

**Las últimas correcciones NO se generaron con un prompt.** Para caras/etiquetas/cabello y bebé se usaron píxeles originales con regiones o curvas documentadas. No regenerar esos detalles. Los prompts históricos, por sí solos, no garantizan la misma identidad o calidad en otro motor.

Leer los documentos anteriores y abrir las fuentes/referencias de Drive antes de producir. Este paquete no trae fotos, credenciales, API ni un generador masivo autónomo. Los validadores son de solo lectura y no consumen generación. Si el editor no protege sujetos/etiquetas o no hay acceso a Drive, registrar el bloqueo sin fabricar una entrega. No instalar/comprar/cargar créditos ni eludir filtros.

Para verificar el paquete sin editar imágenes:
```sh
cd proyectos/farmasi-799
python3 scripts/validar.py
python3 scripts/revisar_relevo.py
python3 scripts/revisar_relevo.py --source 'DSC08258.JPG'
```

La biblioteca exacta no se modifica al redactar plantillas nuevas. Mantener esta copia de main actualizada después de cada entrega: [SINCRONIZAR_GITHUB](proyectos/farmasi-799/SINCRONIZAR_GITHUB.md).
