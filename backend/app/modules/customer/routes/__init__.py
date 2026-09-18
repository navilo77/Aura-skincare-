from fastapi import APIRouter

from app.modules.customer.routes.customer import router as customer_router

router = APIRouter()

router.include_router(customer_router, prefix="/customers", tags=["customers"])
