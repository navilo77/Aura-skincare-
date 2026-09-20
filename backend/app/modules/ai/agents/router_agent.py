from typing import Any

from app.modules.ai.agents.base import BaseAgent
from app.modules.ai.schemas.ai import ChatRequest, ChatResponse
from app.modules.ai.services.prompt_manager import PromptManager


class RouterAgent(BaseAgent):
    name = "router"

    def __init__(self) -> None:
        self.prompt_manager = PromptManager()

    async def handle(self, request: ChatRequest, **kwargs: Any) -> ChatResponse:
        self.prompt_manager.get_router_prompt()
        user_message = request.message.strip().lower()

        if any(
            keyword in user_message
            for keyword in ["order", "tracking", "shipping", "delivery"]
        ):
            agent = "customer"
            confidence = 0.9
            reasoning = "User is asking about order or shipping"
        elif any(
            keyword in user_message
            for keyword in ["product", "recommend", "skin", "price"]
        ):
            agent = "customer"
            confidence = 0.9
            reasoning = "User is asking about products or skincare"
        elif any(
            keyword in user_message for keyword in ["admin", "dashboard", "manage"]
        ):
            agent = "admin"
            confidence = 0.8
            reasoning = "User is asking about admin tasks"
        elif any(
            keyword in user_message
            for keyword in ["campaign", "marketing", "social"]
        ):
            agent = "marketing"
            confidence = 0.8
            reasoning = "User is asking about marketing"
        elif any(
            keyword in user_message
            for keyword in ["help", "support", "return", "refund"]
        ):
            agent = "support"
            confidence = 0.8
            reasoning = "User is asking for support"
        else:
            agent = "customer"
            confidence = 0.5
            reasoning = "Default to customer agent"

        return ChatResponse(
            message=f"{agent}|{confidence}|{reasoning}",
            session_id=request.session_id,
            agent_type="router",
            tool_calls=[{"agent": agent, "confidence": confidence}],
        )
