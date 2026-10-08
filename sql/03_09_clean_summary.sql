-- Objetivo: cuantificar el efecto del filtro trips_clean (decision de 3.6).
-- Fuente: vistas trips y trips_clean.
SELECT t.taxi, t.total, c.validos, t.total - c.validos AS descartados,
       round(100.0 * (t.total - c.validos) / t.total, 2) AS pct_descartado
FROM (SELECT taxi, count(*) total FROM trips GROUP BY taxi) t
JOIN (SELECT taxi, count(*) validos FROM trips_clean GROUP BY taxi) c USING (taxi);
