-- Objetivo: detectar columnas que cambian entre anios (5.7).
-- Fuente: vista trips. Cuenta valores no nulos de columnas introducidas despues de 2024.
SELECT data_year AS anio, taxi, count(*) AS filas,
       count(cbd_congestion_fee) AS con_cbd_fee,
       count(airport_fee)        AS con_airport_fee,
       count(passenger_count)    AS con_pasajeros,
       count(*) FILTER (WHERE payment_type = 0) AS pago_tipo_0
FROM trips GROUP BY ALL ORDER BY anio, taxi;
