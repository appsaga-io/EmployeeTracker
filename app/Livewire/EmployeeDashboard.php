<?php

namespace App\Livewire;

use Livewire\Component;
use App\Models\Attendance;
use App\Models\LeaveRequest;
use Carbon\Carbon;

class EmployeeDashboard extends Component
{
    public $todayAttendance = null;
    public $recentAttendance = [];
    public $pendingLeaveRequests = [];
    public $leaveBalance = 0;

    public function mount()
    {
        $this->loadDashboardData();
    }

    public function loadDashboardData()
    {
        $user = auth()->user();
        $today = Carbon::today();

        // Get today's attendance
        $this->todayAttendance = Attendance::where('user_id', $user->id)
            ->where('date', $today)
            ->first();

        // Get recent attendance records
        $this->recentAttendance = Attendance::where('user_id', $user->id)
            ->orderBy('date', 'desc')
            ->limit(10)
            ->get()
            ->toArray();

        // Get pending leave requests
        $this->pendingLeaveRequests = LeaveRequest::where('user_id', $user->id)
            ->where('status', 'pending')
            ->orderBy('created_at', 'desc')
            ->get()
            ->toArray();

        // Get leave balance
        $this->leaveBalance = $user->leave_balance;
    }

    public function render()
    {
        return view('livewire.employee-dashboard');
    }
}
