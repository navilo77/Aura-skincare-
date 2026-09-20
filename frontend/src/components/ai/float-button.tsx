'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { MessageSquare, X, Sparkles, ChevronRight } from 'lucide-react';
import Link from 'next/link';
import { useState } from 'react';

export function AIFloatButton() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Floating Button */}
      <motion.button
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.25, type: 'spring', stiffness: 200, damping: 20 }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 z-50 flex items-center justify-center w-14 h-14 bg-accent text-white rounded-full shadow-premium hover:shadow-soft-lg transition-shadow"
        aria-label="Open AI Assistant"
      >
        {isOpen ? <X className="h-6 w-6" /> : <Sparkles className="h-6 w-6" />}
      </motion.button>

      {/* Popup Card */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ duration: 0.2, ease: 'easeOut' }}
            className="fixed bottom-24 right-6 z-50 w-80 bg-background border border-border rounded-card shadow-premium p-5"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-accent/10 rounded-full flex items-center justify-center flex-shrink-0">
                  <Sparkles className="h-5 w-5 text-accent" />
                </div>
                <div>
                  <h3 className="font-serif font-semibold text-primary">Aura AI</h3>
                  <p className="text-xs text-secondary-text">Your skincare companion</p>
                </div>
              </div>
            </div>
            <p className="text-sm text-secondary-text mb-4 leading-relaxed">
              Need help finding the perfect skincare routine? Chat with Aura AI for personalized recommendations.
            </p>
            <Link href="/ai" onClick={() => setIsOpen(false)}>
              <button className="w-full btn-primary flex items-center justify-center space-x-2">
                <MessageSquare className="h-4 w-4" />
                <span>Start Chatting</span>
                <ChevronRight className="h-4 w-4" />
              </button>
            </Link>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
