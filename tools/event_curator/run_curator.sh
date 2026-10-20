#!/usr/bin/env bash
# Lanzador de un solo clic para Captoora Studio Curator
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "========================================================"
echo "  🚀 INICIANDO CAPTOORA EVENT CURATOR (LOCAL & OFFLINE)"
echo "  Mac M1 8GB Optimized | Cero APIs externas"
echo "========================================================"

PORT=8855
# Si el puerto ya está en uso, abrir directamente el navegador
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "El servidor ya se encuentra activo en http://127.0.0.1:$PORT"
    open "http://127.0.0.1:$PORT"
else
    # Abrir navegador tras 1 segundo
    (sleep 1 && open "http://127.0.0.1:$PORT") &
    python3 "$DIR/app.py" $PORT
fi
