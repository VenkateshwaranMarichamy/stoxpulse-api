from sqlalchemy import BigInteger, Column, Date, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from app.database import Base


class CommodityProfile(Base):
    __tablename__ = "vw_commodity_profile"
    __table_args__ = {"schema": "commodities"}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    definition = Column(Text)
    uses = Column(Text)
    major_producers = Column(ARRAY(String))
    notes = Column(ARRAY(String))
    trade_records = Column(BigInteger)
    news_count = Column(BigInteger)


class TradeSummary(Base):
    __tablename__ = "vw_trade_summary"
    __table_args__ = {"schema": "commodities"}

    name = Column(String, primary_key=True)
    category = Column(String)
    type = Column(String, primary_key=True)
    year = Column(Integer, primary_key=True)
    countries = Column(ARRAY(String))
    total_value = Column(String)
    currency = Column(String)
    volume_metric = Column(String)
    description = Column(Text)
    source = Column(String)


class LatestNews(Base):
    __tablename__ = "vw_latest_news"
    __table_args__ = {"schema": "commodities"}

    url = Column(String, primary_key=True)
    pub_date = Column(Date)
    commodity = Column(String)
    category = Column(String)
    title = Column(String)
    summary = Column(Text)
    sentiment = Column(String)
    impact_rating = Column(String)
    source = Column(String)
    keywords = Column(ARRAY(String))


class HighImpactNews(Base):
    __tablename__ = "vw_high_impact_news"
    __table_args__ = {"schema": "commodities"}

    url = Column(String, primary_key=True)
    pub_date = Column(Date)
    commodity = Column(String)
    category = Column(String)
    title = Column(String)
    sentiment = Column(String)
    impact_rating = Column(String)
    source = Column(String)
