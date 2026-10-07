'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { Sparkles, Camera, Share2, MessageCircle, ArrowRight } from 'lucide-react';

const footerLinks = {
  shop: [
    { name: 'All Products', href: '/products' },
    { name: 'Cleansers', href: '/products?category=cleansers' },
    { name: 'Serums', href: '/products?category=serums' },
    { name: 'Moisturizers', href: '/products?category=moisturizers' },
    { name: 'Sunscreens', href: '/products?category=sunscreens' },
  ],
  account: [
    { name: 'My Account', href: '/profile' },
    { name: 'Orders', href: '/profile/orders' },
    { name: 'Wishlist', href: '/wishlist' },
    { name: 'Cart', href: '/cart' },
  ],
  support: [
    { name: 'Contact Us', href: '#' },
    { name: 'Shipping & Returns', href: '#' },
    { name: 'FAQ', href: '#' },
    { name: 'Privacy Policy', href: '#' },
  ],
  company: [
    { name: 'About Us', href: '#' },
    { name: 'Careers', href: '#' },
    { name: 'Press', href: '#' },
    { name: 'Blog', href: '#' },
  ],
};

const socialLinks = [
  { icon: Camera, href: '#', label: 'Instagram' },
  { icon: Share2, href: '#', label: 'Twitter' },
  { icon: MessageCircle, href: '#', label: 'WhatsApp' },
];

export function Footer() {
  return (
    <footer className="relative bg-surface border-t border-border overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-gradient-to-br from-accent/5 via-transparent to-accent/5 pointer-events-none" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Main Footer Content */}
        <div className="py-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-12">
          {/* Brand Column */}
          <div className="lg:col-span-2">
            <Link href="/" className="inline-flex items-center space-x-2 group">
              <motion.div
                whileHover={{ scale: 1.05, rotate: 5 }}
                transition={{ type: "spring", stiffness: 300, damping: 20 }}
              >
                <span className="font-serif text-3xl font-semibold tracking-tight text-primary">
                  Aura
                </span>
                <span className="text-accent text-sm font-light tracking-widest uppercase ml-1">
                  Skincare
                </span>
              </motion.div>
            </Link>
            <p className="mt-6 text-sm text-secondary leading-relaxed max-w-sm">
              AI-powered beauty commerce platform. Pure formulations, luminous skin.
              Experience luxury skincare crafted with the purest ingredients.
            </p>

            {/* Social Links */}
            <div className="flex space-x-3 mt-8">
              {socialLinks.map((social) => (
                <motion.a
                  key={social.label}
                  href={social.href}
                  aria-label={social.label}
                  whileHover={{ scale: 1.1, y: -2 }}
                  whileTap={{ scale: 0.9 }}
                  className="w-10 h-10 rounded-full bg-background border border-border flex items-center justify-center text-secondary hover:text-accent hover:border-accent transition-all duration-200"
                >
                  <social.icon className="h-5 w-5" />
                </motion.a>
              ))}
            </div>

            {/* Newsletter */}
            <div className="mt-8">
              <h3 className="font-serif text-lg font-semibold text-primary mb-3">
                Stay Updated
              </h3>
              <form className="flex gap-2">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="flex-1 px-4 py-2.5 bg-background border border-border rounded-input text-sm text-primary placeholder:text-secondary-text focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all"
                />
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-4 py-2.5 bg-accent text-white rounded-button hover:bg-accent-dark transition-colors"
                >
                  <ArrowRight className="h-4 w-4" />
                </motion.button>
              </form>
            </div>
          </div>

          {/* Shop Links */}
          <div>
            <h3 className="font-serif text-lg font-semibold text-primary mb-4">
              Shop
            </h3>
            <ul className="space-y-3">
              {footerLinks.shop.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm text-secondary hover:text-accent transition-colors inline-flex items-center gap-1 group"
                  >
                    <span>{link.name}</span>
                    <ArrowRight className="h-3 w-3 opacity-0 -translate-x-1 group-hover:opacity-100 group-hover:translate-x-0 transition-all" />
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Account Links */}
          <div>
            <h3 className="font-serif text-lg font-semibold text-primary mb-4">
              Account
            </h3>
            <ul className="space-y-3">
              {footerLinks.account.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm text-secondary hover:text-accent transition-colors inline-flex items-center gap-1 group"
                  >
                    <span>{link.name}</span>
                    <ArrowRight className="h-3 w-3 opacity-0 -translate-x-1 group-hover:opacity-100 group-hover:translate-x-0 transition-all" />
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Support Links */}
          <div>
            <h3 className="font-serif text-lg font-semibold text-primary mb-4">
              Support
            </h3>
            <ul className="space-y-3">
              {footerLinks.support.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm text-secondary hover:text-accent transition-colors inline-flex items-center gap-1 group"
                  >
                    <span>{link.name}</span>
                    <ArrowRight className="h-3 w-3 opacity-0 -translate-x-1 group-hover:opacity-100 group-hover:translate-x-0 transition-all" />
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company Links */}
          <div>
            <h3 className="font-serif text-lg font-semibold text-primary mb-4">
              Company
            </h3>
            <ul className="space-y-3">
              {footerLinks.company.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm text-secondary hover:text-accent transition-colors inline-flex items-center gap-1 group"
                  >
                    <span>{link.name}</span>
                    <ArrowRight className="h-3 w-3 opacity-0 -translate-x-1 group-hover:opacity-100 group-hover:translate-x-0 transition-all" />
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="py-8 border-t border-border">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <motion.p
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              className="text-sm text-secondary"
            >
              © 2024 Aura Skincare. All rights reserved.
            </motion.p>

            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              className="flex items-center gap-6"
            >
              <Link
                href="/ai"
                className="flex items-center text-sm text-accent hover:text-accent-dark transition-colors group"
              >
                <Sparkles className="mr-2 h-4 w-4 group-hover:rotate-12 transition-transform" />
                Try AI Skin Analysis
                <ArrowRight className="ml-2 h-3 w-3 group-hover:translate-x-1 transition-transform" />
              </Link>
            </motion.div>
          </div>
        </div>
      </div>
    </footer>
  );
}
