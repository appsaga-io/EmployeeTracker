#!/usr/bin/env python3
"""
Build script for creating executable files from Employee Tracker
Creates .exe files for both GUI and background service versions
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    print("🔧 Installing PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install PyInstaller: {e}")
        return False

def create_icon():
    """Create an icon file for the executable"""
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple icon
        image = Image.new('RGB', (64, 64), color='blue')
        draw = ImageDraw.Draw(image)
        draw.ellipse((16, 16, 48, 48), fill='white')
        draw.text((20, 20), "ET", fill='blue')
        
        # Save as ICO
        image.save('icon.ico', format='ICO')
        print("✅ Icon created: icon.ico")
        return True
    except Exception as e:
        print(f"⚠️  Could not create icon: {e}")
        return False

def build_gui_exe():
    """Build the GUI version executable"""
    print("\n🖥️ Building GUI version...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=EmployeeTrackerGUI",
        "--icon=icon.ico",
        "--add-data=config.env.example;.",
        "--hidden-import=pystray",
        "--hidden-import=PIL",
        "--hidden-import=requests",
        "--hidden-import=dotenv",
        "src/main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ GUI executable created: dist/EmployeeTrackerGUI.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build GUI executable: {e}")
        return False

def build_background_exe():
    """Build the background service executable"""
    print("\n🖥️ Building background service...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=EmployeeTrackerService",
        "--icon=icon.ico",
        "--add-data=config.env.example;.",
        "--hidden-import=pystray",
        "--hidden-import=PIL",
        "--hidden-import=requests",
        "--hidden-import=dotenv",
        "--hidden-import=tkinter",
        "src/background_service.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Background service executable created: dist/EmployeeTrackerService.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build background service executable: {e}")
        return False

def build_tray_exe():
    """Build the tray application executable"""
    print("\n🖥️ Building tray application...")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=EmployeeTrackerTray",
        "--icon=icon.ico",
        "--add-data=config.env.example;.",
        "--hidden-import=pystray",
        "--hidden-import=PIL",
        "--hidden-import=requests",
        "--hidden-import=dotenv",
        "--hidden-import=tkinter",
        "src/tray_app.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Tray application executable created: dist/EmployeeTrackerTray.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build tray application executable: {e}")
        return False

def create_installer_script():
    """Create an installer script for the executables"""
    installer_content = '''@echo off
echo Installing Employee Tracker...
echo.

REM Create application directory
if not exist "%PROGRAMFILES%\\EmployeeTracker" (
    mkdir "%PROGRAMFILES%\\EmployeeTracker"
)

REM Copy executables
copy "dist\\EmployeeTrackerGUI.exe" "%PROGRAMFILES%\\EmployeeTracker\\"
copy "dist\\EmployeeTrackerService.exe" "%PROGRAMFILES%\\EmployeeTracker\\"
copy "dist\\EmployeeTrackerTray.exe" "%PROGRAMFILES%\\EmployeeTracker\\"
copy "config.env.example" "%PROGRAMFILES%\\EmployeeTracker\\config.env"

REM Create desktop shortcuts
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Employee Tracker GUI.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\\EmployeeTracker\\EmployeeTrackerGUI.exe'; $Shortcut.Save()"

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Employee Tracker Service.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\\EmployeeTracker\\EmployeeTrackerService.exe'; $Shortcut.Save()"

REM Create startup shortcut
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Employee Tracker Service.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\\EmployeeTracker\\EmployeeTrackerService.exe'; $Shortcut.Save()"

echo.
echo ✅ Installation completed!
echo.
echo 📋 Installed files:
echo    - EmployeeTrackerGUI.exe (Full GUI version)
echo    - EmployeeTrackerService.exe (Background service)
echo    - EmployeeTrackerTray.exe (System tray version)
echo.
echo 🎯 Desktop shortcuts created
echo 🚀 Service added to startup
echo.
echo 📝 Next steps:
echo    1. Configure API token in config.env
echo    2. Start the application from desktop shortcuts
echo.
pause
'''
    
    with open('install_exe.bat', 'w') as f:
        f.write(installer_content)
    
    print("✅ Installer script created: install_exe.bat")

def create_portable_package():
    """Create a portable package with all executables"""
    print("\n📦 Creating portable package...")
    
    # Create portable directory
    portable_dir = "EmployeeTracker_Portable"
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    
    os.makedirs(portable_dir)
    
    # Copy executables
    if os.path.exists("dist/EmployeeTrackerGUI.exe"):
        shutil.copy2("dist/EmployeeTrackerGUI.exe", portable_dir)
    
    if os.path.exists("dist/EmployeeTrackerService.exe"):
        shutil.copy2("dist/EmployeeTrackerService.exe", portable_dir)
    
    if os.path.exists("dist/EmployeeTrackerTray.exe"):
        shutil.copy2("dist/EmployeeTrackerTray.exe", portable_dir)
    
    # Copy config file
    shutil.copy2("config.env.example", os.path.join(portable_dir, "config.env"))
    
    # Copy documentation
    docs = ["README.md", "BACKGROUND_SERVICE.md", "SETUP_GUIDE.md"]
    for doc in docs:
        if os.path.exists(doc):
            shutil.copy2(doc, portable_dir)
    
    # Create launcher script
    launcher_content = '''@echo off
echo Employee Tracker Portable
echo ========================
echo.
echo Choose version to run:
echo 1. Full GUI Version
echo 2. Background Service (System Tray)
echo 3. Tray Application
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" start EmployeeTrackerGUI.exe
if "%choice%"=="2" start EmployeeTrackerService.exe
if "%choice%"=="3" start EmployeeTrackerTray.exe
if "%choice%"=="4" exit

pause
'''
    
    with open(os.path.join(portable_dir, "launcher.bat"), 'w') as f:
        f.write(launcher_content)
    
    print(f"✅ Portable package created: {portable_dir}/")
    print(f"   - Contains all executables")
    print(f"   - Ready to distribute")
    print(f"   - Run launcher.bat to start")

def cleanup_build_files():
    """Clean up build files"""
    print("\n🧹 Cleaning up build files...")
    
    # Remove build directories
    dirs_to_remove = ["build", "__pycache__"]
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Removed {dir_name}/")
    
    # Remove spec files
    spec_files = ["EmployeeTrackerGUI.spec", "EmployeeTrackerService.spec", "EmployeeTrackerTray.spec"]
    for spec_file in spec_files:
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print(f"✅ Removed {spec_file}")

def main():
    """Main build function"""
    print("🚀 Building Employee Tracker Executables")
    print("=" * 50)
    
    # Install PyInstaller
    if not install_pyinstaller():
        return
    
    # Create icon
    create_icon()
    
    # Build executables
    gui_success = build_gui_exe()
    background_success = build_background_exe()
    tray_success = build_tray_exe()
    
    # Create installer script
    if gui_success or background_success or tray_success:
        create_installer_script()
    
    # Create portable package
    if gui_success or background_success or tray_success:
        create_portable_package()
    
    # Cleanup
    cleanup_build_files()
    
    print("\n" + "=" * 50)
    print("🎉 Build completed!")
    
    if gui_success:
        print("✅ EmployeeTrackerGUI.exe - Full GUI version")
    if background_success:
        print("✅ EmployeeTrackerService.exe - Background service")
    if tray_success:
        print("✅ EmployeeTrackerTray.exe - System tray version")
    
    print("\n📦 Files created:")
    print("   - dist/ folder with executables")
    print("   - EmployeeTracker_Portable/ folder (portable package)")
    print("   - install_exe.bat (installer script)")
    
    print("\n🚀 To install:")
    print("   Run: install_exe.bat")
    
    print("\n📦 To distribute:")
    print("   Share the EmployeeTracker_Portable folder")

if __name__ == "__main__":
    main()

