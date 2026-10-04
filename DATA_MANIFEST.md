# Data manifest

Every raw input needed to rebuild `data/`, with its source, retrieval date and checksum.
Retrieved **2026-10-01** with `code/download_raw.py` (ERA5-Land, Natural Earth) and by hand (Eurostat).
Raw files are not stored in this git repository (`raw/` is ignored); the issue's single Zenodo record (code and data together) includes the ERA5-Land and Natural Earth files.

| file | source | bytes | sha256 |
|---|---|---|---|
| `italy_1980s.nc` | Copernicus CDS, `reanalysis-era5-land-monthly-means`, `monthly_averaged_reanalysis_by_hour_of_day`, 2m_temperature, years 1980–1989, months 06–08, hours 00–23, area N47.6 W6 S35.3 E19 | 13,437,337 | `571e65de6eb56a7afe4dd2301f3721a9ca85acc8d45e13fd3d2b69eae0282ac7` |
| `italy_2020s.nc` | same, years 2020–2025 | 7,906,786 | `afb414874aea202257a7afa961f090fd4c4b20c31adaa57cf42de35016ce48b0` |
| `seu_1980s.nc` | same, years 1980–1989, area N48 W-10 S34 E30 | 49,748,299 | `6d7be6d5c4394c2e2b43ad9dc1a8020648f01d58d88a32390696ad2081e7c937` |
| `seu_2020s.nc` | same, years 2020–2025, area N48 W-10 S34 E30 | 29,724,078 | `bd12d9acc667ce9c5d6a96013b6283292342d8c45d044b850a2eb11604eb8303` |
| `italy_monthly_means.nc` | same dataset, product `monthly_averaged_reanalysis` (plain monthly means), 2m_temperature, all 12 months of 1980–1989 and 2020–2025, time 00:00, area N47.6 W6 S35.3 E19 (192 months). Downloaded 2026-10-04 with `download_raw.py --months`; backs the month-by-month claims | 3,121,249 | `bf5c3c799a194d723b2251492dd26a4c97c785533dffc6a7a67444c57060a1e0` |
| `ne_10m_admin_0_countries.geojson` | https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_admin_0_countries.geojson (public domain) | 13,287,234 | `239eec57ac17f100a11e2536cffc56752c318b50ae765b0918ff7aab4ce8f255` |
| `grid_5km_surf.gpkg` | https://gisco-services.ec.europa.eu/grid/grid_5km_surf.gpkg (Eurostat GISCO; column `TOT_P_2021`, 290,443 cells, EU total 455.7 M) | 106,254,336 | `ff3ffa6ee7b5a9c4c62239089253a298a3810f6b7ee2dc512e649c28e33498a3` |
| `era5land_orography_italy.nc` (in `data/`, used only by `check_cities.py`) | ECMWF ERA5-Land documentation page, `geo_1279l4_0.1x0.1.grib2_v4_unpack.nc` | — | not re-downloaded in the 2026-10-01 rebuild |

## Verification

- **2026-10-01:** `make_intermediate.py` was run on the four hourly ERA5-Land files, the Natural Earth file and the Eurostat grid in an empty copy; its outputs matched the then-shipped `data/`.
- **2026-10-04:** with the updated code and the added `italy_monthly_means.nc`, `make_intermediate.py` rebuilt every file it writes to `data/` identically to the release bundle's: the grids (maximum difference 0.0), `population_by_cell.csv`, `borders.geojson`, `frame_outlines.geojson`, `italy_monthly_mean_temp.csv` and `summers_by_country.csv`. `check_numbers.py` passes 64 of 64. `era5land_orography_italy.nc` is not rebuilt (it comes from ECMWF's documentation page and is used only by `check_cities.py`).
- **Figures:** redrawn from `data/` with matplotlib 3.11.2, they match the published ones in content but not to the pixel (titles and margins shift by a few pixels, and the IF figures are 1 px taller); see the README.

## Licences and credits (each read on the provider's page, with the date)

| source | licence | page read | credit |
|---|---|---|---|
| ERA5-Land (all five ERA5-Land files above come from this dataset, products `monthly_averaged_reanalysis_by_hour_of_day` and `monthly_averaged_reanalysis`) | **CC-BY**, as shown on the dataset page. The page gives the DOI but does not print the full attribution sentence or a redistribution statement. | https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land-monthly-means?tab=overview, read 2026-10-04 (the sister page https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=overview also shows CC-BY, DOI 10.24381/cds.e2161bac, read the same day) | Muñoz Sabater, J. (2019), ERA5-Land monthly averaged data from 1950 to present, Copernicus Climate Change Service (C3S) Climate Data Store, doi:10.24381/cds.68d2bb30. Credit line used here: "Generated using Copernicus Climate Change Service information 2026". |
| Eurostat GISCO 5 km grid, `TOT_P_2021` | **CC BY 4.0 assumed.** Eurostat's census-grid 2021 card says "EU copyright rules apply, while the licence would be under CC-BY 4.0". Seen by the author on 2026-10-01 (screenshot) on the census-grid page https://ec.europa.eu/eurostat/web/gisco/geodata/population-distribution/population-grids; the page text I fetched did not print the sentence, and the 5 km file itself carries no licence text. The editorial decision of 2026-10-04 is to rely on it. The older non-commercial conditions belong to the 2006 and 2011 grids (https://ec.europa.eu/eurostat/web/gisco/geodata/population-distribution, read 2026-10-01). Direct file: https://gisco-services.ec.europa.eu/grid/grid_5km_surf.gpkg (header-checked 2026-10-01, 106,254,336 bytes) | pages above, read 2026-10-01 | © European Union, Eurostat |
| Natural Earth 1:10m admin-0 countries | public domain ("All versions of Natural Earth raster + vector map data ... are in the public domain"; no attribution required) | https://www.naturalearthdata.com/about/terms-of-use/, read 2026-10-04 | "Made with Natural Earth" (optional) |
