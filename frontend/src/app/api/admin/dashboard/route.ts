import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

function normalizeDashboard(data: Record<string, unknown>): Record<string, unknown> {
  const normalized = { ...data };
  if (typeof normalized.total_revenue === "string") {
    normalized.total_revenue = parseFloat(normalized.total_revenue);
  }
  return normalized;
}

export async function GET(request: NextRequest) {
  const token = request.headers.get('authorization')?.replace('Bearer ', '');
  if (!token) {
    return NextResponse.json({ detail: 'Unauthorized' }, { status: 401 });
  }

  const res = await fetch(`${BACKEND_URL}/api/v1/admin/dashboard`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) {
    return NextResponse.json({ detail: 'Failed to fetch dashboard' }, { status: res.status });
  }

  const data = await res.json();
  const normalizedData = normalizeDashboard(data);
  return NextResponse.json(normalizedData);
}
