-- Pregunta: a que horas del dia se concentra la demanda de cada taxi?
-- Fuente: trips_clean.
SELECT taxi, hour(pickup) AS hora, count(*) AS viajes,
       round(100.0 * count(*) / sum(count(*)) OVER (PARTITION BY taxi), 2) AS pct_del_taxi
FROM trips_clean GROUP BY taxi, hour(pickup) ORDER BY taxi, hora;
