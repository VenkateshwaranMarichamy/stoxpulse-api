import logging
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


# ── Commodity Profile ─────────────────────────────────────────────────────────

async def get_commodity_profiles(db: AsyncSession) -> Tuple[int, List[Dict]]:
    count_result = await db.execute(
        text("SELECT COUNT(*) FROM commodities.vw_commodity_profile")
    )
    total = count_result.scalar_one()

    result = await db.execute(
        text("SELECT * FROM commodities.vw_commodity_profile ORDER BY name")
    )
    rows = [dict(r._mapping) for r in result.fetchall()]
    logger.info("Fetched %d commodity profiles", total)
    return total, rows


async def get_commodity_profile_by_id(db: AsyncSession, profile_id: int) -> Optional[Dict]:
    result = await db.execute(
        text("SELECT * FROM commodities.vw_commodity_profile WHERE id = :id"),
        {"id": profile_id},
    )
    row = result.fetchone()
    if row is None:
        logger.warning("CommodityProfile id=%d not found", profile_id)
        return None
    return dict(row._mapping)


# ── Trade Summary ─────────────────────────────────────────────────────────────

async def get_trade_summaries(
    db: AsyncSession,
    commodity: Optional[str] = None,
    year: Optional[int] = None,
) -> Tuple[int, List[Dict]]:
    filters = []
    params: Dict[str, Any] = {}

    if commodity:
        filters.append("name ILIKE :commodity")
        params["commodity"] = f"%{commodity}%"
    if year:
        filters.append("year = :year")
        params["year"] = year

    where = f"WHERE {' AND '.join(filters)}" if filters else ""

    count_result = await db.execute(
        text(f"SELECT COUNT(*) FROM commodities.vw_trade_summary {where}"), params
    )
    total = count_result.scalar_one()

    result = await db.execute(
        text(f"SELECT * FROM commodities.vw_trade_summary {where} ORDER BY name, year DESC, type"),
        params,
    )
    rows = [dict(r._mapping) for r in result.fetchall()]
    logger.info("Fetched %d trade summaries (commodity=%s, year=%s)", total, commodity, year)
    return total, rows


# ── Latest News ───────────────────────────────────────────────────────────────

