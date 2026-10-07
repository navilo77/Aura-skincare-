import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

async function getAuthHeaders(request: Request) {
  const authHeader = request.headers.get('authorization');
  return {
    'Content-Type': 'application/json',
    ...(authHeader ? { Authorization: authHeader } : {}),
  };
}

export async function GET(request: Request) {
  const res = await fetch(`${BACKEND_URL}/api/v1/wishlist`, {
    headers: await getAuthHeaders(request),
    cache: 'no-store',
  });
  const data = await res.json();
  if (res.ok) {
    return NextResponse.json(data);
  }
  return NextResponse.json(data, { status: res.status });
}

export async function POST(request: Request) {
  const body = await request.json();
  const productId = body.product_id;
  const productVariantId = body.product_variant_id;
  
  let url = `${BACKEND_URL}/api/v1/wishlist/items/${productId}`;
  if (productVariantId) {
    url += `?product_variant_id=${productVariantId}`;
  }
  
  const res = await fetch(url, {
    method: 'POST',
    headers: await getAuthHeaders(request),
  });
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
