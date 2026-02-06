// frontend/src/components/task/CreateTaskModal.tsx
import React, { useState } from 'react';
import BrownCard from '@/components/theme/BrownCard';
import BrownButton from '@/components/theme/BrownButton';

interface CreateTaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (title: string, description?: string) => void;
}

const CreateTaskModal: React.FC<CreateTaskModalProps> = ({ isOpen, onClose, onCreate }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onCreate(title, description);
    setTitle('');
    setDescription('');
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <BrownCard className="w-full max-w-md p-6">
        <h2 className="text-xl font-bold text-black mb-4">Create New Task</h2>

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="title" className="block text-black mb-2">
              Title *
            </label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-4 py-2 border border-brown-border rounded-lg focus:outline-none focus:ring-2 focus:ring-brown-accent text-black"
              required
            />
          </div>

          <div className="mb-6">
            <label htmlFor="description" className="block text-black mb-2">
              Description
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-4 py-2 border border-brown-border rounded-lg focus:outline-none focus:ring-2 focus:ring-brown-accent text-black"
              rows={3}
            />
          </div>

          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-brown-border rounded-lg text-black hover:bg-brown-light"
            >
              Cancel
            </button>
            <BrownButton type="submit">Create Task</BrownButton>
          </div>
        </form>
      </BrownCard>
    </div>
  );
};

export default CreateTaskModal;