async def get_latest_news(
    db: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> Tuple[int, List[Dict]]:
    count_result = await db.execute(
        text("SELECT COUNT(*) FROM commodities.vw_latest_news")
    )
    total = count_result.scalar_one()

    result = await db.execute(
        text("""
            SELECT DISTINCT ON (title, pub_date, commodity) *
            FROM commodities.vw_latest_news
            ORDER BY title, pub_date DESC, commodity
            LIMIT :limit OFFSET :offset
        """),
        {"limit": limit, "offset": offset},
    )
    rows = [dict(r._mapping) for r in result.fetchall()]
    logger.info("Fetched %d latest news (limit=%d, offset=%d)", len(rows), limit, offset)
    return total, rows


# ── High Impact News ──────────────────────────────────────────────────────────

async def get_high_impact_news(
    db: AsyncSession,
    commodity: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> Tuple[int, List[Dict]]:
    params: Dict[str, Any] = {"limit": limit, "offset": offset}
    commodity_filter = ""

    if commodity:
        commodity_filter = "WHERE commodity ILIKE :commodity"
        params["commodity"] = f"%{commodity}%"

    count_result = await db.execute(
        text(f"""
            SELECT COUNT(*) FROM (
                SELECT DISTINCT title, pub_date, commodity FROM commodities.vw_high_impact_news {commodity_filter}
            ) t
        """),
        params,
    )
    total = count_result.scalar_one()

    result = await db.execute(
        text(f"""
            SELECT DISTINCT ON (title, pub_date, commodity) *
            FROM commodities.vw_high_impact_news
            {commodity_filter}
            ORDER BY title, pub_date DESC, commodity
            LIMIT :limit OFFSET :offset
        """),
        params,
    )
    rows = [dict(r._mapping) for r in result.fetchall()]
    logger.info(
        "Fetched %d high-impact news (commodity=%s, limit=%d, offset=%d)",
        len(rows), commodity, limit, offset,
    )
    return total, rows


# ── Commodity table CRUD ──────────────────────────────────────────────────────

async def list_commodities(db: AsyncSession) -> List[Dict]:
    result = await db.execute(
        text("SELECT id, name, category FROM commodities.commodities ORDER BY name")
    )
    return [dict(r._mapping) for r in result.fetchall()]


async def create_commodity(db: AsyncSession, data: Dict) -> Dict:
    result = await db.execute(
        text("""
            INSERT INTO commodities.commodities (name, category, definition, uses, major_producers, notes)
            VALUES (:name, :category, :definition, :uses, :major_producers, :notes)
            RETURNING *
        """),
        data,
    )
    await db.commit()
    row = result.fetchone()
    return dict(row._mapping)


async def update_commodity(db: AsyncSession, commodity_id: int, data: Dict) -> Optional[Dict]:
    # Build dynamic SET clause from non-null fields only
    fields = {k: v for k, v in data.items() if v is not None}
    if not fields:
        result = await db.execute(
            text("SELECT * FROM commodities.commodities WHERE id = :id"), {"id": commodity_id}
        )
        row = result.fetchone()
        return dict(row._mapping) if row else None

    set_clause = ", ".join(f"{k} = :{k}" for k in fields)
    fields["id"] = commodity_id
    result = await db.execute(
        text(f"UPDATE commodities.commodities SET {set_clause}, updated_at = now() WHERE id = :id RETURNING *"),
        fields,
    )
    await db.commit()
    row = result.fetchone()
    return dict(row._mapping) if row else None


# ── Commodity News CRUD ───────────────────────────────────────────────────────

async def get_commodity_by_id_raw(db: AsyncSession, commodity_id: int) -> Optional[Dict]:
    result = await db.execute(
        text("SELECT id FROM commodities.commodities WHERE id = :id"), {"id": commodity_id}
    )
    row = result.fetchone()
    return dict(row._mapping) if row else None


async def create_news(db: AsyncSession, data: Dict) -> Dict:
    result = await db.execute(
        text("""
            INSERT INTO commodities.commodity_news
                (commodity_id, title, summary, url, pub_date, impact_rating, sentiment, keywords, source)
            VALUES
                (:commodity_id, :title, :summary, :url, :pub_date, :impact_rating, :sentiment, :keywords, :source)
            RETURNING *
        """),
        data,
    )
    await db.commit()
    row = result.fetchone()
    return dict(row._mapping)


async def update_news(db: AsyncSession, news_id: int, data: Dict) -> Optional[Dict]:
    fields = {k: v for k, v in data.items() if v is not None}
    if not fields:
        result = await db.execute(
            text("SELECT * FROM commodities.commodity_news WHERE id = :id"), {"id": news_id}
        )
        row = result.fetchone()
        return dict(row._mapping) if row else None

    set_clause = ", ".join(f"{k} = :{k}" for k in fields)
    fields["id"] = news_id
    result = await db.execute(
        text(f"UPDATE commodities.commodity_news SET {set_clause}, updated_at = now() WHERE id = :id RETURNING *"),
        fields,
    )
    await db.commit()
    row = result.fetchone()
    return dict(row._mapping) if row else None


# ── Commodity Trade CRUD ──────────────────────────────────────────────────────

async def create_trade(db: AsyncSession, data: Dict) -> Dict:
    result = await db.execute(
        text("""
            INSERT INTO commodities.commodity_trade
                (commodity_id, type, countries, volume_metric, total_value, year, source, description, currency)
            VALUES
                (:commodity_id, :type, :countries, :volume_metric, :total_value, :year, :source, :description, :currency)
            RETURNING *
        """),
        data,
    )
    await db.commit()
    row = result.fetchone()
    return dict(row._mapping)


async def update_trade(db: AsyncSession, trade_id: int, data: Dict) -> Optional[Dict]:
    fields = {k: v for k, v in data.items() if v is not None}
    if not fields:
        result = await db.execute(
            text("SELECT * FROM commodities.commodity_trade WHERE id = :id"), {"id": trade_id}
        )
        row = result.fetchone()
        return dict(row._mapping) if row else None

    set_clause = ", ".join(f"{k} = :{k}" for k in fields)
    fields["id"] = trade_id
    result = await db.execute(
        text(f"UPDATE commodities.commodity_trade SET {set_clause}, updated_at = now() WHERE id = :id RETURNING *"),
        fields,
    )
    await db.commit()
    row = result.fetchone()
    return dict(row._mapping) if row else None
