import uuid
from typing import Any

from app.modules.ai.repositories.conversation import (
    ConversationRepository,
    MessageRepository,
)
from app.modules.ai.services.customer_memory.conversation_memory import (
    ConversationMemory,
)
from app.modules.ai.services.customer_memory.preference_memory import (
    PreferenceMemory,
)
from app.modules.ai.services.customer_memory.profile_memory import (
    ProfileMemory,
)
from app.modules.ai.services.customer_memory.purchase_memory import (
    PurchaseMemory,
)
from app.modules.ai.services.customer_memory.shopping_memory import (
    ShoppingMemory,
)
from app.modules.cart.repositories.cart import CartItemRepository, CartRepository
from app.modules.customer.repositories.customer import CustomerRepository
from app.modules.order.repositories.order import OrderRepository
from app.modules.order.repositories.order_item import OrderItemRepository
from app.modules.product.repositories.brand import BrandRepository
from app.modules.product.repositories.product import ProductRepository
from app.modules.wishlist.repositories.wishlist import (
    WishlistItemRepository,
    WishlistRepository,
)


class CustomerMemoryService:
    def __init__(self, db_session) -> None:
        self.profile_memory = ProfileMemory(CustomerRepository(db_session))
        self.purchase_memory = PurchaseMemory(
            OrderRepository(db_session),
            OrderItemRepository(db_session),
        )
        self.shopping_memory = ShoppingMemory(
            CartRepository(db_session),
            CartItemRepository(db_session),
            WishlistRepository(db_session),
            WishlistItemRepository(db_session),
        )
        self.conversation_memory = ConversationMemory(
            ConversationRepository(db_session),
            MessageRepository(db_session),
        )
        self.preference_memory = PreferenceMemory(
            CustomerRepository(db_session),
            ProductRepository(db_session),
            BrandRepository(db_session),
        )

    async def get_customer_context(
        self, customer_id: uuid.UUID | None
    ) -> dict[str, Any]:
        if customer_id is None:
            return {}

        customer = await self.profile_memory.customer_repository.get_by_id(customer_id)
        if customer is None:
            return {}

        profile = await self.profile_memory.get_profile(customer_id)
        purchase_history = await self.purchase_memory.get_purchase_history(customer_id)
        shopping = await self.shopping_memory.get_shopping(customer_id)
        conversation = await self.conversation_memory.get_conversation(customer_id)
        preferences = await self.preference_memory.get_preferences(
            customer, purchase_history
        )

        return {
            "customer": profile,
            "purchase_history": purchase_history,
            "shopping": shopping,
            "conversation": conversation,
            "preferences": preferences,
        }
