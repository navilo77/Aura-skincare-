import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.models import (
    Inventory,
    ProductSupplier,
    Supplier,
    Warehouse,
)
from app.modules.inventory.repositories.inventory import InventoryRepository
from app.modules.inventory.repositories.product_supplier import (
    ProductSupplierRepository,
)
from app.modules.inventory.repositories.supplier import SupplierRepository
from app.modules.inventory.repositories.warehouse import WarehouseRepository


class MockProduct:
    id: uuid.UUID


@pytest.mark.asyncio
async def test_warehouse_repository_crud(db_session: AsyncSession):
    repo = WarehouseRepository(db_session)
    warehouse = Warehouse(name="Main Warehouse", code="WH-001", location="New York")
    db_session.add(warehouse)
    await db_session.flush()

    fetched = await repo.get_by_id(warehouse.id)
    assert fetched is not None
    assert fetched.name == "Main Warehouse"
    assert fetched.code == "WH-001"

    assert await repo.exists_by_code("WH-001") is True
    assert await repo.exists_by_code("nonexistent") is False

    await repo.delete(warehouse.id)
    assert await repo.get_by_id(warehouse.id) is None


@pytest.mark.asyncio
async def test_warehouse_repository_duplicate_code(db_session: AsyncSession):
    repo = WarehouseRepository(db_session)
    warehouse = Warehouse(name="Warehouse A", code="WH-A")
    db_session.add(warehouse)
    await db_session.flush()

    assert await repo.exists_by_code("WH-A") is True
    assert await repo.exists_by_code_excluding_id("WH-A", uuid.uuid4()) is True
    assert await repo.exists_by_code_excluding_id("WH-A", warehouse.id) is False


@pytest.mark.asyncio
async def test_inventory_repository_crud(db_session: AsyncSession):
    warehouse = Warehouse(name="Warehouse", code="WH-1")
    db_session.add(warehouse)
    await db_session.flush()

    product = MockProduct()
    product.id = uuid.uuid4()

    repo = InventoryRepository(db_session)
    inventory = Inventory(
        product_id=product.id,
        warehouse_id=warehouse.id,
        quantity_on_hand=100,
        quantity_reserved=10,
    )
    db_session.add(inventory)
    await db_session.flush()

    fetched = await repo.get_by_id(inventory.id)
    assert fetched is not None
    assert fetched.quantity_on_hand == 100

    by_product = await repo.get_by_product(product.id)
    assert by_product is not None
    assert by_product.id == inventory.id

    await repo.delete(inventory.id)
    assert await repo.get_by_id(inventory.id) is None


@pytest.mark.asyncio
async def test_supplier_repository_crud(db_session: AsyncSession):
    repo = SupplierRepository(db_session)
    supplier = Supplier(name="Acme Supplies", contact_email="contact@acme.com")
    db_session.add(supplier)
    await db_session.flush()

    fetched = await repo.get_by_id(supplier.id)
    assert fetched is not None
    assert fetched.name == "Acme Supplies"

    assert await repo.exists_by_name("Acme Supplies") is True

    await repo.delete(supplier.id)
    assert await repo.get_by_id(supplier.id) is None


@pytest.mark.asyncio
async def test_product_supplier_repository_crud(db_session: AsyncSession):
    warehouse = Warehouse(name="Warehouse", code="WH-1")
    db_session.add(warehouse)
    await db_session.flush()

    product = MockProduct()
    product.id = uuid.uuid4()

    inventory = Inventory(product_id=product.id, warehouse_id=warehouse.id)
    db_session.add(inventory)
    await db_session.flush()

    supplier = Supplier(name="Supplier A")
    db_session.add(supplier)
    await db_session.flush()

    repo = ProductSupplierRepository(db_session)
    link = ProductSupplier(
        product_id=product.id,
        supplier_id=supplier.id,
        cost_price=10.00,
    )
    db_session.add(link)
    await db_session.flush()

    fetched = await repo.get_by_id(link.id)
    assert fetched is not None

    assert await repo.exists_by_product_and_supplier(product.id, supplier.id) is True

    by_product = await repo.get_by_product(product.id)
    assert len(by_product) == 1

    by_supplier = await repo.get_by_supplier(supplier.id)
    assert len(by_supplier) == 1

    await repo.delete(link.id)
    assert await repo.get_by_id(link.id) is None
