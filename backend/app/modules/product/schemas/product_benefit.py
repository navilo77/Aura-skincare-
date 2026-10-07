import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductBenefitBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    benefit_id: uuid.UUID


class ProductBenefitCreate(ProductBenefitBase):
    pass


class ProductBenefitRead(ProductBenefitBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
