@echo off
title Captoora Studio - Servidor Local
echo ========================================================
echo         CAPTOORA - MOMENTOS QUE PERMANECEN
echo ========================================================
echo Iniciando servidor local en http://localhost:8080 ...
echo Puedes cerrar esta ventana cuando desees detener el servidor.
echo.
start http://localhost:8080
python -m http.server 8080
pause
