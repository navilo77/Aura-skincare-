"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { motion, useInView, AnimatePresence } from "framer-motion";
import {
  Sparkles,
  ShieldCheck,
  Heart,
  Leaf,
  FlaskConical,
  Truck,
  Star,
  ChevronRight,
  ArrowRight,
  Bot,
  Award,
  Repeat,
  Droplets,
  Sun,
  Smile,
  Eye,
  Camera,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Skeleton } from "@/components/ui/skeleton";

interface Product {
  id: string;
  name: string;
  price: number;
  currency: string;
  thumbnail_url: string | null;
  sku: string;
  status: string;
  is_active: boolean;
  is_featured: boolean;
}

const fadeIn = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
      transition: { duration: 0.25, ease: [0, 0, 0.2, 1] as const },
  },
};

const scaleIn = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: {
    opacity: 1,
    scale: 1,
      transition: { duration: 0.25, ease: [0, 0, 0.2, 1] as const },
  },
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.06, delayChildren: 0.1 },
  },
};

const floatingAnimation = {
  y: [0, -8, 0],
  transition: {
    duration: 3,
    repeat: Infinity,
    ease: [0.4, 0, 0.2, 1] as const,
  },
};

const floatingAnimationSlow = {
  y: [0, -6, 0],
  transition: {
    duration: 4,
    repeat: Infinity,
    ease: [0.4, 0, 0.2, 1] as const,
  },
};

function AnimatedSection({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true, margin: "-80px" });

  return (
    <motion.div
      ref={ref}
      initial="hidden"
      animate={isInView ? "visible" : "hidden"}
      variants={fadeIn}
      className={className}
    >
      {children}
    </motion.div>
  );
}

const trustBadges = [
  { icon: Heart, label: "Cruelty-Free" },
  { icon: FlaskConical, label: "Dermatologist Tested" },
  { icon: Leaf, label: "Clean Ingredients" },
  { icon: ShieldCheck, label: "Dermatologically Approved" },
  { icon: Award, label: "Award Winning" },
  { icon: Truck, label: "Free Shipping" },
];

const categories = [
  { name: "Cleansers", icon: Droplets, image: "🧴" },
  { name: "Serums", icon: Sparkles, image: "✨" },
  { name: "Moisturizers", icon: Heart, image: "💧" },
  { name: "Sunscreens", icon: Sun, image: "☀️" },
  { name: "Masks", icon: Smile, image: "🧖‍♀️" },
  { name: "Eye Care", icon: Eye, image: "👁️" },
];

const skinConcerns = [
  { name: "Anti-Aging", emoji: "⏳" },
  { name: "Brightening", emoji: "🌟" },
  { name: "Acne Prone", emoji: "🔬" },
  { name: "Sensitive", emoji: "🌸" },
  { name: "Hydration", emoji: "💧" },
  { name: "Pores", emoji: "✨" },
];

const testimonials = [
  {
    name: "Sarah M.",
    location: "Los Angeles, CA",
    text: "The Pure Radiance Serum transformed my skin in just 2 weeks. My complexion has never been more luminous.",
    rating: 5,
    product: "Pure Radiance Serum",
  },
  {
    name: "Emily R.",
    location: "New York, NY",
    text: "Finally found a brand that combines luxury with clean ingredients. The Hydra Glow Moisturizer is my holy grail.",
    rating: 5,
    product: "Hydra Glow Moisturizer",
  },
  {
    name: "Jessica T.",
    location: "Miami, FL",
    text: "The AI skin analysis was incredibly accurate. It recommended the perfect routine for my combination skin.",
    rating: 5,
    product: "AI Skin Analysis",
  },
];

function ProductBadge({ type }: { type: string }) {
  const styles: Record<string, string> = {
    New: "bg-accent text-white",
    "Best Seller": "bg-primary text-white",
    Limited: "bg-error text-white",
    Discount: "bg-success text-white",
  };

  return (
    <span
      className={cn(
        "inline-block px-3 py-1 text-xs font-medium rounded-full",
        styles[type] || "bg-primary text-white"
      )}
    >
      {type}
    </span>
  );
}

