# Cross-Platform Build System for Employee Tracker

This document explains how to build Employee Tracker executables for both macOS and Windows platforms.

## 🚀 Quick Start

### Option 1: Interactive Cross-Platform Builder
```bash
python3 build_cross_platform.py
```

This will show you a menu with options to:
1. Build for current platform (macOS/Windows)
2. Build for Windows (requires Windows machine)
3. Build for macOS (requires macOS machine)
4. Create installer scripts only
5. Exit

### Option 2: Platform-Specific Builder
```bash
python3 build_exe.py
```

This automatically detects your platform and builds accordingly.

## 📋 Requirements

### Python Dependencies
- Python 3.7+
- PyInstaller
- Pillow (PIL)
- requests
- python-dotenv
- pystray (for system tray functionality)

### Platform Requirements
- **macOS**: macOS 10.13+ (for building macOS apps)
- **Windows**: Windows 10+ (for building Windows executables)

## 🔧 Build Process

### What Gets Built

For each platform, the following executables are created:

1. **EmployeeTrackerGUI** - Full desktop application with GUI
2. **EmployeeTrackerService** - Background service for automatic tracking
3. **EmployeeTrackerTray** - System tray application

### Platform-Specific Outputs

#### macOS
- **File Extension**: `.app` bundles
- **Icons**: PNG format (converted to ICNS by PyInstaller)
- **Data Separator**: `:` (colon)
- **Installation**: `/Applications/EmployeeTracker/`
- **Startup**: LaunchAgent plist files

#### Windows
- **File Extension**: `.exe` files
- **Icons**: ICO format
- **Data Separator**: `;` (semicolon)
- **Installation**: `%PROGRAMFILES%\EmployeeTracker\`
- **Startup**: Windows Startup folder shortcuts

## 📦 Output Structure

After building, you'll get:

```
DesktopTracker/
├── dist/                          # Raw executables
│   ├── EmployeeTrackerGUI.app     # macOS GUI app
│   ├── EmployeeTrackerService.app # macOS service
│   ├── EmployeeTrackerTray.app    # macOS tray app
│   ├── EmployeeTrackerGUI.exe     # Windows GUI exe
│   ├── EmployeeTrackerService.exe # Windows service exe
│   └── EmployeeTrackerTray.exe    # Windows tray exe
├── EmployeeTracker_Portable_macOS/ # macOS portable package
│   ├── EmployeeTrackerGUI.app
│   ├── EmployeeTrackerService.app
│   ├── EmployeeTrackerTray.app
│   ├── config.env
│   └── launcher.sh
├── EmployeeTracker_Portable_Windows/ # Windows portable package
│   ├── EmployeeTrackerGUI.exe
│   ├── EmployeeTrackerService.exe
│   ├── EmployeeTrackerTray.exe
│   ├── config.env
│   └── launcher.bat
├── install_macos.sh              # macOS installer script
├── install_windows.bat           # Windows installer script
├── icon.ico                      # Windows icon
└── icon.png                      # macOS icon
```

## 🛠️ Installation Options

### Option 1: System Installation

#### macOS
```bash
sudo ./install_macos.sh
```

This will:
- Install apps to `/Applications/EmployeeTracker/`
- Create desktop shortcuts
- Add service to startup items
- Set up LaunchAgent for automatic startup

#### Windows
```cmd
install_windows.bat
```

This will:
- Install executables to `%PROGRAMFILES%\EmployeeTracker\`
- Create desktop shortcuts
- Add service to Windows startup folder

### Option 2: Portable Usage

#### macOS
```bash
cd EmployeeTracker_Portable_macOS/
./launcher.sh
```

#### Windows
```cmd
cd EmployeeTracker_Portable_Windows\
launcher.bat
```

## 🔄 Cross-Platform Development

### Building for Different Platforms

**Important**: PyInstaller cannot cross-compile between platforms. You need to run the build script on the target platform.

#### To Build Windows Executables:
1. Run the build script on a Windows machine
2. Or use the cross-platform script and select option 2

#### To Build macOS Executables:
1. Run the build script on a macOS machine
2. Or use the cross-platform script and select option 3

### CI/CD Integration

For automated builds, you can use:

```bash
# Build for current platform only
echo "1" | python3 build_cross_platform.py

# Create installer scripts only
echo "4" | python3 build_cross_platform.py
```

## 🐛 Troubleshooting

### Common Issues

#### PyInstaller Not Found
```bash
# Install PyInstaller
pip install pyinstaller

# Or use the build script which auto-installs it
python3 build_exe.py
```

#### Permission Errors on macOS
```bash
# Make installer executable
chmod +x install_macos.sh

# Run with sudo for system installation
sudo ./install_macos.sh
```

#### Windows Build Fails
- Ensure you're running on Windows
- Check that Python and PyInstaller are properly installed
- Verify all dependencies are installed

#### macOS App Bundle Issues
- PyInstaller shows deprecation warnings for onefile mode with .app bundles
- This is normal and doesn't affect functionality
- Consider using `--onedir` instead of `--onefile` for future versions

### Build Cleanup

If builds fail or you want to start fresh:

```bash
# Clean build artifacts
rm -rf dist/ build/ *.spec

# Remove portable packages
rm -rf EmployeeTracker_Portable_*
```

## 📝 Configuration

### Environment Variables

The build process uses `config.env.example` as a template. Make sure to:

1. Copy `config.env.example` to `config.env`
2. Update the API token and base URL
3. The config file is automatically included in all builds

### Custom Icons

The build system creates icons automatically, but you can replace them:

- `icon.ico` - Windows icon (64x64 pixels)
- `icon.png` - macOS icon (64x64 pixels)

## 🚀 Distribution

### For End Users

1. **Windows Users**: Share `EmployeeTracker_Portable_Windows/` folder or `install_windows.bat`
2. **macOS Users**: Share `EmployeeTracker_Portable_macOS/` folder or `install_macos.sh`

### For Developers

1. Use `build_cross_platform.py` for interactive building
2. Use `build_exe.py` for automated platform-specific builds
3. Both scripts handle dependency installation automatically

## 📊 File Sizes

Typical executable sizes:

- **macOS .app bundles**: 6-10 MB each
- **Windows .exe files**: 6-10 MB each
- **Portable packages**: 20-30 MB total

## 🔒 Security Notes

- All executables are code-signed on macOS (self-signed)
- Windows executables may trigger antivirus warnings (false positives)
- Consider using a code signing certificate for production distribution

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure you're building on the correct platform
4. Check the PyInstaller logs in the `build/` directory

---

**Happy Building! 🎉**
