<?php

namespace App\Http\Controllers\Web;

use App\Http\Controllers\Controller;
use App\Models\Attendance;
use App\Models\LeaveRequest;
use App\Models\User;
use Illuminate\Http\Request;
use Carbon\Carbon;

class AdminController extends Controller
{
    public function __construct()
    {
        $this->middleware('auth');
        $this->middleware('admin');
    }

    /**
     * Show admin dashboard
     */
    public function dashboard()
    {
        $today = Carbon::today();

        // Get today's attendance summary
        $todayAttendance = Attendance::where('date', $today)
            ->with('user')
            ->get();

        $presentCount = $todayAttendance->where('status', 'present')->count();
        $lateCount = $todayAttendance->where('status', 'late')->count();
        $absentCount = User::count() - $todayAttendance->count();

        // Get pending leave requests
        $pendingLeaveRequests = LeaveRequest::where('status', 'pending')
            ->with('user')
            ->orderBy('created_at', 'desc')
            ->get();

        // Get recent attendance records
        $recentAttendance = Attendance::with('user')
            ->orderBy('date', 'desc')
            ->orderBy('created_at', 'desc')
            ->limit(10)
            ->get();

        return view('admin.dashboard', compact(
            'todayAttendance',
            'presentCount',
            'lateCount',
            'absentCount',
            'pendingLeaveRequests',
            'recentAttendance'
        ));
    }

    /**
     * Show all attendance records
     */
    public function attendance(Request $request)
    {
        $query = Attendance::with('user');

        // Filter by date range
        if ($request->filled('start_date')) {
            $query->where('date', '>=', $request->start_date);
        }
        if ($request->filled('end_date')) {
            $query->where('date', '<=', $request->end_date);
        }

        // Filter by user
        if ($request->filled('user_id')) {
            $query->where('user_id', $request->user_id);
        }

        $attendances = $query->orderBy('date', 'desc')
            ->orderBy('created_at', 'desc')
            ->paginate(20);

        $users = User::orderBy('name')->get();

        return view('admin.attendance', compact('attendances', 'users'));
    }

    /**
     * Show all leave requests
     */
    public function leaveRequests(Request $request)
    {
        $query = LeaveRequest::with(['user', 'approver']);

        // Filter by status
        if ($request->filled('status')) {
            $query->where('status', $request->status);
        }

        // Filter by user
        if ($request->filled('user_id')) {
            $query->where('user_id', $request->user_id);
        }

        $leaveRequests = $query->orderBy('created_at', 'desc')
            ->paginate(20);

        $users = User::orderBy('name')->get();

        return view('admin.leave-requests', compact('leaveRequests', 'users'));
    }

    /**
     * Approve a leave request
     */
    public function approveLeaveRequest(Request $request, $id)
    {
        $leaveRequest = LeaveRequest::findOrFail($id);

        $leaveRequest->update([
            'status' => 'approved',
            'approved_by' => auth()->id(),
            'approved_at' => now(),
            'admin_notes' => $request->admin_notes
        ]);

        // Deduct leave balance
        $user = $leaveRequest->user;
        $user->decrement('leave_balance', $leaveRequest->total_days);

        return redirect()->back()->with('success', 'Leave request approved successfully');
    }

    /**
     * Reject a leave request
     */
    public function rejectLeaveRequest(Request $request, $id)
    {
        $leaveRequest = LeaveRequest::findOrFail($id);

        $leaveRequest->update([
            'status' => 'rejected',
            'approved_by' => auth()->id(),
            'approved_at' => now(),
            'admin_notes' => $request->admin_notes
        ]);

        return redirect()->back()->with('success', 'Leave request rejected successfully');
    }
}
