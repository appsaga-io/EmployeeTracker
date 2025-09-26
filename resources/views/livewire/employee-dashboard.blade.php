<div>
    <div class="container-fluid">
        <h1 class="h3 mb-4">Employee Dashboard</h1>

        <!-- Today's Status -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>Today's Status</h5>
                    </div>
                    <div class="card-body">
                        @if($todayAttendance)
                            <p><strong>Check In:</strong> {{ $todayAttendance->check_in ?? 'Not checked in' }}</p>
                            <p><strong>Check Out:</strong> {{ $todayAttendance->check_out ?? 'Not checked out' }}</p>
                            <p><strong>Status:</strong>
                                <span class="badge badge-{{ $todayAttendance->status === 'present' ? 'success' : ($todayAttendance->status === 'late' ? 'warning' : 'danger') }}">
                                    {{ ucfirst($todayAttendance->status) }}
                                </span>
                            </p>
                            @if($todayAttendance->total_work_minutes)
                                <p><strong>Work Hours:</strong> {{ round($todayAttendance->total_work_minutes / 60, 2) }} hours</p>
                            @endif
                        @else
                            <p class="text-muted">No attendance record for today.</p>
                        @endif
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>Leave Balance</h5>
                    </div>
                    <div class="card-body">
                        <h3>{{ $leaveBalance }} days</h3>
                        <a href="{{ route('employee.leave-requests.create') }}" class="btn btn-primary">Request Leave</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Pending Leave Requests -->
        @if(count($pendingLeaveRequests) > 0)
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Pending Leave Requests</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>Leave Type</th>
                                    <th>Start Date</th>
                                    <th>End Date</th>
                                    <th>Total Days</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                @foreach($pendingLeaveRequests as $request)
                                    <tr>
                                        <td>{{ ucfirst($request['leave_type']) }}</td>
                                        <td>{{ \Carbon\Carbon::parse($request['start_date'])->format('M d, Y') }}</td>
                                        <td>{{ \Carbon\Carbon::parse($request['end_date'])->format('M d, Y') }}</td>
                                        <td>{{ $request['total_days'] }}</td>
                                        <td>
                                            <span class="badge badge-warning">{{ ucfirst($request['status']) }}</span>
                                        </td>
                                    </tr>
                                @endforeach
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        @endif

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
