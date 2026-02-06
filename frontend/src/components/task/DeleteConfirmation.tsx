// frontend/src/components/task/DeleteConfirmation.tsx
import React from 'react';
import BrownCard from '@/components/theme/BrownCard';
import BrownButton from '@/components/theme/BrownButton';

interface DeleteConfirmationProps {
  isOpen: boolean;
  taskTitle: string;
  onClose: () => void;
  onConfirm: () => void;
}

const DeleteConfirmation: React.FC<DeleteConfirmationProps> = ({
  isOpen,
  taskTitle,
  onClose,
  onConfirm
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <BrownCard className="w-full max-w-md p-6">
        <h2 className="text-xl font-bold text-black mb-4">Confirm Deletion</h2>

        <p className="mb-6 text-black">
          Are you sure you want to delete the task "<strong>{taskTitle}</strong>"? This action cannot be undone.
        </p>

        <div className="flex justify-end space-x-3">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 border border-brown-border rounded-lg text-black hover:bg-brown-light"
          >
            Cancel
          </button>
          <BrownButton
            onClick={onConfirm}
            className="bg-brown-accent hover:bg-[#6a2834]"
          >
            Delete
          </BrownButton>
        </div>
      </BrownCard>
    </div>
  );
};

export default DeleteConfirmation;