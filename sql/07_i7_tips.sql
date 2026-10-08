-- I7 | P7: Que propina dejan los pasajeros que pagan con tarjeta (% de la tarifa)? (propinas)
-- Solo tarjeta: la propina en efectivo no se registra.
SELECT data_year AS anio, data_month AS mes, 100 * avg(tip_amount / fare_amount) AS propina_pct
FROM trips_clean WHERE payment_type = 1 GROUP BY ALL ORDER BY ALL;
