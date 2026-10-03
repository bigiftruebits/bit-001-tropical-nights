# Key numbers

All figures: hours of relief = of the 8 coldest hours of the day, how many stay below 20 °C.
JJA 2020–2025 vs 1980–1989. ERA5-Land 9 km, population-weighted with GEOSTAT 5 km.

## Aggregate — 8 Southern European EU member states

- population: 134.9 million
- relief per person: 5.93 h -> 3.64 h (loss 2.29 h)
- person-hours lost per summer night: 308 million
- the same, per person: 2.29 h/night x 92 nights = 211 hours = **26.3 full 8-hour cool nights, every summer** — 29% of the summer's 92 nights, the same 29% as the nightly loss of 2.29 of 8 hours
- as a share of life: 26.3 full cool nights a year out of 365 = **7.2% of all the nights of a life**, at today's rate — the same share whatever the length of the life
- aggregate over a whole summer: 28.4 billion person-hours (3.24 million person-years)
- no relief at all: 0.2% -> 5.8% of population
- under 4 hours: 23.5% -> 62.5% (exactly 62.498%, so **62%**, not 63%)
- full 8 hours: 37.7% -> 17.4%

## By country

| country | population (M) | 1980s | 2020s | lost | 0 h now | <4 h now |
|---|---|---|---|---|---|---|
| Malta | 0.5 | 0.98 | 0.00 | 0.98 | 100.0% | 100.0% |
| Greece | 10.4 | 3.08 | 1.29 | 1.80 | 31.2% | 93.8% |
| Spain | 44.9 | 5.61 | 3.42 | 2.19 | 3.5% | 71.8% |
| Italy | 57.9 | 6.08 | 3.23 | 2.84 | 4.2% | 66.7% |
| Croatia | 3.5 | 7.34 | 5.00 | 2.34 | 2.8% | 28.0% |
| Bulgaria | 6.1 | 7.71 | 5.39 | 2.32 | 0.0% | 29.7% |
| Portugal | 9.8 | 7.79 | 7.46 | 0.33 | 0.0% | 3.6% |
| Slovenia | 1.8 | 7.93 | 7.44 | 0.48 | 0.0% | 3.3% |

## Italy, seven largest cities (Figure 2)

| city | tropical nights (% of summer) | relief 1980s | relief 2020s | lost |
|---|---|---|---|---|
| Palermo | 84% | 2.8 h | 0.9 h | 2.0 h |
| Naples | 78% | 3.5 h | 1.0 h | 2.4 h |
| Rome | 73% | 5.0 h | 1.6 h | 3.4 h |
| Bologna | 62% | 6.1 h | 1.9 h | 4.2 h |
| Milan | 22% | 7.5 h | 3.4 h | 4.2 h |
| Genoa | 11% | 7.9 h | 5.9 h | 2.0 h |
| Turin | 6% | 7.9 h | 5.3 h | 2.6 h |

## Italy, seven largest cities — both measures as change (Figure 2, rebuilt)

Ordered by rise in tropical-night share. Re-run 2026-09-21 from the original uploads (`t2m_diurnal_a.nc`, `1787593538286_t2m_diurnal_b.nc`) with `code/make_fig2.py`; every relief value reproduces the earlier table exactly, so the 1980s tropical-night shares are now verified.

| city | tropical 1980s | tropical 2020s | change (percentage points) | relief 1980s | relief 2020s | lost |
|---|---|---|---|---|---|---|
| Rome | 7% | 73% | +66 | 5.0 h | 1.6 h | 3.4 h |
| Bologna | 3% | 62% | +58 | 6.1 h | 1.9 h | 4.2 h |
| Naples | 47% | 78% | +31 | 3.5 h | 1.0 h | 2.4 h |
| Palermo | 61% | 84% | +23 | 2.9 h | 0.9 h | 2.0 h |
| Milan | 0% | 22% | +22 | 7.5 h | 3.4 h | 4.2 h |
| Genoa *(excluded — own cell is sea)* | 0% | 11% | +11 | 7.9 h | 5.9 h | 2.0 h |
| Turin | 0% | 6% | +6 | 7.9 h | 5.3 h | 2.6 h |

- Verdict box ratio: Milan and Bologna lost 4.2 h against Naples 2.4 h (1.75x) and Palermo 2.0 h (2.1x) — "nearly twice", not "more than twice".

