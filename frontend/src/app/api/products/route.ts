import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.toString();
  const res = await fetch(`${BACKEND_URL}/public/v1/products/products${query ? `?${query}` : ''}`, {
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });
  const data = await res.json();
  if (res.ok) {
    return NextResponse.json(data);
  }
  return NextResponse.json(data, { status: res.status });
}
