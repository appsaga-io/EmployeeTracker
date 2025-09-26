<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Attendance;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Carbon\Carbon;

class AttendanceController extends Controller
{
    /**
     * Handle check-in event
     */
    public function checkIn(Request $request): JsonResponse
    {
        $user = $request->user();
        $today = Carbon::today();

        // Check if already checked in today
        $attendance = Attendance::where('user_id', $user->id)
            ->where('date', $today)
            ->first();

        if ($attendance && $attendance->check_in) {
            return response()->json([
                'success' => false,
                'message' => 'Already checked in today'
            ], 400);
        }

        // Create or update attendance record
        if (!$attendance) {
            $attendance = new Attendance([
                'user_id' => $user->id,
                'date' => $today,
                'check_in' => Carbon::now()->format('H:i:s'),
                'status' => 'present'
            ]);
        } else {
            $attendance->check_in = Carbon::now()->format('H:i:s');
            $attendance->status = 'present';
        }

        $attendance->updateStatus();
        $attendance->save();

        return response()->json([
            'success' => true,
            'message' => 'Check-in recorded successfully',
            'data' => $attendance
        ]);
    }

    /**
     * Handle break start event
     */
    public function breakStart(Request $request): JsonResponse
    {
        $user = $request->user();
        $today = Carbon::today();

        $attendance = Attendance::where('user_id', $user->id)
            ->where('date', $today)
            ->first();

        if (!$attendance || !$attendance->check_in) {
            return response()->json([
                'success' => false,
                'message' => 'Must check in before starting break'
            ], 400);
        }

        if ($attendance->break_start) {
            return response()->json([
                'success' => false,
                'message' => 'Break already started'
            ], 400);
        }

        $attendance->break_start = Carbon::now()->format('H:i:s');
        $attendance->save();

        return response()->json([
            'success' => true,
            'message' => 'Break started successfully',
            'data' => $attendance
        ]);
    }

    /**
     * Handle break end event
     */
    public function breakEnd(Request $request): JsonResponse
    {
        $user = $request->user();
        $today = Carbon::today();

        $attendance = Attendance::where('user_id', $user->id)
            ->where('date', $today)
            ->first();

        if (!$attendance || !$attendance->break_start) {
            return response()->json([
                'success' => false,
                'message' => 'Must start break before ending it'
            ], 400);
        }

        if ($attendance->break_end) {
            return response()->json([
                'success' => false,
                'message' => 'Break already ended'
            ], 400);
        }

        $breakEnd = Carbon::now();
        $breakStart = Carbon::parse($attendance->break_start);
        $breakMinutes = $breakEnd->diffInMinutes($breakStart);

        $attendance->break_end = $breakEnd->format('H:i:s');
        $attendance->total_break_minutes += $breakMinutes;
        $attendance->total_work_minutes = $attendance->calculateTotalWorkMinutes();
        $attendance->save();

        return response()->json([
            'success' => true,
            'message' => 'Break ended successfully',
            'data' => $attendance
        ]);
    }

    /**
     * Handle check-out event
     */
    public function checkOut(Request $request): JsonResponse
    {
        $user = $request->user();
        $today = Carbon::today();

        $attendance = Attendance::where('user_id', $user->id)
            ->where('date', $today)
            ->first();

        if (!$attendance || !$attendance->check_in) {
            return response()->json([
                'success' => false,
                'message' => 'Must check in before checking out'
            ], 400);
        }

        if ($attendance->check_out) {
            return response()->json([
                'success' => false,
                'message' => 'Already checked out today'
            ], 400);
        }

        $attendance->check_out = Carbon::now()->format('H:i:s');
        $attendance->total_work_minutes = $attendance->calculateTotalWorkMinutes();
        $attendance->save();

        return response()->json([
            'success' => true,
            'message' => 'Check-out recorded successfully',
            'data' => $attendance
        ]);
    }

    /**
     * Get today's attendance for the authenticated user
     */
    public function today(Request $request): JsonResponse
    {
        $user = $request->user();
        $today = Carbon::today();

        $attendance = Attendance::where('user_id', $user->id)
            ->where('date', $today)
            ->first();

        return response()->json([
            'success' => true,
            'data' => $attendance
        ]);
    }
}
