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

export async function PATCH(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json();

    const response = await fetch(
      `${BACKEND_URL}/api/v1/cart/items/${params.id}`,
      {
        method: "PATCH",
        headers: await getAuthHeaders(request),
        body: JSON.stringify(body),
      }
    );

    const data = await response.json();
    const normalizedData = normalizeCartItem(data);

    return NextResponse.json(normalizedData, {
      status: response.status,
    });
  } catch (error) {
    console.error("Update Cart Item Error:", error);

    return NextResponse.json(
      { message: "Failed to update cart item" },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const response = await fetch(
      `${BACKEND_URL}/api/v1/cart/items/${params.id}`,
      {
        method: "DELETE",
        headers: await getAuthHeaders(request),
      }
    );

    if (response.status === 204) {
      return new NextResponse(null, { status: 204 });
    }

    const data = await response.json();

    return NextResponse.json(data, {
      status: response.status,
    });
  } catch (error) {
    console.error("Delete Cart Item Error:", error);

    return NextResponse.json(
      { message: "Failed to delete cart item" },
      { status: 500 }
    );
  }
}