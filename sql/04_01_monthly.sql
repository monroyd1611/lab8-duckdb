-- Pregunta: como evoluciona el volumen de viajes mes a mes y por taxi?
-- Fuente: trips_clean (Parquet yellow + green).
SELECT data_year AS anio, data_month AS mes, taxi, count(*) AS viajes
FROM trips_clean GROUP BY ALL ORDER BY anio, mes, taxi;
