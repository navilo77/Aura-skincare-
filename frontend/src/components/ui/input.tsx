'use client';

import { motion, HTMLMotionProps } from 'framer-motion';
import { ReactNode } from 'react';

interface InputProps extends Omit<HTMLMotionProps<'input'>, 'children'> {
  label?: string;
  error?: string;
  rightElement?: ReactNode;
}

export function Input({ label, error, className = '', rightElement, ...props }: InputProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-primary mb-1.5">
          {label}
        </label>
      )}
      <div className="relative">
        <motion.input
          whileFocus={{ scale: 1.005 }}
          transition={{ duration: 0.15 }}
          className={[
            'w-full px-4 py-3 bg-background border rounded-input text-primary placeholder-secondary-text transition-all duration-200 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent',
            error ? 'border-error' : 'border-border',
            rightElement ? 'pr-12' : '',
            className,
          ]
            .filter(Boolean)
            .join(' ')}
          {...props}
        />
        {rightElement && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2">
            {rightElement}
          </div>
        )}
      </div>
      {error && <p className="mt-1.5 text-sm text-error">{error}</p>}
    </div>
  );
}
