<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class UserSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // Create admin user
        User::create([
            'name' => 'Admin User',
            'email' => 'admin@example.com',
            'password' => Hash::make('password'),
            'employee_id' => 'EMP001',
            'department' => 'IT',
            'position' => 'System Administrator',
            'hire_date' => now()->subYear(),
            'leave_balance' => 20.00,
            'is_admin' => true,
        ]);

        // Create sample employees
        User::create([
            'name' => 'John Doe',
            'email' => 'john@example.com',
            'password' => Hash::make('password'),
            'employee_id' => 'EMP002',
            'department' => 'Engineering',
            'position' => 'Software Developer',
            'hire_date' => now()->subMonths(6),
            'leave_balance' => 15.00,
            'is_admin' => false,
        ]);

        User::create([
            'name' => 'Jane Smith',
            'email' => 'jane@example.com',
            'password' => Hash::make('password'),
            'employee_id' => 'EMP003',
            'department' => 'Marketing',
            'position' => 'Marketing Manager',
            'hire_date' => now()->subMonths(3),
            'leave_balance' => 18.00,
            'is_admin' => false,
        ]);
    }
}
