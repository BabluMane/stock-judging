# build_log_w3.md — W3 data-assembly, v4 Phase-D locked run (2026-10-01)

Worker: W3 (blow-ups). Evidence-only: no engine runs (run_name_date never called); events.grade_all used for grading only.
Output dir: `~/workspace/stock-judging/v3/validation/v4_oos/phase_d_inputs/`
Assembly script: `/tmp/w3_assemble.py` (rerunnable). Beta table: `_beta_table.json` (see bottom).

## JOB 1 — public beta table (done): `_beta_table.json`
- ONE judgment input, loudly documented: Yahoo Finance 5Y-monthly adjusted closes vs NIFTY 50 (^NSEI); beta = cov/var. Chosen because the Yahoo v8 chart API was fetchable for all 13 incl. SME/BSE names; investing.com bot-checks, moneycontrol unreliable.
- Symbols: INFY.NS, SBIN.NS, SRF.NS, LT.NS, ENDURANCE.NS, DRREDDY.NS, DABUR.NS, MARUTI.NS, CYIENT.NS, AUROPHARMA.NS, SUPREMEENG.NS, PBMPOLY.BO, VARROC.NS.
- 60-mo windows; as_of 2026-09/2026-10 (Oct 2026 monthly bar just opened). **PBM exception:** Yahoo PBMPOLY.NS had 1 overlapping month; used **PBMPOLY.BO** (BSE series, 59 mo, as_of 2026-08) — named in table.

## JOB 2 — 5 blow-up JSONs (done)
All non-financial. Screener slugs resolved via search API (SUPREMEENG standalone per R3, PBMPOLY/consolidated, VARROC/consolidated); sectors are screener "Sector" breadcrumb verbatim: supremeeng "Capital Goods", pbm "Textiles", varroc "Automobile and Auto Components".

| file | scoring_fy | fy years | prices | eps_pts | events grade | PIT |
|---|---|---|---|---|---|---|
| supremeeng_2020-03-31 | 2019 | 2016–2023 | 417 wk, screener, 2018-09-07→2026-10-01 | 29 | T2 resignation_fraud_or_unpaid_fees → SEVERE | 2019-05-29 ✓ |
| supremeeng_2021-03-31 | 2020 | 2016–2023 | same | 29 | same → SEVERE | 2020-08-05 ✓ |
| pbm_2019-03-31 | 2018 | 2015–2023 | 320 wk, **Yahoo PBMPOLY.BO**, 2000-01-31→2026-08-31 | 1 | T2 resignation_no_stated_reasons → MODERATE | 2018-05-21 ✓ |
| pbm_2020-03-31 | 2019 | 2015–2023 | same | 1 | same → MODERATE | 2019-05-29 ✓ |
| varroc_2019-03-31 | 2018 | 2015–2023 | 431 wk, screener, 2018-07-06→2026-10-01 | 42 | T2 opinion_qualified → SEVERE | 2018-06-06 ✓ |

