from typing import Any

from app.modules.customer.repositories.customer import CustomerRepository
from app.modules.product.repositories.brand import BrandRepository
from app.modules.product.repositories.product import ProductRepository


class PreferenceMemory:
    def __init__(
        self,
        customer_repository: CustomerRepository,
        product_repository: ProductRepository,
        brand_repository: BrandRepository,
    ) -> None:
        self.customer_repository = customer_repository
        self.product_repository = product_repository
        self.brand_repository = brand_repository

    async def get_preferences(
        self,
        customer,
        purchase_history: list[dict[str, Any]],
    ) -> dict[str, Any]:
        favorite_brands: list[str] = []
        product_names: list[str] = []
        for order in purchase_history:
            for item in order.get("items", []):
                product_names.append(item.get("product_name", ""))

        if product_names:
            products = await self.product_repository.get_list_by_filters(
                {"name": product_names[0]}
            )
            if not products:
                favorite_brands = self._infer_brands_from_names(product_names)
            else:
                brand_ids = [p.brand_id for p in products if hasattr(p, "brand_id")]
                for brand_id in brand_ids:
                    brand = await self.brand_repository.get_by_id(brand_id)
                    if brand and brand.name not in favorite_brands:
                        favorite_brands.append(brand.name)

        budget = self._infer_budget(purchase_history)

        return {
            "language": "bangla",
            "favorite_brands": favorite_brands[:5],
            "budget": budget,
            "routine": self._infer_routine(customer, purchase_history),
            "avoid_ingredients": self._infer_avoid_ingredients(customer),
        }

    def _infer_brands_from_names(self, product_names: list[str]) -> list[str]:
        brands: list[str] = []
        for name in product_names:
            parts = name.split()
            if parts:
                candidate = parts[0]
                if candidate not in brands:
                    brands.append(candidate)
        return brands[:5]

    def _infer_budget(self, purchase_history: list[dict[str, Any]]) -> str:
        totals = [
            order.get("total_amount", 0)
            for order in purchase_history
            if order.get("total_amount")
        ]
        if not totals:
            return "medium"
        average = sum(totals) / len(totals)
        if average < 500:
            return "budget"
        if average < 1500:
            return "medium"
        return "premium"

    def _infer_routine(self, customer, purchase_history: list[dict[str, Any]]) -> str:
        skin_type = getattr(customer, "skin_type", None)
        routine_parts: list[str] = []
        if skin_type:
            routine_parts.append(skin_type)
        for order in purchase_history:
            for item in order.get("items", []):
                name = item.get("product_name", "").lower()
                if "cleanser" in name and "Cleanser" not in routine_parts:
                    routine_parts.append("Cleanser")
                if "moisturizer" in name and "Moisturizer" not in routine_parts:
                    routine_parts.append("Moisturizer")
                if "sunscreen" in name and "Sunscreen" not in routine_parts:
                    routine_parts.append("Sunscreen")
                if "serum" in name and "Serum" not in routine_parts:
                    routine_parts.append("Serum")
        return ", ".join(routine_parts[:5]) if routine_parts else "basic"

    def _infer_avoid_ingredients(self, customer) -> list[str]:
        concerns = getattr(customer, "skin_concerns", None) or []
        mapping = {
            "acne": ["oil", "comedogenic"],
            "sensitive": ["fragrance", "alcohol"],
            "dry": ["alcohol", "strong-fragrance"],
            "oily": ["heavy-oils"],
        }
        avoid: list[str] = []
        for concern in concerns:
            ingredients = mapping.get(concern.lower(), [])
            for ingredient in ingredients:
                if ingredient not in avoid:
                    avoid.append(ingredient)
        return avoid
