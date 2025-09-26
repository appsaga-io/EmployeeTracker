# 🎯 Employee Tracker Desktop Application - Complete Overview

## 📁 Project Structure

```
EmployeeTracker/
├── 📁 DesktopTracker/                    # Desktop Application
│   ├── 📁 src/
│   │   └── main.py                      # Main GUI application
│   ├── 📁 config/
│   │   └── config.env                   # Configuration file
│   ├── 📁 logs/                         # Application logs
│   ├── 🐳 Dockerfile                    # Docker configuration
│   ├── 🐳 docker-compose.yml            # Docker Compose setup
│   ├── 📋 requirements.txt              # Python dependencies
│   ├── ⚙️ setup.py                      # Setup script
│   ├── 🧪 test_api.py                   # API testing script
│   ├── 🔑 get_token.py                  # Token helper script
│   ├── 🚀 run.bat                       # Windows batch launcher
│   ├── 🚀 run.ps1                       # PowerShell launcher
│   ├── 🐳 docker-setup.bat              # Docker setup script
│   ├── 📖 README.md                     # Main documentation
│   ├── 📖 SETUP_GUIDE.md                # Detailed setup guide
│   └── 📖 OVERVIEW.md                   # This file
└── 📁 EmployeeTracker/                  # Laravel Backend
    ├── 📁 app/
    ├── 📁 database/
    ├── 📁 routes/
    └── ... (Laravel files)
```

## 🚀 Quick Start

### 1. Start Laravel Backend
```bash
cd EmployeeTracker
php artisan serve --port=8080
```

### 2. Get API Token
```bash
cd DesktopTracker
python get_token.py
```

### 3. Run Desktop App
```bash
# Option 1: Python
python src/main.py

# Option 2: Docker
docker-compose up --build

# Option 3: Windows
run.bat
```

## 🔧 Features

### Desktop Application Features
- ✅ **Check In/Out**: Track daily attendance
- ⏰ **Break Management**: Start and end breaks
- 📊 **Real-time Status**: Live attendance updates
- 🔔 **Break Reminders**: Automatic reminders after 4 hours
- 🔐 **Secure API**: Token-based authentication
- 🐳 **Docker Support**: Easy deployment
- 🖥️ **Windows GUI**: Native Windows application

### Laravel Backend Features
- 🔐 **Sanctum Authentication**: Secure API tokens
- 📊 **Livewire Dashboards**: Real-time admin/employee dashboards
- ⏰ **Attendance Tracking**: Complete attendance management
- 🏖️ **Leave Management**: Leave request system
- 👥 **User Management**: Admin and employee roles
- 📈 **Reports**: Attendance and leave reports

## 🔌 API Integration

The desktop app integrates with these Laravel API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/user` | GET | Get current user info |
| `/api/attendance/check-in` | POST | Check in |
| `/api/attendance/check-out` | POST | Check out |
| `/api/attendance/break-start` | POST | Start break |
| `/api/attendance/break-end` | POST | End break |
| `/api/attendance/today` | GET | Get today's attendance |
| `/api/leave-requests` | GET/POST | Manage leave requests |

## 🛠️ Technology Stack

### Desktop Application
- **Python 3.11+**: Core language
- **Tkinter**: GUI framework
- **Requests**: HTTP client for API calls
- **Python-dotenv**: Environment configuration
- **Docker**: Containerization

### Laravel Backend
- **Laravel 12**: PHP framework
- **Livewire**: Real-time components
- **Sanctum**: API authentication
- **Bootstrap 5**: UI framework
- **SQLite**: Database (configurable)

## 📋 Prerequisites

### For Desktop Application
- Python 3.11+ (for local development)
- Docker Desktop (for containerized deployment)
- Windows 10/11 (target platform)

### For Laravel Backend
- PHP 8.1+
- Composer
- SQLite (or MySQL/PostgreSQL)

## 🚀 Deployment Options

### Option 1: Local Development
1. Install Python 3.11+
2. Install Laravel backend dependencies
3. Run both applications locally

### Option 2: Docker Deployment
1. Install Docker Desktop
2. Use docker-compose for easy deployment
3. Both applications run in containers

### Option 3: Production Deployment
1. Deploy Laravel backend to server
2. Update API_BASE_URL in config
3. Deploy desktop app to workstations

## 🔐 Security Features

- **API Token Authentication**: Secure token-based auth
- **HTTPS Support**: Encrypted communication
- **Input Validation**: Server-side validation
- **Role-based Access**: Admin/employee permissions
- **Session Management**: Secure session handling

## 📊 Monitoring & Logging

- **Application Logs**: Stored in `logs/` directory
- **API Logging**: Laravel logs API requests
- **Error Tracking**: Comprehensive error handling
- **Debug Mode**: Detailed debugging information

## 🎯 Use Cases

### For Employees
- Track daily attendance
- Manage break times
- View attendance history
- Submit leave requests

### For Administrators
- Monitor employee attendance
- Approve/reject leave requests
- Generate attendance reports
- Manage user accounts

### For Organizations
- Centralized attendance management
- Real-time attendance tracking
- Leave management system
- Compliance reporting

## 🔄 Workflow

1. **Employee starts work** → Check in via desktop app
2. **During work** → Take breaks using app
3. **End of day** → Check out via desktop app
4. **Admin monitoring** → View real-time dashboard
5. **Leave requests** → Submit and manage via web interface

## 📈 Future Enhancements

- **Mobile App**: iOS/Android companion app
- **Biometric Integration**: Fingerprint/face recognition
- **GPS Tracking**: Location-based attendance
- **Advanced Reporting**: Detailed analytics
- **Integration**: HR system integration
- **Notifications**: Push notifications

## 🆘 Support & Troubleshooting

### Common Issues
1. **API Connection**: Check Laravel backend status
2. **Authentication**: Verify API token
3. **Docker Issues**: Check Docker Desktop status
4. **Python Dependencies**: Run `pip install -r requirements.txt`

### Debug Tools
- `python test_api.py`: Test API connectivity
- `python get_token.py`: Get API token
- Debug mode: Set `DEBUG=1` environment variable

## 📞 Getting Help

1. Check the troubleshooting section
2. Run the test scripts
3. Check application logs
4. Verify backend connectivity
5. Review configuration files

---

## 🎉 Ready to Use!

Your complete Employee Tracker system is now ready with:
- ✅ Laravel 12 backend with Livewire
- ✅ Desktop application for Windows
- ✅ Docker support for easy deployment
- ✅ Complete API integration
- ✅ Real-time attendance tracking
- ✅ Leave management system

Start by running the Laravel backend and then launch the desktop application! 🚀