- **Events/sources:** supremeeng 2021-11-03 (tier-1 NSE filing, R T Jain & Co fee-dispute resignation, first exchange disclosure); pbm 2020-09-30 (tier-1 BSE intimation scrip 514087, no reason stated — underlying 18-Jul-2020 letter URL now serves the 2022 successor filing, unrecoverable); varroc 2020-06-25 (FY20 audited-results filing, SRBC & Co consolidated report headed "Qualified Opinion", ₹943.68M disputed warranty claim).
- **PBM subcase verdict (settled):** "resignation_no_stated_reasons" → MODERATE, robust to the alternate reading (other-stated-reason also grades MODERATE).
- **results_published** = board-meeting/AR-signing-date proxy for annual-results announcement: supremeeng FY19 2019-05-29, FY20 2020-08-05 (NSE Reg 33(3)(d) declaration), FY22 2022-06-07 (auditor report in NSE AR ZIP); pbm FY18 2018-05-21, FY19 2019-05-29, FY20 2020-07-31, FY21 2021-06-30 (from R6 AR caches); varroc FY18 2018-06-06, FY19 2019-05-24, FY20 2020-06-25, FY21 2021-06-04 (SRBC consolidated auditor report, BSE AR pdf). Pre-listing FYs → None + named gap. Cooling-off: supremeeng E1 2021-11-03 ≤ FY22 print 2022-06-07 ✓; pbm E1 2020-09-30 ≤ FY21 print 2021-06-30 ✓; varroc E1 2020-06-25 ≤ FY21 print 2021-06-04 ✓.
- **corp_actions (Yahoo splits):** SUPREMEENG.NS 1:10 ex 2022-03-03 (post-window → no U1 restatement, screener EPS already restated); VARROC.NS: no Yahoo record of the known FY18 ₹10→₹1 subdivision (pre-FY18-end → doesn't touch the basis diagnostic); PBMPOLY.BO: none.
- **equity_increase_solely_bonus_split:** supremeeng False (2→25cr: pre-listing raises + Sep-2018 IPO); pbm True (no increase; 8→7cr decrease FY20); varroc False (10→15cr: pre-IPO raises + Jul-2018 IPO).
- **pledge:** [] (no pledged-share sub-rows in static screener HTML; JS-gated expansion) — evidence of absence at this source, not proof of zero.
- **mcap_cr** (screener page, 2026-10-01): supremeeng ₹106, pbm ₹39.9, varroc ₹12,891. mcap_price = last weekly close (pbm: 2026-08-31).

## Named gaps (never interpolated, never invented)
1. **PBM prices:** screener chart API serves only 25 points server-side (2026-08-17→2026-10-01) — data wall, verified myself. Fallback: Yahoo PBMPOLY.BO weekly adjusted closes, 320 weeks from 2000-01-31, as_of 2026-08-31. Cross-checked vs R6's screener-sourced P_d0: 2019-03-31 Yahoo 75.01 vs 78.65; 2020-03-31 32.17 vs 28.85 (within ~12%).
2. **PBM EPS series:** 1 point only (2026-09-15, 2.67) — U3 UNCOMPUTABLE for both pbm name-dates (informational gate only; U1/U2 unaffected).
3. **Varroc pre-d0 price history:** listed 2018-07-06 → 38 weeks before d0=2019-03-31, short of 12m. d5_crash computable (≥26w); anchor p0 fine.
4. **FY span limits:** supremeeng screener P&L starts Mar 2016 (FY15 absent for scoring FY2019); pbm/varroc start Mar 2015 (FY14 absent for scoring FY2018). Engine delta() fail-closed handles missing priors.
5. **fy sub-rows not in static screener HTML** (JS-gated): current_assets, current_liabilities, material_cost, raw_material_pct, revaluation_reserve → None. U3-relevant, gates nothing.
6. **audited_eps_by_fy:** None — R3/R6/R7 verified audited/sourced ≈1.0 at Gate 1 (documented in dossiers); exact re-extraction not done, optional field, gates nothing.
7. Pre-listing FYs have results_published=None (no annual results as a listed co) — named, expected.

## Validation performed
- Each JSON: exactly the 16 NameDate fields, no extras; NameDate(**data) constructs after ISO-date deserialization (proper None handling).
- events.grade_all on all 5 (allowed, not an engine run): grades SEVERE/SEVERE/MODERATE/MODERATE/SEVERE — all T2, all graded.
- select_scoring_fy(fy, d0) == manifest scoring_fy for all 5 (63-day rule).
- Prices strictly ascending; pre-d0 ≥12m except varroc (named gap 3); as_of ≥ d0+24m all 5.
- **Coordinator schema_check.py has 2 bugs (not my data):** (a) fy parse puts the whole row `r` where results_published is None → TypeError crash; (b) FY-coverage check `yrs[-need+1:]` compares 4 items to a 5-item range AND breaks with the brief-required post-E1 fy extension. Flagged for coordinator fix; my independent validation above covers the same ground correctly.

## JOB 3 — W1/W2 cross-validation (pending)
- W1 mid-flight: `_raw/` has infy/sbin/srf/lt/endurance fy + series + `_verify_cells.json`; cells self-consistent (infy EPS 35.26, sbin 25.11, srf 16.08 match gate-1 U1 values; all verify_cells true). No final `<name_date>.json` from W1 yet; W2 nothing yet. Full spot-checks will run when their final JSONs land.

## Durable lessons (appended to AGENTS.md)
- Screener chart API is company-depth-dependent: PBM (BSE 514087) serves only ~25 recent points server-side while NSE peers serve 400+ — verify point counts before trusting the series; Yahoo BSE weekly is the fallback.
- Screener static HTML lacks JS-gated sub-rows (pledged shares, current assets/liabilities, material cost, revaluation reserve) — pledge=[] means "not visible", not "zero".
- Screener "Sector" breadcrumb verbatim is what is_financial reads ("Banks"/"Finance") — record it exactly.
- Yahoo splits API reports bonuses as splits too (ratio=new:old); post-window splits need no ex-date precision since screener EPS is already restated.
