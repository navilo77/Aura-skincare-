'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FileText,
  Megaphone,
  LayoutTemplate,
  History,
  Plus,
  Search,
  MoreVertical,
} from 'lucide-react';
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

interface MarketingCampaign {
  id: string;
  name: string;
  description: string | null;
  status: string;
  start_date: string | null;
  end_date: string | null;
  created_at: string;
}

interface MarketingTemplate {
  id: string;
  name: string;
  content_type: string;
  prompt: string;
  is_active: string;
  created_at: string;
}

interface MarketingHistoryItem {
  id: string;
  content_id: string | null;
  action: string;
  metadata: string | null;
  created_at: string;
}

type Tab = 'content' | 'campaigns' | 'templates' | 'history';

export default function MarketingPage() {
  const [activeTab, setActiveTab] = useState<Tab>('content');
  const [contents, setContents] = useState<MarketingContent[]>([]);
  const [campaigns, setCampaigns] = useState<MarketingCampaign[]>([]);
  const [templates, setTemplates] = useState<MarketingTemplate[]>([]);
  const [history, setHistory] = useState<MarketingHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchMarketingData = () => {
    setLoading(true);
    setError(null);
    Promise.all([
      fetch('/api/marketing/contents').then((res) => (res.ok ? res.json() : [])),
      fetch('/api/marketing/campaigns').then((res) => (res.ok ? res.json() : [])),
      fetch('/api/marketing/templates').then((res) => (res.ok ? res.json() : [])),
      fetch('/api/marketing/history').then((res) => (res.ok ? res.json() : [])),
    ])
      .then(([contentsData, campaignsData, templatesData, historyData]) => {
        setContents(Array.isArray(contentsData) ? contentsData : []);
        setCampaigns(Array.isArray(campaignsData) ? campaignsData : []);
        setTemplates(Array.isArray(templatesData) ? templatesData : []);
        setHistory(Array.isArray(historyData) ? historyData : []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchMarketingData();
  }, []);

  const tabs: { id: Tab; label: string; icon: typeof FileText }[] = [
    { id: 'content', label: 'Content', icon: FileText },
    { id: 'campaigns', label: 'Campaigns', icon: Megaphone },
    { id: 'templates', label: 'Templates', icon: LayoutTemplate },
    { id: 'history', label: 'History', icon: History },
  ];

  const filteredContents = contents.filter(
    (c) =>
      c.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.body.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.content_type.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredCampaigns = campaigns.filter(
    (c) =>
      c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.status.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredTemplates = templates.filter(
    (t) =>
      t.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.content_type.toLowerCase().includes(searchQuery.toLowerCase())
  );

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
          <Button onClick={fetchMarketingData}>Retry</Button>
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
          className="mb-10"
        >
          <h1 className="font-serif text-3xl md:text-4xl font-semibold text-primary tracking-tight">
            Marketing
          </h1>
          <p className="mt-2 text-primary-light text-sm md:text-base">
            Manage your content, campaigns, templates, and activity
          </p>
        </motion.div>

        <div className="relative mb-8">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-primary-light" />
          <input
            type="text"
            placeholder="Search..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 pr-4 py-2.5 bg-surface border border-border rounded-input text-sm text-primary placeholder-primary-light focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent w-full sm:w-80 transition-all duration-200"
          />
        </div>

        <div className="flex flex-wrap gap-1 mb-8 border-b border-border">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`relative flex items-center gap-2 px-4 py-3 text-sm font-medium transition-colors duration-200 rounded-t-lg ${
                  isActive ? 'text-accent' : 'text-primary-light hover:text-primary'
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
                {isActive && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute bottom-0 left-2 right-2 h-0.5 bg-accent rounded-full"
                    transition={{ type: 'spring', bounce: 0, duration: 0.3 }}
                  />
                )}
              </button>
            );
          })}
        </div>

        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.25 }}
          >
            {activeTab === 'content' && (
              <div className="space-y-5">
                <div className="flex justify-between items-center">
                  <h2 className="font-serif text-xl font-semibold text-primary">Content</h2>
                  <Button variant="primary" className="inline-flex items-center gap-2">
                    <Plus className="w-4 h-4" />
                    Create Content
                  </Button>
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
            )}

            {activeTab === 'campaigns' && (
              <div className="space-y-5">
                <div className="flex justify-between items-center">
                  <h2 className="font-serif text-xl font-semibold text-primary">Campaigns</h2>
                  <Button variant="primary" className="inline-flex items-center gap-2">
                    <Plus className="w-4 h-4" />
                    Create Campaign
                  </Button>
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
                          <span
                            className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize shrink-0 ${
                              campaign.status === 'active'
                                ? 'bg-success/10 text-success'
                                : campaign.status === 'paused'
                                ? 'bg-accent/10 text-accent'
                                : 'bg-primary/5 text-primary-light'
                            }`}
                          >
                            {campaign.status}
                          </span>
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
                              : 'No start'}
                            {campaign.end_date
                              ? ` - ${new Date(campaign.end_date).toLocaleDateString()}`
                              : ''}
                          </span>
                         </div>
                       </Card>
                     ))}
                  </div>
                )}
              </div>
            )}

            {activeTab === 'templates' && (
              <div className="space-y-5">
                <div className="flex justify-between items-center">
                  <h2 className="font-serif text-xl font-semibold text-primary">Templates</h2>
                  <Button variant="primary" className="inline-flex items-center gap-2">
                    <Plus className="w-4 h-4" />
                    Create Template
                  </Button>
                </div>
                {filteredTemplates.length === 0 ? (
                  <div className="text-center py-24">
                    <p className="text-primary-light text-sm mb-3">No templates found</p>
                    <Button size="sm">Create Template</Button>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                     {filteredTemplates.map((template, i) => {
                       const channel = template.content_type.toLowerCase();
                       const channelColors: Record<string, string> = {
                         email: 'bg-accent/10 text-accent',
                         sms: 'bg-success/10 text-success',
                         push: 'bg-primary/10 text-primary',
                       };
                       return (
                         <Card
                           key={template.id}
                           className="shadow-soft hover:shadow-soft-lg transition-all duration-200"
                         >
                          <div className="flex items-center justify-between mb-3">
                            <h3 className="font-serif text-lg font-semibold text-primary truncate pr-4">
                              {template.name}
                            </h3>
                            <span
                              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize shrink-0 ${
                                channelColors[channel] || 'bg-primary/5 text-primary-light'
                              }`}
                            >
                              {channel}
                            </span>
                          </div>
                          <p className="text-sm text-primary-light line-clamp-3 mb-4">
                            {template.prompt}
                          </p>
                          <div className="flex items-center justify-between pt-3 border-t border-border">
                            <span
                              className={`text-xs font-medium ${
                                template.is_active === 'true'
                                  ? 'text-success'
                                  : 'text-primary-light'
                              }`}
                            >
                              {template.is_active === 'true' ? 'Active' : 'Inactive'}
                            </span>
                            <span className="text-xs text-primary-light">
                              {new Date(template.created_at).toLocaleDateString()}
                            </span>
                           </div>
                         </Card>
                       );
                     })}
                  </div>
                )}
              </div>
            )}

            {activeTab === 'history' && (
              <div className="space-y-5">
                <h2 className="font-serif text-xl font-semibold text-primary">History</h2>
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
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
