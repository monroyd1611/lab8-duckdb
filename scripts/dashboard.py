#!/usr/bin/env python3
"""Tablero de indicadores (matplotlib) sobre trips_clean.

Ejecuta las consultas sql/07_*.sql, dibuja 4 KPIs y 10 indicadores en una sola
figura y la guarda en docs/dashboard.png. Se adapta a los anios presentes.

Uso:  python scripts/dashboard.py
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import labutil as lu

SALIDA = lu.ROOT / "docs" / "dashboard.png"
AZUL = "#1f4e79"
PALETA_ANIOS = ["#9ecae1", "#4292c6", "#08306b", "#d94801"]
MESES = list("EFMAMJJASOND")
DIAS = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]


def estilo(ax, titulo, sub=None):
    ax.set_title(titulo, loc="left", fontsize=11, fontweight="bold", pad=18)
    if sub:
        ax.text(0, 1.015, sub, transform=ax.transAxes, fontsize=8, color="#555", va="bottom")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25)


def lineas_por_anio(ax, df, col, anios, ylab):
    for c, a in zip(PALETA_ANIOS, anios):
        g = df[df.anio == a]
        ax.plot(g.mes, g[col], marker="o", ms=3, color=c, label=str(a))
    ax.set_xticks(range(1, 13), MESES)
    ax.set_ylabel(ylab)
    ax.legend(frameon=False, fontsize=8, ncol=len(anios))


def main():
    con = lu.connect()
    d = {n: lu.q(con, f"07_{n}.sql", mostrar_sql=False) for n in
         ["kpi", "i1_monthly_trips", "i2_revenue", "i3_fare_distance", "i4_heatmap", "i5_green_share",
          "i6_payment_mix", "i7_tips", "i8_speed", "i9_cbd_fee", "i10_top_zones"]}
    k = d["kpi"].iloc[0]
    anios = sorted(d["i1_monthly_trips"].anio.unique())

    fig = plt.figure(figsize=(18, 20))
    gs = fig.add_gridspec(5, 3, height_ratios=[0.5, 1, 1, 1, 1], hspace=0.5, wspace=0.22)
    fig.suptitle(f"Tablero de viajes de taxi NYC - {', '.join(map(str, anios))}", fontsize=18,
                 fontweight="bold", x=0.06, ha="left", y=0.925)

    # KPIs
    cards = [("Viajes validos", f"{k.viajes / 1e6:,.1f} M"), ("Ingresos", f"US$ {k.ingresos / 1e9:,.2f} mil M"),
             ("Tarifa media", f"US$ {k.tarifa_media:,.2f}"), ("Pago con tarjeta", f"{k.pct_tarjeta:.1f} %")]
    sub = gs[0, :].subgridspec(1, 4, wspace=0.08)
    for i, (t, v) in enumerate(cards):
        ax = fig.add_subplot(sub[i]); ax.axis("off")
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes, color="#eef3f8"))
        ax.text(0.5, 0.64, v, ha="center", va="center", fontsize=20, fontweight="bold", color=AZUL)
        ax.text(0.5, 0.2, t, ha="center", va="center", fontsize=11, color="#444")

    # I1 viajes por mes
    ax = fig.add_subplot(gs[1, 0]); estilo(ax, "I1 Viajes por mes", "demanda, millones")
    df = d["i1_monthly_trips"].assign(v=lambda x: x.viajes / 1e6); lineas_por_anio(ax, df, "v", anios, "millones")
    # I2 ingresos
    ax = fig.add_subplot(gs[1, 1]); estilo(ax, "I2 Ingresos por mes", "total_amount, millones de USD")
    lineas_por_anio(ax, d["i2_revenue"], "ingresos_musd", anios, "M USD")
    # I3 tarifa media
    ax = fig.add_subplot(gs[1, 2]); estilo(ax, "I3 Tarifa media por anio y taxi", "USD")
    t3 = d["i3_fare_distance"]; w = 0.8 / 2
    for j, (taxi, c) in enumerate([("yellow", "#E8B400"), ("green", "#2E8B57")]):
        g = t3[t3.taxi == taxi]
        pos = [anios.index(a) + (j - 0.5) * w for a in g.anio]
        b = ax.bar(pos, g.tarifa_media, w, color=c, label=taxi)
        ax.bar_label(b, fmt="%.1f", fontsize=8)
    ax.set_xticks(range(len(anios)), anios); ax.legend(frameon=False, fontsize=8)
    # I4 heatmap
    ax = fig.add_subplot(gs[2, 0]); estilo(ax, "I4 Demanda por dia y hora", "viajes (miles) - todos los anios")
    m = d["i4_heatmap"].pivot(index="dia", columns="hora", values="viajes").values / 1e3
    im = ax.imshow(m, aspect="auto", cmap="Blues"); ax.set_yticks(range(7), DIAS)
    ax.set_xticks(range(0, 24, 3)); ax.grid(False); fig.colorbar(im, ax=ax, fraction=0.04)
    # I5 participacion verde
    ax = fig.add_subplot(gs[2, 1]); estilo(ax, "I5 Participacion del taxi verde", "% de los viajes")
    lineas_por_anio(ax, d["i5_green_share"], "pct_verde", anios, "%")
    # I6 medios de pago
    ax = fig.add_subplot(gs[2, 2]); estilo(ax, "I6 Medio de pago por anio", "% de los viajes")
    p = d["i6_payment_mix"].pivot(index="anio", columns="medio", values="pct").fillna(0)
    base = np.zeros(len(p))
    for col, c in zip([c for c in ["tarjeta", "efectivo", "flex/app", "otro"] if c in p], ["#1f4e79", "#7fb2d9", "#d94801", "#bbb"]):
        ax.bar(p.index.astype(str), p[col], bottom=base, color=c, label=col); base += p[col].values
    ax.legend(frameon=False, fontsize=8, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.06))
    # I7 propinas
    ax = fig.add_subplot(gs[3, 0]); estilo(ax, "I7 Propina con tarjeta", "% de la tarifa")
    lineas_por_anio(ax, d["i7_tips"], "propina_pct", anios, "%")
    # I8 velocidad
    ax = fig.add_subplot(gs[3, 1]); estilo(ax, "I8 Velocidad media por hora", "mph (millas / horas)")
    for c, a in zip(PALETA_ANIOS, anios):
        g = d["i8_speed"][d["i8_speed"].anio == a]; ax.plot(g.hora, g.velocidad_mph, color=c, label=str(a))
    ax.set_xlabel("hora de recogida"); ax.legend(frameon=False, fontsize=8, ncol=len(anios))
    # I9 cbd fee
    ax = fig.add_subplot(gs[3, 2]); estilo(ax, "I9 Viajes con cargo de congestion (CBD)", "% de los viajes del mes")
    lineas_por_anio(ax, d["i9_cbd_fee"], "pct_con_cargo", anios, "%")
    # I10 zonas
    ax = fig.add_subplot(gs[4, :2]); estilo(ax, "I10 Top 10 zonas de recogida", "viajes (millones) - ID de zona TLC")
    z = d["i10_top_zones"]; ax.bar(z.zona.astype(str), z.viajes / 1e6, color=AZUL)
    ax.set_xlabel("PULocationID")
    ax = fig.add_subplot(gs[4, 2]); ax.axis("off")
    ax.text(0, 1, "Notas\n\nDatos: NYC TLC Trip Record Data\n(yellow + green).\nFuente de calculo: DuckDB sobre Parquet\n(vista trips_clean).\nConsultas: sql/07_*.sql",
            va="top", fontsize=10, color="#444")

    SALIDA.parent.mkdir(exist_ok=True)
    fig.savefig(SALIDA, dpi=110, bbox_inches="tight", facecolor="white")
    print(f"Tablero guardado en {SALIDA}")


if __name__ == "__main__":
    main()
