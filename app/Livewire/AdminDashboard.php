<?php

namespace App\Livewire;

use Livewire\Component;
use App\Models\Attendance;
use App\Models\LeaveRequest;
use App\Models\User;
use Carbon\Carbon;

class AdminDashboard extends Component
{
    public $presentCount = 0;
    public $lateCount = 0;
    public $absentCount = 0;
    public $pendingLeaveRequests = [];
    public $recentAttendance = [];

    public function mount()
    {
        $this->loadDashboardData();
    }

    public function loadDashboardData()
    {
        $today = Carbon::today();

        // Get today's attendance summary
        $todayAttendance = Attendance::where('date', $today)
            ->with('user')
            ->get();

        $this->presentCount = $todayAttendance->where('status', 'present')->count();
        $this->lateCount = $todayAttendance->where('status', 'late')->count();
        $this->absentCount = User::count() - $todayAttendance->count();

        // Get pending leave requests
        $this->pendingLeaveRequests = LeaveRequest::where('status', 'pending')
            ->with('user')
            ->orderBy('created_at', 'desc')
            ->limit(5)
            ->get()
            ->toArray();

        // Get recent attendance records
        $this->recentAttendance = Attendance::with('user')
            ->orderBy('date', 'desc')
            ->orderBy('created_at', 'desc')
            ->limit(10)
            ->get()
            ->toArray();
    }

    public function render()
    {
        return view('livewire.admin-dashboard');
    }
}
