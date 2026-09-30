"""
Download the public raw inputs, only if you want to rebuild data/ yourself
(python make_intermediate.py). Readers who only want to check the article's
numbers and figures do not need this: data/ already holds everything.

    pip install "cdsapi>=0.7.2" requests
    python download_raw.py

ERA5-Land needs a free Copernicus account and a token in ~/.cdsapirc:
    url: https://cds.climate.copernicus.eu/api
    key: <YOUR-PERSONAL-ACCESS-TOKEN>
and the dataset licence accepted once, in a browser, on the dataset page.

The population grid must be downloaded by hand (see README): Eurostat attaches
download conditions to it that you accept on its page.
"""
import requests, cdsapi
from config import RAW

RAW.mkdir(exist_ok=True)
AREAS = {"italy": [47.6, 6.0, 35.3, 19.0],       # N, W, S, E
         "seu":   [48.0, -10.0, 34.0, 30.0]}
YEARS = {"1980s": [str(y) for y in range(1980, 1990)],
         "2020s": [str(y) for y in range(2020, 2026)]}
c = cdsapi.Client()
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
