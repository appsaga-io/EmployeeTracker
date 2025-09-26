# 🖥️ Employee Tracker Background Service

## Overview

The Employee Tracker Background Service runs silently in the system tray, providing a non-intrusive way to track attendance without keeping a visible window open.

## Features

### 🎯 Core Features
- **System Tray Icon**: Runs in background with visual status indicators
- **Right-click Menu**: Access all controls through context menu
- **System Notifications**: Toast notifications for actions and reminders
- **Auto-start**: Can be configured to start with Windows
- **Silent Operation**: No visible windows, runs in background

### 📊 Status Indicators
- **Green Icon (✓)**: Present and checked in
- **Orange Icon (!)**: Late arrival
- **Blue Icon (ET)**: Other status
- **Gray Icon (?)**: No data available

### 🔧 Controls Available
- **Check In**: Start your work day
- **Check Out**: End your work day
- **Start Break**: Begin break time
- **End Break**: End break time
- **Settings**: Configure API token and view status
- **Refresh**: Update attendance data
- **Exit**: Close the application

## Quick Start

### 1. Install Dependencies
```bash
python setup.py
```

### 2. Configure API Token
Edit `config.env` and add your API token:
```env
API_BASE_URL=http://localhost:8080/api
API_TOKEN=your_token_here
```

### 3. Start Background Service
```bash
# Option 1: Direct Python
python src/background_service.py

# Option 2: Batch file
start_background.bat

# Option 3: PowerShell
.\start_background.ps1
```

### 4. Find the Tray Icon
Look for the "ET" icon in your system tray (bottom-right corner of screen)

## Usage Guide

### First Time Setup
1. **Start the service** using one of the methods above
2. **Right-click the tray icon**
3. **Select "Settings"**
4. **Enter your API token**
5. **Click "Save Token"**

### Daily Usage
1. **Right-click the tray icon** when you start work
2. **Select "Check In"** to start your day
3. **Use "Start Break"** and "End Break"** for breaks
4. **Select "Check Out"** when you finish work

### Monitoring
- **Right-click → "Employee Tracker"** to view current status
- **Icon color** indicates your current status
- **System notifications** will alert you of actions and reminders

## Installation as Windows Service

### Automatic Installation
```bash
python install_service.py
```

This will:
- Create service scripts
- Add startup shortcut
- Install required dependencies
- Create application icon

### Manual Installation
1. **Create startup shortcut**:
   - Copy `start_service.vbs` to Windows startup folder
   - Or add `start_service.bat` to Windows startup

2. **Configure auto-start**:
   - Right-click on `start_service.vbs`
   - Select "Create shortcut"
   - Move shortcut to startup folder

## Configuration

### Environment Variables
Edit `config.env`:
```env
# API Configuration
API_BASE_URL=http://localhost:8080/api
API_TOKEN=your_token_here

# Application Settings
AUTO_START_BREAK_AFTER_MINUTES=240
AUTO_REMINDER_ENABLED=true
REMINDER_INTERVAL_MINUTES=30

# UI Settings
THEME=light
WINDOW_SIZE=400x600
ALWAYS_ON_TOP=true
```

### API Token Setup
1. **Get token from Laravel**:
   ```bash
   cd ../EmployeeTracker
   php artisan tinker
   ```
   ```php
   $user = \App\Models\User::where('email', 'admin@example.com')->first();
   $token = $user->createToken('desktop-tracker')->plainTextToken;
   echo $token;
   ```

2. **Add to config.env**:
   ```env
   API_TOKEN=your_copied_token_here
   ```

## Troubleshooting

### Common Issues

1. **Tray icon not visible**:
   - Check if Windows is hiding tray icons
   - Look in "Show hidden icons" area
   - Restart the application

2. **API connection failed**:
   - Verify Laravel backend is running
   - Check API token in config.env
   - Test with `python test_api.py`

3. **Service won't start**:
   - Check Python installation
   - Install dependencies: `pip install -r requirements.txt`
   - Check config.env file exists

4. **Notifications not working**:
   - Check Windows notification settings
   - Ensure app has notification permissions
   - Try running as administrator

### Debug Mode
Enable debug logging:
```bash
set DEBUG=1
python src/background_service.py
```

### Log Files
Check `logs/` directory for application logs and error messages.

## Advanced Usage

### Custom Icons
Replace `icon.ico` with your custom icon file.

### Custom Notifications
Modify notification settings in the code:
```python
# In background_service.py
def show_notification(self, title, message):
    self.tray_icon.notify(message, title)
```

### Auto-start Configuration
1. **Windows Startup Folder**:
   - Press `Win + R`
   - Type `shell:startup`
   - Add `start_service.vbs`

2. **Registry Method**:
   - Run `install_service.py`
   - This will create registry entries

3. **Task Scheduler**:
   - Create a task to run `start_service.bat`
   - Set trigger to "At startup"

## Security Considerations

- **API Token**: Store securely, don't share
- **Network**: Use HTTPS in production
- **Permissions**: Run with minimal required permissions
- **Updates**: Keep dependencies updated

## Performance

- **Memory Usage**: ~20-30MB RAM
- **CPU Usage**: Minimal (only during API calls)
- **Network**: Only when making API requests
- **Disk**: Minimal (only for config and logs)

## Uninstallation

### Remove from Startup
1. Delete shortcut from startup folder
2. Remove registry entries (if created)
3. Delete task scheduler entries

### Remove Application
1. Stop the service
2. Delete application folder
3. Remove Python dependencies (optional)

## Support

For issues and support:
1. Check troubleshooting section
2. Review log files
3. Test API connectivity
4. Verify configuration

---

## 🎉 Ready to Use!

Your Employee Tracker Background Service is now ready to run silently in the background, providing seamless attendance tracking without any visible windows! 🚀

