// frontend/src/app/(auth)/login/page.tsx
'use client';

import React, { useState } from 'react';
import { login } from '@/services/auth';
import Link from 'next/link';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const result = await login({ email, password });
      // Redirect to welcome page after successful login, passing the user's name
      window.location.href = `/welcome?username=${encodeURIComponent(result.user.name)}`;
    } catch (err: any) {
      setError(err.message || 'An error occurred during login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="w-full max-w-md bg-card-bg border border-border rounded-xl p-6 shadow-sm cursor-glow transition-shadow duration-300 card-ai-style">
        <h1 className="text-2xl font-bold text-center mb-6 bg-gradient-to-r from-ai-blue to-ai-purple bg-clip-text text-transparent">Login to Your Account</h1>

        {error && (
          <div className="mb-4 p-3 bg-card-bg text-ai-red rounded-md border border-border">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="email" className="block text-foreground mb-2">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full input-animated"
              required
            />
          </div>

          <div className="mb-6">
            <label htmlFor="password" className="block text-foreground mb-2">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full input-animated"
              required
            />
          </div>

          <div className="flex flex-col gap-3">
            <button
              type="submit"
              disabled={loading}
              className="btn-ai-gradient w-full py-3 rounded-lg ripple-effect"
            >
              {loading ? 'Logging In...' : 'Login'}
            </button>

            <div className="text-center text-foreground mt-4">
              Don't have an account?{' '}
              <Link href="/signup" className="text-ai-blue hover:underline">
                Sign Up
              </Link>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;