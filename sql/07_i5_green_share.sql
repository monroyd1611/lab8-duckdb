-- I5 | P5: Que participacion tiene el taxi verde en el total de viajes? (mercado)
SELECT data_year AS anio, data_month AS mes,
       100.0 * avg(CASE WHEN taxi = 'green' THEN 1 ELSE 0 END) AS pct_verde
FROM trips_clean GROUP BY ALL ORDER BY ALL;
