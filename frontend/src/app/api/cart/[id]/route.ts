import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

async function getAuthHeaders(request: Request) {
  const authHeader = request.headers.get('authorization');
  return {
    'Content-Type': 'application/json',
    ...(authHeader ? { Authorization: authHeader } : {}),
  };
}

export async function PATCH(request: Request, { params }: { params: { id: string } }) {
  const body = await request.json();
  const res = await fetch(`${BACKEND_URL}/public/v1/cart/items/${params.id}`, {
    method: 'PATCH',
    headers: await getAuthHeaders(request),
    body: JSON.stringify(body),
  });
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}

export async function DELETE(request: Request, { params }: { params: { id: string } }) {
  const res = await fetch(`${BACKEND_URL}/public/v1/cart/items/${params.id}`, {
    method: 'DELETE',
    headers: await getAuthHeaders(request),
  });
  if (res.ok) {
    return NextResponse.json(null, { status: 204 });
  }
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
