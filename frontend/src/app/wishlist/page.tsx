'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Heart, ShoppingBag, Trash2, ArrowRight } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';

interface WishlistItem {
  id: string;
  product_id: string;
  name?: string;
  price?: number;
  currency?: string;
  image_url?: string;
}

export default function WishlistPage() {
  const [items, setItems] = useState<WishlistItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [retryCount, setRetryCount] = useState(0);

  const fetchWishlist = () => {
    setLoading(true);
    setError('');
    fetch('/api/wishlist')
      .then((res) => res.ok ? res.json() : { items: [] })
      .then((data) => {
        setItems(data.items || []);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load wishlist. Please try again.');
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchWishlist();
  }, [retryCount]);

  const removeItem = async (productId: string) => {
    await fetch(`/api/wishlist/items/${productId}`, { method: 'DELETE' });
    setItems(items.filter((item) => item.product_id !== productId));
  };

  const moveToCart = async (productId: string) => {
    await fetch('/api/cart/items', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: productId, quantity: 1 }),
    });
    removeItem(productId);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="w-full max-w-7xl px-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.from({ length: 3 }).map((_, i) => (
              <Skeleton key={i} className="h-80 w-full" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center px-4">
          <Heart className="w-12 h-12 text-border mx-auto mb-4" />
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
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
        >
          <h1 className="font-serif text-3xl md:text-4xl font-semibold text-primary tracking-tight">
            My Wishlist
          </h1>
          <p className="mt-2 text-secondary-text">
            {items.length > 0
              ? `${items.length} item${items.length !== 1 ? 's' : ''} saved for later`
              : ''}
          </p>
        </motion.div>

        {items.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.25 }}
            className="mt-16 flex flex-col items-center justify-center text-center"
          >
            <div className="w-20 h-20 rounded-full bg-surface flex items-center justify-center mb-6">
              <Heart className="w-10 h-10 text-accent" />
            </div>
            <h2 className="font-serif text-2xl font-semibold text-primary mb-2">
              Your wishlist is empty
            </h2>
            <p className="text-secondary-text mb-8 max-w-sm">
              Save your favorite skincare essentials and come back to them anytime.
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
          <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {items.map((item, index) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.25, delay: index * 0.05 }}
              >
                <Card className="h-full flex flex-col">
                  <div className="aspect-square bg-surface flex items-center justify-center relative overflow-hidden rounded-t-card">
                    {item.image_url ? (
                      <img
                        src={item.image_url}
                        alt={item.name || 'Product'}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="flex flex-col items-center justify-center text-secondary-text">
                        <ShoppingBag className="w-12 h-12 mb-2 opacity-40" />
                        <span className="text-sm">Product Image</span>
                      </div>
                    )}
                  </div>
                  <div className="p-5 flex-1 flex flex-col">
                    <h3 className="font-serif text-lg font-medium text-primary mb-1 truncate">
                      {item.name || `Product ${item.product_id.slice(0, 8)}`}
                    </h3>
                    <p className="text-secondary-text text-sm mb-4">
                      {item.price != null
                        ? `${item.currency || '$'}${item.price.toFixed(2)}`
                        : 'Price unavailable'}
                    </p>
                    <div className="flex gap-2 mt-auto">
                      <Button
                        onClick={() => moveToCart(item.product_id)}
                        className="flex-1"
                        size="sm"
                      >
                        Move to Cart
                      </Button>
                      <Button
                        onClick={() => removeItem(item.product_id)}
                        variant="secondary"
                        size="sm"
                        aria-label="Remove from wishlist"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
