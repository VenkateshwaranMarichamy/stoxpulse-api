from datetime import date
from decimal import Decimal
from typing import Generic, List, Literal, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, HttpUrl, field_validator

T = TypeVar("T")


# ── Generic ───────────────────────────────────────────────────────────────────

class PaginatedResponse(BaseModel, Generic[T]):
    total_count: int
    items: List[T]


# ── View schemas (read) ───────────────────────────────────────────────────────

class CommodityProfileSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: Optional[str] = None
    category: Optional[str] = None
    definition: Optional[str] = None
    uses: Optional[str] = None
    major_producers: Optional[List[str]] = None
    notes: Optional[List[str]] = None
    trade_records: Optional[int] = None
    news_count: Optional[int] = None


class TradeSummarySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None
    category: Optional[str] = None
    type: Optional[str] = None
    year: Optional[int] = None
    countries: Optional[List[str]] = None
    total_value: Optional[str] = None
    currency: Optional[str] = None
    volume_metric: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None


class LatestNewsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    pub_date: Optional[date] = None
    commodity: Optional[str] = None
    category: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    sentiment: Optional[str] = None
    impact_rating: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    keywords: Optional[List[str]] = None


class HighImpactNewsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    pub_date: Optional[date] = None
    commodity: Optional[str] = None
    category: Optional[str] = None
    title: Optional[str] = None
    sentiment: Optional[str] = None
    impact_rating: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None


# ── Commodity table schemas ───────────────────────────────────────────────────

class CommodityListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    category: str


class CommodityCreate(BaseModel):
    name: str
    category: str
    definition: Optional[str] = None
    uses: Optional[str] = None
    major_producers: Optional[List[str]] = None
    notes: Optional[List[str]] = None


class CommodityUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    definition: Optional[str] = None
    uses: Optional[str] = None
    major_producers: Optional[List[str]] = None
    notes: Optional[List[str]] = None


class CommodityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    category: str
    definition: Optional[str] = None
    uses: Optional[str] = None
    major_producers: Optional[List[str]] = None
    notes: Optional[List[str]] = None


# ── Commodity News schemas ────────────────────────────────────────────────────

class NewsCreate(BaseModel):
    commodity_id: int
    title: str
    summary: Optional[str] = None
    url: Optional[str] = None
    pub_date: Optional[date] = None
    impact_rating: Optional[Literal["low", "medium", "high"]] = None
    sentiment: Optional[Literal["bullish", "bearish", "neutral"]] = None
    keywords: Optional[List[str]] = None
    source: Optional[str] = None


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    url: Optional[str] = None
    pub_date: Optional[date] = None
    impact_rating: Optional[Literal["low", "medium", "high"]] = None
    sentiment: Optional[Literal["bullish", "bearish", "neutral"]] = None
    keywords: Optional[List[str]] = None
    source: Optional[str] = None


class NewsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    commodity_id: int
    title: str
    summary: Optional[str] = None
    url: Optional[str] = None
    pub_date: Optional[date] = None
    impact_rating: Optional[str] = None
    sentiment: Optional[str] = None
    keywords: Optional[List[str]] = None
    source: Optional[str] = None


# ── Commodity Trade schemas ───────────────────────────────────────────────────

class TradeCreate(BaseModel):
    commodity_id: int
    type: Literal["export", "import"]
    countries: Optional[List[str]] = None
    volume_metric: Optional[str] = None
    total_value: Optional[str] = None
    year: Optional[int] = None
    source: Optional[str] = None
    description: Optional[str] = None
    currency: Optional[str] = None


class TradeUpdate(BaseModel):
    type: Optional[Literal["export", "import"]] = None
    countries: Optional[List[str]] = None
    volume_metric: Optional[str] = None
    total_value: Optional[str] = None
    year: Optional[int] = None
    source: Optional[str] = None
    description: Optional[str] = None
    currency: Optional[str] = None


class TradeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    commodity_id: int
    type: str
    countries: Optional[List[str]] = None
    volume_metric: Optional[str] = None
    total_value: Optional[str] = None
    year: Optional[int] = None
    source: Optional[str] = None
    description: Optional[str] = None
    currency: Optional[str] = None
