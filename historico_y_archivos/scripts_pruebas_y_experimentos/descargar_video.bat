@echo off
title Captoora Studio - Descargador de Videos (yt-dlp)
echo ========================================================
echo         CAPTOORA STUDIO - MEDIA DOWNLOADER
echo ========================================================
echo Puedes descargar videos de YouTube, Instagram Reels, TikTok, etc.
echo.
set /p URL="Pega el enlace del video aqui y presiona ENTER: "
echo.
echo Descargando en maxima resolucion...
"C:\Users\USUARIO\AppData\Local\Microsoft\WinGet\Links\yt-dlp.exe" -f "bestvideo+bestaudio/best" --merge-output-format mp4 "%URL%"
echo.
echo ========================================================
echo Descarga finalizada! El archivo se guardo en esta carpeta.
echo ========================================================
pause
