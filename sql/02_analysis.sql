CREATE OR REPLACE VIEW MARKET_ETL_DB.MARTS.REAL_RATES_ANALYSIS AS
SELECT
    month,
    cpi,
    fed_funds_rate,
    treasury_10y,
    unemployment_rate,
    ROUND(
        (cpi - LAG(cpi, 12) OVER (ORDER BY month)) / LAG(cpi, 12) OVER (ORDER BY month) * 100,
        2
    ) AS cpi_yoy_pct,
    ROUND(
        fed_funds_rate - (
            (cpi - LAG(cpi, 12) OVER (ORDER BY month)) / LAG(cpi, 12) OVER (ORDER BY month) * 100
        ),
        2
    ) AS real_fed_funds_rate
FROM MARKET_ETL_DB.MARTS.INFLATION_RATES_MONTHLY
ORDER BY month;