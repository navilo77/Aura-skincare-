import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/marketing/history`, {
    headers: { Authorization: request.headers.get('authorization') || '' },
  });

  if (!res.ok) {
    return NextResponse.json({ detail: 'Failed to fetch history' }, { status: res.status });
  }

  const data = await res.json();
  return NextResponse.json(data);
}
