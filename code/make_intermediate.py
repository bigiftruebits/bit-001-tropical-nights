"""
Build the shared intermediate data in data/ from the raw downloads.

Reads raw/ (ERA5-Land, the Eurostat 2021 census grid, Natural Earth); writes
hours of relief and tropical-night maps per decade, population per grid cell,
the outlines, and the per-summer tables used for the uncertainty.

    python make_intermediate.py

BIG IF TRUE · tropical-nights · https://github.com/bigiftruebits/bit-001-tropical-nights
Author: Riccardo Gallotti (FBK). Code by Claude Opus 5, then Claude Opus 5.5, under his direction.
Licence: MIT (code); data licences in DATA_MANIFEST.md.
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
    per_summer_tables(out)


def per_summer_tables(pop):
    """One row per country and summer: national mean temperature (land cells in
    the country, all hours, day-weighted) and hours of relief per person. These
    let anyone redo the year-by-year resampling behind the article's uncertainty."""
    rows, monthly = [], []
    ne_borders = json.load(open(DATA / "borders.geojson"))
    for dec in ("1980s", "2020s"):
        da = xr.open_dataset(RAW / f"seu_{dec}.nc")["t2m"] - 273.15
        t = "valid_time" if "valid_time" in da.dims else "time"
        ym = (da[t].dt.year * 100 + da[t].dt.month).rename("ym")
        mean_t = da.groupby(ym).mean(t)                                  # monthly mean temperature
        below = (da < THRESHOLD_C).groupby(ym).sum(t, skipna=False)
        below = xr.where(below > SLEEP_HOURS, SLEEP_HOURS, below)
        f0 = da.isel({t: 0}); lon, lat = np.meshgrid(f0.longitude.values, f0.latitude.values)
        for key in ("italy", "spain", "greece"):
            g = prep(shape(ne_borders[key]))
            m = np.fromiter((g.contains(Point(x, y)) for x, y in zip(lon.ravel(), lat.ravel())),
                            bool, lon.size).reshape(lon.shape) & ~np.isnan(f0.values)
            d = pop[pop.country == key]
            sel = dict(latitude=xr.DataArray(d.lat.values), longitude=xr.DataArray(d.lon.values))
            for y in sorted(set(int(v // 100) for v in ym.values)):
                ks = [y * 100 + mo for mo in (6, 7, 8)]; w = np.array([30.0, 31.0, 31.0])
                tm = np.array([float(mean_t.sel(ym=k).values[m].mean()) for k in ks])
                rl = np.array([float(np.average(below.sel(ym=k).sel(**sel, method="nearest").values,
                                                weights=d.population.values)) for k in ks])
                rows.append(dict(country=key, year=y, jja_mean_temp_c=round(float((tm * w).sum() / w.sum()), 4),
                                 relief_per_person_h=round(float((rl * w).sum() / w.sum()), 4)))
                if key == "italy":
                    for k, v in zip(ks, tm):
                        monthly.append(dict(year=y, month=k % 100, mean_temp_c=round(v, 4)))
    # the eight countries together: the article's headline number and its range
    for dec in ("1980s", "2020s"):
        da = xr.open_dataset(RAW / f"seu_{dec}.nc")["t2m"] - 273.15
        t = "valid_time" if "valid_time" in da.dims else "time"
        ym = (da[t].dt.year * 100 + da[t].dt.month).rename("ym")
        below = xr.where((da < THRESHOLD_C).groupby(ym).sum(t, skipna=False) > SLEEP_HOURS, SLEEP_HOURS,
                         (da < THRESHOLD_C).groupby(ym).sum(t, skipna=False))
        sel = dict(latitude=xr.DataArray(pop.lat.values), longitude=xr.DataArray(pop.lon.values))
        for y in sorted(set(int(v // 100) for v in ym.values)):
            ks = [y * 100 + mo for mo in (6, 7, 8)]; w = np.array([30.0, 31.0, 31.0])
            rl = np.array([float(np.average(below.sel(ym=k).sel(**sel, method="nearest").values,
                                            weights=pop.population.values)) for k in ks])
            rows.append(dict(country="eight_countries", year=y, jja_mean_temp_c=float("nan"),
                             relief_per_person_h=round(float((rl * w).sum() / w.sum()), 4)))
    pd.DataFrame(rows).to_csv(DATA / "summers_by_country.csv", index=False)
    # All twelve months, if the monthly-means download is present (download_raw.py --months)
    mm = RAW / "italy_monthly_means.nc"
    if mm.exists():
        da = xr.open_dataset(mm)["t2m"] - 273.15; t = "valid_time" if "valid_time" in da.dims else "time"
        f0 = da.isel({t: 0}); lon, lat = np.meshgrid(f0.longitude.values, f0.latitude.values)
        g = prep(shape(ne_borders["italy"]))
        m = np.fromiter((g.contains(Point(x, y)) for x, y in zip(lon.ravel(), lat.ravel())),
                        bool, lon.size).reshape(lon.shape) & ~np.isnan(f0.values)
        monthly = [dict(year=int(v.dt.year), month=int(v.dt.month),
                        mean_temp_c=round(float(da.sel({t: v}).values[m].mean()), 4)) for v in da[t]]
    pd.DataFrame(monthly).to_csv(DATA / "italy_monthly_mean_temp.csv", index=False)
    print(f"per-summer tables written ({'all twelve months' if mm.exists() else 'June-August only'})")


if __name__ == "__main__":
    main()
