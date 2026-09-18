import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.inventory.services.adjustment import AdjustmentService
from app.modules.inventory.services.inventory import InventoryService
from app.modules.inventory.services.movement import MovementService
from app.modules.inventory.services.supplier import SupplierService
from app.modules.inventory.services.warehouse import WarehouseService


class MockProduct:
    id: uuid.UUID


@pytest.mark.asyncio
async def test_warehouse_service_crud(db_session: AsyncSession):
    service = WarehouseService(db_session)
    warehouse = await service.create(
        name="Main Warehouse",
        code="WH-001",
        location="New York",
    )
    assert warehouse.id is not None
    assert warehouse.code == "WH-001"

    fetched = await service.get_by_id(warehouse.id)
    assert fetched is not None

    warehouses, total = await service.get_list()
    assert total == 1

    updated = await service.update(warehouse_id=warehouse.id, name="Updated Warehouse")
    assert updated.name == "Updated Warehouse"

    await service.delete(warehouse.id)
    assert await service.get_by_id(warehouse.id) is None


@pytest.mark.asyncio
async def test_warehouse_service_duplicate_code(db_session: AsyncSession):
    service = WarehouseService(db_session)
    await service.create(name="Warehouse A", code="WH-A")

    with pytest.raises(ValueError) as exc:
        await service.create(name="Warehouse B", code="WH-A")
    assert "code already exists" in str(exc.value)


@pytest.mark.asyncio
async def test_inventory_service_crud(db_session: AsyncSession):
    warehouse_service = WarehouseService(db_session)
    inventory_service = InventoryService(db_session)

    warehouse = await warehouse_service.create(name="Warehouse", code="WH-1")

    product = MockProduct()
    product.id = uuid.uuid4()

    inventory = await inventory_service.create(
        product_id=product.id,
        warehouse_id=warehouse.id,
        quantity_on_hand=100,
        quantity_reserved=10,
    )
    assert inventory.id is not None
    assert inventory.quantity_on_hand == 100

    fetched = await inventory_service.get_by_product(product.id)
    assert fetched is not None

    inventories, total = await inventory_service.get_list()
    assert total == 1

    updated = await inventory_service.update(
        product_id=product.id, low_stock_threshold=5
    )
    assert updated.low_stock_threshold == 5

    await inventory_service.delete(product.id)
    assert await inventory_service.get_by_product(product.id) is None


@pytest.mark.asyncio
async def test_inventory_service_duplicate_product(db_session: AsyncSession):
    warehouse_service = WarehouseService(db_session)
    inventory_service = InventoryService(db_session)

    warehouse = await warehouse_service.create(name="Warehouse", code="WH-1")

    product = MockProduct()
    product.id = uuid.uuid4()

    await inventory_service.create(product_id=product.id, warehouse_id=warehouse.id)

    with pytest.raises(ValueError) as exc:
        await inventory_service.create(product_id=product.id, warehouse_id=warehouse.id)
    assert "Inventory record already exists" in str(exc.value)


@pytest.mark.asyncio
async def test_supplier_service_crud(db_session: AsyncSession):
    service = SupplierService(db_session)
    supplier = await service.create(
        name="Acme Supplies",
        contact_email="contact@acme.com",
    )
    assert supplier.id is not None
    assert supplier.name == "Acme Supplies"

    fetched = await service.get_by_id(supplier.id)
    assert fetched is not None

    suppliers, total = await service.get_list()
    assert total == 1

    updated = await service.update(supplier_id=supplier.id, name="Acme Corp")
    assert updated.name == "Acme Corp"

    await service.delete(supplier.id)
    assert await service.get_by_id(supplier.id) is None


@pytest.mark.asyncio
async def test_movement_service_quantity_sign(db_session: AsyncSession):
    warehouse_service = WarehouseService(db_session)
    inventory_service = InventoryService(db_session)
    movement_service = MovementService(db_session)

    warehouse = await warehouse_service.create(name="Warehouse", code="WH-1")

    product = MockProduct()
    product.id = uuid.uuid4()

    inventory = await inventory_service.create(
        product_id=product.id,
        warehouse_id=warehouse.id,
        quantity_on_hand=100,
        quantity_reserved=10,
    )

    movement = await movement_service.create(
        inventory_id=inventory.id,
        movement_type="purchase",
        quantity=50,
    )
    assert movement.quantity == 50

    with pytest.raises(ValueError) as exc:
        await movement_service.create(
            inventory_id=inventory.id,
            movement_type="sale",
            quantity=10,
        )
    assert "quantity must be negative" in str(exc.value)


@pytest.mark.asyncio
async def test_adjustment_service_approval(db_session: AsyncSession):
    warehouse_service = WarehouseService(db_session)
    inventory_service = InventoryService(db_session)
    adjustment_service = AdjustmentService(db_session)

    warehouse = await warehouse_service.create(name="Warehouse", code="WH-1")

    product = MockProduct()
    product.id = uuid.uuid4()

    inventory = await inventory_service.create(
        product_id=product.id,
        warehouse_id=warehouse.id,
        quantity_on_hand=100,
        quantity_reserved=10,
    )

    adjustment = await adjustment_service.create(
        inventory_id=inventory.id,
        adjustment_type="correction",
        quantity_change=5,
        reason="Count correction",
    )
    assert adjustment.is_approved is False

    approved = await adjustment_service.approve(
        adjustment_id=adjustment.id,
        approved=True,
        approved_by=uuid.uuid4(),
    )
    assert approved.is_approved is True
