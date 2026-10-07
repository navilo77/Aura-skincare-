from collections.abc import Callable
from enum import StrEnum

from fastapi import HTTPException, status

from app.modules.auth.models.user import User


class Permission(StrEnum):
    VIEW_OWN_PROFILE = "view_own_profile"
    UPDATE_OWN_PROFILE = "update_own_profile"
    VIEW_OWN_ORDERS = "view_own_orders"
    MANAGE_OWN_CART = "manage_own_cart"
    RECEIVE_AI_RECOMMENDATIONS = "receive_ai_recommendations"
    VIEW_CUSTOMER_INFO = "view_customer_info"
    VIEW_ORDERS = "view_orders"
    HANDLE_SUPPORT_REQUESTS = "handle_support_requests"
    MANAGE_CAMPAIGNS = "manage_campaigns"
    CREATE_MARKETING_CONTENT = "create_marketing_content"
    VIEW_CAMPAIGN_ANALYTICS = "view_campaign_analytics"
    MANAGE_PRODUCTS = "manage_products"
    MANAGE_ORDERS = "manage_orders"
    MANAGE_USERS = "manage_users"
    VIEW_REPORTS = "view_reports"
    MANAGE_PROMOTIONS = "manage_promotions"
    FULL_ADMINISTRATION = "full_administration"
    SECURITY_CONFIGURATION = "security_configuration"
    USER_ROLE_MANAGEMENT = "user_role_management"
    INFRASTRUCTURE_CONFIGURATION = "infrastructure_configuration"
    ACCESS_APPROVED_APIS = "access_approved_apis"
    READ_BUSINESS_KNOWLEDGE = "read_business_knowledge"
    EXECUTE_APPROVED_WORKFLOWS = "execute_approved_workflows"


ROLE_PERMISSIONS: dict[str, list[Permission]] = {
    "customer": [
        Permission.VIEW_OWN_PROFILE,
        Permission.UPDATE_OWN_PROFILE,
        Permission.VIEW_OWN_ORDERS,
        Permission.MANAGE_OWN_CART,
        Permission.RECEIVE_AI_RECOMMENDATIONS,
    ],
    "support": [
        Permission.VIEW_CUSTOMER_INFO,
        Permission.VIEW_ORDERS,
        Permission.HANDLE_SUPPORT_REQUESTS,
    ],
    "marketing": [
        Permission.MANAGE_CAMPAIGNS,
        Permission.CREATE_MARKETING_CONTENT,
        Permission.VIEW_CAMPAIGN_ANALYTICS,
    ],
    "admin": [
        Permission.MANAGE_PRODUCTS,
        Permission.MANAGE_ORDERS,
        Permission.MANAGE_USERS,
        Permission.VIEW_REPORTS,
        Permission.MANAGE_PROMOTIONS,
    ],
    "system_administrator": [
        Permission.FULL_ADMINISTRATION,
        Permission.SECURITY_CONFIGURATION,
        Permission.USER_ROLE_MANAGEMENT,
        Permission.INFRASTRUCTURE_CONFIGURATION,
    ],
    "ai_agent": [
        Permission.ACCESS_APPROVED_APIS,
        Permission.READ_BUSINESS_KNOWLEDGE,
        Permission.EXECUTE_APPROVED_WORKFLOWS,
    ],
}


def has_permission(user: User, permission: Permission) -> bool:
    return permission in ROLE_PERMISSIONS.get(user.role, [])


def require_permission(permission: Permission) -> Callable[[User], User]:
    def dependency(current_user: User) -> User:
        if not has_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission.value}' required",
            )
        return current_user

    return dependency


def require_role(allowed_roles: list[str]) -> Callable[[User], User]:
    def dependency(current_user: User) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role privileges",
            )
        return current_user

    return dependency


def require_any_role(allowed_roles: list[str]) -> Callable[[User], User]:
    def dependency(current_user: User) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role privileges",
            )
        return current_user

    return dependency
