-- ============================================================
-- Commodity API Views
-- Adjust the SELECT sources to match your actual table names
-- ============================================================

-- 1. vw_commodity_profile
CREATE OR REPLACE VIEW vw_commodity_profile AS
SELECT
    id,
    name,
    category,
    unit,
    description,
    current_price,
    currency,
    exchange,
    country_of_origin,
    last_updated
FROM commodities;  -- replace with your actual table name


-- 2. vw_trade_summary
CREATE OR REPLACE VIEW vw_trade_summary AS
SELECT
    id,
    commodity,
    year,
    total_export_volume,
    total_import_volume,
    net_trade_balance,
    top_exporter,
    top_importer,
    avg_price,
    currency
FROM trade_summaries;  -- replace with your actual table name


-- 3. vw_latest_news
CREATE OR REPLACE VIEW vw_latest_news AS
SELECT
    id,
    headline,
    summary,
    source,
    url,
    commodity,
    published_at,
    sentiment
FROM news
ORDER BY published_at DESC;  -- replace with your actual table name


-- 4. vw_high_impact_news
CREATE OR REPLACE VIEW vw_high_impact_news AS
SELECT
    id,
    headline,
    summary,
    source,
    url,
    commodity,
    published_at,
    impact_score,
    sentiment
FROM news
WHERE impact_score IS NOT NULL
ORDER BY impact_score DESC;  -- replace with your actual table name
