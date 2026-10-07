import uuid
from typing import Any

from app.modules.customer.repositories.customer import CustomerRepository


class ProfileMemory:
    def __init__(self, customer_repository: CustomerRepository) -> None:
        self.customer_repository = customer_repository

    async def get_profile(self, customer_id: uuid.UUID) -> dict[str, Any]:
        customer = await self.customer_repository.get_by_id(customer_id)
        if not customer:
            return {}
        return {
            "name": customer.full_name,
            "email": customer.email,
            "phone": customer.phone,
            "skin_type": customer.skin_type,
            "skin_concerns": customer.skin_concerns or [],
            "status": customer.status,
        }
