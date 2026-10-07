from enum import StrEnum

from fastapi import Depends, HTTPException, status

from app.api.dependencies.auth import get_current_user
from app.modules.auth.models.user import User


class Permission(StrEnum):
    # User management
    USER_READ = "user:read"
    USER_WRITE = "user:write"
    USER_DELETE = "user:delete"

    # Product management
    PRODUCT_READ = "product:read"
    PRODUCT_WRITE = "product:write"
    PRODUCT_DELETE = "product:delete"

    # Order management
    ORDER_READ = "order:read"
    ORDER_WRITE = "order:write"
    ORDER_DELETE = "order:delete"
    ORDER_REFUND = "order:refund"

    # Inventory management
    INVENTORY_READ = "inventory:read"
    INVENTORY_WRITE = "inventory:write"
    INVENTORY_DELETE = "inventory:delete"

    # Customer management
    CUSTOMER_READ = "customer:read"
    CUSTOMER_WRITE = "customer:write"
    CUSTOMER_DELETE = "customer:delete"

    # Admin settings
    SETTINGS_READ = "settings:read"
    SETTINGS_WRITE = "settings:write"

    # Analytics
    ANALYTICS_READ = "analytics:read"

    # Marketing
    MARKETING_READ = "marketing:read"
    MARKETING_WRITE = "marketing:write"

    # System
    SYSTEM_ADMIN = "system:admin"


ROLE_PERMISSIONS = {
    "customer": [
        Permission.USER_READ,  # own profile only
    ],
    "support": [
        Permission.USER_READ,
        Permission.ORDER_READ,
        Permission.CUSTOMER_READ,
        Permission.PRODUCT_READ,
    ],
    "marketing": [
        Permission.PRODUCT_READ,
        Permission.CUSTOMER_READ,
        Permission.MARKETING_READ,
        Permission.MARKETING_WRITE,
        Permission.ANALYTICS_READ,
    ],
    "admin": [
        Permission.USER_READ,
        Permission.USER_WRITE,
        Permission.USER_DELETE,
        Permission.PRODUCT_READ,
        Permission.PRODUCT_WRITE,
        Permission.PRODUCT_DELETE,
        Permission.ORDER_READ,
        Permission.ORDER_WRITE,
        Permission.ORDER_DELETE,
        Permission.ORDER_REFUND,
        Permission.INVENTORY_READ,
        Permission.INVENTORY_WRITE,
        Permission.INVENTORY_DELETE,
        Permission.CUSTOMER_READ,
        Permission.CUSTOMER_WRITE,
        Permission.CUSTOMER_DELETE,
        Permission.SETTINGS_READ,
        Permission.SETTINGS_WRITE,
        Permission.ANALYTICS_READ,
        Permission.MARKETING_READ,
        Permission.MARKETING_WRITE,
    ],
    "system_administrator": [p for p in Permission],
}


def get_user_permissions(role: str) -> list[Permission]:
    return ROLE_PERMISSIONS.get(role, [])


def has_permission(role: str, permission: Permission) -> bool:
    return permission in get_user_permissions(role)


def require_permission(permission: Permission):
    async def permission_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if not has_permission(current_user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {permission.value} required",
            )
        return current_user

    return permission_checker


def require_any_permission(*permissions: Permission):
    async def permission_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        user_perms = get_user_permissions(current_user.role)
        if not any(p in user_perms for p in permissions):
            required = [p.value for p in permissions]
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: one of {required} required",
            )
        return current_user

    return permission_checker


def require_all_permissions(*permissions: Permission):
    async def permission_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        user_perms = get_user_permissions(current_user.role)
        if not all(p in user_perms for p in permissions):
            required = [p.value for p in permissions]
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: all of {required} required",
            )
        return current_user

    return permission_checker
