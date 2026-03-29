"""
All database access lives here — thin async wrappers over SQLAlchemy queries.
"""
import logging
from typing import List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CommodityProfile, HighImpactNews, LatestNews, TradeSummary

logger = logging.getLogger(__name__)


# ── Commodity Profile ─────────────────────────────────────────────────────────

async def get_commodity_profiles(
    db: AsyncSession,
) -> Tuple[int, List[CommodityProfile]]:
    count_q = select(func.count()).select_from(CommodityProfile)
    total = (await db.execute(count_q)).scalar_one()

    rows = (await db.execute(select(CommodityProfile))).scalars().all()
    logger.info("Fetched %d commodity profiles", total)
    return total, list(rows)


async def get_commodity_profile_by_id(
    db: AsyncSession, profile_id: int
) -> Optional[CommodityProfile]:
    result = await db.execute(
        select(CommodityProfile).where(CommodityProfile.id == profile_id)
    )
    row = result.scalar_one_or_none()
    if row is None:
        logger.warning("CommodityProfile id=%d not found", profile_id)
    return row


# ── Trade Summary ─────────────────────────────────────────────────────────────

async def get_trade_summaries(
    db: AsyncSession,
    commodity: Optional[str] = None,
    year: Optional[int] = None,
) -> Tuple[int, List[TradeSummary]]:
    q = select(TradeSummary)
    if commodity:
        q = q.where(TradeSummary.commodity.ilike(f"%{commodity}%"))
    if year:
        q = q.where(TradeSummary.year == year)

    count_q = select(func.count()).select_from(q.subquery())
    total = (await db.execute(count_q)).scalar_one()

    rows = (await db.execute(q)).scalars().all()
    logger.info("Fetched %d trade summaries (commodity=%s, year=%s)", total, commodity, year)
    return total, list(rows)


# ── Latest News ───────────────────────────────────────────────────────────────

async def get_latest_news(
    db: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> Tuple[int, List[LatestNews]]:
    count_q = select(func.count()).select_from(LatestNews)
    total = (await db.execute(count_q)).scalar_one()

    q = select(LatestNews).order_by(LatestNews.published_at.desc()).limit(limit).offset(offset)
    rows = (await db.execute(q)).scalars().all()
    logger.info("Fetched %d latest news (limit=%d, offset=%d)", len(rows), limit, offset)
    return total, list(rows)


# ── High Impact News ──────────────────────────────────────────────────────────

async def get_high_impact_news(
    db: AsyncSession,
    commodity: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> Tuple[int, List[HighImpactNews]]:
    q = select(HighImpactNews)
    if commodity:
        q = q.where(HighImpactNews.commodity.ilike(f"%{commodity}%"))

    count_q = select(func.count()).select_from(q.subquery())
    total = (await db.execute(count_q)).scalar_one()

    q = q.order_by(HighImpactNews.impact_score.desc()).limit(limit).offset(offset)
    rows = (await db.execute(q)).scalars().all()
    logger.info(
        "Fetched %d high-impact news (commodity=%s, limit=%d, offset=%d)",
        len(rows), commodity, limit, offset,
    )
    return total, list(rows)
