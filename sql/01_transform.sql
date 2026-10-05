CREATE OR REPLACE VIEW MARKET_ETL_DB.MARTS.INFLATION_RATES_MONTHLY AS
WITH monthly_base AS (
    SELECT
        DATE_TRUNC('MONTH', obs_date) AS month,
        metric,
        value,
        ROW_NUMBER() OVER (
            PARTITION BY DATE_TRUNC('MONTH', obs_date), metric
            ORDER BY obs_date DESC
        ) AS rn
    FROM MARKET_ETL_DB.RAW.ECON_SERIES
)
SELECT
    month,
    MAX(CASE WHEN metric = 'cpi_headline' THEN value END)      AS cpi,
    MAX(CASE WHEN metric = 'pce_price_index' THEN value END)   AS pce,
    MAX(CASE WHEN metric = 'fed_funds_rate' THEN value END)    AS fed_funds_rate,
    MAX(CASE WHEN metric = 'treasury_10y' THEN value END)      AS treasury_10y,
    MAX(CASE WHEN metric = 'unemployment_rate' THEN value END) AS unemployment_rate
FROM monthly_base
WHERE rn = 1
GROUP BY month
ORDER BY month;