-- Objetivo: total de registros por tipo de taxi (3.2).
-- Fuente: yellow_tripdata_*.parquet y green_tripdata_*.parquet (via vista trips).
SELECT taxi, count(*) AS registros FROM trips GROUP BY taxi
UNION ALL
SELECT 'TOTAL', count(*) FROM trips;
