@echo off
title J.A.R.V.I.S MARK XV - Stark Industries
cd /d "%~dp0"
echo.
echo   ============================================
echo   J.A.R.V.I.S MARK XV
echo   Just A Rather Very Intelligent System
echo   ============================================
echo.

REM --- Python detection ---
set PYTHON=
set PYTHONW=

REM Try Python 3.11 (primary)
set "P311=C:\Users\bdjaj\AppData\Local\Programs\Python\Python311\python.exe"
set "P311W=C:\Users\bdjaj\AppData\Local\Programs\Python\Python311\pythonw.exe"
if exist "%P311W%" (
    set PYTHON=%P311%
    set PYTHONW=%P311W%
    echo [OK] Python 3.11 found
    goto :found
)

REM Try default python
where python >nul 2>nul
if %errorlevel% equ 0 (
    for /f "delims=" %%i in ('where python') do set PYTHON=%%i
    set PYTHONW=%PYTHON%w
    echo [OK] Python found: %PYTHON%
    goto :found
)

echo [FAIL] Python not found. Install Python 3.11 at:
echo        C:\Users\bdjaj\AppData\Local\Programs\Python\Python311\
pause
exit /b 1

:found

REM --- Quick dependency check ---
echo.
echo Checking dependencies...
%PYTHON% -c "import openai, colorama, sounddevice, pyttsx3, psutil, requests, numpy" 2>nul
if %errorlevel% neq 0 (
    echo Installing missing packages...
    %PYTHON% -m pip install openai colorama sounddevice pyttsx3 psutil requests numpy -q
)

REM --- Optional plugin deps ---
echo Checking optional plugins...
%PYTHON% -c "import cv2, numpy" 2>nul || (
    echo Installing surveillance deps...
    %PYTHON% -m pip install opencv-python numpy -q
)
%PYTHON% -c "import playwright" 2>nul || (
    echo Installing browser agent deps...
    %PYTHON% -m pip install playwright -q
    %PYTHON% -m playwright install chromium 2>nul
)
%PYTHON% -c "import mediapipe" 2>nul || (
    echo Installing gesture control deps...
    %PYTHON% -m pip install mediapipe -q
)

REM --- Launch ---
echo.
echo [BOOT] Starting J.A.R.V.I.S Neural Core...
echo [BOOT] Opening Holographic Interface...
echo.

REM Kill any existing JARVIS instances (targeted - only jarvis processes)
powershell -Command "Get-CimInstance Win32_Process | Where-Object { ($_.Name -match 'pythonw?\.exe') -and ($_.CommandLine -match 'jarvis|JARVIS') } | ForEach-Object { try { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue } catch {} }" 2>nul

REM Start JARVIS launcher (headless - no console spam)
start "" %PYTHONW% JARVIS.pyw

echo J.A.R.V.I.S is initializing. The HUD will appear shortly.
echo Say "JARVIS" to activate.
echo.
timeout /t 3 >nul
exit /b 0
