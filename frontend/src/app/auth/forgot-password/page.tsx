'use client';

import { useState } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Mail, Home } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [submitError, setSubmitError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setMessage('');
    setSubmitError('');

    if (!email) {
      setError('Email is required');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('/api/auth/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });
      if (response.ok) {
        setMessage('If an account exists, a reset link has been sent to your email.');
        setEmail('');
      } else {
        const data = await response.json().catch(() => ({}));
        setError(data.detail || 'Something went wrong. Please try again.');
      }
    } catch {
      setSubmitError('Network error. Please check your connection and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    setSubmitError('');
    setError('');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4 py-12">
      <motion.div
        initial={{ opacity: 0, scale: 0.96 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.25, ease: 'easeOut' }}
        className="w-full max-w-md"
      >
        <div className="bg-surface border border-border rounded-card p-8 md:p-10 shadow-soft">
          <div className="mb-8">
            <Link href="/" className="inline-flex items-center gap-2 text-secondary-text hover:text-accent transition-colors duration-200 mb-6">
              <Home className="w-4 h-4" />
              <span className="text-sm">Back to Home</span>
            </Link>
            <div className="text-center">
              <h1 className="font-serif text-3xl md:text-4xl font-semibold text-primary tracking-tight mb-2">
                Forgot Password
              </h1>
              <p className="text-secondary-text text-sm">
                Enter your email and we&apos;ll send you a reset link
              </p>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            {submitError && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-4 bg-error/10 border border-error/20 rounded-input flex items-center justify-between"
              >
                <p className="text-sm text-error">{submitError}</p>
                <Button type="button" variant="secondary" size="sm" onClick={handleRetry}>
                  Retry
                </Button>
              </motion.div>
            )}
            <Input
              label="Email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              error={error}
              required
            />

            {message && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-4 bg-success/10 border border-success/20 rounded-input"
              >
                <p className="text-sm text-success">{message}</p>
              </motion.div>
            )}

            <Button type="submit" loading={isLoading} className="w-full" size="lg">
              Send Reset Link
            </Button>
          </form>

          <p className="text-center mt-8 text-sm text-secondary-text">
            Remember your password?{' '}
            <Link href="/auth/login" className="text-accent hover:text-accent-dark font-medium transition-colors">
              Sign in
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
}
