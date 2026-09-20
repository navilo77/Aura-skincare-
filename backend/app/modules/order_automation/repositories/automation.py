import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order_automation.models import (
    AutomationJob,
    InventoryAlert,
    InventoryTransaction,
    OrderEvent,
)
from app.modules.order_automation.repositories.base import BaseRepository


class InventoryTransactionRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, InventoryTransaction)

    async def list_by_product(self, product_id: uuid.UUID, skip: int = 0, limit: int = 20) -> tuple[list[InventoryTransaction], int]:
        return await self.get_list(skip=skip, limit=limit, product_id=product_id)


class OrderEventRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, OrderEvent)

    async def list_by_order(self, order_id: uuid.UUID, skip: int = 0, limit: int = 50) -> tuple[list[OrderEvent], int]:
        return await self.get_list(skip=skip, limit=limit, order_id=order_id)


class AutomationJobRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, AutomationJob)

    async def get_by_job_type(self, job_type: str) -> AutomationJob | None:
        result = await self.session.execute(
            select(AutomationJob)
            .where(AutomationJob.job_type == job_type)
            .order_by(AutomationJob.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()


class InventoryAlertRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, InventoryAlert)

    async def list_unresolved(self, skip: int = 0, limit: int = 50) -> tuple[list[InventoryAlert], int]:
        query = select(InventoryAlert).where(InventoryAlert.is_resolved == False)  # noqa: E712
        total_result = await self.session.execute(select(InventoryAlert.id).where(InventoryAlert.is_resolved == False))  # noqa: E712
        total = len(total_result.scalars().all())
        paginated_query = query.offset(skip).limit(limit)
        result = await self.session.execute(paginated_query)
        return list(result.scalars().all()), total
