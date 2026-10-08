#!/usr/bin/env python3
"""Crea en Metabase el tablero del Ejercicio 7 usando su API.

Pasos (idempotente, se puede volver a ejecutar):
  1. crea data/processed/metabase.duckdb con las vistas de sql/00_views.sql
     (solo vistas: Metabase consulta los Parquet directamente);
  2. si Metabase no esta configurado, crea el usuario administrador;
  3. registra la base DuckDB en Metabase (modo solo lectura);
  4. crea/actualiza una pregunta SQL por cada consulta sql/07_*.sql;
  5. crea/actualiza el tablero "Lab 8 - Viajes de taxi NYC".

Se ejecuta dentro del contenedor `lab`, que ve los mismos datos que Metabase
(/workspace/data) y la misma version de DuckDB que su driver:

    docker compose exec -e MB_EMAIL=<correo> -e MB_PASSWORD=<clave> \
        lab python scripts/metabase_dashboard.py

MB_EMAIL/MB_PASSWORD son las credenciales del administrador local de Metabase
(si Metabase aun no se configuro, el script lo crea con ellas).
"""

import os
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))
import labutil as lu

MB_URL = os.environ.get("MB_URL", "http://metabase:3000")
MB_EMAIL = os.environ["MB_EMAIL"]
MB_PASSWORD = os.environ["MB_PASSWORD"]
DB_FILE = lu.PROCESSED / "metabase.duckdb"
DB_NAME = "Lab 8 DuckDB"
TABLERO = "Lab 8 - Viajes de taxi NYC"
MARCA = "[lab8-auto] "  # prefijo en la descripcion para reconocer lo creado por el script


def sql_de(nombre: str) -> str:
    return lu.sql_text(f"{nombre}.sql").strip().rstrip(";")


def por_anio(nombre: str, cols: str) -> str:
    """Envuelve la consulta para que el anio sea texto (serie por anio en Metabase)."""
    return f"SELECT CAST(anio AS VARCHAR) AS anio, {cols}\nFROM (\n{sql_de(nombre)}\n) q"


KPI = sql_de("07_kpi")
DIAS = "CASE dia WHEN 1 THEN '1 Lun' WHEN 2 THEN '2 Mar' WHEN 3 THEN '3 Mie' WHEN 4 THEN '4 Jue' " \
       "WHEN 5 THEN '5 Vie' WHEN 6 THEN '6 Sab' ELSE '7 Dom' END"
USD = {"number_style": "currency", "currency": "USD"}


def linea(dim, serie, metrica, titulo_y):
    return {"graph.dimensions": [dim, serie], "graph.metrics": [metrica],
            "graph.y_axis.title_text": titulo_y, "graph.show_values": False}


# (nombre, descripcion, sql, display, visualization_settings, size_x, size_y)
TARJETAS = [
    ("KPI Viajes validos", "Total de viajes en trips_clean.", f"SELECT viajes FROM ({KPI}) q", "scalar",
     {"scalar.compact_primary_number": True}, 6, 3),
    ("KPI Ingresos", "Suma de total_amount (USD).", f"SELECT ingresos FROM ({KPI}) q", "scalar",
     {"scalar.compact_primary_number": True, "column_settings": {'["name","ingresos"]': USD}}, 6, 3),
    ("KPI Tarifa media", "Promedio de fare_amount (USD).", f"SELECT tarifa_media FROM ({KPI}) q", "scalar",
     {"column_settings": {'["name","tarifa_media"]': {**USD, "decimals": 2}}}, 6, 3),
    ("KPI Pago con tarjeta", "% de viajes con payment_type = 1.", f"SELECT pct_tarjeta FROM ({KPI}) q", "scalar",
     {"column_settings": {'["name","pct_tarjeta"]': {"suffix": " %", "decimals": 1}}}, 6, 3),
    ("I1 Viajes por mes", "P1: cuantos viajes hay por mes y como cambia entre anios? sql/07_i1_monthly_trips.sql",
     por_anio("07_i1_monthly_trips", "mes, viajes"), "line", linea("mes", "anio", "viajes", "viajes"), 12, 6),
    ("I2 Ingresos por mes (M USD)", "P2: cuanto ingreso generan los viajes cada mes? sql/07_i2_revenue.sql",
     por_anio("07_i2_revenue", "mes, ingresos_musd"), "line", linea("mes", "anio", "ingresos_musd", "M USD"), 12, 6),
    ("I3 Tarifa media por anio y taxi", "P3: precio medio por anio y taxi. sql/07_i3_fare_distance.sql",
     por_anio("07_i3_fare_distance", "taxi, round(tarifa_media, 2) AS tarifa_media"), "bar",
     {"graph.dimensions": ["anio", "taxi"], "graph.metrics": ["tarifa_media"], "graph.show_values": True,
      "series_settings": {"yellow": {"color": "#E8B400"}, "green": {"color": "#2E8B57"}}}, 12, 6),
    ("I4 Demanda por dia y hora", "P4: en que dia y hora se concentra la demanda? sql/07_i4_heatmap.sql",
     f"SELECT {DIAS} AS dia, hora, viajes FROM (\n{sql_de('07_i4_heatmap')}\n) q", "line",
     linea("hora", "dia", "viajes", "viajes"), 12, 6),
    ("I5 Participacion del taxi verde (%)", "P5: % de viajes del taxi verde. sql/07_i5_green_share.sql",
     por_anio("07_i5_green_share", "mes, pct_verde"), "line", linea("mes", "anio", "pct_verde", "%"), 12, 6),
    ("I6 Medio de pago por anio (%)", "P6: como cambia el medio de pago? sql/07_i6_payment_mix.sql",
     por_anio("07_i6_payment_mix", "medio, round(pct, 1) AS pct"), "bar",
     {"graph.dimensions": ["anio", "medio"], "graph.metrics": ["pct"], "stackable.stack_type": "stacked"}, 12, 6),
    ("I7 Propina con tarjeta (% de la tarifa)", "P7: propina de quienes pagan con tarjeta. sql/07_i7_tips.sql",
     por_anio("07_i7_tips", "mes, propina_pct"), "line", linea("mes", "anio", "propina_pct", "%"), 12, 6),
    ("I8 Velocidad media por hora (mph)", "P8: velocidad promedio durante el dia. sql/07_i8_speed.sql",
     por_anio("07_i8_speed", "hora, velocidad_mph"), "line", linea("hora", "anio", "velocidad_mph", "mph"), 12, 6),
    ("I9 Viajes con cargo de congestion CBD (%)", "P9: % de viajes con cbd_congestion_fee. sql/07_i9_cbd_fee.sql",
     por_anio("07_i9_cbd_fee", "mes, pct_con_cargo"), "line", linea("mes", "anio", "pct_con_cargo", "%"), 12, 6),
    ("I10 Top 10 zonas de recogida", "P10: zonas con mas recogidas (ID de zona TLC). sql/07_i10_top_zones.sql",
     f"SELECT CAST(zona AS VARCHAR) AS zona, viajes FROM (\n{sql_de('07_i10_top_zones')}\n) q", "bar",
     {"graph.dimensions": ["zona"], "graph.metrics": ["viajes"], "graph.x_axis.scale": "ordinal"}, 12, 6),
]


