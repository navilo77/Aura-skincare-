import { NextResponse } from "next/server";

const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";

function normalizeProduct(product: Record<string, unknown>): Record<string, unknown> {
  const normalized = { ...product };
  if (typeof normalized.price === "string") {
    normalized.price = parseFloat(normalized.price);
  }
  if (normalized.compare_at_price && typeof normalized.compare_at_price === "string") {
    normalized.compare_at_price = parseFloat(normalized.compare_at_price);
  }
  if (normalized.thumbnail_url === null) {
    normalized.thumbnail_url = undefined;
  }
  return normalized;
}

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const query = searchParams.toString();

    const response = await fetch(
      `${BACKEND_URL}/api/v1/products${query ? `?${query}` : ""}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        cache: "no-store",
      }
    );

    const data = await response.json();
    const normalizedData = Array.isArray(data) ? data.map(normalizeProduct) : data;

    return NextResponse.json(normalizedData, {
      status: response.status,
    });
  } catch (error) {
    console.error("Products API Error:", error);

    return NextResponse.json(
      {
        success: false,
        message: "Failed to fetch products",
      },
      {
        status: 500,
      }
    );
  }
}