from __future__ import annotations

from typing import Any

from langgraph.graph import END, StateGraph

from app.modules.ai.agents.customer_agent import CustomerAIAgent
from app.modules.ai.agents.router_agent import RouterAgent
from app.modules.ai.schemas.ai import ChatRequest, ChatResponse
from app.modules.ai.tools.base import ToolRegistry


class LangGraphAIService:
    def __init__(self, tool_registry: ToolRegistry) -> None:
        self.router = RouterAgent()
        self.customer_agent = CustomerAIAgent(tool_registry)
        self.tool_registry = tool_registry
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(dict)

        async def router_node(state: dict) -> dict:
            request = state["request"]
            response = await self.router.handle(request)
            state["router_result"] = response
            state["next_agent"] = "customer"
            return state

        async def customer_node(state: dict) -> dict:
            request = state["request"]
            response = await self.customer_agent.handle(
                request,
                history=state.get("history", []),
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
    ) -> ChatResponse:
        state = {
            "request": request,
            "history": history or [],
        }
        result = await self.graph.ainvoke(state)
        return result["final_response"]
