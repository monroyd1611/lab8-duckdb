-- Comparacion justa entre anios: solo enero-agosto (los meses que existen en los tres anios).
-- Fuente: trips_clean.
SELECT data_year AS anio, count(*) AS viajes, round(sum(total_amount) / 1e6, 1) AS ingresos_musd,
       round(avg(fare_amount), 2) AS tarifa_media,
       round(100.0 * avg(CASE WHEN taxi = 'green' THEN 1 ELSE 0 END), 2) AS pct_verde,
       round(100.0 * avg(CASE WHEN payment_type = 1 THEN 1 ELSE 0 END), 1) AS pct_tarjeta,
       round(100.0 * avg(CASE WHEN payment_type = 0 THEN 1 ELSE 0 END), 1) AS pct_flex,
       round(100.0 * avg(CASE WHEN payment_type = 2 THEN 1 ELSE 0 END), 1) AS pct_efectivo,
       round(sum(trip_distance) / (sum(date_diff('second', pickup, dropoff)) / 3600.0), 2) AS velocidad_mph,
       round(100.0 * avg(CASE WHEN coalesce(cbd_congestion_fee, 0) > 0 THEN 1 ELSE 0 END), 1) AS pct_cbd
FROM trips_clean WHERE data_month <= 8 GROUP BY data_year ORDER BY data_year;
