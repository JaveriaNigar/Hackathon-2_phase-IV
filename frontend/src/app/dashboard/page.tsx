// frontend/src/app/dashboard/page.tsx
'use client';

import React, { useEffect, useState } from 'react';
import { getTasks, getPendingTasksCount, getCompletedTasksCount, updateTask, createTask } from '@/services/tasks';
import { isAuthenticated } from '@/lib/auth';
import { redirect } from 'next/navigation';
import TaskList from '@/components/dashboard/TaskList';
import { getCurrentUser } from '@/services/auth';
import Link from 'next/link';

interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
  updated_at: string;
}

// Define the task interface to match the TaskList component expectations
interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  userId: string;
  dueDate?: string;
  priority: string;
  createdAt: string;
  updatedAt: string;
  completedAt?: string | null;
}

// Define the backend task interface
interface BackendTask {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  due_date?: string;
  priority: string;
  created_at: string;
  updated_at: string;
}

// Convert backend task to frontend format
const convertBackendTaskToFrontend = (backendTask: BackendTask): Task => ({
  id: backendTask.id.toString(), // Convert to string for consistency
  title: backendTask.title,
  description: backendTask.description,
  completed: backendTask.completed,
  userId: backendTask.user_id,
  dueDate: backendTask.due_date,
  priority: backendTask.priority,
  createdAt: backendTask.created_at,
  updatedAt: backendTask.updated_at,
  completedAt: null
});

