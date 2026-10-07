import logging
from typing import Any

from app.modules.ai.agents.base import BaseAgent
from app.modules.ai.providers.base import AIProvider
from app.modules.ai.schemas.ai import ChatRequest, ChatResponse
from app.modules.ai.services.customer_memory import CustomerMemoryService
from app.modules.ai.services.prompt_builder import PromptBuilder
from app.modules.ai.services.rag.rag_service import RAGService
from app.modules.ai.services.rag.schemas import SearchQuery
from app.modules.ai.services.tool_manager import ToolCallLogger, ToolManager
from app.modules.ai.tools.base import ToolRegistry

logger = logging.getLogger(__name__)


class CustomerAIAgent(BaseAgent):
    name = "customer"

    def __init__(
        self,
        tool_registry: ToolRegistry,
        ai_provider: AIProvider,
        prompt_builder: PromptBuilder,
        tool_manager: ToolManager,
        customer_memory_service: CustomerMemoryService,
        tool_call_logger: ToolCallLogger | None = None,
        rag_service: RAGService | None = None,
    ) -> None:
        self.prompt_builder = prompt_builder
        self.tool_registry = tool_registry
        self.ai_provider = ai_provider
        self.tool_manager = tool_manager
        self.customer_memory_service = customer_memory_service
        self.tool_call_logger = tool_call_logger
        self.rag_service = rag_service

    async def handle(self, request: ChatRequest, **kwargs: Any) -> ChatResponse:
        history = kwargs.get("history", [])
        db = kwargs.get("db")
        user_id = kwargs.get("user_id")
        tools_to_run = self._select_tools(request.message)
        tool_results = await self.tool_manager.execute(
            request, tools_to_run, db=db, tool_call_logger=self.tool_call_logger
        )

        customer_context = {}
        if self.customer_memory_service and user_id:
            customer_context = await self.customer_memory_service.get_customer_context(
                user_id
            )

        rag_context = None
        if self.rag_service is not None:
            rag_query = self._build_rag_query(request.message)
            if rag_query is not None:
                try:
                    rag_context = await self.rag_service.search(rag_query)
                except Exception as exc:
                    logger.warning(
                        "RAG retrieval failed for '%s': %s. Continuing "
                        "without knowledge.",
                        request.message,
                        exc,
                    )

        full_prompt = self.prompt_builder.build(
            {
                "request": request,
                "history": history,
                "tool_results": tool_results,
                "customer_context": customer_context or None,
                "rag_context": rag_context,
            }
        )

        ai_message = await self.ai_provider.generate(full_prompt)

        if not ai_message:
            ai_message = self._generate_fallback_response(request.message, tool_results)

        return ChatResponse(
            message=ai_message,
            session_id=request.session_id,
            agent_type="customer",
            tool_calls=tool_results,
        )

    def _build_rag_query(self, message: str) -> SearchQuery | None:
        query = message.strip().lower()
        if not query:
            return None

        knowledge_terms = (
            "policy",
            "policies",
            "refund",
            "return",
            "exchange",
            "shipping",
            "delivery",
            "coupon",
            "discount",
            "promotion",
            "promotions",
            "privacy",
            "terms",
            "ingredient",
            "ingredients",
            "side effect",
            "side effects",
            "how to use",
            "usage",
            "suitable",
            "skin type",
            "skin concern",
            "guide",
            "faq",
            "business hours",
            "hours",
            "contact",
            "warranty",
            "guarantee",
            "payment method",
            "membership",
            "reward",
            "verification",
            "authentic",
        )

        for term in knowledge_terms:
            if term in query:
                return SearchQuery(query=message.strip(), status="available")

        return None

    def _generate_fallback_response(
        self,
        user_message: str,
        tool_results: list[dict[str, Any]],
    ) -> str:
        user_msg = user_message.strip().lower()

        # Greetings
        if user_msg in ["hi", "hello", "hey", "সালাম", "হ্যালো", "কেমন আছেন", "hi there"]:
            return (
                "হ্যালো! **Aura Skincare**-এ আপনাকে স্বাগতম। 🌿\n\n"
                "আমি আপনার ভার্চুয়াল বিউটি কনসালট্যান্ট **Aura AI**। আপনার ত্বক, প্রোডাক্ট বা স্কিনকেয়ার "
                "রুটিন সংক্রান্ত যেকোনো বিষয়ে আমি সাহায্য করতে পারি। আজ আপনাকে কীভাবে সাহায্য করতে পারি?"
            )

        # Check for product tool results first
        found_products: list[dict[str, Any]] = []
        for res in tool_results:
            if res.get("tool") == "search_products" and res.get("results"):
                found_products = res["results"]
                break

        if found_products:
            lines = ["হ্যাঁ, **Aura Skincare**-এ আমাদের চমৎকার কিছু প্রোডাক্ট রয়েছে: 🌸\n"]
            for p in found_products[:3]:
                name = p.get("name", "Product")
                price = p.get("price", "")
                desc = p.get("description", "")
                price_str = f" - মূল্য: **{price}**" if price else ""
                lines.append(f"• **{name}**{price_str}")
                if desc:
                    lines.append(f"  _{desc}_")
            lines.append(
                "\nআপনার ত্বকের টাইপ (শুষ্ক, তৈলাক্ত বা সংবেদনশীল) জানালে আমি আপনাকে সবচেয়ে উপযুক্ত প্রোডাক্টটি সাজেস্ট করতে পারি।"
            )
            return "\n".join(lines)

        return (
            "ধন্যবাদ! **Aura Skincare**-এর পণ্য, উপাদান, দাম বা স্কিনকেয়ার রুটিন সংক্রান্ত "
            "যেকোনো প্রশ্নের উত্তর দিতে আমি প্রস্তুত। আপনার ত্বক বা পছন্দের প্রোডাক্ট সম্পর্কে আরেকটু বিস্তারিত বলবেন?"
        )

    def _select_tools(self, message: str) -> list[str]:
        message_lower = message.lower()
        selected = []
        if any(
            keyword in message_lower
            for keyword in [
                "product",
                "search",
                "find",
                "recommend",
                "cream",
                "serum",
                "lotion",
                "cleanser",
                "sunscreen",
                "facewash",
                "oil",
                "acne",
                "skin",
                "আছে",
                "ক্রিম",
                "দাম",
                "প্রোডাক্ট",
                "price",
                "ময়েশ্চারাইজার",
            ]
        ):
            selected.append("search_products")
        if any(keyword in message_lower for keyword in ["cart", "basket"]):
            selected.append("get_cart")
        if any(keyword in message_lower for keyword in ["wishlist", "saved"]):
            selected.append("get_wishlist")
        if any(keyword in message_lower for keyword in ["order", "track", "status"]):
            selected.append("track_order")
        if any(
            keyword in message_lower for keyword in ["shipping", "delivery", "cost"]
        ):
            selected.append("shipping_cost")
        if any(keyword in message_lower for keyword in ["coupon", "discount", "promo"]):
            selected.append("coupons")
        if any(
            keyword in message_lower for keyword in ["stock", "available", "inventory"]
        ):
            selected.append("inventory_check")
        if any(keyword in message_lower for keyword in ["category", "categories"]):
            selected.append("search_categories")
        return selected
