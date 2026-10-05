"""
Draw the Mediterranean maps used by the preview image: hours of relief, 1980s and 2020s.

Reads data/ (the southern-Europe relief map and the country outlines); writes
figures/fig-001-preview-map[-it].png: the basin in 1980-1989 above the basin in 2020-2025,
as in Figure 3, without a colour bar. Chosen for #001's preview by Riccardo on 2026-10-04
(test PREVIEW-AB-3; see deviations.md). 4.4 in wide, no text under 9 pt.

    python make_preview_map.py en|it [--single]

BIG IF TRUE · tropical-nights · https://github.com/bigiftruebits/bit-001-tropical-nights
Author: Riccardo Gallotti (FBK). Code by Claude Opus 5.5 under his direction.
Licence: MIT (code); data licences in DATA_MANIFEST.md.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATA, FIGURES, FRAME
import numpy as np, xarray as xr
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.patheffects as pe
from matplotlib.text import Text
from shapely.geometry import shape

LANG = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("en", "it") else "en"
SINGLE = "--single" in sys.argv          # only the 2020-2025 map, for the stacked variant A
TXT = {"en": dict(cbar="hours of relief, of the 8 coolest hours of the night", names={},
                  out="fig-001-preview-map.png"),
       "it": dict(cbar="ore di sollievo, delle 8 ore più fresche della notte",
                  names={"Milan": "Milano", "Rome": "Roma", "Athens": "Atene", "Algiers": "Algeri"},
                  out="fig-001-preview-map-it.png")}[LANG]
CITIES = [("Madrid", -3.70, 40.42, 3, 3, "left"), ("Milan", 9.19, 45.46, 3, 3, "left"),
          ("Rome", 12.50, 41.90, 3, 3, "left"), ("Athens", 23.73, 37.98, -3, 3, "right"),
          ("Algiers", 3.06, 36.75, 3, -4, "left")]
W, DPI, MIN_PT = 4.4, 450, 9.0
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
HALO = [pe.withStroke(linewidth=2.2, foreground="white")]
B = xr.open_dataarray(DATA / "seu_relief_2020s.nc")
W0, S0, E0, N0 = FRAME[0], 35.0, FRAME[2], FRAME[3]
asp = 1 / np.cos(np.deg2rad((S0 + N0) / 2)); MW = W - 0.16; MH = MW * (N0 - S0) * asp / (E0 - W0)
A = xr.open_dataarray(DATA / "seu_relief_1980s.nc")
GAP = 0.08
H = 0.06 + MH + 0.06 if SINGLE else 0.06 + MH + GAP + MH + 0.06
fig = plt.figure(figsize=(W, H))
inch = lambda x, y, w, h: [x / W, y / H, w / W, h / H]
outlines = [shape(g) for g in json.load(open(DATA / "frame_outlines.geojson")).values()]
for f, period, y0 in (((B, "2020–2025", 0.06),) if SINGLE else ((A, "1980–1989", 0.06 + MH + GAP), (B, "2020–2025", 0.06))):
    ax = fig.add_axes(inch(0.08, y0, MW, MH))
    m = ax.pcolormesh(f.longitude, f.latitude, f.values, cmap="YlGnBu", vmin=0, vmax=8, shading="auto")
    for g in outlines:
        for p in (g.geoms if g.geom_type == "MultiPolygon" else [g]):
            x, y = p.exterior.xy; ax.plot(x, y, color="#333", lw=.35, zorder=4)
    for n, lo, la, dx, dy, ha in CITIES:
        ax.plot(lo, la, "o", ms=2.4, mfc="white", mec="k", mew=.6, zorder=5)
        ax.annotate(TXT["names"].get(n, n), (lo, la), xytext=(dx, dy), textcoords="offset points", fontsize=9,
                    weight="bold", ha=ha, va="bottom" if dy > 0 else "top", zorder=6, path_effects=HALO)
    ax.set_aspect(asp); ax.set_xlim(W0, E0); ax.set_ylim(S0, N0); ax.set_xticks([]); ax.set_yticks([])
    [q.set_linewidth(.5) for q in ax.spines.values()]
    ax.text(0.015, 0.97, period, transform=ax.transAxes, fontsize=10, weight="bold", va="top", path_effects=HALO, zorder=7)
# no colour bar in the preview (Riccardo, 2026-10-04): the two decades compare by eye
w, h = fig.get_size_inches()
small = [(t.get_text(), t.get_fontsize()) for t in fig.findobj(Text) if t.get_visible() and t.get_text().strip() and t.get_fontsize() < MIN_PT]
assert not small, f"text under {MIN_PT} pt: {small[:4]}"
out = TXT["out"].replace("preview-map", "preview-map-2020s") if SINGLE else TXT["out"]
FIGURES.mkdir(exist_ok=True); fig.savefig(FIGURES / out, dpi=DPI)
print(f"written {out}  {w:.1f} x {h:.2f} in")
