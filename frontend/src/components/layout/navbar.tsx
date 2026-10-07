'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Menu,
  X,
  Search,
  Heart,
  ShoppingBag,
  User,
  Sparkles,
  ChevronDown,
  Sun,
  Moon,
  ShoppingCart,
} from 'lucide-react';
import { useTheme } from '@/components/theme-provider';
import { Button } from '@/components/ui/button';
import { useCartStore } from '@/lib/store/useCartStore';
import { useWishlistStore } from '@/lib/store/useWishlistStore';

const categories = [
  { name: 'Cleansers', href: '/products?category=cleansers' },
  { name: 'Serums', href: '/products?category=serums' },
  { name: 'Moisturizers', href: '/products?category=moisturizers' },
  { name: 'Sunscreens', href: '/products?category=sunscreens' },
  { name: 'Masks', href: '/products?category=masks' },
  { name: 'Eye Care', href: '/products?category=eye-care' },
];

export function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isMegaMenuOpen, setIsMegaMenuOpen] = useState(false);
  const { theme, toggleTheme } = useTheme();
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  const cartCount = useCartStore(state => state.getTotalItems());
  const setDrawerOpen = useCartStore(state => state.setDrawerOpen);
  const wishlistCount = useWishlistStore(state => state.items.length);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <>
      {/* Announcement Bar */}
      <motion.div
        initial={{ y: -50 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        className="relative bg-gradient-to-r from-accent via-accent-light to-accent text-white overflow-hidden"
      >
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMSIgZmlsbD0id2hpdGUiIGZpbGwtb3BhY2l0eT0iMC41Ii8+PC9zdmc+')] opacity-20" />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5">
          <div className="flex items-center justify-center gap-2 text-sm font-medium">
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <Sparkles className="w-4 h-4" />
            </motion.div>
            <span>Free shipping on orders over $50 | Use code</span>
            <span className="font-bold mx-1 px-2 py-0.5 bg-white/20 rounded-md backdrop-blur-sm">
              AURA10
            </span>
            <span>for 10% off</span>
          </div>
        </div>
      </motion.div>

      {/* Main Navbar */}
      <header
        className={[
          'sticky top-0 z-50 transition-all duration-500',
          isScrolled
            ? 'bg-background/80 backdrop-blur-2xl border-b border-border shadow-soft'
            : 'bg-transparent',
        ]
          .filter(Boolean)
          .join(' ')}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 lg:h-20">
            {/* Logo */}
            <Link href="/" className="flex items-center space-x-2 group">
              <motion.div
                whileHover={{ scale: 1.05, rotate: 5 }}
                transition={{ type: "spring", stiffness: 300, damping: 20 }}
                className="relative"
              >
                <span className="font-serif text-2xl font-semibold tracking-tight text-primary relative z-10">
                  Aura
                </span>
                <span className="text-accent text-sm font-light tracking-widest uppercase ml-1">
                  Skincare
                </span>
              </motion.div>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden lg:flex items-center space-x-1">
              <Link
                href="/products"
                className="relative px-4 py-2 text-sm font-medium text-primary hover:text-accent transition-colors group"
              >
                Shop
                <span className="absolute bottom-0 left-4 right-4 h-0.5 bg-accent scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left" />
              </Link>

              {/* Mega Menu */}
              <div
                className="relative"
                onMouseEnter={() => setIsMegaMenuOpen(true)}
                onMouseLeave={() => setIsMegaMenuOpen(false)}
              >
                <button className="relative px-4 py-2 text-sm font-medium text-primary hover:text-accent transition-colors flex items-center gap-1 group">
                  Categories
                  <motion.div
                    animate={{ rotate: isMegaMenuOpen ? 180 : 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <ChevronDown className="h-4 w-4" />
                  </motion.div>
                  <span className="absolute bottom-0 left-4 right-4 h-0.5 bg-accent scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left" />
                </button>

                <AnimatePresence>
                  {isMegaMenuOpen && (
                    <motion.div
                      initial={{ opacity: 0, y: 10, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: 10, scale: 0.95 }}
                      transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
                      className="absolute top-full left-1/2 -translate-x-1/2 mt-4 w-screen max-w-4xl bg-background/95 backdrop-blur-2xl border border-border rounded-card shadow-premium p-8"
                    >
                      <div className="grid grid-cols-4 gap-8">
                        {categories.map((category, index) => (
                          <motion.div
                            key={category.name}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.05 }}
                          >
                            <Link
                              href={category.href}
                              className="group block p-4 rounded-button hover:bg-surface transition-all duration-200"
                            >
                              <h3 className="font-medium text-primary group-hover:text-accent transition-colors mb-1">
                                {category.name}
                              </h3>
                              <p className="text-xs text-secondary">
                                Shop {category.name.toLowerCase()}
                              </p>
                            </Link>
                          </motion.div>
                        ))}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              <Link
                href="/ai"
                className="relative px-4 py-2 text-sm font-medium text-primary hover:text-accent transition-colors flex items-center gap-1.5 group"
              >
                <Sparkles className="h-4 w-4" />
                AI Assistant
                <span className="absolute bottom-0 left-4 right-4 h-0.5 bg-accent scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left" />
              </Link>
            </nav>

            {/* Right Actions */}
            <div className="flex items-center gap-2">
              {/* Search */}
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setIsSearchOpen(!isSearchOpen)}
                className="hidden md:flex p-2 rounded-full hover:bg-surface transition-colors relative"
                aria-label="Search"
              >
                <Search className="h-5 w-5" />
              </motion.button>

              {/* Wishlist */}
              <Link
                href="/wishlist"
                className="hidden md:flex p-2 rounded-full hover:bg-surface transition-colors relative group"
                aria-label="Wishlist"
              >
                <motion.div
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <Heart className="h-5 w-5" />
                </motion.div>
                {wishlistCount > 0 && (
                  <motion.span
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="absolute -top-1 -right-1 h-5 w-5 bg-accent text-white text-xs rounded-full flex items-center justify-center font-medium"
                  >
                    {wishlistCount}
                  </motion.span>
                )}
              </Link>

              {/* Cart */}
              <button
                onClick={() => setDrawerOpen(true)}
                className="hidden md:flex p-2 rounded-full hover:bg-surface transition-colors relative group"
                aria-label="Cart"
              >
                <motion.div
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <ShoppingBag className="h-5 w-5" />
                </motion.div>
                {cartCount > 0 && (
                  <motion.span
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="absolute -top-1 -right-1 h-5 w-5 bg-accent text-white text-xs rounded-full flex items-center justify-center font-medium"
                  >
                    {cartCount}
                  </motion.span>
                )}
              </button>

              {/* Theme Toggle */}
              <motion.button
                whileHover={{ scale: 1.1, rotate: 15 }}
                whileTap={{ scale: 0.9 }}
                onClick={toggleTheme}
                className="p-2 rounded-full hover:bg-surface transition-colors"
                aria-label="Toggle theme"
              >
                {theme === 'light' ? (
                  <Moon className="h-5 w-5" />
                ) : (
                  <Sun className="h-5 w-5" />
                )}
              </motion.button>

              {/* Profile */}
              <Link
                href="/profile"
                className="hidden md:flex p-2 rounded-full hover:bg-surface transition-colors relative group"
                aria-label="Profile"
              >
                <motion.div
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                >
                  <User className="h-5 w-5" />
                </motion.div>
              </Link>

              {/* Mobile menu button */}
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="lg:hidden p-2 rounded-full hover:bg-surface transition-colors relative"
                aria-label="Menu"
              >
                <AnimatePresence mode="wait">
                  {isMobileMenuOpen ? (
                    <motion.div
                      key="close"
                      initial={{ rotate: -90, opacity: 0 }}
                      animate={{ rotate: 0, opacity: 1 }}
                      exit={{ rotate: 90, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                    >
                      <X className="h-6 w-6" />
                    </motion.div>
                  ) : (
                    <motion.div
                      key="menu"
                      initial={{ rotate: 90, opacity: 0 }}
                      animate={{ rotate: 0, opacity: 1 }}
                      exit={{ rotate: -90, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                    >
                      <Menu className="h-6 w-6" />
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.button>
            </div>
          </div>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isMobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
              className="lg:hidden bg-background/95 backdrop-blur-2xl border-t border-border overflow-hidden"
            >
              <div className="px-4 py-6 space-y-2">
                {categories.map((category, index) => (
                  <motion.div
                    key={category.name}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                  >
                    <Link
                      href={category.href}
                      className="block py-3 text-base font-medium text-primary hover:text-accent transition-colors"
                      onClick={() => setIsMobileMenuOpen(false)}
                    >
                      {category.name}
                    </Link>
                  </motion.div>
                ))}
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 }}
                  className="pt-4 border-t border-border space-y-2"
                >
                  <Link
                    href="/products"
                    className="flex items-center py-3 text-base font-medium text-primary hover:text-accent transition-colors"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <Search className="mr-3 h-5 w-5" />
                    Search
                  </Link>
                  <Link
                    href="/wishlist"
                    className="flex items-center py-3 text-base text-primary hover:text-accent transition-colors"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <Heart className="mr-3 h-5 w-5" />
                    Wishlist
                  </Link>
                  <Link
                    href="/cart"
                    className="flex items-center py-3 text-base text-primary hover:text-accent transition-colors"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <ShoppingBag className="mr-3 h-5 w-5" />
                    Cart
                  </Link>
                  <Link
                    href="/profile"
                    className="flex items-center py-3 text-base text-primary hover:text-accent transition-colors"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <User className="mr-3 h-5 w-5" />
                    Profile
                  </Link>
                </motion.div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </header>
    </>
  );
}
