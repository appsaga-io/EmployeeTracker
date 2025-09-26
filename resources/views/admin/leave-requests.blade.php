@extends('layouts.app')

@section('content')
<div class="container">
    <div class="row">
        <div class="col-md-12">
            <h1>Leave Requests</h1>

            <!-- Filters -->
            <div class="card mb-4">
                <div class="card-body">
                    <form method="GET" action="{{ route('admin.leave-requests') }}">
                        <div class="row">
                            <div class="col-md-3">
                                <label for="status" class="form-label">Status</label>
                                <select class="form-control" id="status" name="status">
                                    <option value="">All Status</option>
                                    <option value="pending" {{ request('status') == 'pending' ? 'selected' : '' }}>Pending</option>
                                    <option value="approved" {{ request('status') == 'approved' ? 'selected' : '' }}>Approved</option>
                                    <option value="rejected" {{ request('status') == 'rejected' ? 'selected' : '' }}>Rejected</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <label for="user_id" class="form-label">Employee</label>
                                <select class="form-control" id="user_id" name="user_id">
                                    <option value="">All Employees</option>
                                    @foreach($users as $user)
                                        <option value="{{ $user->id }}" {{ request('user_id') == $user->id ? 'selected' : '' }}>
                                            {{ $user->name }}
                                        </option>
                                    @endforeach
                                </select>
                            </div>
                            <div class="col-md-3">
                                <label class="form-label">&nbsp;</label>
                                <div>
                                    <button type="submit" class="btn btn-primary">Filter</button>
                                    <a href="{{ route('admin.leave-requests') }}" class="btn btn-secondary">Clear</a>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Leave Requests Table -->
            <div class="card">
                <div class="card-body">
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
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                @foreach($leaveRequests as $request)
                                    <tr>
                                        <td>{{ $request->user->name }}</td>
                                        <td>{{ ucfirst($request->leave_type) }}</td>
                                        <td>{{ $request->start_date->format('M d, Y') }}</td>
                                        <td>{{ $request->end_date->format('M d, Y') }}</td>
                                        <td>{{ $request->total_days }}</td>
                                        <td>{{ Str::limit($request->reason, 50) }}</td>
                                        <td>
                                            <span class="badge badge-{{ $request->status === 'approved' ? 'success' : ($request->status === 'rejected' ? 'danger' : 'warning') }}">
                                                {{ ucfirst($request->status) }}
                                            </span>
                                        </td>
                                        <td>
                                            @if($request->status === 'pending')
                                                <form method="POST" action="{{ route('admin.leave-requests.approve', $request->id) }}" class="d-inline">
                                                    @csrf
                                                    <div class="input-group">
                                                        <input type="text" name="admin_notes" class="form-control form-control-sm" placeholder="Notes (optional)">
                                                        <button type="submit" class="btn btn-success btn-sm">Approve</button>
                                                    </div>
                                                </form>
                                                <form method="POST" action="{{ route('admin.leave-requests.reject', $request->id) }}" class="d-inline mt-1">
                                                    @csrf
                                                    <div class="input-group">
                                                        <input type="text" name="admin_notes" class="form-control form-control-sm" placeholder="Notes (optional)">
                                                        <button type="submit" class="btn btn-danger btn-sm">Reject</button>
                                                    </div>
                                                </form>
                                            @else
                                                <small class="text-muted">
                                                    {{ $request->approved_at ? 'Processed on ' . $request->approved_at->format('M d, Y') : '' }}
                                                </small>
                                            @endif
                                        </td>
                                    </tr>
                                @endforeach
                            </tbody>
                        </table>
                    </div>

                    {{ $leaveRequests->links() }}
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
