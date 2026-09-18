import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import Warehouse
from app.modules.inventory.repositories.warehouse import WarehouseRepository


class WarehouseService:
    def __init__(self, session: AsyncSession):
        self.repository = WarehouseRepository(session)

    async def create(
        self,
        name: str,
        code: str,
        location: str | None = None,
        is_active: bool = True,
    ) -> Warehouse:
        code = code.upper()
        if await self.repository.exists_by_code(code):
            raise ValueError("Warehouse code already exists")

        warehouse = Warehouse(
            name=name,
            code=code,
            location=location,
            is_active=is_active,
        )
        return await self.repository.create(warehouse)

    async def update(
        self,
        warehouse_id: uuid.UUID,
        name: str | None = None,
        code: str | None = None,
        location: str | None = None,
        is_active: bool | None = None,
    ) -> Warehouse:
        warehouse = await self.repository.get_by_id(warehouse_id)
        if not warehouse:
            raise ValueError("Warehouse not found")

        if code is not None:
            code = code.upper()
            if await self.repository.exists_by_code_excluding_id(code, warehouse_id):
                raise ValueError("Warehouse code already exists")
            warehouse.code = code

        if name is not None:
            warehouse.name = name
        if location is not None:
            warehouse.location = location
        if is_active is not None:
            warehouse.is_active = is_active

        return await self.repository.update(warehouse)

    async def delete(self, warehouse_id: uuid.UUID) -> None:
        warehouse = await self.repository.get_by_id(warehouse_id)
        if not warehouse:
            raise ValueError("Warehouse not found")
        await self.repository.delete(warehouse_id)

    async def get_by_id(self, warehouse_id: uuid.UUID) -> Warehouse | None:
        return await self.repository.get_by_id(warehouse_id)

    async def get_list(
        self, skip: int = 0, limit: int = 20, search: str | None = None
    ) -> tuple[list[Warehouse], int]:
        query = await self.repository._build_query(
            search=search,
            search_fields=["name", "code"],
        )
        query = query.order_by(Warehouse.name)
        paginated_query, total = await self.repository._apply_pagination(
            query, skip, limit
        )
        result = await self.repository.session.execute(paginated_query)
        return list(result.scalars().all()), total
