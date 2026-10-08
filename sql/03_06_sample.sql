-- Objetivo: muestra aleatoria de 5 registros de cada taxi (3.5).
-- Fuente: vista trips (Parquet yellow + green).
(SELECT * FROM trips USING SAMPLE 5 ROWS)
UNION ALL BY NAME
(SELECT * FROM trips WHERE taxi = 'green' USING SAMPLE 5 ROWS);
