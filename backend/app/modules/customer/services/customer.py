import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.customer.models import Customer
from app.modules.customer.repositories.customer import CustomerRepository


class CustomerService:
    def __init__(self, session: AsyncSession):
        self.repository = CustomerRepository(session)

    async def create(
        self,
        full_name: str,
        email: str,
        phone: str | None = None,
        status: str = "active",
        skin_type: str | None = None,
        skin_concerns: list[str] | None = None,
    ) -> Customer:
        email = self._normalize_email(email)
        if phone:
            phone = self._normalize_phone(phone)

        await self._validate_email_unique(email)
        if phone:
            await self._validate_phone_unique(phone)

        self._validate_status(status)

        customer = Customer(
            full_name=full_name.strip(),
            email=email,
            phone=phone,
            status=status,
            skin_type=skin_type.strip() if skin_type else None,
            skin_concerns=skin_concerns,
        )
        return await self.repository.create(customer)

    async def update(
        self,
        customer_id: uuid.UUID,
        full_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        status: str | None = None,
        skin_type: str | None = None,
        skin_concerns: list[str] | None = None,
    ) -> Customer:
        customer = await self.repository.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")

        if email is not None:
            email = self._normalize_email(email)
            await self._validate_email_unique(email, exclude_id=customer_id)
            customer.email = email

        if phone is not None:
            phone = self._normalize_phone(phone)
            if phone:
                await self._validate_phone_unique(phone, exclude_id=customer_id)
            customer.phone = phone

        if full_name is not None:
            customer.full_name = full_name.strip()

        if status is not None:
            self._validate_status(status)
            customer.status = status

        if skin_type is not None:
            customer.skin_type = skin_type.strip() if skin_type else None

        if skin_concerns is not None:
            customer.skin_concerns = skin_concerns

        return await self.repository.update(customer)

    async def delete(self, customer_id: uuid.UUID) -> None:
        customer = await self.repository.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")

        await self.repository.delete(customer_id)

    async def get_by_id(self, customer_id: uuid.UUID) -> Customer | None:
        return await self.repository.get_by_id(customer_id)

    async def get_list(
        self,
        skip: int = 0,
        limit: int = 20,
        status: str | None = None,
        search: str | None = None,
    ) -> tuple[list[Customer], int]:
        return await self.repository.get_list(
            skip=skip, limit=limit, status=status, search=search
        )

    async def _validate_email_unique(
        self, email: str, exclude_id: uuid.UUID | None = None
    ) -> None:
        if exclude_id:
            if await self.repository.exists_by_email_excluding_id(email, exclude_id):
                raise ValueError(f"Email {email} is already in use")
        else:
            if await self.repository.exists_by_email(email):
                raise ValueError(f"Email {email} is already in use")

    async def _validate_phone_unique(
        self, phone: str, exclude_id: uuid.UUID | None = None
    ) -> None:
        if not phone:
            return
        if exclude_id:
            if await self.repository.exists_by_phone_excluding_id(phone, exclude_id):
                raise ValueError(f"Phone {phone} is already in use")
        else:
            if await self.repository.exists_by_phone(phone):
                raise ValueError(f"Phone {phone} is already in use")

    @staticmethod
    def _validate_status(status: str) -> None:
        valid_statuses = ["active", "inactive", "suspended"]
        if status not in valid_statuses:
            raise ValueError(
                f"Invalid status: {status}. Must be one of: {', '.join(valid_statuses)}"
            )

    @staticmethod
    def _normalize_email(email: str) -> str:
        return email.strip().lower()

    @staticmethod
    def _normalize_phone(phone: str) -> str:
        return phone.strip()
