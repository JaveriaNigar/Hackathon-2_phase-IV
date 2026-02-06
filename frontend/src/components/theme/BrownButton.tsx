// frontend/src/components/theme/BrownButton.tsx
import React from 'react';

interface BrownButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  className?: string;
  disabled?: boolean;
}

const BrownButton: React.FC<BrownButtonProps> = ({
  children,
  onClick,
  type = 'button',
  className = '',
  disabled = false
}) => {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`
        btn-brown-gradient
        ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-90 hover:transform hover:translate-y-[-1px]'}
        ${className}
      `}
    >
      {children}
    </button>
  );
};

export default BrownButton;