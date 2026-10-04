"""
Draw Figure 1 (BIG): tropical nights in Italy, 1980s against 2020s.

Reads data/; writes figures/. Phone-sized: 4.4 in wide, no text under 9 pt,
height at most 1.75 x width; refuses to save a figure that breaks the rule.

    python make_fig1.py en|it

BIG IF TRUE · tropical-nights · https://github.com/bigiftruebits/bit-001-tropical-nights
Author: Riccardo Gallotti (FBK). Code by Claude Opus 5, then Claude Opus 5.5, under his direction.
Licence: MIT (code); data licences in DATA_MANIFEST.md.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATA, FIGURES
import numpy as np, xarray as xr
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.patheffects as pe
from matplotlib.text import Text
from shapely.geometry import shape, Point
from shapely.prepared import prep

LANG = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("en", "it") else "en"
# ---- everything a reader might want to change, in one table -------------------------
TXT = {"en": dict(title="Italy’s summer nights\nstopped cooling down",
                  cbar="share of the summer with a tropical night",
                  names={}, out="fig-001-big-tropical-nights.png"),
       "it": dict(title="Le notti estive italiane\nhanno smesso di rinfrescarsi",
                  cbar="estate con notti tropicali",
                  names={"Milan": "Milano", "Rome": "Roma", "Naples": "Napoli"},
                  out="fig-001-big-tropical-nights-it.png")}[LANG]
CITIES = [  # name, lon, lat, dx, dy (points), ha
    ("Milan", 9.19, 45.46, 3, 3, "left"), ("Rome", 12.50, 41.90, -3, 3, "right"),
    ("Naples", 14.25, 40.85, 4, -3, "left"), ("Palermo", 13.36, 38.12, -3, 4, "right")]
W, DPI, MIN_PT = 4.4, 450, 9.0
# --------------------------------------------------------------------------------------
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
HALO = [pe.withStroke(linewidth=2.2, foreground="white")]
a = xr.open_dataarray(DATA / "italy_tropical_1980s.nc"); b = xr.open_dataarray(DATA / "italy_tropical_2020s.nc")
italy = shape(json.load(open(DATA / "borders.geojson"))["italy"]); g = prep(italy)
lon, lat = np.meshgrid(a.longitude.values, a.latitude.values)
ins = np.fromiter((g.contains(Point(x, y)) for x, y in zip(lon.ravel(), lat.ravel())), bool, lon.size).reshape(lon.shape)
M = xr.DataArray(ins, coords=a.coords, dims=a.dims); a, b = a.where(M), b.where(M)

bb = italy.bounds; asp = 1 / np.cos(np.deg2rad((bb[1] + bb[3]) / 2))
xspan, yspan = bb[2] - bb[0] + 0.6, bb[3] - bb[1] + 0.6
mw = 2.08; mh = mw * yspan * asp / xspan                     # map width and height, inches
H = 0.80 + mh + 0.28 + 0.62                                   # colour bar, maps, period labels, title
fig = plt.figure(figsize=(W, H))
inch = lambda x, y, w, h: [x / W, y / H, w / W, h / H]
for i, (f, period) in enumerate(((a, "1980–1989"), (b, "2020–2025"))):
    ax = fig.add_axes(inch(0.08 + i * (mw + 0.08), 0.80, mw, mh))
    m = ax.pcolormesh(f.longitude, f.latitude, f.values, cmap="OrRd", vmin=0, vmax=100, shading="auto")
    for p in (italy.geoms if italy.geom_type == "MultiPolygon" else [italy]):
        x, y = p.exterior.xy; ax.plot(x, y, color="k", lw=.45, zorder=4)
    for n, lo, la, dx, dy, ha in CITIES:
        ax.plot(lo, la, "o", ms=2.6, mfc="white", mec="k", mew=.6, zorder=5)
        ax.annotate(TXT["names"].get(n, n), (lo, la), xytext=(dx, dy), textcoords="offset points",
                    fontsize=9, weight="bold", ha=ha, zorder=6, path_effects=HALO, annotation_clip=True)
    ax.set_aspect(asp); ax.set_xlim(bb[0] - .3, bb[2] + .3); ax.set_ylim(bb[1] - .3, bb[3] + .3)
    ax.set_xticks([]); ax.set_yticks([]); [s.set_linewidth(.5) for s in ax.spines.values()]
    fig.text((0.08 + i * (mw + 0.08) + mw / 2) / W, (0.80 + mh + 0.06) / H, period,
             ha="center", va="bottom", fontsize=10, weight="bold")
cax = fig.add_axes(inch(0.5, 0.44, W - 1.0, 0.11))
cb = fig.colorbar(m, cax=cax, orientation="horizontal"); cb.set_ticks([0, 25, 50, 75, 100])
cb.set_ticklabels(["0%", "25%", "50%", "75%", "100%"]); cb.ax.tick_params(labelsize=9, length=2)
cb.set_label(TXT["cbar"], fontsize=9, labelpad=3)
fig.text(0.5, 1 - 0.06 / H, TXT["title"], ha="center", va="top", fontsize=11, weight="bold", linespacing=1.15)

# ---- the phone rule, enforced -----------------------------------------------------------
w, h = fig.get_size_inches()
assert h / w <= 1.75, f"height/width {h / w:.2f} exceeds 1.75"
small = [(t.get_text(), t.get_fontsize()) for t in fig.findobj(Text)
         if t.get_visible() and t.get_text().strip() and t.get_fontsize() < MIN_PT]
assert not small, f"text under {MIN_PT} pt: {small[:4]}"
FIGURES.mkdir(exist_ok=True)
fig.savefig(FIGURES / TXT["out"], dpi=DPI)
print(f"written {TXT['out']}  {w:.1f} x {h:.2f} in  (ratio {h / w:.2f})")
