-- I4 | P4: En que dia y hora se concentra la demanda? (patron semanal)
SELECT isodow(pickup) AS dia, hour(pickup) AS hora, count(*) AS viajes
FROM trips_clean GROUP BY ALL ORDER BY ALL;
