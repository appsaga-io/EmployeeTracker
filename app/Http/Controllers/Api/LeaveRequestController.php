<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\LeaveRequest;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Carbon\Carbon;

class LeaveRequestController extends Controller
{
    /**
     * Get all leave requests for the authenticated user
     */
    public function index(Request $request): JsonResponse
    {
        $user = $request->user();
        $leaveRequests = LeaveRequest::where('user_id', $user->id)
            ->orderBy('created_at', 'desc')
            ->get();

        return response()->json([
            'success' => true,
            'data' => $leaveRequests
        ]);
    }

    /**
     * Create a new leave request
     */
    public function store(Request $request): JsonResponse
    {
        $request->validate([
            'leave_type' => 'required|in:sick,vacation,personal,emergency,other',
            'start_date' => 'required|date|after_or_equal:today',
            'end_date' => 'required|date|after_or_equal:start_date',
            'reason' => 'required|string|max:500'
        ]);

        $user = $request->user();
        $startDate = Carbon::parse($request->start_date);
        $endDate = Carbon::parse($request->end_date);
        $totalDays = $startDate->diffInDays($endDate) + 1;

        // Check if user has enough leave balance
        if ($totalDays > $user->leave_balance) {
            return response()->json([
                'success' => false,
                'message' => 'Insufficient leave balance'
            ], 400);
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
            return response()->json([
                'success' => false,
                'message' => 'You already have a leave request for this period'
            ], 400);
        }

        $leaveRequest = LeaveRequest::create([
            'user_id' => $user->id,
            'leave_type' => $request->leave_type,
            'start_date' => $startDate,
            'end_date' => $endDate,
            'total_days' => $totalDays,
            'reason' => $request->reason,
        ]);

        return response()->json([
            'success' => true,
            'message' => 'Leave request submitted successfully',
            'data' => $leaveRequest
        ], 201);
    }

    /**
     * Get a specific leave request
     */
    public function show(Request $request, $id): JsonResponse
    {
        $user = $request->user();
        $leaveRequest = LeaveRequest::where('user_id', $user->id)
            ->findOrFail($id);

        return response()->json([
            'success' => true,
            'data' => $leaveRequest
        ]);
    }

    /**
     * Cancel a pending leave request
     */
    public function cancel(Request $request, $id): JsonResponse
    {
        $user = $request->user();
        $leaveRequest = LeaveRequest::where('user_id', $user->id)
            ->findOrFail($id);

        if ($leaveRequest->status !== 'pending') {
            return response()->json([
                'success' => false,
                'message' => 'Only pending leave requests can be cancelled'
            ], 400);
        }

        $leaveRequest->delete();

        return response()->json([
            'success' => true,
            'message' => 'Leave request cancelled successfully'
        ]);
    }
}
