import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.repositories.category import CategoryRepository
from app.modules.product.schemas.category import (
    CategoryCreate,
    CategoryRead,
    CategoryTree,
    CategoryUpdate,
)
from app.modules.product.services.category import CategoryService
from app.shared.database.session import get_db

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryRead])
async def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    parent_id: uuid.UUID | None = Query(None),
    is_active: bool | None = Query(None),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = CategoryService(db)
    categories, _ = await service.get_list(
        skip=skip,
        limit=limit,
        parent_id=parent_id,
        is_active=is_active,
        search=search,
    )
    return categories


@router.get("/tree", response_model=list[CategoryTree])
async def get_category_tree(db: AsyncSession = Depends(get_db)) -> Any:
    repo = CategoryRepository(db)
    all_categories = await repo.get_all_with_children()
    category_map = {str(c.id): CategoryTree.model_validate(c) for c in all_categories}
    for tree in category_map.values():
        tree.children = []
    roots = []
    for category in all_categories:
        tree = category_map[str(category.id)]
        if category.parent_id is None:
            roots.append(tree)
        else:
            parent = category_map.get(str(category.parent_id))
            if parent:
                parent.children.append(tree)
    return roots


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Any:
    service = CategoryService(db)
    category = await service.get_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: CategoryCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = CategoryService(db)
    try:
        category = await service.create(
            name=payload.name,
            slug=payload.slug,
            parent_id=payload.parent_id,
            description=payload.description,
            image_url=payload.image_url,
            sort_order=payload.sort_order,
        )
        return category
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.patch("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: uuid.UUID,
    payload: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = CategoryService(db)
    try:
        category = await service.update(
            category_id=category_id,
            name=payload.name,
            slug=payload.slug,
            parent_id=payload.parent_id,
            description=payload.description,
            image_url=payload.image_url,
            sort_order=payload.sort_order,
            is_active=payload.is_active,
        )
        return category
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/{category_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_category(
    category_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Any:
    service = CategoryService(db)
    try:
        await service.delete(category_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
