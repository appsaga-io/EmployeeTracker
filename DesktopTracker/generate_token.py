#!/usr/bin/env python3
"""
API Token Generator for Employee Tracker
This script helps generate API tokens for the desktop application
"""

import requests
import json
import sys

def generate_token():
    """Generate API token by creating a user and getting token"""

    # API base URL
    api_base_url = "http://localhost:8080/api"

    print("🔑 Employee Tracker API Token Generator")
    print("=" * 40)

    # Get user credentials
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()

    if not email or not password:
        print("❌ Email and password are required!")
        return None

    try:
        # First, try to login via web interface to get session
        # For now, we'll use a direct approach with the API
        print("🔄 Generating token...")

        # Note: This is a simplified approach
        # In a real scenario, you'd need to implement proper authentication
        # For now, we'll show how to get token from Laravel tinker

        print("\n📋 To get your API token, please run the following commands:")
        print("1. Open terminal/command prompt")
        print("2. Navigate to the Laravel project directory")
        print("3. Run: php artisan tinker")
        print("4. In tinker, run:")
        print(f"   $user = \\App\\Models\\User::where('email', '{email}')->first();")
        print("   $token = $user->createToken('desktop-tracker')->plainTextToken;")
        print("   echo $token;")
        print("\n5. Copy the token and paste it in the desktop application")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_api_connection():
    """Test API connection"""
    api_base_url = "http://localhost:8080/api"

    print("\n🔍 Testing API connection...")

    try:
        response = requests.get(f"{api_base_url}/user", timeout=5)
        if response.status_code == 200:
            print("✅ API is accessible")
            return True
        else:
            print(f"⚠️  API responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the Laravel backend is running on http://localhost:8080")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Employee Tracker Setup Assistant")
    print("=" * 40)

    # Test API connection
    if not test_api_connection():
        print("\n❌ Please start the Laravel backend first:")
        print("   cd ../EmployeeTracker")
        print("   php artisan serve --port=8080")
        return

    # Generate token instructions
    generate_token()

    print("\n✅ Setup complete!")
    print("\n📝 Next steps:")
    print("1. Get your API token using the instructions above")
    print("2. Edit config.env file and add your token")
    print("3. Run the desktop application: python src/main.py")

if __name__ == "__main__":
    main()

