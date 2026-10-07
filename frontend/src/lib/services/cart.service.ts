import { api } from '../api';

export interface CartItem {
  id: string;
  cart_id: string;
  product_id: string;
  product_variant_id?: string | null;
  quantity: number;
  unit_price: number;
  subtotal: number;
  product_name?: string | null;
  thumbnail_url?: string | null;
}

export interface Cart {
  id: string;
  user_id: string;
  items: CartItem[];
}

export const cartService = {
  getCart: async () => {
    const response = await api.get<Cart>('/cart');
    return response.data;
  },
  
  addItem: async (productId: string, quantity: number, variantId?: string) => {
    const response = await api.post<CartItem>('/cart/items', {
      product_id: productId,
      quantity,
      product_variant_id: variantId
    });
    return response.data;
  },
  
  updateItem: async (itemId: string, quantity: number) => {
    const response = await api.patch<CartItem>(`/cart/items/${itemId}`, { quantity });
    return response.data;
  },
  
  removeItem: async (itemId: string) => {
    await api.delete(`/cart/items/${itemId}`);
  },
  
  clearCart: async () => {
    await api.delete('/cart');
  }
};
