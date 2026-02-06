// frontend/src/components/dashboard/UserInfoCards.tsx
import React from 'react';

interface User {
  id: string;
  name: string;
  email: string;
}

interface UserInfoCardsProps {
  user: User | null;
  taskCount: number;
  pendingTaskCount: number;
  completedTaskCount: number;
}

const UserInfoCards: React.FC<UserInfoCardsProps> = ({ user, taskCount, pendingTaskCount, completedTaskCount }) => {
  return (
    <div className="w-full flex">
      {/* Inner row - right aligned */}
      <div className="flex flex-col md:flex-row gap-4 ml-auto">
        {/* Name Box */}
        <div className="w-[240px] h-[100px] flex flex-col items-center justify-center
                        bg-card-bg border border-border rounded-xl shadow-sm
                        cursor-glow transition-all duration-300 card-ai-style scale-in">
          <h3 className="text-sm font-semibold text-ai-blue mb-1">Name</h3>
          <p className="text-sm font-medium text-foreground">{user?.name || 'User'}</p>
        </div>

        {/* Email Box */}
        <div className="w-[240px] h-[100px] flex flex-col items-center justify-center
                        bg-card-bg border border-border rounded-xl shadow-sm
                        cursor-glow transition-all duration-300 card-ai-style scale-in" style={{animationDelay: '0.1s'}}>
          <h3 className="text-sm font-semibold text-ai-purple mb-1">Email</h3>
          <p className="text-sm font-medium text-foreground">{user?.email || 'user@example.com'}</p>
        </div>

        {/* Total Tasks Box */}
        <div className="w-[240px] h-[100px] flex flex-col items-center justify-center
                        bg-card-bg border border-border rounded-xl shadow-sm
                        cursor-glow transition-all duration-300 card-ai-style scale-in" style={{animationDelay: '0.2s'}}>
          <h3 className="text-sm font-semibold text-ai-green mb-1">Total Tasks</h3>
          <p className="text-sm font-medium text-foreground">{taskCount}</p>
        </div>

        {/* Pending Tasks Box */}
        <div className="w-[240px] h-[100px] flex flex-col items-center justify-center
                        bg-card-bg border border-border rounded-xl shadow-sm
                        cursor-glow transition-all duration-300 card-ai-style scale-in" style={{animationDelay: '0.3s'}}>
          <h3 className="text-sm font-semibold text-ai-cyan mb-1">Pending Tasks</h3>
          <p className="text-sm font-medium text-foreground">{pendingTaskCount}</p>
        </div>

        {/* Completed Tasks Box */}
        <div className="w-[240px] h-[100px] flex flex-col items-center justify-center
                        bg-card-bg border border-border rounded-xl shadow-sm
                        cursor-glow transition-all duration-300 card-ai-style scale-in" style={{animationDelay: '0.4s'}}>
          <h3 className="text-sm font-semibold text-ai-blue mb-1">Completed Tasks</h3>
          <p className="text-sm font-medium text-foreground">{completedTaskCount}</p>
        </div>
      </div>
    </div>
  );
};

export default UserInfoCards;
