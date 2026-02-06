// frontend/src/components/task/TaskModal.tsx
import React, { useState, useEffect } from 'react';
import BrownCard from '@/components/theme/BrownCard';
import BrownButton from '@/components/theme/BrownButton';

interface Task {
  id?: string;
  title: string;
  description?: string;
  dueDate?: string;
  priority: string;
  completed?: boolean;
  createdAt?: string;
  updatedAt?: string;
  completedAt?: string | null;
}

interface TaskModalProps {
  isOpen: boolean;
  task?: Task | null;
  onClose: () => void;
  onSave: (taskData: Omit<Task, 'id' | 'createdAt' | 'updatedAt' | 'completedAt' | 'completed'> & { id?: string }) => void;
}

const TaskModal: React.FC<TaskModalProps> = ({ isOpen, task, onClose, onSave }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [priority, setPriority] = useState('normal');

  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description || '');
      setDueDate(task.dueDate || '');
      setPriority(task.priority || 'normal');
    } else {
      // Reset form for new task
      setTitle('');
      setDescription('');
      setDueDate('');
      setPriority('normal');
    }
  }, [task, isOpen]); // Added isOpen to the dependency array to reset when modal closes and reopens

  console.log('TaskModal rendered with isOpen:', isOpen);
  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const taskData = {
      id: task?.id,
      title,
      description: description || undefined,
      dueDate: dueDate || undefined,
      priority
    };

    onSave(taskData);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" style={{ zIndex: 9999 }}>
      <BrownCard className="w-full max-w-md p-6">
        <h2 className="text-xl font-bold text-black mb-4">
          {task ? 'Edit Task' : 'Create New Task'}
        </h2>

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="title" className="block text-black mb-2">
              Task Title *
            </label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-4 py-2 border border-brown-border rounded-lg focus:outline-none focus:ring-2 focus:ring-brown-accent text-black"
              required
              autoFocus
            />
          </div>

          <div className="mb-4">
            <label htmlFor="description" className="block text-black mb-2">
              Task Description
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-4 py-2 border border-brown-border rounded-lg focus:outline-none focus:ring-2 focus:ring-brown-accent text-black"
              rows={3}
              placeholder="Optional description..."
            />
          </div>

          <div className="mb-4">
            <label htmlFor="dueDate" className="block text-black mb-2">
              Due Date
            </label>
            <input
              id="dueDate"
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              className="w-full px-4 py-2 border border-brown-border rounded-lg focus:outline-none focus:ring-2 focus:ring-brown-accent text-black"
            />
          </div>

          <div className="mb-6">
            <label className="block text-black mb-2">
              Priority
            </label>
            <div className="flex space-x-4">
              <label className="inline-flex items-center">
                <input
                  type="radio"
                  name="priority"
                  value="normal"
                  checked={priority === 'normal'}
                  onChange={() => setPriority('normal')}
                  className="text-brown-accent focus:ring-brown-accent"
                />
                <span className="ml-2 text-black">Normal</span>
              </label>
              <label className="inline-flex items-center">
                <input
                  type="radio"
                  name="priority"
                  value="urgent"
                  checked={priority === 'urgent'}
                  onChange={() => setPriority('urgent')}
                  className="text-brown-accent focus:ring-brown-accent"
                />
                <span className="ml-2 text-black">Urgent</span>
              </label>
            </div>
          </div>

          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-brown-border rounded-lg text-black hover:bg-brown-light"
            >
              Cancel
            </button>
            <BrownButton type="submit">
              {task ? 'Update Task' : 'Add Task'}
            </BrownButton>
          </div>
        </form>
      </BrownCard>
    </div>
  );
};

export default TaskModal;