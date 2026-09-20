'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Search, Workflow, CheckCircle2, Clock, XCircle, AlertCircle } from 'lucide-react';
import { AdminLayout } from '@/components/admin/admin-layout';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

interface AutomationJob {
  id: string;
  job_type: string;
  status: string;
  scheduled_at: string | null;
  started_at: string | null;
  completed_at: string | null;
  error_message: string | null;
  created_at: string;
}

const statusConfig: Record<string, { bg: string; icon: typeof CheckCircle2 }> = {
  completed: { bg: 'bg-success/10 text-success', icon: CheckCircle2 },
  running: { bg: 'bg-accent/10 text-accent', icon: Clock },
  failed: { bg: 'bg-error/10 text-error', icon: XCircle },
  pending: { bg: 'bg-surface text-primary-light', icon: AlertCircle },
};

export default function AutomationJobsPage() {
  const [jobs, setJobs] = useState<AutomationJob[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const router = useRouter();

  const fetchJobs = () => {
    setLoading(true);
    setError(null);
    const token = localStorage.getItem('admin_token');
    fetch('/api/admin/automation-jobs', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.ok ? res.json() : [])
      .then((data) => {
        setJobs(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => {
    const token = localStorage.getItem('admin_token');
    if (!token) {
      router.push('/admin/login');
      return;
    }
    fetchJobs();
  }, [router]);

  const filtered = jobs.filter((j) =>
    j.job_type.toLowerCase().includes(search.toLowerCase()) ||
    j.status.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <AdminLayout>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.25 }}
        className="space-y-6"
      >
        <div>
          <h1 className="font-serif text-3xl md:text-4xl font-semibold text-foreground tracking-tight">
            Automation Jobs
          </h1>
          <p className="text-secondary-text mt-1">Monitor scheduled tasks and workflow executions</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 md:gap-6">
          {['completed', 'running', 'failed'].map((status, i) => {
            const count = jobs.filter((j) => j.status === status).length;
            const config = statusConfig[status];
            const Icon = config.icon;
            return (
              <Card key={status} className="shadow-soft">
                <div className="flex items-center gap-4">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${config.bg}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  <div>
                    <p className="text-secondary-text text-sm capitalize">{status}</p>
                    <p className="font-serif text-2xl font-semibold text-foreground">{count}</p>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>

        <Card className="shadow-soft">
          <div className="p-4 md:p-6 border-b border-border">
            <div className="relative max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-secondary-text" />
              <input
                type="text"
                placeholder="Search jobs..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="input-field pl-10"
              />
            </div>
          </div>

          {loading ? (
            <div className="p-6 space-y-4">
              {[...Array(5)].map((_, i) => (
                <Skeleton key={i} className="h-12 w-full" />
              ))}
            </div>
          ) : error ? (
            <div className="p-6 text-center">
              <p className="text-secondary-text mb-4">{error}</p>
              <Button onClick={fetchJobs}>Retry</Button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Type</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Status</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Scheduled</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Started</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Completed</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Error</th>
                    <th className="text-left py-3 px-4 md:px-6 text-xs font-semibold text-secondary-text uppercase tracking-wider">Date</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {filtered.map((job, i) => {
                    const config = statusConfig[job.status] || statusConfig.pending;
                    const StatusIcon = config.icon;
                    return (
                      <motion.tr
                        key={job.id}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.2, delay: i * 0.03 }}
                        className="hover:bg-surface/50 transition-colors duration-150"
                      >
                        <td className="py-4 px-4 md:px-6 text-sm font-medium text-foreground capitalize">{job.job_type.replace(/_/g, ' ')}</td>
                        <td className="py-4 px-4 md:px-6">
                          <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium ${config.bg}`}>
                            <StatusIcon className="w-3 h-3" />
                            {job.status}
                          </span>
                        </td>
                        <td className="py-4 px-4 md:px-6 text-sm text-secondary-text">
                          {job.scheduled_at ? new Date(job.scheduled_at).toLocaleString() : '-'}
                        </td>
                        <td className="py-4 px-4 md:px-6 text-sm text-secondary-text">
                          {job.started_at ? new Date(job.started_at).toLocaleString() : '-'}
                        </td>
                        <td className="py-4 px-4 md:px-6 text-sm text-secondary-text">
                          {job.completed_at ? new Date(job.completed_at).toLocaleString() : '-'}
                        </td>
                        <td className="py-4 px-4 md:px-6 text-sm text-error max-w-xs truncate">{job.error_message || '-'}</td>
                        <td className="py-4 px-4 md:px-6 text-sm text-secondary-text">
                          {new Date(job.created_at).toLocaleString()}
                        </td>
                      </motion.tr>
                    );
                  })}
                  {filtered.length === 0 && (
                    <tr>
                      <td colSpan={7} className="py-12 text-center">
                        <p className="text-secondary-text text-sm mb-3">No jobs found</p>
                        <Button size="sm" onClick={() => setSearch('')}>Clear Search</Button>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </Card>
      </motion.div>
    </AdminLayout>
  );
}
