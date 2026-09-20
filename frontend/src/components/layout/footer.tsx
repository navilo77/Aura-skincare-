'use client';

import Link from 'next/link';
import { Sparkles, Camera, Share2, MessageCircle } from 'lucide-react';

export function Footer() {
  return (
    <footer className="bg-surface border-t border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1">
            <Link href="/" className="flex items-center space-x-2">
              <span className="font-serif text-2xl font-semibold tracking-tight">
                Aura
              </span>
              <span className="text-accent text-sm font-light tracking-widest uppercase">
                Skincare
              </span>
            </Link>
            <p className="mt-4 text-sm text-secondary-text">
              AI-powered beauty commerce platform. Pure formulations, luminous skin.
            </p>
            <div className="flex space-x-4 mt-6">
              <a href="#" className="text-secondary-text hover:text-accent transition-colors">
                <Camera className="h-5 w-5" />
              </a>
              <a href="#" className="text-secondary-text hover:text-accent transition-colors">
                <Share2 className="h-5 w-5" />
              </a>
              <a href="#" className="text-secondary-text hover:text-accent transition-colors">
                <MessageCircle className="h-5 w-5" />
              </a>
            </div>
          </div>

          {/* Shop */}
          <div>
            <h3 className="font-serif text-lg font-semibold mb-4">Shop</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/products" className="text-sm text-secondary-text hover:text-accent transition-colors">
                  All Products
                </Link>
              </li>
              <li>
                <Link href="/products?category=cleansers" className="text-sm text-secondary-text hover:text-accent transition-colors">
                  Cleansers
                </Link>
              </li>
              <li>
                <Link href="/products?category=serums" className="text-sm text-secondary-text hover:text-accent transition-colors">
                  Serums
                </Link>
              </li>
              <li>
                <Link href="/products?category=moisturizers" className="text-sm text-secondary-text hover:text-accent transition-colors">
                  Moisturizers
                </Link>
              </li>
            </ul>
          </div>

          {/* Account */}
          <div>
            <h3 className="font-serif text-lg font-semibold mb-4">Account</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/profile" className="text-sm text-secondary-text hover:text-accent transition-colors">
                  My Account
                </Link>
              </li>
              <li>
                <Link href="/profile/orders" className="text-sm text-secondary-text hover:text-accent transition-colors">
                  Orders
                </Link>
              </li>
              <li>
                <Link href="/wishlist" className="text-sm text-secondary-text hover:text-accent transition-colors">
                  Wishlist
                </Link>
              </li>
              <li>
                <Link href="/auth/login" className="text-sm text-secondary-text hover:text-accent transition-colors">
                  Login
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="font-serif text-lg font-semibold mb-4">Support</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-sm text-secondary-text hover:text-accent transition-colors">
                  Contact Us
                </a>
              </li>
              <li>
                <a href="#" className="text-sm text-secondary-text hover:text-accent transition-colors">
                  Shipping & Returns
                </a>
              </li>
              <li>
                <a href="#" className="text-sm text-secondary-text hover:text-accent transition-colors">
                  FAQ
                </a>
              </li>
              <li>
                <a href="#" className="text-sm text-secondary-text hover:text-accent transition-colors">
                  Privacy Policy
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-border flex flex-col md:flex-row justify-between items-center">
          <p className="text-sm text-secondary-text">
            © 2024 Aura Skincare. All rights reserved.
          </p>
          <Link
            href="/ai"
            className="mt-4 md:mt-0 flex items-center text-sm text-accent hover:text-accent-dark transition-colors"
          >
            <Sparkles className="mr-2 h-4 w-4" />
            Try AI Skin Analysis
          </Link>
        </div>
      </div>
    </footer>
  );
}
