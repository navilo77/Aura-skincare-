from typing import Any

from app.modules.ai.agents.base import BaseAgent
from app.modules.ai.schemas.ai import ChatRequest, ChatResponse
from app.modules.ai.services.prompt_manager import PromptManager
from app.modules.ai.tools.base import ToolRegistry


class CustomerAIAgent(BaseAgent):
    name = "customer"

    def __init__(self, tool_registry: ToolRegistry) -> None:
        self.prompt_manager = PromptManager()
        self.tool_registry = tool_registry

    async def handle(self, request: ChatRequest, **kwargs: Any) -> ChatResponse:
        history = kwargs.get("history", [])
        prompt = self.prompt_manager.build_context(request.message, history)
        tools_to_run = self._select_tools(request.message)

        tool_results = []
        for tool_name in tools_to_run:
            tool = self.tool_registry.get(tool_name)
            if tool:
                result = await tool.run(request)
                tool_results.append(result)

        response_parts = [prompt]
        if tool_results:
            response_parts.append("\n\nTool results:")
            for result in tool_results:
                response_parts.append(f"- {result.get('message', str(result))}")

        response_text = "\n".join(response_parts)
        guardrails = self.prompt_manager.get_guardrails()
        final_response = (
            f"{guardrails}\n\n{response_text}\n\n"
            "Remember: Only use verified information."
        )

        return ChatResponse(
            message=final_response,
            session_id=request.session_id,
            agent_type="customer",
            tool_calls=tool_results,
        )

    def _select_tools(self, message: str) -> list[str]:
        message_lower = message.lower()
        selected = []
        if any(
            keyword in message_lower
            for keyword in ["product", "search", "find", "recommend"]
        ):
            selected.append("search_products")
        if any(keyword in message_lower for keyword in ["cart", "basket"]):
            selected.append("get_cart")
        if any(keyword in message_lower for keyword in ["wishlist", "saved"]):
            selected.append("get_wishlist")
        if any(
            keyword in message_lower for keyword in ["order", "track", "status"]
        ):
            selected.append("track_order")
        if any(
            keyword in message_lower
            for keyword in ["shipping", "delivery", "cost"]
        ):
            selected.append("shipping_cost")
        if any(
            keyword in message_lower
            for keyword in ["coupon", "discount", "promo"]
        ):
            selected.append("coupons")
        if any(
            keyword in message_lower
            for keyword in ["stock", "available", "inventory"]
        ):
            selected.append("inventory_check")
        if any(
            keyword in message_lower
            for keyword in ["category", "categories"]
        ):
            selected.append("search_categories")
        return selected
