# Employee Tracker Desktop Application

A Windows desktop application for tracking employee attendance using the Laravel API backend.

## Features

- ✅ **Check In/Out**: Track daily attendance
- ⏰ **Break Management**: Start and end breaks
- 📊 **Real-time Status**: View current attendance status
- 🔔 **Break Reminders**: Automatic reminders after 4 hours of work
- 🔐 **API Integration**: Secure authentication with Laravel backend
- 🐳 **Docker Support**: Easy deployment with Docker
- 🖥️ **System Tray**: Runs in background with system tray icon
- 🚀 **Auto-start**: Can be configured to start with Windows
- 📦 **Executable**: Can be built into standalone .exe files

## Prerequisites

- Python 3.11+ (for local development)
- Docker & Docker Compose (for containerized deployment)
- Laravel API backend running on http://localhost:8080

## Quick Start

### Option 1: Docker (Recommended)

1. **Build and run with Docker:**
   ```bash
   docker-compose up --build
   ```

2. **Get API Token:**
   - Go to http://localhost:8080
   - Login with admin credentials
   - Generate API token (see API documentation)

3. **Configure the app:**
   - Edit `config.env` file
   - Add your API token

### Option 2: Local Development

1. **Setup the application:**
   ```bash
   python setup.py
   ```

2. **Get API Token:**
   - Go to http://localhost:8080
   - Login with admin credentials
   - Generate API token

3. **Configure the app:**
   - Edit `config.env` file
   - Add your API token

4. **Run the application:**
   ```bash
   # Full GUI version
   python src/main.py
   
   # Background service (system tray)
   python src/background_service.py
   
   # Or use launchers
   start_background.bat
   start_background.ps1
   ```

## Configuration

Edit the `config.env` file to configure the application:

```env
# API Configuration
API_BASE_URL=http://localhost:8080/api
API_TOKEN=your_api_token_here

# Application Settings
AUTO_START_BREAK_AFTER_MINUTES=240
AUTO_REMINDER_ENABLED=true
REMINDER_INTERVAL_MINUTES=30

# UI Settings
THEME=light
WINDOW_SIZE=400x600
ALWAYS_ON_TOP=true
```

## Getting API Token

### Method 1: Using Laravel Tinker
```bash
cd ../EmployeeTracker
php artisan tinker
```
Then in tinker:
```php
$user = \App\Models\User::where('email', 'admin@example.com')->first();
$token = $user->createToken('desktop-tracker')->plainTextToken;
echo $token;
```

### Method 2: Using Web Interface
1. Go to http://localhost:8080
2. Login with admin credentials
3. Use the API endpoints to generate a token

## Usage

### Full GUI Version
1. **Launch the application**: `python src/main.py`
2. **Set API Token**: Enter your API token in the configuration section
3. **Check In**: Click "Check In" when you start work
4. **Take Breaks**: Use "Start Break" and "End Break" buttons
5. **Check Out**: Click "Check Out" when you finish work

### Background Service (System Tray)
1. **Launch the service**: `python src/background_service.py` or `start_background.bat`
2. **Find the tray icon**: Look for the "ET" icon in your system tray
3. **Right-click the icon**: Access all controls through the context menu
4. **Configure**: Use "Settings" to set your API token
5. **Monitor**: Use "Employee Tracker" to view current status

### System Tray Features
- **Right-click menu** with all attendance actions
- **Visual status indicators** (green=present, orange=late, gray=no data)
- **System notifications** for actions and reminders
- **Background operation** - no visible windows
- **Auto-start capability** with Windows

## Features in Detail

### Attendance Tracking
- **Check In**: Records your start time for the day
- **Check Out**: Records your end time and calculates total work hours
- **Break Management**: Track break times and total break duration
- **Status Display**: Shows current attendance status (Present, Late, Absent)

### Break Reminders
- Automatic reminders after 4 hours of continuous work
- Configurable reminder intervals
- Visual notifications for break suggestions

### Real-time Updates
- Live status updates
- Today's summary display
- Work hour calculations
- Break time tracking

## API Integration

The desktop app integrates with the following Laravel API endpoints:

- `POST /api/attendance/check-in` - Check in
- `POST /api/attendance/check-out` - Check out
- `POST /api/attendance/break-start` - Start break
- `POST /api/attendance/break-end` - End break
- `GET /api/attendance/today` - Get today's attendance

## Troubleshooting

### Common Issues

1. **"API token not set" error:**
   - Make sure you've entered a valid API token
   - Verify the token is correct by testing with the API

2. **"Failed to connect to API" error:**
   - Check if the Laravel backend is running on http://localhost:8080
   - Verify the API_BASE_URL in config.env

3. **Docker GUI issues on Windows:**
   - Make sure X11 forwarding is enabled
   - Use WSL2 with X11 server for better compatibility

### Debug Mode

Enable debug mode by setting environment variable:
```bash
export DEBUG=1
python src/main.py
```

## Development

### Project Structure
```
DesktopTracker/
├── src/
│   ├── main.py              # Full GUI application
│   ├── tray_app.py          # System tray application
│   └── background_service.py # Background service
├── config/
│   └── config.env           # Configuration file
├── logs/                    # Application logs
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── setup.py               # Setup script
├── install_service.py      # Windows service installer
├── start_background.bat    # Background service launcher
├── start_background.ps1    # PowerShell launcher
├── run.bat                 # Full GUI launcher
├── run.ps1                 # PowerShell GUI launcher
└── README.md              # This file
```

### Adding New Features

1. Modify `src/main.py` for UI changes
2. Update `requirements.txt` for new dependencies
3. Test with Docker: `docker-compose up --build`

## License

This project is part of the Employee Tracker system and follows the same license terms.

## Support

For issues and support:
1. Check the troubleshooting section
2. Verify API connectivity
3. Check application logs in the `logs/` directory
