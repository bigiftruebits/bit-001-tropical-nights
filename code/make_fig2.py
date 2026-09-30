"""Figure 2 — IF beat, BIG IF TRUE #001.

Genoa is excluded: its own ERA5-Land cell is sea, and the nearest land cells
run from 1.9 h (coast) to 8 h (hills), so no single cell represents the city.
See check_cities.py and bug-log entry 10.

Rebuilt so that both measures are read as CHANGE. The earlier version set
today's tropical-night share beside the change in hours of relief, which
compares a level with a change (bug-log entry 9). Here the left column is the
change in tropical-night share since the 1980s, and cities are ordered by it,
so the reader sees directly where the two measures of change disagree.

Author: Riccardo Gallotti (FBK). Code by Claude Opus 5 under his direction.
"""
import json, sys
import numpy as np, pandas as pd, xarray as xr
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from shapely.geometry import shape, Point
from shapely.prepared import prep

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATA, FIGURES
FIGURES.mkdir(exist_ok=True)
LANG = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("en", "it") else "en"
BORDERS = DATA / "borders.geojson"
TXT = {
  "en": dict(title="Tropical nights miss where cool air is being lost", map="Hours of relief today",
             cbar="hours of relief (of 8)", trop="Tropical nights", rel="Hours of relief",
             xtrop="share of the summer that is a tropical night", xrel="hours of relief (of 8)",
             then="1980s", now="2020s", out="fig-001-if-hours-of-relief.png", names={}),
  "it": dict(title="Le notti tropicali non mostrano dove si perde l'aria fresca", map="Ore di sollievo oggi",
             cbar="ore di sollievo (su 8)", trop="Notti tropicali", rel="Ore di sollievo",
             xtrop="estate con notti tropicali", xrel="ore di sollievo (su 8)",
             then="1980–1989", now="2020–2025", out="fig-001-if-hours-of-relief-it.png",
             names={"Rome": "Roma", "Milan": "Milano", "Naples": "Napoli", "Turin": "Torino"}),
}[LANG]
NM = lambda n: TXT["names"].get(n, n)
DEC = lambda v: f"{v:.1f}".replace(".", ",") if LANG == "it" else f"{v:.1f}"
THRESH, K = 20.0, 8
BIG7 = [("Rome",12.4964,41.9028),("Milan",9.1900,45.4642),("Naples",14.2681,40.8518),
        ("Turin",7.6869,45.0703),("Palermo",13.3615,38.1157),
        ("Bologna",11.3426,44.4949)]
BLUE, RED = "#5b8fa8", "#c1440e"

ra = xr.open_dataarray(DATA / "italy_relief_1980s.nc"); rb = xr.open_dataarray(DATA / "italy_relief_2020s.nc")
ta = xr.open_dataarray(DATA / "italy_tropical_1980s.nc"); tb = xr.open_dataarray(DATA / "italy_tropical_2020s.nc")
italy = shape(json.load(open(BORDERS))["italy"]); g = prep(italy)
lon, lat = np.meshgrid(ra.longitude.values, ra.latitude.values)
inside = np.fromiter((g.contains(Point(x,y)) for x,y in zip(lon.ravel(),lat.ravel())),
                     bool, lon.size).reshape(lon.shape)
M = xr.DataArray(inside, coords=ra.coords, dims=ra.dims)
ra, rb, ta, tb = (f.where(M) for f in (ra, rb, ta, tb))

def at(f, lo, la, r=.6):
    s = f.sel(latitude=slice(la+r, la-r), longitude=slice(lo-r, lo+r)); v = s.values
    L, A = np.meshgrid(s.longitude.values, s.latitude.values)
    d = np.where(np.isnan(v), np.inf, (L-lo)**2 + (A-la)**2)
    return float(v[np.unravel_index(np.argmin(d), d.shape)])

t = pd.DataFrame([dict(city=n, tA=at(ta,lo,la), tB=at(tb,lo,la),
                       cA=at(ra,lo,la), cB=at(rb,lo,la)) for n,lo,la in BIG7])
t["dT"] = t.tB - t.tA; t["lost"] = t.cA - t.cB
t = t.sort_values("dT", ascending=False).reset_index(drop=True)
t.round(2).to_csv(FIGURES / "fig2_cities.csv", index=False)
print(t.round(2).to_string(index=False))

