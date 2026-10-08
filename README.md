# Lab 8 - DuckDB

Repositorio base del laboratorio 8 del curso **CC3084 - Data Science**
(Universidad del Valle de Guatemala, Ciclo 2, 2026).

Este es el repositorio **proporcionado por el docente**. Contiene la estructura
del proyecto, el ambiente de ejecucion basado en Docker y un script que descarga
los datos de **2026**. Todo lo demas debe ser construido por cada equipo.

## Trabajo con fork

El laboratorio se desarrolla y se entrega sobre un **fork** de este repositorio.
No se trabaja directamente sobre el repositorio del docente.

1. Realice un fork de este repositorio:
   <https://github.com/menene/duckdb>

2. Clone **su propio fork** (no el del docente):

   ```bash
   git clone https://github.com/<su-usuario>/duckdb.git
   cd duckdb
   ```

3. Opcional, para recibir correcciones publicadas por el docente:

   ```bash
   git remote add upstream https://github.com/menene/duckdb.git
   git fetch upstream
   ```

Realice commits frecuentes y descriptivos: el historial del repositorio es parte
de la evaluacion. **La entrega del laboratorio es la URL de su fork.**

## Estructura

```text
duckdb/
|
+-- data/
|   +-- raw/
|   +-- processed/
|
+-- notebooks/
|
+-- scripts/
|
+-- sql/
|
+-- docs/
|
+-- Dockerfile
+-- metabase.Dockerfile
+-- docker-compose.yml
+-- README.md
```

## Requisitos

- Docker, con Docker Compose
- Git

La primera construccion del ambiente descarga varios cientos de MB y puede
tardar algunos minutos.

Considere el espacio en disco: las imagenes de Docker ocupan unos 3 GB y los
datos de los tres anios del laboratorio superan 1.5 GB, a los que se suma la
base materializada del Ejercicio 6. Se recomienda tener al menos 10 GB libres.

## Datos

El repositorio incluye `scripts/download_data.py`, que descarga los archivos de
2026 publicados por la TLC (`--help` muestra las opciones disponibles). Los
archivos se guardan en `data/raw/<tipo>/<anio>/`.

La TLC publica cada mes con varias semanas de atraso, por lo que los ultimos
meses de 2026 todavia no existen. El script consulta al servidor que meses estan
publicados, de modo que vuelve a ejecutarse sin problema conforme aparezcan
nuevos archivos.

Los datos descargados **no deben incluirse en el repositorio Git**. El archivo
`.gitignore` ya esta configurado para evitarlo.

Fuente de datos: NYC TLC Trip Record Data
<https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page>

Dentro de los contenedores, la carpeta `data/` del proyecto esta montada en
`/workspace/data`. Esa es la ruta que deben usar las herramientas que corren
dentro del ambiente, no la ruta de su computadora.

> **Nota sobre DuckDB:** un archivo `.duckdb` admite un solo proceso con permiso
> de escritura a la vez. Si conecta una herramienta externa a su base de datos,
> use el modo de solo lectura (`read_only`) en esa conexion; de lo contrario los
> demas procesos no podran abrir el archivo.

## Material a entregar

Al finalizar, su fork debe contener:

- el codigo fuente modificado y los scripts de descarga;
- las consultas SQL desarrolladas;
- el notebook o notebooks utilizados;
- la documentacion de las consultas;
- los scripts utilizados para los benchmarks;
- el codigo de los indicadores y visualizaciones;
- el tablero o la evidencia del tablero desarrollado;
- este `README.md`, completado segun la siguiente seccion.

Los archivos de datos descargados **no** deben incluirse.

---

# Documentacion del equipo

Las siguientes secciones deben ser completadas por cada equipo. El README final
debe permitir que una persona que no participo en el desarrollo pueda levantar el
ambiente, descargar los datos, ejecutar el analisis, reproducir los benchmarks y
generar los resultados principales.

