"""Figure 2 — IF: the same cities measured two ways. Phone-sized.

    python make_fig2.py en|it        -> figures/fig-001-if-hours-of-relief[-it].png

One test, as IF requires (§4.9): six cities, ordered by how much their tropical
nights rose, measured first by tropical nights and then by hours of relief, in
the same rows. Drawn 4.4 in wide, no text under 9 pt, height <= 1.75 x width
(§4.12), enforced below. Reads data/ only.

Author: Riccardo Gallotti (FBK). Code by Claude Opus 5.5 under his direction.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DATA, FIGURES
import numpy as np, pandas as pd, xarray as xr
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.text import Text

LANG = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("en", "it") else "en"
# ---- everything a reader might want to change, in one table -------------------------
TXT = {"en": dict(title="Tropical nights miss where\ncool air is being lost", trop="Tropical nights",
                  rel="Hours of relief", xtrop="share of the summer that is a tropical night",
                  xrel="hours of relief (of 8)", then="1980s", now="2020s", names={},
                  out="fig-001-if-hours-of-relief.png"),
       "it": dict(title="Le notti tropicali non mostrano\ndove si perde l’aria fresca", trop="Notti tropicali",
                  rel="Ore di sollievo", xtrop="estate con notti tropicali",
                  xrel="ore di sollievo (su 8)", then="1980–1989", now="2020–2025",
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

ROW, AX_H = 0.29, 0.29 * len(t)
H = 0.42 + AX_H + 0.30 + 0.50 + AX_H + 0.30 + 0.30 + 0.62
fig = plt.figure(figsize=(W, H))
inch = lambda x, y, w, h: [x / W, y / H, w / W, h / H]
X0, XW, XV = 1.05, 2.30, 3.47             # axes left, axes width, value column (inches)

def panel(y0, title, a, b, xmax, ticks, ticklabels, xlabel, value):
    """a = 1980s (blue), b = 2020s (red), always."""
    ax = fig.add_axes(inch(X0, y0, XW, AX_H))
    for i, r in t.iterrows():
        ax.plot([a[i], b[i]], [i, i], color=GREY, lw=3.2, solid_capstyle="round", zorder=1)
        ax.scatter(a[i], i, s=34, color=BLUE, zorder=3); ax.scatter(b[i], i, s=34, color=RED, zorder=3)
        fig.text(XV / W, (y0 + AX_H * (len(t) - 0.5 - i) / len(t)) / H, value(r), fontsize=9,
                 weight="bold", va="center")
    ax.set_yticks(range(len(t))); ax.set_yticklabels([TXT["names"].get(c, c) for c in t.city])
    ax.invert_yaxis(); ax.set_ylim(len(t) - .5, -.5)
    ax.set_xlim(-.03 * xmax, xmax); ax.set_xticks(ticks); ax.set_xticklabels(ticklabels)
    ax.set_xlabel(xlabel, fontsize=9, labelpad=2); ax.grid(axis="x", alpha=.3); ax.set_axisbelow(True)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.tick_params(length=2)
    fig.text(0.10 / W, (y0 + AX_H + 0.08) / H, title, fontsize=10, weight="bold", va="bottom")

yB = 0.42; yA = yB + AX_H + 0.30 + 0.50
panel(yA, TXT["trop"], t.tA, t.tB, 104, [0, 50, 100], ["0%", "50%", "100%"], TXT["xtrop"],
      lambda r: f"{r.tA:.0f}% → {r.tB:.0f}%")
panel(yB, TXT["rel"], t.rA, t.rB, 8.3, [0, 2, 4, 6, 8], ["0", "2", "4", "6", "8"], TXT["xrel"],
      lambda r: f"−{dec(r.lost)} h")
h1 = plt.Line2D([], [], marker="o", ls="", color=BLUE, ms=5.5, label=TXT["then"])
h2 = plt.Line2D([], [], marker="o", ls="", color=RED, ms=5.5, label=TXT["now"])
fig.legend(handles=[h1, h2], loc="center", bbox_to_anchor=(0.5, (H - 0.62 - 0.13) / H), ncol=2,
           frameon=False, fontsize=9, handletextpad=0.3, columnspacing=1.4)
fig.text(0.5, 1 - 0.06 / H, TXT["title"], ha="center", va="top", fontsize=11, weight="bold", linespacing=1.15)

# ---- the phone rule, enforced -----------------------------------------------------------
w, h = fig.get_size_inches()
assert h / w <= 1.75, f"height/width {h / w:.2f} exceeds 1.75"
small = [(x.get_text(), x.get_fontsize()) for x in fig.findobj(Text)
         if x.get_visible() and x.get_text().strip() and x.get_fontsize() < MIN_PT]
assert not small, f"text under {MIN_PT} pt: {small[:4]}"
FIGURES.mkdir(exist_ok=True)
t.round(2).to_csv(FIGURES / "fig2_cities.csv", index=False)
fig.savefig(FIGURES / TXT["out"], dpi=DPI)
print(f"written {TXT['out']}  {w:.1f} x {h:.2f} in  (ratio {h / w:.2f})")
