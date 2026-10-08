-- Pregunta: como se distribuyen la distancia y la duracion de los viajes?
-- Fuente: trips_clean.
SELECT taxi,
  round(avg(trip_distance), 2)                           AS dist_media,
  round(quantile_cont(trip_distance, 0.50), 2)           AS dist_p50,
  round(quantile_cont(trip_distance, 0.90), 2)           AS dist_p90,
  round(quantile_cont(trip_distance, 0.99), 2)           AS dist_p99,
  round(avg(date_diff('second', pickup, dropoff)) / 60, 1) AS dur_media_min,
  round(quantile_cont(date_diff('second', pickup, dropoff) / 60.0, 0.50), 1) AS dur_p50_min,
  round(quantile_cont(date_diff('second', pickup, dropoff) / 60.0, 0.99), 1) AS dur_p99_min
FROM trips_clean GROUP BY taxi;
