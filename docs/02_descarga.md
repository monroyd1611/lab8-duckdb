# Ejercicio 2 - Sistema de descarga

## Analisis del script base (2.1)

`scripts/download_data.py` tenia el anio 2026 fijo en una constante (`ANIO`) y
en cuatro funciones, por lo que no podia reutilizarse para otros anios. El
resto (reintentos, archivo temporal `.part`, `HEAD` para saber si un mes esta
publicado, omision de archivos existentes) ya funcionaba.

## Cambios realizados (2.6)

1. `ANIO = 2026` -> `ANIOS = (2026,)` (lista de anios por defecto).
2. `construir_nombre`, `construir_url`, `ruta_destino` y `descargar` reciben
   `anio` como parametro.
3. Nueva opcion `--anios` (p. ej. `--anios 2024 2025 2026`); `main` itera anio x tipo.
4. Nuevo `scripts/verify_data.py` para comprobar la completitud.

Los requisitos 2.2-2.4 se cumplen asi: todos los meses 1-12 de yellow y green se
consultan con `HEAD`; se guardan en `data/raw/<tipo>/<anio>/`; si el archivo
existe y pesa > 0 bytes se omite.

## Ejecucion (2.5)

Primera corrida: 16 descargados, 0 existentes, 8 no publicados (sep-dic 2026).
Segunda corrida: 0 descargados, 16 existentes.

## Como se determino que esta completo (2.7)

`python scripts/verify_data.py` hace, por tipo y anio:

- pregunta al servidor (`HEAD`) que meses estan publicados = lo esperado;
- comprueba que cada uno de esos meses existe localmente;
- abre el footer Parquet con DuckDB (un archivo truncado falla) y compara
  `num_rows` de los metadatos con `count(*)`;
- verifica que no queden `.part` sin terminar.

Resultado 2026: yellow 8/8 meses (29,703,355 filas) y green 8/8 (337,114 filas).
