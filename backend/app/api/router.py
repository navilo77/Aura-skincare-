from fastapi import APIRouter

from app.api.public import router as public_router
from app.api.v1 import router as v1_router

router = APIRouter()

router.include_router(v1_router, prefix="/api/v1")
router.include_router(public_router, prefix="/public/v1")
