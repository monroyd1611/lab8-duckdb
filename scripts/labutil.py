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


def connect(database: str = ":memory:", read_only: bool = False, views: bool = True,
            anio: str = "*"):
    """`anio` limita las vistas y consultas a un anio ("2026"); "*" lee todos."""
    global ANIO
    ANIO = str(anio)
    con = duckdb.connect(database, read_only=read_only)
    if views:
        con.execute(sql_text("00_views.sql"))
    return con


def q(con, nombre: str, mostrar_sql: bool = True, **extra):
    """Ejecuta un archivo .sql (o texto SQL) y devuelve un DataFrame."""
    texto = sql_text(nombre, **extra)
    if mostrar_sql:
        print(f"-- {nombre if nombre.endswith('.sql') else 'consulta'}\n{texto.strip()}\n")
    return con.execute(texto).df()
