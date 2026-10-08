-- I8 | P8: A que velocidad promedio circulan los taxis durante el dia? (congestion)
-- Razon de sumas (millas totales / horas totales), robusta frente a viajes extremos.
SELECT data_year AS anio, hour(pickup) AS hora,
       sum(trip_distance) / (sum(date_diff('second', pickup, dropoff)) / 3600.0) AS velocidad_mph
FROM trips_clean GROUP BY ALL ORDER BY ALL;
