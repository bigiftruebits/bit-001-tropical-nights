# bit-001-tropical-nights — deviations from the format

Changes applied to this issue before `BIG_IF_TRUE_FORMAT.md` records them, and
places where the issue departs from the format, with the reason.

## 2026-10-04 — figure spec change (strategy chat, agreed by Riccardo)

Treated as the spec until the editorial manager updates §4.9, §4.12 and the
figure guide. The note, in short:

1. Unchanged: 4.4 in wide at 450 dpi (~1980 px), no text under 9 pt, checked at
   360 px; every script asserts height <= 1.75 × width.
2. BIG and TRUE are also Substack Notes: horizontal, optimal ratio 0.8,
   comfortable 0.75–1.0, above 1.0 rare; titles state the point; a secondary
   panel goes beside a map, not below it; TRUE at most two panels, side by side,
   lettered (a, b).
3. IF is article-only: optimal ratio 1.0–1.25, allowed 0.6–1.75.
4. New: a preview image, 1200 × 630, from the BIG PNG and the Verdict's
   headline number in KEY_NUMBERS, by a standalone script that fails if the
   number is missing or the gloss runs past two lines; checked at 160 and 520 px.

## Since then: format §1, §4.9, §4.12 and §9.8 revised the same day

The revised format now holds these rules (BIG at most two panels, TRUE at most three,
IF as many as the test needs, all within one phone screen; BIG and TRUE in the 0.8
Note shape; the preview image), so they are no longer deviations. How #001 meets them:

- **Figure 1 (BIG)** — two maps, 4.4 × 3.97 in, ratio 0.90; title "Rome's hot summer
  nights: 7% → 73%". Asserted 0.75–1.0.
- **Figure 2 (IF)** — the map is back at Riccardo's request and, at his second request, fills the
  height of the left column (2.15 × 2.8 in), with the two charts compact on the right; 4.4 × 3.86 in,
  ratio 0.88: below IF's optimal 1.0–1.25, inside the allowed 0.6–1.75. Asserted 0.6–1.75.
- **Figure 3 (TRUE)** — three panels: (a) the basin in 1980–1989 and (b) in 2020–2025, full width,
  then (c) the people in four bands, each label with the average hours per person (the separate
  per-person panel no longer fits the three-panel limit).

## Still deviations

- **Figure 3 (TRUE) is 4.4 × 6.62 in, ratio 1.50, not the 0.8 Note shape** (Riccardo, 2026-10-04): he
  asked for both decades of the basin, for the comparison. Two full-width maps cannot fit the 0.8 shape
  legibly; side by side, each would be about 2.1 × 0.9 in. Inside the overall 1.75 limit. The script
  asserts ≤ 1.75 and that the legend stays on the figure. Maps, colour bar and legend run the full
  width (Riccardo).
- **Figure 2 (IF)** has no frame around the map (Riccardo), and its script asserts that the colour bar's
  labels stay below the map.

- **#001's preview is built on the Mediterranean map, not on the BIG figure** (Riccardo,
  2026-10-04, after the A/B test, method PREVIEW-AB-3). The Verdict's number, 2.3 h per
  southern European, is the TRUE finding, and the basin map shows where it applies; the
  BIG figure shows Italy. `make_preview_map.py` draws the basin in both decades from `data/`, stacked as in Figure 3,
  without a colour bar (EN and IT) and `make_preview.py`
  reads it in place of the BIG PNG. Format §9.8 says BIG: for the editorial manager.

- **Preview file names use the number, not the slug:** `fig-001-preview.png` and
  `-it.png`, matching #001's already numbered figures (`fig-001-*`), since the issue
  launches under that number.
- **The previews sit in `article/preview/`, not `article/figures/`,** so the
  repository's `verify_release.py` — which redraws and compares every `fig-001-*.png`
  in `article/figures/` — stays unchanged.
- **The preview's gloss** is "fewer cool hours a night, per person": the first draft
  ("…per southern European") needed three lines and the script refused it. The number
  is the southern-European average while the BIG figure beside it shows Italy; the
  format pairs them by design.

## 2026-10-04 — test: preview image A/B (task=test, method PREVIEW-AB-1)

Agreed by Riccardo in the strategy chat. A test, not a change to the issue: its
outputs are in `tests/preview-ab-2026-10-04/` of the analysis chat's bundle, outside
`repo/figures/`, `article/` and every figure manifest. Tag:
`[BIT=bit-001-tropical-nights phase=preview method=PREVIEW-AB-1 task=test]`.

