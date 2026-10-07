import uuid

from app.modules.cart.repositories.cart import CartItemRepository, CartRepository
from app.modules.wishlist.repositories.wishlist import (
    WishlistItemRepository,
    WishlistRepository,
)


class ShoppingMemory:
    def __init__(
        self,
        cart_repository: CartRepository,
        cart_item_repository: CartItemRepository,
        wishlist_repository: WishlistRepository,
        wishlist_item_repository: WishlistItemRepository,
    ) -> None:
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository
        self.wishlist_repository = wishlist_repository
        self.wishlist_item_repository = wishlist_item_repository

    async def get_shopping(self, customer_id: uuid.UUID) -> dict[str, list]:
        cart = await self.cart_repository.get_by_user_id(customer_id)
        cart_items: list[dict] = []
        if cart:
            items = await self.cart_item_repository.list_by_cart(cart.id)
            for item in items:
                cart_items.append(
                    {
                        "product_id": str(item.product_id),
                        "product_variant_id": (
                            str(item.product_variant_id)
                            if item.product_variant_id
                            else None
                        ),
                        "quantity": item.quantity,
                        "unit_price": float(item.unit_price),
                        "subtotal": float(item.subtotal),
                    }
                )

        wishlist = await self.wishlist_repository.get_by_user_id(customer_id)
        wishlist_items: list[dict] = []
        if wishlist:
            items = await self.wishlist_item_repository.list_by_wishlist(wishlist.id)
            for item in items:
                wishlist_items.append(
                    {
                        "product_id": str(item.product_id),
                        "product_variant_id": (
                            str(item.product_variant_id)
                            if item.product_variant_id
                            else None
                        ),
                    }
                )

        return {"cart": cart_items, "wishlist": wishlist_items}
