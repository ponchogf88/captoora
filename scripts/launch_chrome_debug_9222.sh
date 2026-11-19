#!/usr/bin/env bash
set -euo pipefail

# Lanza una instancia dedicada de Google Chrome con Remote Debugging Port 9222
# Chrome 136+ exige un --user-data-dir separado del perfil principal para exponer el puerto 9222.
PROFILE_DIR="${HOME}/.cache/captoora-chrome-9222"
mkdir -p "${PROFILE_DIR}"

exec "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir="${PROFILE_DIR}" \
  --no-first-run \
  --no-default-browser-check \
  "$@"
