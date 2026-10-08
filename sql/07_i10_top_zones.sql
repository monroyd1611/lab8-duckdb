-- I10 | P10: Que zonas concentran las recogidas? (geografia; IDs de zona de la TLC)
SELECT pu_location AS zona, count(*) AS viajes
FROM trips_clean GROUP BY zona ORDER BY viajes DESC LIMIT 10;
