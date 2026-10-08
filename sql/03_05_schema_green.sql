-- Objetivo: columnas y tipos de los archivos green (3.3, 3.4).
-- Fuente: data/raw/green/*/*.parquet
DESCRIBE SELECT * FROM read_parquet('{RAW}/green/{ANIO}/*.parquet', union_by_name = true);
