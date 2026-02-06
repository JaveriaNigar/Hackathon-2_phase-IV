// frontend/src/app/welcome/WelcomeContent.tsx
'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { Suspense } from 'react';

function WelcomeComponent() {
  const [username, setUsername] = useState<string | null>(null);
  const searchParams = useSearchParams();

  useEffect(() => {
    const userParam = searchParams.get('username');
    const storedUsername = localStorage.getItem('username');

    if (userParam) {
      setUsername(decodeURIComponent(userParam));
    } else if (storedUsername) {
      setUsername(storedUsername);
    } else {
      setUsername('User');
    }
  }, [searchParams]);

  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      {/* justify-center added to vertically and horizontally center */}
      <div className="text-center max-w-4xl px-4">
        <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6 bg-gradient-to-r from-ai-blue to-ai-purple bg-clip-text text-transparent">
          Welcome, {username || 'User'}!
        </h1>

        <p className="text-xl text-foreground/80 mb-10 max-w-2xl mx-auto">
          Ready to boost your productivity with AI-powered task management? <br />
          Let's make organizing your tasks smarter and more efficient.
        </p>

        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <Link href="/dashboard">
            <button className="btn-ai-gradient px-8 py-4 text-lg w-full sm:w-auto rounded-lg ripple-effect">
              Dashboard
            </button>
          </Link>

          <Link href={`/ask-agent${username ? `?username=${encodeURIComponent(username)}` : ''}`}>
            <button className="btn-ai-gradient px-8 py-4 text-lg w-full sm:w-auto rounded-lg ripple-effect pulse">
              Ask Todo Agent
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}

function WelcomeContent() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-background flex items-start justify-center">
          <div className="text-center mt-2">
            <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-4 bg-gradient-to-r from-ai-blue to-ai-purple bg-clip-text text-transparent">
              Welcome!
            </h1>
            <p className="text-xl text-foreground/80">
              Loading your personalized experience...
            </p>
          </div>
        </div>
      }
    >
      <div className="min-h-screen bg-background flex items-start justify-center">
        <div className="text-center max-w-4xl px-4 mt-2">
          <WelcomeComponent />
        </div>
      </div>
    </Suspense>
  );
}

export default WelcomeContent;
