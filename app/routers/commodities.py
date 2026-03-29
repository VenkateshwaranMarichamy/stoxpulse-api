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


# ── Commodity Profile ─────────────────────────────────────────────────────────

@router.get(
    "/profiles",
    response_model=PaginatedResponse[CommodityProfileSchema],
    summary="List all commodity profiles",
)
async def list_profiles(db: AsyncSession = Depends(get_db)):
    total, items = await crud.get_commodity_profiles(db)
    return {"total_count": total, "items": items}


@router.get(
    "/profiles/{profile_id}",
    response_model=CommodityProfileSchema,
    summary="Get a single commodity profile by ID",
)
async def get_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    row = await crud.get_commodity_profile_by_id(db, profile_id)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Commodity profile with id={profile_id} not found",
        )
    return row


# ── Trade Summary ─────────────────────────────────────────────────────────────

@router.get(
    "/trade-summary",
    response_model=PaginatedResponse[TradeSummarySchema],
    summary="List trade summaries with optional filters",
)
async def list_trade_summaries(
    commodity: Optional[str] = Query(None, description="Filter by commodity name"),
    year: Optional[int] = Query(None, description="Filter by year", ge=1900, le=2100),
    db: AsyncSession = Depends(get_db),
):
    total, items = await crud.get_trade_summaries(db, commodity=commodity, year=year)
    return {"total_count": total, "items": items}


# ── Latest News ───────────────────────────────────────────────────────────────

@router.get(
    "/latest-news",
    response_model=PaginatedResponse[LatestNewsSchema],
    summary="Get latest commodity news",
)
async def list_latest_news(
    limit: int = Query(50, ge=1, le=500, description="Max records to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: AsyncSession = Depends(get_db),
):
    total, items = await crud.get_latest_news(db, limit=limit, offset=offset)
    return {"total_count": total, "items": items}


# ── High Impact News ──────────────────────────────────────────────────────────

@router.get(
    "/high-impact-news",
    response_model=PaginatedResponse[HighImpactNewsSchema],
    summary="Get high-impact commodity news",
)
async def list_high_impact_news(
    commodity: Optional[str] = Query(None, description="Filter by commodity name"),
    limit: int = Query(50, ge=1, le=500, description="Max records to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: AsyncSession = Depends(get_db),
):
    total, items = await crud.get_high_impact_news(
        db, commodity=commodity, limit=limit, offset=offset
    )
    return {"total_count": total, "items": items}