const DashboardPage = () => {
  const [user, setUser] = useState<User | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [pendingTaskCount, setPendingTaskCount] = useState<number>(0);
  const [completedTaskCount, setCompletedTaskCount] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState<'all' | 'pending' | 'done'>('all');

  useEffect(() => {
    // Check if user is authenticated
    if (!isAuthenticated()) {
      // Redirect to login if not authenticated
      window.location.href = '/login';
      return;
    }

    // Fetch user profile and tasks
    const fetchData = async () => {
      try {
        // Get the current user's profile from the backend
        const userData = await getCurrentUser();
        setUser(userData);

        // Fetch tasks for the user
        const backendTasks: BackendTask[] = await getTasks();
        // Convert backend tasks to frontend format
        const frontendTasks = backendTasks.map(convertBackendTaskToFrontend);
        setTasks(frontendTasks);

        // Fetch pending tasks count
        const pendingCount = await getPendingTasksCount();
        setPendingTaskCount(pendingCount.pending);

        // Fetch completed tasks count
        const completedCount = await getCompletedTasksCount();
        setCompletedTaskCount(completedCount.completed);
      } catch (err: any) {
        // More specific error handling for different types of errors
        if (err.message.includes('fetch')) {
          setError('Unable to connect to the server. Please check your connection and try again.');
        } else if (err.message.includes('401') || err.message.includes('403')) {
          setError('Authentication failed. Please log in again.');
          // Redirect to login after a delay
          setTimeout(() => {
            window.location.href = '/login';
          }, 2000);
        } else {
          setError(err.message || 'Error fetching user data or tasks');
        }
        console.error('Error fetching user data or tasks:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Listen for global task changes (from the Agent)
    const handleTasksChanged = () => {
      fetchData();
    };

    window.addEventListener('tasksChanged', handleTasksChanged);

    return () => {
      window.removeEventListener('tasksChanged', handleTasksChanged);
    };
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-ai-blue mx-auto"></div>
          <p className="mt-4 text-foreground">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  const handleAddTaskClick = () => {
    // Navigate to the add-task page
    window.location.href = '/add-task';
  };


  // Calculate urgent tasks - count tasks with high priority that are not completed
  const urgentTasksCount = tasks.filter(task => {
    return task.priority === 'high' && !task.completed;
  }).length;

  // Calculate progress based on filter
  let progressPercentage = 0;
  if (filter === 'all') {
    const total = pendingTaskCount + completedTaskCount;
    progressPercentage = total > 0 ? Math.round((completedTaskCount / total) * 100) : 0;
  } else if (filter === 'done') {
    const total = tasks.length;
    progressPercentage = total > 0 ? Math.round((completedTaskCount / total) * 100) : 0;
  } else if (filter === 'pending') {
    const total = tasks.length;
    progressPercentage = total > 0 ? Math.round((pendingTaskCount / total) * 100) : 0;
  }

  return (
    <div className="container mx-auto px-4 py-8 min-h-screen bg-background">
      {/* Stats Section */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8 fade-in" style={{ animationDelay: '0.1s' }}>
        <div className="bg-card-bg border border-border rounded-xl p-5 cursor-glow transition-shadow duration-300 card-ai-style flex flex-col items-center justify-center h-32">
          <h3 className="text-lg font-semibold text-ai-blue mb-1">Total Tasks</h3>
          <p className="text-2xl font-bold text-foreground">{tasks.length}</p>
        </div>

        <div className="bg-card-bg border border-border rounded-xl p-5 cursor-glow transition-shadow duration-300 card-ai-style flex flex-col items-center justify-center h-32">
          <h3 className="text-lg font-semibold text-ai-cyan mb-1">Pending Tasks</h3>
          <p className="text-2xl font-bold text-foreground">{pendingTaskCount}</p>
        </div>

        <div className="bg-card-bg border border-border rounded-xl p-5 cursor-glow transition-shadow duration-300 card-ai-style flex flex-col items-center justify-center h-32">
          <h3 className="text-lg font-semibold text-ai-green mb-1">Completed Tasks</h3>
          <p className="text-2xl font-bold text-foreground">{completedTaskCount}</p>
        </div>

        <div className="bg-card-bg border border-border rounded-xl p-5 cursor-glow transition-shadow duration-300 card-ai-style flex flex-col items-center justify-center h-32">
          <h3 className="text-lg font-semibold text-ai-purple mb-1">Urgent Tasks</h3>
          <p className="text-2xl font-bold text-foreground">{urgentTasksCount}</p>
        </div>
      </div>

      {/* Progress Line with Filters */}
      <div className="flex flex-col md:flex-row items-center justify-between mb-8 gap-4">
        <div className="w-full md:w-2/3">
          <div className="w-full bg-card-bg rounded-full h-6 border border-border overflow-hidden">
            <div
              className="bg-gradient-to-r from-ai-blue to-ai-purple h-full rounded-full transition-all duration-500 ease-out"
              style={{ width: progressPercentage + '%' }}
            ></div>
          </div>
        </div>

        <div className="flex gap-2 w-full md:w-1/3 justify-end">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg transition-colors ${filter === 'all'
              ? 'bg-ai-blue text-white'
              : 'bg-card-bg text-foreground border border-border hover:bg-[#2a2a2a]'
              }`}
          >
            All
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`px-4 py-2 rounded-lg transition-colors ${filter === 'pending'
              ? 'bg-ai-cyan text-white'
              : 'bg-card-bg text-foreground border border-border hover:bg-[#2a2a2a]'
              }`}
          >
            Pending
          </button>
          <button
            onClick={() => setFilter('done')}
            className={`px-4 py-2 rounded-lg transition-colors ${filter === 'done'
              ? 'bg-ai-green text-white'
              : 'bg-card-bg text-foreground border border-border hover:bg-[#2a2a2a]'
              }`}
          >
            Done
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-card-bg text-ai-blue rounded-lg border border-border fade-in">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 fade-in" style={{ animationDelay: '0.2s' }}>
        <div className="lg:col-span-3">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-semibold text-foreground">Your Tasks</h2>
            <Link href="/add-task">
              <button
                className="btn-ai-gradient px-8 py-4 text-lg rounded-lg ripple-effect"
              >
                Add Task
              </button>
            </Link>
          </div>

          <TaskList
            tasks={tasks}
            onTaskAdded={(newTask) => {
              setTasks(prevTasks => [newTask, ...prevTasks]);
              // Update pending or completed count based on the new task's status
              if (newTask.completed) {
                setCompletedTaskCount(prevCount => prevCount + 1);
              } else {
                setPendingTaskCount(prevCount => prevCount + 1);
              }
            }}
            onTaskUpdated={(updatedTask) => {
              setTasks(prevTasks =>
                prevTasks.map(task => task.id === updatedTask.id ? updatedTask : task)
              );

              // Update pending and completed counts based on completion status change
              const oldTask = tasks.find(t => t.id === updatedTask.id);
              if (oldTask && oldTask.completed !== updatedTask.completed) {
                if (oldTask.completed && !updatedTask.completed) {
                  // Task changed from completed to not completed (pending)
                  setCompletedTaskCount(prevCount => prevCount - 1);
                  setPendingTaskCount(prevCount => prevCount + 1);
                } else if (!oldTask.completed && updatedTask.completed) {
                  // Task changed from not completed (pending) to completed
                  setPendingTaskCount(prevCount => prevCount - 1);
                  setCompletedTaskCount(prevCount => prevCount + 1);
                }
              }
            }}
            onTaskDeleted={(deletedTaskId) => {
              const deletedTask = tasks.find(t => t.id === deletedTaskId);
              setTasks(prevTasks =>
                prevTasks.filter(task => task.id !== deletedTaskId)
              );

              // Update pending or completed count based on the deleted task's status
              if (deletedTask) {
                if (deletedTask.completed) {
                  setCompletedTaskCount(prevCount => Math.max(0, prevCount - 1));
                } else {
                  setPendingTaskCount(prevCount => Math.max(0, prevCount - 1));
                }
              }
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;