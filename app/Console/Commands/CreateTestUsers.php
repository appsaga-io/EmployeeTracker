<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class CreateTestUsers extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'user:create-test';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Create test users for the application';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        // Create admin user if not exists
        if (!User::where('email', 'admin@example.com')->exists()) {
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
            $this->info('Admin user created!');
        }

        // Create employee users if not exist
        if (!User::where('email', 'john@example.com')->exists()) {
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
            $this->info('John Doe user created!');
        }

        if (!User::where('email', 'jane@example.com')->exists()) {
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
            $this->info('Jane Smith user created!');
        }

        // Display all users
        $this->info('All users in database:');
        $users = User::all(['name', 'email', 'is_admin', 'employee_id']);
        foreach ($users as $user) {
            $this->info("- {$user->name} ({$user->email}) - Admin: " . ($user->is_admin ? 'Yes' : 'No') . " - ID: {$user->employee_id}");
        }
    }
}