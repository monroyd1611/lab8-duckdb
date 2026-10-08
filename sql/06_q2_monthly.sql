-- Q2 serie mensual: viajes por anio, mes y taxi.
SELECT data_year, data_month, taxi, count(*) AS viajes
FROM {SRC} GROUP BY ALL ORDER BY ALL;
