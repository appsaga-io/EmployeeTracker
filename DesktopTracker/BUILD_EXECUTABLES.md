# 🔨 Building Employee Tracker Executables

## Overview

This guide shows you how to build standalone `.exe` files from the Employee Tracker Python application. The executables will run on Windows without requiring Python to be installed.

## Prerequisites

- Python 3.11+ installed
- All dependencies installed (`pip install -r requirements.txt`)
- Windows operating system

## Quick Build

### Option 1: Using Batch File
```bash
build.bat
```

### Option 2: Using PowerShell
```powershell
.\build.ps1
```

### Option 3: Manual Build
```bash
python build_exe.py
```

## What Gets Built

The build process creates three different executables:

### 1. EmployeeTrackerGUI.exe
- **Full GUI version** with complete interface
- **Windowed application** with visible interface
- **Best for**: Users who want full control and visibility

### 2. EmployeeTrackerService.exe
- **Background service** that runs in system tray
- **No visible windows** - runs silently
- **Best for**: Users who want minimal interface

### 3. EmployeeTrackerTray.exe
- **System tray application** with context menu
- **Minimal interface** with tray icon
- **Best for**: Users who want quick access via tray

## Build Process

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Build Script
```bash
python build_exe.py
```

### Step 3: Find Executables
Look in the `dist/` folder for your `.exe` files.

## Build Output

After building, you'll have:

```
dist/
├── EmployeeTrackerGUI.exe      # Full GUI version
├── EmployeeTrackerService.exe  # Background service
└── EmployeeTrackerTray.exe     # System tray version

EmployeeTracker_Portable/       # Portable package
├── EmployeeTrackerGUI.exe
├── EmployeeTrackerService.exe
├── EmployeeTrackerTray.exe
├── config.env
├── launcher.bat
└── README.md

install_exe.bat                 # Installer script
```

## Installation Options

### Option 1: Portable Package
1. **Copy** the `EmployeeTracker_Portable` folder to any location
2. **Run** `launcher.bat` to choose which version to start
3. **Configure** `config.env` with your API token

### Option 2: System Installation
1. **Run** `install_exe.bat` as administrator
2. **Executables** will be installed to `Program Files`
3. **Desktop shortcuts** will be created
4. **Service** will be added to startup

### Option 3: Manual Installation
1. **Copy** executables to desired location
2. **Create** shortcuts manually
3. **Configure** `config.env` file

## Configuration

### Before Building
1. **Edit** `config.env.example` with your settings
2. **Set** your API token
3. **Configure** other settings as needed

### After Building
1. **Edit** `config.env` in the executable directory
2. **Set** your API token
3. **Restart** the application

## Distribution

### For Internal Use
- **Share** the `EmployeeTracker_Portable` folder
- **Include** setup instructions
- **Provide** API token configuration

### For External Distribution
- **Test** on target machines
- **Include** documentation
- **Provide** support contact

## Troubleshooting

### Common Build Issues

1. **PyInstaller not found**:
   ```bash
   pip install pyinstaller
   ```

2. **Missing dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Import errors**:
   - Check all dependencies are installed
   - Verify Python version compatibility

4. **Large executable size**:
   - This is normal for PyInstaller
   - Executables are typically 50-100MB

### Runtime Issues

1. **Executable won't start**:
   - Check Windows Defender/antivirus
   - Run as administrator
   - Check system requirements

2. **API connection failed**:
   - Verify `config.env` exists
   - Check API token is correct
   - Ensure Laravel backend is running

3. **Tray icon not visible**:
   - Check system tray settings
   - Look in "Show hidden icons"
   - Restart the application

## Advanced Configuration

### Custom Icon
Replace `icon.ico` with your custom icon before building.

### Custom Build Options
Edit `build_exe.py` to modify build parameters:

```python
# Add custom data files
"--add-data=your_file.txt;.",

# Add hidden imports
"--hidden-import=your_module",

# Change executable name
"--name=YourAppName",
```

### Build Optimization
For smaller executables:

```python
# Add to PyInstaller command
"--exclude-module=unused_module",
"--strip",
"--optimize=2",
```

## File Sizes

Typical executable sizes:
- **EmployeeTrackerGUI.exe**: ~80-100MB
- **EmployeeTrackerService.exe**: ~70-90MB
- **EmployeeTrackerTray.exe**: ~70-90MB

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11
- **RAM**: 100MB available
- **Disk**: 200MB free space
- **Network**: Internet connection for API

### Recommended Requirements
- **OS**: Windows 11
- **RAM**: 500MB available
- **Disk**: 500MB free space
- **Network**: Stable internet connection

## Security Considerations

- **Executables** are not digitally signed
- **Windows Defender** may flag as unknown
- **Add exception** if needed
- **Scan** with antivirus before distribution

## Updates and Maintenance

### Updating Executables
1. **Rebuild** with new code
2. **Replace** old executables
3. **Update** configuration if needed

### Version Control
- **Tag** releases in version control
- **Document** changes between versions
- **Test** thoroughly before distribution

---

## 🎉 Ready to Build!

Your Employee Tracker can now be built into standalone executables that run on any Windows machine without requiring Python installation! 🚀

### Quick Start:
1. Run `build.bat`
2. Find executables in `dist/` folder
3. Distribute the `EmployeeTracker_Portable` folder
4. Users can run `launcher.bat` to start

