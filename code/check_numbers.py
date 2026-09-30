"""
Recompute every number in BIG IF TRUE #001 from the shared data in data/, and
compare each one with the value printed in the article.

    python check_numbers.py

Reads only data/. Prints one line per number: PASS if it rounds to the
published value, FAIL otherwise. A FAIL is a finding: please report it.

Author: Riccardo Gallotti (FBK). Code by Claude Opus 5 under his direction.
"""
import json
import numpy as np, pandas as pd, xarray as xr
from shapely.geometry import shape, Point
from shapely.prepared import prep
from config import DATA

CITIES = {"Rome": (12.4964, 41.9028), "Milan": (9.19, 45.4642), "Naples": (14.2681, 40.8518),
          "Turin": (7.6869, 45.0703), "Palermo": (13.3615, 38.1157), "Bologna": (11.3426, 44.4949),
          "Troina": (14.5975, 37.7847), "Crema": (9.686, 45.363)}
results = []


def check(label, value, published, decimals):
    # "rounds to the published value": within half a unit of its last digit.
    # Stated explicitly so the result never depends on how ties are broken.
    ok = abs(value - published) <= 0.5 * 10 ** -decimals + 1e-9
    results.append(ok)
    print(f"  {'PASS' if ok else 'FAIL'}  {label:62s} {value:9.{decimals + 1}f}   published {published}")


def at(field, lon, lat, r=0.6):
    """Value of the nearest valid land cell (a city's own cell may be sea)."""
    s = field.sel(latitude=slice(lat + r, lat - r), longitude=slice(lon - r, lon + r))
    L, A = np.meshgrid(s.longitude.values, s.latitude.values)
    d = np.where(np.isnan(s.values), np.inf, (L - lon) ** 2 + (A - lat) ** 2)
    return float(s.values[np.unravel_index(np.argmin(d), d.shape)])


def inside(field, geom):
    g = prep(geom)
    lon, lat = np.meshgrid(field.longitude.values, field.latitude.values)
    m = np.fromiter((g.contains(Point(x, y)) for x, y in zip(lon.ravel(), lat.ravel())),
                    bool, lon.size).reshape(lon.shape)
    return m & ~np.isnan(field.values)


load = lambda n: xr.open_dataarray(DATA / n)
tA, tB = load("italy_tropical_1980s.nc"), load("italy_tropical_2020s.nc")
iA, iB = load("italy_relief_1980s.nc"), load("italy_relief_2020s.nc")
sA, sB = load("seu_relief_1980s.nc"), load("seu_relief_2020s.nc")
borders = {k: shape(v) for k, v in json.load(open(DATA / "borders.geojson")).items()}
pop = pd.read_csv(DATA / "population_by_cell.csv")

print("\nBIG — Italy")
v = inside(tA, borders["italy"])
# "the share of Italy where the typical summer night stays above 20 °C": share of
# Italy's land cells where at least half of the summer has a tropical average night
check("land where the typical summer night stays > 20 °C, 1980s (%)", np.mean(tA.values[v] >= 50) * 100, 6, 0)
check("land where the typical summer night stays > 20 °C, 2020s (%)", np.mean(tB.values[v] >= 50) * 100, 33, 0)
check("Rome, share of the summer with tropical nights, 1980s (%)", at(tA, *CITIES["Rome"]), 7, 0)
check("Rome, share of the summer with tropical nights, 2020s (%)", at(tB, *CITIES["Rome"]), 73, 0)
check("Milan, share of the summer with tropical nights, 2020s (%)", at(tB, *CITIES["Milan"]), 22, 0)

print("\nAnecdote — Troina and Crema (hours of relief)")
tr0, tr1 = at(iA, *CITIES["Troina"]), at(iB, *CITIES["Troina"])
cr0, cr1 = at(iA, *CITIES["Crema"]), at(iB, *CITIES["Crema"])
check("gap Troina - Crema, 1980s (h)", tr0 - cr0, 0.9, 1)
check("gap Troina - Crema, 2020s (h)", tr1 - cr1, 3.3, 1)

