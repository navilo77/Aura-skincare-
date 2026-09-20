'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { Minus, Plus, X, ShoppingBag, ArrowLeft, ShieldCheck, Truck, CreditCard, PackageOpen } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

interface CartItem {
  id: string;
  product_id: string;
  quantity: number;
  unit_price: number;
  subtotal: number;
  product_name?: string;
  thumbnail_url?: string;
  notes?: string;
}

export default function CartPage() {
  const [items, setItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [updatingId, setUpdatingId] = useState<string | null>(null);
  const [error, setError] = useState('');
  const [retryCount, setRetryCount] = useState(0);

  const fetchCart = () => {
    setLoading(true);
    setError('');
    fetch('/api/cart')
      .then((res) => res.ok ? res.json() : { items: [] })
      .then((data) => {
        setItems(data.items || []);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load cart. Please try again.');
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchCart();
  }, [retryCount]);

  const updateQuantity = async (itemId: string, quantity: number) => {
    if (quantity < 1) return;
    setUpdatingId(itemId);
    try {
      const res = await fetch(`/api/cart/items/${itemId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quantity }),
      });
      if (res.ok) {
        const data = await res.json();
        setItems((prev) =>
          prev.map((item) =>
            item.id === itemId
              ? { ...item, quantity: data.quantity || quantity, subtotal: data.subtotal || item.unit_price * quantity }
              : item
          )
        );
      }
    } finally {
      setUpdatingId(null);
    }
  };

  const removeItem = async (itemId: string) => {
    await fetch(`/api/cart/items/${itemId}`, { method: 'DELETE' });
    setItems((prev) => prev.filter((item) => item.id !== itemId));
  };

  const subtotal = items.reduce((sum, item) => sum + item.subtotal, 0);
  const shipping = subtotal > 50 ? 0 : 5.99;
  const tax = subtotal * 0.08;
  const total = subtotal + shipping + tax;

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="w-full max-w-7xl px-4">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 space-y-4">
              {Array.from({ length: 2 }).map((_, i) => (
                <Skeleton key={i} className="h-32 w-full" />
              ))}
            </div>
            <Skeleton className="h-64 w-full" />
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center px-4">
          <ShoppingBag className="w-12 h-12 text-border mx-auto mb-4" />
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
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 lg:py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
          className="mb-8"
        >
          <Link
            href="/products"
            className="inline-flex items-center text-secondary-text hover:text-accent transition-colors mb-4 text-sm"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Continue Shopping
          </Link>
          <h1 className="font-serif text-4xl md:text-5xl font-semibold tracking-tight text-primary">
            Shopping Cart
          </h1>
          {items.length > 0 && (
            <p className="mt-2 text-secondary-text">
              {items.length} {items.length === 1 ? 'item' : 'items'} in your cart
            </p>
          )}
        </motion.div>

        {items.length === 0 ? (
          /* Empty Cart */
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.25 }}
            className="bg-surface border border-border rounded-card p-12 text-center max-w-2xl mx-auto shadow-soft"
          >
            <div className="w-20 h-20 bg-background rounded-full flex items-center justify-center mx-auto mb-6">
              <PackageOpen className="w-10 h-10 text-accent" />
            </div>
            <h2 className="font-serif text-2xl font-semibold mb-3">Your cart is empty</h2>
            <p className="text-secondary-text mb-8 max-w-md mx-auto">
              Looks like you haven&apos;t added any products yet. Explore our collection and find your perfect skincare match.
            </p>
            <Link href="/products">
              <Button size="lg">Browse Products</Button>
            </Link>
          </motion.div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Cart Items */}
            <div className="lg:col-span-2 space-y-4">
              <AnimatePresence mode="popLayout">
                {items.map((item, index) => (
                  <motion.div
                    key={item.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, x: -50, transition: { duration: 0.2 } }}
                    transition={{ duration: 0.25, delay: index * 0.05 }}
                    className="bg-surface border border-border rounded-card p-6 shadow-soft"
                  >
                    <div className="flex flex-col sm:flex-row gap-6">
                      {/* Product Image */}
                      <Link href={`/products/${item.product_id}`} className="flex-shrink-0">
                        <div className="w-full sm:w-24 h-24 bg-background rounded-button overflow-hidden flex items-center justify-center border border-border">
                          {item.thumbnail_url ? (
                            <img
                              src={item.thumbnail_url}
                              alt={item.product_name || 'Product'}
                              className="w-full h-full object-cover"
                            />
                          ) : (
                            <ShoppingBag className="w-8 h-8 text-accent opacity-60" />
                          )}
                        </div>
                      </Link>

                      {/* Product Details */}
                      <div className="flex-1 min-w-0">
                        <div className="flex flex-col sm:flex-row sm:justify-between gap-4">
                          <div className="flex-1">
                            <Link
                              href={`/products/${item.product_id}`}
                              className="font-serif text-lg font-semibold text-primary hover:text-accent transition-colors line-clamp-1"
                            >
                              {item.product_name || `Product ${item.product_id.slice(0, 8)}`}
                            </Link>
                            <p className="text-secondary-text text-sm mt-1">
                              ${item.unit_price.toFixed(2)}
                            </p>
                          </div>

                          <div className="flex items-center gap-6">
                            {/* Quantity */}
                            <div className="flex items-center border border-border rounded-button overflow-hidden bg-background">
                              <button
                                onClick={() => updateQuantity(item.id, item.quantity - 1)}
                                disabled={updatingId === item.id || item.quantity <= 1}
                                className="p-2 hover:bg-surface transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                aria-label={`Decrease quantity of ${item.product_name || 'item'}`}
                              >
                                <Minus className="w-4 h-4" />
                              </button>
                              <span className="px-4 py-2 text-sm font-medium min-w-[3rem] text-center">
                                {item.quantity}
                              </span>
                              <button
                                onClick={() => updateQuantity(item.id, item.quantity + 1)}
                                disabled={updatingId === item.id}
                                className="p-2 hover:bg-surface transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                aria-label={`Increase quantity of ${item.product_name || 'item'}`}
                              >
                                <Plus className="w-4 h-4" />
                              </button>
                            </div>

                            {/* Subtotal */}
                            <div className="text-right min-w-[5rem]">
                              <p className="font-serif text-lg font-semibold text-primary">
                                ${item.subtotal.toFixed(2)}
                              </p>
                            </div>
                          </div>
                        </div>

                        {/* Notes & Remove */}
                        <div className="mt-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                          <input
                            type="text"
                            placeholder="Add a note for this item (optional)"
                            defaultValue={item.notes}
                            className="w-full sm:w-80 px-3 py-2 bg-background border border-border rounded-input text-sm text-primary placeholder-secondary-text focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all"
                          />
                          <button
                            onClick={() => removeItem(item.id)}
                            className="inline-flex items-center text-sm text-secondary-text hover:text-error transition-colors"
                            aria-label={`Remove ${item.product_name || 'item'} from cart`}
                          >
                            <X className="w-4 h-4 mr-1.5" />
                            Remove
                          </button>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>

            {/* Order Summary Sidebar */}
            <div className="lg:col-span-1">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.25, delay: 0.1 }}
                className="bg-surface border border-border rounded-card p-6 shadow-soft sticky top-24"
              >
                <h2 className="font-serif text-2xl font-semibold mb-6">Order Summary</h2>

                <div className="space-y-4 mb-6">
                  <div className="flex justify-between text-secondary-text">
                    <span>Subtotal</span>
                    <span>${subtotal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-secondary-text">
                    <span>Shipping</span>
                    <span>
                      {shipping === 0 ? (
                          <span className="text-success font-medium">FREE</span>
                      ) : (
                        `$${shipping.toFixed(2)}`
                      )}
                    </span>
                  </div>
                  <div className="flex justify-between text-secondary-text">
                    <span>Estimated Tax</span>
                    <span>${tax.toFixed(2)}</span>
                  </div>
                  <div className="border-t border-border pt-4 flex justify-between text-primary font-semibold text-lg">
                    <span>Total</span>
                    <span>${total.toFixed(2)}</span>
                  </div>
                </div>

                <Link href="/checkout" className="block">
                  <Button className="w-full" size="lg">
                    Proceed to Checkout
                  </Button>
                </Link>

                {/* Trust Badges */}
                <div className="mt-8 pt-6 border-t border-border">
                  <div className="grid grid-cols-1 gap-3">
                    <div className="flex items-center text-sm text-secondary-text">
                      <ShieldCheck className="w-5 h-5 text-accent mr-3 flex-shrink-0" />
                      Secure Checkout
                    </div>
                    <div className="flex items-center text-sm text-secondary-text">
                      <Truck className="w-5 h-5 text-accent mr-3 flex-shrink-0" />
                      Free shipping over $50
                    </div>
                    <div className="flex items-center text-sm text-secondary-text">
                      <CreditCard className="w-5 h-5 text-accent mr-3 flex-shrink-0" />
                      All major cards accepted
                    </div>
                  </div>
                </div>
              </motion.div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
