# Employee Tracker Desktop Application Launcher
Write-Host "Starting Employee Tracker Desktop Application..." -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Yellow
} catch {
    Write-Host "Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ and try again" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if config file exists
if (-not (Test-Path "config.env")) {
    Write-Host "Configuration file not found. Running setup..." -ForegroundColor Yellow
    python setup.py
    Write-Host ""
}

# Check if requirements are installed
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
    Write-Host "Installing requirements..." -ForegroundColor Yellow
    pip install -r requirements.txt
} else {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
}

# Run the application
Write-Host "Starting application..." -ForegroundColor Green
python src/main.py

Read-Host "Press Enter to exit"

