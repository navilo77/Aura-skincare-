'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Sparkles,
  Plus,
  Clock,
  MoreHorizontal,
  Paperclip,
  Send,
  Menu,
  X,
  Search,
  Image as ImageIcon,
  ShoppingBag,
} from 'lucide-react';
import { Button } from '@/components/ui/button';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  productCards?: ProductCard[];
  routineCards?: RoutineCard[];
}

interface ProductCard {
  id: string;
  name: string;
  price: number;
  image: string;
  category: string;
}

interface RoutineCard {
  id: string;
  name: string;
  steps: string[];
  products: string[];
}

interface Conversation {
  id: string;
  title: string;
  timestamp: Date;
}

export default function AIChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId] = useState(() => crypto.randomUUID());
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [conversations] = useState<Conversation[]>([
    { id: '1', title: 'Skincare routine for oily skin', timestamp: new Date(Date.now() - 86400000) },
    { id: '2', title: 'Best vitamin C serums', timestamp: new Date(Date.now() - 172800000) },
    { id: '3', title: 'How to treat dark spots', timestamp: new Date(Date.now() - 259200000) },
  ]);
  const [charCount, setCharCount] = useState(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const suggestedQuestions = [
    'What products are best for dry skin?',
    'Create a morning skincare routine',
    'Recommend products for acne-prone skin',
    'How do I layer serums properly?',
  ];

  const mockProducts: ProductCard[] = [
    {
      id: '1',
      name: 'Hydrating Rose Serum',
      price: 89,
      image: '/images/products/serum-1.jpg',
      category: 'Serums',
    },
    {
      id: '2',
      name: 'Vitamin C Brightening Cream',
      price: 120,
      image: '/images/products/cream-1.jpg',
      category: 'Moisturizers',
    },
  ];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    setCharCount(input.length);
  }, [input]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;
    setError(null);

    const userMessage = input.trim();
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: userMessage,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage, session_id: sessionId }),
      });
      const data = await res.json();
      if (res.ok) {
        const aiMsg: Message = {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: data.message || 'I am here to help with your skincare questions.',
          timestamp: new Date(),
          productCards: userMessage.toLowerCase().includes('recommend') || userMessage.toLowerCase().includes('best')
            ? mockProducts
            : undefined,
          routineCards: userMessage.toLowerCase().includes('routine') || userMessage.toLowerCase().includes('morning')
            ? [
                {
                  id: 'r1',
                  name: 'Morning Glow Routine',
                  steps: ['Gentle Cleanser', 'Vitamin C Serum', 'Moisturizer', 'Sunscreen SPF 50'],
                  products: ['Hydrating Rose Serum', 'Vitamin C Brightening Cream'],
                },
              ]
            : undefined,
        };
        setMessages((prev) => [...prev, aiMsg]);
      } else {
        const errMsg = data.detail || 'Something went wrong';
        setError(errMsg);
        setMessages((prev) => [
          ...prev,
          {
            id: crypto.randomUUID(),
            role: 'assistant',
            content: `Sorry, I encountered an error: ${errMsg}. Please try again.`,
            timestamp: new Date(),
          },
        ]);
      }
    } catch {
      const errMsg = 'Network error. Please check your connection.';
      setError(errMsg);
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: `Sorry, I encountered an error: ${errMsg}. Please try again.`,
          timestamp: new Date(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestedQuestion = (question: string) => {
    setInput(question);
    textareaRef.current?.focus();
  };

  const TypingIndicator = () => (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 10 }}
      transition={{ duration: 0.2 }}
      className="flex items-center space-x-1.5 bg-surface px-4 py-3 rounded-2xl rounded-bl-md w-fit"
    >
      {[0, 1, 2].map((i) => (
        <motion.span
          key={i}
          animate={{ y: [0, -4, 0], opacity: [0.4, 1, 0.4] }}
          transition={{
            duration: 0.6,
            repeat: Infinity,
            delay: i * 0.15,
          }}
          className="w-1.5 h-1.5 bg-secondary-text rounded-full"
        />
      ))}
    </motion.div>
  );

  const ProductCardComponent = ({ product }: { product: ProductCard }) => (
    <div className="bg-background border border-border rounded-product p-3 flex space-x-3 shadow-soft hover:shadow-soft-lg transition-shadow duration-200">
      <div className="w-16 h-16 bg-surface rounded-lg flex-shrink-0 flex items-center justify-center">
        <ImageIcon className="h-6 w-6 text-secondary-text" />
      </div>
      <div className="flex-1 min-w-0">
        <h4 className="font-medium text-sm text-primary truncate">{product.name}</h4>
        <p className="text-xs text-secondary-text">{product.category}</p>
        <div className="flex items-center justify-between mt-2">
          <span className="font-semibold text-accent">${product.price}</span>
          <button className="px-3 py-1 bg-accent text-white text-xs rounded-button hover:bg-accent-dark transition-colors flex items-center space-x-1">
            <ShoppingBag className="h-3 w-3" />
            <span>Add</span>
          </button>
        </div>
      </div>
    </div>
  );

  const RoutineCardComponent = ({ routine }: { routine: RoutineCard }) => (
    <div className="bg-background border border-border rounded-product p-4 shadow-soft">
      <h4 className="font-serif font-semibold text-primary mb-3">{routine.name}</h4>
      <div className="space-y-2.5">
        {routine.steps.map((step, idx) => (
          <div key={idx} className="flex items-start space-x-3">
            <div className="w-5 h-5 bg-accent/10 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
              <span className="text-[10px] text-accent font-medium">{idx + 1}</span>
            </div>
            <p className="text-sm text-primary">{step}</p>
          </div>
        ))}
      </div>
      <div className="mt-3 pt-3 border-t border-border">
        <p className="text-xs text-secondary-text">
          Includes: {routine.products.join(', ')}
        </p>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-background flex">
      {/* Mobile Overlay */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <aside
        className={[
          'fixed inset-y-0 left-0 z-50 w-80 bg-background border-r border-border shadow-soft-lg transition-transform duration-200 ease-in-out flex-shrink-0',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full',
          'lg:translate-x-0 lg:static lg:z-auto lg:shadow-none',
        ]
          .filter(Boolean)
          .join(' ')}
      >
        <div className="flex flex-col h-full">
          {/* Sidebar Header */}
          <div className="flex items-center justify-between p-6 border-b border-border">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-accent/10 rounded-full flex items-center justify-center">
                <Sparkles className="h-5 w-5 text-accent" />
              </div>
              <div>
                <h1 className="font-serif text-xl font-semibold text-primary">Aura AI</h1>
                <p className="text-xs text-secondary-text">Skincare Assistant</p>
              </div>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden p-2 hover:bg-surface rounded-button transition-colors"
              aria-label="Close sidebar"
            >
              <X className="h-5 w-5 text-primary" />
            </button>
          </div>

          {/* New Chat Button */}
          <div className="p-4">
            <Button
              variant="secondary"
              className="w-full justify-center space-x-2"
              onClick={() => setMessages([])}
            >
              <Plus className="h-4 w-4" />
              <span>New Chat</span>
            </Button>
          </div>

          {/* Conversation History */}
          <div className="flex-1 overflow-y-auto px-4">
            <h3 className="text-xs font-semibold text-secondary-text uppercase tracking-wider mb-3 px-2">
              Recent Chats
            </h3>
            <div className="space-y-1">
              {conversations.length === 0 ? (
                <p className="text-sm text-secondary-text px-2 py-4 text-center">
                  No conversations yet
                </p>
              ) : (
                conversations.map((conv) => (
                  <button
                    key={conv.id}
                    className="w-full flex items-center justify-between p-3 rounded-button hover:bg-surface transition-colors text-left group"
                  >
                    <div className="flex items-center space-x-3 min-w-0">
                      <Clock className="h-4 w-4 text-secondary-text flex-shrink-0" />
                      <span className="text-sm text-primary truncate">{conv.title}</span>
                    </div>
                    <MoreHorizontal className="h-4 w-4 text-secondary-text opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0" />
                  </button>
                ))
              )}
            </div>
          </div>

          {/* Suggested Questions */}
          <div className="p-4 border-t border-border">
            <h3 className="text-xs font-semibold text-secondary-text uppercase tracking-wider mb-3 px-2">
              Suggested Questions
            </h3>
            <div className="space-y-2">
              {suggestedQuestions.map((question, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    handleSuggestedQuestion(question);
                    setSidebarOpen(false);
                  }}
                  className="w-full text-left p-3 text-sm text-secondary-text hover:text-primary hover:bg-surface rounded-button transition-colors line-clamp-2"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        </div>
      </aside>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
          className="sticky top-0 z-30 bg-background/80 backdrop-blur-md border-b border-border"
        >
          <div className="flex items-center justify-between px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden p-2 -ml-2 hover:bg-surface rounded-button transition-colors"
              >
                <Menu className="h-5 w-5 text-primary" />
              </button>
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-accent/10 rounded-full flex items-center justify-center">
                  <Sparkles className="h-4 w-4 text-accent" />
                </div>
                <div>
                  <h2 className="font-serif text-lg font-semibold text-primary">Aura AI</h2>
                  <p className="text-xs text-secondary-text">
                    {messages.length > 0 ? 'Active conversation' : 'Ready to help'}
                  </p>
                </div>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Button variant="ghost" size="sm" aria-label="Search conversations">
                <Search className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </motion.header>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6">
          {error && (
            <div className="max-w-3xl mx-auto mb-4">
              <div className="bg-error/5 border border-error/20 rounded-input px-4 py-3 flex items-center justify-between">
                <p className="text-sm text-error">{error}</p>
                <Button variant="ghost" size="sm" onClick={() => setError(null)}>Dismiss</Button>
              </div>
            </div>
          )}
          <div className="max-w-3xl mx-auto space-y-6">
            <AnimatePresence>
              {messages.length === 0 && !loading && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.25 }}
                  className="text-center py-16"
                >
                  <div className="w-20 h-20 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-6">
                    <Sparkles className="h-10 w-10 text-accent" />
                  </div>
                  <h3 className="font-serif text-2xl font-semibold text-primary mb-3">
                    Welcome to Aura AI
                  </h3>
                  <p className="text-secondary-text max-w-md mx-auto mb-8">
                    Your personal skincare assistant. Ask me anything about products, routines, or ingredients.
                  </p>
                  <div className="flex flex-wrap justify-center gap-2">
                    {suggestedQuestions.slice(0, 2).map((q, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleSuggestedQuestion(q)}
                        className="px-4 py-2 bg-surface border border-border rounded-full text-sm text-secondary-text hover:text-primary hover:border-accent transition-all duration-200"
                      >
                        {q}
                      </button>
                    ))}
                  </div>
                </motion.div>
              )}

              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.25 }}
                  className={`flex ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`flex items-start space-x-3 max-w-[85%] sm:max-w-[75%] ${
                      message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                    }`}
                  >
                    {/* Avatar */}
                    <div
                      className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                        message.role === 'user'
                          ? 'bg-accent text-white'
                          : 'bg-accent/10 text-accent'
                      }`}
                    >
                      {message.role === 'user' ? (
                        <span className="text-xs font-medium">You</span>
                      ) : (
                        <Sparkles className="h-4 w-4" />
                      )}
                    </div>

                    {/* Message Content */}
                    <div
                      className={`px-4 py-3 rounded-2xl ${
                        message.role === 'user'
                          ? 'bg-accent text-white rounded-br-md'
                          : 'bg-surface text-primary rounded-bl-md'
                      }`}
                    >
                      <p className="text-sm sm:text-base leading-relaxed whitespace-pre-wrap">
                        {message.content}
                      </p>

                      {/* Product Recommendation Cards */}
                      {message.productCards && message.productCards.length > 0 && (
                        <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-3">
                          {message.productCards.map((product) => (
                            <ProductCardComponent key={product.id} product={product} />
                          ))}
                        </div>
                      )}

                      {/* Routine Recommendation Cards */}
                      {message.routineCards && message.routineCards.length > 0 && (
                        <div className="mt-3 space-y-3">
                          {message.routineCards.map((routine) => (
                            <RoutineCardComponent key={routine.id} routine={routine} />
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}

              {loading && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex items-start space-x-3"
                >
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-accent/10 text-accent flex items-center justify-center">
                    <Sparkles className="h-4 w-4" />
                  </div>
                  <TypingIndicator />
                </motion.div>
              )}
              <div ref={messagesEndRef} />
            </AnimatePresence>
          </div>
        </div>

        {/* Input Area */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
          className="border-t border-border bg-background/80 backdrop-blur-md px-4 sm:px-6 lg:px-8 py-4"
        >
          <div className="max-w-3xl mx-auto">
            {/* Suggested Questions */}
            {messages.length === 0 && (
              <div className="flex flex-wrap gap-2 mb-4">
                {suggestedQuestions.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSuggestedQuestion(q)}
                    className="px-3 py-1.5 bg-surface border border-border rounded-button text-xs sm:text-sm text-secondary-text hover:text-primary hover:border-accent transition-all duration-200"
                  >
                    {q}
                  </button>
                ))}
              </div>
            )}

            <form onSubmit={sendMessage} className="relative">
              <div className="flex items-end space-x-2 bg-surface border border-border rounded-2xl px-4 py-3 shadow-soft focus-within:border-accent focus-within:shadow-soft-lg transition-all duration-200">
                <button
                  type="button"
                  className="flex-shrink-0 p-1 text-secondary-text hover:text-primary transition-colors"
                  aria-label="Attach file"
                >
                  <Paperclip className="h-5 w-5" />
                </button>
                <textarea
                  ref={textareaRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      sendMessage(e);
                    }
                  }}
                  placeholder="Ask me anything about products, orders, or skincare..."
                  rows={1}
                  className="flex-1 resize-none bg-transparent border-none outline-none text-primary placeholder-secondary-text text-sm sm:text-base leading-relaxed max-h-32"
                  disabled={loading}
                  aria-label="Chat message input"
                />
                <div className="flex items-center space-x-2 flex-shrink-0">
                  <span className="text-xs text-secondary-text hidden sm:block">
                    {charCount}/500
                  </span>
                  <Button
                    type="submit"
                    disabled={loading || !input.trim()}
                    size="sm"
                    aria-label="Send message"
                  >
                    <Send className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </form>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
