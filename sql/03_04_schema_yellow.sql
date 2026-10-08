-- Objetivo: columnas y tipos de los archivos yellow (3.3, 3.4).
-- Fuente: data/raw/yellow/*/*.parquet
DESCRIBE SELECT * FROM read_parquet('{RAW}/yellow/*/*.parquet', union_by_name = true);
