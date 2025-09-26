#!/usr/bin/env python3
"""
Cross-platform build script for creating executable files from Employee Tracker
Supports both macOS (.app bundles) and Windows (.exe files)
Creates executables for GUI, background service, and tray application versions
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def get_platform_info():
    """Get platform information"""
    system = platform.system().lower()
    is_macos = system == 'darwin'
    is_windows = system == 'windows'

    print(f"🖥️  Detected platform: {platform.system()} ({platform.machine()})")
    return {
        'system': system,
        'is_macos': is_macos,
        'is_windows': is_windows,
        'executable_ext': '.app' if is_macos else '.exe',
        'data_separator': ':' if is_macos else ';',
        'icon_ext': '.icns' if is_macos else '.ico'
    }

def get_pyinstaller_path():
    """Get the correct PyInstaller path"""
    try:
        # Try to find pyinstaller in PATH first
        subprocess.check_call(['pyinstaller', '--version'],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        return 'pyinstaller'
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Try common installation paths
        possible_paths = [
            '/Users/deepakdumraliya/Library/Python/3.9/bin/pyinstaller',
            '/usr/local/bin/pyinstaller',
            '/opt/homebrew/bin/pyinstaller',
            'pyinstaller'
        ]

        for path in possible_paths:
            try:
                subprocess.check_call([path, '--version'],
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)
                return path
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue

        return 'pyinstaller'  # Fallback

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

def create_icon(platform_info):
    """Create icon files for both platforms"""
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple icon
        image = Image.new('RGB', (64, 64), color='blue')
        draw = ImageDraw.Draw(image)
        draw.ellipse((16, 16, 48, 48), fill='white')
        draw.text((20, 20), "ET", fill='blue')
        
        # Save as ICO for Windows
        image.save('icon.ico', format='ICO')
        print("✅ Icon created: icon.ico")
        
        # For macOS, create ICNS (optional - PyInstaller can convert ICO)
        if platform_info['is_macos']:
            try:
                # Create multiple sizes for ICNS
                sizes = [16, 32, 64, 128, 256, 512]
                images = []
                for size in sizes:
                    resized = image.resize((size, size), Image.Resampling.LANCZOS)
                    images.append(resized)
                
                # Save as PNG first, then convert to ICNS if possible
                image.save('icon.png', format='PNG')
                print("✅ Icon created: icon.png")
            except Exception as e:
                print(f"⚠️  Could not create PNG icon: {e}")
        
        return True
    except Exception as e:
        print(f"⚠️  Could not create icon: {e}")
        return False

def build_gui_exe(platform_info, pyinstaller_path):
    """Build the GUI version executable"""
    print("\n🖥️ Building GUI version...")
    
    # Choose icon file based on platform
    icon_file = "icon.png" if platform_info['is_macos'] else "icon.ico"
    
    cmd = [
        pyinstaller_path,
        "--onefile",
        "--windowed",
        "--name=EmployeeTrackerGUI",
        f"--icon={icon_file}",
        f"--add-data=config.env.example{platform_info['data_separator']}.",
        "--hidden-import=pystray",
        "--hidden-import=PIL",
        "--hidden-import=requests",
        "--hidden-import=dotenv",
        "src/main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        ext = platform_info['executable_ext']
        print(f"✅ GUI executable created: dist/EmployeeTrackerGUI{ext}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build GUI executable: {e}")
        return False

def build_background_exe(platform_info, pyinstaller_path):
    """Build the background service executable"""
    print("\n🖥️ Building background service...")
    
    # Choose icon file based on platform
    icon_file = "icon.png" if platform_info['is_macos'] else "icon.ico"
    
    cmd = [
        pyinstaller_path,
        "--onefile",
        "--windowed",
        "--name=EmployeeTrackerService",
        f"--icon={icon_file}",
        f"--add-data=config.env.example{platform_info['data_separator']}.",
        "--hidden-import=pystray",
        "--hidden-import=PIL",
        "--hidden-import=requests",
        "--hidden-import=dotenv",
        "--hidden-import=tkinter",
        "src/background_service.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        ext = platform_info['executable_ext']
        print(f"✅ Background service executable created: dist/EmployeeTrackerService{ext}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build background service executable: {e}")
        return False

def build_tray_exe(platform_info, pyinstaller_path):
    """Build the tray application executable"""
    print("\n🖥️ Building tray application...")
    
    # Choose icon file based on platform
    icon_file = "icon.png" if platform_info['is_macos'] else "icon.ico"
    
    cmd = [
        pyinstaller_path,
        "--onefile",
        "--windowed",
        "--name=EmployeeTrackerTray",
        f"--icon={icon_file}",
        f"--add-data=config.env.example{platform_info['data_separator']}.",
        "--hidden-import=pystray",
        "--hidden-import=PIL",
        "--hidden-import=requests",
        "--hidden-import=dotenv",
        "--hidden-import=tkinter",
        "src/tray_app.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        ext = platform_info['executable_ext']
        print(f"✅ Tray application executable created: dist/EmployeeTrackerTray{ext}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build tray application executable: {e}")
        return False

def create_installer_script(platform_info):
    """Create platform-specific installer scripts"""
    if platform_info['is_windows']:
        # Windows installer script
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
        
        with open('install_windows.bat', 'w') as f:
            f.write(installer_content)
        print("✅ Windows installer script created: install_windows.bat")
        
    elif platform_info['is_macos']:
        # macOS installer script
        installer_content = '''#!/bin/bash

echo "Installing Employee Tracker..."
echo ""

# Create application directory
APP_DIR="/Applications/EmployeeTracker"
sudo mkdir -p "$APP_DIR"

# Copy executables
sudo cp -r "dist/EmployeeTrackerGUI.app" "$APP_DIR/"
sudo cp -r "dist/EmployeeTrackerService.app" "$APP_DIR/"
sudo cp -r "dist/EmployeeTrackerTray.app" "$APP_DIR/"
sudo cp "config.env.example" "$APP_DIR/config.env"

# Create desktop shortcuts (macOS)
ln -sf "$APP_DIR/EmployeeTrackerGUI.app" "$HOME/Desktop/Employee Tracker GUI.app"
ln -sf "$APP_DIR/EmployeeTrackerService.app" "$HOME/Desktop/Employee Tracker Service.app"

# Add to startup items (macOS)
STARTUP_DIR="$HOME/Library/LaunchAgents"
mkdir -p "$STARTUP_DIR"

cat > "$STARTUP_DIR/com.employeetracker.service.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.employeetracker.service</string>
    <key>ProgramArguments</key>
    <array>
        <string>$APP_DIR/EmployeeTrackerService.app/Contents/MacOS/EmployeeTrackerService</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

echo ""
echo "✅ Installation completed!"
echo ""
echo "📋 Installed files:"
echo "   - EmployeeTrackerGUI.app (Full GUI version)"
echo "   - EmployeeTrackerService.app (Background service)"
echo "   - EmployeeTrackerTray.app (System tray version)"
echo ""
echo "🎯 Desktop shortcuts created"
echo "🚀 Service added to startup"
echo ""
echo "📝 Next steps:"
echo "   1. Configure API token in $APP_DIR/config.env"
echo "   2. Start the application from desktop shortcuts"
echo ""
'''
        
        with open('install_macos.sh', 'w') as f:
            f.write(installer_content)
        
        # Make it executable
        os.chmod('install_macos.sh', 0o755)
        print("✅ macOS installer script created: install_macos.sh")

def create_portable_package(platform_info):
    """Create a platform-specific portable package with all executables"""
    print("\n📦 Creating portable package...")
    
    # Create portable directory
    portable_dir = f"EmployeeTracker_Portable_{platform_info['system'].title()}"
    if os.path.exists(portable_dir):
        shutil.rmtree(portable_dir)
    
    os.makedirs(portable_dir)
    
    # Copy executables based on platform
    ext = platform_info['executable_ext']
    
    if platform_info['is_macos']:
        # Copy .app bundles
        if os.path.exists("dist/EmployeeTrackerGUI.app"):
            shutil.copytree("dist/EmployeeTrackerGUI.app", 
                          os.path.join(portable_dir, "EmployeeTrackerGUI.app"))
        
        if os.path.exists("dist/EmployeeTrackerService.app"):
            shutil.copytree("dist/EmployeeTrackerService.app", 
                          os.path.join(portable_dir, "EmployeeTrackerService.app"))
        
        if os.path.exists("dist/EmployeeTrackerTray.app"):
            shutil.copytree("dist/EmployeeTrackerTray.app", 
                          os.path.join(portable_dir, "EmployeeTrackerTray.app"))
    else:
        # Copy .exe files
        if os.path.exists(f"dist/EmployeeTrackerGUI{ext}"):
            shutil.copy2(f"dist/EmployeeTrackerGUI{ext}", portable_dir)
        
        if os.path.exists(f"dist/EmployeeTrackerService{ext}"):
            shutil.copy2(f"dist/EmployeeTrackerService{ext}", portable_dir)
        
        if os.path.exists(f"dist/EmployeeTrackerTray{ext}"):
            shutil.copy2(f"dist/EmployeeTrackerTray{ext}", portable_dir)
    
    # Copy config file
    shutil.copy2("config.env.example", os.path.join(portable_dir, "config.env"))
    
    # Copy documentation
    docs = ["README.md", "BACKGROUND_SERVICE.md", "SETUP_GUIDE.md"]
    for doc in docs:
        if os.path.exists(doc):
            shutil.copy2(doc, portable_dir)
    
    # Create platform-specific launcher script
    if platform_info['is_windows']:
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
        launcher_file = "launcher.bat"
    else:
        launcher_content = '''#!/bin/bash

echo "Employee Tracker Portable"
echo "========================"
echo ""
echo "Choose version to run:"
echo "1. Full GUI Version"
echo "2. Background Service (System Tray)"
echo "3. Tray Application"
echo "4. Exit"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "Starting GUI Version..."
        open EmployeeTrackerGUI.app
        ;;
    2)
        echo "Starting Background Service..."
        open EmployeeTrackerService.app
        ;;
    3)
        echo "Starting Tray Application..."
        open EmployeeTrackerTray.app
        ;;
    4)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        ;;
esac
'''
        launcher_file = "launcher.sh"
    
    with open(os.path.join(portable_dir, launcher_file), 'w') as f:
        f.write(launcher_content)
    
    # Make launcher executable on macOS/Linux
    if not platform_info['is_windows']:
        os.chmod(os.path.join(portable_dir, launcher_file), 0o755)
    
    print(f"✅ Portable package created: {portable_dir}/")
    print(f"   - Contains all executables")
    print(f"   - Ready to distribute")
    print(f"   - Run {launcher_file} to start")

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
    print("🚀 Building Employee Tracker Executables (Cross-Platform)")
    print("=" * 60)
    
    # Get platform information
    platform_info = get_platform_info()
    
    # Install PyInstaller
    if not install_pyinstaller():
        return
    
    # Get PyInstaller path
    pyinstaller_path = get_pyinstaller_path()
    print(f"🔧 Using PyInstaller: {pyinstaller_path}")
    
    # Create icon
    create_icon(platform_info)
    
    # Build executables
    gui_success = build_gui_exe(platform_info, pyinstaller_path)
    background_success = build_background_exe(platform_info, pyinstaller_path)
    tray_success = build_tray_exe(platform_info, pyinstaller_path)
    
    # Create installer script
    if gui_success or background_success or tray_success:
        create_installer_script(platform_info)
    
    # Create portable package
    if gui_success or background_success or tray_success:
        create_portable_package(platform_info)
    
    # Cleanup
    cleanup_build_files()
    
    print("\n" + "=" * 60)
    print("🎉 Build completed!")
    
    ext = platform_info['executable_ext']
    if gui_success:
        print(f"✅ EmployeeTrackerGUI{ext} - Full GUI version")
    if background_success:
        print(f"✅ EmployeeTrackerService{ext} - Background service")
    if tray_success:
        print(f"✅ EmployeeTrackerTray{ext} - System tray version")
    
    print(f"\n📦 Files created:")
    print(f"   - dist/ folder with executables")
    print(f"   - EmployeeTracker_Portable_{platform_info['system'].title()}/ folder (portable package)")
    
    if platform_info['is_windows']:
        print(f"   - install_windows.bat (Windows installer script)")
        print(f"\n🚀 To install:")
        print(f"   Run: install_windows.bat")
    elif platform_info['is_macos']:
        print(f"   - install_macos.sh (macOS installer script)")
        print(f"\n🚀 To install:")
        print(f"   Run: ./install_macos.sh")
    
    print(f"\n📦 To distribute:")
    print(f"   Share the EmployeeTracker_Portable_{platform_info['system'].title()} folder")
    
    print(f"\n🌍 Platform Support:")
    print(f"   - Current: {platform_info['system'].title()}")
    print(f"   - To build for Windows: Run this script on Windows")
    print(f"   - To build for macOS: Run this script on macOS")

if __name__ == "__main__":
    main()

