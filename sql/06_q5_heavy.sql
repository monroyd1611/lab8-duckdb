-- Q5 agregacion pesada: 20 pares origen-destino mas frecuentes con percentiles (alta cardinalidad).
SELECT pu_location, do_location, count(*) AS viajes, avg(fare_amount) AS tarifa_media,
       quantile_cont(trip_distance, 0.5) AS dist_mediana
FROM {SRC} GROUP BY ALL ORDER BY viajes DESC LIMIT 20;
