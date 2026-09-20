'use client';

import { useState, useEffect, useMemo } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronRight, SlidersHorizontal, X, Heart, Star, Search, Plus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';

interface Product {
  id: string;
  name: string;
  price: number;
  currency: string;
  thumbnail_url?: string;
  sku?: string;
  status?: string;
  is_active?: boolean;
  is_featured?: boolean;
  brand_id?: string;
  category_id?: string;
}

type SortOption = 'newest' | 'price_asc' | 'price_desc' | 'best_selling';
type StatusFilter = 'all' | 'active' | 'inactive';

const PRODUCTS_PER_PAGE = 8;

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [displayCount, setDisplayCount] = useState(PRODUCTS_PER_PAGE);
  const [addingToCart, setAddingToCart] = useState<string | null>(null);

  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState<SortOption>('newest');
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('all');
  const [priceRange, setPriceRange] = useState({ min: '', max: '' });
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);

   const fetchProducts = async () => {
     try {
       setLoading(true);
       const params = new URLSearchParams();
       if (search) params.set('search', search);
       if (statusFilter !== 'all') params.set('status', statusFilter);
       if (priceRange.min) params.set('min_price', priceRange.min);
       if (priceRange.max) params.set('max_price', priceRange.max);
       if (sortBy === 'price_asc') {
         params.set('sort_by', 'price');
         params.set('sort_order', 'asc');
       } else if (sortBy === 'price_desc') {
         params.set('sort_by', 'price');
         params.set('sort_order', 'desc');
       } else if (sortBy === 'best_selling') {
         params.set('sort_by', 'is_featured');
         params.set('sort_order', 'desc');
       }

       const res = await fetch(`/api/products?${params.toString()}`);
       if (!res.ok) throw new Error('Failed to fetch products');
       const data = await res.json();
       setProducts(Array.isArray(data) ? data : []);
     } catch (err) {
       setError(err instanceof Error ? err.message : 'Something went wrong');
     } finally {
       setLoading(false);
     }
   };

   useEffect(() => {
     fetchProducts();
   }, [search, statusFilter, priceRange, sortBy]);

  const uniqueCategories = useMemo(() => {
    return Array.from(new Set(products.map((p) => p.category_id).filter((id): id is string => id !== undefined)));
  }, [products]);

  const filteredProducts = useMemo(() => {
    let result = [...products];

    if (selectedCategories.length > 0) {
      result = result.filter((p) => p.category_id && selectedCategories.includes(p.category_id));
    }

    if (sortBy === 'price_asc') {
      result.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price_desc') {
      result.sort((a, b) => b.price - a.price);
    } else if (sortBy === 'best_selling') {
      result.sort((a, b) => (b.is_featured ? 1 : 0) - (a.is_featured ? 1 : 0));
    }

    return result;
  }, [products, selectedCategories, sortBy]);

  const visibleProducts = filteredProducts.slice(0, displayCount);
  const hasMore = filteredProducts.length > displayCount;

  const addToCart = async (productId: string) => {
    setAddingToCart(productId);
    try {
      await fetch('/api/cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId, quantity: 1 }),
      });
    } catch {
      // silent fail for demo
    } finally {
      setAddingToCart(null);
    }
  };

  const toggleCategory = (catId: string) => {
    setSelectedCategories((prev) =>
      prev.includes(catId) ? prev.filter((c) => c !== catId) : [...prev, catId]
    );
    setDisplayCount(PRODUCTS_PER_PAGE);
  };

  const clearFilters = () => {
    setSearch('');
    setStatusFilter('all');
    setPriceRange({ min: '', max: '' });
    setSelectedCategories([]);
    setSortBy('newest');
    setDisplayCount(PRODUCTS_PER_PAGE);
  };

  const activeFiltersCount =
    (search ? 1 : 0) +
    (statusFilter !== 'all' ? 1 : 0) +
    (priceRange.min || priceRange.max ? 1 : 0) +
    selectedCategories.length;

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.04 } },
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.25 } },
  };

  const sidebarVariants = {
    open: { x: 0, opacity: 1 },
    closed: { x: '-100%', opacity: 0 },
  };

  const renderStars = (rating: number) => {
    return (
      <div className="flex items-center gap-0.5">
        {[1, 2, 3, 4, 5].map((star) => (
          <Star
            key={star}
            size={14}
            className={
              star <= Math.round(rating)
                ? 'fill-accent text-accent'
                : 'text-border'
            }
          />
        ))}
        <span className="text-xs text-secondary-text ml-1">{rating.toFixed(1)}</span>
      </div>
    );
  };

  const ProductSkeleton = () => (
    <div className="bg-surface rounded-product p-4 animate-pulse">
      <Skeleton className="w-full aspect-square mb-4 rounded-product" />
      <Skeleton className="h-5 w-3/4 mb-2" />
      <Skeleton className="h-4 w-1/2 mb-3" />
      <div className="flex items-center gap-2">
        <Skeleton className="h-5 w-16" />
        <Skeleton className="h-4 w-12" />
      </div>
    </div>
  );

  const ProductCard = ({ product }: { product: Product }) => {
    const rating = (product.id.charCodeAt(0) % 30 + 20) / 10;
    const hasDiscount = product.id.charCodeAt(1) % 3 === 0;
    const discountPercent = hasDiscount ? 15 + (product.id.charCodeAt(2) % 25) : 0;
    const originalPrice = hasDiscount ? product.price / (1 - discountPercent / 100) : product.price;

    const badges = [];
    if (product.is_featured) badges.push({ label: 'Best Seller', variant: 'best' as const });
    if (product.is_active && product.status === 'active' && product.id.charCodeAt(3) % 2 === 0)
      badges.push({ label: 'New', variant: 'new' as const });
    if (hasDiscount) badges.push({ label: `-${discountPercent}%`, variant: 'limited' as const });
    if (product.status === 'limited' || product.status === 'low_stock')
      badges.push({ label: 'Limited', variant: 'limited' as const });

    const finalPrice = hasDiscount ? product.price : originalPrice;
    const displayOriginal = hasDiscount ? originalPrice : null;

    return (
      <motion.div
        variants={cardVariants}
        className="group relative bg-surface rounded-product overflow-hidden shadow-soft hover:shadow-premium transition-shadow duration-250"
      >
        <Link href={`/products/${product.id}`} className="block">
          <div className="relative aspect-square overflow-hidden bg-background">
            {product.thumbnail_url ? (
              <img
                src={product.thumbnail_url}
                alt={product.name}
                className="w-full h-full object-cover transition-transform duration-250 group-hover:scale-110"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-secondary-text">
                No Image
              </div>
            )}

            {badges.length > 0 && (
              <div className="absolute top-3 left-3 flex flex-wrap gap-1.5">
                {badges.map((badge) => (
                  <Badge key={badge.label} variant={badge.variant} className="shadow-sm">
                    {badge.label}
                  </Badge>
                ))}
              </div>
            )}

            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              onClick={(e) => {
                e.preventDefault();
              }}
              aria-label="Add to wishlist"
              className="absolute top-3 right-3 p-2 bg-background/80 backdrop-blur-sm rounded-full shadow-soft hover:bg-background transition-colors"
            >
              <Heart size={18} className="text-primary hover:text-error transition-colors" />
            </motion.button>

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              whileHover={{ opacity: 1, y: 0 }}
              className="absolute bottom-3 left-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity duration-250"
            >
              <Button
                size="sm"
                className="w-full rounded-button shadow-premium"
                onClick={(e) => {
                  e.preventDefault();
                  addToCart(product.id);
                }}
                loading={addingToCart === product.id}
              >
                <Plus size={16} className="mr-1.5" />
                Quick Add
              </Button>
            </motion.div>
          </div>
        </Link>

        <div className="p-4">
          <Link href={`/products/${product.id}`} className="block">
            <h3 className="font-serif text-lg font-medium text-primary line-clamp-1 mb-1 group-hover:text-accent transition-colors duration-200">
              {product.name}
            </h3>
            <div className="mb-2">{renderStars(rating)}</div>
            <div className="flex items-center gap-2">
              <span className="text-base font-semibold text-primary">
                {product.currency || '$'} {finalPrice.toFixed(2)}
              </span>
              {displayOriginal && (
                <span className="text-sm text-secondary-text line-through">
                  {product.currency || '$'} {displayOriginal.toFixed(2)}
                </span>
              )}
            </div>
          </Link>
        </div>
      </motion.div>
    );
  };

  const FilterSidebar = ({ isMobile = false }: { isMobile?: boolean }) => (
    <div className={isMobile ? 'p-6' : ''}>
      <div className="flex items-center justify-between mb-6">
        <h2 className="font-serif text-xl font-medium text-primary">Filters</h2>
        {isMobile && (
          <button onClick={() => setSidebarOpen(false)} className="p-1">
            <X size={20} className="text-primary" />
          </button>
        )}
      </div>

      <div className="space-y-6">
        <div>
          <h3 className="text-sm font-semibold text-primary uppercase tracking-wider mb-3">
            Categories
          </h3>
          <div className="space-y-2">
            {uniqueCategories.length === 0 ? (
              <p className="text-sm text-secondary-text">No categories available</p>
            ) : (
              uniqueCategories.map((catId) => (
                <label
                  key={catId}
                  className="flex items-center gap-2 cursor-pointer group"
                >
                  <input
                    type="checkbox"
                    checked={selectedCategories.includes(catId)}
                    onChange={() => toggleCategory(catId)}
                    className="w-4 h-4 rounded border-border text-accent focus:ring-accent"
                  />
                  <span className="text-sm text-primary group-hover:text-accent transition-colors">
                    {catId}
                  </span>
                </label>
              ))
            )}
          </div>
        </div>

        <div>
          <h3 className="text-sm font-semibold text-primary uppercase tracking-wider mb-3">
            Price Range
          </h3>
          <div className="flex items-center gap-2">
            <input
              type="number"
              placeholder="Min"
              value={priceRange.min}
              onChange={(e) => {
                setPriceRange((prev) => ({ ...prev, min: e.target.value }));
                setDisplayCount(PRODUCTS_PER_PAGE);
              }}
              className="w-full px-3 py-2 bg-background border border-border rounded-input text-sm text-primary placeholder:text-secondary-text focus:outline-none focus:border-accent transition-colors"
            />
            <span className="text-secondary-text">-</span>
            <input
              type="number"
              placeholder="Max"
              value={priceRange.max}
              onChange={(e) => {
                setPriceRange((prev) => ({ ...prev, max: e.target.value }));
                setDisplayCount(PRODUCTS_PER_PAGE);
              }}
              className="w-full px-3 py-2 bg-background border border-border rounded-input text-sm text-primary placeholder:text-secondary-text focus:outline-none focus:border-accent transition-colors"
            />
          </div>
        </div>

        <div>
          <h3 className="text-sm font-semibold text-primary uppercase tracking-wider mb-3">
            Status
          </h3>
          <div className="space-y-2">
            {(['all', 'active', 'inactive'] as StatusFilter[]).map((status) => (
              <label key={status} className="flex items-center gap-2 cursor-pointer group">
                <input
                  type="radio"
                  name="status"
                  checked={statusFilter === status}
                  onChange={() => {
                    setStatusFilter(status);
                    setDisplayCount(PRODUCTS_PER_PAGE);
                  }}
                  className="w-4 h-4 border-border text-accent focus:ring-accent"
                />
                <span className="text-sm text-primary capitalize group-hover:text-accent transition-colors">
                  {status === 'all' ? 'All Statuses' : status}
                </span>
              </label>
            ))}
          </div>
        </div>

        {isMobile && (
          <div className="pt-4 border-t border-border">
            <Button
              variant="primary"
              className="w-full rounded-button"
              onClick={() => setSidebarOpen(false)}
            >
              Apply Filters
            </Button>
            <Button
              variant="ghost"
              className="w-full mt-2 rounded-button"
              onClick={clearFilters}
            >
              Clear All
            </Button>
          </div>
        )}
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-background">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.25 }}
        className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-16"
      >
        {/* Breadcrumb */}
        <nav className="flex items-center gap-2 text-sm mb-6">
          <Link href="/" className="text-secondary-text hover:text-accent transition-colors">
            Home
          </Link>
          <ChevronRight size={14} className="text-border" />
          <span className="text-primary font-medium">All Products</span>
        </nav>

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-8">
          <div>
            <h1 className="font-serif text-4xl sm:text-5xl font-medium text-primary mb-2">
              All Products
            </h1>
            <p className="text-secondary-text">
              {loading
                ? 'Discovering products...'
                : `${filteredProducts.length} product${filteredProducts.length !== 1 ? 's' : ''} found`}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="relative">
              <Search
                size={18}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-secondary-text"
              />
               <input
                 type="text"
                 placeholder="Search products..."
                 aria-label="Search products"
                 value={search}
                 onChange={(e) => {
                   setSearch(e.target.value);
                   setDisplayCount(PRODUCTS_PER_PAGE);
                 }}
                 className="pl-10 pr-4 py-2.5 bg-surface border border-border rounded-button text-sm text-primary placeholder:text-secondary-text focus:outline-none focus:border-accent transition-colors w-64"
               />
            </div>

            <div className="relative">
              <select
                value={sortBy}
                onChange={(e) => {
                  setSortBy(e.target.value as SortOption);
                  setDisplayCount(PRODUCTS_PER_PAGE);
                }}
                className="appearance-none pl-4 pr-10 py-2.5 bg-surface border border-border rounded-button text-sm text-primary focus:outline-none focus:border-accent transition-colors cursor-pointer"
              >
                <option value="newest">Newest</option>
                <option value="price_asc">Price: Low to High</option>
                <option value="price_desc">Price: High to Low</option>
                <option value="best_selling">Best Selling</option>
              </select>
              <ChevronRight
                size={16}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-secondary-text rotate-[-90deg] pointer-events-none"
              />
            </div>

            <Button
              variant="secondary"
              size="md"
              className="lg:hidden rounded-button relative"
              onClick={() => setSidebarOpen(true)}
            >
              <SlidersHorizontal size={18} className="mr-2" />
              Filters
              {activeFiltersCount > 0 && (
                <span className="absolute -top-1 -right-1 w-5 h-5 bg-accent text-white text-xs rounded-full flex items-center justify-center">
                  {activeFiltersCount}
                </span>
              )}
            </Button>
          </div>
        </div>

        <div className="flex gap-8">
          {/* Desktop Sidebar */}
          <aside className="hidden lg:block w-64 flex-shrink-0">
            <div className="sticky top-8 bg-surface rounded-card p-6 shadow-soft border border-border">
              <FilterSidebar />
              {activeFiltersCount > 0 && (
                <div className="mt-4 pt-4 border-t border-border">
                  <Button
                    variant="ghost"
                    size="sm"
                    className="w-full rounded-button text-sm"
                    onClick={clearFilters}
                  >
                    Clear All Filters
                  </Button>
                </div>
              )}
            </div>
          </aside>

          {/* Mobile Sidebar Overlay */}
          <AnimatePresence>
            {sidebarOpen && (
              <>
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="fixed inset-0 bg-black/40 z-40 lg:hidden"
                  onClick={() => setSidebarOpen(false)}
                />
                <motion.div
                  initial={{ x: '-100%', opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  exit={{ x: '-100%', opacity: 0 }}
                  transition={{ duration: 0.25 }}
                  className="fixed left-0 top-0 h-full w-80 bg-surface z-50 shadow-premium lg:hidden overflow-y-auto"
                >
                  <FilterSidebar isMobile />
                </motion.div>
              </>
            )}
          </AnimatePresence>

          {/* Product Grid */}
          <main className="flex-1">
             {error ? (
               <motion.div
                 initial={{ opacity: 0, scale: 0.95 }}
                 animate={{ opacity: 1, scale: 1 }}
                 className="text-center py-20 bg-surface rounded-card shadow-soft border border-border"
               >
                 <p className="text-secondary-text text-lg mb-4">{error}</p>
                 <Button variant="primary" onClick={fetchProducts}>
                   Try Again
                 </Button>
               </motion.div>
             ) : loading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {Array.from({ length: 6 }).map((_, i) => (
                  <ProductSkeleton key={i} />
                ))}
              </div>
            ) : visibleProducts.length === 0 ? (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center py-20 bg-surface rounded-card shadow-soft border border-border"
              >
                <div className="w-20 h-20 mx-auto mb-4 bg-background rounded-full flex items-center justify-center">
                  <Search size={32} className="text-secondary-text" />
                </div>
                <h3 className="font-serif text-2xl text-primary mb-2">No products found</h3>
                <p className="text-secondary-text mb-6 max-w-md mx-auto">
                  We couldn&apos;t find any products matching your criteria. Try adjusting your filters or search terms.
                </p>
                <div className="flex items-center justify-center gap-3">
                  <Button variant="primary" onClick={clearFilters}>
                    Clear All Filters
                  </Button>
                  <Link href="/products">
                    <Button variant="outline">Browse All Products</Button>
                  </Link>
                </div>
              </motion.div>
            ) : (
              <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="visible"
                className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
              >
                {visibleProducts.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </motion.div>
            )}

            {/* Load More */}
            {hasMore && !loading && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-12 text-center"
              >
                <Button
                  variant="outline"
                  size="lg"
                  className="rounded-button px-12"
                  onClick={() => setDisplayCount((prev) => prev + PRODUCTS_PER_PAGE)}
                >
                  Load More
                </Button>
              </motion.div>
            )}
          </main>
        </div>
      </motion.div>
    </div>
  );
}
