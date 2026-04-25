import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_db
from app.schemas import (
    CommodityCreate, CommodityListItem, CommodityOut, CommodityUpdate,
    NewsCreate, NewsOut, NewsUpdate,
    TradeCreate, TradeOut, TradeUpdate,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/commodities", tags=["Admin — Write"])


# ── Commodity list (for dropdowns) ────────────────────────────────────────────

@router.get("/list", response_model=List[CommodityListItem],
            summary="Simple list of all commodities (id + name + category)")
async def list_commodities(db: AsyncSession = Depends(get_db)):
    rows = await crud.list_commodities(db)
    return [CommodityListItem.model_validate(r) for r in rows]


# ── Commodity CRUD ────────────────────────────────────────────────────────────

@router.post("/", response_model=CommodityOut, status_code=status.HTTP_201_CREATED,
             summary="Add a new commodity")
async def create_commodity(payload: CommodityCreate, db: AsyncSession = Depends(get_db)):
    row = await crud.create_commodity(db, payload.model_dump())
    return CommodityOut.model_validate(row)


@router.patch("/{commodity_id}", response_model=CommodityOut,
              summary="Update an existing commodity")
async def update_commodity(
    commodity_id: int, payload: CommodityUpdate, db: AsyncSession = Depends(get_db)
):
    row = await crud.update_commodity(db, commodity_id, payload.model_dump(exclude_unset=True))
    if row is None:
        raise HTTPException(status_code=404, detail=f"Commodity id={commodity_id} not found")
    return CommodityOut.model_validate(row)


# ── News CRUD ─────────────────────────────────────────────────────────────────

@router.post("/news", response_model=NewsOut, status_code=status.HTTP_201_CREATED,
             summary="Add news for a commodity")
async def create_news(payload: NewsCreate, db: AsyncSession = Depends(get_db)):
    # Validate commodity exists
    if not await crud.get_commodity_by_id_raw(db, payload.commodity_id):
        raise HTTPException(
            status_code=404,
            detail=f"Commodity id={payload.commodity_id} not found. Add the commodity first.",
        )
    row = await crud.create_news(db, payload.model_dump())
    return NewsOut.model_validate(row)


@router.patch("/news/{news_id}", response_model=NewsOut,
              summary="Update a news entry")
async def update_news(
    news_id: int, payload: NewsUpdate, db: AsyncSession = Depends(get_db)
):
    row = await crud.update_news(db, news_id, payload.model_dump(exclude_unset=True))
    if row is None:
        raise HTTPException(status_code=404, detail=f"News id={news_id} not found")
    return NewsOut.model_validate(row)


# ── Trade CRUD ────────────────────────────────────────────────────────────────

@router.post("/trade", response_model=TradeOut, status_code=status.HTTP_201_CREATED,
             summary="Add a trade record for a commodity")
async def create_trade(payload: TradeCreate, db: AsyncSession = Depends(get_db)):
    # Validate commodity exists
    if not await crud.get_commodity_by_id_raw(db, payload.commodity_id):
        raise HTTPException(
            status_code=404,
            detail=f"Commodity id={payload.commodity_id} not found. Add the commodity first.",
        )
    row = await crud.create_trade(db, payload.model_dump())
    return TradeOut.model_validate(row)


@router.patch("/trade/{trade_id}", response_model=TradeOut,
              summary="Update a trade record")
async def update_trade(
    trade_id: int, payload: TradeUpdate, db: AsyncSession = Depends(get_db)
):
    row = await crud.update_trade(db, trade_id, payload.model_dump(exclude_unset=True))
    if row is None:
        raise HTTPException(status_code=404, detail=f"Trade id={trade_id} not found")
    return TradeOut.model_validate(row)
