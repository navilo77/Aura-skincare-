from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SortField(StrEnum):
    NAME = "name"
    SLUG = "slug"
    PRICE = "price"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    RATING = "rating"
    BEST_SELLING = "best_selling"


class AvailabilityStatus(StrEnum):
    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"
    PREORDER = "preorder"


class ProductSearchFilter(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    search: str | None = Field(None, description="Search query")
    status: str | None = Field(None, description="Product status")
    product_type: str | None = Field(None, description="Product type")
    is_active: bool | None = Field(None, description="Whether product is active")
    is_featured: bool | None = Field(None, description="Whether product is featured")

    category_slug: str | None = Field(None, description="Category slug")
    brand_slug: str | None = Field(None, description="Brand slug")
    skin_type_slug: str | None = Field(None, description="Skin type slug")
    concern_slug: str | None = Field(None, description="Skin concern slug")
    ingredient_slug: str | None = Field(None, description="Ingredient slug")
    benefit_slug: str | None = Field(None, description="Benefit slug")
    tag_slug: str | None = Field(None, description="Product tag slug")
    routine_slug: str | None = Field(None, description="Routine type slug")

    price_min: Decimal | None = Field(None, ge=0, description="Minimum price")
    price_max: Decimal | None = Field(None, ge=0, description="Maximum price")
    rating: float | None = Field(None, ge=0, le=5, description="Minimum rating")
    availability: AvailabilityStatus | None = Field(
        None,
        description="Stock availability",
    )
    sort: SortField = Field(
        SortField.CREATED_AT,
        description="Sort field",
    )
    sort_order: str | None = Field(
        "desc",
        pattern="^(asc|desc)$",
        description="Sort direction",
    )
    page: int | None = Field(1, ge=1, description="Page number")
    limit: int | None = Field(20, ge=1, le=100, description="Items per page")

    @field_validator("price_max")
    @classmethod
    def price_range_valid(cls, v: Decimal | None, info: any) -> Decimal | None:
        price_min = info.data.get("price_min")
        if v is not None and price_min is not None:
            if v < price_min:
                raise ValueError("price_max must be greater than or equal to price_min")
        return v
