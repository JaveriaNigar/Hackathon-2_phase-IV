// frontend/src/services/tasks.ts
import { getToken, isAuthenticated } from '@/lib/auth';
import apiClient from './api';

interface Task {
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

interface TaskCreateRequest {
  title: string;
  description?: string;
  due_date?: string;
  priority?: string;
}

interface TaskUpdateRequest {
  title?: string;
  description?: string;
  completed?: boolean;
  due_date?: string;
  priority?: string;
}

/**
 * Helper function to extract user ID from JWT token
 */
const getUserIdFromToken = (): string => {
  const token = getToken();
  if (!token) {
    throw new Error('No authentication token found');
  }

  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const userId = payload.userId || payload.sub;

    if (!userId) {
      throw new Error('User ID not found in token');
    }

    return userId;
  } catch (error) {
    console.error('Error decoding token:', error);
    throw new Error('Invalid token format');
  }
};

/**
 * Helper function to make authenticated API requests using unified apiClient
 */
const apiRequest = async (endpoint: string, options: any = {}) => {
  try {
    const method = (options.method || 'GET').toLowerCase();
    const config = {
      ...options,
      url: endpoint,
      method,
    };

    // axios uses 'data' for the request body
    if (options.body && !options.data) {
      config.data = typeof options.body === 'string' ? JSON.parse(options.body) : options.body;
    }

    const response = await apiClient(config);
    return response.data;
  } catch (error: any) {
    console.error(`API request failed [${endpoint}]:`, error);
    throw new Error(error.response?.data?.detail || `HTTP error! status: ${error.response?.status}`);
  }
};

/**
 * Get all tasks for a user
 * @returns Promise resolving to array of tasks
 */
export const getTasks = async (): Promise<Task[]> => {
  try {
    const userId = getUserIdFromToken();
    const tasks = await apiRequest(`${userId}/tasks?t=${Date.now()}`);
    return tasks;
  } catch (error) {
    console.error('Error fetching tasks:', error);
    throw error;
  }
};

/**
 * Create a new task
 * @param taskData - The task data to create
 * @returns Promise resolving to the created task
 */
export const createTask = async (taskData: TaskCreateRequest): Promise<Task> => {
  try {
    const userId = getUserIdFromToken();
    const task = await apiRequest(`${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
    return task;
  } catch (error) {
    console.error('Error creating task:', error);
    throw error;
  }
};

/**
 * Update an existing task
 * @param taskId - The ID of the task to update
 * @param taskData - The updated task data
 * @returns Promise resolving to the updated task
 */
export const updateTask = async (taskId: string, taskData: TaskUpdateRequest): Promise<Task> => {
  try {
    const userId = getUserIdFromToken();
    const task = await apiRequest(`${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
    return task;
  } catch (error) {
    console.error('Error updating task:', error);
    throw error;
  }
};

/**
 * Delete a task
 * @param taskId - The ID of the task to delete
 * @returns Promise resolving when task is deleted
 */
export const deleteTask = async (taskId: string): Promise<void> => {
  try {
    const userId = getUserIdFromToken();
    await apiRequest(`${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  } catch (error) {
    console.error('Error deleting task:', error);
    throw error;
  }
};

/**
 * Toggle task completion status
 * @param taskId - The ID of the task to update completion status
 * @returns Promise resolving to the updated task
 */
export const toggleComplete = async (taskId: string): Promise<Task> => {
  try {
    const userId = getUserIdFromToken();
    const task = await apiRequest(`${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
    });
    return task;
  } catch (error) {
    console.error('Error toggling task completion:', error);
    throw error;
  }
};

/**
 * Get the count of pending tasks for a user
 * @returns Promise resolving to an object with the pending count
 */
export interface PendingTasksCount {
  pending: number;
}

export const getPendingTasksCount = async (): Promise<PendingTasksCount> => {
  try {
    const userId = getUserIdFromToken();
    const result = await apiRequest(`${userId}/pending-tasks`);
    return result;
  } catch (error) {
    console.error('Error fetching pending tasks count:', error);
    throw error;
  }
};

/**
 * Get the count of completed tasks for a user
 * @returns Promise resolving to an object with the completed count
 */
export interface CompletedTasksCount {
  completed: number;
}

export const getCompletedTasksCount = async (): Promise<CompletedTasksCount> => {
  try {
    const userId = getUserIdFromToken();
    const result = await apiRequest(`${userId}/completed-tasks`);
    return result;
  } catch (error) {
    console.error('Error fetching completed tasks count:', error);
    throw error;
  }
};

/**
 * Get a single task by ID
 * @param taskId - The ID of the task to retrieve
 * @returns Promise resolving to the task
 */
export const getTaskById = async (taskId: string): Promise<Task> => {
  try {
    if (!taskId) {
      throw new Error('Task ID is required to fetch a task');
    }

    const userId = getUserIdFromToken();
    const task = await apiRequest(`${userId}/tasks/${taskId}`);
    return task;
  } catch (error) {
    console.error('Error fetching task by ID:', error);
    throw error;
  }
};