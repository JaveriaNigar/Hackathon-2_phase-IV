// frontend/src/components/dashboard/TaskList.tsx
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { toggleComplete, deleteTask, createTask, updateTask, getTasks } from '@/services/tasks';
import { getToken } from '@/lib/auth';

// Define the task interface to match backend response
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

// Define the frontend task interface
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

interface TaskListProps {
  tasks: Task[];
  onTaskAdded?: (task: Task) => void;
  onTaskUpdated?: (task: Task) => void;
  onTaskDeleted?: (taskId: string) => void;
  onEditTask?: (task: Task) => void;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onTaskAdded,
  onTaskUpdated,
  onTaskDeleted,
  onEditTask
}) => {
  const [localTasks, setLocalTasks] = useState<Task[]>(tasks);
  const [loadingTaskId, setLoadingTaskId] = useState<string | null>(null);


  // Get user ID from token
  const token = getToken();
  let userId = '';
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      userId = payload.userId || payload.sub || '';

      // Ensure userId is valid
      if (!userId) {
        console.error('User ID not found in token payload');
      }
    } catch (err) {
      console.error('Error parsing token:', err);
    }
  }

  // Update local state when parent tasks prop changes
  useEffect(() => {
    setLocalTasks(tasks);
  }, [tasks]);

  // Listen for tasksChanged event to refresh tasks
  useEffect(() => {
    const handleTasksChanged = async () => {
      try {
        const refreshedTasks = await getTasks();
        // Convert backend tasks to frontend format
        const convertedTasks = refreshedTasks.map(backendTask => ({
          id: backendTask.id.toString(),
          title: backendTask.title,
          description: backendTask.description,
          completed: backendTask.completed,
          userId: backendTask.user_id,
          dueDate: backendTask.due_date,
          priority: backendTask.priority,
          createdAt: backendTask.created_at,
          updatedAt: backendTask.updated_at,
          completedAt: null
        }));
        setLocalTasks(convertedTasks);
      } catch (error) {
        console.error('Error refreshing tasks:', error);
      }
    };

    window.addEventListener('tasksChanged', handleTasksChanged);

    // Cleanup listener on unmount
    return () => {
      window.removeEventListener('tasksChanged', handleTasksChanged);
    };
  }, []);

  // Convert backend task to frontend format
  const convertBackendTaskToFrontend = (backendTask: BackendTask): Task => ({
    id: backendTask.id.toString(),
    title: backendTask.title,
    description: backendTask.description,
    completed: backendTask.completed,
    userId: backendTask.user_id,
    dueDate: backendTask.due_date,
    priority: backendTask.priority,
    createdAt: backendTask.created_at,
    updatedAt: backendTask.updated_at,
    completedAt: null // Backend doesn't send completedAt in response
  });

  const handleToggleComplete = async (taskId: string, currentStatus: boolean) => {
    // Prevent multiple clicks while request is in progress
    if (loadingTaskId === taskId) {
      return;
    }

    setLoadingTaskId(taskId);
    try {
      const updatedTask: BackendTask = await toggleComplete(taskId);
      const frontendTask = convertBackendTaskToFrontend(updatedTask);
      setLocalTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? frontendTask : task
        )
      );

      // Call parent callback to update parent state
      if (onTaskUpdated) {
        onTaskUpdated(frontendTask);
      }
    } catch (error) {
      console.error('Error toggling task:', error);
      // Optionally notify the parent component about the error
    } finally {
      setLoadingTaskId(null);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    // Prevent multiple clicks while request is in progress
    if (loadingTaskId === taskId) {
      return;
    }

    setLoadingTaskId(taskId);
    try {
      await deleteTask(taskId);
      setLocalTasks(prevTasks =>
        prevTasks.filter(task => task.id !== taskId)
      );

      // Call parent callback to update parent state
      if (onTaskDeleted) {
        onTaskDeleted(taskId);
      }
    } catch (error) {
      console.error('Error deleting task:', error);
      // Optionally notify the parent component about the error
    } finally {
      setLoadingTaskId(null);
    }
  };

  if (localTasks.length === 0) {
    return (
      <div className="space-y-4">
        <div className="text-center py-12 bg-card-bg border border-border rounded-xl shadow-sm cursor-glow transition-shadow duration-300 card-ai-style fade-in">
          <h3 className="text-xl font-semibold text-ai-blue mb-2">No tasks yet</h3>
          <p className="text-foreground">Add your first task to get started!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {localTasks.map((task) => (
        <div key={task.id} className="p-4 bg-card-bg border border-border rounded-xl shadow-sm cursor-glow transition-shadow duration-300 card-ai-style slide-in">
          {/* Display task */}
          <div className="flex items-start">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => handleToggleComplete(task.id, task.completed)}
              disabled={loadingTaskId === task.id}
              className="mt-1 mr-3 h-5 w-5 rounded border-border text-ai-blue focus:ring-ai-blue"
            />
            <div className="flex-1">
              <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-ai-purple' : 'text-foreground'}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`mt-1 ${task.completed ? 'line-through text-ai-purple' : 'text-foreground/70'}`}>
                  {task.description}
                </p>
              )}
              {task.dueDate && (
                <p className="mt-1 text-sm text-foreground/70">
                  Due: {new Date(task.dueDate).toLocaleDateString()}
                </p>
              )}
              {task.priority && (
                <span className={`inline-block mt-1 px-2 py-1 text-xs rounded-full ${task.priority === 'high'
                    ? 'bg-ai-purple text-white'
                    : task.priority === 'medium'
                      ? 'bg-ai-green text-white'
                      : 'bg-ai-blue text-white'
                  }`}>
                  {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                </span>
              )}
              <div className="mt-2 flex space-x-3">
                <Link href={`/add-task?id=${task.id}`}>
                  <button
                    type="button"
                    className="text-sm text-ai-blue hover:underline"
                  >
                    Edit
                  </button>
                </Link>
                <button
                  onClick={() => handleDeleteTask(task.id)}
                  className="text-sm text-ai-red hover:underline"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default TaskList;