## City robustness check (2026-09-21)

Every city quoted in the article, checked against the land cells within 15 km. `check_cities.py`.

| city | own cell | cell used | relief today, nearby | spread | relief lost, nearby | tropical today, nearby |
|---|---|---|---|---|---|---|
| Rome | land | 0.4 km | 1.2-2.2 h | 0.9 h | 2.2-4.1 h | 62-78% |
| Milan | land | 4.0 km | 2.9-3.9 h | 1.0 h | 3.7-4.2 h | 17-34% |
| Naples | land | 6.0 km | 1.0-1.2 h | 0.2 h | 2.3-2.9 h | 78-78% |
| Turin | land | 3.5 km | 4.2-6.0 h | 1.8 h | 2.0-3.5 h | 0-11% |
| Palermo | land | 3.8 km | 0.9-2.0 h | 1.1 h | 2.0-3.3 h | 62-84% |
| Genoa | SEA | 11.1 km | 1.9-6.3 h | 4.4 h | 1.6-3.7 h | 11-67% |
| Bologna | land | 3.4 km | 1.7-3.4 h | 1.6 h | 3.9-4.3 h | 28-62% |
| Troina | land | 1.7 km | 1.4-6.8 h | 5.4 h | 1.1-3.4 h | 0-62% |
| Crema | land | 4.2 km | 2.0-3.1 h | 1.1 h | 3.9-4.3 h | 22-56% |
| Bari | land | 3.0 km | 0.4-1.0 h | 0.6 h | 1.8-2.8 h | 84-95% |
| Catania | land | 1.4 km | 0.3-2.0 h | 1.7 h | 1.1-3.5 h | 56-95% |

