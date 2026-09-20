import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

async function getAuthHeaders(request: Request) {
  const authHeader = request.headers.get('authorization');
  return {
    'Content-Type': 'application/json',
    ...(authHeader ? { Authorization: authHeader } : {}),
  };
}

export async function DELETE(request: Request, { params }: { params: { productId: string } }) {
  const res = await fetch(`${BACKEND_URL}/api/v1/wishlist/items/${params.productId}`, {
    method: 'DELETE',
    headers: await getAuthHeaders(request),
  });
  if (res.ok) {
    return NextResponse.json(null, { status: 204 });
  }
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
