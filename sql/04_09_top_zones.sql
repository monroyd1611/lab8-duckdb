-- Pregunta: que zonas concentran mas recogidas?
-- Fuente: trips_clean. Se usan los IDs de zona de la TLC (no se descarga el catalogo).
SELECT taxi, pu_location AS zona, count(*) AS viajes,
       round(100.0 * count(*) / sum(count(*)) OVER (PARTITION BY taxi), 2) AS pct
FROM trips_clean GROUP BY taxi, pu_location QUALIFY row_number() OVER (PARTITION BY taxi ORDER BY viajes DESC) <= 10
ORDER BY taxi, viajes DESC;
