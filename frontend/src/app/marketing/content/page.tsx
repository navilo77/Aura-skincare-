'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, Plus, MoreVertical } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

interface MarketingContent {
  id: string;
  campaign_id: string | null;
  template_id: string | null;
  content_type: string;
  title: string | null;
  body: string;
  metadata: string | null;
  created_at: string;
}

export default function MarketingContentPage() {
  const [contents, setContents] = useState<MarketingContent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchContents = () => {
    setLoading(true);
    setError(null);
    fetch('/api/marketing/contents')
      .then((res) => (res.ok ? res.json() : []))
      .then((data) => {
        setContents(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchContents();
  }, []);

  const filteredContents = contents.filter(
    (c) =>
      c.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.body.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.content_type.toLowerCase().includes(searchQuery.toLowerCase())
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
          <Button onClick={fetchContents}>Retry</Button>
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
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="font-serif text-3xl md:text-4xl font-semibold text-primary tracking-tight">
                Content
              </h1>
              <p className="mt-2 text-primary-light text-sm md:text-base">
                Manage your marketing content pieces
              </p>
            </div>
            <Button variant="primary" className="inline-flex items-center gap-2 w-full sm:w-auto justify-center">
              <Plus className="w-4 h-4" />
              Create Content
            </Button>
          </div>
        </motion.div>

        <div className="relative mb-8">
          <input
            type="text"
            placeholder="Search content..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-4 pr-4 py-2.5 bg-surface border border-border rounded-input text-sm text-primary placeholder-primary-light focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent w-full sm:w-80 transition-all duration-200"
          />
        </div>

        {filteredContents.length === 0 ? (
          <div className="text-center py-24">
            <p className="text-primary-light text-sm mb-3">No content found</p>
            <Button size="sm">Create Content</Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredContents.map((content, i) => (
              <Card
                key={content.id}
                className="shadow-soft hover:shadow-soft-lg transition-all duration-200 group"
              >
                <div className="flex items-start justify-between mb-3">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-background text-primary-light border border-border capitalize">
                    {content.content_type}
                  </span>
                  <button className="p-1.5 rounded-full hover:bg-background transition-colors duration-200 opacity-0 group-hover:opacity-100">
                    <MoreVertical className="w-4 h-4 text-primary-light" />
                  </button>
                </div>
                <h3 className="font-serif text-lg font-semibold text-primary mb-1 truncate">
                  {content.title || 'Untitled'}
                </h3>
                <p className="text-sm text-primary-light line-clamp-2 mb-4">
                  {content.body.slice(0, 120)}
                </p>
                <div className="flex items-center justify-between pt-3 border-t border-border">
                  <span className="text-xs text-primary-light">
                    {new Date(content.created_at).toLocaleDateString()}
                  </span>
                  <div className="flex gap-3">
                    <button className="text-xs text-accent hover:text-accent-dark transition-colors duration-200 font-medium">
                      Edit
                    </button>
                    <button className="text-xs text-error hover:opacity-80 transition-colors duration-200 font-medium">
                      Delete
                    </button>
                  </div>
                 </div>
               </Card>
             ))}
          </div>
        )}
      </div>
    </div>
  );
}
