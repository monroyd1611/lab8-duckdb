-- Objetivo: contar anomalias de calidad en yellow y green (3.6).
-- Fuente: yellow_tripdata_*.parquet y green_tripdata_*.parquet (via vista trips).
SELECT taxi,
  count(*)                                                AS total,
  count(*) FILTER (WHERE passenger_count IS NULL)         AS pasajeros_nulos,
  count(*) FILTER (WHERE passenger_count = 0)             AS pasajeros_cero,
  count(*) FILTER (WHERE trip_distance = 0)               AS distancia_cero,
  count(*) FILTER (WHERE trip_distance >= 100)            AS distancia_100_o_mas,
  count(*) FILTER (WHERE fare_amount <= 0)                AS tarifa_no_positiva,
  count(*) FILTER (WHERE total_amount <= 0)               AS total_no_positivo,
  count(*) FILTER (WHERE total_amount >= 1000)            AS total_1000_o_mas,
  count(*) FILTER (WHERE dropoff <= pickup)               AS bajada_antes_o_igual_subida,
  count(*) FILTER (WHERE dropoff - pickup >= INTERVAL 6 HOUR) AS duracion_6h_o_mas,
  count(*) FILTER (WHERE year(pickup) <> data_year OR month(pickup) <> data_month) AS fuera_del_mes_del_archivo,
  count(*) FILTER (WHERE payment_type = 0)                AS pago_tipo_0,
  count(*) FILTER (WHERE tip_amount < 0)                  AS propina_negativa
FROM trips GROUP BY taxi ORDER BY taxi;
