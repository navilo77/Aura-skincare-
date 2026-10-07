'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import {
  Star,
  Minus,
  Plus,
  Heart,
  Truck,
  ShieldCheck,
  RotateCcw,
  Sparkles,
  ChevronRight,
  ShoppingCart,
} from 'lucide-react';
import { Skeleton } from '@/components/ui/skeleton';
import { cn } from '@/lib/utils';

import { Product } from "@/lib/services/product.service";

import { useProduct, useProducts } from '@/lib/hooks/useProducts';
import { useCartStore } from '@/lib/store/useCartStore';
import { cartService } from '@/lib/services/cart.service';
import { useWishlistStore } from '@/lib/store/useWishlistStore';

const CONTAINER_VARIANTS = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.06, delayChildren: 0.1 },
  },
};

const ITEM_VARIANTS = {
  hidden: { opacity: 0, y: 14 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.25 },
  },
};

const TAB_CONTENT_VARIANTS = {
  hidden: { opacity: 0, y: 10 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.2 },
  },
  exit: {
    opacity: 0,
    y: -10,
    transition: { duration: 0.15 },
  },
};

export default function ProductDetailPage({ params }: { params: { id: string } }) {
  const [quantity, setQuantity] = useState(1);
  const [activeTab, setActiveTab] = useState('description');
  const [selectedImage, setSelectedImage] = useState(0);
  const [isZoomed, setIsZoomed] = useState(false);
  const [isAddingToCart, setIsAddingToCart] = useState(false);
  const [isAddingToWishlist, setIsAddingToWishlist] = useState(false);
  const [showMobileBar, setShowMobileBar] = useState(false);
  const [addedToCart, setAddedToCart] = useState(false);

  const productId = params.id;
  const { data: product, isLoading: loading, error, refetch } = useProduct(productId);
  const { data: allProducts } = useProducts({ limit: 5 });
  
  const cartStore = useCartStore();
  const wishlistStore = useWishlistStore();

  const relatedProducts = (allProducts || []).filter((p) => p.id !== productId).slice(0, 4);

  useEffect(() => {
    const onScroll = () => {
      setShowMobileBar(window.scrollY > 300);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const incrementQuantity = () => {
    if (product && quantity < product.stock_quantity) {
      setQuantity((q) => q + 1);
    }
  };

  const decrementQuantity = () => {
    setQuantity((q) => (q > 1 ? q - 1 : 1));
  };

  const handleAddToCart = async () => {
    if (!product) return;
    setIsAddingToCart(true);
    try {
      const addedItem = await cartService.addItem(product.id, quantity);
      cartStore.addItem({
        ...addedItem,
        product_name: product.name,
        thumbnail_url: product.thumbnail_url,
      });
      cartStore.setDrawerOpen(true);
      setAddedToCart(true);
      setTimeout(() => setAddedToCart(false), 2000);
    } catch {
      // silent fail
    } finally {
      setIsAddingToCart(false);
    }
  };

  const handleAddToWishlist = async () => {
    if (!product) return;
    setIsAddingToWishlist(true);
    try {
      // Assuming a wishlistService would be here, but we will use the local store for now
      wishlistStore.addItem({
        id: product.id,
        product_id: product.id,
      });
    } catch {
      // silent fail
    } finally {
      setIsAddingToWishlist(false);
    }
  };

  const getInitials = (name: string) => {
    const words = name.trim().split(/\s+/);
    if (words.length >= 2) return (words[0][0] + words[words.length - 1][0]).toUpperCase();
    return name.slice(0, 2).toUpperCase();
  };

  const currencySymbol = (product?.currency === 'EUR' ? '€' : product?.currency === 'GBP' ? '£' : '$');
  const price = product?.price ?? 0;
  const oldPrice = product?.old_price;
  const hasDiscount = typeof oldPrice === 'number' && oldPrice > price;
  const discountPercent = hasDiscount ? Math.round(((oldPrice! - price) / oldPrice!) * 100) : 0;
  const isInStock = product ? product.stock_quantity > 0 : false;

  const allImages = product?.images?.filter(Boolean) || (product?.thumbnail_url ? [product.thumbnail_url] : []);
  const displayImage = allImages[selectedImage] || '';

  const tabs = [
    { id: 'description', label: 'Description' },
    { id: 'ingredients', label: 'Ingredients' },
    { id: 'benefits', label: 'Benefits' },
    { id: 'directions', label: 'Directions' },
    { id: 'reviews', label: 'Reviews' },
  ];

  const trustBadges = [
    { icon: ShieldCheck, label: 'Authenticity Guaranteed' },
    { icon: Truck, label: 'Free Shipping' },
    { icon: RotateCcw, label: '30-Day Returns' },
  ];

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-10">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-14">
            <div className="space-y-4">
              <Skeleton className="aspect-square md:aspect-[4/5] w-full rounded-card" />
              <div className="flex gap-3">
                <Skeleton className="w-16 h-16 md:w-20 md:h-20 rounded-lg flex-shrink-0" />
                <Skeleton className="w-16 h-16 md:w-20 md:h-20 rounded-lg flex-shrink-0" />
                <Skeleton className="w-16 h-16 md:w-20 md:h-20 rounded-lg flex-shrink-0" />
                <Skeleton className="w-16 h-16 md:w-20 md:h-20 rounded-lg flex-shrink-0" />
              </div>
            </div>
            <div className="flex flex-col gap-5 md:gap-6">
              <Skeleton className="h-10 w-3/4 rounded" />
              <Skeleton className="h-5 w-1/2 rounded" />
              <Skeleton className="h-12 w-1/3 rounded" />
              <Skeleton className="h-24 w-full rounded" />
              <div className="flex flex-col sm:flex-row gap-3">
                <Skeleton className="h-14 w-32 rounded-button" />
                <Skeleton className="h-14 flex-1 rounded-button" />
                <Skeleton className="h-14 w-14 rounded-button" />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4 bg-background">
        <p className="text-xl text-secondary-text">Failed to load product</p>
        <p className="text-secondary-text">{error.message || 'An error occurred'}</p>
        <button
          onClick={() => refetch()}
          className="inline-flex items-center gap-2 px-6 py-3 bg-accent text-white font-medium rounded-button hover:bg-accent-dark transition-all duration-200 shadow-soft"
        >
          <ShoppingCart size={18} />
          Try Again
        </button>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4 bg-background">
        <p className="text-xl text-secondary-text">Product not found</p>
        <Link
          href="/products"
          className="inline-flex items-center gap-2 px-6 py-3 bg-accent text-white font-medium rounded-button hover:bg-accent-dark transition-all duration-200 shadow-soft"
        >
          <ShoppingCart size={18} />
          Browse Products
        </Link>
      </div>
    );
  }

  return (
    <motion.div
      variants={CONTAINER_VARIANTS}
      initial="hidden"
      animate="visible"
      className="min-h-screen pb-24 md:pb-0 bg-background text-foreground"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-10">
        <motion.nav variants={ITEM_VARIANTS} className="flex items-center gap-2 text-sm mb-6 md:mb-8 flex-wrap">
          <Link href="/" className="text-secondary-text hover:text-accent transition-colors duration-150">
            Home
          </Link>
          <ChevronRight size={14} className="text-border" />
          <Link href={`/products?category=${encodeURIComponent(product.category || '')}`} className="transition-colors duration-150 hover:text-accent">
            {product.category || 'Products'}
          </Link>
          <ChevronRight size={14} className="text-border" />
          <span className="font-medium truncate text-foreground">
            {product.name}
          </span>
        </motion.nav>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-14 mb-14 md:mb-20">
          <motion.div variants={ITEM_VARIANTS} className="space-y-4">
            <div
              className="relative rounded-card overflow-hidden aspect-square md:aspect-[4/5] cursor-crosshair bg-surface"
              onMouseEnter={() => setIsZoomed(true)}
              onMouseLeave={() => setIsZoomed(false)}
            >
              {displayImage ? (
                <motion.img
                  key={selectedImage}
                  src={displayImage}
                  alt={product.name}
                  className="w-full h-full object-cover"
                  initial={{ opacity: 0, scale: 1.05 }}
                  animate={{ opacity: 1, scale: isZoomed ? 1.15 : 1 }}
                  transition={{ duration: 0.25, ease: 'easeOut' }}
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <span className="font-serif text-6xl md:text-7xl font-semibold tracking-wider text-accent opacity-35">
                    {getInitials(product.name)}
                  </span>
                </div>
              )}
              {hasDiscount && (
                <span className="absolute top-4 left-4 px-3 py-1.5 text-xs font-semibold tracking-wide uppercase rounded-full bg-accent text-white">
                  -{discountPercent}%
                </span>
              )}
              {!isInStock && (
                <div className="absolute inset-0 flex items-center justify-center bg-black/20 backdrop-blur-[2px]">
                  <span className="px-4 py-2 rounded-full text-sm font-medium bg-background/90 text-foreground">
                    Out of Stock
                  </span>
                </div>
              )}
            </div>

            {allImages.length > 1 && (
              <div className="flex gap-3 overflow-x-auto pb-1 scrollbar-hide" role="group" aria-label="Product image gallery">
                {allImages.map((img, idx) => (
                  <button
                    key={idx}
                    onClick={() => setSelectedImage(idx)}
                    aria-label={`View product image ${idx + 1}`}
                    aria-pressed={selectedImage === idx}
                    className={cn(
                      "flex-shrink-0 w-16 h-16 md:w-20 md:h-20 rounded-lg overflow-hidden border-2 transition-all duration-200",
                      selectedImage === idx ? "border-accent opacity-100" : "border-border opacity-70"
                    )}
                  >
                    <img src={img} alt={`${product.name} view ${idx + 1}`} className="w-full h-full object-cover" />
                  </button>
                ))}
              </div>
            )}
          </motion.div>

          <motion.div variants={ITEM_VARIANTS} className="flex flex-col gap-5 md:gap-6">
            <div>
              <h1 className="font-serif text-3xl md:text-4xl lg:text-[2.75rem] font-semibold leading-tight tracking-tight">
                {product.name}
              </h1>

              <div className="flex items-center gap-3 mt-4">
                {product.rating ? (
                  <>
              <div className="flex items-center gap-1">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star
                    key={i}
                    size={18}
                    className={i < Math.floor(product.rating!) ? 'fill-accent text-accent' : 'text-border opacity-40'}
                  />
                ))}
              </div>
              <span className="text-sm font-medium text-foreground">
                {product.rating.toFixed(1)}
              </span>
              <span className="text-sm text-secondary-text">
                ({product.review_count ?? 0} reviews)
              </span>
                  </>
                ) : (
                  <span className="text-sm text-secondary-text">
                    No reviews yet
                  </span>
                )}
              </div>

              <div className="flex items-baseline gap-3 mt-4">
                <span className="text-3xl md:text-4xl font-semibold tracking-tight text-foreground">
                  {currencySymbol}{price.toFixed(2)}
                </span>
                {hasDiscount && (
                  <>
                    <span className="text-xl line-through text-secondary-text">
                      {currencySymbol}{oldPrice!.toFixed(2)}
                    </span>
                    <span className="text-sm font-semibold px-2 py-0.5 rounded-full bg-accent/10 text-accent">
                      Save {discountPercent}%
                    </span>
                  </>
                )}
              </div>
            </div>

            <p className="text-base leading-relaxed text-secondary-text">
              {product.description || 'A luxurious formulation designed to nourish, protect, and revitalize your skin with the finest ingredients.'}
            </p>

            <div className="flex flex-wrap gap-4 text-sm text-secondary-text">
              {product.sku && (
                <span className="px-3 py-1.5 rounded-lg bg-surface border border-border">
                  SKU: <span className="font-medium text-foreground">{product.sku}</span>
                </span>
              )}
              <span
                className={cn(
                  "px-3 py-1.5 rounded-lg flex items-center gap-1.5",
                  isInStock ? "border-success/20 text-success bg-success/5" : "border-error/20 text-error bg-error/5"
                )}
              >
                <span className="w-1.5 h-1.5 rounded-full bg-current" />
                {isInStock ? `In Stock (${product.stock_quantity} available)` : 'Out of Stock'}
              </span>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 pt-1">
            <div className="flex items-center rounded-button border border-border overflow-hidden">
              <button
                onClick={decrementQuantity}
                disabled={quantity <= 1}
                aria-label="Decrease quantity"
                className="px-4 py-3 transition-colors duration-150 disabled:opacity-40 hover:bg-surface text-foreground"
              >
                <Minus size={16} />
              </button>
              <span className="px-5 py-3 font-medium text-base min-w-[3rem] text-center select-none text-foreground">
                {quantity}
              </span>
              <button
                onClick={incrementQuantity}
                disabled={!isInStock || quantity >= product.stock_quantity}
                aria-label="Increase quantity"
                className="px-4 py-3 transition-colors duration-150 disabled:opacity-40 hover:bg-surface text-foreground"
              >
                <Plus size={16} />
              </button>
            </div>

              <motion.button
                whileTap={{ scale: 0.97 }}
                onClick={handleAddToCart}
                disabled={!isInStock || isAddingToCart}
                className="flex-1 flex items-center justify-center gap-2 px-6 py-3.5 rounded-button text-white font-semibold text-base transition-all duration-200 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed bg-accent"
              >
                <ShoppingCart size={18} />
                {addedToCart ? 'Added!' : isAddingToCart ? 'Adding...' : 'Add to Cart'}
              </motion.button>

              <motion.button
                whileTap={{ scale: 0.95 }}
                onClick={handleAddToWishlist}
                disabled={isAddingToWishlist}
                aria-label="Add to wishlist"
                className="px-5 py-3.5 rounded-button border-2 border-border flex items-center justify-center transition-all duration-200 hover:bg-surface disabled:opacity-50 text-foreground"
              >
                <Heart size={18} />
              </motion.button>
            </div>

            <motion.button
              whileTap={{ scale: 0.97 }}
              onClick={() => {
                const params = new URLSearchParams({ product_id: product.id, product_name: product.name, product_price: String(price) });
                window.location.href = `/ai?${params.toString()}`;
              }}
              className="w-full flex items-center justify-center gap-2 px-6 py-3.5 rounded-button border-2 border-accent font-medium text-base transition-all duration-200 hover:shadow-md text-accent bg-transparent"
            >
              <Sparkles size={18} />
              Ask AI for Recommendations
            </motion.button>

            <div className="flex flex-wrap gap-4 pt-2">
              {trustBadges.map(({ icon: Icon, label }) => (
                <div key={label} className="flex items-center gap-2 text-sm text-secondary-text">
                  <Icon size={16} className="text-accent" />
                  <span>{label}</span>
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        <motion.div variants={ITEM_VARIANTS} className="mb-16 md:mb-24">
          <div className="flex border-b border-border overflow-x-auto">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                aria-selected={activeTab === tab.id}
                className="relative px-4 py-3 text-sm font-medium whitespace-nowrap transition-colors duration-200"
              >
                {tab.label}
                {activeTab === tab.id && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute bottom-0 left-0 right-0 h-[2px] bg-accent"
                    transition={{ type: 'spring', stiffness: 300, damping: 25 }}
                  />
                )}
              </button>
            ))}
          </div>

          <div className="mt-6 relative min-h-[120px]">
            <AnimatePresence mode="wait">
              {activeTab === 'description' && (
                <motion.div key="description" variants={TAB_CONTENT_VARIANTS} initial="hidden" animate="visible" exit="exit" className="text-base leading-relaxed text-secondary-text">
                  {product.description || 'A luxurious formulation designed to nourish, protect, and revitalize your skin with the finest ingredients. Crafted with care for a radiant complexion.'}
                </motion.div>
              )}
              {activeTab === 'ingredients' && (
                <motion.div key="ingredients" variants={TAB_CONTENT_VARIANTS} initial="hidden" animate="visible" exit="exit" className="text-base leading-relaxed text-secondary-text">
                  <p className="mb-3 font-medium text-foreground">Key Ingredients</p>
                  <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {(product.ingredients
                      ? product.ingredients.split(',').map((i) => i.trim()).filter(Boolean)
                      : ['Hyaluronic Acid', 'Niacinamide', 'Vitamin C', 'Peptide Complex', 'Ceramides', 'Botanical Extracts']
                    ).map((ing, i) => (
                      <li key={i} className="flex items-center gap-2 text-sm">
                        <span className="w-1.5 h-1.5 rounded-full flex-shrink-0 bg-accent" />
                        {ing}
                      </li>
                    ))}
                  </ul>
                </motion.div>
              )}
              {activeTab === 'benefits' && (
                <motion.div key="benefits" variants={TAB_CONTENT_VARIANTS} initial="hidden" animate="visible" exit="exit" className="text-base leading-relaxed text-secondary-text">
                  <ul className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {(product.benefits && product.benefits.length > 0
                      ? product.benefits
                      : [
                          'Deeply hydrates and plumps skin',
                          'Brightens and evens skin tone',
                          'Reduces fine lines and wrinkles',
                          'Strengthens skin barrier',
                          'Soothes and calms irritation',
                          'Improves overall radiance',
                        ]
                    ).map((benefit, i) => (
                      <li key={i} className="flex items-start gap-2.5 text-sm">
                        <span className="mt-0.5 w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 bg-accent/10">
                          <Sparkles size={12} className="text-accent" />
                        </span>
                        {benefit}
                      </li>
                    ))}
                  </ul>
                </motion.div>
              )}
              {activeTab === 'directions' && (
                <motion.div key="directions" variants={TAB_CONTENT_VARIANTS} initial="hidden" animate="visible" exit="exit" className="text-base leading-relaxed text-secondary-text">
                  {product.directions || (
                    <>
                      <p className="mb-3">Apply a small amount to clean, dry skin. Gently massage in upward circular motions until fully absorbed.</p>
                      <p>Use morning and evening for best results. Follow with sunscreen during the day. For external use only. Avoid direct contact with eyes.</p>
                    </>
                  )}
                </motion.div>
              )}
              {activeTab === 'reviews' && (
                <motion.div key="reviews" variants={TAB_CONTENT_VARIANTS} initial="hidden" animate="visible" exit="exit" className="space-y-4">
                  {product.reviews && product.reviews.length > 0 ? (
                    product.reviews.map((review) => (
                      <div key={review.id} className="p-4 rounded-card bg-surface border border-border">
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-medium text-sm text-foreground">{review.author}</span>
                          <span className="text-xs text-secondary-text">{review.date}</span>
                        </div>
                        <div className="flex gap-0.5 mb-2">
                          {Array.from({ length: 5 }).map((_, i) => (
                            <Star key={i} size={14} className={i < review.rating ? 'fill-accent text-accent' : 'text-border opacity-30'} />
                          ))}
                        </div>
                        <p className="text-sm text-secondary-text">{review.text}</p>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-10">
                      <p className="text-base mb-2 text-secondary-text">No reviews yet</p>
                      <p className="text-sm text-secondary-text opacity-70">Be the first to share your experience with this product.</p>
                    </div>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>

        {relatedProducts.length > 0 && (
          <motion.section variants={ITEM_VARIANTS} className="mb-10">
            <h2 className="font-serif text-2xl md:text-3xl font-semibold tracking-tight mb-6 md:mb-8">You May Also Love</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
              {relatedProducts.map((rp, idx) => (
                <motion.div
                  key={rp.id}
                  variants={ITEM_VARIANTS}
                  whileHover={{ y: -4 }}
                  transition={{ duration: 0.2, ease: 'easeOut' }}
                  onClick={() => (window.location.href = `/products/${rp.id}`)}
                  className="cursor-pointer rounded-xl overflow-hidden group bg-surface border border-border"
                  role="link"
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      window.location.href = `/products/${rp.id}`;
                    }
                  }}
                >
                  <div className="aspect-square overflow-hidden">
                    {rp.thumbnail_url ? (
                      <img src={rp.thumbnail_url} alt={rp.name} className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105" />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center">
                        <span className="font-serif text-2xl font-semibold text-accent opacity-30">
                          {getInitials(rp.name)}
                        </span>
                      </div>
                    )}
                  </div>
                  <div className="p-3 md:p-4">
                    <h3 className="font-serif text-sm md:text-base font-medium truncate mb-1">{rp.name}</h3>
                    <p className="text-sm font-semibold text-accent">
                      ${rp.price.toFixed(2)}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.section>
        )}
      </div>

      <AnimatePresence>
        {showMobileBar && (
          <motion.div
            initial={{ y: '100%', opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: '100%', opacity: 0 }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            className="fixed bottom-0 left-0 right-0 z-50 md:hidden px-4 py-3 flex gap-3 items-center bg-background border-t border-border shadow-soft"
          >
            <div className="flex items-center rounded-button border border-border overflow-hidden">
              <button onClick={decrementQuantity} disabled={quantity <= 1} aria-label="Decrease quantity" className="px-3 py-2 disabled:opacity-40 text-foreground">
                <Minus size={16} />
              </button>
              <span className="px-4 py-2 font-medium text-sm min-w-[2.5rem] text-center select-none text-foreground">
                {quantity}
              </span>
              <button onClick={incrementQuantity} disabled={!isInStock || quantity >= product.stock_quantity} aria-label="Increase quantity" className="px-3 py-2 disabled:opacity-40 text-foreground">
                <Plus size={16} />
              </button>
            </div>
            <motion.button
              whileTap={{ scale: 0.97 }}
              onClick={handleAddToCart}
              disabled={!isInStock}
              className="flex-1 flex items-center justify-center gap-2 py-3 rounded-button text-white font-semibold text-sm transition-all duration-200 bg-accent"
            >
              <ShoppingCart size={16} />
              {addedToCart ? 'Added!' : 'Add to Cart'}
            </motion.button>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
