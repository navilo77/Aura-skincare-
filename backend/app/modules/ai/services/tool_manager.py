import logging
import time
from typing import Any, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.schemas.ai import ChatRequest
from app.modules.ai.tools.base import ToolRegistry

logger = logging.getLogger(__name__)


class ToolCallLogger(Protocol):
    async def __call__(
        self,
        tool_name: str,
        message: str,
        result: dict[str, Any],
        latency_ms: float,
        *,
        status: str = ...,
        error_message: str | None = ...,
    ) -> None: ...


class ToolManager:
    def __init__(
        self,
        tool_registry: ToolRegistry,
    ) -> None:
        self.tool_registry = tool_registry

    async def execute(
        self,
        request: ChatRequest,
        tool_names: list[str],
        db: AsyncSession | None = None,
        tool_call_logger: ToolCallLogger | None = None,
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for tool_name in tool_names:
            tool = self.tool_registry.get(tool_name)
            if not tool:
                continue
            start = time.perf_counter()
            try:
                result = await tool.run(request, db=db)
                latency_ms = (time.perf_counter() - start) * 1000
                if tool_call_logger is not None:
                    await tool_call_logger(
                        tool_name,
                        request.message,
                        result,
                        latency_ms,
                        status="success",
                    )
            except Exception as exc:
                latency_ms = (time.perf_counter() - start) * 1000
                logger.error("Tool %s failed: %s", tool_name, exc)
                result = {"tool": tool_name, "message": str(exc)}
                if tool_call_logger is not None:
                    await tool_call_logger(
                        tool_name,
                        request.message,
                        result,
                        latency_ms,
                        status="error",
                        error_message=str(exc),
                    )
            results.append(result)
        return results
