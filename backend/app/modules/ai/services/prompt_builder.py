from pathlib import Path
from typing import Any

from app.modules.ai.schemas.ai import ChatRequest
from app.modules.ai.services.rag.schemas import RetrievalContext


class PromptBuilder:
    def __init__(self) -> None:
        self.prompts: dict[str, str] = {}
        prompts_dir = Path(__file__).parent.parent / "prompts"
        for prompt_file in prompts_dir.glob("*.md"):
            name = prompt_file.stem
            self.prompts[name] = prompt_file.read_text(encoding="utf-8")

    def build(self, context: dict[str, Any]) -> str:
        request: ChatRequest = context["request"]
        history: list[dict[str, Any]] = context.get("history", [])
        tool_results: list[dict[str, Any]] | None = context.get("tool_results")
        customer_context: dict[str, Any] | None = context.get("customer_context")
        rag_context: RetrievalContext | None = context.get("rag_context")

        prompt_parts = [
            self.prompts.get("system", ""),
            self.prompts.get("customer", ""),
            self.prompts.get("guardrails", ""),
        ]

        if rag_context and rag_context.has_results:
            prompt_parts.append("\n\nAura Business Knowledge (verified):")
            for chunk in rag_context.chunks:
                prompt_parts.append(
                    f"- [{chunk.category}] {chunk.content}"
                )
            prompt_parts.append(
                "\nUse only the verified business knowledge above "
                "when answering policy, shipping, returns, coupons, "
                "ingredients and similar questions."
            )

        if tool_results:
            prompt_parts.append("\n\nVerified Product Data (from tools):")
            for result in tool_results:
                prompt_parts.append(f"- {result.get('message', str(result))}\n")

        if customer_context:
            customer = customer_context.get("customer", {})
            if customer:
                prompt_parts.append("\n\nCustomer Profile:")
                if customer.get("name"):
                    prompt_parts.append(f"- Name: {customer['name']}")
                if customer.get("skin_type"):
                    prompt_parts.append(f"- Skin Type: {customer['skin_type']}")
                if customer.get("skin_concerns"):
                    concerns = ", ".join(customer["skin_concerns"])
                    prompt_parts.append(f"- Skin Concerns: {concerns}")
                if customer.get("status"):
                    prompt_parts.append(f"- Status: {customer['status']}")

            purchase_history = customer_context.get("purchase_history", [])
            if purchase_history:
                prompt_parts.append("\n\nPurchase History:")
                for order in purchase_history[:5]:
                    prompt_parts.append(
                        f"- Order {order.get('order_number', '')}: "
                        f"{order.get('status', '')} | "
                        f"{order.get('currency', '')} {order.get('total_amount', 0)}"
                    )
                    items = order.get("items", [])
                    for item in items[:3]:
                        prompt_parts.append(
                            f"  * {item.get('product_name', '')}"
                            f" x{item.get('quantity', 0)}"
                        )

            shopping = customer_context.get("shopping", {})
            cart_items = shopping.get("cart", [])
            if cart_items:
                prompt_parts.append("\n\nCurrent Cart:")
                for item in cart_items[:5]:
                    prompt_parts.append(
                        f"- Product {item.get('product_id', '')}"
                        f" x{item.get('quantity', 0)}"
                    )

            wishlist_items = shopping.get("wishlist", [])
            if wishlist_items:
                prompt_parts.append("\n\nWishlist:")
                for item in wishlist_items[:5]:
                    prompt_parts.append(f"- Product {item.get('product_id', '')}")

            conversation = customer_context.get("conversation", {})
            summary = conversation.get("summary", "")
            if summary:
                prompt_parts.append("\n\nPrevious Conversation Summary:")
                prompt_parts.append(summary)

            recent_topics = conversation.get("recent_topics", [])
            if recent_topics:
                prompt_parts.append("\n\nRecent Topics:")
                prompt_parts.append(", ".join(recent_topics[:10]))

            previous_recommendations = conversation.get("previous_recommendations", [])
            if previous_recommendations:
                prompt_parts.append("\n\nPrevious Recommendations:")
                for rec in previous_recommendations[-3:]:
                    prompt_parts.append(f"- {rec[:200]}")

            preferences = customer_context.get("preferences", {})
            if preferences:
                prompt_parts.append("\n\nCustomer Preferences:")
                if preferences.get("language"):
                    prompt_parts.append(
                        f"- Preferred Language: {preferences['language']}"
                    )
                if preferences.get("favorite_brands"):
                    brands = ", ".join(preferences["favorite_brands"])
                    prompt_parts.append(f"- Favorite Brands: {brands}")
                if preferences.get("budget"):
                    prompt_parts.append(f"- Budget Range: {preferences['budget']}")
                if preferences.get("routine"):
                    prompt_parts.append(
                        f"- Preferred Routine: {preferences['routine']}"
                    )
                if preferences.get("avoid_ingredients"):
                    avoid = ", ".join(preferences["avoid_ingredients"])
                    prompt_parts.append(f"- Ingredients to Avoid: {avoid}")

        if history:
            prompt_parts.append("\n\nConversation history:")
            for entry in history[-10:]:
                role = entry.get("role", "user")
                content = entry.get("content", "")
                prompt_parts.append(f"{role}: {content}")
        prompt_parts.append(f"\n\nUser: {request.message}\nAssistant:")
        prompt = "\n".join(prompt_parts)
        return prompt
