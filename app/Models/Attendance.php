<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Carbon\Carbon;

class Attendance extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'user_id',
        'date',
        'check_in',
        'check_out',
        'break_start',
        'break_end',
        'total_break_minutes',
        'total_work_minutes',
        'status',
        'notes',
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'date' => 'date',
        'check_in' => 'datetime:H:i:s',
        'check_out' => 'datetime:H:i:s',
        'break_start' => 'datetime:H:i:s',
        'break_end' => 'datetime:H:i:s',
    ];

    /**
     * Get the user that owns the attendance.
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    /**
     * Calculate total work minutes for the day
     */
    public function calculateTotalWorkMinutes()
    {
        if (!$this->check_in || !$this->check_out) {
            return 0;
        }

        $checkIn = Carbon::parse($this->date . ' ' . $this->check_in);
        $checkOut = Carbon::parse($this->date . ' ' . $this->check_out);
        $totalMinutes = $checkOut->diffInMinutes($checkIn);

        return $totalMinutes - $this->total_break_minutes;
    }

    /**
     * Update the status based on check-in time
     */
    public function updateStatus()
    {
        if (!$this->check_in) {
            $this->status = 'absent';
            return;
        }

        $checkInTime = Carbon::parse($this->check_in);
        $expectedCheckIn = Carbon::parse('09:00:00'); // Assuming 9 AM is the expected check-in time

        if ($checkInTime->gt($expectedCheckIn)) {
            $this->status = 'late';
        } else {
            $this->status = 'present';
        }
    }
}
