'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

interface MarketingHistoryItem {
  id: string;
  content_id: string | null;
  action: string;
  metadata: string | null;
  created_at: string;
}

export default function MarketingHistoryPage() {
  const [history, setHistory] = useState<MarketingHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchHistory = () => {
    setLoading(true);
    setError(null);
    fetch('/api/marketing/history')
      .then((res) => (res.ok ? res.json() : []))
      .then((data) => {
        setHistory(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const filteredHistory = history.filter((h) =>
    [h.action, h.content_id || ''].some((v) =>
      v.toLowerCase().includes(searchQuery.toLowerCase())
    )
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Skeleton className="h-8 w-32" />
          <Skeleton className="h-4 w-24" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-secondary-text mb-4">{error}</p>
          <Button onClick={fetchHistory}>Retry</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
          className="mb-8"
        >
          <a
            href="/marketing"
            className="inline-flex items-center gap-1.5 text-sm text-primary-light hover:text-accent transition-colors duration-200 mb-4"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Marketing
          </a>
          <h1 className="font-serif text-3xl md:text-4xl font-semibold text-primary tracking-tight">
            History
          </h1>
          <p className="mt-2 text-primary-light text-sm md:text-base">
            Activity log and audit trail for marketing operations
          </p>
        </motion.div>

        <div className="relative mb-8">
          <input
            type="text"
            placeholder="Search history..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-4 pr-4 py-2.5 bg-surface border border-border rounded-input text-sm text-primary placeholder-primary-light focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent w-full sm:w-80 transition-all duration-200"
          />
        </div>

        {filteredHistory.length === 0 ? (
          <div className="text-center py-24">
            <p className="text-primary-light text-sm mb-3">No history found</p>
          </div>
        ) : (
          <Card className="shadow-soft overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left p-4 text-xs font-medium text-primary-light uppercase tracking-wider">
                      Date
                    </th>
                    <th className="text-left p-4 text-xs font-medium text-primary-light uppercase tracking-wider">
                      Action
                    </th>
                    <th className="text-left p-4 text-xs font-medium text-primary-light uppercase tracking-wider">
                      Content
                    </th>
                    <th className="text-left p-4 text-xs font-medium text-primary-light uppercase tracking-wider">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {filteredHistory.map((item, i) => (
                    <motion.tr
                      key={item.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.25, delay: i * 0.03 }}
                      className="border-b border-border last:border-b-0 hover:bg-background transition-colors duration-200"
                    >
                      <td className="p-4 text-sm text-primary whitespace-nowrap">
                        {new Date(item.created_at).toLocaleString()}
                      </td>
                      <td className="p-4 text-sm text-primary font-medium capitalize">
                        {item.action.replace(/_/g, ' ')}
                      </td>
                      <td className="p-4 text-sm text-primary-light">
                        {item.content_id ? (
                          <span className="font-mono text-xs bg-background px-2 py-1 rounded">
                            {item.content_id.slice(0, 8)}...
                          </span>
                        ) : (
                          '-'
                        )}
                      </td>
                      <td className="p-4">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-success/10 text-success">
                          Success
                        </span>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
