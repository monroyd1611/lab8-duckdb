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

## Ampliacion a 2024 y 2025 (Ejercicios 5 y 8)

`ANIOS` paso de `(2026,)` a `(2026, 2024)` y luego a `(2026, 2025, 2024)`;
tambien se puede indicar `--anios` por linea de comandos. No se modifico nada mas
del flujo: los archivos se separan por `data/raw/<tipo>/<anio>/`, de modo que los
anios nuevos no tocan los ya descargados (5.2, 8.2) y el criterio "existe y pesa
> 0 bytes" evita volver a descargarlos (5.3).

Hallazgo durante la ampliacion: en la primera corrida de 2024, `yellow 2024-03`
quedo marcado como "no publicado" por un fallo transitorio del `HEAD`. Se corrigio
`esta_publicado()`: ahora reintenta y solo considera "no publicado" una respuesta
403/404. `verify_data.py` detecta este tipo de hueco (compara con el servidor).

Resultado final (`python scripts/verify_data.py --anios 2024 2025 2026`):

| tipo | anio | meses | filas |
|------|------|-------|-------|
| yellow | 2024 | 12/12 | 41,169,720 |
| green  | 2024 | 12/12 | 660,218 |
| yellow | 2025 | 12/12 | 48,722,602 |
| green  | 2025 | 12/12 | 591,375 |
| yellow | 2026 | 8/8 (sep-dic aun no publicados) | 29,703,355 |
| green  | 2026 | 8/8 | 337,114 |

Segunda ejecucion tras agregar 2025: 0 descargados, 64 existentes.
