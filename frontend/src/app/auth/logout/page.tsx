'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function LogoutPage() {
  const router = useRouter();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');

  useEffect(() => {
    const performLogout = async () => {
      try {
        const res = await fetch('/api/auth/logout', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        });
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        if (res.ok) {
          setStatus('success');
          setTimeout(() => router.push('/auth/login'), 800);
        } else {
          setStatus('error');
          setTimeout(() => router.push('/auth/login'), 1500);
        }
      } catch {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setStatus('error');
        setTimeout(() => router.push('/auth/login'), 1500);
      }
    };

    performLogout();
  }, [router]);

  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.25 }}
        className="text-center px-4"
      >
        <div className="w-16 h-16 rounded-full bg-surface flex items-center justify-center mx-auto mb-6">
          <LogOut className="w-8 h-8 text-accent" />
        </div>
        <h1 className="font-serif text-2xl font-semibold text-primary mb-2">
          {status === 'loading' ? 'Logging out...' : status === 'success' ? 'Logged Out' : 'Logging out...'}
        </h1>
        <p className="text-secondary-text">
          {status === 'loading'
            ? 'Please wait while we sign you out.'
            : status === 'success'
              ? 'You have been successfully logged out.'
              : 'Redirecting you to the login page...'}
        </p>
        {status === 'loading' && (
          <div className="mt-6 flex justify-center">
            <div className="w-6 h-6 border-2 border-accent border-t-transparent rounded-full animate-spin" />
          </div>
        )}
        {status === 'success' && (
          <div className="mt-6">
            <Button
              variant="primary"
              onClick={() => router.push('/auth/login')}
            >
              Go to Login
            </Button>
          </div>
        )}
      </motion.div>
    </div>
  );
}
