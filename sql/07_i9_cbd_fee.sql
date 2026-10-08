-- I9 | P9: Que parte de los viajes paga el cargo por congestion de Manhattan (cbd_congestion_fee)? (regulacion)
SELECT data_year AS anio, data_month AS mes,
       100.0 * avg(CASE WHEN coalesce(cbd_congestion_fee, 0) > 0 THEN 1 ELSE 0 END) AS pct_con_cargo,
       avg(cbd_congestion_fee) FILTER (WHERE cbd_congestion_fee > 0) AS cargo_medio
FROM trips_clean GROUP BY ALL ORDER BY ALL;
