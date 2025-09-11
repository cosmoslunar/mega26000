@echo off
echo ============================
echo   Building JARVIS•AI .exe
echo ============================

REM Install pyinstaller if not already installed
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pyinstaller...
    pip install pyinstaller
)

REM Build exe from jarvis.py
pyinstaller --onefile jarvis.py

echo.
echo Build finished!
echo You can find jarvis.exe inside the 'dist' folder.
pause