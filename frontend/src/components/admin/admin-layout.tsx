'use client';

import { useState, useEffect, type ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LayoutDashboard,
  Package,
  FolderTree,
  Tag,
  Warehouse,
  ClipboardList,
  TicketPercent,
  Image as ImageIcon,
  Settings,
  AlertTriangle,
  CalendarCheck,
  Workflow,
  Activity,
  LogOut,
  Menu,
} from 'lucide-react';

const navItems = [
  { href: '/admin/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/admin/products', label: 'Products', icon: Package },
  { href: '/admin/categories', label: 'Categories', icon: FolderTree },
  { href: '/admin/brands', label: 'Brands', icon: Tag },
  { href: '/admin/inventory-dashboard', label: 'Inventory', icon: Warehouse },
  { href: '/admin/stock-alerts', label: 'Stock Alerts', icon: AlertTriangle },
  { href: '/admin/reservations', label: 'Reservations', icon: CalendarCheck },
  { href: '/admin/orders', label: 'Orders', icon: ClipboardList },
  { href: '/admin/coupons', label: 'Coupons', icon: TicketPercent },
  { href: '/admin/banners', label: 'Banners', icon: ImageIcon },
  { href: '/admin/automation-jobs', label: 'Automation', icon: Workflow },
  { href: '/admin/order-timeline', label: 'Order Timeline', icon: Activity },
  { href: '/admin/settings', label: 'Settings', icon: Settings },
];

interface AdminLayoutProps {
  children: ReactNode;
}

export function AdminLayout({ children }: AdminLayoutProps) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('admin_token');
    if (!token) {
      router.push('/admin/login');
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('admin_token');
    router.push('/admin/login');
  };

  const SidebarContent = ({ onCloseMobile }: { onCloseMobile?: () => void }) => (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-3 px-6 py-6">
        <div className="w-9 h-9 rounded-xl bg-accent flex items-center justify-center shadow-soft">
          <span className="text-white font-serif font-bold text-lg">A</span>
        </div>
        <span className="font-serif text-xl font-semibold text-foreground tracking-tight">
          Aura Admin
        </span>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={onCloseMobile}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group ${
                isActive
                  ? 'bg-accent/10 text-accent'
                  : 'text-secondary-text hover:bg-surface hover:text-foreground'
              }`}
            >
              <Icon
                className={`w-5 h-5 flex-shrink-0 ${
                  isActive ? 'text-accent' : 'text-secondary-text group-hover:text-foreground'
                }`}
              />
              <span className="text-sm font-medium whitespace-nowrap">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="px-3 py-4 border-t border-border">
        <button
          onClick={() => {
            handleLogout();
            onCloseMobile?.();
          }}
          className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-secondary-text hover:text-error hover:bg-error/5 transition-all duration-200 w-full"
        >
          <LogOut className="w-5 h-5 flex-shrink-0" />
          <span className="text-sm font-medium whitespace-nowrap">Logout</span>
        </button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-background">
      <button
        onClick={() => setMobileOpen(true)}
        className="lg:hidden fixed top-4 left-4 z-50 w-10 h-10 bg-background border border-border rounded-xl flex items-center justify-center shadow-soft"
      >
        <Menu className="w-5 h-5 text-foreground" />
      </button>

      <AnimatePresence>
        {mobileOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setMobileOpen(false)}
              className="lg:hidden fixed inset-0 bg-black/20 backdrop-blur-sm z-40"
            />
            <motion.aside
              initial={{ x: '-100%' }}
              animate={{ x: 0 }}
              exit={{ x: '-100%' }}
              transition={{ duration: 0.25, ease: 'easeOut' }}
              className="lg:hidden fixed left-0 top-0 bottom-0 w-72 bg-background border-r border-border z-50 shadow-premium"
            >
              <SidebarContent onCloseMobile={() => setMobileOpen(false)} />
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      <aside className="hidden lg:flex fixed left-0 top-0 bottom-0 w-[260px] bg-background border-r border-border flex-col z-30 shadow-soft">
        <SidebarContent />
      </aside>

      <main className="lg:ml-[260px] min-h-screen transition-all duration-250">
        <div className="p-4 md:p-8 lg:p-10 max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
