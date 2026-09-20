'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Search, ClipboardList, Eye } from 'lucide-react';
import { AdminLayout } from '@/components/admin/admin-layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

interface Order {
  id: string;
  customer_id: string;
  total: number;
  status: string;
  created_at: string;
}

export default function AdminOrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const router = useRouter();

  const fetchOrders = () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem('admin_token');
    fetch('/api/admin/dashboard', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.ok ? res.json() : {})
      .then(() => {
        setOrders([]);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    const token = localStorage.getItem('admin_token');
    if (!token) {
      router.push('/admin/login');
      return;
    }
    fetchOrders();
  }, [router]);

  const filtered = orders.filter((o) =>
    o.id.toLowerCase().includes(search.toLowerCase()) ||
    o.customer_id.toLowerCase().includes(search.toLowerCase()) ||
    o.status.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <AdminLayout>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.25 }}
        className="space-y-6"
      >
        <div>
          <h1 className="font-serif text-3xl md:text-4xl font-semibold text-foreground tracking-tight">
            Orders
          </h1>
          <p className="text-secondary-text mt-1">View and manage customer orders</p>
        </div>

        <Card className="shadow-soft">
          <div className="p-4 md:p-6 border-b border-border">
            <div className="relative max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-secondary-text" />
              <input
                type="text"
                placeholder="Search orders..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="input-field pl-10"
              />
            </div>
          </div>

          {loading ? (
            <div className="p-6 space-y-4">
              {[...Array(5)].map((_, i) => (
                <Skeleton key={i} className="h-12 w-full" />
              ))}
            </div>
          ) : error ? (
            <div className="p-6 text-center">
              <p className="text-secondary-text mb-4">{error}</p>
              <Button onClick={fetchOrders}>Retry</Button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Order ID</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Customer</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Total</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Status</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Date</th>
                    <th className="text-right py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {filtered.map((order, i) => (
                    <motion.tr
                      key={order.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.2, delay: i * 0.03 }}
                      className="hover:bg-surface/50 transition-colors duration-150"
                    >
                      <td className="py-4 px-4 md:px-6 text-sm font-medium text-foreground font-mono">{order.id}</td>
                      <td className="py-4 px-4 md:px-6 text-sm text-secondary-text">{order.customer_id}</td>
                      <td className="py-4 px-4 md:px-6 text-sm text-foreground">${order.total.toFixed(2)}</td>
                      <td className="py-4 px-4 md:px-6">
                        <span className={`inline-flex px-2.5 py-1 rounded-lg text-xs font-medium capitalize ${
                          order.status === 'delivered' ? 'bg-success/10 text-success' :
                          order.status === 'pending' ? 'bg-accent/10 text-accent' :
                          'bg-error/10 text-error'
                        }`}>
                          {order.status}
                        </span>
                      </td>
                      <td className="py-4 px-4 md:px-6 text-sm text-secondary-text">
                        {new Date(order.created_at).toLocaleDateString()}
                      </td>
                      <td className="py-4 px-4 md:px-6">
                        <div className="flex items-center justify-end gap-2">
                          <button className="p-2 rounded-lg hover:bg-surface text-secondary-text hover:text-foreground transition-colors duration-150" aria-label="View order details">
                            <Eye className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </motion.tr>
                  ))}
                  {filtered.length === 0 && (
                    <tr>
                      <td colSpan={6} className="py-12 text-center">
                        <p className="text-secondary-text text-sm mb-3">No orders found</p>
                        <Button size="sm" onClick={() => setSearch('')}>Clear Search</Button>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </Card>
      </motion.div>
    </AdminLayout>
  );
}
