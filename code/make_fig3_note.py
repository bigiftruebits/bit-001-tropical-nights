"""
Draw the Note version of Figure 3 (TRUE), in the 0.8 Note shape: the basin map, hours per person, people by band.

Reads data/ (the relief maps and the population per grid cell); writes figures/.
At most three panels, 0.8 shape (format §4.9, revised 2026-10-04): (a) the basin map
of hours of relief today, (b) hours of relief per person, then and now, (c) the same
people in four bands; (b) and (c) for the eight countries and Greece, Italy, Spain.

    python make_fig3_note.py en|it        -> figures/fig-001-true-note[-it].png

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
from config import FRAME

LANG = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("en", "it") else "en"
# ---- everything a reader might want to change, in one table -------------------------
TXT = {"en": dict(title="Cool nights are scarcest where people live", a="Hours per person",
                  b="People by hours of relief", m="2020–2025", cbar="hours of relief, of 8", then="1980s", now="2020s",
                  bands=["no relief (0 h)", "under 4 h", "4–8 h", "full 8 h"],
                  groups=[("8 countries", None), ("Greece", "greece"), ("Italy", "italy"), ("Spain", "spain")],
                  names={}, out="fig-001-true-note.png"),
       "it": dict(title="Meno notti fresche dove vive la gente", a="Ore a persona",
                  b="Persone per ore di sollievo", m="2020–2025", cbar="ore di sollievo, su 8", then="1980–89", now="2020–25",
                  bands=["nessun sollievo (0 h)", "meno di 4 h", "4–8 h", "8 h piene"],
                  groups=[("8 paesi", None), ("Grecia", "greece"), ("Italia", "italy"), ("Spagna", "spain")],
                  names={"Milan": "Milano", "Rome": "Roma", "Athens": "Atene", "Algiers": "Algeri"},
                  out="fig-001-true-note-it.png")}[LANG]
BLUE, RED, GREY = "#5b8fa8", "#c1440e", "#d0d0d0"
BANDS = ["#7a1f0a", "#e08a5a", "#a9cfe0", "#2f6d8c"]          # 0 h, <4 h, 4-8 h, full 8 h
W, DPI, MIN_PT = 4.4, 450, 9.0
# --------------------------------------------------------------------------------------
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "xtick.labelsize": 9, "ytick.labelsize": 9.5})
A = xr.open_dataarray(DATA / "seu_relief_1980s.nc"); B = xr.open_dataarray(DATA / "seu_relief_2020s.nc")
pop = pd.read_csv(DATA / "population_by_cell.csv")

def stats(d):
    sel = lambda F: F.sel(latitude=xr.DataArray(d.lat.values), longitude=xr.DataArray(d.lon.values), method="nearest").values
    a, b, w = sel(A), sel(B), d.population.values
    bands = lambda v: np.array([w[v < .5].sum(), w[(v >= .5) & (v < 4)].sum(), w[(v >= 4) & (v < 7.5)].sum(),
                                w[v >= 7.5].sum()]) / w.sum() * 100
    return dict(wa=np.average(a, weights=w), wb=np.average(b, weights=w), ba=bands(a), bb=bands(b))
S = [stats(pop if k is None else pop[pop.country == k]) for _, k in TXT["groups"]]

n, BLOCK = len(S), 0.31                                   # one block per group, inches
W0, S0, E0, N0 = FRAME[0], 35.0, FRAME[2], FRAME[3]       # the frame, empty southern edge trimmed
asp = 1 / np.cos(np.deg2rad((S0 + N0) / 2)); MW = W - 0.16; MH = MW * (N0 - S0) * asp / (E0 - W0)
y0, AH = 0.50, n * BLOCK                                  # panels b and c: legends and ticks below
yC = y0 + AH + 0.22 + 0.08                                # colour bar
yM = yC + 0.26                                            # map
H = yM + MH + 0.36
fig = plt.figure(figsize=(W, H))
inch = lambda x, y, w, h: [x / W, y / H, w / W, h / H]

# (a) the basin map of hours of relief today
mx = fig.add_axes(inch(0.08, yM, MW, MH))
m = mx.pcolormesh(B.longitude, B.latitude, B.values, cmap="YlGnBu", vmin=0, vmax=8, shading="auto")
for geo in json.load(open(DATA / "frame_outlines.geojson")).values():
    gg = shape(geo)
    for p in (gg.geoms if gg.geom_type == "MultiPolygon" else [gg]):
        x, yy = p.exterior.xy; mx.plot(x, yy, color="#333", lw=.3, zorder=4)
HALO = [pe.withStroke(linewidth=2.2, foreground="white")]
for nm, lo, la, dx, dy, ha in [("Madrid", -3.70, 40.42, 3, 3, "left"), ("Milan", 9.19, 45.46, 3, 3, "left"),
                               ("Rome", 12.50, 41.90, 3, 3, "left"), ("Athens", 23.73, 37.98, -3, 3, "right"),
                               ("Algiers", 3.06, 36.75, 3, -4, "left")]:
    mx.plot(lo, la, "o", ms=2.4, mfc="white", mec="k", mew=.6, zorder=5)
    mx.annotate(TXT["names"].get(nm, nm), (lo, la), xytext=(dx, dy), textcoords="offset points", fontsize=9,
                weight="bold", ha=ha, va="bottom" if dy > 0 else "top", zorder=6, path_effects=HALO)
mx.set_aspect(asp); mx.set_xlim(W0, E0); mx.set_ylim(S0, N0); mx.set_xticks([]); mx.set_yticks([])
[q.set_linewidth(.5) for q in mx.spines.values()]
mx.text(0.012, 0.96, f"a  {TXT['m']}", transform=mx.transAxes, fontsize=9.5, weight="bold", va="top", path_effects=HALO, zorder=7)
cx = fig.add_axes(inch(0.30, yC, 1.9, 0.08))
cb = fig.colorbar(m, cax=cx, orientation="horizontal"); cb.set_ticks([0, 4, 8]); cb.ax.tick_params(labelsize=9, length=2)
cb.ax.xaxis.set_ticks_position("top")                     # ticks above the bar, clear of panels b and c
fig.text(2.30 / W, (yC + 0.04) / H, TXT["cbar"], fontsize=9, va="center")

# (a) hours of relief per person: one dumbbell per group
ax = fig.add_axes(inch(0.86, y0, 1.08, AH))
for i, s in enumerate(S):
    yc = n - 1 - i
    ax.plot([s["wb"], s["wa"]], [yc, yc], color=GREY, lw=3.2, solid_capstyle="round", zorder=1)
    ax.scatter(s["wa"], yc, s=34, color=BLUE, zorder=3); ax.scatter(s["wb"], yc, s=34, color=RED, zorder=3)
ax.set_yticks(range(n)); ax.set_yticklabels([g for g, _ in TXT["groups"]][::-1]); ax.set_ylim(-.5, n - .5)
ax.set_xlim(0, 8.3); ax.set_xticks([0, 4, 8]); ax.set_xticklabels(["0 h", "4 h", "8 h"])
ax.grid(axis="x", alpha=.3); ax.set_axisbelow(True); ax.tick_params(length=2)
[ax.spines[q].set_visible(False) for q in ("top", "right")]
fig.text(0.06 / W, (y0 + AH + 0.06) / H, f"b  {TXT['a']}", fontsize=9.5, weight="bold", va="bottom")
hd = [plt.Line2D([], [], marker="o", ls="", color=c, ms=5, label=l) for c, l in ((BLUE, TXT["then"]), (RED, TXT["now"]))]
leg_b = fig.legend(handles=hd, loc="center", bbox_to_anchor=((0.86 + 0.54) / W, 0.165 / H), ncol=1, frameon=False,
           fontsize=9, handletextpad=0.2, labelspacing=0.2)        # two rows: clear of panel c's legend in both languages

# (b) the same people in four bands: two bars per group, then and now
bx = fig.add_axes(inch(2.56, y0, W - 2.56 - 0.26, AH))
for i, s in enumerate(S):
    for j, band in enumerate((s["ba"], s["bb"])):
        yc = (n - 1 - i) + (0.2 if j == 0 else -0.2); left = 0
        for v, c in zip(band, BANDS):
            bx.barh(yc, v, left=left, height=.38, color=c, edgecolor="white", lw=.4)
            if v >= 14:
                bx.text(left + v / 2, yc, f"{v:.0f}", ha="center", va="center", fontsize=9, weight="bold",
                        color="#20404f" if c == BANDS[2] else "white")
            left += v
bx.set_yticks([k + d for k in range(n) for d in (0.2, -0.2)])
bx.set_yticklabels([lab for k in range(n) for lab in (TXT["then"], TXT["now"])], fontsize=9)
bx.set_ylim(-.5, n - .5); bx.set_xlim(0, 100); bx.set_xticks([0, 50, 100])
bx.set_xticklabels(["0%", "50%", "100%"]); bx.tick_params(length=2)
[bx.spines[q].set_visible(False) for q in ("top", "right")]
fig.text(2.00 / W, (y0 + AH + 0.06) / H, f"c  {TXT['b']}", fontsize=9.5, weight="bold", va="bottom")
hb = [plt.Rectangle((0, 0), 1, 1, color=c) for c in BANDS]
leg_c = fig.legend(hb, TXT["bands"], loc="center", bbox_to_anchor=((2.05 + (W - 2.10) / 2) / W, 0.165 / H), ncol=2,
           frameon=False, fontsize=9, handlelength=1.0, handletextpad=0.3, columnspacing=0.6, labelspacing=0.2)
fig.text(0.5, 1 - 0.06 / H, TXT["title"], ha="center", va="top", fontsize=11, weight="bold", linespacing=1.15)

# ---- no two legends may overlap ----------------------------------------------------------
fig.canvas.draw(); r = fig.canvas.get_renderer()
bb_b, bb_c = leg_b.get_window_extent(r), leg_c.get_window_extent(r)
assert bb_b.x1 < bb_c.x0, f"legends overlap: panel b ends at {bb_b.x1:.0f}px, panel c starts at {bb_c.x0:.0f}px"

# ---- the shape rules, enforced (format §4.12) -------------------------------------------
w, h = fig.get_size_inches()
assert h / w <= 1.75, f"height/width {h / w:.2f} exceeds 1.75"
assert 0.75 <= h / w <= 1.0, f"TRUE ratio {h / w:.2f} outside the comfortable 0.75-1.0"
small = [(x.get_text(), x.get_fontsize()) for x in fig.findobj(Text)
         if x.get_visible() and x.get_text().strip() and x.get_fontsize() < MIN_PT]
assert not small, f"text under {MIN_PT} pt: {small[:4]}"
FIGURES.mkdir(exist_ok=True)
fig.savefig(FIGURES / TXT["out"], dpi=DPI)
print(f"written {TXT['out']}  {w:.1f} x {h:.2f} in  (ratio {h / w:.2f}); 8 countries {S[0]['wa']:.2f} -> {S[0]['wb']:.2f} h")
