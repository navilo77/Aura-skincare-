'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Warehouse, TrendingUp, TrendingDown, ArrowUpRight } from 'lucide-react';
import { AdminLayout } from '@/components/admin/admin-layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

interface InventoryTransaction {
  id: string;
  product_id: string;
  warehouse_id: string;
  quantity_change: number;
  transaction_type: string;
  reference_type: string | null;
  reference_id: string | null;
  notes: string | null;
  performed_by: string | null;
  created_at: string;
}

export default function InventoryDashboardPage() {
  const [transactions, setTransactions] = useState<InventoryTransaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const fetchTransactions = () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem('admin_token');
    fetch('/api/admin/inventory-dashboard', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.ok ? res.json() : [])
      .then((data) => {
        setTransactions(Array.isArray(data) ? data : []);
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
    fetchTransactions();
  }, [router]);

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
            Inventory Dashboard
          </h1>
          <p className="text-secondary-text mt-1">Monitor stock movements and warehouse activity</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6">
          {[
            { title: 'Total Transactions', value: transactions.length.toString(), icon: Warehouse },
            { title: 'Inbound', value: transactions.filter(t => t.quantity_change > 0).length.toString(), icon: TrendingUp },
            { title: 'Outbound', value: transactions.filter(t => t.quantity_change < 0).length.toString(), icon: TrendingDown },
          ].map((stat, i) => {
            const Icon = stat.icon;
            return (
              <Card className="shadow-soft">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center text-accent">
                    <Icon className="w-6 h-6" />
                  </div>
                  <div>
                    <p className="text-secondary-text text-sm">{stat.title}</p>
                    <p className="font-serif text-2xl font-semibold text-foreground">{stat.value}</p>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>

        <Card className="shadow-soft">
          <div className="p-4 md:p-6 border-b border-border">
            <h2 className="font-serif text-xl font-semibold text-foreground">Recent Transactions</h2>
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
              <Button onClick={fetchTransactions}>Retry</Button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Product</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Warehouse</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Change</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Type</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Date</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {transactions.map((tx, i) => (
                    <motion.tr
                      key={tx.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.2, delay: i * 0.03 }}
                      className="hover:bg-surface/50 transition-colors duration-150"
                    >
                      <td className="py-4 px-4 md:px-6 text-sm font-medium text-foreground">{tx.product_id}</td>
                      <td className="py-4 px-4 md:px-6 text-sm text-secondary-text">{tx.warehouse_id}</td>
                      <td className={`py-4 px-4 md:px-6 text-sm font-medium ${tx.quantity_change > 0 ? 'text-success' : 'text-error'}`}>
                        {tx.quantity_change > 0 ? '+' : ''}{tx.quantity_change}
                      </td>
                      <td className="py-4 px-4 md:px-6 text-sm text-secondary-text">{tx.transaction_type}</td>
                      <td className="py-4 px-4 md:px-6 text-sm text-secondary-text">
                        {new Date(tx.created_at).toLocaleString()}
                      </td>
                    </motion.tr>
                  ))}
                  {transactions.length === 0 && (
                    <tr>
                      <td colSpan={5} className="py-12 text-center">
                        <p className="text-secondary-text text-sm mb-3">No transactions found</p>
                        <Button size="sm" onClick={fetchTransactions}>Retry</Button>
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
