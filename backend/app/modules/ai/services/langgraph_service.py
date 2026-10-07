from __future__ import annotations

from typing import Any

from langgraph.graph import END, StateGraph

from app.modules.ai.agents.customer_agent import CustomerAIAgent
from app.modules.ai.agents.router_agent import RouterAgent
from app.modules.ai.providers.base import AIProvider
from app.modules.ai.schemas.ai import ChatRequest, ChatResponse
from app.modules.ai.services.customer_memory import CustomerMemoryService
from app.modules.ai.services.prompt_builder import PromptBuilder
from app.modules.ai.services.rag.rag_service import RAGService
from app.modules.ai.services.tool_manager import ToolCallLogger, ToolManager
from app.modules.ai.tools.base import ToolRegistry


class LangGraphAIService:
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
        self.router = RouterAgent()
        self.customer_agent = CustomerAIAgent(
            tool_registry,
            ai_provider=ai_provider,
            prompt_builder=prompt_builder,
            tool_manager=tool_manager,
            customer_memory_service=customer_memory_service,
            tool_call_logger=tool_call_logger,
            rag_service=rag_service,
        )
        self.tool_registry = tool_registry
        self.rag_service = rag_service
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(dict)

        async def router_node(state: dict) -> dict:
            request = state["request"]
            response = await self.router.handle(request)
            state["router_result"] = response
            # TODO: Extend graph with admin/marketing/support agent nodes
            # Currently all routed requests go to customer agent per intentional design
            state["next_agent"] = response.next_agent
            return state

        async def customer_node(state: dict) -> dict:
            request = state["request"]
            response = await self.customer_agent.handle(
                request,
                history=state.get("history", []),
                db=state.get("db"),
                user_id=state.get("user_id"),
                rag_service=self.rag_service,
            )
            state["final_response"] = response
            return state

        graph.add_node("router", router_node)
        graph.add_node("customer", customer_node)

        graph.set_entry_point("router")
        graph.add_edge("router", "customer")
        graph.add_edge("customer", END)

        return graph.compile()

    async def chat(
        self,
        request: ChatRequest,
        history: list[dict[str, Any]] | None = None,
        db: Any = None,
        user_id: Any = None,
    ) -> ChatResponse:
        state = {
            "request": request,
            "history": history or [],
            "db": db,
            "user_id": user_id,
        }
        result = await self.graph.ainvoke(state)
        return result["final_response"]
