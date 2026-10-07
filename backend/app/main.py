import asyncio
import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status as http_status

from app.api.middleware.audit_log import AuditLogMiddleware
from app.api.router import router
from app.config.settings import settings
from app.integrations.redis import redis_client

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_client.connect()
    try:
        yield
    finally:
        await redis_client.disconnect()


app = FastAPI(
    title="Aura Skincare API",
    description="Aura Skincare backend API",
    version="1.0.1",
    contact={"name": "Aura Skincare", "email": "support@auraskincare.com"},
    license_info={"name": "Proprietary"},
    terms_of_service="https://auraskincare.com/terms",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuditLogMiddleware)

app.include_router(router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "Aura Backend"}


@app.get("/health/ready")
async def readiness_check() -> dict[str, str]:
    try:
        if not await redis_client.ping():
            raise HTTPException(
                status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Redis is unavailable",
            )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Redis is unavailable: {exc}",
        )
    return {"status": "ok", "redis": "connected"}