def crear_base_duckdb():
    if DB_FILE.exists():
        print(f"Base ya existe: {DB_FILE}")
        return
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    con = lu.connect(str(DB_FILE))  # solo crea las vistas sobre los Parquet
    con.close()
    print(f"Base creada con vistas sobre Parquet: {DB_FILE}")


class Metabase:
    def __init__(self):
        self.s = requests.Session()

    def api(self, metodo, ruta, **kw):
        r = self.s.request(metodo, f"{MB_URL}/api/{ruta}", timeout=300, **kw)
        if not r.ok:
            raise RuntimeError(f"{metodo} {ruta}: {r.status_code} {r.text[:300]}")
        return r.json() if r.content else None

    def preparar_y_entrar(self):
        props = self.api("GET", "session/properties")
        if not props.get("has-user-setup"):
            self.api("POST", "setup", json={
                "token": props["setup-token"],
                "user": {"email": MB_EMAIL, "password": MB_PASSWORD,
                         "first_name": "Lab8", "last_name": "Admin", "site_name": "Lab 8 DuckDB"},
                "prefs": {"site_name": "Lab 8 DuckDB", "site_locale": "es", "allow_tracking": False},
            })
            print("Metabase configurado (usuario administrador creado)")
        token = self.api("POST", "session", json={"username": MB_EMAIL, "password": MB_PASSWORD})["id"]
        self.s.headers["X-Metabase-Session"] = token
        return token

    def base(self):
        for db in self.api("GET", "database")["data"]:
            if db["name"] == DB_NAME:
                return db["id"]
        db = self.api("POST", "database", json={
            "engine": "duckdb", "name": DB_NAME,
            "details": {"database_file": str(DB_FILE), "read_only": True},
        })
        print(f"Base registrada en Metabase (id {db['id']})")
        return db["id"]

    def tarjetas(self, db_id):
        existentes = {c["name"]: c["id"] for c in self.api("GET", "card", params={"f": "all"})
                      if (c.get("description") or "").startswith(MARCA) and not c.get("archived")}
        ids = []
        for nombre, desc, sql, display, viz, sx, sy in TARJETAS:
            cuerpo = {"name": nombre, "description": MARCA + desc, "display": display,
                      "visualization_settings": viz,
                      "dataset_query": {"type": "native", "database": db_id, "native": {"query": sql}}}
            if nombre in existentes:
                self.api("PUT", f"card/{existentes[nombre]}", json=cuerpo)
                ids.append((existentes[nombre], sx, sy))
            else:
                ids.append((self.api("POST", "card", json=cuerpo)["id"], sx, sy))
            print(f"  pregunta lista: {nombre}")
        return ids

    def tablero(self, tarjetas):
        dash = next((d for d in self.api("GET", "dashboard") if d["name"] == TABLERO and not d.get("archived")), None)
        if dash is None:
            dash = self.api("POST", "dashboard", json={
                "name": TABLERO,
                "description": "Indicadores del Ejercicio 7 calculados con DuckDB sobre los Parquet (vista trips_clean)."})
        fila, col, dashcards = 0, 0, []
        for i, (card_id, sx, sy) in enumerate(tarjetas):
            if col + sx > 24:
                fila, col = fila + alto, 0
            dashcards.append({"id": -(i + 1), "card_id": card_id, "row": fila, "col": col,
                              "size_x": sx, "size_y": sy, "parameter_mappings": [],
                              "visualization_settings": {}})
            alto = sy
            col += sx
        self.api("PUT", f"dashboard/{dash['id']}", json={"dashcards": dashcards})
        return dash["id"]


def main():
    crear_base_duckdb()
    mb = Metabase()
    mb.preparar_y_entrar()
    db_id = mb.base()
    dash_id = mb.tablero(mb.tarjetas(db_id))
    print(f"Tablero listo: http://localhost:3000/dashboard/{dash_id}")


if __name__ == "__main__":
    main()
