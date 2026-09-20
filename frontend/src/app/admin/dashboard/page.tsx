'use client';

import { useState, useEffect, type ComponentType } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import {
  ShoppingBag,
  DollarSign,
  Clock,
  AlertTriangle,
  ArrowUpRight,
  Package,
  Tag,
  TicketPercent,
  ImageIcon,
} from 'lucide-react';
import { AdminLayout } from '@/components/admin/admin-layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

interface DashboardStats {
  total_orders: number;
  total_revenue: number;
  pending_orders: number;
  low_stock_count: number;
}

const statCards: { title: string; key: keyof DashboardStats; icon: ComponentType<{ className?: string }>; color: string; prefix?: string }[] = [
  { title: 'Total Orders', key: 'total_orders', icon: ShoppingBag, color: 'text-accent' },
  { title: 'Revenue', key: 'total_revenue', icon: DollarSign, color: 'text-success', prefix: '$' },
  { title: 'Pending Orders', key: 'pending_orders', icon: Clock, color: 'text-accent' },
  { title: 'Low Stock', key: 'low_stock_count', icon: AlertTriangle, color: 'text-error' },
];

const quickActions = [
  { href: '/admin/products', label: 'Manage Products', icon: Package },
  { href: '/admin/categories', label: 'Manage Categories', icon: Tag },
  { href: '/admin/brands', label: 'Manage Brands', icon: Tag },
  { href: '/admin/coupons', label: 'Manage Coupons', icon: TicketPercent },
  { href: '/admin/banners', label: 'Manage Banners', icon: ImageIcon },
];

export default function AdminDashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const fetchDashboard = () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem('admin_token');
    fetch('/api/admin/dashboard', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch dashboard');
        return res.json();
      })
      .then((data) => {
        setStats(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || 'Something went wrong');
        setLoading(false);
      });
  };

  useEffect(() => {
    const token = localStorage.getItem('admin_token');
    if (!token) {
      router.push('/admin/login');
      return;
    }
    fetchDashboard();
  }, [router]);

  return (
    <AdminLayout>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.25 }}
        className="space-y-8"
      >
        <div>
          <h1 className="font-serif text-3xl md:text-4xl font-semibold text-foreground tracking-tight">
            Dashboard
          </h1>
          <p className="text-secondary-text mt-2">Welcome back to Aura Admin</p>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
            {[...Array(4)].map((_, i) => (
              <Card key={i} className="h-32">
                <Skeleton className="h-6 w-24 mb-3" />
                <Skeleton className="h-8 w-16" />
              </Card>
            ))}
          </div>
        ) : error ? (
          <div className="text-center py-16">
            <p className="text-secondary-text mb-4">{error}</p>
            <Button onClick={fetchDashboard}>Retry</Button>
          </div>
        ) : stats ? (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
              {statCards.map((card, i) => {
                const Icon = card.icon;
                const value = card.prefix
                  ? `${card.prefix}${(stats[card.key as keyof DashboardStats] as number).toFixed(2)}`
                  : stats[card.key as keyof DashboardStats];
                return (
                  <Card className="shadow-soft hover:shadow-soft-lg transition-shadow duration-200">
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="text-secondary-text text-sm font-medium mb-1">{card.title}</p>
                        <p className="font-serif text-3xl font-semibold text-foreground">{value as string}</p>
                      </div>
                      <div className={`w-10 h-10 rounded-xl bg-surface flex items-center justify-center ${card.color}`}>
                        <Icon className="w-5 h-5" />
                      </div>
                    </div>
                  </Card>
                );
              })}
            </div>

            <div>
              <h2 className="font-serif text-2xl font-semibold text-foreground mb-4">Quick Actions</h2>
                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 md:gap-4">
                  {quickActions.map((action, i) => {
                    const Icon = action.icon;
                    return (
                      <a key={action.href} href={action.href}>
                        <Card className="shadow-soft hover:shadow-soft-lg hover:border-accent/30 transition-all duration-200 group cursor-pointer flex flex-col items-center justify-center gap-3 py-6">
                          <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center group-hover:bg-accent/20 transition-colors duration-200">
                            <Icon className="w-6 h-6 text-accent" />
                          </div>
                          <span className="text-sm font-medium text-foreground text-center">{action.label}</span>
                        </Card>
                      </a>
                    );
                  })}
                </div>
            </div>
          </>
        ) : (
          <Card className="text-center py-16">
            <p className="text-secondary-text mb-4">No dashboard data available</p>
            <Button onClick={fetchDashboard}>Retry</Button>
          </Card>
        )}
      </motion.div>
    </AdminLayout>
  );
}
