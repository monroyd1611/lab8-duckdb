#!/usr/bin/env python3
"""Verifica que los archivos Parquet descargados esten completos.

Para cada archivo en data/raw/<tipo>/<anio>/ comprueba con DuckDB que:
  - el footer de Parquet se puede leer (el archivo no esta truncado);
  - el conteo de filas coincide con los metadatos;
y para cada tipo/anio compara contra los meses que la TLC publica
(consulta HEAD al servidor). Devuelve codigo 1 si falta algo.

Uso:
    python scripts/verify_data.py
    python scripts/verify_data.py --anios 2026 2025
"""

import argparse
import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).parent))
from download_data import ANIOS, DIR_DESTINO, TIPOS_TAXI, construir_url, esta_publicado, ruta_destino


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica la descarga.")
    parser.add_argument("--anios", type=int, nargs="+", default=list(ANIOS))
    anios = parser.parse_args().anios

    con = duckdb.connect()
    problemas = 0
    print(f"{'tipo':7}{'anio':6}{'esperados':>10}{'locales':>9}{'filas':>14}  estado")
    for anio in anios:
        for tipo in TIPOS_TAXI:
            esperados = [m for m in range(1, 13) if esta_publicado(construir_url(tipo, anio, m))]
            locales = [m for m in esperados if ruta_destino(tipo, anio, m).exists()]
            filas = 0
            estado = "OK"
            for m in locales:
                ruta = str(ruta_destino(tipo, anio, m))
                try:
                    meta = con.execute(
                        "SELECT num_rows FROM parquet_file_metadata(?)", [ruta]
                    ).fetchone()[0]
                    real = con.execute("SELECT count(*) FROM read_parquet(?)", [ruta]).fetchone()[0]
                except duckdb.Error as error:
                    estado = f"CORRUPTO {ruta.rsplit('/', 1)[-1]}: {error}"
                    problemas += 1
                    break
                if meta != real:
                    estado = f"FILAS DISTINTAS {ruta}"
                    problemas += 1
                    break
                filas += real
            if len(locales) != len(esperados):
                faltan = sorted(set(esperados) - set(locales))
                estado = f"FALTAN meses {faltan}"
                problemas += 1
            print(f"{tipo:7}{anio:<6}{len(esperados):>10}{len(locales):>9}{filas:>14,}  {estado}")

    sobrantes = list(DIR_DESTINO.rglob("*.part"))
    if sobrantes:
        print(f"Archivos temporales sin terminar: {sobrantes}")
        problemas += 1
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
