-- Q3 perfil horario: viajes y propina media por hora y medio de pago.
SELECT hour(pickup) AS hora, payment_type, count(*) AS viajes, avg(tip_amount) AS propina_media
FROM {SRC} GROUP BY ALL ORDER BY ALL;
