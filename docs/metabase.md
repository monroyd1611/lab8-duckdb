# Tablero en Metabase (Ejercicio 7.4 - 7.5)

Además del tablero estático de matplotlib (`docs/dashboard.png`), los mismos
indicadores se publicaron en **Metabase**, la herramienta incluida en el
ambiente Docker. Evidencia: [`metabase_dashboard.png`](metabase_dashboard.png).

## Cómo se construye

Todo lo hace `scripts/metabase_dashboard.py` por medio de la API de Metabase,
por lo que el tablero se puede reconstruir desde cero:

```bash
docker compose up -d
docker compose exec -e MB_EMAIL=<correo> -e MB_PASSWORD=<clave> lab python scripts/metabase_dashboard.py
# -> Tablero listo: http://localhost:3000/dashboard/<id>
```

1. Crea `data/processed/metabase.duckdb` que contiene **solo vistas** (`sql/00_views.sql`)
   sobre `/workspace/data/raw/**/*.parquet`. Metabase consulta los Parquet directamente; no se copia ningún dato.
2. Si Metabase no está configurado, crea el usuario administrador con `MB_EMAIL`/`MB_PASSWORD`.
3. Registra la base en Metabase con el driver DuckDB en modo **solo lectura**
   (un archivo `.duckdb` admite un solo proceso escritor).
4. Crea o actualiza una pregunta SQL nativa por indicador y arma el tablero.
   Es idempotente: al volver a ejecutarlo actualiza las mismas preguntas.

El script corre dentro del contenedor `lab` porque ahí la ruta de los datos
(`/workspace/data`) y la versión de DuckDB (1.5.5) coinciden con las del
contenedor de Metabase y su driver.

## Preguntas del tablero

Cada pregunta usa el texto de su archivo `sql/07_*.sql`. Solo se envuelve en un
`SELECT` externo cuando hace falta convertir el año, el día o la zona a texto
para que Metabase los trate como series o categorías.

| Tarjeta | Consulta | Visualización |
|---------|----------|---------------|
| KPI Viajes válidos / Ingresos / Tarifa media / Pago con tarjeta | `07_kpi.sql` | número |
| I1 Viajes por mes | `07_i1_monthly_trips.sql` | líneas por año |
| I2 Ingresos por mes | `07_i2_revenue.sql` | líneas por año |
| I3 Tarifa media por año y taxi | `07_i3_fare_distance.sql` | barras agrupadas |
| I4 Demanda por día y hora | `07_i4_heatmap.sql` | líneas por día (Metabase no tiene mapa de calor) |
| I5 Participación del taxi verde | `07_i5_green_share.sql` | líneas por año |
| I6 Medio de pago por año | `07_i6_payment_mix.sql` | barras apiladas |
| I7 Propina con tarjeta | `07_i7_tips.sql` | líneas por año |
| I8 Velocidad media por hora | `07_i8_speed.sql` | líneas por año |
| I9 Viajes con cargo CBD | `07_i9_cbd_fee.sql` | líneas por año |
| I10 Top 10 zonas | `07_i10_top_zones.sql` | barras |

Cada tarjeta tarda entre 2 y 6 segundos sobre 113.6 M de viajes (2024-2026),
leyendo los Parquet a través de las vistas. Los valores coinciden con los del
tablero de matplotlib (113.6 M viajes, US$ 3.30 mil M, tarifa media US$ 20.23,
70.4 % con tarjeta).