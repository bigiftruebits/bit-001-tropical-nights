"""
Draw Figure 2 (IF): six cities measured as tropical nights and as hours of relief.

Reads data/; writes figures/. One chart, same cities in the same rows;
phone-sized and checked like Figure 1.

    python make_fig2.py en|it

BIG IF TRUE · tropical-nights · https://github.com/bigiftruebits/bit-001-tropical-nights
Author: Riccardo Gallotti (FBK). Code by Claude Opus 5, then Claude Opus 5.5, under his direction.
Licence: MIT (code); data licences in DATA_MANIFEST.md.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATA, FIGURES
import numpy as np, pandas as pd, xarray as xr
import matplotlib; matplotlib.use("Agg")
import json
import matplotlib.pyplot as plt, matplotlib.patheffects as pe
from matplotlib.text import Text
from shapely.geometry import shape

LANG = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("en", "it") else "en"
# ---- everything a reader might want to change, in one table -------------------------
TXT = {"en": dict(title="Tropical nights miss where\ncool air is being lost", trop="Tropical nights",
                  rel="Hours of relief", map="Hours of relief today", cbar="of the 8 coolest hours", xtrop="share of the summer",
                  xrel="hours of relief (of 8)", then="1980s", now="2020s", names={},
                  out="fig-001-if-hours-of-relief.png"),
       "it": dict(title="Le notti tropicali non mostrano\ndove si perde l’aria fresca", trop="Notti tropicali",
                  rel="Ore di sollievo", map="Ore di sollievo oggi", cbar="delle 8 ore più fresche", xtrop="parte dell’estate",
                  xrel="ore di sollievo (su 8)", then="1980–89", now="2020–25",
                  names={"Rome": "Roma", "Milan": "Milano", "Naples": "Napoli", "Turin": "Torino"},
                  out="fig-001-if-hours-of-relief-it.png")}[LANG]
# Genoa is not shown: its own grid cell is sea (see check_cities.py and the limitations)
CITIES = [("Rome", 12.4964, 41.9028), ("Milan", 9.19, 45.4642), ("Naples", 14.2681, 40.8518),
          ("Turin", 7.6869, 45.0703), ("Palermo", 13.3615, 38.1157), ("Bologna", 11.3426, 44.4949)]
BLUE, RED, GREY = "#5b8fa8", "#c1440e", "#d0d0d0"
W, DPI, MIN_PT = 4.4, 450, 9.0
# --------------------------------------------------------------------------------------
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "xtick.labelsize": 9, "ytick.labelsize": 9.5})
dec = (lambda v: f"{v:.1f}".replace(".", ",")) if LANG == "it" else (lambda v: f"{v:.1f}")
load = lambda n: xr.open_dataarray(DATA / n)
tA, tB, rA, rB = (load(f"italy_{k}.nc") for k in ("tropical_1980s", "tropical_2020s", "relief_1980s", "relief_2020s"))

def at(f, lo, la, r=.6):
    s = f.sel(latitude=slice(la + r, la - r), longitude=slice(lo - r, lo + r)); v = s.values
    L, A = np.meshgrid(s.longitude.values, s.latitude.values)
    d = np.where(np.isnan(v), np.inf, (L - lo) ** 2 + (A - la) ** 2)
    return float(v[np.unravel_index(np.argmin(d), d.shape)])

t = pd.DataFrame([dict(city=n, tA=at(tA, lo, la), tB=at(tB, lo, la), rA=at(rA, lo, la), rB=at(rB, lo, la))
                  for n, lo, la in CITIES])
t = t.assign(rise=t.tB - t.tA, lost=t.rA - t.rB).sort_values("rise", ascending=False).reset_index(drop=True)

# Layout: the map fills the height of the left column; two compact charts on the right
italy = shape(json.load(open(DATA / "borders.geojson"))["italy"]); bb = italy.bounds
asp = 1 / np.cos(np.deg2rad((bb[1] + bb[3]) / 2))
MW = 2.15; MH = MW * (bb[3] - bb[1] + .6) * asp / (bb[2] - bb[0] + .6)     # map width, height (inches)
CB = 0.46                                                                   # colour bar under the map
COL = MH + CB                                                               # height of both columns
LEG, PT, TK, GAP = 0.25, 0.22, 0.20, 0.12          # legend, chart title, tick labels, gap between charts
AX_H = (COL - LEG - GAP - 2 * (PT + TK)) / 2; ROW = AX_H / len(t)
TITLE, BOT = 0.55, 0.12
H = BOT + COL + TITLE
fig = plt.figure(figsize=(W, H))
inch = lambda x, y, w, h: [x / W, y / H, w / W, h / H]
X0, XW, XV = 2.90, 0.62, 3.58             # chart axes left, width, value column (inches)
def panel(y0, title, a, b, xmax, ticks, ticklabels, value):
    """a = 1980s (blue), b = 2020s (red), always."""
    ax = fig.add_axes(inch(X0, y0, XW, AX_H))
    for i, r in t.iterrows():
        ax.plot([a[i], b[i]], [i, i], color=GREY, lw=2.6, solid_capstyle="round", zorder=1)
        ax.scatter(a[i], i, s=24, color=BLUE, zorder=3); ax.scatter(b[i], i, s=24, color=RED, zorder=3)
        fig.text(XV / W, (y0 + AX_H * (len(t) - 0.5 - i) / len(t)) / H, value(r), fontsize=9,
                 weight="bold", va="center")
    ax.set_yticks(range(len(t))); ax.set_yticklabels([TXT["names"].get(c, c) for c in t.city], fontsize=9)
    ax.invert_yaxis(); ax.set_ylim(len(t) - .5, -.5)
    ax.set_xlim(-.03 * xmax, xmax); ax.set_xticks(ticks); ax.set_xticklabels(ticklabels)
    ax.grid(axis="x", alpha=.3); ax.set_axisbelow(True); ax.tick_params(length=2, pad=1)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    fig.text((X0 - 0.62) / W, (y0 + AX_H + 0.05) / H, title, fontsize=10, weight="bold", va="bottom")

yB = BOT + TK; yA = yB + AX_H + PT + GAP + TK
panel(yA, TXT["trop"], t.tA, t.tB, 104, [0, 50, 100], ["0", "50", "100%"], lambda r: f"{r.tA:.0f}% → {r.tB:.0f}%")
panel(yB, TXT["rel"], t.rA, t.rB, 8.3, [0, 4, 8], ["0 h", "4 h", "8 h"], lambda r: f"−{dec(r.lost)} h")

# the map of hours of relief today, the full height of the left column
yM = BOT + CB
mx = fig.add_axes(inch(0.06, yM, MW, MH))
from shapely.geometry import Point
from shapely.prepared import prep
gI = prep(italy); LO2, LA2 = np.meshgrid(rB.longitude.values, rB.latitude.values)
inI = np.fromiter((gI.contains(Point(x, y)) for x, y in zip(LO2.ravel(), LA2.ravel())), bool, LO2.size).reshape(LO2.shape)
mm = mx.pcolormesh(rB.longitude, rB.latitude, np.where(inI, rB.values, np.nan), cmap="YlGnBu", vmin=0, vmax=8, shading="auto")
for p in (italy.geoms if italy.geom_type == "MultiPolygon" else [italy]):
    x, y = p.exterior.xy; mx.plot(x, y, color="k", lw=.4, zorder=4)
HALO = [pe.withStroke(linewidth=2.2, foreground="white")]
POS = {"Turin": (3, -3, "left"), "Milan": (3, 3, "left"), "Bologna": (3, -3, "left"),
       "Rome": (-3, 2, "right"), "Naples": (3, -2, "left"), "Palermo": (-3, 3, "right")}
for n, lo, la in CITIES:
    dx, dy, ha = POS[n]
    mx.plot(lo, la, "o", ms=2.6, mfc="white", mec="k", mew=.6, zorder=5)
    mx.annotate(TXT["names"].get(n, n), (lo, la), xytext=(dx, dy), textcoords="offset points", fontsize=9,
                weight="bold", ha=ha, va="bottom" if dy > 0 else "top", zorder=6, path_effects=HALO)
mx.set_aspect(asp); mx.set_xlim(bb[0] - .3, bb[2] + .3); mx.set_ylim(bb[1] - .3, bb[3] + .3)
mx.set_xticks([]); mx.set_yticks([]); [q.set_visible(False) for q in mx.spines.values()]   # no frame
mx.text(0.03, 0.03, TXT["map"], transform=mx.transAxes, ha="left", va="bottom", fontsize=9.5, weight="bold",
        path_effects=HALO, zorder=7, linespacing=1.1)                       # title inside, over the open sea
cx = fig.add_axes(inch(0.20, BOT + 0.20, MW - 0.28, 0.08))
cb = fig.colorbar(mm, cax=cx, orientation="horizontal"); cb.set_ticks([0, 4, 8]); cb.ax.tick_params(labelsize=9, length=2, pad=1)
cb.ax.xaxis.set_ticks_position("top")
fig.text((0.20 + (MW - 0.28) / 2) / W, (BOT + 0.02) / H, TXT["cbar"], ha="center", va="bottom", fontsize=9)
fig.canvas.draw(); _r = fig.canvas.get_renderer()
_top = max(t.get_window_extent(_r).y1 for t in cb.ax.get_xticklabels() if t.get_text())
assert _top < mx.get_window_extent(_r).y0, "colour-bar labels overlap the map"
h1 = plt.Line2D([], [], marker="o", ls="", color=BLUE, ms=5, label=TXT["then"])
h2 = plt.Line2D([], [], marker="o", ls="", color=RED, ms=5, label=TXT["now"])
fig.legend(handles=[h1, h2], loc="center", bbox_to_anchor=((X0 + 0.5) / W, (BOT + COL - LEG / 2) / H), ncol=2,
           frameon=False, fontsize=9, handletextpad=0.2, columnspacing=0.9)
fig.text(0.5, 1 - 0.06 / H, TXT["title"], ha="center", va="top", fontsize=11, weight="bold", linespacing=1.15)

# ---- the phone rule, enforced -----------------------------------------------------------
w, h = fig.get_size_inches()
assert h / w <= 1.75, f"height/width {h / w:.2f} exceeds 1.75"
# IF is article-only: allowed 0.6-1.75, optimal 1.0-1.25 (spec note, 2026-10-04)
assert 0.6 <= h / w <= 1.75, f"IF ratio {h / w:.2f} outside 0.6-1.75"
small = [(x.get_text(), x.get_fontsize()) for x in fig.findobj(Text)
         if x.get_visible() and x.get_text().strip() and x.get_fontsize() < MIN_PT]
assert not small, f"text under {MIN_PT} pt: {small[:4]}"
FIGURES.mkdir(exist_ok=True)
t.round(2).to_csv(FIGURES / "fig2_cities.csv", index=False)
fig.savefig(FIGURES / TXT["out"], dpi=DPI)
print(f"written {TXT['out']}  {w:.1f} x {h:.2f} in  (ratio {h / w:.2f})")
