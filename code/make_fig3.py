"""
Draw Figure 3 (TRUE): the basin maps and the population bands, panels a-c.

Reads data/; writes figures/. Lettered composite; phone-sized and checked
like Figure 1.

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
TXT = {"en": dict(title="Night-time relief is scarcest\nwhere people live", cbar="hours of relief, of 8",
                  c="People by hours of relief", xpop="% of population", dec=lambda v: f"{v:.1f}",
                  bands=["no relief (0 h)", "under 4 h", "4–8 h", "full 8 h"],
                  focus=[("Greece", "greece"), ("Italy", "italy"), ("Spain", "spain")],
                  names={}, out="fig-001-true-hours-of-relief.png"),
       "it": dict(title="Il sollievo notturno è più scarso\nproprio dove vive la gente", cbar="ore di sollievo, su 8",
                  c="Popolazione per ore di sollievo", xpop="% della popolazione",
                  dec=lambda v: f"{v:.1f}".replace(".", ","),
                  bands=["nessun sollievo (0 h)", "meno di 4 h", "4–8 h", "8 h piene"],
                  focus=[("Grecia", "greece"), ("Italia", "italy"), ("Spagna", "spain")],
                  names={"Milan": "Milano", "Rome": "Roma", "Athens": "Atene", "Algiers": "Algeri"},
                  out="fig-001-true-hours-of-relief-it.png")}[LANG]
CITIES = [  # name, lon, lat, dx, dy (points), ha
    ("Madrid", -3.70, 40.42, 3, 3, "left"), ("Milan", 9.19, 45.46, 3, 3, "left"),
    ("Rome", 12.50, 41.90, 3, 3, "left"), ("Athens", 23.73, 37.98, -3, 3, "right"),
    ("Algiers", 3.06, 36.75, 3, -4, "left")]
BANDS = ["#7a1f0a", "#e08a5a", "#a9cfe0", "#2f6d8c"]          # 0 h, <4 h, 4-8 h, full 8 h
W, DPI, MIN_PT = 4.4, 450, 9.0
# --------------------------------------------------------------------------------------
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "xtick.labelsize": 9, "ytick.labelsize": 9})
HALO = [pe.withStroke(linewidth=2.2, foreground="white")]
A = xr.open_dataarray(DATA / "seu_relief_1980s.nc"); B = xr.open_dataarray(DATA / "seu_relief_2020s.nc")
OUT = json.load(open(DATA / "frame_outlines.geojson")); pop = pd.read_csv(DATA / "population_by_cell.csv")

def stats(d):
    sel = lambda F: F.sel(latitude=xr.DataArray(d.lat.values), longitude=xr.DataArray(d.lon.values), method="nearest").values
    a, b, w = sel(A), sel(B), d.population.values
    bands = lambda v: [w[v < .5].sum(), w[(v >= .5) & (v < 4)].sum(), w[(v >= 4) & (v < 7.5)].sum(), w[v >= 7.5].sum()]
    return dict(wa=np.average(a, weights=w), wb=np.average(b, weights=w),
                ba=np.array(bands(a)) / w.sum() * 100, bb=np.array(bands(b)) / w.sum() * 100)
S = {k: stats(pop[pop.country == k]) for _, k in TXT["focus"]}

W0, S0, E0, N0 = FRAME; asp = 1 / np.cos(np.deg2rad((S0 + N0) / 2))
MW = W - 0.16; MH = MW * (N0 - S0) * asp / (E0 - W0)
BAR_H = 1.42
H = 0.36 + BAR_H + 0.30 + 0.40 + 0.35 + 0.45 + MH + 0.06 + MH + 0.58
fig = plt.figure(figsize=(W, H))
inch = lambda x, y, w, h: [x / W, y / H, w / W, h / H]

yb = 0.36 + BAR_H + 0.30 + 0.40 + 0.35 + 0.45                  # bottom of map b
for letter, f, period, y in (("a", A, "1980–1989", yb + MH + 0.06), ("b", B, "2020–2025", yb)):
    ax = fig.add_axes(inch(0.08, y, MW, MH))
    m = ax.pcolormesh(f.longitude, f.latitude, f.values, cmap="YlGnBu", vmin=0, vmax=8, shading="auto")
    for geo in OUT.values():
        gg = shape(geo)
        for p in (gg.geoms if gg.geom_type == "MultiPolygon" else [gg]):
            x, yy = p.exterior.xy; ax.plot(x, yy, color="#333", lw=.3, zorder=4)
    for n, lo, la, dx, dy, ha in CITIES:
        ax.plot(lo, la, "o", ms=2.4, mfc="white", mec="k", mew=.6, zorder=5)
        ax.annotate(TXT["names"].get(n, n), (lo, la), xytext=(dx, dy), textcoords="offset points", fontsize=9,
                    weight="bold", ha=ha, va="bottom" if dy > 0 else "top", zorder=6, path_effects=HALO,
                    annotation_clip=True)
    ax.set_aspect(asp); ax.set_xlim(W0, E0); ax.set_ylim(S0, N0); ax.set_xticks([]); ax.set_yticks([])
    [s.set_linewidth(.5) for s in ax.spines.values()]
    ax.text(0.012, 0.965, f"{letter}  {period}", transform=ax.transAxes, fontsize=10, weight="bold",
            va="top", ha="left", zorder=7, path_effects=HALO)
cax = fig.add_axes(inch(0.6, yb - 0.22, W - 1.2, 0.10))
cb = fig.colorbar(m, cax=cax, orientation="horizontal"); cb.set_ticks(range(0, 9, 2))
cb.ax.tick_params(labelsize=9, length=2); cb.set_label(TXT["cbar"], fontsize=9, labelpad=2)

# (c) four bands per country and period; the label carries the average hours per person
ax = fig.add_axes(inch(1.62, 0.36, W - 1.62 - 0.12, BAR_H))
ticks, labels, pos = [], [], 0
for name, k in TXT["focus"]:
    for per, band, mean in (("1980–89", S[k]["ba"], S[k]["wa"]), ("2020–25", S[k]["bb"], S[k]["wb"])):
        left = 0
        for v, c in zip(band, BANDS):
            ax.barh(pos, v, left=left, color=c, height=.78, edgecolor="white", lw=.5)
            if v >= 9:
                ax.text(left + v / 2, pos, f"{v:.0f}", ha="center", va="center", fontsize=9, weight="bold",
                        color="#20404f" if c == BANDS[2] else "white")
            left += v
        ticks.append(pos); labels.append(f"{name}, {per} ({TXT['dec'](mean)} h)"); pos += 1
    pos += 0.45
ax.set_yticks(ticks); ax.set_yticklabels(labels); ax.invert_yaxis(); ax.set_ylim(pos - .2, -.6)
ax.set_xlim(0, 100); ax.set_xticks([0, 50, 100]); ax.set_xlabel(TXT["xpop"], fontsize=9, labelpad=2)
ax.tick_params(length=2); [ax.spines[s].set_visible(False) for s in ("top", "right")]
fig.text(0.10 / W, (0.36 + BAR_H + 0.30 + 0.40 + 0.05) / H, f"c  {TXT['c']}", fontsize=10, weight="bold", va="bottom")
hh = [plt.Rectangle((0, 0), 1, 1, color=c) for c in BANDS]
fig.legend(hh, TXT["bands"], loc="center", bbox_to_anchor=(0.5, (0.36 + BAR_H + 0.30 + 0.18) / H), ncol=2,
           frameon=False, fontsize=9, handlelength=1.1, handletextpad=0.4, columnspacing=1.2, labelspacing=0.3)
fig.text(0.5, 1 - 0.06 / H, TXT["title"], ha="center", va="top", fontsize=11, weight="bold", linespacing=1.15)

# ---- the phone rule, enforced -----------------------------------------------------------
w, h = fig.get_size_inches()
assert h / w <= 1.75, f"height/width {h / w:.2f} exceeds 1.75"
small = [(x.get_text(), x.get_fontsize()) for x in fig.findobj(Text)
         if x.get_visible() and x.get_text().strip() and x.get_fontsize() < MIN_PT]
assert not small, f"text under {MIN_PT} pt: {small[:4]}"
FIGURES.mkdir(exist_ok=True)
fig.savefig(FIGURES / TXT["out"], dpi=DPI)
print(f"written {TXT['out']}  {w:.1f} x {h:.2f} in  (ratio {h / w:.2f})")
