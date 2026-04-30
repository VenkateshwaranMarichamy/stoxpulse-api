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

@router.get(
    "/list",
    response_model=List[CommodityListItem],
    summary="Simple list of all commodities (id + name + category)",
    description="Returns a lightweight list of all commodities — id, name, and category only. Useful for populating dropdowns and foreign-key lookups.",
)
async def list_commodities(db: AsyncSession = Depends(get_db)):
    rows = await crud.list_commodities(db)
    return [CommodityListItem.model_validate(r) for r in rows]


# ── Commodity CRUD ────────────────────────────────────────────────────────────

@router.post(
    "/",
    response_model=CommodityOut,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new commodity",
    description="Creates a new commodity record. `name` and `category` are required. Optional fields: `definition`, `uses`, `major_producers` (array), `notes` (array).",
)
async def create_commodity(payload: CommodityCreate, db: AsyncSession = Depends(get_db)):
    row = await crud.create_commodity(db, payload.model_dump())
    return CommodityOut.model_validate(row)


@router.patch(
    "/{commodity_id}",
    response_model=CommodityOut,
    summary="Update an existing commodity",
    description="Partially updates a commodity by ID. Only fields included in the request body are updated. Returns 404 if the commodity does not exist.",
)
async def update_commodity(
    commodity_id: int, payload: CommodityUpdate, db: AsyncSession = Depends(get_db)
):
    row = await crud.update_commodity(db, commodity_id, payload.model_dump(exclude_unset=True))
    if row is None:
        raise HTTPException(status_code=404, detail=f"Commodity id={commodity_id} not found")
    return CommodityOut.model_validate(row)


# ── News CRUD ─────────────────────────────────────────────────────────────────

@router.post(
    "/news",
    response_model=NewsOut,
    status_code=status.HTTP_201_CREATED,
    summary="Add a news article for a commodity",
    description="Creates a news article linked to an existing commodity via `commodity_id`. Returns 404 if the commodity does not exist. `impact_rating` must be one of: `low`, `medium`, `high`. `sentiment` must be one of: `bullish`, `bearish`, `neutral`.",
)
async def create_news(payload: NewsCreate, db: AsyncSession = Depends(get_db)):
    if not await crud.get_commodity_by_id_raw(db, payload.commodity_id):
        raise HTTPException(
            status_code=404,
            detail=f"Commodity id={payload.commodity_id} not found. Add the commodity first.",
        )
    row = await crud.create_news(db, payload.model_dump())
    return NewsOut.model_validate(row)


@router.patch(
    "/news/{news_id}",
    response_model=NewsOut,
    summary="Update a news article",
    description="Partially updates a news article by ID. Only fields included in the request body are updated. Returns 404 if the news article does not exist.",
)
async def update_news(
    news_id: int, payload: NewsUpdate, db: AsyncSession = Depends(get_db)
):
    row = await crud.update_news(db, news_id, payload.model_dump(exclude_unset=True))
    if row is None:
        raise HTTPException(status_code=404, detail=f"News id={news_id} not found")
    return NewsOut.model_validate(row)


# ── Trade CRUD ────────────────────────────────────────────────────────────────

@router.post(
    "/trade",
    response_model=TradeOut,
    status_code=status.HTTP_201_CREATED,
    summary="Add a trade record for a commodity",
    description="Creates a trade record linked to an existing commodity via `commodity_id`. Returns 404 if the commodity does not exist. `type` must be either `export` or `import`.",
)
async def create_trade(payload: TradeCreate, db: AsyncSession = Depends(get_db)):
    if not await crud.get_commodity_by_id_raw(db, payload.commodity_id):
        raise HTTPException(
            status_code=404,
            detail=f"Commodity id={payload.commodity_id} not found. Add the commodity first.",
        )
    row = await crud.create_trade(db, payload.model_dump())
    return TradeOut.model_validate(row)


@router.patch(
    "/trade/{trade_id}",
    response_model=TradeOut,
    summary="Update a trade record",
    description="Partially updates a trade record by ID. Only fields included in the request body are updated. Returns 404 if the trade record does not exist.",
)
async def update_trade(
    trade_id: int, payload: TradeUpdate, db: AsyncSession = Depends(get_db)
):
    row = await crud.update_trade(db, trade_id, payload.model_dump(exclude_unset=True))
    if row is None:
        raise HTTPException(status_code=404, detail=f"Trade id={trade_id} not found")
    return TradeOut.model_validate(row)
