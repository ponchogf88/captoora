@echo off
chcp 65001 >nul
echo ============================================================================
echo   CAPTOORA STUDIO - CLASIFICADOR AUTOMATICO PARA PIXIESET (INDIVIDUALES VS GRUPALES)
echo ============================================================================
"%USERPROFILE%\.local\bin\python.exe" "%~dp0CLASIFICAR_FOTOS_DESCARGADAS.py"
echo.
pause
