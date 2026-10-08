-- KPI globales (tarjetas del tablero): viajes, ingresos, tarifa media y % pago con tarjeta.
-- Fuente: trips_clean.
SELECT count(*) AS viajes, sum(total_amount) AS ingresos, avg(fare_amount) AS tarifa_media,
       100.0 * avg(CASE WHEN payment_type = 1 THEN 1 ELSE 0 END) AS pct_tarjeta,
       min(data_year) AS anio_min, max(data_year) AS anio_max
FROM trips_clean;
