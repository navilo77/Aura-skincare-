'use client';

import { cva, type VariantProps } from 'class-variance-authority';

const badgeVariants = cva(
  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-accent/10 text-accent',
        success: 'bg-success/10 text-success',
        error: 'bg-error/10 text-error',
        new: 'bg-accent text-white',
        best: 'bg-primary text-white',
        limited: 'bg-error text-white',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

interface BadgeProps extends VariantProps<typeof badgeVariants> {
  children: React.ReactNode;
  className?: string;
}

export function Badge({ variant, children, className = '' }: BadgeProps) {
  return (
    <span className={badgeVariants({ variant, className })}>
      {children}
    </span>
  );
}
