#!/usr/bin/env python3
"""
Setup script for Employee Tracker Desktop Application
"""

import os
import subprocess
import sys

def install_requirements():
    """Install Python requirements"""
    print("Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    return True

def create_config():
    """Create configuration file if it doesn't exist"""
    config_file = "config.env"
    if not os.path.exists(config_file):
        print("Creating configuration file...")
        with open(config_file, 'w') as f:
            f.write("# API Configuration\n")
            f.write("API_BASE_URL=http://localhost:8080/api\n")
            f.write("API_TOKEN=\n")
            f.write("\n")
            f.write("# Application Settings\n")
            f.write("AUTO_START_BREAK_AFTER_MINUTES=240\n")
            f.write("AUTO_REMINDER_ENABLED=true\n")
            f.write("REMINDER_INTERVAL_MINUTES=30\n")
            f.write("\n")
            f.write("# UI Settings\n")
            f.write("THEME=light\n")
            f.write("WINDOW_SIZE=400x600\n")
            f.write("ALWAYS_ON_TOP=true\n")
        print("✅ Configuration file created!")
    else:
        print("✅ Configuration file already exists!")

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'config']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")

def main():
    """Main setup function"""
    print("🚀 Setting up Employee Tracker Desktop Application...")
    print("=" * 50)

    # Create directories
    create_directories()

    # Create config file
    create_config()

    # Install requirements
    if install_requirements():
        print("\n✅ Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Get an API token from the Laravel application")
        print("2. Edit config.env and add your API token")
        print("3. Run: python src/main.py")
        print("\n🐳 Or use Docker:")
        print("1. docker-compose up --build")
    else:
        print("\n❌ Setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()