function StarRating({ rating }: { rating: number }) {
  return (
    <div className="flex items-center gap-1">
      {[...Array(5)].map((_, i) => (
        <Star
          key={i}
          size={14}
          className={cn(
            i < rating ? "fill-accent text-accent" : "text-border"
          )}
        />
      ))}
    </div>
  );
}

function ProductCard({
  product,
  badge,
  index,
}: {
  product: Product;
  badge?: string;
  index: number;
}) {
  const [imageError, setImageError] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  const discount = badge === "Discount" ? Math.floor(Math.random() * 20 + 10) : 0;

  return (
    <motion.div
      variants={scaleIn}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className={cn(
        "group relative bg-background border border-border rounded-product overflow-hidden transition-all duration-200",
        isHovered ? "shadow-premium -translate-y-1" : "shadow-soft"
      )}
    >
      <div className="relative aspect-[4/5] overflow-hidden bg-surface">
        {product.thumbnail_url && !imageError ? (
          <img
            src={product.thumbnail_url}
            alt={product.name}
            onError={() => setImageError(true)}
            className={cn(
              "w-full h-full object-cover transition-transform duration-300",
              isHovered ? "scale-105" : "scale-100"
            )}
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-surface to-border flex items-center justify-center">
            <Sparkles className="w-12 h-12 text-accent opacity-30" />
          </div>
        )}
        {badge && (
          <div className="absolute top-4 left-4">
            <ProductBadge type={badge} />
          </div>
        )}
      </div>
      <div className="p-5">
        <h3 className="font-serif text-lg font-medium text-primary mb-1 line-clamp-1">
          {product.name}
        </h3>
        <p className="text-sm text-secondary mb-3">SKU: {product.sku}</p>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="font-serif text-xl font-semibold text-primary">
              {product.currency === "USD" ? "$" : product.currency}
              {product.price.toFixed(2)}
            </span>
            {discount > 0 && (
              <span className="text-sm text-secondary line-through">
                ${(product.price / (1 - discount / 100)).toFixed(2)}
              </span>
            )}
          </div>
          <StarRating rating={5} />
        </div>
      </div>
    </motion.div>
  );
}

