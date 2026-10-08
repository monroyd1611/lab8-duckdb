-- Objetivo: la consulta mensual de 04_01 reutilizada tal cual con dos anios (5.7).
-- Fuente: trips_clean.
SELECT data_year AS anio, data_month AS mes, taxi, count(*) AS viajes
FROM trips_clean GROUP BY ALL ORDER BY anio, mes, taxi;
