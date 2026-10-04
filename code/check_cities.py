"""
Does each quoted place's value describe the place? Reads data/ only.

For every city in the article: is its own grid cell land or sea, how far away is
the cell actually used, how high does ERA5-Land's terrain put that cell, and how
much do hours of relief vary across the land cells within 15 km? A large spread
means the city's value depends on which cell is picked.

    python check_cities.py

BIG IF TRUE · tropical-nights · https://github.com/bigiftruebits/bit-001-tropical-nights
Author: Riccardo Gallotti (FBK). Code by Claude Opus 5 under his direction.

Licence: MIT (code); data licences in DATA_MANIFEST.md."""
import numpy as np, pandas as pd, xarray as xr
from config import DATA

CITIES = [("Rome", 12.4964, 41.9028), ("Milan", 9.19, 45.4642), ("Naples", 14.2681, 40.8518),
          ("Turin", 7.6869, 45.0703), ("Palermo", 13.3615, 38.1157), ("Genoa", 8.9463, 44.4056),
          ("Bologna", 11.3426, 44.4949), ("Troina", 14.5975, 37.7847), ("Crema", 9.686, 45.363),
          ("Bari", 16.8719, 41.1171), ("Catania", 15.0873, 37.5079)]
rA = xr.open_dataarray(DATA / "italy_relief_1980s.nc"); rB = xr.open_dataarray(DATA / "italy_relief_2020s.nc")
H = xr.open_dataset(DATA / "era5land_orography_italy.nc")["elevation_m"]
LO, LA = np.meshgrid(rB.longitude.values, rB.latitude.values); land = ~np.isnan(rB.values)
rows = []
for n, lo, la in CITIES:
    km = np.hypot((LO - lo) * 111 * np.cos(np.deg2rad(la)), (LA - la) * 111)
    own = np.unravel_index(np.argmin(km), km.shape)
    used = np.unravel_index(np.argmin(np.where(land, km, np.inf)), km.shape)
    near = land & (km <= 15)
    rows.append(dict(city=n, own_cell="land" if land[own] else "SEA",
                     cell_used_km=round(float(km[used]), 1),
                     cell_height_m=round(float(H.sel(latitude=LA[used], longitude=LO[used], method="nearest"))),
                     relief_now=round(float(rB.values[used]), 1),
                     relief_within_15km=f"{rB.values[near].min():.1f}-{rB.values[near].max():.1f}",
                     spread_h=round(float(rB.values[near].max() - rB.values[near].min()), 1)))
print(pd.DataFrame(rows).to_string(index=False))
print("\nGenoa's own cell is sea; its nearest land cell sits in the hills behind the city,"
      "\nwhich is why it is not among the cities in Figure 2.")
