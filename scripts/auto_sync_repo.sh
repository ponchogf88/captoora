#!/bin/bash
# ==============================================================================
# CAPTOORA AUTO-SYNC DAEMON (12:00 PM & 12:00 AM)
# Sincroniza automáticamente el repositorio GitHub ponchogf88/captoora y el espejo
# en Google Drive dos veces al día (mediodía y medianoche).
# ==============================================================================

REPO_DIR="/Users/user/captoora"
GDRIVE_LOGS="/Users/user/Library/CloudStorage/GoogleDrive-lic.jagf87@gmail.com/Mi unidad/PROJECTS/RESPALDOS_PROYECTOS/AI CAPTOORA/BITACORA_Y_MEMORIA_CENTRAL/logs"
LOG_FILE="${REPO_DIR}/logs/auto_sync.log"

mkdir -p "${REPO_DIR}/logs"
echo "=== [$(date '+%Y-%m-%d %H:%M:%S')] Iniciando Auto-Sync Captoora ===" >> "${LOG_FILE}"

cd "${REPO_DIR}" || exit 1

# Pull previo con rebase para evitar rechazos
git pull --rebase origin main >> "${LOG_FILE}" 2>&1

# Sincronizar archivos y bitácoras modificadas
git add -A >> "${LOG_FILE}" 2>&1

if git diff --staged --quiet; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] No hay cambios nuevos para commitear." >> "${LOG_FILE}"
else
    COMMIT_MSG="auto: sync programado [$(date '+%Y-%m-%d %H:%M:%S')]"
    git commit -m "${COMMIT_MSG}" >> "${LOG_FILE}" 2>&1
    git push origin main >> "${LOG_FILE}" 2>&1
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Push a GitHub completado con éxito." >> "${LOG_FILE}"
fi

# Respaldo espejo a Google Drive
if [ -d "${GDRIVE_LOGS}" ]; then
    cp -rf "${REPO_DIR}/logs/"* "${GDRIVE_LOGS}/" 2>/dev/null
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Espejo a Google Drive actualizado." >> "${LOG_FILE}"
fi

echo "=== [$(date '+%Y-%m-%d %H:%M:%S')] Auto-Sync finalizado con éxito ===" >> "${LOG_FILE}"
