"""Figure 3 — southern Europe, hours of relief, population-weighted."""
import json
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATA, FIGURES
FIGURES.mkdir(exist_ok=True)
import sys
LANG = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("en", "it") else "en"
TXT = {
  "en": dict(title="Night-time relief is scarcest where people live",
             cbar="hours of relief — of the 8 coldest hours of the day, how many stay below 20 °C",
             xpp="mean hours of relief per person", xpop="% of population", then="1980s", now="2020s",
             band_then="1980s", band_now="2020s",
             bands=["no relief (0 h)", "under 4 h", "4–8 h", "full 8 h"],
             focus=["Greece", "Italy", "Spain"], names={}, out="fig-001-true-hours-of-relief.png"),
  "it": dict(title="Il sollievo notturno è più scarso proprio dove vive la gente",
             cbar="ore di sollievo — delle 8 ore più fresche del giorno, quante restano sotto i 20 °C",
             xpp="ore medie di sollievo a persona", xpop="% della popolazione", then="1980–1989", now="2020–2025",
             band_then="1980–89", band_now="2020–25",
             bands=["nessun sollievo (0 h)", "meno di 4 h", "4–8 h", "8 h piene"],
             focus=["Grecia", "Italia", "Spagna"],
             names={"Lisbon": "Lisbona", "Barcelona": "Barcellona", "Marseille": "Marsiglia", "Milan": "Milano",
                    "Rome": "Roma", "Naples": "Napoli", "Tunis": "Tunisi", "Algiers": "Algeri",
                    "Athens": "Atene", "Bucharest": "Bucarest"},
             out="fig-001-true-hours-of-relief-it.png"),
}[LANG]
NM = lambda n: TXT["names"].get(n, n)
DEC = lambda v: f"{v:.1f}".replace(".", ",") if LANG == "it" else f"{v:.1f}"
import numpy as np
import xarray as xr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from shapely.geometry import shape

plt.rcParams.update({"font.family": "DejaVu Sans"})

A = xr.open_dataarray(DATA / "seu_relief_1980s.nc")
B = xr.open_dataarray(DATA / "seu_relief_2020s.nc")
OUT = json.load(open(DATA / "frame_outlines.geojson"))
import pandas as pd
# Per-person figures for the lower panels, from the population assigned to each cell
_pop = pd.read_csv(DATA / "population_by_cell.csv")
def _stats(d):
    sel = lambda F: F.sel(latitude=xr.DataArray(d.lat.values), longitude=xr.DataArray(d.lon.values),
                          method="nearest").values
    a, b, w = sel(A), sel(B), d.population.values
    bands = lambda v: [float(w[v < .5].sum() / w.sum() * 100), float(w[(v >= .5) & (v < 4)].sum() / w.sum() * 100),
                       float(w[(v >= 4) & (v < 7.5)].sum() / w.sum() * 100), float(w[v >= 7.5].sum() / w.sum() * 100)]
    return dict(wa=float(np.average(a, weights=w)), wb=float(np.average(b, weights=w)),
                band_a=bands(a), band_b=bands(b))
S = {k: _stats(_pop[_pop.country == k]) for k in ("greece", "italy", "spain")}

BLUE, RED = "#5b8fa8", "#c1440e"
NORTH, WEST, EAST, SOUTH = 47.2, -10.0, 30.0, 34.0

# name, lon, lat, dx, dy, ha, va   — offsets in points, hand-placed to avoid
# collisions and to keep every label inside the axes. Lisbon sits at -9.14,
# less than a degree from the western edge, so its label must run east.
CITIES = [
    ("Lisbon",    -9.14, 38.72,  7, -5, "left",  "top"),
    ("Madrid",    -3.70, 40.42,  6,  4, "left",  "bottom"),
    ("Barcelona",  2.17, 41.39,  6,  4, "left",  "bottom"),
    ("Marseille",  5.37, 43.30, -6,  4, "right", "bottom"),
    ("Milan",      9.19, 45.46,  6,  4, "left",  "bottom"),
    ("Rome",      12.50, 41.90,  6,  4, "left",  "bottom"),
    ("Naples",    14.25, 40.85,  6, -4, "left",  "top"),
    ("Palermo",   13.36, 38.12, -6,  4, "right", "bottom"),
    ("Tunis",     10.18, 36.81, -6, -4, "right", "top"),
    ("Algiers",    3.06, 36.75,  6, -4, "left",  "top"),
    ("Athens",    23.73, 37.98,  6, -4, "left",  "top"),
    ("Bucharest", 26.10, 44.44, -6,  4, "right", "bottom"),
    ("Sarajevo",  18.41, 43.86,  6,  4, "left",  "bottom"),
]
FOCUS = list(zip(TXT["focus"], ["greece", "italy", "spain"]))
COL = ["#7a1f0a", "#e08a5a", "#a9cfe0", "#2f6d8c"]
LBL = TXT["bands"]
HALO = [pe.withStroke(linewidth=2.6, foreground="white")]

