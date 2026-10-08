-- Q1 agregacion global: tarifa y distancia medias por taxi (escanea pocas columnas).
SELECT taxi, count(*) AS viajes, avg(fare_amount) AS tarifa_media, avg(trip_distance) AS dist_media
FROM {SRC} GROUP BY taxi;
