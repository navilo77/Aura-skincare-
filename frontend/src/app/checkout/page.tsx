'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { Check, ChevronRight, ShieldCheck, Truck, CreditCard, ShoppingBag, ArrowLeft } from 'lucide-react';
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
}

const STEPS = ['Shipping', 'Review', 'Confirmation'];

export default function CheckoutPage() {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [step, setStep] = useState(1);
  const [orderNumber, setOrderNumber] = useState('');
  const [error, setError] = useState('');
  const [retryCount, setRetryCount] = useState(0);

  const [address, setAddress] = useState({
    address_line1: '',
    address_line2: '',
    city: '',
    state: '',
    postal_code: '',
    country: 'US',
    phone: '',
  });

  const [coupon, setCoupon] = useState('');

  const fetchCart = () => {
    setLoading(true);
    setError('');
    fetch('/api/cart')
      .then((res) => res.ok ? res.json() : { items: [] })
      .then((data) => {
        setCartItems(data.items || []);
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

  const subtotal = cartItems.reduce((sum, item) => sum + item.subtotal, 0);
  const shipping = subtotal > 50 ? 0 : 5.99;
  const tax = subtotal * 0.08;
  const total = subtotal + shipping + tax;

  const handleShippingSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setStep(2);
  };

  const handlePlaceOrder = async () => {
    setSubmitting(true);
    setError('');
    try {
      const res = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          shipping_address: address,
          items: cartItems.map((item) => ({ product_id: item.product_id, quantity: item.quantity })),
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setOrderNumber(data.order_number || '');
        setStep(3);
      } else {
        const data = await res.json().catch(() => ({}));
        setError(data.detail || data.message || 'Failed to place order. Please try again.');
      }
    } catch {
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="w-full max-w-7xl px-4">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 space-y-4">
              <Skeleton className="h-8 w-32" />
              <Skeleton className="h-64 w-full" />
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
          <Link href="/cart" className="inline-flex items-center text-secondary-text hover:text-accent transition-colors mb-4 text-sm">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Cart
          </Link>
          <h1 className="font-serif text-4xl md:text-5xl font-semibold tracking-tight text-primary">
            Checkout
          </h1>
        </motion.div>

        {/* Progress Indicator */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25, delay: 0.05 }}
          className="mb-12"
        >
          <div className="flex items-center justify-center">
            {STEPS.map((label, idx) => (
              <div key={label} className="flex items-center">
                <div className="flex items-center">
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium transition-all duration-200 ${
                      step > idx + 1
                        ? 'bg-accent text-white'
                        : step === idx + 1
                        ? 'bg-accent text-white shadow-lg shadow-accent/30'
                        : 'bg-surface border border-border text-secondary-text'
                    }`}
                  >
                    {step > idx + 1 ? <Check className="w-5 h-5" /> : idx + 1}
                  </div>
                  <span
                    className={`ml-3 text-sm font-medium hidden sm:block ${
                      step >= idx + 1 ? 'text-primary' : 'text-secondary-text'
                    }`}
                  >
                    {label}
                  </span>
                </div>
                {idx < STEPS.length - 1 && (
                  <div
                    className={`w-12 sm:w-20 h-0.5 mx-4 transition-all duration-300 ${
                      step > idx + 1 ? 'bg-accent' : 'bg-border'
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
        </motion.div>

        {cartItems.length === 0 && step < 3 ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.25 }}
            className="bg-surface border border-border rounded-card p-12 text-center max-w-2xl mx-auto shadow-soft"
          >
            <div className="w-20 h-20 bg-background rounded-full flex items-center justify-center mx-auto mb-6">
              <ShoppingBag className="w-10 h-10 text-accent" />
            </div>
            <h2 className="font-serif text-2xl font-semibold mb-3">Your cart is empty</h2>
            <p className="text-secondary-text mb-8 max-w-md mx-auto">
              Add items to your cart before checking out.
            </p>
            <Link href="/products">
              <Button size="lg">Browse Products</Button>
            </Link>
          </motion.div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Content */}
            <div className="lg:col-span-2">
              <AnimatePresence mode="wait">
                {step === 1 && (
                  <motion.div
                    key="shipping"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.25 }}
                    className="bg-surface border border-border rounded-card p-6 md:p-8 shadow-soft"
                  >
                    <h2 className="font-serif text-2xl font-semibold mb-6">Shipping Address</h2>
                    <form onSubmit={handleShippingSubmit} className="space-y-5">
                      <div>
                        <label className="block text-sm font-medium text-primary mb-1.5">
                          Address Line 1 <span className="text-error">*</span>
                        </label>
                        <input
                          type="text"
                          required
                          value={address.address_line1}
                          onChange={(e) => setAddress({ ...address, address_line1: e.target.value })}
                          className="w-full px-4 py-3 bg-background border border-border rounded-input text-primary placeholder-secondary-text transition-all duration-200 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent"
                          placeholder="Street address"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-primary mb-1.5">
                          Address Line 2
                        </label>
                        <input
                          type="text"
                          value={address.address_line2}
                          onChange={(e) => setAddress({ ...address, address_line2: e.target.value })}
                          className="w-full px-4 py-3 bg-background border border-border rounded-input text-primary placeholder-secondary-text transition-all duration-200 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent"
                          placeholder="Apartment, suite, unit, etc."
                        />
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                        <div>
                          <label className="block text-sm font-medium text-primary mb-1.5">
                            City <span className="text-error">*</span>
                          </label>
                          <input
                            type="text"
                            required
                            value={address.city}
                            onChange={(e) => setAddress({ ...address, city: e.target.value })}
                            className="w-full px-4 py-3 bg-background border border-border rounded-input text-primary placeholder-secondary-text transition-all duration-200 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent"
                            placeholder="City"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-primary mb-1.5">
                            State / Province <span className="text-error">*</span>
                          </label>
                          <input
                            type="text"
                            required
                            value={address.state}
                            onChange={(e) => setAddress({ ...address, state: e.target.value })}
                            className="w-full px-4 py-3 bg-background border border-border rounded-input text-primary placeholder-secondary-text transition-all duration-200 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent"
                            placeholder="State"
                          />
                        </div>
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                        <div>
                          <label className="block text-sm font-medium text-primary mb-1.5">
                            Postal Code <span className="text-error">*</span>
                          </label>
                          <input
                            type="text"
                            required
                            value={address.postal_code}
                            onChange={(e) => setAddress({ ...address, postal_code: e.target.value })}
                            className="w-full px-4 py-3 bg-background border border-border rounded-input text-primary placeholder-secondary-text transition-all duration-200 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent"
                            placeholder="Postal code"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-primary mb-1.5">
                            Country <span className="text-error">*</span>
                          </label>
                          <select
                            required
                            value={address.country}
                            onChange={(e) => setAddress({ ...address, country: e.target.value })}
                            className="w-full px-4 py-3 bg-background border border-border rounded-input text-primary transition-all duration-200 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent"
                          >
                            <option value="US">United States</option>
                            <option value="CA">Canada</option>
                            <option value="GB">United Kingdom</option>
                            <option value="AU">Australia</option>
                            <option value="IN">India</option>
                          </select>
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-primary mb-1.5">
                          Phone Number
                        </label>
                        <input
                          type="tel"
                          value={address.phone}
                          onChange={(e) => setAddress({ ...address, phone: e.target.value })}
                          className="w-full px-4 py-3 bg-background border border-border rounded-input text-primary placeholder-secondary-text transition-all duration-200 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent"
                          placeholder="(555) 123-4567"
                        />
                      </div>

                      {/* Coupon Code */}
                      <div className="pt-2">
                        <label className="block text-sm font-medium text-primary mb-1.5">
                          Coupon Code
                        </label>
                        <div className="flex gap-3">
                          <input
                            type="text"
                            value={coupon}
                            onChange={(e) => setCoupon(e.target.value)}
                            className="flex-1 px-4 py-3 bg-background border border-border rounded-input text-primary placeholder-secondary-text transition-all duration-200 focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent"
                            placeholder="Enter code"
                          />
                          <Button type="button" variant="secondary">
                            Apply
                          </Button>
                        </div>
                      </div>

                      <div className="pt-4">
                        <Button type="submit" size="lg" className="w-full sm:w-auto">
                          Continue to Review
                          <ChevronRight className="w-4 h-4 ml-2" />
                        </Button>
                      </div>
                    </form>
                  </motion.div>
                )}

                {step === 2 && (
                  <motion.div
                    key="review"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.25 }}
                    className="bg-surface border border-border rounded-card p-6 md:p-8 shadow-soft"
                  >
                    <h2 className="font-serif text-2xl font-semibold mb-6">Review Your Order</h2>

                    {/* Shipping Address */}
                    <div className="mb-8">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-medium">Shipping Address</h3>
                        <button
                          onClick={() => setStep(1)}
                          className="text-sm text-accent hover:text-accent-dark transition-colors"
                          aria-label="Edit shipping address"
                        >
                          Edit
                        </button>
                      </div>
                      <div className="bg-background border border-border rounded-button p-4 text-sm text-secondary-text">
                        <p className="font-medium text-primary">{address.address_line1}</p>
                        {address.address_line2 && <p>{address.address_line2}</p>}
                        <p>
                          {address.city}, {address.state} {address.postal_code}
                        </p>
                        <p>{address.country}</p>
                        {address.phone && <p className="mt-1">{address.phone}</p>}
                      </div>
                    </div>

                    {/* Order Items */}
                    <div className="mb-8">
                      <h3 className="text-lg font-medium mb-4">Order Items</h3>
                      <div className="space-y-3">
                        {cartItems.map((item) => (
                          <div
                            key={item.id}
                            className="flex items-center gap-4 bg-background border border-border rounded-button p-4"
                          >
                            <div className="w-16 h-16 bg-surface rounded-button overflow-hidden flex-shrink-0 flex items-center justify-center border border-border">
                              {item.thumbnail_url ? (
                                <img
                                  src={item.thumbnail_url}
                                  alt={item.product_name || 'Product'}
                                  className="w-full h-full object-cover"
                                />
                              ) : (
                                <ShoppingBag className="w-6 h-6 text-accent opacity-60" />
                              )}
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="font-medium text-primary line-clamp-1">
                                {item.product_name || `Product ${item.product_id.slice(0, 8)}`}
                              </p>
                              <p className="text-sm text-secondary-text">Qty: {item.quantity}</p>
                            </div>
                            <p className="font-medium text-primary">${item.subtotal.toFixed(2)}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {error && (
                      <div className="mb-6 p-4 bg-error/10 border border-error/20 rounded-button text-error text-sm">
                        {error}
                      </div>
                    )}

                    <div className="flex flex-col sm:flex-row gap-4">
                      <Button variant="secondary" onClick={() => setStep(1)} className="sm:w-auto">
                        <ArrowLeft className="w-4 h-4 mr-2" />
                        Back
                      </Button>
                      <Button onClick={handlePlaceOrder} loading={submitting} className="flex-1 sm:flex-none">
                        Place Order
                      </Button>
                    </div>
                  </motion.div>
                )}

                {step === 3 && (
                  <motion.div
                    key="confirmation"
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.25 }}
                    className="bg-surface border border-border rounded-card p-8 md:p-12 text-center shadow-soft max-w-2xl mx-auto"
                  >
                    <div className="w-16 h-16 bg-success/10 rounded-full flex items-center justify-center mx-auto mb-6">
                      <Check className="w-8 h-8 text-success" />
                    </div>
                    <h2 className="font-serif text-3xl font-semibold mb-3">Order Confirmed!</h2>
                    <p className="text-secondary-text mb-2">
                      Thank you for your purchase. Your order has been placed successfully.
                    </p>
                    {orderNumber && (
                      <p className="text-lg font-medium text-primary mb-8">
                        Order Number: <span className="text-accent">{orderNumber}</span>
                      </p>
                    )}
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                      <Link href="/profile/orders">
                        <Button size="lg">
                          View Orders
                          <ChevronRight className="w-4 h-4 ml-2" />
                        </Button>
                      </Link>
                      <Link href="/products">
                        <Button variant="secondary" size="lg">
                          Continue Shopping
                        </Button>
                      </Link>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Order Summary Sidebar */}
            {step < 3 && (
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

                  {/* Trust Badges */}
                  <div className="pt-6 border-t border-border">
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
            )}
          </div>
        )}
      </div>
    </div>
  );
}
