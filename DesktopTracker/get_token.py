#!/usr/bin/env python3
"""
Get API Token for Employee Tracker Desktop Application
This script helps you get an API token from the Laravel backend
"""

import requests
import json
import sys

def get_token_from_laravel():
    """Instructions to get token from Laravel"""
    print("🔑 Getting API Token from Laravel Backend")
    print("=" * 50)

    print("To get your API token, please follow these steps:")
    print()
    print("1. Make sure the Laravel backend is running:")
    print("   cd ../EmployeeTracker")
    print("   php artisan serve --port=8080")
    print()
    print("2. Open a new terminal and run:")
    print("   cd ../EmployeeTracker")
    print("   php artisan tinker")
    print()
    print("3. In the tinker console, run these commands:")
    print("   $user = \\App\\Models\\User::where('email', 'admin@example.com')->first();")
    print("   $token = $user->createToken('desktop-tracker')->plainTextToken;")
    print("   echo $token;")
    print()
    print("4. Copy the token and paste it in the desktop application")
    print()
    print("Alternative: You can also use any of these pre-created users:")
    print("   - admin@example.com (password: password)")
    print("   - john@example.com (password: password)")
    print("   - jane@example.com (password: password)")

def test_backend_connection():
    """Test if the backend is running"""
    print("🔍 Testing Backend Connection")
    print("=" * 30)

    try:
        response = requests.get("http://localhost:8080", timeout=5)
        if response.status_code == 200 or response.status_code == 302:
            print("✅ Laravel backend is running on http://localhost:8080")
            return True
        else:
            print(f"⚠️  Backend responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Laravel backend")
        print("   Please start the backend first:")
        print("   cd ../EmployeeTracker")
        print("   php artisan serve --port=8080")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Employee Tracker - API Token Setup")
    print("=" * 40)

    # Test backend connection
    if test_backend_connection():
        get_token_from_laravel()
    else:
        print("\n❌ Please start the Laravel backend first!")
        sys.exit(1)

if __name__ == "__main__":
    main()

