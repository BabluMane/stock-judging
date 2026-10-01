# W3 Mediocrity-Selection Findings — v4 Phase-D set (MEDIOCRITIES axis)

Worker: W3. Evidence-only. The system is NOT LIVE; no company is ever called investable.
Scope: 10 candidate companies × 2 consecutive March-31 scoring dates (20 name-dates), large+mid cap mix.
v3.11 mediocrity convention: documented flat / de-rating / range-bound multi-year profile from public market history (cf. emami de-rating, marico range-bound 2019–21, ongc flat-to-lower).

## Funnel table

| # | Company (slug) | Cap | Name-dates | Scoring FYs (63d PIT) | Thesis (one line) |
|---|---|---|---|---|---|
| 1 | Dr Reddy's (drreddy) | Large | 2019-03-31 ∩ 2020-03-31 | FY18 EPS 11.41; FY19 EPS 23.49 | US generics price erosion 2017–19; MOSL Jan-2018 said the stock "will remain range bound" (~₹2,000–3,000 band 2017–19) |
| 2 | Infosys (infy) | Large | 2019-03-31 ∩ 2020-03-31 | FY18 EPS 36.69; FY19 EPS 35.26 | Founder–board governance war, CEO Sikka's Aug-2017 exit; crashed to 4-yr low (~₹870, −13% in a day) and traded sideways through 2019 |
| 3 | Axis Bank (axisbank) | Large | 2019-03-31 ∩ 2020-03-31 | FY18 EPS 1.78; FY19 EPS 19.59 | NPA-cycle overhang (FY18 PAT collapsed); large-cap bank traded sideways ₹500–750 across 2016–21 |
| 4 | SBI (sbin) | Large | 2020-03-31 ∩ 2021-03-31 | FY19 EPS 2.58; FY20 EPS 22.15 | PSU-bank discount; flat ~₹200–350 2015–20; FY18 printed a consolidated loss (EPS −5.11) on provisions, recovered by FY20 |
| 5 | Dabur (dabur) | Large | 2020-03-31 ∩ 2021-03-31 | FY19 EPS 8.17; FY20 EPS 8.18 | Defensive FMCG; price range-bound ₹400–560 across 2019–22 while EPS barely moved — classic flat/de-rating profile |
| 6 | Godrej Consumer (godrejcp) | Large | 2019-03-31 ∩ 2020-03-31 | FY18 EPS 15.99; FY19 EPS 22.91 | De-rated from 2017 highs to a ~₹500–700 band 2019–21 on weak volume growth; equity capital shows 1:1 (FY18) + 1:2 (FY19) bonuses |
| 7 | Eicher Motors (eichermot) | Large | 2019-03-31 ∩ 2020-03-31 | FY18 EPS 71.89; FY19 EPS 80.75 | Royal Enfield demand peaked 2017; sales fell from late-2018 (Dec-2018 −13% YoY), stock shed ~40% from peak then went flat; 1:10 split Aug-2020 |
| 8 | Maruti Suzuki (maruti) | Large | 2019-03-31 ∩ 2020-03-31 | FY18 EPS 260.86; FY19 EPS 253.21 | Auto slowdown + BS-VI transition; flat ₹6,000–7,500 2018–21 while EPS declined 260.86 → 145.30 across FY18–FY21 |
| 9 | Cyient (cyient) | Mid | 2020-03-31 ∩ 2021-03-31 | FY19 EPS 42.33; FY20 EPS 31.14 | Midcap ER&D/IT; flat ₹400–600 2017–21; COVID quarter crushed FY21 EPS to 33.06 from 42.33 |
| 10 | Aurobindo Pharma (auropharma) | Mid/Large | 2019-03-31 ∩ 2020-03-31 | FY18 EPS 41.36; FY19 EPS 40.36 | US FDA overhangs; price flat ₹700–900 2017–21 even as EPS grew 41.36 → 91.05 by FY21 — textbook de-rating mediocrity |

## Exclusion triage (all kills, with reasons)

