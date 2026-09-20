'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowLeft, Package, MapPin, CreditCard, Truck, CheckCircle } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';

interface OrderItem {
  id: string;
  product_id: string;
  product_name?: string;
  quantity: number;
  unit_price: number;
  total_price: number;
  image_url?: string;
}

interface OrderDetail {
  id: string;
  order_number: string;
  status: string;
  total_amount: number;
  currency: string;
  created_at: string;
  shipping_address?: {
    address_line1: string;
    address_line2?: string;
    city: string;
    state: string;
    postal_code: string;
    country: string;
  };
  items: OrderItem[];
}

const statusSteps = ['pending', 'confirmed', 'processing', 'shipped', 'delivered'];

const statusColors: Record<string, string> = {
  pending: 'default',
  confirmed: 'default',
  processing: 'default',
  shipped: 'default',
  delivered: 'success',
  cancelled: 'error',
};

export default function OrderDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [order, setOrder] = useState<OrderDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [retryCount, setRetryCount] = useState(0);

  const fetchOrder = () => {
    setLoading(true);
    setError('');
    fetch(`/api/profile/orders/${params.id}`)
      .then((res) => res.ok ? res.json() : null)
      .then((data) => {
        setOrder(data);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load order details. Please try again.');
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchOrder();
  }, [params.id, retryCount]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="w-full max-w-4xl space-y-4 px-4">
          <Skeleton className="h-10 w-48" />
          <Skeleton className="h-32 w-full" />
          <Skeleton className="h-64 w-full" />
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

  if (!order) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <Package className="w-12 h-12 text-border mx-auto mb-4" />
          <p className="text-secondary-text mb-4">Order not found</p>
          <Link
            href="/profile/orders"
            className="inline-flex items-center text-accent hover:text-accent-dark transition-colors"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to orders
          </Link>
        </div>
      </div>
    );
  }

  const currentStatusIndex = statusSteps.indexOf(order.status.toLowerCase());

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
          className="mb-8"
        >
          <Link
            href="/profile/orders"
            className="inline-flex items-center text-secondary-text hover:text-accent transition-colors mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to orders
          </Link>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h1 className="font-serif text-3xl md:text-4xl font-semibold text-primary tracking-tight">
                Order {order.order_number}
              </h1>
              <p className="text-secondary-text mt-1">
                Placed on{' '}
                {new Date(order.created_at).toLocaleDateString('en-US', {
                  month: 'long',
                  day: 'numeric',
                  year: 'numeric',
                })}
              </p>
            </div>
            <span
              className={`inline-block px-4 py-2 rounded-full text-sm font-medium w-fit`}
            >
              <Badge variant={statusColors[order.status.toLowerCase()] as any}>
                {order.status}
              </Badge>
            </span>
          </div>
        </motion.div>

        {currentStatusIndex >= 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, delay: 0.05 }}
            className="mb-8"
          >
            <Card>
              <h3 className="font-serif text-lg font-semibold text-primary mb-6">
                Order Status
              </h3>
              <div className="flex items-center justify-between">
                {statusSteps.map((step, index) => (
                  <div key={step} className="flex flex-col items-center flex-1">
                    <div
                      className={`w-10 h-10 rounded-full flex items-center justify-center mb-2 transition-colors ${
                        index <= currentStatusIndex
                          ? 'bg-accent text-white'
                          : 'bg-surface text-secondary-text'
                      }`}
                    >
                      {index <= currentStatusIndex ? (
                        <CheckCircle className="w-5 h-5" />
                      ) : (
                        <span className="text-xs font-medium">{index + 1}</span>
                      )}
                    </div>
                    <span
                      className={`text-xs font-medium capitalize ${
                        index <= currentStatusIndex ? 'text-accent' : 'text-secondary-text'
                      }`}
                    >
                      {step}
                    </span>
                  </div>
                ))}
              </div>
              <div className="mt-4 h-1 bg-surface rounded-full overflow-hidden">
                <div
                  className="h-full bg-accent rounded-full transition-all duration-500"
                  style={{ width: `${((currentStatusIndex + 1) / statusSteps.length) * 100}%` }}
                />
              </div>
            </Card>
          </motion.div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.25, delay: 0.1 }}
            >
              <Card>
                <h3 className="font-serif text-lg font-semibold text-primary mb-4 flex items-center gap-2">
                  <Package className="w-5 h-5 text-accent" />
                  Order Items
                </h3>
                <div className="space-y-4">
                  {order.items?.map((item) => (
                    <div
                      key={item.id}
                      className="flex items-center gap-4 p-4 bg-surface rounded-button"
                    >
                      <div className="w-16 h-16 bg-background rounded-lg flex items-center justify-center flex-shrink-0 overflow-hidden">
                        {item.image_url ? (
                          <img
                            src={item.image_url}
                            alt={item.product_name || 'Product'}
                            className="w-full h-full object-cover"
                          />
                        ) : (
                          <Package className="w-6 h-6 text-border" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-primary text-sm truncate">
                          {item.product_name || `Product ${item.product_id.slice(0, 8)}`}
                        </p>
                        <p className="text-xs text-secondary-text mt-1">
                          Qty: {item.quantity} x {order.currency || '$'}
                          {(item.unit_price || 0).toFixed(2)}
                        </p>
                      </div>
                      <p className="font-semibold text-primary text-sm flex-shrink-0">
                        {order.currency || '$'}
                        {(item.total_price || 0).toFixed(2)}
                      </p>
                    </div>
                  ))}
                </div>
                <div className="mt-4 pt-4 border-t border-border flex justify-between items-center">
                  <span className="text-secondary-text">Total</span>
                  <span className="font-serif text-xl font-semibold text-primary">
                    {order.currency || '$'}
                    {(order.total_amount || 0).toFixed(2)}
                  </span>
                </div>
              </Card>
            </motion.div>
          </div>

          <div className="space-y-6">
            {order.shipping_address && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.25, delay: 0.15 }}
              >
                <Card>
                  <h3 className="font-serif text-lg font-semibold text-primary mb-3 flex items-center gap-2">
                    <MapPin className="w-5 h-5 text-accent" />
                    Shipping Address
                  </h3>
                  <div className="text-sm text-secondary-text space-y-1">
                    <p>{order.shipping_address.address_line1}</p>
                    {order.shipping_address.address_line2 && (
                      <p>{order.shipping_address.address_line2}</p>
                    )}
                    <p>
                      {order.shipping_address.city}, {order.shipping_address.state}{' '}
                      {order.shipping_address.postal_code}
                    </p>
                    <p>{order.shipping_address.country}</p>
                  </div>
                </Card>
              </motion.div>
            )}

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.25, delay: 0.2 }}
            >
              <Card>
                <h3 className="font-serif text-lg font-semibold text-primary mb-3 flex items-center gap-2">
                  <CreditCard className="w-5 h-5 text-accent" />
                  Order Summary
                </h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between text-secondary-text">
                    <span>Subtotal</span>
                    <span>
                      {order.currency || '$'}
                      {(order.total_amount || 0).toFixed(2)}
                    </span>
                  </div>
                  <div className="flex justify-between text-secondary-text">
                    <span>Shipping</span>
                    <span>Free</span>
                  </div>
                  <div className="pt-2 border-t border-border flex justify-between font-semibold text-primary">
                    <span>Total</span>
                    <span>
                      {order.currency || '$'}
                      {(order.total_amount || 0).toFixed(2)}
                    </span>
                  </div>
                </div>
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.25, delay: 0.25 }}
            >
              <Card>
                <h3 className="font-serif text-lg font-semibold text-primary mb-3 flex items-center gap-2">
                  <Truck className="w-5 h-5 text-accent" />
                  Shipping Info
                </h3>
                <div className="space-y-2 text-sm text-secondary-text">
                  <p>Standard Shipping</p>
                  <p>Free shipping on all orders</p>
                  <p className="text-xs">
                    Estimated delivery:{' '}
                    {new Date(order.created_at).toLocaleDateString('en-US', {
                      month: 'long',
                      day: 'numeric',
                      year: 'numeric',
                    })}
                  </p>
                </div>
              </Card>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