## Como levantar el ambiente

Con Docker (recomendado):

```bash
git clone https://github.com/<su-usuario>/duckdb.git && cd duckdb
docker compose up --build -d
docker compose ps            # lab y metabase deben estar "running"
docker compose exec lab python scripts/verify_data.py   # prueba rapida dentro del contenedor
```

| Servicio | URL | Para que sirve |
|----------|-----|----------------|
| `lab` | <http://localhost:8888> | JupyterLab (sin token) con Python, DuckDB, pandas, matplotlib |
| `metabase` | <http://localhost:3000> | Metabase con el driver de DuckDB |

Para detenerlo: `docker compose down`.

Alternativa sin Docker (entorno virtual local):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install duckdb pandas pyarrow matplotlib requests jupyterlab
jupyter lab
```

En este caso las rutas son relativas a la raiz del repositorio (`data/raw/...`);
los notebooks detectan ambos casos automaticamente. Ver
[docs/01_ambiente.md](docs/01_ambiente.md) para el proposito de cada directorio,
las herramientas del ambiente y por que importa la reproducibilidad.

## Como descargar los datos

```bash
python scripts/download_data.py                       # 2024, 2025 y 2026 (por defecto), yellow y green
python scripts/download_data.py --anios 2024 2025 2026
python scripts/download_data.py --taxi green --anios 2025
python scripts/verify_data.py --anios 2024 2025 2026  # comprueba que esta completo
```

Dentro de Docker: `docker compose exec lab python scripts/download_data.py --anios 2024 2025 2026`.
El script es idempotente: no vuelve a descargar archivos existentes. Cambios al
script y criterio de completitud: [docs/02_descarga.md](docs/02_descarga.md).

## Como ejecutar el analisis

Los notebooks (en `notebooks/`, abrir en JupyterLab) estan en orden y ya contienen sus salidas; para regenerarlos use *Run All*.
Todas las consultas estan en `sql/` (`00_views.sql` define `trips` y `trips_clean`); `scripts/labutil.py` las ejecuta.

| Notebook | Ejercicio |
|----------|-----------|
| `03_consultas_parquet.ipynb` | 3 - consultas directas, calidad de datos (alcance 2026) |
| `04_analisis_exploratorio.ipynb` | 4 - EDA (alcance 2026) |
| `05_incorporacion_2024.ipynb` | 5 - incorporacion de 2024 |
| `06_benchmark.ipynb` | 6 - Parquet vs tabla DuckDB |
| `07_indicadores_tablero.ipynb` | 7 - indicadores y tablero |
| `08_analisis_completo.ipynb` | 8 - tres anios y patrones |

Documentos: `docs/01_ambiente.md`, `docs/02_descarga.md`, `docs/09_discusion.md`.

## Como reproducir los benchmarks

```bash
python scripts/benchmark.py --repeticiones 5   # escribe docs/benchmark_results.csv y data/processed/lab8.duckdb
```

Requiere los tres anios descargados (~10 min y ~6 GiB de disco para la base). Analisis en `notebooks/06_benchmark.ipynb`.

## Como generar los resultados principales

```bash
python scripts/dashboard.py   # tablero matplotlib -> docs/dashboard.png
```

El tablero (10 indicadores + 4 KPIs) esta versionado en `docs/dashboard.png`.

Tablero en Metabase (mismos indicadores, consultando los Parquet desde Metabase):

```bash
docker compose exec -e MB_EMAIL=<correo> -e MB_PASSWORD=<clave> lab python scripts/metabase_dashboard.py
```

Abre el enlace que imprime (`http://localhost:3000/dashboard/<id>`). Si Metabase aun
no esta configurado, el script crea el administrador con esas credenciales.
Detalles y evidencia: [docs/metabase.md](docs/metabase.md).

Discusion final (Ejercicio 9): [docs/09_discusion.md](docs/09_discusion.md).
