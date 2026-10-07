from app.modules.product.repositories.benefit import BenefitRepository
from app.modules.product.repositories.brand import BrandRepository
from app.modules.product.repositories.category import CategoryRepository
from app.modules.product.repositories.ingredient import IngredientRepository
from app.modules.product.repositories.product import ProductRepository
from app.modules.product.repositories.product_benefit import ProductBenefitRepository
from app.modules.product.repositories.product_image import ProductImageRepository
from app.modules.product.repositories.product_ingredient import (
    ProductIngredientRepository,
)
from app.modules.product.repositories.product_routine import ProductRoutineRepository
from app.modules.product.repositories.product_skin_concern import (
    ProductSkinConcernRepository,
)
from app.modules.product.repositories.product_skin_type import ProductSkinTypeRepository
from app.modules.product.repositories.product_tag import ProductTagRepository
from app.modules.product.repositories.product_variant import ProductVariantRepository
from app.modules.product.repositories.routine_type import RoutineTypeRepository
from app.modules.product.repositories.skin_concern import SkinConcernRepository
from app.modules.product.repositories.skin_type import SkinTypeRepository
from app.modules.product.repositories.tag import TagRepository

__all__ = [
    "BenefitRepository",
    "BrandRepository",
    "CategoryRepository",
    "IngredientRepository",
    "ProductBenefitRepository",
    "ProductImageRepository",
    "ProductIngredientRepository",
    "ProductRepository",
    "ProductRoutineRepository",
    "ProductSkinConcernRepository",
    "ProductSkinTypeRepository",
    "ProductTagRepository",
    "ProductVariantRepository",
    "RoutineTypeRepository",
    "SkinConcernRepository",
    "SkinTypeRepository",
    "TagRepository",
]
