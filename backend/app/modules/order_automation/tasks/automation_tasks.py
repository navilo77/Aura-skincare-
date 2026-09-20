from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.repositories.inventory import InventoryRepository
from app.modules.order_automation.repositories.automation import (
    AutomationJobRepository,
    InventoryAlertRepository,
)
from app.modules.order_automation.services.automation import AutomationJobService


class AutomationTasks:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.inventory_repository = InventoryRepository(session)
        self.job_repository = AutomationJobRepository(session)
        self.alert_repository = InventoryAlertRepository(session)
        self.job_service = AutomationJobService(session)

    async def run_inventory_sync(self) -> None:
        job = await self.job_service.create(
            job_type="inventory_sync",
            status="running",
            started_at=datetime.now(UTC),
        )
        try:
            pass
        except Exception as exc:
            await self.job_service.mark_completed(job.id, error_message=str(exc))
            raise
        await self.job_service.mark_completed(job.id)

    async def run_low_stock_scan(self) -> None:
        job = await self.job_service.create(
            job_type="low_stock_scan",
            status="running",
            started_at=datetime.now(UTC),
        )
        try:
            inventories, _ = await self.inventory_repository.get_list(skip=0, limit=1000)
            for inventory in inventories[0]:
                available = inventory.quantity_on_hand - inventory.quantity_reserved
                if available <= inventory.low_stock_threshold and not inventory.is_tracking_enabled:
                    continue
                alert_type = "out_of_stock" if available <= 0 else "low_stock"
                await self.alert_repository.create(
                    product_id=inventory.product_id,
                    warehouse_id=inventory.warehouse_id,
                    alert_type=alert_type,
                    message=f"Product {inventory.product_id} is {alert_type} with {available} units available",
                )
        except Exception as exc:
            await self.job_service.mark_completed(job.id, error_message=str(exc))
            raise
        await self.job_service.mark_completed(job.id)

    async def run_expired_reservation_cleanup(self) -> None:
        job = await self.job_service.create(
            job_type="expired_reservation_cleanup",
            status="running",
            started_at=datetime.now(UTC),
        )
        try:
            pass
        except Exception as exc:
            await self.job_service.mark_completed(job.id, error_message=str(exc))
            raise
        await self.job_service.mark_completed(job.id)

    async def run_order_event_processing(self, order_id: str, event_type: str) -> None:
        job = await self.job_service.create(
            job_type="order_event_processing",
            status="running",
            started_at=datetime.now(UTC),
            metadata='{"order_id": "%s", "event_type": "%s"}' % (order_id, event_type),
        )
        try:
            pass
        except Exception as exc:
            await self.job_service.mark_completed(job.id, error_message=str(exc))
            raise
        await self.job_service.mark_completed(job.id)
