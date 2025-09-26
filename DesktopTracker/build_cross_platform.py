#!/usr/bin/env python3
"""
Cross-platform build script for Employee Tracker
This script can build executables for both macOS and Windows
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
    
    print(f"🖥️  Current platform: {platform.system()} ({platform.machine()})")
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

def build_for_platform(target_platform):
    """Build executables for a specific platform"""
    print(f"\n🔨 Building for {target_platform.title()}...")
    
    # Set environment variables for cross-compilation
    if target_platform == 'windows' and platform.system().lower() != 'windows':
        print("⚠️  Cross-compilation to Windows from macOS/Linux is not supported by PyInstaller")
        print("   Please run this script on a Windows machine to build Windows executables")
        return False
    
    # Get PyInstaller path
    pyinstaller_path = get_pyinstaller_path()
    print(f"🔧 Using PyInstaller: {pyinstaller_path}")
    
    # Platform-specific configurations
    if target_platform == 'windows':
        icon_file = "icon.ico"
        data_sep = ";"
        ext = ".exe"
    else:  # macOS
        icon_file = "icon.png"
        data_sep = ":"
        ext = ".app"
    
    # Build commands for each application
    apps = [
        {
            'name': 'EmployeeTrackerGUI',
            'script': 'src/main.py',
            'hidden_imports': ['pystray', 'PIL', 'requests', 'dotenv']
        },
        {
            'name': 'EmployeeTrackerService',
            'script': 'src/background_service.py',
            'hidden_imports': ['pystray', 'PIL', 'requests', 'dotenv', 'tkinter']
        },
        {
            'name': 'EmployeeTrackerTray',
            'script': 'src/tray_app.py',
            'hidden_imports': ['pystray', 'PIL', 'requests', 'dotenv', 'tkinter']
        }
    ]
    
    success_count = 0
    
    for app in apps:
        print(f"\n📱 Building {app['name']}...")
        
        cmd = [
            pyinstaller_path,
            '--clean',
            '--onefile',
            '--windowed',
            f"--name={app['name']}",
            f"--icon={icon_file}",
            f"--add-data=config.env.example{data_sep}.",
        ]
        
        # Add hidden imports
        for imp in app['hidden_imports']:
            cmd.append(f"--hidden-import={imp}")
        
        cmd.append(app['script'])
        
        try:
            subprocess.check_call(cmd)
            print(f"✅ {app['name']}{ext} created successfully")
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build {app['name']}: {e}")
    
    return success_count > 0

def create_icons():
    """Create icons for both platforms"""
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple icon
        image = Image.new('RGB', (64, 64), color='blue')
        draw = ImageDraw.Draw(image)
        draw.ellipse((16, 16, 48, 48), fill='white')
        draw.text((20, 20), "ET", fill='blue')
        
        # Save as ICO for Windows
        image.save('icon.ico', format='ICO')
        print("✅ Windows icon created: icon.ico")
        
        # Save as PNG for macOS
        image.save('icon.png', format='PNG')
        print("✅ macOS icon created: icon.png")
        
        return True
    except Exception as e:
        print(f"⚠️  Could not create icons: {e}")
        return False

def create_installer_scripts():
    """Create installer scripts for both platforms"""
    
    # Windows installer
    windows_installer = '''@echo off
echo Installing Employee Tracker for Windows...
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
echo ✅ Windows installation completed!
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
        f.write(windows_installer)
    print("✅ Windows installer script created: install_windows.bat")
    
    # macOS installer
    macos_installer = '''#!/bin/bash

echo "Installing Employee Tracker for macOS..."
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
echo "✅ macOS installation completed!"
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
        f.write(macos_installer)
    
    # Make it executable
    os.chmod('install_macos.sh', 0o755)
    print("✅ macOS installer script created: install_macos.sh")

def create_portable_packages():
    """Create portable packages for both platforms"""
    
    # Windows portable package
    windows_dir = "EmployeeTracker_Portable_Windows"
    if os.path.exists(windows_dir):
        shutil.rmtree(windows_dir)
    os.makedirs(windows_dir)
    
    # Copy Windows executables
    for exe in ["EmployeeTrackerGUI.exe", "EmployeeTrackerService.exe", "EmployeeTrackerTray.exe"]:
        if os.path.exists(f"dist/{exe}"):
            shutil.copy2(f"dist/{exe}", windows_dir)
    
    # Copy config file
    shutil.copy2("config.env.example", os.path.join(windows_dir, "config.env"))
    
    # Create Windows launcher
    windows_launcher = '''@echo off
echo Employee Tracker Portable (Windows)
echo ===================================
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
    
    with open(os.path.join(windows_dir, "launcher.bat"), 'w') as f:
        f.write(windows_launcher)
    
    print(f"✅ Windows portable package created: {windows_dir}/")
    
    # macOS portable package
    macos_dir = "EmployeeTracker_Portable_macOS"
    if os.path.exists(macos_dir):
        shutil.rmtree(macos_dir)
    os.makedirs(macos_dir)
    
    # Copy macOS app bundles
    for app in ["EmployeeTrackerGUI.app", "EmployeeTrackerService.app", "EmployeeTrackerTray.app"]:
        if os.path.exists(f"dist/{app}"):
            shutil.copytree(f"dist/{app}", os.path.join(macos_dir, app))
    
    # Copy config file
    shutil.copy2("config.env.example", os.path.join(macos_dir, "config.env"))
    
    # Create macOS launcher
    macos_launcher = '''#!/bin/bash

echo "Employee Tracker Portable (macOS)"
echo "================================="
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
    
    with open(os.path.join(macos_dir, "launcher.sh"), 'w') as f:
        f.write(macos_launcher)
    
    # Make launcher executable
    os.chmod(os.path.join(macos_dir, "launcher.sh"), 0o755)
    
    print(f"✅ macOS portable package created: {macos_dir}/")

def main():
    """Main function"""
    print("🚀 Employee Tracker Cross-Platform Builder")
    print("=" * 50)
    
    current_platform = get_platform_info()
    
    print(f"\n📋 Build Options:")
    print(f"1. Build for current platform ({current_platform['system'].title()})")
    print(f"2. Build for Windows (requires Windows machine)")
    print(f"3. Build for macOS (requires macOS machine)")
    print(f"4. Create installer scripts only")
    print(f"5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        # Build for current platform
        if build_for_platform(current_platform['system']):
            create_installer_scripts()
            create_portable_packages()
            print(f"\n✅ Build completed for {current_platform['system'].title()}!")
        else:
            print(f"\n❌ Build failed for {current_platform['system'].title()}")
    
    elif choice == "2":
        # Build for Windows
        if current_platform['system'] == 'windows':
            if build_for_platform('windows'):
                create_installer_scripts()
                create_portable_packages()
                print("\n✅ Windows build completed!")
            else:
                print("\n❌ Windows build failed!")
        else:
            print("\n⚠️  Cannot build Windows executables on non-Windows platform")
            print("   Please run this script on a Windows machine")
    
    elif choice == "3":
        # Build for macOS
        if current_platform['system'] == 'darwin':
            if build_for_platform('darwin'):
                create_installer_scripts()
                create_portable_packages()
                print("\n✅ macOS build completed!")
            else:
                print("\n❌ macOS build failed!")
        else:
            print("\n⚠️  Cannot build macOS executables on non-macOS platform")
            print("   Please run this script on a macOS machine")
    
    elif choice == "4":
        # Create installer scripts only
        create_installer_scripts()
        create_portable_packages()
        print("\n✅ Installer scripts created!")
    
    elif choice == "5":
        print("\n👋 Goodbye!")
        return
    
    else:
        print("\n❌ Invalid choice!")
        return
    
    print(f"\n📦 Files created:")
    print(f"   - dist/ folder with executables")
    print(f"   - EmployeeTracker_Portable_Windows/ (Windows portable)")
    print(f"   - EmployeeTracker_Portable_macOS/ (macOS portable)")
    print(f"   - install_windows.bat (Windows installer)")
    print(f"   - install_macos.sh (macOS installer)")
    
    print(f"\n🌍 Platform Support:")
    print(f"   - Windows: Run install_windows.bat or use portable package")
    print(f"   - macOS: Run ./install_macos.sh or use portable package")

if __name__ == "__main__":
    # Create icons first
    create_icons()
    main()
