from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.integrations.n8n import n8n_client
from app.modules.inventory.repositories.inventory import InventoryRepository
from app.modules.order_automation.models import (
    OrderEvent,
)
from app.modules.order_automation.repositories.automation import (
    AutomationJobRepository,
    InventoryAlertRepository,
    InventoryTransactionRepository,
    OrderEventRepository,
)
from app.modules.order_automation.services.automation import (
    AutomationJobService,
    InventoryAlertService,
)


class AutomationTasks:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.inventory_repository = InventoryRepository(session)
        self.job_repository = AutomationJobRepository(session)
        self.alert_repository = InventoryAlertRepository(session)
        self.transaction_repository = InventoryTransactionRepository(session)
        self.order_event_repository = OrderEventRepository(session)
        self.job_service = AutomationJobService(session)
        self.alert_service = InventoryAlertService(session)

    async def run_inventory_sync(self) -> None:
        job = await self.job_service.create(
            job_type="inventory_sync",
            status="running",
            started_at=datetime.now(UTC),
        )
        try:
            # Sync inventory with external systems (ERP, WMS, etc.)
            # This would integrate with n8n workflows
            await self._trigger_n8n_workflow("inventory_sync", {"job_id": str(job.id)})
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
            inventories, _ = await self.inventory_repository.get_list(
                skip=0, limit=1000
            )
            for inventory in inventories[0]:
                available = inventory.quantity_on_hand - inventory.quantity_reserved
                if (
                    available <= inventory.low_stock_threshold
                    and not inventory.is_tracking_enabled
                ):
                    continue
                alert_type = "out_of_stock" if available <= 0 else "low_stock"
                await self.alert_repository.create(
                    product_id=inventory.product_id,
                    warehouse_id=inventory.warehouse_id,
                    alert_type=alert_type,
                    message=f"Product {inventory.product_id} is {alert_type} with {available} units available",
                )
                # Trigger n8n workflow for alert notification
                await self._trigger_n8n_workflow(
                    "inventory_alert",
                    {
                        "product_id": str(inventory.product_id),
                        "warehouse_id": str(inventory.warehouse_id),
                        "alert_type": alert_type,
                        "available": available,
                        "threshold": inventory.low_stock_threshold,
                    },
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
            # Find and release expired reservations
            # This would release inventory reservations that have expired
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
            extra_metadata='{"order_id": "%s", "event_type": "%s"}'
            % (order_id, event_type),
        )
        try:
            # Create order event record
            order_uuid = uuid.UUID(order_id)
            event = OrderEvent(
                order_id=order_uuid,
                event_type=event_type,
                description=f"Order {event_type}",
            )
            await self.order_event_repository.create(event)

            # Trigger n8n workflow for order event
            await self._trigger_n8n_workflow(
                f"order_{event_type}",
                {
                    "order_id": order_id,
                    "event_type": event_type,
                },
            )

            # Specific workflows based on event type
            if event_type == "confirmed":
                await self._trigger_n8n_workflow(
                    "order_confirmation", {"order_id": order_id}
                )
            elif event_type == "shipped":
                await self._trigger_n8n_workflow(
                    "order_shipped", {"order_id": order_id}
                )
            elif event_type == "delivered":
                await self._trigger_n8n_workflow(
                    "order_delivered", {"order_id": order_id}
                )
            elif event_type == "cancelled":
                await self._trigger_n8n_workflow(
                    "order_cancelled", {"order_id": order_id}
                )
                # Release inventory reservations
                await self._release_order_reservations(order_uuid)
            elif event_type == "refunded":
                await self._trigger_n8n_workflow(
                    "order_refunded", {"order_id": order_id}
                )

        except Exception as exc:
            await self.job_service.mark_completed(job.id, error_message=str(exc))
            raise
        await self.job_service.mark_completed(job.id)

    async def _release_order_reservations(self, order_id: uuid.UUID) -> None:
        # Release inventory reservations for this order
        # This would integrate with inventory module
        pass

    async def _trigger_n8n_workflow(
        self, workflow_name: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        webhook_url = f"{settings.n8n_webhook_url}/{workflow_name}"
        return await n8n_client.trigger_webhook(webhook_url, payload)
