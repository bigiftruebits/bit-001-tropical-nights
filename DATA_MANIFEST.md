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
| `ne_10m_admin_0_countries.geojson` | https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_admin_0_countries.geojson (public domain) | 13,287,234 | `239eec57ac17f100a11e2536cffc56752c318b50ae765b0918ff7aab4ce8f255` |
| `grid_5km_surf.gpkg` | https://gisco-services.ec.europa.eu/grid/grid_5km_surf.gpkg (Eurostat GISCO; column `TOT_P_2021`, 290,443 cells, EU total 455.7 M) | 106,254,336 | `ff3ffa6ee7b5a9c4c62239089253a298a3810f6b7ee2dc512e649c28e33498a3` |
| `era5land_orography_italy.nc` (in `data/`, used only by `check_cities.py`) | ECMWF ERA5-Land documentation page, `geo_1279l4_0.1x0.1.grib2_v4_unpack.nc` | — | not re-downloaded in the 2026-10-01 rebuild |

## Verification (2026-10-01)

`make_intermediate.py` was run on the files above in an empty copy. Every file it writes to `data/` is **identical** to the shipped one (grids: maximum difference 0.0 and identical missing-value masks; `population_by_cell.csv`, `borders.geojson`, `frame_outlines.geojson`: identical), and `check_numbers.py` passes 48 of 48 on the rebuilt data.

## Citations and licences

- ERA5-Land monthly averaged data: Muñoz Sabater, J. (2019), Copernicus Climate Change Service (C3S) Climate Data Store, doi:10.24381/cds.68d2bb30. Attribution required: "Generated using Copernicus Climate Change Service information 2026". Licence: Copernicus licence.
- Eurostat GISCO 5 km grid, © European Union, Eurostat. Eurostat's census-grid page states that EU copyright rules apply and that the licence would be CC BY 4.0. `TOT_P_2021` is 2021 census population, so **CC BY 4.0 is assumed** for `grid_5km_surf.gpkg` and for the derived `data/population_by_cell.csv` (the file itself carries no licence text; not confirmed in writing with Eurostat). Attribution: © European Union, Eurostat.
- Natural Earth: public domain.