1. Burn-list check (`burn_list_winmed.json`, 243 tokens; normalization: lowercase, strip spaces, `&`→`and`): **0 matches** across all 10 candidate slugs.
2. Prior-sets check (`prior_sets_winmed.json`; company token = name-date before last underscore; 77 unique company tokens across in-sample + v3.8–v3.11): **0 matches**. (v3.11 mediocrities emami/marico/ongc/sunpharma/nhpc excluded by construction — none proposed.)
3. R2 (PR #13) list: not in local mirror; cross-checked from memory of Phase-C sweeps — none of the 10 is a distressed/blow-up-examined company (no flfl/simplexinf/omaxe/adaniports/fsc/ptc overlap).
4. Renamed/demerged tickers: no identity collisions (e.g. cyient ≠ cyientdlm; sbin is the live SBI slug; merged associate-bank slugs SBBJ/SBT not used).
5. Deliberate near-miss — **sbin_2019-03-31 NOT proposed**: scoring FY18 consolidated EPS is −5.11 (non-positive) → chose 2020∩2021 (FY19/FY20 positive) instead.

## Listing-date + March-FY confirmation

All 10 are mainboard companies listed well before 2019 (DRREDDY 1986, INFY 1993, AXISBANK 1998, SBIN —, DABUR 1994, GODREJCP 2001, EICHERMOT 2004, MARUTI 2003, CYIENT 1997, AUROPHARMA 1995), all March-FY. Listed-at-d0 proven by the firewall: all 40 name-dates returned a close within 10 days of d0 (zero "no close" notes).

## Informational firewall ratios (NOT a selection gate)

| name-date | P_d0 | P_G1 | ratio | name-date | P_d0 | P_G1 | ratio |
|---|---|---|---|---|---|---|---|
| drreddy_2019-03-31 | 556.05 | 257.11 | 2.163 | dabur_2021-03-31 | 529.80 | 226.79 | 2.336 |
| drreddy_2020-03-31 | 583.30 | 334.30 | 1.745 | godrejcp_2019-03-31 | 686.00 | 349.48 | 1.963 |
| infy_2019-03-31 | 743.85 | 668.19 | 1.113 | godrejcp_2020-03-31 | 499.45 | 418.96 | 1.192 |
| infy_2020-03-31 | 652.70 | 757.13 | 0.862 | eichermot_2019-03-31 | 2054.77 | 2349.37 | 0.875 |
| axisbank_2019-03-31 | 777.25 | 240.91 | 3.226 | eichermot_2020-03-31 | 1431.98 | 2514.36 | 0.570 |
| axisbank_2020-03-31 | 359.75 | 189.95 | 1.894 | maruti_2019-03-31 | 6672.55 | 6533.26 | 1.021 |
| sbin_2020-03-31 | 195.95 | 136.51 | 1.435 | maruti_2020-03-31 | 4646.10 | 6592.42 | 0.705 |
| sbin_2021-03-31 | 357.20 | 190.12 | 1.879 | cyient_2020-03-31 | 232.75 | 748.31 | 0.311 |
| dabur_2020-03-31 | 423.00 | 217.96 | 1.941 | cyient_2021-03-31 | 642.80 | 483.95 | 1.328 |
| | | | | auropharma_2019-03-31 | 784.25 | 1257.92 | 0.623 |
| | | | | auropharma_2020-03-31 | 392.25 | 1422.90 | 0.276 |

28/40 plausible-True, 12 False, 0 uncomputable notes; ratios recomputed independently from raw P_d0/P_G1 — exact match. Full 40-record file: `winmed_w3_firewall.json`. Banks classified financial (Broad Industry reading per V4_OOS_PREREG).

## Scoring FYs + consolidated EPS + corporate actions (per name-date)

Scoring FY per 63d PIT (nominal FY-end+60d convention): d0 2019-03-31 → FY18; d0 2020-03-31 → FY19; d0 2021-03-31 → FY20. All caches consolidated, year-span Mar 2015 → TTM (eichermot Dec 2014 → TTM, 15-month Mar-2016 column — March-FY; no truncation, d0s fully covered).

Corporate actions in/before the scoring windows (from balance-sheet Equity Capital jumps + public record):
- infy: 1:1 bonus Jun-2015 (572→1,144), 1:1 bonus Sep-2018 (1,088→2,170) — both ≤ d0; screener EPS already restated
- godrejcp: 1:1 bonus FY18 (34→68), 1:2 bonus FY19 (68→102) — both ≤ d0; screener EPS restated
- auropharma: 1:1 bonus Jul-2015 (29→59) — pre-window; screener EPS restated
- eichermot: 1:10 SPLIT Aug-2020 — AFTER both d0s (2019-03-31, 2020-03-31); P_d0/EPS in cache are split-adjusted; coordinator to note for price-basis consistency
- axisbank: no bonus/split in window (gradual ESOP/QIP rises only); sbin: none in window (1:10 split was Nov-2014, pre-cache); dabur/drreddy/maruti/cyient: none in window

Per-name-date EPS table is in `winmed_w3_leads.json` (scoring_fy_eps + full FY15–FY23 consolidated EPS series per company).

## Notes for the coordinator

- Mediocrities selected for documented flat/de-rated public profiles, deliberately NOT tuned to engine outputs; firewall ratios are informational only.
- eichermot P_d0 values are post-split adjusted closes; FY18/FY19 EPS (71.89/80.75) in screener are split-restated — consistent within the cache but the 1:10 split (Aug-2020) sits between d0-2020 and any forward window.
- sbin_2019-03-31 excluded from proposal (FY18 EPS −5.11); sbin double is 2020∩2021.
- Deliverables: this file, `winmed_w3_leads.json`, `winmed_w3_firewall.json`; caches in `winmed_w3/cache/` (10 consolidated JSONs).
