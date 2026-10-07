from typing import Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.marketing_ai.schemas.marketing import (
    MarketingAILogRead,
    MarketingAssetCreate,
    MarketingAssetRead,
    MarketingCampaignCreate,
    MarketingCampaignRead,
    MarketingContentCreate,
    MarketingContentRead,
    MarketingHistoryRead,
    MarketingTemplateCreate,
    MarketingTemplateRead,
)
from app.modules.marketing_ai.services.marketing import (
    MarketingAILogService,
    MarketingAssetService,
    MarketingCampaignService,
    MarketingContentService,
    MarketingHistoryService,
    MarketingTemplateService,
)
from app.shared.database.session import get_db

router = APIRouter()


@router.post(
    "/campaigns",
    response_model=MarketingCampaignRead,
    status_code=status.HTTP_201_CREATED,
    tags=["marketing"],
)
async def create_campaign(
    payload: MarketingCampaignCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = MarketingCampaignService(db)
    return await service.create(**payload.model_dump())


@router.get(
    "/campaigns", response_model=list[MarketingCampaignRead], tags=["marketing"]
)
async def list_campaigns(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = MarketingCampaignService(db)
    campaigns, _ = await service.get_list(skip=skip, limit=limit)
    return campaigns


@router.post(
    "/templates",
    response_model=MarketingTemplateRead,
    status_code=status.HTTP_201_CREATED,
    tags=["marketing"],
)
async def create_template(
    payload: MarketingTemplateCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = MarketingTemplateService(db)
    return await service.create(**payload.model_dump())


@router.get(
    "/templates", response_model=list[MarketingTemplateRead], tags=["marketing"]
)
async def list_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = MarketingTemplateService(db)
    templates, _ = await service.repository.get_list(skip=skip, limit=limit)
    return templates


@router.post(
    "/contents",
    response_model=MarketingContentRead,
    status_code=status.HTTP_201_CREATED,
    tags=["marketing"],
)
async def create_content(
    payload: MarketingContentCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = MarketingContentService(db)
    return await service.create(**payload.model_dump())


@router.get("/contents", response_model=list[MarketingContentRead], tags=["marketing"])
async def list_contents(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = MarketingContentService(db)
    contents, _ = await service.get_list(skip=skip, limit=limit)
    return contents


@router.post(
    "/assets",
    response_model=MarketingAssetRead,
    status_code=status.HTTP_201_CREATED,
    tags=["marketing"],
)
async def create_asset(
    payload: MarketingAssetCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    service = MarketingAssetService(db)
    return await service.create(**payload.model_dump())


@router.get("/history", response_model=list[MarketingHistoryRead], tags=["marketing"])
async def list_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = MarketingHistoryService(db)
    history, _ = await service.repository.get_list(skip=skip, limit=limit)
    return history


@router.get("/logs", response_model=list[MarketingAILogRead], tags=["marketing"])
async def list_ai_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = MarketingAILogService(db)
    logs, _ = await service.repository.get_list(skip=skip, limit=limit)
    return logs
