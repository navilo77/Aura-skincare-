import uuid
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.payment.models import Payment, PaymentMethod, Refund
from app.modules.payment.repositories.base import BaseRepository


class PaymentRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Payment)

    async def get_by_order_id(self, order_id: uuid.UUID) -> list[Payment]:
        stmt = select(Payment).where(Payment.order_id == order_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_customer_id(
        self, customer_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> tuple[list[Payment], int]:
        stmt = select(Payment).where(Payment.customer_id == customer_id)
        count_stmt = (
            select(func.count())
            .select_from(Payment)
            .where(Payment.customer_id == customer_id)
        )

        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()

        stmt = stmt.order_by(Payment.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def get_by_stripe_payment_intent_id(
        self, stripe_payment_intent_id: str
    ) -> Payment | None:
        stmt = select(Payment).where(
            Payment.stripe_payment_intent_id == stripe_payment_intent_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **kwargs: Any) -> Payment:
        payment = Payment(**kwargs)
        self.session.add(payment)
        await self.session.flush()
        return payment


class PaymentMethodRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, PaymentMethod)

    async def get_by_customer_id(
        self, customer_id: uuid.UUID, skip: int = 0, limit: int = 20
    ) -> tuple[list[PaymentMethod], int]:
        stmt = select(PaymentMethod).where(PaymentMethod.customer_id == customer_id)
        count_stmt = (
            select(func.count())
            .select_from(PaymentMethod)
            .where(PaymentMethod.customer_id == customer_id)
        )

        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()

        stmt = stmt.order_by(PaymentMethod.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def get_by_stripe_payment_method_id(
        self, stripe_payment_method_id: str
    ) -> PaymentMethod | None:
        stmt = select(PaymentMethod).where(
            PaymentMethod.stripe_payment_method_id == stripe_payment_method_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_default(self, customer_id: uuid.UUID) -> PaymentMethod | None:
        stmt = select(PaymentMethod).where(
            PaymentMethod.customer_id == customer_id, PaymentMethod.is_default
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def set_default(
        self, customer_id: uuid.UUID, payment_method_id: uuid.UUID
    ) -> None:
        # Unset current default
        stmt = select(PaymentMethod).where(
            PaymentMethod.customer_id == customer_id, PaymentMethod.is_default
        )
        result = await self.session.execute(stmt)
        current_default = result.scalar_one_or_none()
        if current_default:
            current_default.is_default = False

        # Set new default
        stmt = select(PaymentMethod).where(PaymentMethod.id == payment_method_id)
        result = await self.session.execute(stmt)
        new_default = result.scalar_one_or_none()
        if new_default:
            new_default.is_default = True

        await self.session.flush()

    async def create(self, **kwargs: Any) -> PaymentMethod:
        payment_method = PaymentMethod(**kwargs)
        self.session.add(payment_method)
        await self.session.flush()
        return payment_method


class RefundRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Refund)

    async def get_by_payment_id(self, payment_id: uuid.UUID) -> list[Refund]:
        stmt = select(Refund).where(Refund.payment_id == payment_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_stripe_refund_id(self, stripe_refund_id: str) -> Refund | None:
        stmt = select(Refund).where(Refund.stripe_refund_id == stripe_refund_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **kwargs: Any) -> Refund:
        refund = Refund(**kwargs)
        self.session.add(refund)
        await self.session.flush()
        return refund
