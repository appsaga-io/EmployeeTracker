# 🚀 Employee Tracker Desktop Application - Setup Guide

## Quick Start (Windows)

### Option 1: Using Docker (Recommended)

1. **Prerequisites:**
   - Docker Desktop installed
   - Laravel backend running on http://localhost:8080

2. **Run the application:**
   ```bash
   docker-setup.bat
   ```

### Option 2: Using Python (Local Development)

1. **Prerequisites:**
   - Python 3.11+ installed
   - Laravel backend running on http://localhost:8080

2. **Setup and run:**
   ```bash
   python setup.py
   python src/main.py
   ```

## Detailed Setup Instructions

### Step 1: Start the Laravel Backend

1. Open terminal/command prompt
2. Navigate to the Laravel project:
   ```bash
   cd ../EmployeeTracker
   ```
3. Start the Laravel server:
   ```bash
   php artisan serve --port=8080
   ```
4. Verify it's running by visiting: http://localhost:8080

### Step 2: Get API Token

#### Method 1: Using Laravel Tinker (Recommended)

1. Open a new terminal
2. Navigate to the Laravel project:
   ```bash
   cd ../EmployeeTracker
   ```
3. Run tinker:
   ```bash
   php artisan tinker
   ```
4. In tinker, run these commands:
   ```php
   $user = \App\Models\User::where('email', 'admin@example.com')->first();
   $token = $user->createToken('desktop-tracker')->plainTextToken;
   echo $token;
   ```
5. Copy the token (it will be a long string)

#### Method 2: Using the Helper Script

1. Run the token helper:
   ```bash
   python get_token.py
   ```
2. Follow the instructions displayed

### Step 3: Configure the Desktop App

1. Edit the `config.env` file
2. Add your API token:
   ```env
   API_BASE_URL=http://localhost:8080/api
   API_TOKEN=your_token_here
   ```

### Step 4: Run the Desktop Application

#### Using Python:
```bash
python src/main.py
```

#### Using Docker:
```bash
docker-compose up --build
```

#### Using Windows Batch:
```bash
run.bat
```

#### Using PowerShell:
```powershell
.\run.ps1
```

## Testing the Setup

Run the API test script to verify everything is working:

```bash
python test_api.py
```

This will test:
- ✅ Backend connectivity
- ✅ API authentication
- ✅ Attendance endpoints

## Troubleshooting

### Common Issues

1. **"Cannot connect to API" error:**
   - Make sure Laravel backend is running on http://localhost:8080
   - Check if port 8080 is available

2. **"API token not set" error:**
   - Make sure you've added the token to config.env
   - Verify the token is correct

3. **Docker GUI issues:**
   - On Windows, make sure X11 forwarding is enabled
   - Use WSL2 with X11 server for better compatibility

4. **Python dependencies issues:**
   - Run: `pip install -r requirements.txt`
   - Make sure Python 3.11+ is installed

### Debug Mode

Enable debug mode for more detailed error messages:

```bash
set DEBUG=1
python src/main.py
```

## Application Features

### Main Interface
- **API Configuration**: Set your API token
- **Current Status**: Shows today's attendance status
- **Attendance Actions**: Check in/out, start/end breaks
- **Today's Summary**: Detailed attendance information

### Key Features
- ✅ Real-time attendance tracking
- ⏰ Break management
- 🔔 Automatic break reminders (after 4 hours)
- 📊 Work hour calculations
- 🔐 Secure API authentication

## File Structure

```
DesktopTracker/
├── src/
│   └── main.py              # Main application
├── config/
│   └── config.env           # Configuration file
├── logs/                    # Application logs
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── setup.py               # Setup script
├── test_api.py            # API test script
├── get_token.py           # Token helper script
├── run.bat                # Windows batch launcher
├── run.ps1                # PowerShell launcher
├── docker-setup.bat       # Docker setup script
└── README.md              # Documentation
```

## Support

If you encounter issues:

1. Check the troubleshooting section
2. Run `python test_api.py` to diagnose API issues
3. Verify the Laravel backend is running
4. Check the application logs in the `logs/` directory

## Next Steps

Once the desktop application is running:

1. Set your API token
2. Check in when you start work
3. Use break management features
4. Check out when you finish work
5. Monitor your attendance summary

The application will automatically sync with the Laravel backend and update your attendance records in real-time!

