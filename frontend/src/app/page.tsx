// frontend/src/app/page.tsx
import React from 'react';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center fade-in">
          <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6 bg-gradient-to-r from-ai-blue to-ai-purple bg-clip-text text-transparent">
            Welcome to <span className="text-ai-blue">AI</span> Todo App
          </h1>

          <p className="text-xl text-foreground/80 mb-10 max-w-2xl mx-auto slide-in">
            Experience the future of task management with our AI-powered interface. <br />
            Organize, prioritize, and accomplish your goals with intelligent assistance.
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-4 slide-in" style={{animationDelay: '0.2s'}}>
            <Link href="/signup">
              <button className="btn-ai-gradient px-8 py-4 text-lg w-full sm:w-auto rounded-lg ripple-effect pulse">
                Get Started
              </button>
            </Link>

            <Link href="/login">
              <button className="btn-ai-gradient px-8 py-4 text-lg w-full sm:w-auto rounded-lg ripple-effect">
                Login
              </button>
            </Link>
          </div>
        </div>

        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto fade-in" style={{animationDelay: '0.3s'}}>
          <div className="chat-card cursor-glow scale-in">
            <div className="flex items-center mb-4">
              <div className="w-3 h-3 rounded-full bg-ai-green mr-2"></div>
              <h3 className="text-xl font-semibold text-ai-blue">Smart Organization</h3>
            </div>
            <p className="text-foreground/80">
              Our AI assistant helps you categorize and prioritize tasks automatically,
              ensuring you focus on what matters most.
            </p>
          </div>

          <div className="chat-card cursor-glow scale-in" style={{animationDelay: '0.1s'}}>
            <div className="flex items-center mb-4">
              <div className="w-3 h-3 rounded-full bg-ai-cyan mr-2"></div>
              <h3 className="text-xl font-semibold text-ai-purple">Progress Tracking</h3>
            </div>
            <p className="text-foreground/80">
              Visualize your productivity trends and get insights on your performance
              to continuously improve your workflow.
            </p>
          </div>

          <div className="chat-card cursor-glow scale-in" style={{animationDelay: '0.2s'}}>
            <div className="flex items-center mb-4">
              <div className="w-3 h-3 rounded-full bg-ai-blue mr-2"></div>
              <h3 className="text-xl font-semibold text-ai-green">Secure & Private</h3>
            </div>
            <p className="text-foreground/80">
              Your data is encrypted and securely stored with industry-standard protocols.
              Privacy is our top priority.
            </p>
          </div>
        </div>

        <div className="mt-20 max-w-3xl mx-auto fade-in" style={{animationDelay: '0.4s'}}>
          <div className="chat-card cursor-glow scale-in">
            <h2 className="text-2xl font-bold text-foreground mb-4">How It Works</h2>
            <div className="space-y-4">
              <div className="flex items-start slide-in">
                <div className="flex-shrink-0 mt-1">
                  <div className="w-8 h-8 rounded-full bg-ai-blue flex items-center justify-center text-white font-bold">1</div>
                </div>
                <p className="ml-4 text-foreground/80">Sign up and connect your AI assistant to your workflow</p>
              </div>
              <div className="flex items-start slide-in" style={{animationDelay: '0.1s'}}>
                <div className="flex-shrink-0 mt-1">
                  <div className="w-8 h-8 rounded-full bg-ai-purple flex items-center justify-center text-white font-bold">2</div>
                </div>
                <p className="ml-4 text-foreground/80">Add tasks and let our AI categorize and prioritize them</p>
              </div>
              <div className="flex items-start slide-in" style={{animationDelay: '0.2s'}}>
                <div className="flex-shrink-0 mt-1">
                  <div className="w-8 h-8 rounded-full bg-ai-green flex items-center justify-center text-white font-bold">3</div>
                </div>
                <p className="ml-4 text-foreground/80">Track progress and receive intelligent recommendations</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
