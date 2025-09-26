@echo off
echo Starting Employee Tracker Background Service...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.11+ and try again
    pause
    exit /b 1
)

REM Check if config file exists
if not exist config.env (
    echo Configuration file not found. Running setup...
    python setup.py
    echo.
)

REM Run the background service
echo Starting background service...
echo The application will run in the system tray.
echo Right-click the tray icon to access controls.
echo.

python src/background_service.py

pause

