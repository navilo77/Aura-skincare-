import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

async function getAuthHeaders(request: Request) {
  const authHeader = request.headers.get('authorization');
  return {
    'Content-Type': 'application/json',
    ...(authHeader ? { Authorization: authHeader } : {}),
  };
}

function normalizeProfile(profile: Record<string, unknown>): Record<string, unknown> {
  // Profile doesn't have Decimal fields, but normalize for consistency
  return profile;
}

export async function GET(request: Request) {
  const res = await fetch(`${BACKEND_URL}/api/v1/profile`, {
    headers: await getAuthHeaders(request),
    cache: 'no-store',
  });
  const data = await res.json();
  const normalizedData = normalizeProfile(data);
  if (res.ok) {
    return NextResponse.json(normalizedData);
  }
  return NextResponse.json(normalizedData, { status: res.status });
}

export async function PATCH(request: Request) {
  const body = await request.json();
  const res = await fetch(`${BACKEND_URL}/api/v1/profile`, {
    method: 'PATCH',
    headers: await getAuthHeaders(request),
    body: JSON.stringify(body),
  });
  const data = await res.json();
  const normalizedData = normalizeProfile(data);
  return NextResponse.json(normalizedData, { status: res.status });
}
