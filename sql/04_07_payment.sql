-- Pregunta: como pagan los pasajeros y cuanta propina dejan segun el medio?
-- Fuente: trips_clean. payment_type: 0 flex, 1 tarjeta, 2 efectivo, 3 sin cargo, 4 disputa, 5 desconocido, 6 anulado.
SELECT taxi,
  CASE payment_type WHEN 0 THEN '0 flex/app' WHEN 1 THEN '1 tarjeta' WHEN 2 THEN '2 efectivo'
       WHEN 3 THEN '3 sin cargo' WHEN 4 THEN '4 disputa' ELSE '5+ otro' END AS medio_pago,
  count(*) AS viajes,
  round(100.0 * count(*) / sum(count(*)) OVER (PARTITION BY taxi), 2) AS pct,
  round(avg(tip_amount), 2) AS propina_media,
  round(100 * avg(tip_amount / fare_amount), 2) AS propina_pct_tarifa
FROM trips_clean GROUP BY 1, 2 ORDER BY taxi, medio_pago;
