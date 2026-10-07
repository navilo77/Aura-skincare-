import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order_automation.models import (
    AutomationJob,
    InventoryAlert,
    InventoryTransaction,
    OrderEvent,
)
from app.modules.order_automation.repositories.automation import (
    AutomationJobRepository,
    InventoryAlertRepository,
    InventoryTransactionRepository,
    OrderEventRepository,
)


class InventoryTransactionService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = InventoryTransactionRepository(session)

    async def create(self, **kwargs: Any) -> InventoryTransaction:
        transaction = InventoryTransaction(**kwargs)
        return await self.repository.create(transaction)

    async def list_by_product(
        self, product_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> tuple[list[InventoryTransaction], int]:
        return await self.repository.list_by_product(product_id, skip=skip, limit=limit)


class OrderEventService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = OrderEventRepository(session)

    async def create(self, **kwargs: Any) -> OrderEvent:
        event = OrderEvent(**kwargs)
        return await self.repository.create(event)

    async def list_by_order(
        self, order_id: uuid.UUID, skip: int = 0, limit: int = 50
    ) -> tuple[list[OrderEvent], int]:
        return await self.repository.list_by_order(order_id, skip=skip, limit=limit)


class AutomationJobService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AutomationJobRepository(session)

    async def create(self, **kwargs: Any) -> AutomationJob:
        job = AutomationJob(**kwargs)
        return await self.repository.create(job)

    async def get_latest(self, job_type: str) -> AutomationJob | None:
        return await self.repository.get_by_job_type(job_type)

    async def mark_running(self, job_id: uuid.UUID) -> AutomationJob:
        job = await self.repository.get_by_id(job_id)
        if job:
            job.status = "running"
            job.started_at = datetime.now(UTC)
            await self.repository.session.flush()
            await self.repository.session.refresh(job)
        return job

    async def mark_completed(
        self, job_id: uuid.UUID, error_message: str | None = None
    ) -> AutomationJob:
        job = await self.repository.get_by_id(job_id)
        if job:
            job.status = "completed" if not error_message else "failed"
            job.completed_at = datetime.now(UTC)
            if error_message:
                job.error_message = error_message
            await self.repository.session.flush()
            await self.repository.session.refresh(job)
        return job


class InventoryAlertService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = InventoryAlertRepository(session)

    async def create(self, **kwargs: Any) -> InventoryAlert:
        alert = InventoryAlert(**kwargs)
        return await self.repository.create(alert)

    async def list_unresolved(
        self, skip: int = 0, limit: int = 50
    ) -> tuple[list[InventoryAlert], int]:
        return await self.repository.list_unresolved(skip=skip, limit=limit)

    async def resolve(self, alert_id: uuid.UUID) -> InventoryAlert:
        alert = await self.repository.get_by_id(alert_id)
        if alert:
            alert.is_resolved = True
            alert.resolved_at = datetime.now(UTC)
            await self.repository.session.flush()
            await self.repository.session.refresh(alert)
        return alert
