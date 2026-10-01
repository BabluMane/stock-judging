# v4 Phase-D Winner/Mediocrity Set — Selection Dossier (SET_WINMED)

Coordinator: Musey. Evidence-only. No engine changes, no Phase-D execution.
The system is NOT LIVE; no company is ever called investable.

## Shape

- **Winners:** 5 companies × 2 consecutive March-31 name-dates = 10
- **Mediocrities:** 5 companies × 2 consecutive March-31 name-dates = 10
- Max 2 name-dates/company. All dates ≥ 2019-03-31, vintages 2019–2022.
- Certified blow-ups (5 name-dates, separate dossier): supremeeng_2020/2021, pbm_2019/2020, varroc_2019.

## Final set

| Tier | Company | Name-dates | One-line thesis |
|---|---|---|---|
| W | Infosys (infy) | 2020-03-31, 2021-03-31 | COVID-era digital deal boom + large-deal wins → multi-year EPS compounding and sustained P/E re-rating |
| W | State Bank of India (sbin) | 2021-03-31, 2022-03-31 | PSU-bank credit-cost normalization + corporate-book recovery → 2021-24 re-rating (~2.5× in 3y) |
| W | SRF (srf) | 2019-03-31, 2020-03-31 | Fluorochemicals/specialty-chemicals capex cycle + import substitution; EPS 16.08 → 64.27 FY18–FY22 |
| W | L&T (lt) | 2021-03-31, 2022-03-31 | Domestic capex-cycle order-book boom + asset monetization/NWC discipline → 2021-25 run |
| W | Endurance Technologies (endurance) | 2020-03-31, 2021-03-31 | 2W/4W ancillary share gains + premiumization → steady FY19–FY24 compounding |
| M | Dr Reddy's (drreddy) | 2019-03-31, 2020-03-31 | US generics price erosion 2017–19; MOSL Jan-2018: "will remain range bound" (~₹2,000–3,000 band) |
| M | Dabur (dabur) | 2020-03-31, 2021-03-31 | FMCG range-bound ₹400–560 2019–22 while EPS flat (8.17 → 8.18) — classic flat/de-rating profile |
| M | Maruti Suzuki (maruti) | 2019-03-31, 2020-03-31 | Auto slowdown + BS-VI; flat ₹6k–7.5k 2018–21, EPS declined 260.86 → 145.30 FY18–FY21 |
| M | Cyient (cyient) | 2020-03-31, 2021-03-31 | Midcap ER&D/IT; flat ₹400–600 2017–21 |
| M | Aurobindo Pharma (auropharma) | 2019-03-31, 2020-03-31 | US FDA overhangs; price flat ₹700–900 2017–21 while EPS grew 41.36 → 91.05 — textbook de-rating |

Sectors covered: IT, PSU banking, chemicals (srf), infra (lt), auto ancillary (endurance), pharma ×2, FMCG (dabur), auto OEM (maruti). Caps: 7 large, 2 mid (endurance, cyient), 1 mid/large (auropharma).

## Selection method (evidence-only)

1. **Three workers, separate axes** (per oos-evidence-sweep skill): W1 large-cap winners, W2 mid/small-cap winners, W3 mediocrities. Each ran exclusion triage FIRST (burn list 243 tokens + 77 prior-set company tokens, normalized), then theses from general public market history — no price-data fitting, no threshold grids, no tuning to engine outputs.
2. **Firewall-first batching** (per R3/R4/R6 lesson): informational P_d0/P_G1 ratio computed BEFORE evidence pulls; ratio is NOT a selection gate. Adjudication preference: all 10 winner name-dates ended fill-plausible (≤2.0), supporting leg-(b) feasibility; mediocrity ratios mixed (16/20 plausible, 4 over 2.0: drreddy_2019 2.163, dabur_2021 2.336) — immaterial, mediocrity fills are not part of the bar.
3. **Exact U1/U2 on frozen engine_v4.usability** run by the COORDINATOR (not workers) for all 60 candidate name-dates — 60/60 PASS, worker EPS matched screener-cache EPS exactly on all 60. Corp actions verified: srf 4:1 bonus Oct-2021, infy/tcs bonuses pre-window, bajajfinsv 5:1 split+1:1 bonus ex 13-Sep-2022 (post-window), eichermot 1:10 split Aug-2020 (post-window; cache split-adjusted), godrejcp FY18/FY19 bonuses (restated in screener; ex-dates not independently sourced — documented caveat, U1 verdict unaffected), aartiind/vinatiorga/elgiequip splits post-window (restated in screener; exact ex-dates not sourced — caveat only).
4. **Disjointness** at company AND name-date level vs five prior sets + R1–R7 burn list + blow-up companies: `check_disjoint_winmed.py` → DISJOINT: True.

## Exclusion audit (coordinator-verified, not worker-claimed)

- All 30 worker candidates independently checked vs canonical prior lists (imported from check_disjoint_v310/v311): 30/30 clean at company level.
- Final 20 asserted vs prior sets + burn list + blow-ups: DISJOINT True (script exit 0).
- Renamed/demerged: no identity collisions (cyient ≠ cyientdlm; uno-minda deliberately avoided — mindacorp burn token confusion hazard).

## Adjudication decisions

- **Cross-tier collisions resolved:** infy, axisbank, sbin appeared in BOTH worker pools. infy_2020-03-31 and axisbank_2019/2020-03-31 were exact name-date collisions; sbin a company-level collision. All three kept in the WINNER tier (W1's axis); dropped from the mediocrity pool. Mediocrities chosen from W3's remaining 7.
- **Winners chosen for sector diversity + fill-plausible profile:** infy (IT), sbin (bank), srf (chemicals), lt (infra), endurance (auto ancillary). Alternates verified: tcs, bajajfinsv, aartiind, atul, fineorg (all clean, U1/U2 PASS).
- **Mediocrities chosen for sector diversity:** drreddy (pharma), dabur (FMCG), maruti (auto), cyient (midcap services), auropharma (pharma-mid). Alternates verified: godrejcp, eichermot (both clean, U1/U2 PASS).
- aavas dropped from winner contention on leg-(b) feasibility (financial-model firewall 3.543/6.033 — anchor unlikely to fill); thesis intact, documented as near-miss.

## Kills / near-misses (with reasons)

- W1: vbl — December FY, band-invalid.
- W2: timken — screener consolidated P&L only Mar 2025→TTM (FY-end-change legacy); aubank — consolidated page stale Mar 2014–Mar 2017. Both data-availability kills, not economics. Truncation confirmed SOURCE-side (raw HTML), not fetch artifact — per the truncated-cache lesson.
- W3: sbin_2019-03-31 deliberately NOT proposed (scoring FY18 EPS −5.11 non-positive); double shifted to 2020∩2021.
- godrejcp/eichermot (mediocrity alternates), tcs/bajajfinsv/aartiind/atul/fineorg (winner alternates): verified, kept in reserve.

## Files

- `set_winmed.json` — the 20 name-dates with theses, shape, alternates.
- `winmed_firewall_results.json` — 120 deduplicated firewall records (informational; "selected" flag on the 20).
- `check_disjoint_winmed.py` — DISJOINT: True, exit 0.
- Worker evidence: `winmed_w1/`, `winmed_w2/`, `winmed_w3/` (findings, leads, firewall, caches).
- `burn_list_winmed.json`, `prior_sets_winmed.json` — exclusion inputs.
