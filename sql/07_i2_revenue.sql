-- I2 | P2: Cuantos ingresos (total_amount) generan los viajes cada mes? (negocio)
SELECT data_year AS anio, data_month AS mes, sum(total_amount) / 1e6 AS ingresos_musd
FROM trips_clean GROUP BY ALL ORDER BY ALL;
