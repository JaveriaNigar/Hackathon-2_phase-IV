'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { createTask, getTaskById, updateTask } from '@/services/tasks';
import { isAuthenticated } from '@/lib/auth';
import { getCurrentUser } from '@/services/auth';

interface TaskFormData {
  id?: string;
  title: string;
  description?: string;
  dueDate?: string;
  priority: string;
}

// Force dynamic rendering to prevent SSR issues
export const dynamic = 'force-dynamic';

// Separate the component logic to handle Suspense boundary
const AddTaskContent = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const taskId = searchParams.get('id'); // If taskId exists, we're in edit mode

  const [formData, setFormData] = useState<TaskFormData>({
    title: '',
    description: '',
    dueDate: '',
    priority: 'medium'
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [initialLoad, setInitialLoad] = useState(true);

  // Load task data if in edit mode
  useEffect(() => {
    const loadTaskData = async () => {
      if (!taskId) {
        // If no taskId, we're in create mode, so just set initialLoad to false
        setInitialLoad(false);
        return;
      }

      try {
        // Check authentication
        if (!isAuthenticated()) {
          router.push('/login');
          return;
        }

        // Get current user
        const user = await getCurrentUser();

        // Fetch task details
        const task = await getTaskById(taskId);

        // Map old priority values to new ones
        let mappedPriority = task.priority;
        if (task.priority === 'normal') {
          mappedPriority = 'low';
        } else if (task.priority === 'urgent') {
          mappedPriority = 'high';
        }

        setFormData({
          id: taskId,
          title: task.title,
          description: task.description || '',
          dueDate: task.due_date || '',
          priority: mappedPriority || 'medium'
        });
      } catch (err: any) {
        console.error('Error fetching task:', err);
        setError(err.message || 'Failed to load task data. Redirecting to dashboard...');
        setTimeout(() => {
          router.push('/dashboard');
        }, 3000);
      } finally {
        setInitialLoad(false);
      }
    };

    loadTaskData();
  }, [taskId, router]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Check authentication
      if (!isAuthenticated()) {
        router.push('/login');
        return;
      }

      // Get current user
      const user = await getCurrentUser();

      if (taskId) {
        // Update existing task
        await updateTask(taskId, {
          title: formData.title,
          description: formData.description || undefined,
          due_date: formData.dueDate || undefined,
          priority: formData.priority
        });
      } else {
        // Create new task
        await createTask({
          title: formData.title,
          description: formData.description || undefined,
          due_date: formData.dueDate || undefined,
          priority: formData.priority
        });
      }

      // Redirect back to dashboard
      router.refresh();
      router.push('/dashboard');
    } catch (err: any) {
      console.error(taskId ? 'Error updating task:' : 'Error creating task:', err);
      setError(err.message || (taskId ? 'Failed to update task. Please try again.' : 'Failed to create task. Please try again.'));
      setLoading(false);
    }
  };

  const handleCancel = () => {
    router.push('/dashboard');
  };

  if (initialLoad) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-ai-blue mx-auto"></div>
          <p className="mt-4 text-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="w-full max-w-md bg-card-bg border border-border rounded-xl p-6 shadow-sm cursor-glow transition-shadow duration-300 card-ai-style">
        <h1 className="text-2xl font-bold text-center mb-6 bg-gradient-to-r from-ai-blue to-ai-purple bg-clip-text text-transparent">
          {taskId ? 'Edit Task' : 'Create New Task'}
        </h1>

        {error && (
          <div className="mb-4 p-3 bg-card-bg text-ai-red rounded-md border border-border">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="title" className="block text-foreground mb-2">
              Task Title *
            </label>
            <input
              id="title"
              name="title"
              type="text"
              value={formData.title}
              onChange={handleChange}
              className="w-full input-animated"
              required
              autoFocus
            />
          </div>

          <div className="mb-4">
            <label htmlFor="description" className="block text-foreground mb-2">
              Task Description
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              className="w-full input-animated"
              rows={3}
              placeholder="Optional description..."
            />
          </div>

          <div className="mb-4">
            <label htmlFor="dueDate" className="block text-foreground mb-2">
              Due Date
            </label>
            <input
              id="dueDate"
              name="dueDate"
              type="date"
              value={formData.dueDate}
              onChange={handleChange}
              className="w-full input-animated"
            />
          </div>

          <div className="mb-6">
            <label className="block text-foreground mb-2">
              Priority
            </label>
            <div className="flex space-x-4">
              <label className="inline-flex items-center">
                <input
                  type="radio"
                  name="priority"
                  value="low"
                  checked={formData.priority === 'low'}
                  onChange={handleChange}
                  className="text-ai-blue focus:ring-ai-blue"
                />
                <span className="ml-2 text-foreground">Low</span>
              </label>
              <label className="inline-flex items-center">
                <input
                  type="radio"
                  name="priority"
                  value="medium"
                  checked={formData.priority === 'medium'}
                  onChange={handleChange}
                  className="text-ai-green focus:ring-ai-green"
                />
                <span className="ml-2 text-foreground">Medium</span>
              </label>
              <label className="inline-flex items-center">
                <input
                  type="radio"
                  name="priority"
                  value="high"
                  checked={formData.priority === 'high'}
                  onChange={handleChange}
                  className="text-ai-purple focus:ring-ai-purple"
                />
                <span className="ml-2 text-foreground">High</span>
              </label>
            </div>
          </div>

          <div className="flex justify-between">
            <button
              type="button"
              onClick={handleCancel}
              className="btn-ai-gradient bg-card-bg border border-border text-foreground hover:bg-[#2a2a2a]"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="btn-ai-gradient"
            >
              {loading ? (taskId ? 'Updating...' : 'Creating...') : (taskId ? 'Update Task' : 'Create Task')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

const AddTaskPage = () => {
  return (
    <React.Suspense fallback={
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-ai-blue mx-auto"></div>
          <p className="mt-4 text-foreground">Loading...</p>
        </div>
      </div>
    }>
      <AddTaskContent />
    </React.Suspense>
  );
};

export default AddTaskPage;