'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { User, Package, Heart, ArrowRight, Settings, Shield, MapPin } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';

interface Profile {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  is_verified: boolean;
}

interface Order {
  id: string;
  order_number: string;
  status: string;
  total_amount: number;
  currency: string;
  created_at: string;
}

interface Address {
  id: string;
  address_line1: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  is_default: boolean;
}

const quickLinks = [
  { href: '/profile/edit', label: 'Edit Profile', icon: Settings },
  { href: '/profile/addresses', label: 'Addresses', icon: MapPin },
  { href: '/profile/change-password', label: 'Change Password', icon: Shield },
  { href: '/profile/orders', label: 'Orders', icon: Package },
  { href: '/wishlist', label: 'Wishlist', icon: Heart },
];

const statusColors: Record<string, string> = {
  pending: 'default',
  confirmed: 'default',
  processing: 'default',
  shipped: 'default',
  delivered: 'success',
  cancelled: 'error',
};

export default function ProfilePage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [orders, setOrders] = useState<Order[]>([]);
  const [addresses, setAddresses] = useState<Address[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [retryCount, setRetryCount] = useState(0);

  const fetchProfileData = () => {
    setLoading(true);
    setError('');
    Promise.all([
      fetch('/api/profile').then((res) => res.ok ? res.json() : null),
      fetch('/api/profile/orders').then((res) => res.ok ? res.json() : []),
      fetch('/api/profile/addresses').then((res) => res.ok ? res.json() : []),
    ])
      .then(([profileData, ordersData, addressesData]) => {
        setProfile(profileData);
        setOrders(Array.isArray(ordersData) ? ordersData : []);
        setAddresses(Array.isArray(addressesData) ? addressesData : []);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load profile data. Please try again.');
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchProfileData();
  }, [retryCount]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="w-full max-w-2xl space-y-4 px-4">
          <Skeleton className="h-10 w-48 mx-auto" />
          <Skeleton className="h-32 w-full" />
          <div className="grid grid-cols-2 gap-4">
            <Skeleton className="h-24 w-full" />
            <Skeleton className="h-24 w-full" />
          </div>
          <Skeleton className="h-48 w-full" />
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center px-4">
          <User className="w-12 h-12 text-border mx-auto mb-4" />
          <p className="text-secondary-text mb-4">Please log in to view your profile.</p>
          <Button onClick={() => (window.location.href = '/auth/login')} variant="primary">
            Go to Login
          </Button>
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

  const recentOrders = orders.slice(0, 3);

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
        >
          <h1 className="font-serif text-3xl md:text-4xl font-semibold text-primary tracking-tight">
            My Account
          </h1>
        </motion.div>

        <div className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.25, delay: 0.05 }}
            >
              <Card className="bg-gradient-to-br from-surface to-background">
                <div className="flex items-start gap-4">
                  <div className="w-14 h-14 rounded-full bg-accent/10 flex items-center justify-center flex-shrink-0">
                    <User className="w-7 h-7 text-accent" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h2 className="font-serif text-xl font-semibold text-primary">
                      Welcome back, {profile.full_name?.split(' ')[0] || 'there'}
                    </h2>
                    <p className="text-secondary-text text-sm mt-1 truncate">
                      {profile.email}
                    </p>
                    {profile.is_verified && (
                      <Badge variant="success" className="mt-2">Verified Account</Badge>
                    )}
                  </div>
                </div>
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.25, delay: 0.1 }}
            >
              <div className="grid grid-cols-2 gap-4">
                <Card hover className="cursor-pointer" onClick={() => (window.location.href = '/profile/orders')}>
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-accent/10 flex items-center justify-center">
                      <Package className="w-5 h-5 text-accent" />
                    </div>
                    <div>
                      <p className="text-2xl font-serif font-semibold text-primary">
                        {orders.length}
                      </p>
                      <p className="text-sm text-secondary-text">Orders</p>
                    </div>
                  </div>
                </Card>
                <Card hover className="cursor-pointer" onClick={() => (window.location.href = '/wishlist')}>
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-accent/10 flex items-center justify-center">
                      <Heart className="w-5 h-5 text-accent" />
                    </div>
                    <div>
                      <p className="text-2xl font-serif font-semibold text-primary">
                        {addresses.length}
                      </p>
                      <p className="text-sm text-secondary-text">Addresses</p>
                    </div>
                  </div>
                </Card>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.25, delay: 0.15 }}
            >
              <Card>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-serif text-xl font-semibold text-primary">
                    Recent Orders
                  </h3>
                  {orders.length > 3 && (
                    <Link
                      href="/profile/orders"
                      className="text-sm text-accent hover:text-accent-dark flex items-center transition-colors"
                    >
                      View all
                      <ArrowRight className="ml-1 w-4 h-4" />
                    </Link>
                  )}
                </div>
                {recentOrders.length === 0 ? (
                  <div className="text-center py-8">
                    <Package className="w-10 h-10 text-border mx-auto mb-3" />
                    <p className="text-secondary-text text-sm">No orders yet</p>
                    <Link
                      href="/products"
                      className="inline-block mt-4 text-sm text-accent hover:text-accent-dark transition-colors"
                    >
                      Start shopping
                    </Link>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {recentOrders.map((order) => (
                      <Link
                        key={order.id}
                        href={`/profile/orders/${order.id}`}
                        className="flex items-center justify-between p-4 bg-surface rounded-button hover:bg-border/30 transition-colors"
                      >
                        <div className="flex items-center gap-3 min-w-0">
                          <div className="w-10 h-10 rounded-full bg-background flex items-center justify-center flex-shrink-0">
                            <Package className="w-5 h-5 text-secondary-text" />
                          </div>
                          <div className="min-w-0">
                            <p className="font-medium text-primary text-sm truncate">
                              {order.order_number}
                            </p>
                            <p className="text-xs text-secondary-text">
                              {new Date(order.created_at).toLocaleDateString('en-US', {
                                month: 'short',
                                day: 'numeric',
                                year: 'numeric',
                              })}
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center gap-3 flex-shrink-0">
                          <Badge variant={statusColors[order.status.toLowerCase()] as any}>
                            {order.status}
                          </Badge>
                          <span className="text-sm font-medium text-primary">
                            {order.currency || '$'}
                            {(order.total_amount || 0).toFixed(2)}
                          </span>
                        </div>
                      </Link>
                    ))}
                  </div>
                )}
              </Card>
            </motion.div>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, delay: 0.2 }}
            className="lg:col-span-1"
          >
            <Card>
              <h3 className="font-serif text-xl font-semibold text-primary mb-4">
                Quick Links
              </h3>
              <div className="space-y-2">
                {quickLinks.map((link) => (
                  <Link
                    key={link.href}
                    href={link.href}
                    className="flex items-center gap-3 p-3 rounded-button hover:bg-surface transition-colors group"
                  >
                    <div className="w-10 h-10 rounded-full bg-surface flex items-center justify-center group-hover:bg-accent/10 transition-colors">
                      <link.icon className="w-5 h-5 text-secondary-text group-hover:text-accent transition-colors" />
                    </div>
                    <span className="text-sm font-medium text-primary group-hover:text-accent transition-colors">
                      {link.label}
                    </span>
                    <ArrowRight className="w-4 h-4 text-border ml-auto group-hover:text-accent transition-colors" />
                  </Link>
                ))}
              </div>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
