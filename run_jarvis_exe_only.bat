@echo off
REM Simple launcher - runs existing Jarvis.exe

if exist "dist\Jarvis.exe" (
    echo Launching Jarvis AI Assistant...
    cd dist
    Jarvis.exe
    cd ..
) else (
    echo ERROR: Jarvis.exe not found
    echo Run 'run_jarvis.bat' first to build the executable
    pause
    exit /b 1
)