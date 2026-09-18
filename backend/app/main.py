import asyncio
import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router
from app.config.settings import settings

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("uvicorn")

app = FastAPI(
    title="Aura Skincare API",
    description="Aura Skincare backend API",
    version="0.1.0",
    contact={"name": "Aura Skincare", "email": "support@auraskincare.com"},
    license_info={"name": "Proprietary"},
    terms_of_service="https://auraskincare.com/terms",
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

app.include_router(router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "Aura Backend"}
