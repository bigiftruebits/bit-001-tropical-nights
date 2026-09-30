# BIG IF TRUE #001 — code and data

Everything needed to check *"Southern Europe has stopped cooling down at
night"* (English) / *"L'Europa meridionale ha smesso di rinfrescarsi di notte"*
(Italian): every figure, and every number the article prints.

Author: Riccardo Gallotti, Fondazione Bruno Kessler (FBK).
Code written and run by Claude Opus 5 (Anthropic), working from the author's
instructions.

Site with the figures: https://bigiftruebits.github.io/bit-001-tropical-nights/

## Cards on the table

- **Who did what:** code written and run by Claude Opus 5 (Anthropic) under the author's direction; the author set the questions, framing and editorial choices. The code was not re-read line by line and nothing is peer-reviewed.
- **Errors found and fixed:** 17 entries in [`NOTES.md`](NOTES.md).
- **Numbers:** every number in [`KEY_NUMBERS.md`](KEY_NUMBERS.md); `check_numbers.py` re-derives 48 of them.
- **Peer-reviewed work on the same question:** Vavassori, Žgela & Brovelli, *Applied Geomatics* 18:84 (2026), open access (the benchmark).
- **Sources behind the health and cooling statements:** Murage, Hajat & Kovats, *Environmental Epidemiology* (London, 1993–2015) and the nationwide Japanese analysis in *Environmental Health Perspectives* 131 (2023) on night-time heat and mortality; de Munck et al., *Int. J. Climatology* 33 (2013), Salamanca et al., *J. Geophys. Res. Atmos.* 119 (2014) and the IEA's *The Future of Cooling* (2018) on air conditioning.
- **Code and data:** open, in this repository.
- **How to cite:** Zenodo version DOI, *added after the first tagged release.* Cite the DOI, not the post.

**Reproduced it, or found a difference?** Open an issue titled "Reproduced" or "Mismatch" with what you ran and what you got.

## Check the article in three commands

```
pip install -r requirements.txt
cd code
python check_numbers.py        # recomputes the article's numbers, PASS/FAIL each
python make_fig1.py en         # and make_fig2.py, make_fig3.py; "it" for Italian
python check_cities.py         # does each quoted place's value describe the place?
```

`check_numbers.py` reads only `data/` and compares 48 numbers with the values
printed in the article. On the published data all 48 pass. The figure scripts
redraw the published figures, in both languages, pixel for pixel. Nothing is
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
| Copernicus Climate Change Service, ERA5-Land monthly averaged reanalysis by hour of day, 2 m temperature | temperatures | Copernicus licence; attribution required — "Generated using Copernicus Climate Change Service information 2026" |
| Eurostat GISCO, 5 km statistical grid with 2021 census population (`grid_5km_surf.gpkg`, `TOT_P_2021`), https://ec.europa.eu/eurostat/web/gisco/geodata/grids | population | © European Union, Eurostat. Eurostat attaches download conditions to its population grids, which are accepted on its page; GEOSTAT data are for non-commercial use. `population_by_cell.csv` is derived from this grid |
| Natural Earth 1:10m admin-0 countries | country outlines | public domain |

## What cannot be checked from `data/` alone

Two statements in the article's limitations rest on inputs not in this
package, and say so here rather than pass silently:

- the **±0.6 °C** sampling uncertainty on the warming, which comes from
  resampling the raw summers year by year;
- **June +3.2 °C, September +1.0 °C**, which needs a monthly-means download
  that includes September, and was computed in an earlier run that could not be
  repeated after its working files were lost.

## Licence

Code: MIT. Text of the article and figures: © Riccardo Gallotti. Data: as in the
table above.
