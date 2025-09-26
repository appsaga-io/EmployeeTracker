<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class CreateAdminUser extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'user:create-admin';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Create an admin user';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        // Check if admin already exists
        if (User::where('email', 'admin@example.com')->exists()) {
            $this->info('Admin user already exists!');
            return;
        }

        // Create admin user
        $admin = User::create([
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

        $this->info('Admin user created successfully!');
        $this->info('Email: admin@example.com');
        $this->info('Password: password');
    }
}