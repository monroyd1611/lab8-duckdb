-- Objetivo: ver las fechas de recogida fuera del periodo del archivo (3.6).
-- Fuente: vista trips.
SELECT taxi, year(pickup) AS anio_pickup, data_year, count(*) AS viajes
FROM trips
WHERE year(pickup) <> data_year OR month(pickup) <> data_month
GROUP BY ALL ORDER BY viajes DESC LIMIT 15;
