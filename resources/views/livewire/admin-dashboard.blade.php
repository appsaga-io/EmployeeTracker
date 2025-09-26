<div>
    <div class="container-fluid">
        <h1 class="h3 mb-4">Admin Dashboard</h1>

        <!-- Today's Summary -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card text-white bg-success">
                    <div class="card-body">
                        <h5 class="card-title">Present</h5>
                        <h2>{{ $presentCount }}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-warning">
                    <div class="card-body">
                        <h5 class="card-title">Late</h5>
                        <h2>{{ $lateCount }}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-danger">
                    <div class="card-body">
                        <h5 class="card-title">Absent</h5>
                        <h2>{{ $absentCount }}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-info">
                    <div class="card-body">
                        <h5 class="card-title">Pending Leave Requests</h5>
                        <h2>{{ count($pendingLeaveRequests) }}</h2>
                    </div>
                </div>
            </div>
        </div>

        <!-- Pending Leave Requests -->
        <div class="card mb-4">
            <div class="card-header">
                <h5>Pending Leave Requests</h5>
            </div>
            <div class="card-body">
                @if(count($pendingLeaveRequests) > 0)
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Employee</th>
                                    <th>Leave Type</th>
                                    <th>Start Date</th>
                                    <th>End Date</th>
                                    <th>Total Days</th>
                                    <th>Reason</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                @foreach($pendingLeaveRequests as $request)
                                    <tr>
                                        <td>{{ $request['user']['name'] }}</td>
                                        <td>{{ ucfirst($request['leave_type']) }}</td>
                                        <td>{{ \Carbon\Carbon::parse($request['start_date'])->format('M d, Y') }}</td>
                                        <td>{{ \Carbon\Carbon::parse($request['end_date'])->format('M d, Y') }}</td>
                                        <td>{{ $request['total_days'] }}</td>
                                        <td>{{ Str::limit($request['reason'], 50) }}</td>
                                        <td>
                                            <a href="{{ route('admin.leave-requests') }}" class="btn btn-sm btn-primary">Review</a>
                                        </td>
                                    </tr>
                                @endforeach
                            </tbody>
                        </table>
                    </div>
                @else
                    <p class="text-muted">No pending leave requests.</p>
                @endif
            </div>
        </div>

        <!-- Recent Attendance -->
        <div class="card">
            <div class="card-header">
                <h5>Recent Attendance</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Employee</th>
                                <th>Date</th>
                                <th>Check In</th>
                                <th>Check Out</th>
                                <th>Status</th>
                                <th>Work Hours</th>
                            </tr>
                        </thead>
                        <tbody>
                            @foreach($recentAttendance as $attendance)
                                <tr>
                                    <td>{{ $attendance['user']['name'] }}</td>
                                    <td>{{ \Carbon\Carbon::parse($attendance['date'])->format('M d, Y') }}</td>
                                    <td>{{ $attendance['check_in'] ?? '-' }}</td>
                                    <td>{{ $attendance['check_out'] ?? '-' }}</td>
                                    <td>
                                        <span class="badge badge-{{ $attendance['status'] === 'present' ? 'success' : ($attendance['status'] === 'late' ? 'warning' : 'danger') }}">
                                            {{ ucfirst($attendance['status']) }}
                                        </span>
                                    </td>
                                    <td>{{ $attendance['total_work_minutes'] ? round($attendance['total_work_minutes'] / 60, 2) . ' hrs' : '-' }}</td>
                                </tr>
                            @endforeach
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
