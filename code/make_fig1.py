"""Figure 1 — BIG beat, BIG IF TRUE #001: tropical nights in Italy, 1980s vs 2020s.

    python make_fig1.py en      -> fig-001-big-tropical-nights.png
    python make_fig1.py it      -> fig-001-big-tropical-nights-it.png

Same design and definitions as nightheat/figures.py::figure1. Tropical-night
share = % of summer months whose mean night minimum is >= 20 C (months, not
individual nights), day-weighted over June-August. Reads data/ only.

Author: Riccardo Gallotti (FBK). Code by Claude Opus 5 under his direction.
"""
import json, sys
import numpy as np, xarray as xr
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import shape, Point
from shapely.prepared import prep

LANG = sys.argv[1] if len(sys.argv) > 1 else "en"
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATA, FIGURES
FIGURES.mkdir(exist_ok=True)
BORDERS = DATA / "borders.geojson"
TXT = {
    "en": dict(title="Italy's summer nights stopped cooling down",
               cbar="share of summer with a tropical night (%)",
               cities=["Milan", "Rome", "Naples", "Bari", "Palermo", "Catania"],
               out="fig-001-big-tropical-nights.png"),
    "it": dict(title="Le notti estive italiane hanno smesso di rinfrescarsi",
               cbar="estate con notti tropicali (%)",
               cities=["Milano", "Roma", "Napoli", "Bari", "Palermo", "Catania"],
               out="fig-001-big-tropical-nights-it.png"),
}[LANG]
COORDS = [(9.19, 45.46), (12.50, 41.90), (14.25, 40.85), (16.87, 41.12),
          (13.36, 38.12), (15.09, 37.50)]


a = xr.open_dataarray(DATA / "italy_tropical_1980s.nc")
b = xr.open_dataarray(DATA / "italy_tropical_2020s.nc")
italy = shape(json.load(open(BORDERS))["italy"]); g = prep(italy)
lon, lat = np.meshgrid(a.longitude.values, a.latitude.values)
ins = np.fromiter((g.contains(Point(x, y)) for x, y in zip(lon.ravel(), lat.ravel())),
                  bool, lon.size).reshape(lon.shape)
M = xr.DataArray(ins, coords=a.coords, dims=a.dims)
a, b = a.where(M), b.where(M)

plt.rcParams.update({"font.family": "DejaVu Sans"})
fig, axes = plt.subplots(1, 2, figsize=(11.5, 7.0))
bb = italy.bounds
for ax, f, ttl in zip(axes, [a, b], ["1980–1989", "2020–2025"]):
    m = ax.pcolormesh(f.longitude, f.latitude, f.values, cmap="OrRd", vmin=0, vmax=100,
                      shading="auto")
    for p in (italy.geoms if italy.geom_type == "MultiPolygon" else [italy]):
        x, y = p.exterior.xy; ax.plot(x, y, color="k", lw=.65, zorder=4)
    for n, (lo, la) in zip(TXT["cities"], COORDS):
        ax.plot(lo, la, "o", ms=3.4, mfc="white", mec="k", mew=.8, zorder=5)
        ax.annotate(n, (lo, la), xytext=(3, 2), textcoords="offset points", fontsize=8, zorder=5)
    ax.set_aspect(1 / np.cos(np.deg2rad((bb[1] + bb[3]) / 2)))
    ax.set_xlim(bb[0] - .3, bb[2] + .3); ax.set_ylim(bb[1] - .3, bb[3] + .3)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(ttl, fontsize=13, weight="bold")
cb = fig.colorbar(m, ax=axes, fraction=.03, pad=.02)
cb.set_label(TXT["cbar"], fontsize=10)
fig.suptitle(TXT["title"], fontsize=17, weight="bold", y=.95)
fig.savefig(FIGURES / TXT["out"], dpi=170, bbox_inches="tight")
print("written", TXT["out"])
