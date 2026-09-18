from app.modules.analytics.routes.analytics import router as analytics_router
from app.modules.analytics.routes.event import router as event_router

__all__ = [
    "analytics_router",
    "event_router",
]
