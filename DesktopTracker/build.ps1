# Employee Tracker Executable Builder
Write-Host "Building Employee Tracker Executables..." -ForegroundColor Green
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

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run build script
Write-Host "Running build script..." -ForegroundColor Yellow
python build_exe.py

Write-Host ""
Write-Host "Build completed! Check the dist/ folder for executables." -ForegroundColor Green
Read-Host "Press Enter to exit"

