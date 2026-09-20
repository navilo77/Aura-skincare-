import type { Metadata } from "next";
import { Inter, Playfair_Display } from "next/font/google";
import { ThemeProvider } from "@/components/theme-provider";
import { Navbar } from "@/components/layout/navbar";
import { Footer } from "@/components/layout/footer";
import { MobileBottomNav } from "@/components/layout/mobile-bottom-nav";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const playfair = Playfair_Display({
  subsets: ["latin"],
  variable: "--font-playfair",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000"),
  title: {
    default: "Aura Skincare | Pure Formulations, Luminous Skin",
    template: "%s | Aura Skincare",
  },
  description: "Discover luxury skincare formulated with pure ingredients. AI-powered beauty commerce platform offering cleansers, serums, moisturizers, and more.",
  keywords: ["skincare", "luxury skincare", "AI skincare", "clean beauty", "serums", "moisturizers", "cleansers", "Aura Skincare"],
  authors: [{ name: "Aura Skincare" }],
  creator: "Aura Skincare",
  publisher: "Aura Skincare",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "/",
    siteName: "Aura Skincare",
    title: "Aura Skincare | Pure Formulations, Luminous Skin",
    description: "Discover luxury skincare formulated with pure ingredients. AI-powered beauty commerce platform.",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "Aura Skincare - Pure Formulations, Luminous Skin",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Aura Skincare | Pure Formulations, Luminous Skin",
    description: "Discover luxury skincare formulated with pure ingredients.",
    images: ["/og-image.jpg"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  verification: {
    google: process.env.GOOGLE_SITE_VERIFICATION,
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} ${playfair.variable} font-sans antialiased`}>
        <ThemeProvider>
          <div className="min-h-screen flex flex-col">
            <Navbar />
            <main className="flex-1">{children}</main>
            <Footer />
            <MobileBottomNav />
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
