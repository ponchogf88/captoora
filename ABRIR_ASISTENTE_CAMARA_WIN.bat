@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================================================
echo   ARGON LENS AI — ASISTENTE DE CAMARA Y VOZ EN TIEMPO REAL (WINDOWS)
echo ========================================================================

start "" "http://127.0.0.1:8765/index.html"

if exist "%USERPROFILE%\.local\bin\uv.exe" (
    "%USERPROFILE%\.local\bin\uv.exe" run --with pillow python asistente_camara_ia\servidor_tether_ia.py
) else (
    python asistente_camara_ia\servidor_tether_ia.py
)
pause
