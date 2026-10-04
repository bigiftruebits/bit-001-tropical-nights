"""
Download the public raw inputs, to rebuild data/ from scratch.

Fetches ERA5-Land (Copernicus account needed), all twelve months for Italy,
and the Natural Earth outlines into raw/; says where to get the Eurostat
population grid by hand. Not needed to check the article: data/ is shipped.

    python download_raw.py            # everything
    python download_raw.py --months   # only the all-months file

BIG IF TRUE · tropical-nights · https://github.com/bigiftruebits/bit-001-tropical-nights
Author: Riccardo Gallotti (FBK). Code by Claude Opus 5, then Claude Opus 5.5, under his direction.
Licence: MIT (code); data licences in DATA_MANIFEST.md.
"""
import sys, requests, cdsapi
from config import RAW
MONTHS_ONLY = "--months" in sys.argv   # just the all-months file used for the month-by-month claims

RAW.mkdir(exist_ok=True)
AREAS = {"italy": [47.6, 6.0, 35.3, 19.0],       # N, W, S, E
         "seu":   [48.0, -10.0, 34.0, 30.0]}
YEARS = {"1980s": [str(y) for y in range(1980, 1990)],
         "2020s": [str(y) for y in range(2020, 2026)]}
c = cdsapi.Client()
mm = RAW / "italy_monthly_means.nc"
if not mm.exists():
    # All twelve months, plain monthly means: for "June warmed more than any other
    # month" and the September figures in the limitations (small, a few MB)
    c.retrieve("reanalysis-era5-land-monthly-means", {
        "product_type": ["monthly_averaged_reanalysis"], "variable": ["2m_temperature"],
        "year": YEARS["1980s"] + YEARS["2020s"], "month": [f"{m:02d}" for m in range(1, 13)],
        "time": ["00:00"], "area": AREAS["italy"],
        "data_format": "netcdf", "download_format": "unarchived"}, str(mm))
    print("got", mm.name)
if MONTHS_ONLY:
    sys.exit(0)
for region, area in AREAS.items():
    for dec, years in YEARS.items():
        out = RAW / f"{region}_{dec}.nc"
        if out.exists():
            print("have", out.name); continue
        c.retrieve("reanalysis-era5-land-monthly-means", {
            "product_type": ["monthly_averaged_reanalysis_by_hour_of_day"],
            "variable": ["2m_temperature"], "year": years, "month": ["06", "07", "08"],
            "time": [f"{h:02d}:00" for h in range(24)], "area": area,
            "data_format": "netcdf", "download_format": "unarchived"}, str(out))
        print("got", out.name)

ne = RAW / "ne_10m_admin_0_countries.geojson"
if not ne.exists():
    url = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
           "master/geojson/ne_10m_admin_0_countries.geojson")
    ne.write_bytes(requests.get(url, timeout=300).content); print("got", ne.name)

if not (RAW / "grid_5km_surf.gpkg").exists():
    print("\nStill needed, by hand: Eurostat GISCO 5 km statistical grid with 2021 census"
          "\npopulation (grid_5km_surf.gpkg, column TOT_P_2021), from"
          "\n  https://ec.europa.eu/eurostat/web/gisco/geodata/grids"
          f"\nSave it as {RAW / 'grid_5km_surf.gpkg'}")
