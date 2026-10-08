-- Vistas base sobre los archivos Parquet (no copian datos).
-- Los globs incluyen todos los anios descargados: al bajar un anio nuevo
-- aparece automaticamente, sin modificar ninguna consulta.

CREATE OR REPLACE VIEW yellow_raw AS
SELECT * FROM read_parquet('{RAW}/yellow/*/*.parquet', union_by_name = true, filename = true);

CREATE OR REPLACE VIEW green_raw AS
SELECT * FROM read_parquet('{RAW}/green/*/*.parquet', union_by_name = true, filename = true);

-- Esquema comun de yellow + green. data_year/data_month vienen del nombre del
-- archivo (mes de publicacion), no del timestamp, que puede estar corrupto.
CREATE OR REPLACE VIEW trips AS
SELECT 'yellow' AS taxi, VendorID AS vendor_id,
       tpep_pickup_datetime AS pickup, tpep_dropoff_datetime AS dropoff,
       CAST(passenger_count AS INTEGER) AS passenger_count, trip_distance,
       CAST(RatecodeID AS INTEGER) AS ratecode_id, store_and_fwd_flag,
       PULocationID AS pu_location, DOLocationID AS do_location,
       CAST(payment_type AS INTEGER) AS payment_type,
       fare_amount, extra, mta_tax, tip_amount, tolls_amount,
       improvement_surcharge, total_amount, congestion_surcharge,
       Airport_fee AS airport_fee, cbd_congestion_fee,
       CAST(NULL AS INTEGER) AS trip_type,
       CAST(regexp_extract(filename, '_(\d{4})-(\d{2})\.parquet$', 1) AS INTEGER) AS data_year,
       CAST(regexp_extract(filename, '_(\d{4})-(\d{2})\.parquet$', 2) AS INTEGER) AS data_month
FROM yellow_raw
UNION ALL BY NAME
SELECT 'green' AS taxi, VendorID AS vendor_id,
       lpep_pickup_datetime AS pickup, lpep_dropoff_datetime AS dropoff,
       CAST(passenger_count AS INTEGER) AS passenger_count, trip_distance,
       CAST(RatecodeID AS INTEGER) AS ratecode_id, store_and_fwd_flag,
       PULocationID AS pu_location, DOLocationID AS do_location,
       CAST(payment_type AS INTEGER) AS payment_type,
       fare_amount, extra, mta_tax, tip_amount, tolls_amount,
       improvement_surcharge, total_amount, congestion_surcharge,
       cbd_congestion_fee, CAST(trip_type AS INTEGER) AS trip_type,
       CAST(regexp_extract(filename, '_(\d{4})-(\d{2})\.parquet$', 1) AS INTEGER) AS data_year,
       CAST(regexp_extract(filename, '_(\d{4})-(\d{2})\.parquet$', 2) AS INTEGER) AS data_month
FROM green_raw;

-- Viajes validos segun las reglas de calidad definidas en el Ejercicio 3:
-- el viaje ocurre en el mes del archivo, dura entre 0 y 6 h, recorre entre
-- 0 y 100 millas y tiene tarifa y total positivos.
CREATE OR REPLACE VIEW trips_clean AS
SELECT * FROM trips
WHERE year(pickup) = data_year AND month(pickup) = data_month
  AND dropoff > pickup AND dropoff - pickup < INTERVAL 6 HOUR
  AND trip_distance > 0 AND trip_distance < 100
  AND fare_amount > 0 AND total_amount > 0 AND total_amount < 1000;
