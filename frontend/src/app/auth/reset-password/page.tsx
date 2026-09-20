'use client';

import { useState, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Home } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { PasswordStrength } from '@/components/auth/password-strength';
import { Skeleton } from '@/components/ui/skeleton';

function ResetPasswordForm() {
  const searchParams = useSearchParams();
  const token = searchParams.get('token');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [submitError, setSubmitError] = useState('');

  useEffect(() => {
    if (!token) {
      setError('Invalid or missing token.');
    }
  }, [token]);

  const validate = () => {
    const newErrors: string[] = [];
    if (!password) newErrors.push('Password is required');
    if (password.length < 8) newErrors.push('Password must be at least 8 characters');
    if (password !== confirmPassword) newErrors.push('Passwords do not match');
    return newErrors.join(' ');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setMessage('');
    setSubmitError('');

    const validationError = validate();
    if (validationError) {
      setError(validationError);
      return;
    }

    if (!token) {
      setError('Invalid or missing token.');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('/api/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, new_password: password }),
      });
      if (response.ok) {
        setMessage('Password reset successfully. Redirecting to login...');
        setTimeout(() => {
          window.location.href = '/auth/login';
        }, 2500);
      } else {
        const data = await response.json().catch(() => ({}));
        setError(data.detail || 'Failed to reset password. Please try again.');
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
                Reset Password
              </h1>
              <p className="text-secondary-text text-sm">
                Create a new password for your account
              </p>
            </div>
          </div>

          {error && !token && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 p-4 bg-error/10 border border-error/20 rounded-input"
            >
              <p className="text-sm text-error">{error}</p>
              <Link href="/auth/forgot-password" className="text-sm text-accent hover:text-accent-dark underline mt-2 inline-block">
                Request a new reset link
              </Link>
            </motion.div>
          )}

          {!error && (
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
              <div>
                <Input
                  label="New Password"
                  type="password"
                  placeholder="Create a strong password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  minLength={8}
                />
                <PasswordStrength password={password} />
              </div>

              <Input
                label="Confirm Password"
                type="password"
                placeholder="Re-enter your password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                error={confirmPassword && password !== confirmPassword ? 'Passwords do not match' : undefined}
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
                Reset Password
              </Button>
            </form>
          )}

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

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center bg-background px-4 py-12">
        <div className="w-full max-w-md">
          <div className="bg-surface border border-border rounded-card p-8 md:p-10 shadow-soft">
            <div className="text-center">
              <Skeleton className="h-8 w-8 rounded-full mx-auto mb-4" />
              <Skeleton className="h-4 w-32 mx-auto" />
            </div>
          </div>
        </div>
      </div>
    }>
      <ResetPasswordForm />
    </Suspense>
  );
}
