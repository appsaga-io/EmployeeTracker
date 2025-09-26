#!/usr/bin/env python3
"""
Test script for Employee Tracker Background Service
Tests the background service functionality
"""

import sys
import os
import time
import threading
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")

    try:
        import requests
        print("✅ requests imported")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False

    try:
        import pystray
        print("✅ pystray imported")
    except ImportError as e:
        print(f"❌ pystray import failed: {e}")
        return False

    try:
        from PIL import Image, ImageDraw
        print("✅ PIL imported")
    except ImportError as e:
        print(f"❌ PIL import failed: {e}")
        return False

    try:
        import tkinter as tk
        print("✅ tkinter imported")
    except ImportError as e:
        print(f"❌ tkinter import failed: {e}")
        return False

    return True

def test_config():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")

    load_dotenv('config.env')

    api_base_url = os.getenv('API_BASE_URL', 'http://localhost:8080/api')
    api_token = os.getenv('API_TOKEN', '')

    print(f"API Base URL: {api_base_url}")
    print(f"API Token: {'Set' if api_token else 'Not set'}")

    if not api_token:
        print("⚠️  API token not set. Please configure config.env")
        return False

    return True

def test_api_connection():
    """Test API connection"""
    print("\n🌐 Testing API connection...")

    load_dotenv('config.env')
    api_base_url = os.getenv('API_BASE_URL', 'http://localhost:8080/api')
    api_token = os.getenv('API_TOKEN', '')

    if not api_token:
        print("❌ No API token configured")
        return False

    try:
        import requests

        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.get(f"{api_base_url}/user", headers=headers, timeout=10)

        if response.status_code == 200:
            print("✅ API connection successful")
            return True
        else:
            print(f"❌ API connection failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ API connection error: {e}")
        return False

def test_background_service():
    """Test background service creation"""
    print("\n🖥️ Testing background service...")

    try:
        from background_service import BackgroundTrackerService

        # Create service instance (don't run it)
        service = BackgroundTrackerService()
        print("✅ Background service created successfully")

        # Test tray icon creation
        if service.tray_icon:
            print("✅ Tray icon created successfully")
        else:
            print("❌ Tray icon creation failed")
            return False

        return True

    except Exception as e:
        print(f"❌ Background service test failed: {e}")
        return False

def test_gui_components():
    """Test GUI components"""
    print("\n🖼️ Testing GUI components...")

    try:
        import tkinter as tk
        from tkinter import messagebox

        # Test basic tkinter functionality
        root = tk.Tk()
        root.withdraw()  # Hide the window

        # Test messagebox
        # messagebox.showinfo("Test", "GUI test successful")

        root.destroy()
        print("✅ GUI components working")
        return True

    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Employee Tracker Background Service Test Suite")
    print("=" * 60)

    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_config),
        ("API Connection Test", test_api_connection),
        ("Background Service Test", test_background_service),
        ("GUI Components Test", test_gui_components),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")

    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Background service is ready to use.")
        print("\n🚀 To start the service:")
        print("   python src/background_service.py")
        print("   or")
        print("   start_background.bat")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        print("\n🔧 Common fixes:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Configure API token in config.env")
        print("   3. Start Laravel backend: php artisan serve --port=8080")

if __name__ == "__main__":
    main()