- **Genoa excluded from Figure 2**: own cell is sea; nearby land runs 1.9–6.3 h (coast to hills).
- Terrain check (ERA5-Land's own 0.1-degree terrain, `era5land_orography_italy.nc`): Troina's cell sits at 882 m against a town at ~1,120 m, with neighbours from 384 m (south, 1.4 h) to 1,119 m (north, 6.8 h); Palermo's cell 237 m against a city near sea level; Genoa's fallback cell 393 m. Crema 84 m, Milan 131 m, Turin 239 m, Rome 43 m match their towns.
- Differences between cities of about 0.5 h or less are within cell-to-cell uncertainty.
- Robust whichever nearby cells are used: Milan and Bologna lost >= 3.7 h; Naples and Palermo <= 3.3 h.

## Anecdote check: Troina vs Crema

| | relief 1980s | relief 2020s |
|---|---|---|
| Troina, Sicily (~1120 m) | 7.8 h | 6.3 h |
| Crema, Po plain (~79 m) | 7.0 h | 3.0 h |

Gap widened from 0.9 h to 3.3 h. (Earlier recorded as 0.8 -> 3.2 with Crema at 3.1: that run averaged months without weighting by days; every other figure is day-weighted. Exact values 6.96 -> 3.03 h.)

## Italy, tropical nights (Figure 1)

- land with a typical summer night above 20 °C: 6% -> 33%
- Rome: 7% -> 73% of the summer; Milan: 0% -> 22%

## Monthly warming, Italy (quoted in the limitations box)

Verified 2026-09-28 from `italy_monthly_means.nc` (ERA5-Land monthly means, final data, all twelve months), Natural Earth Italy outline, by `check_numbers.py`. Replaces the earlier values, which came from a run that could not be repeated after a container reset; the claims all stand.

| month | 1980s | 2020s | change |
|---|---|---|---|
| Jan | 2.5 °C | 4.5 °C | +1.97 |
| Feb | 3.2 °C | 6.2 °C | +3.00 |
| Mar | 6.1 °C | 7.8 °C | +1.69 |
| Apr | 9.6 °C | 10.8 °C | +1.16 |
| May | 13.7 °C | 15.4 °C | +1.65 |
| Jun | 17.7 °C | 20.9 °C | +3.21 |
| Jul | 21.2 °C | 23.5 °C | +2.26 |
| Aug | 20.9 °C | 23.1 °C | +2.22 |
| Sep | 17.9 °C | 18.9 °C | +1.01 |
| Oct | 13.2 °C | 14.4 °C | +1.25 |
| Nov | 7.4 °C | 9.3 °C | +1.84 |
| Dec | 4.1 °C | 5.7 °C | +1.63 |

- June warmed more than any other month (+3.21 °C; February next, +3.00); September least of all twelve (+1.01 °C; April next, +1.16).

## Italy, one summer at a time (population-weighted hours of relief)

Computed 2026-09-28 from the original Italian uploads; the averages reproduce the article (6.08 h and 3.23 h). `italy_relief_by_summer.csv`.

| summer | hours per person |
|---|---|
| 1980s, each summer | 5.3–7.0 |
| 2020 | 4.27 |
| 2021 | 3.90 |
| 2022 | 2.20 |
| 2023 | 3.46 |
| 2024 | 2.71 |
| 2025 | 2.84 |

- The most comfortable summer of the 2020s (2020, 4.3 h) gave less cool air than the worst summer of the 1980s (5.3 h): the two decades do not overlap.

## Summer 2026 (not in the article)

From `t2m_diurnal_JJA2026_southern_europe.nc`: June final ERA5-Land, July and August preliminary (expver 0005). Same grid and land-sea mask as the article's data; 2025 recomputed on this grid reproduces 2.84 h exactly.

- Italy, hours of relief per person: **1.43 h** — the worst summer in the series (previous worst 2022, 2.20 h); 2020-2026 average would be 2.97 h against 3.23 h for 2020-2025.
- Troina's cell: June 8 h, July 2 h, August 0 h; summer 3.3 h (2020-2025 mean 6.3 h). August night minimum 20.5 °C, above any August 2020-2025. Cells at the town's own height (1,048-1,119 m) read the same.
- Crema's cell: summer 0.3 h; August night minimum 22.6 °C.
- Kept out of the article: the Troina figure conflicts with the author's own experience of sleeping well there, and cannot be checked against a thermometer yet (the SIAS open-data portal was unreachable). The contrast holds in the grid — Troina's August nights about 2 °C cooler than Crema's.

## Where people live vs the land (backs the Figure 3 title)

| | relief today, land | where people live | loss, land | loss, people |
|---|---|---|---|---|
| Italy | 4.41 h | 3.23 h | 2.31 h | 2.84 h |
| Spain | 4.94 h | 3.42 h | 1.76 h | 2.19 h |
| Greece | 3.03 h | 1.29 h | 2.20 h | 1.80 h |

Land averages weighted by cell area (cosine of latitude), within each country's Natural Earth outline. Relief is lower where people live in all three; the loss is larger where people live in Italy and Spain only.

## Sampling uncertainty, recomputed (2026-09-28)

Year-by-year resampling of the summers, 20,000 draws, fixed seed 20260928 (`check_numbers.py`).

| | warming | ± °C (95%) | loss per person | ± h (95%) |
|---|---|---|---|---|
| Italy | +2.56 °C | 0.66 | 2.85 h | 0.69 |
| Spain | +2.45 °C | 0.71 | 2.19 h | 0.60 |
| Greece | +2.22 °C | 0.88 | 1.80 h | 0.76 |

- Italy loses more than Spain in 99% of draws; Spain more than Greece in only 82%.
- Replaces the earlier "roughly ±0.6 °C" and "the ordering of the three countries does not depend on it".
- June warming +3.21 °C reproduced; September still needs the all-months download.

## Headline range (Verdict and numbers strip)

Eight countries, loss per person per night: **2.29 h, 95% interval 1.75–2.81** (±0.53, "give or take half an hour"). In full cool nights per summer: 26 (20–32); as a share of a lifetime's nights: 7% (5.5–8.9%, "between about 6% and 9%"). Year-by-year resampling, fixed seed 20260928.

Natural frequencies used in the prose for the population shares: under 4 h, 23.5% → 62.5% ("about one in four" → "more than three in five"); a full 8 h, 37.7% → 17.4% ("almost two in five" → "about one in six").

## Numbers quoted from other work

- Vavassori, Žgela & Brovelli 2026 (doi:10.1007/s12518-026-00734-x): 2.2 km reanalysis; 100-plus Air Force stations; 1981–2024; tropical nights rising about 6–7 days per decade, steepest below 500 m.
- Murage, Hajat & Kovats 2017 (doi:10.1097/EE9.0000000000000005): London, 1993–2015.
- Kim et al. 2023 (doi:10.1289/EHP11444): about 10% excess all-cause mortality on hot nights, Japan.
