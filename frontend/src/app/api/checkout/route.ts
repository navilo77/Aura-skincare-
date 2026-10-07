import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

async function getAuthHeaders(request: Request) {
  const authHeader = request.headers.get('authorization');
  const cookieStore = await cookies();
  const accessToken = cookieStore.get('access_token')?.value;
  const authorization = authHeader || (accessToken ? `Bearer ${accessToken}` : '');

  return {
    'Content-Type': 'application/json',
    ...(authorization ? { Authorization: authorization } : {}),
  };
}

function normalizeOrder(order: Record<string, unknown>): Record<string, unknown> {
  const normalized = { ...order };
  if (typeof normalized.total_amount === "string") {
    normalized.total_amount = parseFloat(normalized.total_amount);
  }
  if (normalized.items && Array.isArray(normalized.items)) {
    normalized.items = normalized.items.map((item: Record<string, unknown>) => {
      const normItem = { ...item };
      if (typeof normItem.unit_price === "string") {
        normItem.unit_price = parseFloat(normItem.unit_price);
      }
      if (typeof normItem.total_price === "string") {
        normItem.total_price = parseFloat(normItem.total_price);
      }
      return normItem;
    });
  }
  return normalized;
}

export async function POST(request: Request) {
  try {
    const body = await request.json();

    const profileRes = await fetch(`${BACKEND_URL}/api/v1/profile`, {
      headers: await getAuthHeaders(request),
      cache: 'no-store',
    });

    if (!profileRes.ok) {
      const data = await profileRes.json().catch(() => ({}));
      return NextResponse.json(data, { status: profileRes.status });
    }

    const profile = await profileRes.json();

    const orderPayload = {
      customer_id: profile.id,
      items: body.items,
      shipping_address: {
        ...body.shipping_address,
        full_name: profile.full_name,
      },
      status: 'pending',
      currency: 'USD',
    };

    const res = await fetch(`${BACKEND_URL}/api/v1/orders`, {
      method: 'POST',
      headers: await getAuthHeaders(request),
      body: JSON.stringify(orderPayload),
    });

    const data = await res.json();
    const normalizedData = normalizeOrder(data);
    return NextResponse.json(normalizedData, { status: res.status });
  } catch {
    return NextResponse.json(
      { message: 'Failed to place order' },
      { status: 500 }
    );
  }
}
