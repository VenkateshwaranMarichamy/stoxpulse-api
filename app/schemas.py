from datetime import date
from decimal import Decimal
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


# ── Generic paginated response ────────────────────────────────────────────────
class PaginatedResponse(BaseModel, Generic[T]):
    total_count: int
    items: List[T]


# ── Commodity Profile ─────────────────────────────────────────────────────────
class CommodityProfileSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    description: Optional[str] = None
    current_price: Optional[Decimal] = None
    currency: Optional[str] = None
    exchange: Optional[str] = None
    country_of_origin: Optional[str] = None
    last_updated: Optional[date] = None


# ── Trade Summary ─────────────────────────────────────────────────────────────
class TradeSummarySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    commodity: Optional[str] = None
    year: Optional[int] = None
    total_export_volume: Optional[Decimal] = None
    total_import_volume: Optional[Decimal] = None
    net_trade_balance: Optional[Decimal] = None
    top_exporter: Optional[str] = None
    top_importer: Optional[str] = None
    avg_price: Optional[Decimal] = None
    currency: Optional[str] = None


# ── Latest News ───────────────────────────────────────────────────────────────
class LatestNewsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    headline: Optional[str] = None
    summary: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    commodity: Optional[str] = None
    published_at: Optional[date] = None
    sentiment: Optional[str] = None


# ── High Impact News ──────────────────────────────────────────────────────────
class HighImpactNewsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    headline: Optional[str] = None
    summary: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    commodity: Optional[str] = None
    published_at: Optional[date] = None
    impact_score: Optional[Decimal] = None
    sentiment: Optional[str] = None
