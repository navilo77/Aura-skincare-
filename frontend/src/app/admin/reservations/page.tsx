'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Search, CalendarCheck, CheckCircle2, Clock } from 'lucide-react';
import { AdminLayout } from '@/components/admin/admin-layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

interface Reservation {
  id: string;
  inventory_id: string;
  order_item_id: string;
  quantity: number;
  status: string;
  expires_at: string | null;
  created_at: string;
}

export default function ReservationsPage() {
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const router = useRouter();

  const fetchReservations = () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem('admin_token');
    fetch('/api/admin/reservations', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.ok ? res.json() : [])
      .then((data) => {
        setReservations(Array.isArray(data) ? data : []);
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
    fetchReservations();
  }, [router]);

  const filtered = reservations.filter((r) =>
    r.inventory_id.toLowerCase().includes(search.toLowerCase()) ||
    r.order_item_id.toLowerCase().includes(search.toLowerCase()) ||
    r.status.toLowerCase().includes(search.toLowerCase())
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
            Reservations
          </h1>
          <p className="text-secondary-text mt-1">Track inventory reservations and allocations</p>
        </div>

        <Card className="shadow-soft">
          <div className="p-4 md:p-6 border-b border-border">
            <div className="relative max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-secondary-text" />
              <input
                type="text"
                placeholder="Search reservations..."
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
              <Button onClick={fetchReservations}>Retry</Button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Inventory</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Order Item</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Quantity</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Status</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Expires</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Date</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {filtered.map((reservation, i) => (
                    <motion.tr
                      key={reservation.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.2, delay: i * 0.03 }}
                      className="hover:bg-surface/50 transition-colors duration-150"
                    >
                      <td className="py-4 px-4 md:px-6 text-sm font-medium text-foreground">{reservation.inventory_id}</td>
                      <td className="py-4 px-4 md:px-6 text-sm text-secondary-text font-mono">{reservation.order_item_id}</td>
                      <td className="py-4 px-4 md:px-6 text-sm text-foreground">{reservation.quantity}</td>
                      <td className="py-4 px-4 md:px-6">
                        <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium ${
                          reservation.status === 'active' ? 'bg-success/10 text-success' : 'bg-accent/10 text-accent'
                        }`}>
                          {reservation.status === 'active' ? <CheckCircle2 className="w-3 h-3" /> : <Clock className="w-3 h-3" />}
                          {reservation.status}
                        </span>
                      </td>
                      <td className="py-4 px-4 md:px-6 text-sm text-secondary-text">
                        {reservation.expires_at ? new Date(reservation.expires_at).toLocaleString() : '-'}
                      </td>
                      <td className="py-4 px-4 md:px-6 text-sm text-secondary-text">
                        {new Date(reservation.created_at).toLocaleString()}
                      </td>
                    </motion.tr>
                  ))}
                  {filtered.length === 0 && (
                    <tr>
                      <td colSpan={6} className="py-12 text-center">
                        <p className="text-secondary-text text-sm mb-3">No reservations found</p>
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
