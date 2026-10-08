-- I6 | P6: Como cambia el medio de pago a traves de los anios? (pagos)
SELECT data_year AS anio,
       CASE payment_type WHEN 1 THEN 'tarjeta' WHEN 2 THEN 'efectivo' WHEN 0 THEN 'flex/app' ELSE 'otro' END AS medio,
       100.0 * count(*) / sum(count(*)) OVER (PARTITION BY data_year) AS pct
FROM trips_clean GROUP BY data_year, 2 ORDER BY 1, 2;
