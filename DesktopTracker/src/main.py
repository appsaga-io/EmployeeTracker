#!/usr/bin/env python3
"""
Employee Tracker Desktop Application
A simple desktop application for tracking employee attendance using the Laravel API
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import requests
import json
import os
from datetime import datetime, timedelta
import threading
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

class EmployeeTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Employee Tracker")
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        # API Configuration
        self.api_base_url = os.getenv('API_BASE_URL', 'http://localhost:8080/api')
        self.api_token = os.getenv('API_TOKEN', '')

        # Application state
        self.current_attendance = None
        self.is_break_active = False
        self.break_start_time = None
        self.reminder_thread = None
        self.reminder_running = False

        # Setup UI
        self.setup_ui()
        self.load_attendance_data()

        # Start reminder thread
        self.start_reminder_thread()

    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="Employee Tracker",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # API Token section
        token_frame = ttk.LabelFrame(main_frame, text="API Configuration", padding="5")
        token_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(token_frame, text="API Token:").grid(row=0, column=0, sticky=tk.W)
        self.token_entry = ttk.Entry(token_frame, width=40, show="*")
        self.token_entry.grid(row=0, column=1, padx=(5, 0))
        self.token_entry.insert(0, self.api_token)

        ttk.Button(token_frame, text="Set Token",
                  command=self.set_api_token).grid(row=0, column=2, padx=(5, 0))

        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Current Status", padding="5")
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        self.status_label = ttk.Label(status_frame, text="Not checked in",
                                     font=('Arial', 12))
        self.status_label.grid(row=0, column=0, columnspan=2)

        self.time_label = ttk.Label(status_frame, text="", font=('Arial', 10))
        self.time_label.grid(row=1, column=0, columnspan=2)

        # Attendance buttons
        button_frame = ttk.LabelFrame(main_frame, text="Attendance Actions", padding="5")
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        self.checkin_btn = ttk.Button(button_frame, text="Check In",
                                     command=self.check_in, state=tk.NORMAL)
        self.checkin_btn.grid(row=0, column=0, padx=5, pady=5)

        self.checkout_btn = ttk.Button(button_frame, text="Check Out",
                                      command=self.check_out, state=tk.DISABLED)
        self.checkout_btn.grid(row=0, column=1, padx=5, pady=5)

        self.break_start_btn = ttk.Button(button_frame, text="Start Break",
                                         command=self.start_break, state=tk.DISABLED)
        self.break_start_btn.grid(row=1, column=0, padx=5, pady=5)

        self.break_end_btn = ttk.Button(button_frame, text="End Break",
                                       command=self.end_break, state=tk.DISABLED)
        self.break_end_btn.grid(row=1, column=1, padx=5, pady=5)

        # Today's summary
        summary_frame = ttk.LabelFrame(main_frame, text="Today's Summary", padding="5")
        summary_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        self.summary_text = tk.Text(summary_frame, height=8, width=45, state=tk.DISABLED)
        self.summary_text.grid(row=0, column=0, columnspan=2)

        # Refresh button
        ttk.Button(main_frame, text="Refresh Data",
                  command=self.load_attendance_data).grid(row=5, column=0, columnspan=2, pady=10)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def set_api_token(self):
        """Set the API token"""
        token = self.token_entry.get().strip()
        if token:
            self.api_token = token
            # Save to config file
            with open('config.env', 'w') as f:
                f.write(f"API_BASE_URL={self.api_base_url}\n")
                f.write(f"API_TOKEN={token}\n")
            messagebox.showinfo("Success", "API Token updated successfully!")
            self.load_attendance_data()
        else:
            messagebox.showerror("Error", "Please enter a valid API token!")

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
            messagebox.showerror("API Error", f"Failed to connect to API: {str(e)}")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return None

    def check_in(self):
        """Check in for the day"""
        result = self.make_api_request('POST', '/attendance/check-in')
        if result and result.get('success'):
            messagebox.showinfo("Success", "Checked in successfully!")
            self.load_attendance_data()
        else:
            messagebox.showerror("Error", result.get('message', 'Failed to check in'))

    def check_out(self):
        """Check out for the day"""
        result = self.make_api_request('POST', '/attendance/check-out')
        if result and result.get('success'):
            messagebox.showinfo("Success", "Checked out successfully!")
            self.load_attendance_data()
        else:
            messagebox.showerror("Error", result.get('message', 'Failed to check out'))

    def start_break(self):
        """Start break"""
        result = self.make_api_request('POST', '/attendance/break-start')
        if result and result.get('success'):
            self.is_break_active = True
            self.break_start_time = datetime.now()
            messagebox.showinfo("Success", "Break started!")
            self.load_attendance_data()
        else:
            messagebox.showerror("Error", result.get('message', 'Failed to start break'))

    def end_break(self):
        """End break"""
        result = self.make_api_request('POST', '/attendance/break-end')
        if result and result.get('success'):
            self.is_break_active = False
            self.break_start_time = None
            messagebox.showinfo("Success", "Break ended!")
            self.load_attendance_data()
        else:
            messagebox.showerror("Error", result.get('message', 'Failed to end break'))

    def load_attendance_data(self):
        """Load today's attendance data"""
        if not self.api_token:
            self.status_label.config(text="Please set API token first")
            return

        result = self.make_api_request('GET', '/attendance/today')
        if result and result.get('success'):
            self.current_attendance = result.get('data')
            self.update_ui()
        else:
            self.status_label.config(text="No attendance data for today")
            self.update_button_states(False, False, False, False)

    def update_ui(self):
        """Update the UI based on current attendance data"""
        if not self.current_attendance:
            return

        # Update status
        status = self.current_attendance.get('status', 'Unknown')
        check_in = self.current_attendance.get('check_in', 'Not checked in')
        check_out = self.current_attendance.get('check_out', 'Not checked out')

        self.status_label.config(text=f"Status: {status.title()}")
        self.time_label.config(text=f"Check In: {check_in} | Check Out: {check_out}")

        # Update button states
        has_checkin = bool(check_in and check_in != 'Not checked in')
        has_checkout = bool(check_out and check_out != 'Not checked out')
        has_break_start = bool(self.current_attendance.get('break_start'))
        has_break_end = bool(self.current_attendance.get('break_end'))

        self.update_button_states(not has_checkin, has_checkin and not has_checkout,
                                 has_checkin and not has_break_start,
                                 has_break_start and not has_break_end)

        # Update summary
        self.update_summary()

    def update_button_states(self, checkin_enabled, checkout_enabled,
                           break_start_enabled, break_end_enabled):
        """Update button states"""
        self.checkin_btn.config(state=tk.NORMAL if checkin_enabled else tk.DISABLED)
        self.checkout_btn.config(state=tk.NORMAL if checkout_enabled else tk.DISABLED)
        self.break_start_btn.config(state=tk.NORMAL if break_start_enabled else tk.DISABLED)
        self.break_end_btn.config(state=tk.NORMAL if break_end_enabled else tk.DISABLED)

    def update_summary(self):
        """Update the summary text"""
        if not self.current_attendance:
            return

        summary = f"Date: {self.current_attendance.get('date', 'N/A')}\n"
        summary += f"Check In: {self.current_attendance.get('check_in', 'Not checked in')}\n"
        summary += f"Check Out: {self.current_attendance.get('check_out', 'Not checked out')}\n"
        summary += f"Break Start: {self.current_attendance.get('break_start', 'Not started')}\n"
        summary += f"Break End: {self.current_attendance.get('break_end', 'Not ended')}\n"
        summary += f"Total Break Minutes: {self.current_attendance.get('total_break_minutes', 0)}\n"
        summary += f"Total Work Minutes: {self.current_attendance.get('total_work_minutes', 0)}\n"
        summary += f"Status: {self.current_attendance.get('status', 'Unknown').title()}\n"

        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(1.0, summary)
        self.summary_text.config(state=tk.DISABLED)

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
                            self.root.after(0, lambda: messagebox.showwarning(
                                "Break Reminder",
                                "You've been working for more than 4 hours. Consider taking a break!"
                            ))
            except Exception as e:
                print(f"Reminder error: {e}")

            time.sleep(1800)  # Check every 30 minutes

    def run(self):
        """Run the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        """Handle application closing"""
        self.reminder_running = False
        self.root.destroy()

def main():
    """Main function"""
    app = EmployeeTracker()
    app.run()

if __name__ == "__main__":
    main()

