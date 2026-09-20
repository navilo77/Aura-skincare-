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
} from 'lucide-react';
import { useTheme } from '@/components/theme-provider';
import { Button } from '@/components/ui/button';

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
  const [cartCount, setCartCount] = useState(0);
  const [wishlistCount, setWishlistCount] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <>
      {/* Announcement Bar */}
      <div className="bg-primary text-white text-center py-2 text-sm">
        Free shipping on orders over $50 | Use code AURA10 for 10% off
      </div>

      {/* Main Navbar */}
      <header
        className={[
          'sticky top-0 z-50 transition-all duration-300',
          isScrolled
            ? 'bg-background/95 backdrop-blur-md border-b border-border shadow-soft'
            : 'bg-transparent',
        ]
          .filter(Boolean)
          .join(' ')}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 lg:h-20">
            {/* Logo */}
            <Link href="/" className="flex items-center space-x-2">
              <span className="font-serif text-2xl font-semibold tracking-tight">
                Aura
              </span>
              <span className="text-accent text-sm font-light tracking-widest uppercase">
                Skincare
              </span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden lg:flex items-center space-x-8">
              <Link
                href="/products"
                className="text-sm font-medium text-primary hover:text-accent transition-colors"
              >
                Shop
              </Link>

              {/* Mega Menu */}
              <div
                className="relative"
                onMouseEnter={() => setIsMegaMenuOpen(true)}
                onMouseLeave={() => setIsMegaMenuOpen(false)}
              >
                <button className="flex items-center text-sm font-medium text-primary hover:text-accent transition-colors">
                  Categories
                  <ChevronDown className="ml-1 h-4 w-4" />
                </button>

                <AnimatePresence>
                  {isMegaMenuOpen && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 10 }}
                      transition={{ duration: 0.2 }}
                      className="absolute top-full left-1/2 -translate-x-1/2 mt-4 w-screen max-w-4xl bg-background border border-border rounded-card shadow-premium p-8"
                    >
                      <div className="grid grid-cols-4 gap-8">
                        {categories.map((category) => (
                          <Link
                            key={category.name}
                            href={category.href}
                            className="group block p-4 rounded-button hover:bg-surface transition-colors"
                          >
                            <h3 className="font-medium text-primary group-hover:text-accent transition-colors">
                              {category.name}
                            </h3>
                          </Link>
                        ))}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              <Link
                href="/ai"
                className="flex items-center text-sm font-medium text-primary hover:text-accent transition-colors"
              >
                <Sparkles className="mr-1 h-4 w-4" />
                AI Assistant
              </Link>
            </nav>

            {/* Right Actions */}
            <div className="flex items-center space-x-4">
              <button
                onClick={toggleTheme}
                className="p-2 rounded-full hover:bg-surface transition-colors"
                aria-label="Toggle theme"
              >
                {theme === 'light' ? (
                  <Moon className="h-5 w-5" />
                ) : (
                  <Sun className="h-5 w-5" />
                )}
              </button>

              <Link
                href="/products"
                className="hidden md:flex p-2 rounded-full hover:bg-surface transition-colors"
                aria-label="Search"
              >
                <Search className="h-5 w-5" />
              </Link>

              <Link
                href="/wishlist"
                className="hidden md:flex p-2 rounded-full hover:bg-surface transition-colors relative"
                aria-label="Wishlist"
              >
                <Heart className="h-5 w-5" />
                {wishlistCount > 0 && (
                  <span className="absolute -top-1 -right-1 h-4 w-4 bg-accent text-white text-xs rounded-full flex items-center justify-center">
                    {wishlistCount}
                  </span>
                )}
              </Link>

              <Link
                href="/cart"
                className="hidden md:flex p-2 rounded-full hover:bg-surface transition-colors relative"
                aria-label="Cart"
              >
                <ShoppingBag className="h-5 w-5" />
                {cartCount > 0 && (
                  <span className="absolute -top-1 -right-1 h-4 w-4 bg-accent text-white text-xs rounded-full flex items-center justify-center">
                    {cartCount}
                  </span>
                )}
              </Link>

              <Link
                href="/profile"
                className="hidden md:flex p-2 rounded-full hover:bg-surface transition-colors"
                aria-label="Profile"
              >
                <User className="h-5 w-5" />
              </Link>

              {/* Mobile menu button */}
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="lg:hidden p-2 rounded-full hover:bg-surface transition-colors"
                aria-label="Menu"
              >
                {isMobileMenuOpen ? (
                  <X className="h-6 w-6" />
                ) : (
                  <Menu className="h-6 w-6" />
                )}
              </button>
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
              transition={{ duration: 0.2 }}
              className="lg:hidden bg-background border-b border-border"
            >
              <div className="px-4 py-4 space-y-2">
                <Link
                  href="/products"
                  className="block py-2 text-base font-medium text-primary hover:text-accent transition-colors"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Shop
                </Link>
                {categories.map((category) => (
                  <Link
                    key={category.name}
                    href={category.href}
                    className="block py-2 pl-4 text-base text-primary hover:text-accent transition-colors"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    {category.name}
                  </Link>
                ))}
                <Link
                  href="/ai"
                  className="flex items-center py-2 text-base font-medium text-primary hover:text-accent transition-colors"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  <Sparkles className="mr-2 h-4 w-4" />
                  AI Assistant
                </Link>
                <div className="pt-4 border-t border-border">
                  <Link
                    href="/wishlist"
                    className="flex items-center py-2 text-base text-primary hover:text-accent transition-colors"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <Heart className="mr-2 h-5 w-5" />
                    Wishlist
                  </Link>
                  <Link
                    href="/cart"
                    className="flex items-center py-2 text-base text-primary hover:text-accent transition-colors"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <ShoppingBag className="mr-2 h-5 w-5" />
                    Cart
                  </Link>
                  <Link
                    href="/profile"
                    className="flex items-center py-2 text-base text-primary hover:text-accent transition-colors"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <User className="mr-2 h-5 w-5" />
                    Profile
                  </Link>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </header>
    </>
  );
}
