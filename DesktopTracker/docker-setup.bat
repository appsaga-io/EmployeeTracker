@echo off
echo Setting up Employee Tracker Desktop Application with Docker...
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker is not installed or not in PATH
    echo Please install Docker Desktop and try again
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo Docker Compose is not available
    echo Please install Docker Compose and try again
    pause
    exit /b 1
)

echo Docker and Docker Compose are available
echo.

REM Create config file if it doesn't exist
if not exist config.env (
    echo Creating configuration file...
    copy config.env.example config.env
    echo Configuration file created. Please edit config.env and add your API token.
    echo.
)

echo Building and starting the application...
docker-compose up --build

pause

