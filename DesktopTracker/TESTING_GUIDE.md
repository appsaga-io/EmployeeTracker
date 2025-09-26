# 🧪 Employee Tracker Testing Guide

## Overview

This guide shows you how to test the Employee Tracker system to ensure everything works correctly before deployment.

## Testing Checklist

### ✅ Prerequisites Testing
- [ ] Laravel backend is running
- [ ] Database is migrated and seeded
- [ ] API endpoints are accessible
- [ ] Python dependencies are installed

### ✅ API Testing
- [ ] Authentication works
- [ ] Attendance endpoints respond
- [ ] Leave request endpoints work
- [ ] Error handling is proper

### ✅ Desktop Application Testing
- [ ] GUI version launches
- [ ] Background service runs
- [ ] System tray icon appears
- [ ] All controls work

### ✅ Integration Testing
- [ ] Desktop app connects to API
- [ ] Data syncs correctly
- [ ] Notifications work
- [ ] Error handling works

## Quick Test Commands

### 1. Test Laravel Backend
```bash
# Start Laravel backend
cd EmployeeTracker
php artisan serve --port=8080

# Test in browser
# Go to: http://localhost:8080
```

### 2. Test API Endpoints
```bash
# Test API connectivity
cd DesktopTracker
python test_api.py
```

### 3. Test Desktop Application
```bash
# Test GUI version
python src/main.py

# Test background service
python src/background_service.py

# Test background service
python test_background.py
```

### 4. Test Executable Building
```bash
# Build executables
python build_exe.py

# Or use batch file
build.bat
```

## Detailed Testing Steps

### Step 1: Laravel Backend Testing

#### 1.1 Start the Backend
```bash
cd EmployeeTracker
php artisan serve --port=8080
```

#### 1.2 Test Web Interface
1. Open browser: http://localhost:8080
2. Login with admin credentials:
   - Email: admin@example.com
   - Password: password
3. Verify dashboard loads
4. Check attendance and leave management sections

#### 1.3 Test API Endpoints
```bash
# Test user endpoint (should return 401 without token)
curl http://localhost:8080/api/user

# Test with token (replace YOUR_TOKEN)
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8080/api/user
```

### Step 2: Desktop Application Testing

#### 2.1 Test Dependencies
```bash
cd DesktopTracker
python test_background.py
```

#### 2.2 Test GUI Version
```bash
python src/main.py
```
**Expected:**
- Window opens with interface
- API token field is visible
- Buttons are present but disabled (no token set)

#### 2.3 Test Background Service
```bash
python src/background_service.py
```
**Expected:**
- No visible window
- System tray icon appears
- Right-click menu works

### Step 3: Integration Testing

#### 3.1 Get API Token
```bash
cd EmployeeTracker
php artisan tinker
```
```php
$user = \App\Models\User::where('email', 'admin@example.com')->first();
$token = $user->createToken('desktop-tracker')->plainTextToken;
echo $token;
```

#### 3.2 Configure Desktop App
1. Edit `config.env`:
   ```env
   API_BASE_URL=http://localhost:8080/api
   API_TOKEN=your_token_here
   ```

#### 3.3 Test Full Workflow
1. **Start desktop app**: `python src/background_service.py`
2. **Right-click tray icon** → Settings
3. **Enter API token** and save
4. **Right-click tray icon** → Check In
5. **Verify** in Laravel dashboard
6. **Test break** functionality
7. **Test check out** functionality

### Step 4: Executable Testing

#### 4.1 Build Executables
```bash
python build_exe.py
```

#### 4.2 Test Each Executable
1. **GUI Version**: `dist/EmployeeTrackerGUI.exe`
2. **Background Service**: `dist/EmployeeTrackerService.exe`
3. **Tray Application**: `dist/EmployeeTrackerTray.exe`

#### 4.3 Test Portable Package
1. **Copy** `EmployeeTracker_Portable` folder
2. **Run** `launcher.bat`
3. **Test** each version

## Automated Testing Scripts

### Test API Connectivity
```bash
python test_api.py
```

### Test Background Service
```bash
python test_background.py
```

### Test Token Generation
```bash
python get_token.py
```

## Common Issues and Solutions

### Issue 1: "Cannot connect to API"
**Solution:**
- Check Laravel backend is running
- Verify port 8080 is available
- Check firewall settings

### Issue 2: "API token not set"
**Solution:**
- Get token from Laravel tinker
- Add to config.env file
- Restart desktop app

### Issue 3: "Tray icon not visible"
**Solution:**
- Check system tray settings
- Look in "Show hidden icons"
- Restart the application

### Issue 4: "Executable won't start"
**Solution:**
- Check Windows Defender
- Run as administrator
- Verify system requirements

## Performance Testing

### Memory Usage
- **GUI Version**: ~50-80MB
- **Background Service**: ~30-50MB
- **Tray Application**: ~30-50MB

### CPU Usage
- **Idle**: <1%
- **API Calls**: 5-10%
- **Background**: <1%

### Network Usage
- **API Calls**: ~1-5KB per request
- **Background**: Minimal

## Load Testing

### Multiple Users
1. **Create multiple users** in Laravel
2. **Generate tokens** for each user
3. **Run multiple instances** of desktop app
4. **Test concurrent** check-ins

### API Load
1. **Use tools** like Postman or curl
2. **Send multiple requests** simultaneously
3. **Monitor** Laravel logs
4. **Check** database performance

## Security Testing

### Authentication
- **Test invalid tokens**
- **Test expired tokens**
- **Test token validation**

### Authorization
- **Test admin-only endpoints**
- **Test user permissions**
- **Test data isolation**

## Browser Testing

### Laravel Web Interface
- **Chrome**: Test all features
- **Firefox**: Test all features
- **Edge**: Test all features
- **Mobile**: Test responsive design

## Documentation Testing

### User Guides
- **Follow setup instructions**
- **Test all documented features**
- **Verify screenshots match**
- **Check for typos**

### API Documentation
- **Test all endpoints**
- **Verify request/response formats**
- **Check error messages**

## Deployment Testing

### Production Environment
1. **Deploy Laravel** to production server
2. **Update API_BASE_URL** in config
3. **Test from different locations**
4. **Verify HTTPS** works

### Desktop Distribution
1. **Test on different Windows versions**
2. **Test on different hardware**
3. **Test without Python installed**
4. **Test with antivirus enabled**

## Reporting Issues

### When Reporting Bugs
Include:
- **Operating System** version
- **Python version** (if applicable)
- **Laravel version**
- **Error messages**
- **Steps to reproduce**
- **Expected vs actual behavior**

### Log Files
Check these locations:
- **Laravel logs**: `storage/logs/laravel.log`
- **Desktop app logs**: `logs/` directory
- **Windows Event Viewer**: Application logs

---

## 🎯 Testing Complete!

Once all tests pass, your Employee Tracker system is ready for production use! 🚀

