"""
SQLAlchemy mapped classes for the PostgreSQL views.
Views are read-only — no primary key enforcement needed beyond mapping.
"""
from sqlalchemy import Column, Date, Integer, Numeric, String, Text
from sqlalchemy.orm import mapped_column

from app.database import Base


class CommodityProfile(Base):
    __tablename__ = "vw_commodity_profile"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    unit = Column(String)
    description = Column(Text)
    current_price = Column(Numeric)
    currency = Column(String)
    exchange = Column(String)
    country_of_origin = Column(String)
    last_updated = Column(Date)


class TradeSummary(Base):
    __tablename__ = "vw_trade_summary"

    id = Column(Integer, primary_key=True)
    commodity = Column(String)
    year = Column(Integer)
    total_export_volume = Column(Numeric)
    total_import_volume = Column(Numeric)
    net_trade_balance = Column(Numeric)
    top_exporter = Column(String)
    top_importer = Column(String)
    avg_price = Column(Numeric)
    currency = Column(String)


class LatestNews(Base):
    __tablename__ = "vw_latest_news"

    id = Column(Integer, primary_key=True)
    headline = Column(String)
    summary = Column(Text)
    source = Column(String)
    url = Column(String)
    commodity = Column(String)
    published_at = Column(Date)
    sentiment = Column(String)


class HighImpactNews(Base):
    __tablename__ = "vw_high_impact_news"

    id = Column(Integer, primary_key=True)
    headline = Column(String)
    summary = Column(Text)
    source = Column(String)
    url = Column(String)
    commodity = Column(String)
    published_at = Column(Date)
    impact_score = Column(Numeric)
    sentiment = Column(String)
