import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export async function GET(_request: Request, { params }: { params: { id: string } }) {
  const res = await fetch(`${BACKEND_URL}/public/v1/products/products/${params.id}`, {
    headers: { 'Content-Type': 'application/json' },
    cache: 'no-store',
  });
  const data = await res.json();
  if (res.ok) {
    return NextResponse.json(data);
  }
  return NextResponse.json(data, { status: res.status });
}
