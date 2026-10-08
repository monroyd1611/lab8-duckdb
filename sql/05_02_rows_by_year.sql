-- Objetivo: consulta conjunta de 2024 y 2026 sin cambiar la vista (5.6).
-- Fuente: vista trips (Parquet de todos los anios).
SELECT data_year AS anio, taxi, count(*) AS viajes, min(pickup) AS primer_pickup, max(pickup) AS ultimo_pickup
FROM trips GROUP BY ALL ORDER BY anio, taxi;
