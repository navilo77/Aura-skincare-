import { NextResponse } from "next/server";

const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";

async function getAuthHeaders(request: Request) {
  const authHeader = request.headers.get("authorization");

  return {
    "Content-Type": "application/json",
    ...(authHeader ? { Authorization: authHeader } : {}),
  };
}

function normalizeCartItem(item: Record<string, unknown>): Record<string, unknown> {
  const normalized = { ...item };
  if (typeof normalized.unit_price === "string") {
    normalized.unit_price = parseFloat(normalized.unit_price);
  }
  if (typeof normalized.subtotal === "string") {
    normalized.subtotal = parseFloat(normalized.subtotal);
  }
  if (normalized.thumbnail_url === null) {
    normalized.thumbnail_url = undefined;
  }
  return normalized;
}

function normalizeCart(cart: Record<string, unknown>): Record<string, unknown> {
  const normalized = { ...cart };
  if (normalized.items && Array.isArray(normalized.items)) {
    normalized.items = normalized.items.map(normalizeCartItem);
  }
  return normalized;
}

export async function GET(request: Request) {
  try {
    const response = await fetch(`${BACKEND_URL}/api/v1/cart`, {
      headers: await getAuthHeaders(request),
      cache: "no-store",
    });

    const data = await response.json();
    const normalizedData = normalizeCart(data);

    return NextResponse.json(normalizedData, {
      status: response.status,
    });
  } catch (error) {
    console.error("Cart API Error:", error);

    return NextResponse.json(
      { message: "Failed to fetch cart" },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();

    const response = await fetch(`${BACKEND_URL}/api/v1/cart/items`, {
      method: "POST",
      headers: await getAuthHeaders(request),
      body: JSON.stringify(body),
    });

    const data = await response.json();
    const normalizedData = normalizeCartItem(data);

    return NextResponse.json(normalizedData, {
      status: response.status,
    });
  } catch (error) {
    console.error("Add Cart Item Error:", error);

    return NextResponse.json(
      { message: "Failed to add cart item" },
      { status: 500 }
    );
  }
}