import { create } from 'zustand';

interface WishlistItem {
  id: string;
  product_id: string;
  product_variant_id?: string | null;
}

interface WishlistState {
  items: WishlistItem[];
  isLoading: boolean;
  setItems: (items: WishlistItem[]) => void;
  addItem: (item: WishlistItem) => void;
  removeItem: (productId: string) => void;
  setLoading: (isLoading: boolean) => void;
  isInWishlist: (productId: string) => boolean;
}

export const useWishlistStore = create<WishlistState>((set, get) => ({
  items: [],
  isLoading: false,
  
  setItems: (items) => set({ items }),
  
  addItem: (item) => set((state) => ({
    items: [...state.items, item]
  })),
  
  removeItem: (productId) => set((state) => ({
    items: state.items.filter(i => i.product_id !== productId)
  })),
  
  setLoading: (isLoading) => set({ isLoading }),
  
  isInWishlist: (productId) => {
    return get().items.some(item => item.product_id === productId);
  }
}));
