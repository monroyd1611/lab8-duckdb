-- I1 | P1: Cuantos viajes hay por mes y como cambia entre anios? (demanda)
SELECT data_year AS anio, data_month AS mes, count(*) AS viajes
FROM trips_clean GROUP BY ALL ORDER BY ALL;
