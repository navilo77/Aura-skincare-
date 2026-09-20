import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/marketing/campaigns`, {
    headers: { Authorization: request.headers.get('authorization') || '' },
  });

  if (!res.ok) {
    return NextResponse.json({ detail: 'Failed to fetch campaigns' }, { status: res.status });
  }

  const data = await res.json();
  return NextResponse.json(data);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/marketing/campaigns`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: request.headers.get('authorization') || '',
    },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
