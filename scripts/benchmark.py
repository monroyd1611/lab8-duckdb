#!/usr/bin/env python3
"""Benchmark: consultar Parquet directamente vs. una tabla materializada en DuckDB.

Para cada alcance de datos (1 mes, 1 anio, 2 anios, ... segun lo descargado):
  1. define `src_parquet` = vista trips_clean sobre los Parquet del alcance;
  2. materializa `tbl_<alcance>` en data/processed/lab8.duckdb (CREATE TABLE AS),
     midiendo el tiempo de creacion;
  3. ejecuta las consultas sql/06_q*.sql sobre ambos orígenes, REPETICIONES veces.
Guarda los resultados en docs/benchmark_results.csv.

Uso:
    python scripts/benchmark.py [--repeticiones 5]
"""

import argparse
import csv
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import duckdb

import labutil as lu

DB = lu.PROCESSED / "lab8.duckdb"
SALIDA = lu.ROOT / "docs" / "benchmark_results.csv"


def alcances():
    """Alcances acumulativos: 1 mes, y luego 1, 2, 3... anios (el mas reciente primero)."""
    anios = sorted(p.name for p in (lu.RAW / "yellow").iterdir() if p.is_dir())
    res = {"1 mes (2026-01)": (["2026/*_2026-01.parquet"], ["2026/*_2026-01.parquet"])}
    recientes = sorted(anios, reverse=True)
    for n in range(1, len(recientes) + 1):
        sel = sorted(recientes[:n])
        res[f"{n} anio{'s' if n > 1 else ''} ({'+'.join(sel)})"] = (sel, sel)
    return res


def conectar_alcance(nombre, spec, db):
    yellow, green = spec
    if "mes" in nombre:  # patrones completos por archivo
        y = [f"{lu.RAW}/yellow/{p}".replace("*_2026", "yellow_tripdata_2026") for p in yellow]
        g = [f"{lu.RAW}/green/{p}".replace("*_2026", "green_tripdata_2026") for p in green]
        return lu.connect(db, yellow=y, green=g)
    return lu.connect(db, anio=yellow)


def cronometrar(con, sql, repeticiones):
    tiempos = []
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        con.execute(sql).fetchall()
        tiempos.append(time.perf_counter() - t0)
    return tiempos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeticiones", type=int, default=5)
    reps = ap.parse_args().repeticiones

    DB.parent.mkdir(parents=True, exist_ok=True)
    DB.unlink(missing_ok=True)
    consultas = sorted(lu.SQL_DIR.glob("06_q*.sql"))
    filas = []
    for i, (nombre, spec) in enumerate(alcances().items()):
        con = conectar_alcance(nombre, spec, str(DB))
        tabla = f"tbl_{i}"
        n_filas = con.execute("SELECT count(*) FROM trips_clean").fetchone()[0]
        t0 = time.perf_counter()
        con.execute(f"CREATE TABLE {tabla} AS SELECT * FROM trips_clean")
        t_crear = time.perf_counter() - t0
        con.execute("CHECKPOINT")
        print(f"\n== {nombre}: {n_filas:,} filas; tabla creada en {t_crear:.2f} s")
        filas.append(dict(alcance=nombre, filas=n_filas, consulta="CREATE TABLE", fuente="tabla",
                          primera_s=round(t_crear, 4), mediana_s=round(t_crear, 4), minimo_s=round(t_crear, 4)))
        for archivo in consultas:
            for fuente, src in (("parquet", "trips_clean"), ("tabla", tabla)):
                sql = lu.sql_text(archivo.name, SRC=src)
                t = cronometrar(con, sql, reps)
                print(f"  {archivo.stem:16} {fuente:8} primera={t[0]:.3f}s mediana={statistics.median(t):.3f}s")
                filas.append(dict(alcance=nombre, filas=n_filas, consulta=archivo.stem, fuente=fuente,
                                  primera_s=round(t[0], 4), mediana_s=round(statistics.median(t), 4),
                                  minimo_s=round(min(t), 4)))
        con.close()

    SALIDA.parent.mkdir(exist_ok=True)
    with SALIDA.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    print(f"\nResultados en {SALIDA}  |  tamano de la base: {DB.stat().st_size / 2**20:.0f} MiB")


if __name__ == "__main__":
    main()
