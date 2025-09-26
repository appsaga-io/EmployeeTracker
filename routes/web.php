<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Auth;
use App\Http\Controllers\Web\AdminController;
use App\Http\Controllers\Web\EmployeeController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/', function () {
    return redirect()->route('login');
});

Auth::routes();

// Employee routes
Route::middleware(['auth'])->group(function () {
    Route::get('/employee/dashboard', [EmployeeController::class, 'dashboard'])->name('employee.dashboard');
    Route::get('/employee/attendance', [EmployeeController::class, 'attendance'])->name('employee.attendance');
    Route::get('/employee/leave-requests', [EmployeeController::class, 'leaveRequests'])->name('employee.leave-requests');
    Route::get('/employee/leave-requests/create', [EmployeeController::class, 'createLeaveRequest'])->name('employee.leave-requests.create');
    Route::post('/employee/leave-requests', [EmployeeController::class, 'storeLeaveRequest'])->name('employee.leave-requests.store');
});

// Admin routes
Route::middleware(['auth', 'admin'])->group(function () {
    Route::get('/admin/dashboard', [AdminController::class, 'dashboard'])->name('admin.dashboard');
    Route::get('/admin/attendance', [AdminController::class, 'attendance'])->name('admin.attendance');
    Route::get('/admin/leave-requests', [AdminController::class, 'leaveRequests'])->name('admin.leave-requests');
    Route::post('/admin/leave-requests/{id}/approve', [AdminController::class, 'approveLeaveRequest'])->name('admin.leave-requests.approve');
    Route::post('/admin/leave-requests/{id}/reject', [AdminController::class, 'rejectLeaveRequest'])->name('admin.leave-requests.reject');
});

Auth::routes();

Route::get('/home', [App\Http\Controllers\HomeController::class, 'index'])->name('home');
