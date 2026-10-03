# AI usage ledger, BIT #001

What is measured here, and what is not. Figures come from the Claude Code session transcripts, not from estimates.

## Measured: packaging and verification (1–3 October 2026)

Two Claude Code sessions: re-downloading the raw inputs, rebuilding `data/`, re-running `check_numbers.py` and the figure scripts, building the Zenodo archive and the web pages. 57 model responses, no sub-agents.

| model | share of effective tokens | effective tokens (M) |
|---|---|---|
| Claude Sonnet 5.5 | 97% | 2.93 |
| Claude Opus 5.5 | 3% (one response) | 0.08 |

| activity | effective tokens (M) | share |
|---|---|---|
| Writing and reasoning | 1.09 | 36% |
| Quality checks | 0.72 | 24% |
| Analytics and modelling | 0.67 | 23% |
| Orchestrating | 0.50 | 17% |
| Reading files | 0.02 | 1% |

Exact tokens, both models: input 116; output 35,038; cache write 854,644; cache read 10,368,700.
Effective tokens = input + 0.1 × cache read + 2 × cache write + 5 × output.
Ledger date: 2026-10-04. Work continues, so later totals will be higher.

## Not measured

- **The analysis and the article** were produced earlier, by Claude Opus 5 working from the author's instructions (see `README.md` and `NOTES.md`; dated entries run from 2026-08-25 to 2026-09-28). Those sessions are not in this ledger, and **their cost is missing**.
- **Editing of the article text** in other chats of the BIG IF TRUE project is not included either.

So these figures describe the work of making the archive and site, not the analysis. Do not read them as the total cost of the issue.

## Cost

No dollar figure is given: the price table used by the tracking scripts is still a placeholder.
