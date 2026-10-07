# pyrefly: ignore [missing-import]
from fastapi import APIRouter

from app.api.public.checkout import router as checkout_router

router = APIRouter()

router.include_router(checkout_router, prefix="/checkout", tags=["checkout"])
