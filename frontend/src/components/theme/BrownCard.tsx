// frontend/src/components/theme/BrownCard.tsx
import React from 'react';

interface BrownCardProps {
  children: React.ReactNode;
  className?: string;
  hoverEffect?: boolean;
}

const BrownCard: React.FC<BrownCardProps> = ({
  children,
  className = '',
  hoverEffect = true
}) => {
  return (
    <div
      className={`
        bg-card-bg border border-border rounded-xl
        ${hoverEffect ? 'hover:shadow-lg transition-shadow duration-300' : ''}
        p-6
        ${className}
      `}
    >
      {children}
    </div>
  );
};

export default BrownCard;