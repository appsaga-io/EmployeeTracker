#!/usr/bin/env python3
"""
Windows Service Installer for Employee Tracker
Installs the Employee Tracker as a Windows service
"""

import os
import sys
import subprocess
import winreg
from pathlib import Path

def create_service_script():
    """Create a service script for Windows"""
    script_content = '''@echo off
cd /d "{}"
python src/background_service.py
'''.format(os.getcwd())

    with open('start_service.bat', 'w') as f:
        f.write(script_content)

    print("✅ Service script created: start_service.bat")

def create_vbs_launcher():
    """Create a VBS launcher to run the service silently"""
    vbs_content = '''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "start_service.bat", 0, False
'''

    with open('start_service.vbs', 'w') as f:
        f.write(vbs_content)

    print("✅ VBS launcher created: start_service.vbs")

def create_startup_shortcut():
    """Create a startup shortcut"""
    try:
        import winshell
        from win32com.client import Dispatch

        # Get startup folder
        startup = winshell.startup()

        # Create shortcut
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(os.path.join(startup, "Employee Tracker.lnk"))
        shortcut.Targetpath = os.path.join(os.getcwd(), "start_service.vbs")
        shortcut.WorkingDirectory = os.getcwd()
        shortcut.IconLocation = os.path.join(os.getcwd(), "icon.ico")
        shortcut.save()

        print("✅ Startup shortcut created")
    except ImportError:
        print("⚠️  pywin32 not installed. Install with: pip install pywin32")
    except Exception as e:
        print(f"⚠️  Could not create startup shortcut: {e}")

def create_icon():
    """Create a simple icon file"""
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
    except Exception as e:
        print(f"⚠️  Could not create icon: {e}")

def install_dependencies():
    """Install required dependencies"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32", "winshell"])
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Could not install dependencies: {e}")

def main():
    """Main installation function"""
    print("🚀 Installing Employee Tracker as Windows Service")
    print("=" * 50)

    # Install dependencies
    install_dependencies()

    # Create service script
    create_service_script()

    # Create VBS launcher
    create_vbs_launcher()

    # Create icon
    create_icon()

    # Create startup shortcut
    create_startup_shortcut()

    print("\n✅ Installation completed!")
    print("\n📋 Files created:")
    print("   - start_service.bat (Service launcher)")
    print("   - start_service.vbs (Silent launcher)")
    print("   - icon.ico (Application icon)")
    print("   - Employee Tracker.lnk (Startup shortcut)")

    print("\n🎯 To start the service:")
    print("   1. Double-click start_service.vbs")
    print("   2. Or add start_service.bat to Windows startup")

    print("\n🔧 To configure:")
    print("   1. Edit config.env file")
    print("   2. Add your API token")
    print("   3. Restart the service")

if __name__ == "__main__":
    main()