- **Variants**, from one script with a variant flag (`make_preview_ab.py`), both
  1200 × 630 with 40 px margins: **A**, split (BIG left ~60%, the Verdict's number in
  its shortest form fitted to the right zone, gloss of at most 8 words on 2 lines; fails
  below 60 px); **B**, the BIG figure alone, centred at ~550 px on flat #FBF2EC.
- **Cases**: #001 first, the case for this issue (the current BIG figure; "2.3 h", the
  Verdict's number in its shortest form, without its range); #002 second, for
  comparison (`fig-002-big-price-map.png`, sha256 matching `fig-002-figure-manifest.md`;
  "6.5¢/l", the key `intracity` in `bit-002-key-numbers.md`).
- **Sheet**: https://claude.ai/artifact/RS8BGtGy8uEsXwN34fNJ87 — full size; a Notes
  link card at 520 px; a post-list row at 160 px; the centre 630 × 630 square at
  160 px; each on light and dark backgrounds. Riccardo judges from it.
- **Method PREVIEW-AB-2** (Riccardo, same day): the same drawing built on the TRUE
  figure instead of BIG, because the Verdict's number (2.3 h per southern European) is
  TRUE's finding, shown in its panel b, while BIG shows Italy. Same number, same gloss,
  same two variants; only the figure changes. On the sheet between #001 on BIG and #002.
  Format §9.8 builds the preview on BIG, so this stays a test until the editorial
  manager changes the rule.
- **Methods PREVIEW-AB-3 and PREVIEW-AB-4** (Riccardo, same day): the same drawing on a
  single map instead of a whole figure: the Mediterranean basin alone (TRUE's panel a)
  and Italy from IF (IF's map), each drawn on its own by `render_maps.py` from
  `data/`. Same number and gloss, both variants.
- **Not a method change** for the issue's own preview (`make_preview.py`, format §9.8),
  which stays as it is unless the test leads to a decision.

## 2026-10-04 — waived: the sensitivity to another baseline

Decision of Riccardo (the issue is in production): the 1990s-baseline check of the
format's checklist is **waived for #001**. The sentence "the two periods sit in one line
of the published configuration, so anyone who prefers the 1990s can rerun it" is
**removed** from both editions rather than kept with a limitation, because it was not
true of the package: the periods are set in `download_raw.py`, and the decade labels
are part of file names in seven scripts, so a rerun needs edits in several places. The
baseline is still declared as a choice ("I was born in 1983 and wanted to compare with
my childhood").

## 2026-10-05 — test: consolidated preview spec (task=test, method PREVIEW-AB-5)

The strategy chat's consolidated preview spec of 2026-10-04, which replaces all earlier preview notes,
tested on #002 and #001 (variants A and B) and applied to #000's real preview. Tag:
`[BIT=bit-001-tropical-nights phase=preview method=PREVIEW-AB-5 task=test]`. Outputs in
`tests/preview-ab-2026-10-05/`, outside every figure manifest.

- **Safe zone** x 200–1000, y 80–480 on the 1200 × 630 canvas, flat #FBF2EC outside; **minimal centre**
  x 428–772, y 218–412. Each saved PNG is read back and its content box checked inside the safe zone.
- **Results:** all five images pass the safe zone and lose nothing in the measured crops (web home page at
  127 and 189 px per side; phone app card). In both split variants the hero number sits right of the
  minimal centre (x 604–998 for #002, x 667–998 for #001): in a split layout it does not fit there.
- **#001's own preview** (`make_preview.py`) is unchanged: this was a test.

## Preview and Note images (2026-10-05)

- **Preview, two variants for Riccardo to choose**, to the final rule (strategy chat, 2026-10-04): safe zone
  x 305–895, y 80–480; variant A stacks the number above the figure, no side-by-side layout. **A:** the
  Verdict's number above the 2020–2025 basin map (the two stacked decades are nearly square and leave no
  room for the number). **B:** the two decades alone, no number. `make_preview.py en|it A|B` replaces the
  split layout of 2026-10-04; each PNG is read back and its content box checked inside the safe zone.
- **TRUE's Note image** is a separate version, `make_fig3_note.py` (one map, ratio 0.99), because the
  article's Figure 3 (two maps, ratio 1.50) is too tall for the Note shape. BIG's Note image is Figure 1.
