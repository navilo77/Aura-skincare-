import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.models import ToolCallLog
from app.modules.ai.repositories.tool_call_log import ToolCallLogRepository


class ToolCallLogService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = ToolCallLogRepository(session)

    async def log_tool_call(
        self,
        session_id: str,
        tool_name: str,
        arguments: str | None = None,
        result: str | None = None,
        status: str = "success",
        latency_ms: int | None = None,
        error_message: str | None = None,
        message_id: uuid.UUID | None = None,
    ) -> ToolCallLog:
        log = ToolCallLog(
            session_id=session_id,
            message_id=message_id,
            tool_name=tool_name,
            arguments=arguments,
            result=result,
            status=status,
            latency_ms=latency_ms,
            error_message=error_message,
        )
        return await self.repository.create(log)
