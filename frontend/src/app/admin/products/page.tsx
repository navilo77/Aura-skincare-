'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Search, Plus, Edit, Trash2, Eye } from 'lucide-react';
import { AdminLayout } from '@/components/admin/admin-layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

import { Product } from "@/lib/services/product.service";

export default function AdminProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const router = useRouter();

  const fetchProducts = () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem('admin_token');
    fetch('/api/products', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.ok ? res.json() : [])
      .then((data) => {
        setProducts(Array.isArray(data) ? data : []);
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
    fetchProducts();
  }, [router]);

  const filtered = products.filter((p) =>
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    p.sku.toLowerCase().includes(search.toLowerCase())
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
              Products
            </h1>
            <p className="text-secondary-text mt-1">Manage your product catalog</p>
          </div>
          <Button variant="primary" className="inline-flex items-center gap-2">
            <Plus className="w-4 h-4" />
            Add Product
          </Button>
        </div>

        <Card className="shadow-soft">
          <div className="p-4 md:p-6 border-b border-border">
            <div className="relative max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-secondary-text" />
              <input
                type="text"
                placeholder="Search products..."
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
              <Button onClick={fetchProducts}>Retry</Button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Name</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">SKU</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Price</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Status</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Active</th>
                    <th className="text-right py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {filtered.map((product, i) => (
                    <motion.tr
                      key={product.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.2, delay: i * 0.03 }}
                      className="hover:bg-surface/50 transition-colors duration-150"
                    >
                      <td className="py-4 px-4 md:px-6 text-sm font-medium text-foreground">{product.name}</td>
                      <td className="py-4 px-4 md:px-6 text-sm text-secondary-text font-mono">{product.sku}</td>
                      <td className="py-4 px-4 md:px-6 text-sm text-foreground">${product.price.toFixed(2)}</td>
                      <td className="py-4 px-4 md:px-6">
                        <span className={`inline-flex px-2.5 py-1 rounded-lg text-xs font-medium ${
                          product.status === 'active' ? 'bg-success/10 text-success' : 'bg-error/10 text-error'
                        }`}>
                          {product.status}
                        </span>
                      </td>
                      <td className="py-4 px-4 md:px-6 text-sm text-secondary-text">{product.is_active ? 'Yes' : 'No'}</td>
                      <td className="py-4 px-4 md:px-6">
                        <div className="flex items-center justify-end gap-2">
                          <button className="p-2 rounded-lg hover:bg-surface text-secondary-text hover:text-foreground transition-colors duration-150" aria-label="View product">
                            <Eye className="w-4 h-4" />
                          </button>
                          <button className="p-2 rounded-lg hover:bg-surface text-secondary-text hover:text-foreground transition-colors duration-150" aria-label="Edit product">
                            <Edit className="w-4 h-4" />
                          </button>
                          <button className="p-2 rounded-lg hover:bg-error/10 text-secondary-text hover:text-error transition-colors duration-150" aria-label="Delete product">
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </motion.tr>
                  ))}
                  {filtered.length === 0 && (
                    <tr>
                      <td colSpan={6} className="py-12 text-center">
                        <p className="text-secondary-text text-sm mb-3">No products found</p>
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
