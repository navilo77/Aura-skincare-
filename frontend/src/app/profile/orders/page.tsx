'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Package, ArrowRight, ShoppingBag } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

interface Order {
  id: string;
  order_number: string;
  status: string;
  total_amount: number;
  currency: string;
  created_at: string;
  item_count?: number;
}

const statusColors: Record<string, string> = {
  pending: 'default',
  confirmed: 'default',
  processing: 'default',
  shipped: 'default',
  delivered: 'success',
  cancelled: 'error',
};

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [retryCount, setRetryCount] = useState(0);

  const fetchOrders = () => {
    setLoading(true);
    setError('');
    fetch('/api/profile/orders')
      .then((res) => res.ok ? res.json() : [])
      .then((data) => {
        setOrders(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load orders. Please try again.');
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchOrders();
  }, [retryCount]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="w-full max-w-2xl space-y-4 px-4">
          <Skeleton className="h-10 w-48 mx-auto" />
          <Skeleton className="h-24 w-full" />
          <Skeleton className="h-24 w-full" />
          <Skeleton className="h-24 w-full" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center px-4">
          <Package className="w-12 h-12 text-border mx-auto mb-4" />
          <p className="text-secondary-text mb-4">{error}</p>
          <Button onClick={() => setRetryCount((c) => c + 1)} variant="primary">
            Try Again
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
        >
          <h1 className="font-serif text-3xl md:text-4xl font-semibold text-primary tracking-tight">
            My Orders
          </h1>
          <p className="mt-2 text-secondary-text">
            {orders.length > 0
              ? `${orders.length} order${orders.length !== 1 ? 's' : ''} placed`
              : ''}
          </p>
        </motion.div>

        {orders.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.25 }}
            className="mt-16 flex flex-col items-center justify-center text-center"
          >
            <div className="w-20 h-20 rounded-full bg-surface flex items-center justify-center mb-6">
              <ShoppingBag className="w-10 h-10 text-accent" />
            </div>
            <h2 className="font-serif text-2xl font-semibold text-primary mb-2">
              No orders yet
            </h2>
            <p className="text-secondary-text mb-8 max-w-sm">
              Start your skincare journey and explore our premium collection.
            </p>
            <Link
              href="/products"
              className="inline-flex items-center px-6 py-3 bg-accent text-white font-medium rounded-button hover:bg-accent-dark transition-all duration-200"
            >
              Explore Products
              <ArrowRight className="ml-2 w-4 h-4" />
            </Link>
          </motion.div>
        ) : (
          <div className="mt-8 space-y-4">
            {orders.map((order, index) => (
              <motion.div
                key={order.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.25, delay: index * 0.05 }}
              >
                <Link href={`/profile/orders/${order.id}`}>
                  <Card hover className="cursor-pointer">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div className="flex items-center gap-4">
                        <div className="w-12 h-12 rounded-full bg-accent/10 flex items-center justify-center flex-shrink-0">
                          <Package className="w-6 h-6 text-accent" />
                        </div>
                        <div>
                          <p className="font-serif font-semibold text-primary">
                            {order.order_number}
                          </p>
                          <p className="text-sm text-secondary-text mt-0.5">
                            {new Date(order.created_at).toLocaleDateString('en-US', {
                              month: 'long',
                              day: 'numeric',
                              year: 'numeric',
                            })}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-4 sm:gap-6">
                        <Badge variant={statusColors[order.status.toLowerCase()] as any}>
                          {order.status}
                        </Badge>
                        <div className="text-right">
                          <p className="font-semibold text-primary">
                            {order.currency || '$'}
                            {(order.total_amount || 0).toFixed(2)}
                          </p>
                          <p className="text-xs text-secondary-text">
                            {order.item_count != null
                              ? `${order.item_count} item${order.item_count !== 1 ? 's' : ''}`
                              : 'View details'}
                          </p>
                        </div>
                        <ArrowRight className="w-5 h-5 text-border hidden sm:block" />
                      </div>
                    </div>
                  </Card>
                </Link>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