print("\nIF — Figure 2 cities (tropical share %, hours of relief)")
PUB = {"Rome": (7, 73, 5.0, 1.6, 3.4), "Bologna": (3, 62, 6.1, 1.9, 4.2), "Naples": (47, 78, 3.5, 1.0, 2.4),
       "Palermo": (61, 84, 2.8, 0.9, 2.0), "Milan": (0, 22, 7.5, 3.4, 4.2), "Turin": (0, 6, 7.9, 5.3, 2.6)}
for c, (ta, tb, ra, rb, lost) in PUB.items():
    a, b, x, y = at(tA, *CITIES[c]), at(tB, *CITIES[c]), at(iA, *CITIES[c]), at(iB, *CITIES[c])
    check(f"{c}: tropical share 1980s", a, ta, 0); check(f"{c}: tropical share 2020s", b, tb, 0)
    check(f"{c}: relief lost (h)", x - y, lost, 1)

print("\nTRUE — people, not territory")
cell = lambda F, d: F.sel(latitude=xr.DataArray(d.lat.values), longitude=xr.DataArray(d.lon.values),
                          method="nearest").values
def per_person(d):
    a, b, w = cell(sA, d), cell(sB, d), d.population.values
    return a, b, w
for ck, (pa, pb) in {"italy": (6.1, 3.2), "spain": (5.6, 3.4), "greece": (3.1, 1.3)}.items():
    a, b, w = per_person(pop[pop.country == ck])
    check(f"{ck}: hours of relief per person, 1980s", np.average(a, weights=w), pa, 1)
    check(f"{ck}: hours of relief per person, 2020s", np.average(b, weights=w), pb, 1)
a, b, w = per_person(pop[pop.country == "italy"])
check("Italy: share with at least 4 h, 1980s (four in five, %)", w[a >= 4].sum() / w.sum() * 100, 79, 0)
check("Italy: share with under 4 h, 2020s (two in three, %)", w[b < 4].sum() / w.sum() * 100, 67, 0)
check("Italy keeps about half of its relief (%)", np.average(b, weights=w) / np.average(a, weights=w) * 100, 53, 0)
a, b, w = per_person(pop[pop.country == "greece"])
check("Greece: population with no relief (true tropical night), 1980s (%)", w[a < 0.5].sum() / w.sum() * 100, 3, 0)
check("Greece: population with no relief (true tropical night), 2020s (%)", w[b < 0.5].sum() / w.sum() * 100, 31, 0)

a, b, w = per_person(pop)
mA, mB = np.average(a, weights=w), np.average(b, weights=w)
check("8 countries: population (millions)", w.sum() / 1e6, 135, 0)
check("8 countries: hours of relief per person, 1980s", mA, 5.9, 1)
check("8 countries: hours of relief per person, 2020s", mB, 3.6, 1)
check("8 countries: loss per person per night (h)", mA - mB, 2.3, 1)
check("southern Europe keeps three of every five hours (%)", mB / mA * 100, 61, 0)
check("person-hours lost per summer night (millions)", (w * (a - b)).sum() / 1e6, 308, 0)
check("full cool nights lost per person per summer", (mA - mB) * 92 / 8, 26, 0)
check("share of a lifetime's nights (%)", (mA - mB) * 92 / 8 / 365.25 * 100, 7, 0)
check("share with under 4 h, 1980s (%)", w[a < 4].sum() / w.sum() * 100, 24, 0)
check("share with under 4 h, 2020s (%)", w[b < 4].sum() / w.sum() * 100, 62, 0)
check("share with a full 8 h, 1980s (%)", w[a >= 7.5].sum() / w.sum() * 100, 38, 0)
check("share with a full 8 h, 2020s (%)", w[b >= 7.5].sum() / w.sum() * 100, 17, 0)

print(f"\n{sum(results)} of {len(results)} numbers reproduce the published values.")
print("\nNot reproducible from data/ alone, by design (they need the raw downloads):")
print("  - the ±0.6 °C sampling uncertainty (year-by-year bootstrap of the raw temperatures)")
print("  - June +3.2 °C / September +1.0 °C (needs a monthly-means download that includes September)")
