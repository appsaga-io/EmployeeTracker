@echo off
echo Building Employee Tracker Executables...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.11+ and try again
    pause
    exit /b 1
)

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Run build script
echo Running build script...
python build_exe.py

echo.
echo Build completed! Check the dist/ folder for executables.
pause

