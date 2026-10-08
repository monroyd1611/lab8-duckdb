-- Objetivo: filas por archivo leyendo solo los metadatos del footer (3.2).
-- Fuente: todos los Parquet de yellow y green.
SELECT regexp_extract(file_name, '([a-z]+)_tripdata_(\d{4}-\d{2})', 1) AS taxi,
       regexp_extract(file_name, '_(\d{4}-\d{2})', 1) AS mes,
       num_rows, num_row_groups
FROM parquet_file_metadata('{RAW}/*/{ANIO}/*.parquet')
ORDER BY taxi, mes;
