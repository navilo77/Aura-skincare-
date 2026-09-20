import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.modules.admin.schemas.activity_log import ActivityLogRead
from app.modules.admin.schemas.audit_log import AuditLogRead
from app.modules.admin.schemas.banner import BannerCreate, BannerRead, BannerUpdate
from app.modules.admin.schemas.coupon import CouponCreate, CouponRead, CouponUpdate
from app.modules.admin.services.activity_log import ActivityLogService
from app.modules.admin.services.audit_log import AuditLogService
from app.modules.admin.services.banner import BannerService
from app.modules.admin.services.coupon import CouponService
from app.modules.auth.models.user import User
from app.shared.database.session import get_db

router = APIRouter()


def admin_required(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in ("admin", "system_administrator"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


@router.get("/dashboard", tags=["admin"])
async def admin_dashboard(
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    from app.modules.inventory.services.inventory import InventoryService
    from app.modules.order.repositories.order import OrderRepository

    order_repository = OrderRepository(db)
    orders, _ = order_repository.get_list(skip=0, limit=1000)

    total_orders = len(orders)
    total_revenue = sum(float(order.total_amount) for order in orders)
    pending_orders = sum(1 for order in orders if order.status == "pending")

    inventory_service = InventoryService(db)
    low_stock = await inventory_service.get_low_stock_items()

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "pending_orders": pending_orders,
        "low_stock_count": len(low_stock),
    }


@router.get("/coupons", response_model=list[CouponRead], tags=["admin"])
async def list_coupons(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = CouponService(db)
    coupons, _ = await service.get_list(skip=skip, limit=limit)
    return coupons


@router.post(
    "/coupons",
    response_model=CouponRead,
    status_code=status.HTTP_201_CREATED,
    tags=["admin"],
)
async def create_coupon(
    payload: CouponCreate,
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = CouponService(db)
    try:
        coupon = await service.create(**payload.model_dump())
        return coupon
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/coupons/{coupon_id}", response_model=CouponRead, tags=["admin"])
async def get_coupon(
    coupon_id: uuid.UUID,
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = CouponService(db)
    coupon = await service.get_by_id(coupon_id)
    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found"
        )
    return coupon


@router.patch("/coupons/{coupon_id}", response_model=CouponRead, tags=["admin"])
async def update_coupon(
    coupon_id: uuid.UUID,
    payload: CouponUpdate,
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = CouponService(db)
    try:
        coupon = await service.update(
            coupon_id, **payload.model_dump(exclude_none=True)
        )
        return coupon
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete(
    "/coupons/{coupon_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["admin"],
)
async def delete_coupon(
    coupon_id: uuid.UUID,
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
) -> None:
    service = CouponService(db)
    try:
        await service.delete(coupon_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.get("/banners", response_model=list[BannerRead], tags=["admin"])
async def list_banners(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = BannerService(db)
    banners, _ = await service.get_list(skip=skip, limit=limit)
    return banners


@router.post(
    "/banners",
    response_model=BannerRead,
    status_code=status.HTTP_201_CREATED,
    tags=["admin"],
)
async def create_banner(
    payload: BannerCreate,
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = BannerService(db)
    try:
        banner = await service.create(**payload.model_dump())
        return banner
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc


@router.get("/banners/{banner_id}", response_model=BannerRead, tags=["admin"])
async def get_banner(
    banner_id: uuid.UUID,
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = BannerService(db)
    banner = await service.get_by_id(banner_id)
    if not banner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Banner not found"
        )
    return banner


@router.patch("/banners/{banner_id}", response_model=BannerRead, tags=["admin"])
async def update_banner(
    banner_id: uuid.UUID,
    payload: BannerUpdate,
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = BannerService(db)
    try:
        banner = await service.update(
            banner_id, **payload.model_dump(exclude_none=True)
        )
        return banner
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.delete(
    "/banners/{banner_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["admin"],
)
async def delete_banner(
    banner_id: uuid.UUID,
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
) -> None:
    service = BannerService(db)
    try:
        await service.delete(banner_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@router.get("/audit-logs", response_model=list[AuditLogRead], tags=["admin"])
async def list_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_id: uuid.UUID | None = Query(None),
    entity_type: str | None = Query(None),
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = AuditLogService(db)
    logs, _ = await service.get_list(
        skip=skip, limit=limit, user_id=user_id, entity_type=entity_type
    )
    return logs


@router.get("/activity-logs", response_model=list[ActivityLogRead], tags=["admin"])
async def list_activity_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_id: uuid.UUID | None = Query(None),
    action: str | None = Query(None),
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = ActivityLogService(db)
    logs, _ = await service.get_list(
        skip=skip, limit=limit, user_id=user_id, action=action
    )
    return logs


@router.get("/settings", tags=["admin"])
async def list_admin_settings(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
) -> Any:
    from app.modules.admin.services.admin_settings import AdminSettingsService

    service = AdminSettingsService(db)
    settings, _ = await service.get_list(skip=skip, limit=limit)
    return settings


@router.patch("/settings/{key}", tags=["admin"])
async def update_admin_setting(
    key: str,
    payload: dict[str, str],
    current_user: User = Depends(admin_required),
    db: AsyncSession = Depends(get_db),
) -> Any:
    from app.modules.admin.services.admin_settings import AdminSettingsService

    service = AdminSettingsService(db)
    try:
        setting = await service.update(key, payload["value"])
        return setting
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
