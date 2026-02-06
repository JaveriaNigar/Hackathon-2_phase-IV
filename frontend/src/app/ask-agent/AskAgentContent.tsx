// frontend/src/app/ask-agent/AskAgentContent.tsx
'use client';

import React from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { Suspense } from 'react';

function AskAgentComponent() {
  const searchParams = useSearchParams();
  const username = searchParams.get('username') || '';

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center fade-in">
          <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6 bg-gradient-to-r from-ai-blue to-ai-purple bg-clip-text text-transparent">
            Todo Agent Interface
          </h1>

          <p className="text-xl text-foreground/80 mb-10 max-w-2xl mx-auto slide-in">
            This is where you'll interact with the AI-powered Todo Agent. <br />
            Ask questions, create tasks, and get intelligent recommendations.
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-4 slide-in" style={{ animationDelay: '0.2s' }}>
            <Link href="/dashboard">
              <button className="btn-ai-gradient px-8 py-4 text-lg w-full sm:w-auto rounded-lg ripple-effect">
                Back to Dashboard
              </button>
            </Link>

            <Link href="/agent">
              <button className="btn-ai-gradient px-8 py-4 text-lg w-full sm:w-auto rounded-lg ripple-effect">
                Ask Todo Agent
              </button>
            </Link>
          </div>
        </div>

        <div className="mt-20 max-w-3xl mx-auto fade-in" style={{ animationDelay: '0.4s' }}>
          <div className="chat-card cursor-glow scale-in">
            <h2 className="text-2xl font-bold text-foreground mb-4">How to Use the Todo Agent</h2>
            <div className="space-y-4">
              <div className="flex items-start slide-in">
                <div className="flex-shrink-0 mt-1">
                  <div className="w-8 h-8 rounded-full bg-ai-blue flex items-center justify-center text-white font-bold">1</div>
                </div>
                <p className="ml-4 text-foreground/80">Type your request in natural language</p>
              </div>
              <div className="flex items-start slide-in" style={{ animationDelay: '0.1s' }}>
                <div className="flex-shrink-0 mt-1">
                  <div className="w-8 h-8 rounded-full bg-ai-purple flex items-center justify-center text-white font-bold">2</div>
                </div>
                <p className="ml-4 text-foreground/80">Our AI will interpret and create appropriate tasks</p>
              </div>
              <div className="flex items-start slide-in" style={{ animationDelay: '0.2s' }}>
                <div className="flex-shrink-0 mt-1">
                  <div className="w-8 h-8 rounded-full bg-ai-green flex items-center justify-center text-white font-bold">3</div>
                </div>
                <p className="ml-4 text-foreground/80">Review and adjust tasks as needed</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function AskAgentContent() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6 bg-gradient-to-r from-ai-blue to-ai-purple bg-clip-text text-transparent">
            Todo Agent Interface
          </h1>
          <p className="text-xl text-foreground/80">Loading agent interface...</p>
        </div>
      </div>
    }>
      <AskAgentComponent />
    </Suspense>
  );
}

export default AskAgentContent;