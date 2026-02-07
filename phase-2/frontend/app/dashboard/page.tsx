'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../components/AuthProvider';
import TaskForm from '../../components/TaskForm';
import TaskList from '../../components/TaskList';
import { useRouter } from 'next/navigation';

const DashboardPage: React.FC = () => {
  const { authState, logout } = useAuth();
  const router = useRouter();
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  useEffect(() => {
    if (!authState.isAuthenticated) {
      router.push('/auth/signin');
    }
  }, [authState.isAuthenticated, router]);

  const handleLogout = () => {
    logout();
    router.push('/auth/signin');
  };

  const handleTaskAdded = () => {
    // Trigger a refresh of the task list
    setRefreshTrigger(prev => prev + 1);
  };

  if (!authState.isAuthenticated) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <h1 className="text-xl font-bold text-gray-900">Todo App</h1>
              </div>
            </div>
            <div className="flex items-center">
              <div className="ml-3 relative">
                <div className="text-sm text-gray-700 mr-4">
                  Welcome, {authState.user?.email}
                </div>
                <button
                  onClick={handleLogout}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <h1 className="text-2xl font-semibold text-gray-900 mb-6">My Tasks</h1>

          <div className="mb-8">
            <TaskForm userId={authState.user?.id || ''} onTaskAdded={handleTaskAdded} />
          </div>

          <div>
            <TaskList userId={authState.user?.id || ''} key={refreshTrigger} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;