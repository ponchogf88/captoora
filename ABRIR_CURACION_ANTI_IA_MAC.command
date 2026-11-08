#!/bin/bash
# ==============================================================================
# LANZADOR 1-CLIC MACOS — CURACIÓN ANTI-IA & LOS 13 ÁLBUMES REALES (CAPTOORA)
# ==============================================================================
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================================="
echo "  CAPTOORA STUDIO — CENTRO DE CURACIÓN ANTI-IA (100% ÓPTICO REAL)"
echo "=================================================================="
echo "1. Sincronizando últimos cambios desde GitHub (origin/main)..."
git pull origin main

echo "2. Abriendo Centro de Curación Anti-IA en tu navegador..."
open "$DIR/CURACION_INSTAGRAM_100_REAL_ANTI_IA.html"

echo "3. Abriendo carpeta lista para publicar HOY (Día 01 Manifiesto 4:5 con EXIF Nikon)..."
open "$DIR/campaigns/curacion-anti-ia-2026/POST_DIA_01_LISTO_PARA_SUBIR_HOY"

echo "4. Copiando el Copy Humano del Día 01 a tu portapapeles de macOS (pbcopy)..."
if [ -f "$DIR/campaigns/curacion-anti-ia-2026/POST_DIA_01_LISTO_PARA_SUBIR_HOY/COPY_LISTO_DIA_01_MANIFIESTO_ANTI_IA.txt" ]; then
  cat "$DIR/campaigns/curacion-anti-ia-2026/POST_DIA_01_LISTO_PARA_SUBIR_HOY/COPY_LISTO_DIA_01_MANIFIESTO_ANTI_IA.txt" | pbcopy
  echo "✅ ¡Copy del Día 01 copiado automáticamente a tu portapapeles (Cmd+V)!"
fi
