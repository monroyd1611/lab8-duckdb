-- Pregunta: cambia la demanda entre dias de semana y fines de semana?
-- Fuente: trips_clean. isodow: 1 = lunes ... 7 = domingo.
SELECT taxi, isodow(pickup) AS dia_semana, count(*) AS viajes,
       round(avg(fare_amount), 2) AS tarifa_media
FROM trips_clean GROUP BY ALL ORDER BY taxi, dia_semana;
