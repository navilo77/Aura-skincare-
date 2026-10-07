import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

export async function POST(request: Request) {
  const body = await request.json();
  const res = await fetch(`${BACKEND_URL}/api/v1/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (res.ok) {
    const response = NextResponse.json(data);
    response.cookies.set('access_token', data.access_token, { httpOnly: true });
    response.cookies.set('refresh_token', data.refresh_token, { httpOnly: true });
    return response;
  }
  return NextResponse.json(data, { status: res.status });
}
