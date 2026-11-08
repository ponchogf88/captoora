# Ley Captoora — Reglas Inquebrantables de Operación

El texto visual extendido está en [docs/LEY_VISUAL_CAPTOORA.md](docs/LEY_VISUAL_CAPTOORA.md).

## 1. REGLA DE ORO DE CERO ELIMINACIÓN (`ZERO DELETE POLICY` — 7 DE NOVIEMBRE DE 2026)
- **Queda terminantemente prohibido borrar o eliminar cualquier archivo, fotografía, video, script, documento o bitácora.**
- Si cualquier archivo o carpeta debe retirarse de la raíz o de una vista activa para mantener el orden, **obligatoriamente se mueve íntegro a la bóveda `historico_y_archivos/`** (tanto en el repositorio como en la nube), preservando su contenido y registrándolo en [`historico_y_archivos/INDICE_ARCHIVO_HISTORICO.md`](historico_y_archivos/INDICE_ARCHIVO_HISTORICO.md).

## 2. ARQUITECTURA MULTI-EQUIPO (MACBOOK PRO 256GB vs iMAC 2015)
- **MacBook Pro (256 GB SSD · `/Users/user`):** Consola ligera de dirección, código y despliegue web (`captoora.studio`). Prohibido descargar lotes pesados de fotos o videos crudos al disco local.
- **iMac 2015 (SSD Externo + HDD Interno · `/Users/imac`):** Estación de fuerza bruta para programas pesados (Canva, TikTok, procesamiento batch) y nodo conectado vía ADB al **Xiaomi Redmi Note 8 (`160305c5`)** con **Artemis** y la cámara **Eufy S350 (Anker) 24/7**.
- **Rutas Dinámicas Obligatorias:** Prohibido usar rutas fijas `/Users/user` o `/Users/imac` en scripts nuevos. Todo script debe importar `scripts/captoora_paths.py` para funcionar automáticamente en ambas computadoras.

## 3. LAS FOTOS DE SESIÓN NO TOCAN EL DISCO INTERNO DE LA MACBOOK
- Desde el 23 de octubre de 2026 queda prohibido que las fotos crudas de sesión saturen el disco interno de 256 GB. Van de la SD a la nube (`Google Drive`). Se conservan el crudo en Drive y la edición final en Pixieset / Portafolio Autorizado.
