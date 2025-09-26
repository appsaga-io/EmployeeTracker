#!/usr/bin/env python3
"""
Employee Tracker System Tray Application
A background system tray application for tracking employee attendance
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
import json
import os
import threading
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pystray
from PIL import Image, ImageDraw
import sys

# Load environment variables
load_dotenv('config.env')

class EmployeeTrackerTray:
    def __init__(self):
        # API Configuration
        self.api_base_url = os.getenv('API_BASE_URL', 'http://localhost:8080/api')
        self.api_token = os.getenv('API_TOKEN', '')

        # Application state
        self.current_attendance = None
        self.is_break_active = False
        self.break_start_time = None
        self.reminder_thread = None
        self.reminder_running = False
        self.tray_icon = None

        # Create system tray icon
        self.create_tray_icon()

        # Load initial data
        self.load_attendance_data()

        # Start reminder thread
        self.start_reminder_thread()

    def create_tray_icon(self):
        """Create system tray icon"""
        # Create a simple icon
        image = Image.new('RGB', (64, 64), color='blue')
        draw = ImageDraw.Draw(image)
        draw.ellipse((16, 16, 48, 48), fill='white')
        draw.text((20, 20), "ET", fill='blue')

        # Create menu
        menu = pystray.Menu(
            pystray.MenuItem("Employee Tracker", self.show_status),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Check In", self.check_in, enabled=lambda item: self.can_check_in()),
            pystray.MenuItem("Check Out", self.check_out, enabled=lambda item: self.can_check_out()),
            pystray.MenuItem("Start Break", self.start_break, enabled=lambda item: self.can_start_break()),
            pystray.MenuItem("End Break", self.end_break, enabled=lambda item: self.can_end_break()),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Settings", self.show_settings),
            pystray.MenuItem("Refresh", self.load_attendance_data),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self.quit_app)
        )

        # Create tray icon
        self.tray_icon = pystray.Icon("EmployeeTracker", image, "Employee Tracker", menu)

    def can_check_in(self):
        """Check if user can check in"""
        if not self.current_attendance:
            return True
        return not bool(self.current_attendance.get('check_in'))

    def can_check_out(self):
        """Check if user can check out"""
        if not self.current_attendance:
            return False
        return bool(self.current_attendance.get('check_in')) and not bool(self.current_attendance.get('check_out'))

    def can_start_break(self):
        """Check if user can start break"""
        if not self.current_attendance:
            return False
        return bool(self.current_attendance.get('check_in')) and not bool(self.current_attendance.get('break_start'))

    def can_end_break(self):
        """Check if user can end break"""
        if not self.current_attendance:
            return False
        return bool(self.current_attendance.get('break_start')) and not bool(self.current_attendance.get('break_end'))

    def get_headers(self):
        """Get API headers with authentication"""
        if not self.api_token:
            raise Exception("API token not set!")
        return {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def make_api_request(self, method, endpoint, data=None):
        """Make API request to the Laravel backend"""
        try:
            url = f"{self.api_base_url}{endpoint}"
            headers = self.get_headers()

            if method.upper() == 'GET':
                response = requests.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            else:
                raise Exception(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.show_notification("API Error", f"Failed to connect to API: {str(e)}")
            return None
        except Exception as e:
            self.show_notification("Error", f"An error occurred: {str(e)}")
            return None

    def check_in(self, icon=None, item=None):
        """Check in for the day"""
        result = self.make_api_request('POST', '/attendance/check-in')
        if result and result.get('success'):
            self.show_notification("Success", "Checked in successfully!")
            self.load_attendance_data()
        else:
            self.show_notification("Error", result.get('message', 'Failed to check in'))

    def check_out(self, icon=None, item=None):
        """Check out for the day"""
        result = self.make_api_request('POST', '/attendance/check-out')
        if result and result.get('success'):
            self.show_notification("Success", "Checked out successfully!")
            self.load_attendance_data()
        else:
            self.show_notification("Error", result.get('message', 'Failed to check out'))

    def start_break(self, icon=None, item=None):
        """Start break"""
        result = self.make_api_request('POST', '/attendance/break-start')
        if result and result.get('success'):
            self.is_break_active = True
            self.break_start_time = datetime.now()
            self.show_notification("Success", "Break started!")
            self.load_attendance_data()
        else:
            self.show_notification("Error", result.get('message', 'Failed to start break'))

    def end_break(self, icon=None, item=None):
        """End break"""
        result = self.make_api_request('POST', '/attendance/break-end')
        if result and result.get('success'):
            self.is_break_active = False
            self.break_start_time = None
            self.show_notification("Success", "Break ended!")
            self.load_attendance_data()
        else:
            self.show_notification("Error", result.get('message', 'Failed to end break'))

    def load_attendance_data(self, icon=None, item=None):
        """Load today's attendance data"""
        if not self.api_token:
            self.show_notification("Configuration", "Please set API token in settings")
            return

        result = self.make_api_request('GET', '/attendance/today')
        if result and result.get('success'):
            self.current_attendance = result.get('data')
            self.update_tray_icon()
        else:
            self.current_attendance = None
            self.update_tray_icon()

    def update_tray_icon(self):
        """Update tray icon based on current status"""
        if not self.current_attendance:
            # No data - gray icon
            image = Image.new('RGB', (64, 64), color='gray')
            draw = ImageDraw.Draw(image)
            draw.ellipse((16, 16, 48, 48), fill='white')
            draw.text((20, 20), "?", fill='gray')
        else:
            status = self.current_attendance.get('status', 'unknown')
            if status == 'present':
                # Present - green icon
                image = Image.new('RGB', (64, 64), color='green')
                draw = ImageDraw.Draw(image)
                draw.ellipse((16, 16, 48, 48), fill='white')
                draw.text((20, 20), "✓", fill='green')
            elif status == 'late':
                # Late - yellow icon
                image = Image.new('RGB', (64, 64), color='orange')
                draw = ImageDraw.Draw(image)
                draw.ellipse((16, 16, 48, 48), fill='white')
                draw.text((20, 20), "!", fill='orange')
            else:
                # Other status - blue icon
                image = Image.new('RGB', (64, 64), color='blue')
                draw = ImageDraw.Draw(image)
                draw.ellipse((16, 16, 48, 48), fill='white')
                draw.text((20, 20), "ET", fill='blue')

        self.tray_icon.icon = image

    def show_status(self, icon=None, item=None):
        """Show current status in a popup"""
        if not self.current_attendance:
            self.show_notification("Status", "No attendance data for today")
            return

        status = self.current_attendance.get('status', 'Unknown').title()
        check_in = self.current_attendance.get('check_in', 'Not checked in')
        check_out = self.current_attendance.get('check_out', 'Not checked out')
        work_minutes = self.current_attendance.get('total_work_minutes', 0)
        break_minutes = self.current_attendance.get('total_break_minutes', 0)

        message = f"Status: {status}\n"
        message += f"Check In: {check_in}\n"
        message += f"Check Out: {check_out}\n"
        message += f"Work Hours: {work_minutes // 60}h {work_minutes % 60}m\n"
        message += f"Break Time: {break_minutes}m"

        self.show_notification("Today's Status", message)

    def show_settings(self, icon=None, item=None):
        """Show settings dialog"""
        # Create a simple settings window
        settings_window = tk.Tk()
        settings_window.title("Employee Tracker Settings")
        settings_window.geometry("400x300")
        settings_window.resizable(False, False)

        # Make window stay on top
        settings_window.attributes('-topmost', True)

        # API Token section
        token_frame = ttk.LabelFrame(settings_window, text="API Configuration", padding="10")
        token_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(token_frame, text="API Token:").pack(anchor=tk.W)
        token_entry = ttk.Entry(token_frame, width=50, show="*")
        token_entry.pack(fill=tk.X, pady=(5, 0))
        token_entry.insert(0, self.api_token)

        def save_token():
            token = token_entry.get().strip()
            if token:
                self.api_token = token
                # Save to config file
                with open('config.env', 'w') as f:
                    f.write(f"API_BASE_URL={self.api_base_url}\n")
                    f.write(f"API_TOKEN={token}\n")
                self.show_notification("Settings", "API Token updated successfully!")
                self.load_attendance_data()
                settings_window.destroy()
            else:
                messagebox.showerror("Error", "Please enter a valid API token!")

        ttk.Button(token_frame, text="Save Token", command=save_token).pack(pady=(10, 0))

        # Status section
        status_frame = ttk.LabelFrame(settings_window, text="Current Status", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        status_text = tk.Text(status_frame, height=8, state=tk.DISABLED)
        status_text.pack(fill=tk.BOTH, expand=True)

        if self.current_attendance:
            status_info = f"Date: {self.current_attendance.get('date', 'N/A')}\n"
            status_info += f"Check In: {self.current_attendance.get('check_in', 'Not checked in')}\n"
            status_info += f"Check Out: {self.current_attendance.get('check_out', 'Not checked out')}\n"
            status_info += f"Break Start: {self.current_attendance.get('break_start', 'Not started')}\n"
            status_info += f"Break End: {self.current_attendance.get('break_end', 'Not ended')}\n"
            status_info += f"Total Work Minutes: {self.current_attendance.get('total_work_minutes', 0)}\n"
            status_info += f"Total Break Minutes: {self.current_attendance.get('total_break_minutes', 0)}\n"
            status_info += f"Status: {self.current_attendance.get('status', 'Unknown').title()}"
        else:
            status_info = "No attendance data available"

        status_text.config(state=tk.NORMAL)
        status_text.insert(1.0, status_info)
        status_text.config(state=tk.DISABLED)

        # Close button
        ttk.Button(settings_window, text="Close", command=settings_window.destroy).pack(pady=10)

        settings_window.mainloop()

    def show_notification(self, title, message):
        """Show system notification"""
        try:
            self.tray_icon.notify(message, title)
        except:
            # Fallback to messagebox if notification fails
            messagebox.showinfo(title, message)

    def start_reminder_thread(self):
        """Start the reminder thread"""
        if not self.reminder_running:
            self.reminder_running = True
            self.reminder_thread = threading.Thread(target=self.reminder_loop, daemon=True)
            self.reminder_thread.start()

    def reminder_loop(self):
        """Reminder loop for break reminders"""
        while self.reminder_running:
            try:
                if self.current_attendance and self.current_attendance.get('check_in'):
                    # Check if user has been working for more than 4 hours without a break
                    check_in_time = self.current_attendance.get('check_in')
                    if check_in_time and not self.current_attendance.get('break_start'):
                        # Parse time and check if 4+ hours have passed
                        check_in_dt = datetime.strptime(f"{self.current_attendance.get('date')} {check_in_time}", "%Y-%m-%d %H:%M:%S")
                        if datetime.now() - check_in_dt > timedelta(hours=4):
                            self.show_notification(
                                "Break Reminder",
                                "You've been working for more than 4 hours. Consider taking a break!"
                            )
            except Exception as e:
                print(f"Reminder error: {e}")

            time.sleep(1800)  # Check every 30 minutes

    def quit_app(self, icon=None, item=None):
        """Quit the application"""
        self.reminder_running = False
        self.tray_icon.stop()
        sys.exit(0)

    def run(self):
        """Run the application"""
        self.tray_icon.run()

def main():
    """Main function"""
    app = EmployeeTrackerTray()
    app.run()

if __name__ == "__main__":
    main()

