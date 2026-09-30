"""
Build the shared intermediate data from the raw downloads.

Readers do NOT need to run this: its output is already in data/. It is here so
anyone can rebuild data/ from the public sources and check that step too.

Raw inputs (paths set in config.py -> RAW):
  ERA5-Land, monthly averaged reanalysis by hour of day, 2 m temperature, JJA
    italy_1980s.nc, italy_2020s.nc              box 47.5N 6E 35.5N 19E
    seu_1980s.nc,   seu_2020s.nc                box 48N -10E 34N 30E
  Eurostat GEOSTAT 2021, 5 km grid              grid_5km_surf.gpkg
  Natural Earth 1:10m admin-0 countries          ne_10m_admin_0_countries.geojson

Output (config.DATA):
  italy_relief_{1980s,2020s}.nc, italy_tropical_{1980s,2020s}.nc
  seu_relief_{1980s,2020s}.nc
  population_by_cell.csv      people assigned to each southern-Europe grid cell
  borders.geojson             outlines of the eight countries counted
  frame_outlines.geojson      every country outline inside the Figure 3 frame

Author: Riccardo Gallotti (FBK). Code by Claude Opus 5 under his direction.
"""
import json, sqlite3
import numpy as np, pandas as pd, xarray as xr
from shapely.geometry import shape, box, mapping, Point
from shapely.prepared import prep
from pyproj import Transformer
from scipy.spatial import cKDTree
from config import RAW, DATA, THRESHOLD_C, SLEEP_HOURS, COUNTRIES, FRAME, MAX_SNAP_KM


def indicators(path):
    """Hours of relief and tropical-night share, day-weighted over June-August.

    hours of relief: of the SLEEP_HOURS coldest hours of each month's mean daily
      cycle, how many stay below THRESHOLD_C (= min(hours below, 8)).
    tropical share: % of summer months whose mean night minimum is >= THRESHOLD_C.
    """
    da = xr.open_dataset(path)["t2m"] - 273.15
    t = "valid_time" if "valid_time" in da.dims else "time"
    ym = (da[t].dt.year * 100 + da[t].dt.month).rename("ym")
    below = (da < THRESHOLD_C).groupby(ym).sum(t, skipna=False)   # skipna=False: a sum
    below = xr.where(below > SLEEP_HOURS, SLEEP_HOURS, below)      # of NaN must stay NaN
    w = xr.where(below.ym % 100 == 6, 30.0, 31.0)
    relief = (below * w).sum("ym") / w.sum()
    trop = ((da.groupby(ym).min(t) >= THRESHOLD_C) * w).sum("ym") / w.sum() * 100
    sea = np.isnan(da.isel({t: 0}))
    clean = lambda o: o.where(~sea).drop_vars(
        [c for c in ("valid_time", "number", "expver") if c in o.coords], errors="ignore")
    return clean(relief).rename("relief_hours"), clean(trop).rename("tropical_share_pct")


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    for dec in ("1980s", "2020s"):
        r, t = indicators(RAW / f"italy_{dec}.nc")
        r.to_netcdf(DATA / f"italy_relief_{dec}.nc"); t.to_netcdf(DATA / f"italy_tropical_{dec}.nc")
        r, _ = indicators(RAW / f"seu_{dec}.nc")
        r.to_netcdf(DATA / f"seu_relief_{dec}.nc")
    print("indicator maps written")

    ne = json.load(open(RAW / "ne_10m_admin_0_countries.geojson"))["features"]
    fr = box(*FRAME)
    borders = {c["key"]: mapping(shape(f["geometry"]).intersection(fr))
               for f in ne for c in COUNTRIES if f["properties"]["NAME"] == c["ne_name"]}
    json.dump(borders, open(DATA / "borders.geojson", "w"))
    frame = {}
    for f in ne:
        g = shape(f["geometry"])
        if g.intersects(fr):
            c = g.intersection(fr)
            if not c.is_empty and c.area > 0.0005:
                frame[f["properties"]["NAME"]] = mapping(c)
    json.dump(frame, open(DATA / "frame_outlines.geojson", "w"))
    print("outlines written")

    # People -> grid cells: each 5 km GEOSTAT cell goes to the nearest valid land
    # cell of the climate grid inside its own country; cells more than
    # MAX_SNAP_KM away are dropped (this removes the Canary Islands).
    ref = xr.open_dataarray(DATA / "seu_relief_1980s.nc")
    lon, lat = np.meshgrid(ref.longitude.values, ref.latitude.values)
    land = ~np.isnan(ref.values)
    con = sqlite3.connect(RAW / "grid_5km_surf.gpkg")
    tr = Transformer.from_crs(3035, 4326, always_xy=True)
    rows = []
    for c in COUNTRIES:
        g = prep(shape(borders[c["key"]]))
        ins = np.fromiter((g.contains(Point(x, y)) for x, y in zip(lon.ravel(), lat.ravel())),
                          bool, lon.size).reshape(lon.shape)
        valid = ins & land
        tree = cKDTree(np.column_stack([lon[valid], lat[valid]]))
        pop = pd.read_sql(f"SELECT X_LLC, Y_LLC, TOT_P_2021 FROM grid_5km_surf "
                          f"WHERE CNTR_ID = '{c['geostat']}'", con)
        px, py = tr.transform(pop.X_LLC.values + 2500, pop.Y_LLC.values + 2500)
        d, idx = tree.query(np.column_stack([px, py]))
        km = d * 111 * np.cos(np.deg2rad(py.mean()))
        keep = km <= MAX_SNAP_KM
        cell = pd.DataFrame({"lat": lat[valid][idx[keep]], "lon": lon[valid][idx[keep]],
                             "population": pop.TOT_P_2021.to_numpy(float)[keep]})
        cell = cell.groupby(["lat", "lon"], as_index=False).population.sum()
        cell.insert(0, "country", c["key"])
        rows.append(cell)
        print(f"   {c['key']:9s} {cell.population.sum()/1e6:6.2f} M people on {len(cell):5d} cells"
              f"   (dropped {pop.TOT_P_2021.to_numpy(float)[~keep].sum()/1e6:.2f} M beyond {MAX_SNAP_KM:.0f} km)")
    out = pd.concat(rows)
    out["lat"] = out.lat.round(2); out["lon"] = out.lon.round(2)
    out.to_csv(DATA / "population_by_cell.csv", index=False)
    print(f"population_by_cell.csv: {out.population.sum()/1e6:.1f} M people")


if __name__ == "__main__":
    main()
