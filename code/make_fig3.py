"""
Draw Figure 3 (TRUE): the basin in both decades, and the people in each band, panels a-c.

Reads data/ (the relief maps, the outlines and the population per grid cell); writes
figures/. (a) 1980-1989 and (b) 2020-2025, every land cell in the frame; (c) the people
of the eight countries, and of Greece, Italy and Spain, in four bands, each label with
the average hours per person. At most three panels (format §4.9). The two maps make it
taller than the 0.8 Note shape: ratio about 1.45, by Riccardo's choice (deviations.md).

    python make_fig3.py en|it

BIG IF TRUE · tropical-nights · https://github.com/bigiftruebits/bit-001-tropical-nights
Author: Riccardo Gallotti (FBK). Code by Claude Opus 5, then Claude Opus 5.5, under his direction.
Licence: MIT (code); data licences in DATA_MANIFEST.md.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATA, FIGURES, FRAME
import numpy as np, pandas as pd, xarray as xr
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.patheffects as pe
from matplotlib.text import Text
from shapely.geometry import shape

LANG = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("en", "it") else "en"
# ---- everything a reader might want to change, in one table -------------------------
TXT = {"en": dict(title="Cool nights are scarcest where people live", c="People by hours of relief",
                  cbar="hours of relief, of the 8 coolest hours", then="1980–89", now="2020–25", dec=lambda v: f"{v:.1f}",
                  bands=["no relief (0 h)", "under 4 h", "4–8 h", "full 8 h"],
                  groups=[("8 countries", None), ("Greece", "greece"), ("Italy", "italy"), ("Spain", "spain")],
                  names={}, out="fig-001-true-hours-of-relief.png"),
       "it": dict(title="Meno notti fresche dove vive la gente", c="Persone per ore di sollievo",
                  cbar="ore di sollievo, delle 8 ore più fresche", then="1980–89", now="2020–25", dec=lambda v: f"{v:.1f}".replace(".", ","),
                  bands=["nessun sollievo (0 h)", "meno di 4 h", "4–8 h", "8 h piene"],
                  groups=[("8 paesi", None), ("Grecia", "greece"), ("Italia", "italy"), ("Spagna", "spain")],
                  names={"Milan": "Milano", "Rome": "Roma", "Athens": "Atene", "Algiers": "Algeri"},
                  out="fig-001-true-hours-of-relief-it.png")}[LANG]
CITIES = [("Madrid", -3.70, 40.42, 3, 3, "left"), ("Milan", 9.19, 45.46, 3, 3, "left"),
          ("Rome", 12.50, 41.90, 3, 3, "left"), ("Athens", 23.73, 37.98, -3, 3, "right"),
          ("Algiers", 3.06, 36.75, 3, -4, "left")]
BANDS = ["#7a1f0a", "#e08a5a", "#a9cfe0", "#2f6d8c"]          # 0 h, <4 h, 4-8 h, full 8 h
W, DPI, MIN_PT = 4.4, 450, 9.0
# --------------------------------------------------------------------------------------
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "xtick.labelsize": 9, "ytick.labelsize": 9})
HALO = [pe.withStroke(linewidth=2.2, foreground="white")]
A = xr.open_dataarray(DATA / "seu_relief_1980s.nc"); B = xr.open_dataarray(DATA / "seu_relief_2020s.nc")
pop = pd.read_csv(DATA / "population_by_cell.csv")
OUT = [shape(g) for g in json.load(open(DATA / "frame_outlines.geojson")).values()]

def stats(d):
    sel = lambda F: F.sel(latitude=xr.DataArray(d.lat.values), longitude=xr.DataArray(d.lon.values), method="nearest").values
    a, b, w = sel(A), sel(B), d.population.values
    bands = lambda v: np.array([w[v < .5].sum(), w[(v >= .5) & (v < 4)].sum(), w[(v >= 4) & (v < 7.5)].sum(),
                                w[v >= 7.5].sum()]) / w.sum() * 100
    return dict(wa=np.average(a, weights=w), wb=np.average(b, weights=w), ba=bands(a), bb=bands(b))
S = [stats(pop if k is None else pop[pop.country == k]) for _, k in TXT["groups"]]

W0, S0, E0, N0 = FRAME[0], 35.0, FRAME[2], FRAME[3]
asp = 1 / np.cos(np.deg2rad((S0 + N0) / 2)); MW = W - 0.08; MH = MW * (N0 - S0) * asp / (E0 - W0)   # full width
n, BLOCK = len(S), 0.36
LEGEND, TICKS, CTITLE, CBAR, GAP, TITLE = 0.34, 0.20, 0.24, 0.40, 0.08, 0.36
yC = LEGEND + TICKS; AH = n * BLOCK                       # panel c
yCB = yC + AH + CTITLE + 0.06                             # colour bar
yB = yCB + CBAR; yA = yB + MH + GAP                       # maps b and a
H = yA + MH + TITLE
fig = plt.figure(figsize=(W, H))
inch = lambda x, y, w, h: [x / W, y / H, w / W, h / H]

for f, lab, y0 in ((A, "a  1980–1989", yA), (B, "b  2020–2025", yB)):
    ax = fig.add_axes(inch(0.04, y0, MW, MH))
    m = ax.pcolormesh(f.longitude, f.latitude, f.values, cmap="YlGnBu", vmin=0, vmax=8, shading="auto")
    for g in OUT:
        for p in (g.geoms if g.geom_type == "MultiPolygon" else [g]):
            x, yy = p.exterior.xy; ax.plot(x, yy, color="#333", lw=.3, zorder=4)
    for nm, lo, la, dx, dy, ha in CITIES:
        ax.plot(lo, la, "o", ms=2.4, mfc="white", mec="k", mew=.6, zorder=5)
        ax.annotate(TXT["names"].get(nm, nm), (lo, la), xytext=(dx, dy), textcoords="offset points", fontsize=9,
                    weight="bold", ha=ha, va="bottom" if dy > 0 else "top", zorder=6, path_effects=HALO)
    ax.set_aspect(asp); ax.set_xlim(W0, E0); ax.set_ylim(S0, N0); ax.set_xticks([]); ax.set_yticks([])
    [q.set_linewidth(.5) for q in ax.spines.values()]
    ax.text(0.012, 0.96, lab, transform=ax.transAxes, fontsize=9.5, weight="bold", va="top", path_effects=HALO, zorder=7)
# the colour bar across the full width, its label underneath
cx = fig.add_axes(inch(0.10, yCB + 0.28, MW - 0.12, 0.08))   # inset so the 0 and 8 labels stay inside
cb = fig.colorbar(m, cax=cx, orientation="horizontal"); cb.set_ticks(range(0, 9)); cb.ax.tick_params(labelsize=9, length=2, pad=1)
fig.text(0.5, (yCB + 0.01) / H, TXT["cbar"], fontsize=9, ha="center", va="bottom")

# (c) four bands per group and decade; each label carries the average hours per person
LX = 1.92
bx = fig.add_axes(inch(LX, yC, W - LX - 0.26, AH))
ticks, labels = [], []
for i, s in enumerate(S):
    for j, (per, band, mean) in enumerate(((TXT["then"], s["ba"], s["wa"]), (TXT["now"], s["bb"], s["wb"]))):
        yc = (n - 1 - i) + (0.2 if j == 0 else -0.2); left = 0
        for v, c in zip(band, BANDS):
            bx.barh(yc, v, left=left, height=.38, color=c, edgecolor="white", lw=.4)
            if v >= 12:
                bx.text(left + v / 2, yc, f"{v:.0f}", ha="center", va="center", fontsize=9, weight="bold",
                        color="#20404f" if c == BANDS[2] else "white")
            left += v
        ticks.append(yc); labels.append(f"{TXT['groups'][i][0]}, {per} ({TXT['dec'](mean)} h)")
bx.set_yticks(ticks); bx.set_yticklabels(labels); bx.set_ylim(-.5, n - .5)
bx.set_xlim(0, 100); bx.set_xticks([0, 50, 100]); bx.set_xticklabels(["0%", "50%", "100%"]); bx.tick_params(length=2)
[bx.spines[q].set_visible(False) for q in ("top", "right")]
fig.text(0.08 / W, (yC + AH + 0.06) / H, f"c  {TXT['c']}", fontsize=9.5, weight="bold", va="bottom")
hb = [plt.Rectangle((0, 0), 1, 1, color=c) for c in BANDS]
# the legend spread across the full width
leg = fig.legend(hb, TXT["bands"], loc="lower left", bbox_to_anchor=(0.04 / W, 0.04 / H, MW / W, 0.26 / H),
                 mode="expand", ncol=4, frameon=False, fontsize=9, handlelength=1.0, handletextpad=0.3, borderaxespad=0)
fig.text(0.5, 1 - 0.06 / H, TXT["title"], ha="center", va="top", fontsize=11, weight="bold")

# ---- checks: nothing overlaps, nothing too small, the shape is allowed --------------------
fig.canvas.draw(); r = fig.canvas.get_renderer()
lb = leg.get_window_extent(r)
assert cx.get_window_extent(r).y1 < fig.axes[1].get_window_extent(r).y0, "colour bar overlaps map b"
assert lb.x0 >= 0 and lb.x1 <= fig.bbox.width, "the legend runs off the figure"
w, h = fig.get_size_inches()
assert h / w <= 1.75, f"height/width {h / w:.2f} exceeds 1.75"
small = [(x.get_text(), x.get_fontsize()) for x in fig.findobj(Text)
         if x.get_visible() and x.get_text().strip() and x.get_fontsize() < MIN_PT]
assert not small, f"text under {MIN_PT} pt: {small[:4]}"
FIGURES.mkdir(exist_ok=True)
fig.savefig(FIGURES / TXT["out"], dpi=DPI)
print(f"written {TXT['out']}  {w:.1f} x {h:.2f} in  (ratio {h / w:.2f}); 8 countries {S[0]['wa']:.2f} -> {S[0]['wb']:.2f} h")
