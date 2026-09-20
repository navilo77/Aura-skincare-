'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, Plus, MoreVertical } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

interface MarketingCampaign {
  id: string;
  name: string;
  description: string | null;
  status: string;
  start_date: string | null;
  end_date: string | null;
  created_at: string;
}

export default function MarketingCampaignsPage() {
  const [campaigns, setCampaigns] = useState<MarketingCampaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchCampaigns = () => {
    setLoading(true);
    setError(null);
    fetch('/api/marketing/campaigns')
      .then((res) => (res.ok ? res.json() : []))
      .then((data) => {
        setCampaigns(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchCampaigns();
  }, []);

  const filteredCampaigns = campaigns.filter(
    (c) =>
      c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.status.toLowerCase().includes(searchQuery.toLowerCase())
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
          <Button onClick={fetchCampaigns}>Retry</Button>
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
                Campaigns
              </h1>
              <p className="mt-2 text-primary-light text-sm md:text-base">
                Track and manage your marketing campaigns
              </p>
            </div>
            <Button variant="primary" className="inline-flex items-center gap-2 w-full sm:w-auto justify-center">
              <Plus className="w-4 h-4" />
              Create Campaign
            </Button>
          </div>
        </motion.div>

        <div className="relative mb-8">
          <input
            type="text"
            placeholder="Search campaigns..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-4 pr-4 py-2.5 bg-surface border border-border rounded-input text-sm text-primary placeholder-primary-light focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent w-full sm:w-80 transition-all duration-200"
          />
        </div>

                {filteredCampaigns.length === 0 ? (
                  <div className="text-center py-24">
                    <p className="text-primary-light text-sm mb-3">No campaigns found</p>
                    <Button size="sm">Create Campaign</Button>
                  </div>
                ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {filteredCampaigns.map((campaign, i) => (
                      <Card
                        key={campaign.id}
                        className="shadow-soft hover:shadow-soft-lg transition-all duration-200 group"
                      >
                <div className="flex items-start justify-between mb-3">
                  <h3 className="font-serif text-lg font-semibold text-primary truncate pr-4">
                    {campaign.name}
                  </h3>
                  <div className="flex items-center gap-2 shrink-0">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${
                        campaign.status === 'active'
                          ? 'bg-success/10 text-success'
                          : campaign.status === 'paused'
                          ? 'bg-accent/10 text-accent'
                          : 'bg-primary/5 text-primary-light'
                      }`}
                    >
                      {campaign.status}
                    </span>
                    <button className="p-1.5 rounded-full hover:bg-background transition-colors duration-200 opacity-0 group-hover:opacity-100">
                      <MoreVertical className="w-4 h-4 text-primary-light" />
                    </button>
                  </div>
                </div>
                {campaign.description && (
                  <p className="text-sm text-primary-light mb-4 line-clamp-2">
                    {campaign.description}
                  </p>
                )}
                <div className="grid grid-cols-3 gap-3 mb-4">
                  {[
                    { label: 'Sent', value: '--' },
                    { label: 'Opened', value: '--' },
                    { label: 'Clicked', value: '--' },
                  ].map((metric) => (
                    <div
                      key={metric.label}
                      className="bg-background rounded-2xl p-3 text-center"
                    >
                      <div className="font-serif text-lg font-semibold text-primary">
                        {metric.value}
                      </div>
                      <div className="text-xs text-primary-light mt-0.5">
                        {metric.label}
                      </div>
                    </div>
                  ))}
                </div>
                <div className="flex items-center justify-between pt-3 border-t border-border text-xs text-primary-light">
                  <span>
                    {campaign.start_date
                      ? new Date(campaign.start_date).toLocaleDateString()
                      : 'No start date'}
                    {campaign.end_date
                      ? ` - ${new Date(campaign.end_date).toLocaleDateString()}`
                      : ''}
                  </span>
                  <span>
                    {new Date(campaign.created_at).toLocaleDateString()}
                  </span>
                 </div>
               </Card>
             ))}
          </div>
        )}
      </div>
    </div>
  );
}
