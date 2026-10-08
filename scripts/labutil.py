"""Utilidades compartidas por los notebooks y scripts del laboratorio.

- `connect()` abre DuckDB y crea las vistas de sql/00_views.sql sobre los
  Parquet (las vistas no copian datos: se resuelven al consultar).
- `sql_text()` / `q()` leen una consulta de sql/ (sustituyendo {RAW}) y la
  ejecutan, imprimiendo el SQL para que quede documentado en el notebook.
"""

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
SQL_DIR = ROOT / "sql"

# Carpeta de anio a leer: "*" = todos los anios descargados; "2026" = solo ese anio.
ANIO = "*"


def sql_text(nombre: str, **extra) -> str:
    texto = (SQL_DIR / nombre).read_text() if nombre.endswith(".sql") else nombre
    valores = {"RAW": str(RAW), "ANIO": ANIO, **extra}
    for clave, valor in valores.items():
        texto = texto.replace("{" + clave + "}", str(valor))
    return texto


def _globs(tipo: str, anio) -> str:
    """Lista de globs SQL para un tipo de taxi. `anio`: "*", "2026" o lista de patrones."""
    if isinstance(anio, (list, tuple)):
        patrones = [f"{RAW}/{tipo}/{a}/*.parquet" for a in anio]
    else:
        patrones = [f"{RAW}/{tipo}/{anio}/*.parquet"]
    return "[" + ", ".join(f"'{p}'" for p in patrones) + "]"


def connect(database: str = ":memory:", read_only: bool = False, views: bool = True,
            anio="*", yellow=None, green=None):
    """Abre DuckDB con las vistas sobre los Parquet.

    `anio` limita a un anio ("2026"), una lista de anios o "*" (todos). Para
    control fino, `yellow`/`green` aceptan listas de globs completos.
    """
    global ANIO
    ANIO = str(anio) if not isinstance(anio, (list, tuple)) else "*"
    con = duckdb.connect(database, read_only=read_only)
    if views:
        lit = lambda l: "[" + ", ".join(f"'{p}'" for p in l) + "]"
        con.execute(sql_text(
            "00_views.sql",
            YELLOW_FILES=lit(yellow) if yellow else _globs("yellow", anio),
            GREEN_FILES=lit(green) if green else _globs("green", anio),
        ))
    return con


def q(con, nombre: str, mostrar_sql: bool = True, **extra):
    """Ejecuta un archivo .sql (o texto SQL) y devuelve un DataFrame."""
    texto = sql_text(nombre, **extra)
    if mostrar_sql:
        print(f"-- {nombre if nombre.endswith('.sql') else 'consulta'}\n{texto.strip()}\n")
    return con.execute(texto).df()
