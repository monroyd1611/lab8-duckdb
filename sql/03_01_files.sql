-- Objetivo: contar y listar los archivos Parquet disponibles (3.1).
-- Fuente: data/raw/*/*/*.parquet
SELECT regexp_extract(file, '/(yellow|green)/', 1) AS taxi, count(*) AS archivos
FROM glob('{RAW}/*/{ANIO}/*.parquet') AS t(file)
GROUP BY ALL ORDER BY taxi;
