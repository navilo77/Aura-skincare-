'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Search, TicketPercent, Plus, Edit, Trash2, Eye } from 'lucide-react';
import { AdminLayout } from '@/components/admin/admin-layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

interface Coupon {
  id: string;
  code: string;
  discount_type: string;
  discount_value: number;
  is_active: boolean;
  starts_at: string;
  expires_at: string;
}

export default function AdminCouponsPage() {
  const [coupons, setCoupons] = useState<Coupon[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const router = useRouter();

  const fetchCoupons = () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem('admin_token');
    fetch('/api/admin/coupons', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.ok ? res.json() : [])
      .then((data) => {
        setCoupons(Array.isArray(data) ? data : []);
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
    fetchCoupons();
  }, [router]);

  const filtered = coupons.filter((c) =>
    c.code.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <AdminLayout>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.25 }}
        className="space-y-6"
      >
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="font-serif text-3xl md:text-4xl font-semibold text-foreground tracking-tight">
              Coupons
            </h1>
            <p className="text-secondary-text mt-1">Manage discount codes and promotions</p>
          </div>
          <Button variant="primary" className="inline-flex items-center gap-2">
            <Plus className="w-4 h-4" />
            Add Coupon
          </Button>
        </div>

        <Card className="shadow-soft">
          <div className="p-4 md:p-6 border-b border-border">
            <div className="relative max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-secondary-text" />
              <input
                type="text"
                placeholder="Search coupons..."
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
              <Button onClick={fetchCoupons}>Retry</Button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Code</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Type</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Value</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Active</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Expires</th>
                    <th className="text-right py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {filtered.map((coupon, i) => (
                    <motion.tr
                      key={coupon.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.2, delay: i * 0.03 }}
                      className="hover:bg-surface/50 transition-colors duration-150"
                    >
                      <td className="py-4 px-4 md:px-6 text-sm font-medium text-foreground font-mono">{coupon.code}</td>
                      <td className="py-4 px-4 md:px-6 text-sm text-secondary-text capitalize">{coupon.discount_type}</td>
                      <td className="py-4 px-4 md:px-6 text-sm text-foreground">
                        {coupon.discount_type === 'percentage' ? `${coupon.discount_value}%` : `$${coupon.discount_value}`}
                      </td>
                      <td className="py-4 px-4 md:px-6">
                        <span className={`inline-flex px-2.5 py-1 rounded-lg text-xs font-medium ${
                          coupon.is_active ? 'bg-success/10 text-success' : 'bg-error/10 text-error'
                        }`}>
                          {coupon.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td className="py-4 px-4 md:px-6 text-sm text-secondary-text">
                        {new Date(coupon.expires_at).toLocaleDateString()}
                      </td>
                      <td className="py-4 px-4 md:px-6">
                        <div className="flex items-center justify-end gap-2">
                          <button className="p-2 rounded-lg hover:bg-surface text-secondary-text hover:text-foreground transition-colors duration-150" aria-label="View coupon">
                            <Eye className="w-4 h-4" />
                          </button>
                          <button className="p-2 rounded-lg hover:bg-surface text-secondary-text hover:text-foreground transition-colors duration-150" aria-label="Edit coupon">
                            <Edit className="w-4 h-4" />
                          </button>
                          <button className="p-2 rounded-lg hover:bg-error/10 text-secondary-text hover:text-error transition-colors duration-150" aria-label="Delete coupon">
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </motion.tr>
                  ))}
                  {filtered.length === 0 && (
                    <tr>
                      <td colSpan={6} className="py-12 text-center">
                        <p className="text-secondary-text text-sm mb-3">No coupons found</p>
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
