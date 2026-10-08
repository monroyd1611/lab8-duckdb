# Ejercicio 1 - Preparacion del ambiente

## Proposito de cada directorio

| Directorio | Proposito |
|------------|-----------|
| `data/raw/` | Parquet originales de la TLC, tal como se descargan (`<tipo>/<anio>/`). Nunca se modifican. Fuera de Git. |
| `data/processed/` | Derivados regenerables (base `.duckdb` materializada, CSV/PNG de resultados pesados). Fuera de Git. |
| `notebooks/` | Analisis interactivo y narrativa (exploracion, EDA, benchmark, tablero). |
| `scripts/` | Codigo reutilizable y ejecutable por linea de comandos (descarga, verificacion, benchmark). |
| `sql/` | Consultas SQL versionadas, una por archivo, con su objetivo documentado. |
| `docs/` | Documentacion y respuestas conceptuales del laboratorio. |
| `Dockerfile` / `docker-compose.yml` | Ambiente de analisis (JupyterLab + librerias fijadas) y servicios. |
| `metabase.Dockerfile` | Metabase con el driver de DuckDB. |

## Verificacion de servicios y herramientas (1.3 y 1.4)

Servicios definidos en `docker-compose.yml`: `lab` (JupyterLab, puerto 8888) y
`metabase` (puerto 3000). Herramientas disponibles en `lab` (ver
`requirements.txt`): Python 3.11, DuckDB, JupyterLab, pandas, PyArrow,
matplotlib y requests; `curl` a nivel de sistema. En `metabase`: Metabase
v0.63.19 + driver DuckDB 1.5.5.0 sobre Java 21.

Verificacion realizada (Docker Desktop 29.8.2, Compose v5.5.1, macOS arm64):

```text
$ docker compose up --build -d
$ docker compose ps
SERVICE    STATUS   PORTS
lab        Up       127.0.0.1:8888->8888/tcp
metabase   Up       127.0.0.1:3000->3000/tcp
$ curl http://127.0.0.1:8888/api         -> 200
$ curl http://127.0.0.1:3000/api/health  -> {"status":"ok"}
```

Dentro de `lab`: Python 3.11.14, duckdb 1.5.5, jupyterlab 4.6.4, pandas 3.0.6,
pyarrow 25.0.1, matplotlib 3.11.2, requests 2.34.2. Desde el contenedor se
ejecutaron `download_data.py` (0 descargados, 64 existentes), `verify_data.py`
(todo OK) y los notebooks 03, 05 y 07 con `jupyter nbconvert --execute`.

Incidencia: la primera construccion fallo en `pip install` por un error de red
transitorio; repetir `docker compose up --build -d` lo resolvio.

Durante el desarrollo tambien se uso un entorno virtual local con las mismas
librerias; los archivos Docker no fueron modificados.

## 1.6 Por que importa un ambiente reproducible

Un analisis de datos es un resultado que depende del codigo *y* de las versiones
de las librerias, del sistema y de la ruta de los datos. Con versiones fijadas y
un contenedor, otra persona (o uno mismo meses despues) obtiene los mismos
resultados con un solo comando; se evitan errores del tipo "en mi maquina
funciona"; los cambios de comportamiento entre versiones (p. ej. DuckDB y el
driver de Metabase deben coincidir) se vuelven explicitos y la revision y
calificacion del trabajo pueden repetirse tal cual.