function TestimonialCard({
  testimonial,
  isActive,
  onClick,
}: {
  testimonial: typeof testimonials[0];
  isActive: boolean;
  onClick: () => void;
}) {
  return (
    <motion.button
      animate={{
        opacity: isActive ? 1 : 0.3,
        scale: isActive ? 1 : 0.95,
      }}
      transition={{ duration: 0.25 }}
      onClick={onClick}
      className={cn(
        "p-6 rounded-card cursor-pointer transition-all duration-200 text-left",
        isActive
          ? "bg-background border border-border shadow-soft"
          : "bg-surface border border-transparent"
      )}
      aria-pressed={isActive}
      type="button"
    >
      <div className="flex items-center gap-1 mb-3">
        {[...Array(testimonial.rating)].map((_, i) => (
          <Star key={i} size={16} className="fill-accent text-accent" />
        ))}
      </div>
      <p className="text-primary font-serif text-lg leading-relaxed mb-4">
        &ldquo;{testimonial.text}&rdquo;
      </p>
      <div>
        <p className="font-medium text-primary">{testimonial.name}</p>
        <p className="text-sm text-secondary">{testimonial.location}</p>
      </div>
    </motion.button>
  );
}

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTestimonial, setActiveTestimonial] = useState(0);
  const [subscribed, setSubscribed] = useState(false);

  const fetchProducts = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/products");
      if (!res.ok) throw new Error("Failed to fetch products");
      const data = await res.json();
      setProducts(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const bestSellers = products.filter((p) => p.is_featured).slice(0, 4);
  const newArrivals = products.slice(0, 4);

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-background via-surface to-background opacity-60" />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 lg:py-24">
          <div className="grid lg:grid-cols-2 gap-12 lg:gap-8 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4, ease: [0, 0, 0.2, 1] as const }}
            >
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-surface rounded-full border border-border mb-6">
                <Sparkles className="w-4 h-4 text-accent" />
                <span className="text-sm font-medium text-secondary">
                  AI-Powered Skincare
                </span>
              </div>
              <h1 className="font-serif text-5xl lg:text-7xl font-semibold text-primary leading-[1.1] mb-6">
                Pure Formulations,{" "}
                <span className="text-accent">Luminous</span> Skin
              </h1>
              <p className="text-lg text-secondary leading-relaxed mb-8 max-w-lg">
                Experience luxury skincare crafted with the purest ingredients,
                enhanced by AI-driven personalization for your unique skin needs.
              </p>
              <div className="flex flex-wrap gap-4">
                <Link
                  href="/products"
                  className="inline-flex items-center gap-2 px-8 py-3.5 bg-accent text-white font-medium rounded-button hover:bg-accent-dark transition-all duration-200 shadow-soft"
                >
                  Shop Now
                  <ArrowRight className="w-4 h-4" />
                </Link>
                <Link
                  href="/ai"
                  className="inline-flex items-center gap-2 px-8 py-3.5 border border-border bg-background text-primary font-medium rounded-button hover:bg-surface transition-all duration-200"
                >
                  <Bot className="w-4 h-4" />
                  Skin Routine AI
                </Link>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4, ease: [0, 0, 0.2, 1] as const, delay: 0.1 }}
              className="relative"
            >
              <div className="relative aspect-square max-w-lg mx-auto">
                {/* Product image placeholder */}
                <div className="absolute inset-0 bg-gradient-to-br from-surface to-background rounded-card border border-border shadow-premium flex items-center justify-center">
                  <div className="text-center">
                    <Sparkles className="w-24 h-24 text-accent mx-auto mb-4 opacity-40" />
                    <p className="font-serif text-2xl text-primary">
                      Premium Product
                    </p>
                    <p className="text-secondary mt-2">Luxury skincare formulation</p>
                  </div>
                </div>

                {/* Floating AI assistant card */}
                <motion.div
                  animate={floatingAnimation}
                  className="absolute -bottom-4 -left-4 lg:-left-8 bg-background border border-border rounded-card p-4 shadow-premium"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-accent/10 rounded-full flex items-center justify-center">
                      <Bot className="w-6 h-6 text-accent" />
                    </div>
                    <div>
                      <p className="font-medium text-primary text-sm">
                        AI Skin Analysis
                      </p>
                      <p className="text-xs text-secondary">
                        Ready to analyze your skin
                      </p>
                    </div>
                  </div>
                </motion.div>

                {/* Authenticity badge */}
                <motion.div
                  animate={floatingAnimationSlow}
                  className="absolute -top-4 -right-4 lg:-right-8 bg-background border border-border rounded-card p-3 shadow-premium"
                >
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="w-6 h-6 text-accent" />
                    <div>
                      <p className="font-medium text-primary text-sm">
                        100% Authentic
                      </p>
                      <p className="text-xs text-secondary">
                        Verified products
                      </p>
                    </div>
                  </div>
                </motion.div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Trust Badges Strip */}
      <section className="border-y border-border bg-surface">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-40px" }}
            variants={staggerContainer}
            className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6"
          >
            {trustBadges.map((badge) => (
              <motion.div
                key={badge.label}
                variants={fadeIn}
                className="flex flex-col items-center text-center gap-2"
              >
                <badge.icon className="w-6 h-6 text-accent" />
                <span className="text-xs font-medium text-secondary">
                  {badge.label}
                </span>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Featured Categories */}
      <section className="py-16 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection className="text-center mb-12">
            <h2 className="font-serif text-4xl font-semibold text-primary mb-4">
              Shop by Category
            </h2>
            <p className="text-secondary max-w-2xl mx-auto">
              Discover our curated collection of premium skincare essentials,
              designed to nurture and transform your skin.
            </p>
          </AnimatedSection>

          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-40px" }}
            variants={staggerContainer}
            className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 lg:gap-6"
          >
            {categories.map((category) => (
              <motion.div
                key={category.name}
                variants={scaleIn}
                className="group cursor-pointer"
              >
                <Link href="/products">
                  <div className="bg-surface border border-border rounded-card p-6 text-center transition-all duration-200 hover:shadow-soft hover:-translate-y-1">
                    <div className="text-4xl mb-3">{category.image}</div>
                    <h3 className="font-serif text-lg font-medium text-primary group-hover:text-accent transition-colors">
                      {category.name}
                    </h3>
                  </div>
                </Link>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Best Sellers */}
      <section className="py-16 lg:py-24 bg-surface">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection className="flex items-end justify-between mb-12">
            <div>
              <h2 className="font-serif text-4xl font-semibold text-primary mb-4">
                Best Sellers
              </h2>
              <p className="text-secondary max-w-xl">
                Our most loved products, trusted by thousands for visible results.
              </p>
            </div>
            <Link
              href="/products"
              className="hidden md:inline-flex items-center gap-2 text-accent font-medium hover:gap-3 transition-all"
            >
              View All
              <ChevronRight className="w-4 h-4" />
            </Link>
          </AnimatedSection>

          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="bg-background border border-border rounded-product p-5">
                  <Skeleton className="aspect-[4/5] rounded-product mb-4" />
                  <Skeleton className="h-4 rounded mb-2" />
                  <Skeleton className="h-3 rounded w-2/3 mb-4" />
                  <Skeleton className="h-6 rounded w-1/3" />
                </div>
              ))}
            </div>
          ) : error ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center py-12 bg-surface rounded-card border border-border"
            >
              <p className="text-secondary-text mb-4">{error}</p>
              <button
                onClick={fetchProducts}
                className="inline-flex items-center gap-2 px-6 py-3 bg-accent text-white font-medium rounded-button hover:bg-accent-dark transition-all duration-200 shadow-soft"
              >
                Try Again
              </button>
            </motion.div>
          ) : bestSellers.length > 0 ? (
            <motion.div
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-40px" }}
              variants={staggerContainer}
              className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"
            >
              {bestSellers.map((product, index) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  badge={
                    index === 0
                      ? "Best Seller"
                      : index === 1
                      ? "New"
                      : index === 2
                      ? "Limited"
                      : undefined
                  }
                  index={index}
                />
              ))}
            </motion.div>
          ) : (
            <motion.div
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={fadeIn}
              className="text-center py-12 bg-surface rounded-card border border-border"
            >
              <p className="text-secondary-text mb-4">No best sellers found</p>
              <Link
                href="/products"
                className="inline-flex items-center gap-2 px-6 py-3 bg-accent text-white font-medium rounded-button hover:bg-accent-dark transition-all duration-200 shadow-soft"
              >
                Browse All Products
                <ArrowRight className="w-4 h-4" />
              </Link>
            </motion.div>
          )}

          <div className="mt-8 md:hidden text-center">
            <Link
              href="/products"
              className="inline-flex items-center gap-2 text-accent font-medium"
            >
              View All
              <ChevronRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* New Arrivals */}
      <section className="py-16 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection className="text-center mb-12">
            <h2 className="font-serif text-4xl font-semibold text-primary mb-4">
              New Arrivals
            </h2>
            <p className="text-secondary max-w-2xl mx-auto">
              Be the first to discover our latest innovations in luxury skincare.
            </p>
          </AnimatedSection>

          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="bg-surface border border-border rounded-product p-5">
                  <Skeleton className="aspect-[4/5] rounded-product mb-4" />
                  <Skeleton className="h-4 rounded mb-2" />
                  <Skeleton className="h-3 rounded w-2/3 mb-4" />
                  <Skeleton className="h-6 rounded w-1/3" />
                </div>
              ))}
            </div>
          ) : error ? (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center py-12 bg-surface rounded-card border border-border"
            >
              <p className="text-secondary-text mb-4">{error}</p>
              <button
                onClick={fetchProducts}
                className="inline-flex items-center gap-2 px-6 py-3 bg-accent text-white font-medium rounded-button hover:bg-accent-dark transition-all duration-200 shadow-soft"
              >
                Try Again
              </button>
            </motion.div>
          ) : newArrivals.length > 0 ? (
            <motion.div
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-40px" }}
              variants={staggerContainer}
              className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"
            >
              {newArrivals.map((product, index) => (
                <ProductCard
                  key={product.id}
                  product={product}
                  badge="New"
                  index={index}
                />
              ))}
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center py-12 bg-surface rounded-card border border-border"
            >
              <p className="text-secondary-text mb-4">No new arrivals yet</p>
              <Link
                href="/products"
                className="inline-flex items-center gap-2 px-6 py-3 bg-accent text-white font-medium rounded-button hover:bg-accent-dark transition-all duration-200 shadow-soft"
              >
                Browse All Products
                <ArrowRight className="w-4 h-4" />
              </Link>
            </motion.div>
          )}
        </div>
      </section>

      {/* Skin Concerns */}
      <section className="py-16 lg:py-24 bg-surface">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection className="text-center mb-12">
            <h2 className="font-serif text-4xl font-semibold text-primary mb-4">
              Targeted Skin Solutions
            </h2>
            <p className="text-secondary max-w-2xl mx-auto">
              Address your specific skin concerns with our scientifically
              formulated solutions.
            </p>
          </AnimatedSection>

          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-40px" }}
            variants={staggerContainer}
            className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4"
          >
            {skinConcerns.map((concern) => (
              <motion.div
                key={concern.name}
                variants={scaleIn}
                className="cursor-pointer"
              >
                <Link href="/products">
                  <div className="bg-background border border-border rounded-card p-6 text-center transition-all duration-200 hover:shadow-soft hover:-translate-y-1">
                    <div className="text-4xl mb-3">{concern.emoji}</div>
                    <h3 className="font-serif text-base font-medium text-primary">
                      {concern.name}
                    </h3>
                  </div>
                </Link>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* AI Assistant CTA */}
      <section className="py-16 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection>
            <div className="relative bg-surface border border-border rounded-card p-8 lg:p-16 overflow-hidden">
              <div className="absolute top-0 right-0 w-1/2 h-full opacity-5">
                <Bot className="w-full h-full" />
              </div>
              <div className="relative grid lg:grid-cols-2 gap-8 items-center">
                <div>
                  <div className="inline-flex items-center gap-2 px-4 py-2 bg-background rounded-full border border-border mb-6">
                    <Bot className="w-4 h-4 text-accent" />
                    <span className="text-sm font-medium text-secondary">
                      AI-Powered
                    </span>
                  </div>
                  <h2 className="font-serif text-4xl lg:text-5xl font-semibold text-primary mb-6 leading-tight">
                    Your Personal
                    <br />
                    <span className="text-accent">Skincare AI</span>
                  </h2>
                  <p className="text-lg text-secondary leading-relaxed mb-8 max-w-lg">
                    Get personalized skincare recommendations powered by advanced
                    AI. Our system analyzes your skin type, concerns, and goals
                    to create the perfect routine just for you.
                  </p>
                  <div className="flex flex-wrap gap-4">
                    <Link
                      href="/ai"
                      className="inline-flex items-center gap-2 px-8 py-3.5 bg-accent text-white font-medium rounded-button hover:bg-accent-dark transition-all duration-200 shadow-soft"
                    >
                      <Bot className="w-4 h-4" />
                      Start AI Analysis
                      <ArrowRight className="w-4 h-4" />
                    </Link>
                  </div>
                </div>
                <div className="hidden lg:flex items-center justify-center">
                  <motion.div
                    animate={{
                      y: [0, -10, 0],
                      rotate: [0, 2, -2, 0],
                    }}
                    transition={{
                      duration: 4,
                      repeat: Infinity,
                      ease: [0.4, 0, 0.2, 1] as const,
                    }}
                    className="w-64 h-64 bg-gradient-to-br from-accent/10 to-accent/5 rounded-full flex items-center justify-center border border-accent/20"
                  >
                    <Bot className="w-32 h-32 text-accent opacity-60" />
                  </motion.div>
                </div>
              </div>
            </div>
          </AnimatedSection>
        </div>
      </section>

      {/* Authenticity & Trust */}
      <section className="py-16 lg:py-24 bg-surface">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection className="text-center mb-12">
            <h2 className="font-serif text-4xl font-semibold text-primary mb-4">
              The Aura Promise
            </h2>
            <p className="text-secondary max-w-2xl mx-auto">
              Every product we create is backed by our commitment to quality,
              purity, and transparency.
            </p>
          </AnimatedSection>

          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-40px" }}
            variants={staggerContainer}
            className="grid md:grid-cols-3 gap-6"
          >
            <motion.div variants={fadeIn} className="bg-background border border-border rounded-card p-8 text-center">
              <ShieldCheck className="w-12 h-12 text-accent mx-auto mb-4" />
              <h3 className="font-serif text-xl font-semibold text-primary mb-3">
                100% Authentic
              </h3>
              <p className="text-secondary text-sm leading-relaxed">
                Every product is verified for authenticity. We source directly
                from manufacturers and guarantee the real deal.
              </p>
            </motion.div>
            <motion.div variants={fadeIn} className="bg-background border border-border rounded-card p-8 text-center">
              <Leaf className="w-12 h-12 text-accent mx-auto mb-4" />
              <h3 className="font-serif text-xl font-semibold text-primary mb-3">
                Clean Formulations
              </h3>
              <p className="text-secondary text-sm leading-relaxed">
                Free from parabens, sulfates, and harmful chemicals. Only the
                purest, most effective ingredients.
              </p>
            </motion.div>
            <motion.div variants={fadeIn} className="bg-background border border-border rounded-card p-8 text-center">
              <Repeat className="w-12 h-12 text-accent mx-auto mb-4" />
              <h3 className="font-serif text-xl font-semibold text-primary mb-3">
                Satisfaction Guaranteed
              </h3>
              <p className="text-secondary text-sm leading-relaxed">
                Love your results or get your money back. We stand behind every
                product we sell.
              </p>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection className="text-center mb-12">
            <h2 className="font-serif text-4xl font-semibold text-primary mb-4">
              What Our Customers Say
            </h2>
            <p className="text-secondary max-w-2xl mx-auto">
              Real stories from real people who have transformed their skin with
              Aura Skincare.
            </p>
          </AnimatedSection>

          <AnimatedSection>
            <div className="grid md:grid-cols-3 gap-6">
              {testimonials.map((testimonial, index) => (
                <TestimonialCard
                  key={testimonial.name}
                  testimonial={testimonial}
                  isActive={activeTestimonial === index}
                  onClick={() => setActiveTestimonial(index)}
                />
              ))}
            </div>
          </AnimatedSection>
        </div>
      </section>

      {/* Instagram Gallery */}
      <section className="py-16 lg:py-24 bg-surface">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection className="text-center mb-12">
            <h2 className="font-serif text-4xl font-semibold text-primary mb-4">
              Follow Us
            </h2>
            <p className="text-secondary max-w-2xl mx-auto">
              Join our community on Instagram for skincare tips, behind-the-scenes,
              and exclusive content.
            </p>
          </AnimatedSection>

          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-40px" }}
            variants={staggerContainer}
            className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4"
          >
            {[...Array(6)].map((_, i) => (
              <motion.div
                key={i}
                variants={scaleIn}
                className="aspect-square bg-gradient-to-br from-surface to-border rounded-product flex items-center justify-center cursor-pointer hover:shadow-soft transition-all duration-200"
              >
                <Camera className="w-8 h-8 text-accent opacity-40" />
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Newsletter */}
      <section className="py-16 lg:py-24">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <AnimatedSection className="text-center">
            <h2 className="font-serif text-4xl font-semibold text-primary mb-4">
              Join the Aura Community
            </h2>
            <p className="text-secondary mb-8">
              Subscribe to receive exclusive offers, skincare tips, and early
              access to new products.
            </p>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                setSubscribed(true);
                setTimeout(() => setSubscribed(false), 3000);
              }}
              className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto"
            >
              <label htmlFor="newsletter-email" className="sr-only">
                Email address
              </label>
              <input
                id="newsletter-email"
                type="email"
                required
                placeholder="Enter your email"
                aria-label="Email address for newsletter"
                className="flex-1 px-5 py-3.5 bg-background border border-border rounded-input text-primary placeholder:text-secondary-text focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-all"
              />
              <motion.button
                type="submit"
                aria-label="Subscribe to newsletter"
                className="px-8 py-3.5 bg-accent text-white font-medium rounded-button hover:bg-accent-dark transition-all duration-200 shadow-soft whitespace-nowrap"
                whileTap={{ scale: 0.97 }}
              >
                {subscribed ? "Subscribed!" : "Subscribe"}
              </motion.button>
            </form>
            <AnimatePresence>
              {subscribed && (
                <motion.p
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  className="text-accent text-sm mt-3 font-medium"
                  role="status"
                  aria-live="polite"
                >
                  Thank you for subscribing!
                </motion.p>
              )}
            </AnimatePresence>
          </AnimatedSection>
        </div>
      </section>
    </div>
  );
}
