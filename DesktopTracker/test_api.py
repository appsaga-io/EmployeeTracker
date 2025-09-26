#!/usr/bin/env python3
"""
API Test Script for Employee Tracker
Tests the connection to the Laravel API backend
"""

import requests
import json
import sys
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('config.env')

def test_api_connection():
    """Test basic API connection"""
    api_base_url = os.getenv('API_BASE_URL', 'http://localhost:8080/api')

    print("🔍 Testing API Connection")
    print("=" * 30)
    print(f"API URL: {api_base_url}")

    try:
        # Test basic connectivity
        response = requests.get(f"{api_base_url}/user", timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 401:
            print("✅ API is accessible (Authentication required)")
            return True
        elif response.status_code == 200:
            print("✅ API is accessible and authenticated")
            return True
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API")
        print("   Make sure the Laravel backend is running on http://localhost:8080")
        return False
    except requests.exceptions.Timeout:
        print("❌ Connection timeout")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_with_token():
    """Test API with authentication token"""
    api_base_url = os.getenv('API_BASE_URL', 'http://localhost:8080/api')
    api_token = os.getenv('API_TOKEN', '')

    if not api_token:
        print("\n⚠️  No API token found in config.env")
        print("   Please add your API token to config.env")
        return False

    print(f"\n🔑 Testing with API Token")
    print("=" * 30)

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(f"{api_base_url}/user", headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            user_data = response.json()
            print("✅ Authentication successful!")
            print(f"   User: {user_data.get('name', 'Unknown')}")
            print(f"   Email: {user_data.get('email', 'Unknown')}")
            return True
        elif response.status_code == 401:
            print("❌ Authentication failed - Invalid token")
            return False
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_attendance_endpoints():
    """Test attendance API endpoints"""
    api_base_url = os.getenv('API_BASE_URL', 'http://localhost:8080/api')
    api_token = os.getenv('API_TOKEN', '')

    if not api_token:
        print("\n⚠️  Skipping attendance tests - No API token")
        return False

    print(f"\n⏰ Testing Attendance Endpoints")
    print("=" * 30)

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # Test today's attendance
    try:
        response = requests.get(f"{api_base_url}/attendance/today", headers=headers, timeout=10)
        print(f"GET /attendance/today - Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Today's attendance endpoint working")
            else:
                print(f"⚠️  API returned error: {data.get('message', 'Unknown error')}")
        else:
            print(f"❌ Failed with status: {response.status_code}")

    except Exception as e:
        print(f"❌ Error testing attendance: {e}")

def main():
    """Main test function"""
    print("🧪 Employee Tracker API Test Suite")
    print("=" * 40)

    # Test basic connection
    if not test_api_connection():
        print("\n❌ Basic API connection failed!")
        print("   Please start the Laravel backend:")
        print("   cd ../EmployeeTracker")
        print("   php artisan serve --port=8080")
        sys.exit(1)

    # Test with token
    test_with_token()

    # Test attendance endpoints
    test_attendance_endpoints()

    print("\n✅ API tests completed!")
    print("\n📝 If all tests passed, you can run the desktop application:")
    print("   python src/main.py")

if __name__ == "__main__":
    main()

