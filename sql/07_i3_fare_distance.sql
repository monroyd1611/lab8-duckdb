-- I3 | P3: Cuanto cuesta y cuanto recorre en promedio un viaje, por anio y taxi? (precio)
SELECT data_year AS anio, taxi, avg(fare_amount) AS tarifa_media, avg(trip_distance) AS dist_media,
       avg(fare_amount) / avg(trip_distance) AS usd_por_milla
FROM trips_clean GROUP BY ALL ORDER BY ALL;
