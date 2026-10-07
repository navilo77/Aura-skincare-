import { api } from '../api';

export interface Product {
  id: string;
  name: string;
  slug: string;
  sku: string;
  price: number;
  compare_at_price?: number | null;
  currency: string;
  thumbnail_url?: string | null;
  is_featured: boolean;
  is_active: boolean;
  brand_id: string;
  category_id: string;
  short_description?: string | null;
  description?: string | null;
  status: string;
  product_type: string;
  stock_quantity: number;
  // Extra UI fields that might not be in backend yet
  images?: string[] | null;
  old_price?: number | null;
  rating?: number | null;
  review_count?: number | null;
  ingredients?: string | null;
  benefits?: string[] | null;
  directions?: string | null;
  category?: string | null;
  reviews?: Array<{ id: string; author: string; rating: number; text: string; date: string }> | null;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  parent_id?: string | null;
  children?: Category[];
}

export const productService = {
  getProducts: async (params?: Record<string, any>) => {
    const response = await api.get<Product[]>('/products', { params });
    return response.data;
  },
  
  getProductById: async (id: string) => {
    const response = await api.get<Product>(`/products/${id}`);
    return response.data;
  },

  getCategories: async () => {
    const response = await api.get<Category[]>('/products/categories/tree');
    return response.data;
  }
};
