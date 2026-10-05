# BIG IF TRUE #001 — code and data

Everything needed to check *"Southern Europe has stopped cooling down at
night"* (English) / *"L'Europa meridionale ha smesso di rinfrescarsi di notte"*
(Italian): every figure, and every number the article prints.

Author: Riccardo Gallotti, Fondazione Bruno Kessler (FBK).
Figures and a short guide: https://bigiftruebits.github.io/bit-001-tropical-nights/
How to cite: one Zenodo record holds this issue's code and data; cite its DOI, not the post. DOI: [10.5281/zenodo.23158810](https://doi.org/10.5281/zenodo.23158810).
Code written by Claude (Anthropic), working from the author's instructions:
Claude Opus 5, then Claude Opus 5.5, in a regular Claude chat (analysis and
writing); this repository set up in Claude Code, almost entirely by Claude
Sonnet 5.5. Usage, measured where it could be and declared unknown where it
could not: `USAGE.md`.

## Check the article in three commands

```
pip install -r requirements.txt
cd code
python check_numbers.py        # recomputes the article's numbers, PASS/FAIL each
python make_fig1.py en         # and make_fig2.py, make_fig3.py; "it" for Italian
python check_cities.py         # does each quoted place's value describe the place?
```

`check_numbers.py` reads only `data/` and runs 68 checks against the values
printed in the article, including the sampling uncertainty, which it recomputes
by resampling the summers year by year (fixed seed). On the published data all 68 pass. The figure scripts
redraw the published figures, in both languages, from `data/`: same data, labels and colours. Exact pixel positions of titles and margins can differ by a few pixels between matplotlib versions (a 2026-10-04 test with matplotlib 3.11.2 showed this; the IF figures came out 1 px taller), so compare the figures by eye or by their data, not by checksum. Nothing is
downloaded and no account is needed.

A FAIL, or a figure that differs, is a finding. Please report it: the article's
receipts promise that errors found will be recorded in the bug log
(`NOTES.md`), and this package exists so that they can be found.

## What is in `data/`

| file | what it holds |
|---|---|
| `italy_relief_{1980s,2020s}.nc` | hours of relief, Italy grid, June–August mean |
| `italy_tropical_{1980s,2020s}.nc` | share of summer months with a tropical average night (%) |
| `seu_relief_{1980s,2020s}.nc` | hours of relief, southern-Europe grid (Figure 3, all population figures) |
| `population_by_cell.csv` | people assigned to each southern-Europe grid cell, eight countries, 134.9 million |
| `borders.geojson` | outlines of the eight countries counted |
| `frame_outlines.geojson` | every country outline inside Figure 3's frame |
| `summers_by_country.csv` | one row per country and summer: mean temperature and hours of relief per person — for the uncertainty |
| `italy_monthly_mean_temp.csv` | Italy's mean temperature for every month of the sixteen years (ERA5-Land monthly means) |
| `era5land_orography_italy.nc` | ERA5-Land's own terrain height, for `check_cities.py` |

All grids are ERA5-Land at 0.1° (~9 km). Periods: June–August 1980–1989 (ten
summers) and 2020–2025 (six).

**Definitions.** *Hours of relief*: of the eight coldest hours of each month's
average daily cycle, how many stay below 20 °C; eight is a good night, zero a
tropical night. *Tropical share*: the percentage of summer months whose average
night never drops below 20 °C — months, not individual nights. Months are
weighted by their days (June 30, July and August 31). *The share of Italy where
the typical summer night stays above 20 °C* (6% → 33%): the share of Italy's
land cells where at least half of the summer has a tropical average night.

**Population.** Each 5 km cell of Eurostat's 2021 census grid is assigned to the
nearest land cell of the climate grid inside its own country; cells more than
50 km from any land cell are dropped, which removes the Canary Islands.

## Rebuilding `data/` from the public sources

Not needed to check the article, but possible: `python download_raw.py`, then
save the Eurostat grid by hand (below), then `python make_intermediate.py`.
Paths are set in `code/config.py`; raw files go in `raw/`.

| source | what | licence |
|---|---|---|
| Copernicus Climate Change Service, ERA5-Land monthly averaged reanalysis by hour of day, 2 m temperature | temperatures | CC-BY (as shown on the CDS dataset page, read 2026-10-04); credit: "Generated using Copernicus Climate Change Service information 2026", doi:10.24381/cds.68d2bb30 |
| Eurostat GISCO, 5 km statistical grid with 2021 census population (`grid_5km_surf.gpkg`, `TOT_P_2021`), https://ec.europa.eu/eurostat/web/gisco/geodata/grids | population | © European Union, Eurostat. CC BY 4.0, as Eurostat's census-grid 2021 entry states ("EU copyright rules apply, while the licence would be under CC-BY 4.0"; read 2026-10-04, screenshot in `licences/`). The older non-commercial conditions apply to the 2006 and 2011 grids. `population_by_cell.csv` is derived from this grid |
| Natural Earth 1:10m admin-0 countries | country outlines | public domain |

Verified 2026-10-04: with `download_raw.py` (which also fetches `italy_monthly_means.nc`, a few MB) and the Eurostat grid saved by hand, `make_intermediate.py` rebuilds every file in `data/` identically (see `DATA_MANIFEST.md`).

## What is and isn't checked

Every number the article prints is checked from `data/` as shipped — 68 checks,
including the ±0.7 °C sampling uncertainty (±0.9 °C in Greece), which is
recomputed by resampling the summers year by year, and the month-by-month
claims (June warmed most, September least), from all twelve months of
ERA5-Land monthly means.

## Licence

Two licences (decided 2026-10-05):

- **Code: MIT** (`LICENSE`): the scripts in `code/`.
- **Everything else we created: CC BY 4.0** (`DATA_LICENSE.md`): the derived data tables in `data/`, the figures, the article texts and the documentation. Credit: Riccardo Gallotti, Fondazione Bruno Kessler.
- **Third-party data keep their providers' licences**, as in the table above and in `DATA_MANIFEST.md` (ERA5-Land CC-BY, the Eurostat 2021 grid CC BY 4.0 as stated by Eurostat, Natural Earth public domain).
