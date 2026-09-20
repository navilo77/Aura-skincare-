import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

async function getAuthHeaders(request: Request) {
  const authHeader = request.headers.get('authorization');
  return {
    'Content-Type': 'application/json',
    ...(authHeader ? { Authorization: authHeader } : {}),
  };
}

export async function POST(request: Request) {
  const body = await request.json();
  const res = await fetch(`${BACKEND_URL}/api/v1/profile/change-password`, {
    method: 'POST',
    headers: await getAuthHeaders(request),
    body: JSON.stringify(body),
  });
  if (res.ok) {
    return NextResponse.json({ message: 'Password changed' }, { status: 200 });
  }
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
