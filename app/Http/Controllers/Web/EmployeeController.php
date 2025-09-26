<?php

namespace App\Http\Controllers\Web;

use App\Http\Controllers\Controller;
use App\Models\Attendance;
use App\Models\LeaveRequest;
use Illuminate\Http\Request;
use Carbon\Carbon;

class EmployeeController extends Controller
{
    public function __construct()
    {
        $this->middleware('auth');
    }

    /**
     * Show employee dashboard
     */
    public function dashboard()
    {
        $user = auth()->user();
        $today = Carbon::today();

        // Get today's attendance
        $todayAttendance = Attendance::where('user_id', $user->id)
            ->where('date', $today)
            ->first();

        // Get recent attendance records
        $recentAttendance = Attendance::where('user_id', $user->id)
            ->orderBy('date', 'desc')
            ->limit(10)
            ->get();

        // Get pending leave requests
        $pendingLeaveRequests = LeaveRequest::where('user_id', $user->id)
            ->where('status', 'pending')
            ->orderBy('created_at', 'desc')
            ->get();

        // Get leave balance
        $leaveBalance = $user->leave_balance;

        return view('employee.dashboard', compact(
            'todayAttendance',
            'recentAttendance',
            'pendingLeaveRequests',
            'leaveBalance'
        ));
    }

    /**
     * Show attendance history
     */
    public function attendance(Request $request)
    {
        $user = auth()->user();
        $query = Attendance::where('user_id', $user->id);

        // Filter by date range
        if ($request->filled('start_date')) {
            $query->where('date', '>=', $request->start_date);
        }
        if ($request->filled('end_date')) {
            $query->where('date', '<=', $request->end_date);
        }

        $attendances = $query->orderBy('date', 'desc')
            ->paginate(20);

        return view('employee.attendance', compact('attendances'));
    }

    /**
     * Show leave requests
     */
    public function leaveRequests()
    {
        $user = auth()->user();
        $leaveRequests = LeaveRequest::where('user_id', $user->id)
            ->orderBy('created_at', 'desc')
            ->paginate(20);

        return view('employee.leave-requests', compact('leaveRequests'));
    }

    /**
     * Show create leave request form
     */
    public function createLeaveRequest()
    {
        return view('employee.create-leave-request');
    }

    /**
     * Store leave request
     */
    public function storeLeaveRequest(Request $request)
    {
        $request->validate([
            'leave_type' => 'required|in:sick,vacation,personal,emergency,other',
            'start_date' => 'required|date|after_or_equal:today',
            'end_date' => 'required|date|after_or_equal:start_date',
            'reason' => 'required|string|max:500'
        ]);

        $user = auth()->user();
        $startDate = Carbon::parse($request->start_date);
        $endDate = Carbon::parse($request->end_date);
        $totalDays = $startDate->diffInDays($endDate) + 1;

        // Check if user has enough leave balance
        if ($totalDays > $user->leave_balance) {
            return redirect()->back()
                ->withErrors(['leave_balance' => 'Insufficient leave balance'])
                ->withInput();
        }

        // Check for overlapping leave requests
        $overlapping = LeaveRequest::where('user_id', $user->id)
            ->where('status', '!=', 'rejected')
            ->where(function ($query) use ($startDate, $endDate) {
                $query->whereBetween('start_date', [$startDate, $endDate])
                    ->orWhereBetween('end_date', [$startDate, $endDate])
                    ->orWhere(function ($q) use ($startDate, $endDate) {
                        $q->where('start_date', '<=', $startDate)
                          ->where('end_date', '>=', $endDate);
                    });
            })
            ->exists();

        if ($overlapping) {
            return redirect()->back()
                ->withErrors(['overlapping' => 'You already have a leave request for this period'])
                ->withInput();
        }

        LeaveRequest::create([
            'user_id' => $user->id,
            'leave_type' => $request->leave_type,
            'start_date' => $startDate,
            'end_date' => $endDate,
            'total_days' => $totalDays,
            'reason' => $request->reason,
        ]);

        return redirect()->route('employee.leave-requests')
            ->with('success', 'Leave request submitted successfully');
    }
}
