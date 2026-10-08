-- Pregunta: cuantos valores atipicos hay y de que tipo?
-- Fuente: trips (sin limpiar) para medir lo que trips_clean elimina, mas velocidades en trips_clean.
SELECT 'velocidad > 80 mph (tras limpiar)' AS anomalia, count(*) AS viajes
FROM trips_clean WHERE trip_distance / (date_diff('second', pickup, dropoff) / 3600.0) > 80
UNION ALL SELECT 'tarifa > 200 USD (tras limpiar)', count(*) FROM trips_clean WHERE fare_amount > 200
UNION ALL SELECT 'propina > tarifa (tras limpiar)', count(*) FROM trips_clean WHERE tip_amount > fare_amount
UNION ALL SELECT 'pasajeros >= 7 (tras limpiar)', count(*) FROM trips_clean WHERE passenger_count >= 7
UNION ALL SELECT 'duracion < 1 min (tras limpiar)', count(*) FROM trips_clean WHERE dropoff - pickup < INTERVAL 1 MINUTE
UNION ALL SELECT 'recogida en pu_location 264/265 (desconocido)', count(*) FROM trips_clean WHERE pu_location IN (264, 265)
UNION ALL SELECT 'total < tarifa (tras limpiar)', count(*) FROM trips_clean WHERE total_amount < fare_amount;
