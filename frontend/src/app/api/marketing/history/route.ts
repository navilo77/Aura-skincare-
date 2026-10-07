import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

export async function GET(request: NextRequest) {
  const res = await fetch(`${BACKEND_URL}/api/v1/marketing/history`, {
    headers: { Authorization: request.headers.get('authorization') || '' },
  });

  if (!res.ok) {
    return NextResponse.json({ detail: 'Failed to fetch history' }, { status: res.status });
  }

  const data = await res.json();
  return NextResponse.json(data);
}
