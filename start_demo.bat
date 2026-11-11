@echo off
TITLE Digii Campus 2.0 - Product Prototype Launcher
COLOR 0A

echo ===============================================================================
echo                DIGII CAMPUS 2.0 - PRODUCT INNOVATION SUITE
echo             Executive APM Transition Prototype - Dhruv Jain
echo ===============================================================================
echo.
echo [*] Checking local server status on port 3000...

powershell -NoProfile -Command "$client = New-Object System.Net.Sockets.TcpClient; try { $client.Connect('127.0.0.1', 3000); exit 0 } catch { exit 1 }" >nul 2>&1

IF %ERRORLEVEL% EQU 0 (
    echo [OK] Local server is already running on http://localhost:3000/
) ELSE (
    echo [*] Starting Digii Campus HTTP server on http://localhost:3000/...
    start /min "Digii Campus Server" powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0product_enhancement\server.ps1" -Port 3000
    timeout /t 2 /nobreak >nul
)

echo [*] Opening prototype in your default web browser...
start http://localhost:3000/index.html

echo.
echo ===============================================================================
echo   PROTOTYPE RUNNING:
echo   - Local URL:          http://localhost:3000/index.html
echo   - Executive Pitch:    Click "Pitch Deck" button in header (or press 'P')
echo   - PM Cockpit:         Click "PM Cockpit" button in header
echo   - Student Hub:        Click "Student Experience Hub" in top navigation
echo ===============================================================================
echo.
echo Press any key to exit this launcher window (server will continue running in background).
pause >nul
