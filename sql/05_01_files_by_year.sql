-- Objetivo: confirmar que los archivos de 2024 y 2026 conviven en el glob (5.5, 5.6).
-- Fuente: data/raw/*/*/*.parquet
SELECT regexp_extract(file, '/(yellow|green)/', 1) AS taxi,
       regexp_extract(file, '/(\d{4})/', 1) AS anio, count(*) AS archivos
FROM glob('{RAW}/*/{ANIO}/*.parquet') AS t(file) GROUP BY ALL ORDER BY taxi, anio;
