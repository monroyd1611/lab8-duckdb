-- Pregunta: en que se diferencian los taxis amarillos de los verdes?
-- Fuente: trips_clean.
SELECT taxi,
  count(*)                                                       AS viajes,
  round(avg(fare_amount), 2)                                     AS tarifa_media,
  round(avg(total_amount), 2)                                    AS total_medio,
  round(avg(trip_distance), 2)                                   AS dist_media,
  round(avg(fare_amount / trip_distance), 2)                     AS tarifa_por_milla,
  round(avg(trip_distance / (date_diff('second', pickup, dropoff) / 3600.0)), 1) AS velocidad_mph,
  round(avg(passenger_count), 2)                                 AS pasajeros_medios,
  round(100.0 * avg(CASE WHEN tolls_amount > 0 THEN 1 ELSE 0 END), 2) AS pct_con_peaje
FROM trips_clean GROUP BY taxi;
