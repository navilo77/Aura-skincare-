import { create } from 'zustand';

interface CartItem {
  id: string;
  product_id: string;
  product_variant_id?: string | null;
  quantity: number;
  unit_price: number;
  subtotal: number;
  product_name?: string | null;
  thumbnail_url?: string | null;
  notes?: string | null;
}

interface CartState {
  items: CartItem[];
  isDrawerOpen: boolean;
  isLoading: boolean;
  setItems: (items: CartItem[]) => void;
  addItem: (item: CartItem) => void;
  removeItem: (itemId: string) => void;
  updateQuantity: (itemId: string, quantity: number) => void;
  clearCart: () => void;
  setDrawerOpen: (isOpen: boolean) => void;
  setLoading: (isLoading: boolean) => void;
  getTotalItems: () => number;
  getTotalAmount: () => number;
}

export const useCartStore = create<CartState>((set, get) => ({
  items: [],
  isDrawerOpen: false,
  isLoading: false,
  
  setItems: (items) => set({ items }),
  
  addItem: (item) => set((state) => {
    const existingItem = state.items.find(i => i.product_id === item.product_id && i.product_variant_id === item.product_variant_id);
    if (existingItem) {
      return {
        items: state.items.map(i => 
          i.id === existingItem.id 
            ? { ...i, quantity: i.quantity + item.quantity, subtotal: (i.quantity + item.quantity) * i.unit_price }
            : i
        )
      };
    }
    return { items: [...state.items, item] };
  }),
  
  removeItem: (itemId) => set((state) => ({
    items: state.items.filter(i => i.id !== itemId)
  })),
  
  updateQuantity: (itemId, quantity) => set((state) => ({
    items: state.items.map(i => 
      i.id === itemId 
        ? { ...i, quantity, subtotal: quantity * i.unit_price }
        : i
    )
  })),
  
  clearCart: () => set({ items: [] }),
  
  setDrawerOpen: (isOpen) => set({ isDrawerOpen: isOpen }),
  
  setLoading: (isLoading) => set({ isLoading }),
  
  getTotalItems: () => {
    return get().items.reduce((total, item) => total + item.quantity, 0);
  },
  
  getTotalAmount: () => {
    return get().items.reduce((total, item) => total + item.subtotal, 0);
  }
}));
