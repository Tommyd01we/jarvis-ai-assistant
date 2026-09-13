@echo off
REM Quick-start batch file for Jarvis AI
REM This file builds and runs Jarvis as executable

echo.
echo ===============================================
echo     JARVIS AI - Quick Start Build & Run
echo ===============================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version

echo.
echo [2/4] Installing/Updating dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed

echo.
echo [3/4] Building Jarvis executable...
python build_executable.py
if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)

echo.
echo [4/4] Launching Jarvis AI...
echo.

REM Check if executable was created
if exist "dist\Jarvis.exe" (
    echo ===============================================
    echo SUCCESS! Starting Jarvis AI...
    echo ===============================================
    echo.
    cd dist
    Jarvis.exe
    cd ..
) else (
    echo ERROR: Jarvis.exe was not created
    pause
    exit /b 1
)

pause