'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useCartStore } from '@/lib/store/useCartStore';
import { cartService } from '@/lib/services/cart.service';
import { X, Minus, Plus, ShoppingBag } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export function CartDrawer() {
  const { items, isDrawerOpen, setDrawerOpen, updateQuantity: localUpdateQuantity, removeItem: localRemoveItem, getTotalAmount } = useCartStore();

  const handleUpdateQuantity = async (itemId: string, quantity: number) => {
    if (quantity < 1) return;
    try {
      const data = await cartService.updateItem(itemId, quantity);
      localUpdateQuantity(itemId, data.quantity || quantity);
    } catch {
      localUpdateQuantity(itemId, quantity);
    }
  };

  const handleRemoveItem = async (itemId: string) => {
    try {
      await cartService.removeItem(itemId);
    } catch {
      // ignore
    }
    localRemoveItem(itemId);
  };

  return (
    <AnimatePresence>
      {isDrawerOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setDrawerOpen(false)}
            className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50"
          />
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed right-0 top-0 bottom-0 w-full max-w-md bg-background border-l border-border z-50 shadow-2xl flex flex-col"
          >
            <div className="flex items-center justify-between p-6 border-b border-border">
              <h2 className="text-xl font-serif font-semibold">Your Cart</h2>
              <button
                onClick={() => setDrawerOpen(false)}
                className="p-2 rounded-full hover:bg-surface transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              {items.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-secondary-text">
                  <ShoppingBag className="w-12 h-12 mb-4 opacity-20" />
                  <p>Your cart is empty.</p>
                  <Button 
                    variant="outline" 
                    className="mt-6"
                    onClick={() => setDrawerOpen(false)}
                  >
                    Continue Shopping
                  </Button>
                </div>
              ) : (
                items.map((item) => (
                  <div key={item.id} className="flex gap-4 border border-border rounded-lg p-4 bg-surface/50">
                    <div className="w-20 h-20 bg-border/50 rounded-md flex-shrink-0 overflow-hidden">
                      {item.thumbnail_url ? (
                        <img src={item.thumbnail_url} alt={item.product_name || 'Product'} className="w-full h-full object-cover" />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center text-secondary-text text-xs">No image</div>
                      )}
                    </div>
                    <div className="flex-1 flex flex-col justify-between">
                      <div>
                        <h3 className="font-medium text-sm line-clamp-2">{item.product_name || 'Product'}</h3>
                        <p className="text-accent text-sm mt-1">${Number(item.unit_price).toFixed(2)}</p>
                      </div>
                      <div className="flex items-center justify-between mt-2">
                        <div className="flex items-center gap-3 bg-background border border-border rounded-md px-2 py-1">
                          <button 
                            onClick={() => handleUpdateQuantity(item.id, Math.max(1, item.quantity - 1))}
                            className="text-secondary-text hover:text-primary transition-colors"
                          >
                            <Minus className="w-3 h-3" />
                          </button>
                          <span className="text-sm w-4 text-center">{item.quantity}</span>
                          <button 
                            onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}
                            className="text-secondary-text hover:text-primary transition-colors"
                          >
                            <Plus className="w-3 h-3" />
                          </button>
                        </div>
                        <button 
                          onClick={() => handleRemoveItem(item.id)}
                          className="text-xs text-secondary-text hover:text-error transition-colors"
                        >
                          Remove
                        </button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>

            {items.length > 0 && (
               <div className="p-6 border-t border-border bg-surface/50">
                 <div className="flex items-center justify-between mb-4">
                   <span className="font-medium">Subtotal</span>
                   <span className="font-serif text-lg font-semibold">${getTotalAmount().toFixed(2)}</span>
                 </div>
                 <p className="text-xs text-secondary-text mb-6">Shipping and taxes calculated at checkout.</p>
                 <div className="grid grid-cols-2 gap-4">
                   <Link href="/cart" onClick={() => setDrawerOpen(false)} className="w-full">
                     <Button variant="outline" className="w-full">View Cart</Button>
                   </Link>
                   <Link href="/checkout" onClick={() => setDrawerOpen(false)} className="w-full">
                     <Button variant="primary" className="w-full">Checkout</Button>
                   </Link>
                 </div>
               </div>
            )}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
