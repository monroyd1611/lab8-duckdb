-- Pregunta: cual es la forma de la distribucion de distancias (histograma)?
-- Fuente: trips_clean. Cajas de 1 milla hasta 20; el resto en 20+.
SELECT taxi, least(floor(trip_distance), 20)::INT AS milla, count(*) AS viajes
FROM trips_clean GROUP BY ALL ORDER BY taxi, milla;