# ---------------- figure ----------------
# Three panels. Tropical nights sit in the middle, drawn exactly like hours of
# relief (1980s dot -> 2020s dot, same rows), so the two pictures of change can
# be compared row by row. Percentages are printed as "7% -> 73%" rather than as
# a change in percentage points, which a general reader cannot decode.
plt.rcParams.update({"font.family": "DejaVu Sans", "xtick.labelsize": 11, "ytick.labelsize": 11})
HALO = [pe.withStroke(linewidth=2.4, foreground="white")]
fig = plt.figure(figsize=(15, 7.2))

# (a) map
ax = fig.add_axes([.0, .05, .37, .85]); ax.set_anchor("W")
m = ax.pcolormesh(rb.longitude, rb.latitude, rb.values, cmap="YlGnBu", vmin=0, vmax=8, shading="auto")
for p in (italy.geoms if italy.geom_type == "MultiPolygon" else [italy]):
    x, y = p.exterior.xy; ax.plot(x, y, color="k", lw=.7, zorder=4)
for n, lo, la in BIG7:
    ax.plot(lo, la, "o", ms=4.5, mfc="white", mec="k", mew=1, zorder=5)
    ax.annotate(NM(n), (lo, la), xytext=(4, 3), textcoords="offset points", fontsize=10,
                weight="bold", zorder=6, path_effects=HALO)
ax.set_aspect(1/np.cos(np.deg2rad(42))); ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(6.2, 18.9); ax.set_ylim(35.3, 47.3)
cax = fig.add_axes([.328, .16, .008, .62])
cb = fig.colorbar(m, cax=cax); cb.set_label(TXT["cbar"], fontsize=10.5)
ax.set_title(TXT["map"], weight="bold", fontsize=13)

y = np.arange(len(t))
def rows(ax):
    ax.set_yticks(y); ax.invert_yaxis(); ax.set_ylim(len(t) - .45, -.55)
    ax.grid(axis="x", alpha=.3); ax.set_axisbelow(True)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)

# (b) tropical nights — the centre of the figure
ax = fig.add_axes([.435, .14, .18, .68])
for i, r in t.iterrows():
    ax.plot([r.tA, r.tB], [i, i], c="#d0d0d0", lw=5, zorder=1, solid_capstyle="round")
    ax.scatter(r.tA, i, s=85, c=BLUE, zorder=3); ax.scatter(r.tB, i, s=85, c=RED, zorder=3)
    ax.annotate(f"{r.tA:.0f}% \u2192 {r.tB:.0f}%", (103, i), fontsize=12, va="center",
                weight="bold", annotation_clip=False)
rows(ax); ax.set_yticklabels([NM(c) for c in t.city], fontsize=13)
ax.set_xlim(-3, 100); ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
ax.set_xlabel(TXT["xtrop"], fontsize=11.5)
ax.set_title(TXT["trop"], weight="bold", fontsize=14.5)

# (c) hours of relief — same rows
ax = fig.add_axes([.735, .14, .18, .68])
for i, r in t.iterrows():
    ax.plot([r.cB, r.cA], [i, i], c="#d0d0d0", lw=5, zorder=1, solid_capstyle="round")
    ax.scatter(r.cA, i, s=85, c=BLUE, zorder=3); ax.scatter(r.cB, i, s=85, c=RED, zorder=3)
    ax.annotate(f"\u2212{DEC(r.lost)} h", (8.6, i), fontsize=12, va="center", weight="bold",
                annotation_clip=False)
rows(ax); ax.set_yticklabels([])
ax.set_xlim(0, 8.3); ax.set_xticks([0, 2, 4, 6, 8])
ax.set_xlabel(TXT["xrel"], fontsize=11.5)
ax.set_title(TXT["rel"], weight="bold", fontsize=14.5)

h = [plt.Line2D([], [], marker="o", ls="", color=BLUE, ms=8, label=TXT["then"]),
     plt.Line2D([], [], marker="o", ls="", color=RED, ms=8, label=TXT["now"])]
fig.legend(handles=h, loc="upper center", bbox_to_anchor=(.675, .925), ncol=2,
           frameon=False, fontsize=12)
fig.suptitle(TXT["title"],
             fontsize=18, weight="bold", y=.985)
fig.savefig(FIGURES / TXT["out"], dpi=170)
print("figure written")
