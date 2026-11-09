#!/bin/bash
# ==============================================================================
# CAPTOORA STUDIO — LANZADOR MAC (UGREEN + CANON EOS 7D MARK II)
# ==============================================================================
cd "$(dirname "$0")"

echo "=================================================================="
echo "  ARGON LENS AI — MODO LOBA PRO (macOS + UGREEN + Canon 7D Mk II)"
echo "=================================================================="

# 1. Liberar bloqueo USB de Fotos / PTPCamera en macOS
killall -9 PTPCamera 2>/dev/null

# 2. Verificar si gphoto2 está instalado para disparo directo por USB en Mac
if ! command -v gphoto2 &> /dev/null; then
  echo "[AVISO] Para disparo directo USB en Mac con tu adaptador UGREEN,"
  echo "        puedes instalar gphoto2 corriendo: brew install gphoto2"
fi

# 3. Matar instancia previa en el puerto 8765 si existe
lsof -ti:8765 | xargs kill -9 2>/dev/null

# 4. Iniciar el servidor en segundo plano y abrir Chrome
python3 asistente_camara_ia/servidor_tether_ia.py &
SERVER_PID=$!

sleep 1.2
open -a "Google Chrome" "http://127.0.0.1:8765/index.html" || open "http://127.0.0.1:8765/index.html"

echo ""
echo "[OK] Estudio abierto en http://127.0.0.1:8765/index.html"
echo "Presiona Ctrl+C en esta ventana cuando termines tu sesión."
wait $SERVER_PID
