import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_db
from app.schemas import (
    CommodityProfileSchema,
    HighImpactNewsSchema,
    LatestNewsSchema,
    PaginatedResponse,
    TradeSummarySchema,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/commodities", tags=["Commodities"])


@router.get(
    "/profiles",
    response_model=PaginatedResponse[CommodityProfileSchema],
    summary="List all commodity profiles",
    description="Returns all commodity profiles from the `vw_commodity_profile` view, ordered by name. Each profile includes definition, uses, major producers, trade record count, and news count.",
)
async def list_profiles(db: AsyncSession = Depends(get_db)):
    total, rows = await crud.get_commodity_profiles(db)
    return {"total_count": total, "items": [CommodityProfileSchema.model_validate(r) for r in rows]}


@router.get(
    "/profiles/{profile_id}",
    response_model=CommodityProfileSchema,
    summary="Get a single commodity profile by ID",
    description="Fetches a single commodity profile by its integer ID. Returns 404 if not found.",
)
async def get_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    row = await crud.get_commodity_profile_by_id(db, profile_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Commodity profile id={profile_id} not found")
    return CommodityProfileSchema.model_validate(row)


@router.get(
    "/trade-summary",
    response_model=PaginatedResponse[TradeSummarySchema],
    summary="Trade summaries — filter by commodity name and/or year",
    description="Returns aggregated trade data from `vw_trade_summary`. Optionally filter by commodity name (case-insensitive partial match) and/or year.",
)
async def list_trade_summaries(
    commodity: Optional[str] = Query(None, description="Case-insensitive partial match on commodity name"),
    year: Optional[int] = Query(None, description="Filter by year", ge=1900, le=2100),
    db: AsyncSession = Depends(get_db),
):
    total, rows = await crud.get_trade_summaries(db, commodity=commodity, year=year)
    return {"total_count": total, "items": [TradeSummarySchema.model_validate(r) for r in rows]}


@router.get(
    "/latest-news",
    response_model=PaginatedResponse[LatestNewsSchema],
    summary="Latest commodity news feed",
    description="Returns the latest commodity news from `vw_latest_news`, deduplicated by title/date/commodity. Supports pagination via `limit` and `offset`.",
)
async def list_latest_news(
    limit: int = Query(50, ge=1, le=500, description="Max records to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: AsyncSession = Depends(get_db),
):
    total, rows = await crud.get_latest_news(db, limit=limit, offset=offset)
    return {"total_count": total, "items": [LatestNewsSchema.model_validate(r) for r in rows]}


@router.get(
    "/high-impact-news",
    response_model=PaginatedResponse[HighImpactNewsSchema],
    summary="High-impact commodity news",
    description="Returns high-impact news from `vw_high_impact_news`, deduplicated by title/date/commodity. Optionally filter by commodity name. Supports pagination.",
)
async def list_high_impact_news(
    commodity: Optional[str] = Query(None, description="Case-insensitive partial match on commodity name"),
    limit: int = Query(50, ge=1, le=500, description="Max records to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: AsyncSession = Depends(get_db),
):
    total, rows = await crud.get_high_impact_news(
        db, commodity=commodity, limit=limit, offset=offset
    )
    return {"total_count": total, "items": [HighImpactNewsSchema.model_validate(r) for r in rows]}
