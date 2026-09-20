import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

async function getAuthHeaders(request: Request) {
  const authHeader = request.headers.get('authorization');
  return {
    'Content-Type': 'application/json',
    ...(authHeader ? { Authorization: authHeader } : {}),
  };
}

export async function GET(request: Request) {
  const res = await fetch(`${BACKEND_URL}/api/v1/profile`, {
    headers: await getAuthHeaders(request),
    cache: 'no-store',
  });
  const data = await res.json();
  if (res.ok) {
    return NextResponse.json(data);
  }
  return NextResponse.json(data, { status: res.status });
}

export async function PATCH(request: Request) {
  const body = await request.json();
  const res = await fetch(`${BACKEND_URL}/api/v1/profile`, {
    method: 'PATCH',
    headers: await getAuthHeaders(request),
    body: JSON.stringify(body),
  });
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