fig = plt.figure(figsize=(16, 9.7))
asp = 1 / np.cos(np.deg2rad(41))
MAP_W, MAP_Y, MAP_H = .445, .565, .335

for f, ttl, x0 in ((A, "1980–1989", .048), (B, "2020–2025", .507)):
    ax = fig.add_axes([x0, MAP_Y, MAP_W, MAP_H])
    m = ax.pcolormesh(f.longitude, f.latitude, f.values, cmap="YlGnBu",
                      vmin=0, vmax=8, shading="auto")
    for geo in OUT.values():
        g = shape(geo)
        for p in (g.geoms if g.geom_type == "MultiPolygon" else [g]):
            x, y = p.exterior.xy
            ax.plot(x, y, color="#333", lw=.4, zorder=4)
    for n, lo, la, dx, dy, ha, va in CITIES:
        if la > NORTH:
            continue
        ax.plot(lo, la, "o", ms=4, mfc="white", mec="black", mew=1.0, zorder=6)
        ax.annotate(NM(n), (lo, la), xytext=(dx, dy), textcoords="offset points",
                    fontsize=9, weight="bold", color="black", ha=ha, va=va,
                    zorder=7, path_effects=HALO,
                    annotation_clip=True)      # never draw outside the axes
    ax.set_aspect(asp)
    ax.set_xlim(WEST, EAST)
    ax.set_ylim(SOUTH, NORTH)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(ttl, fontsize=13, weight="bold", pad=5)

cax = fig.add_axes([.33, MAP_Y - .050, .34, .014])
cb = fig.colorbar(m, cax=cax, orientation="horizontal")
cb.set_label(TXT["cbar"], fontsize=9.5, labelpad=5)

x = np.arange(3)
ax = fig.add_axes([.075, .075, .345, .325])
for i, (nm, k) in enumerate(FOCUS):
    s = S[k]
    ax.plot([s["wb"], s["wa"]], [i, i], c="#c9c9c9", lw=4.5, zorder=1,
            solid_capstyle="round")
    ax.scatter(s["wa"], i, s=95, c=BLUE, zorder=3)
    ax.scatter(s["wb"], i, s=95, c=RED, zorder=3)
    for v, c in ((s["wa"], BLUE), (s["wb"], RED)):
        ax.annotate(DEC(v), (v, i), xytext=(0, 11),
                    textcoords="offset points", fontsize=9.5, ha="center",
                    color=c, weight="bold")
    ax.annotate(f"−{DEC(s['wa'] - s['wb'])} h", (8.6, i), fontsize=11,
                weight="bold", va="center")
ax.set_yticks(x); ax.set_yticklabels([n for n, _ in FOCUS], fontsize=11)
ax.invert_yaxis(); ax.set_xlim(0, 10.1); ax.set_ylim(2.75, -.95)
ax.set_xlabel(TXT["xpp"], fontsize=10)
ax.grid(axis="x", alpha=.3)
h = [plt.Line2D([], [], marker="o", ls="", color=BLUE, ms=8, label=TXT["then"]),
     plt.Line2D([], [], marker="o", ls="", color=RED, ms=8, label=TXT["now"])]
ax.legend(handles=h, fontsize=9, ncol=2, frameon=False, loc="lower center",
          bbox_to_anchor=(.5, 1.005))

ax = fig.add_axes([.545, .075, .42, .325])
ticks, labels = [], []
for i, (nm, k) in enumerate(FOCUS):
    for j, (dec, band) in enumerate(((TXT["band_then"], S[k]["band_a"]),
                                     (TXT["band_now"], S[k]["band_b"]))):
        pos, left = i * 2.6 + j, 0
        for v, c in zip(band, COL):
            ax.barh(pos, v, left=left, color=c, height=.8,
                    edgecolor="white", lw=.7)
            if v > 6:
                ax.annotate(f"{v:.0f}", (left + v / 2, pos), ha="center",
                            va="center", fontsize=9, weight="bold",
                            color="white" if c != COL[2] else "#20404f")
            left += v
        ticks.append(pos); labels.append(f"{nm} {dec}")
ax.set_yticks(ticks); ax.set_yticklabels(labels, fontsize=9); ax.invert_yaxis()
ax.set_xlim(0, 100); ax.set_ylim(max(ticks) + .8, min(ticks) - 1.15)
ax.set_xlabel(TXT["xpop"], fontsize=10)
hh = [plt.Rectangle((0, 0), 1, 1, color=c) for c in COL]
ax.legend(hh, LBL, fontsize=8.5, ncol=4, frameon=False, loc="lower center",
          bbox_to_anchor=(.5, 1.005))

fig.suptitle(TXT["title"], fontsize=20,
             weight="bold", y=.955)
fig.savefig(FIGURES / TXT["out"], dpi=165)
print("fig3 written")
