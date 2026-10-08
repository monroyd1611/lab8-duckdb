# Ejercicio 9 - Discusión

**9.1 Características de DuckDB más útiles.** Consultar Parquet con `read_parquet('glob', union_by_name=true)` sin cargar nada;
SQL completo (ventanas, `QUALIFY`, `GROUP BY ALL`, `quantile_cont`); ejecución columnar y paralela (113 M de filas en 1-3 s en una laptop);
`DESCRIBE`, `parquet_file_metadata` y `glob` para inspeccionar archivos; integración directa con pandas/matplotlib; y que corre embebido, sin servidor.

**9.2 Parquet directo.** *Ventajas:* sin etapa de carga ni duplicación en disco, los archivos nuevos aparecen solos, lectura de solo las columnas necesarias
y salto de row groups con filtros. *Limitaciones:* cada consulta repite lectura y limpieza (7-8x más lento que la tabla en agregaciones, ~37x en filtros selectivos);
el esquema puede variar entre archivos (aquí `cbd_congestion_fee` aparece en 2025 y rompió la vista al consultar solo 2024); no hay índices ni actualizaciones.

**9.3 Tablas materializadas.** *Ventajas:* consultas 2-37x más rápidas, datos ya limpios y tipados, resultados consistentes entre consultas, y soporte de joins/transacciones.
*Limitaciones:* costo de construcción (15 s para 113 M de filas), ~1 GB de disco por año, hay que reconstruirla o actualizarla al llegar archivos nuevos
y un archivo `.duckdb` admite un solo proceso escritor.

**9.4 Frente a pandas.** Pandas carga todo en memoria: 113 M de filas x ~25 columnas exceden la RAM de una laptop típica, mientras que DuckDB procesa por bloques,
usa todos los núcleos, solo lee las columnas necesarias y puede hacerlo sin cargar nada. Además, el análisis queda en SQL declarativo y reutilizable.
Pandas sigue siendo útil para el último paso (graficar resultados agregados pequeños), que es como se usó aquí.

**9.5 Incorporar nuevos datos con cambios mínimos.** Estructura `data/raw/<tipo>/<anio>/`, descarga idempotente parametrizada por año, vistas con glob y `union_by_name`,
esquema unificado `trips`, limpieza centralizada en `trips_clean` y columnas `data_year/data_month` derivadas del nombre del archivo. Agregar 2025 solo requirió descargar archivos.

**9.6 Qué automatizar en producción.** Descarga programada (cron/Airflow) con alertas cuando falte un mes publicado; validación de esquema y de calidad al ingreso
(detectar columnas nuevas, fechas imposibles, caída de volumen); conversión/compactación a Parquet particionado derivado; reconstrucción incremental de tablas;
regeneración del tablero y pruebas de las consultas; control de versiones de datos y monitoreo.

**9.7 Decisiones para la reproducibilidad.** Docker con versiones fijadas; datos fuera de Git con `.gitignore`; scripts parametrizados y verificables (`verify_data.py`);
SQL en archivos versionados, no incrustado en notebooks; rutas relativas vía `labutil.py`; notebooks ejecutados de principio a fin con salidas; commits pequeños;
benchmark y tablero como scripts reproducibles; resultados en `docs/`.

**9.8 Lo que no sería evidente con datos pequeños.** Que la calidad se mide a escala (un 5% de registros inválidos son millones de filas y fechas de 2001 en archivos de 2026);
que el esquema cambia entre años; que las medias engañan con distribuciones sesgadas; que la estrategia de acceso importa (segundos vs. décimas) y que la caché del sistema
influye en las mediciones; que 100 M de filas ya no caben cómodamente en pandas; y que un cambio de captura (el 25% de `payment_type = 0`) puede alterar silenciosamente cualquier indicador.