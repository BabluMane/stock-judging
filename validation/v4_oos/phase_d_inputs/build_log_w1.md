# W1 Phase-D Data Assembly Build Log

**Date:** 2026-10-01  
**Task:** Build 10 WINNER input JSONs for v4 Phase-D locked run (evidence-only, frozen engine never executed)  
**Output dir:** `~/workspace/stock-judging/v3/validation/v4_oos/phase_d_inputs/`

## Name-dates (10)

| Key | d0 | Scoring FY | FY window |
|-----|----|-----------|-----------|
| infy_2020-03-31 | 2020-03-31 | 2019 | 2015–2019 |
| infy_2021-03-31 | 2021-03-31 | 2020 | 2016–2020 |
| sbin_2021-03-31 | 2021-03-31 | 2020 | 2018–2020 |
| sbin_2022-03-31 | 2022-03-31 | 2021 | 2019–2021 |
| srf_2019-03-31 | 2019-03-31 | 2018 | 2014–2018 |
| srf_2020-03-31 | 2020-03-31 | 2019 | 2015–2019 |
| lt_2021-03-31 | 2021-03-31 | 2020 | 2016–2020 |
| lt_2022-03-31 | 2022-03-31 | 2021 | 2017–2021 |
| endurance_2020-03-31 | 2020-03-31 | 2019 | 2015–2019 |
| endurance_2021-03-31 | 2021-03-31 | 2020 | 2016–2020 |

## Data sources

### FY tables
- Source: screener.in consolidated P&L / Balance Sheet / Cash Flow via winmed caches (`port/validation/v4_oos/winmed_w1/cache/{infy,sbin,srf,lt}.json`, `winmed_w2/cache/endurance.json`)
- 14/14 cells spot-checked vs live screener HTML on 2026-10-01 (see `_raw/_verify_cells.json`)
- Fields: equity_capital, reserves, total_assets, pbt, interest, depreciation, net_profit, cfo, sales, opm_pct, dividend_payout_pct, investments, borrowings, eps, raw_material_pct

### Prices / EPS / Corp actions
- Weekly ADJUSTED closes via screener chart API: 901 points (2009-07-03 → 2026-10-01) for infy/sbin/srf/lt; 520 points (2016-10-21 → 2026-10-01) for endurance (listed Oct 2016)
- eps_series: unlagged publication-dated TTM EPS from screener chart API
- corp_actions: Yahoo Finance splits feed (bonuses reported as splits, ratio = new:old)
  - INFY: 1:1 bonuses ex 2014-12-02, 2015-06-15, 2018-09-04
  - SBIN: 10:1 split ex 2014-11-20
  - SRF: 4:1 bonus ex 2021-10-13 (post-window)
  - LT: 3:2 bonuses ex 2013-07-11, 2017-07-13
  - ENDURANCE: none

### results_published (NSE corporate-announcements API)
All 28 dates captured from NSE (actual announcement dates):
- INFY: FY15→2015-04-24, FY16→2016-04-15, FY17→2017-04-13, FY18→2018-04-13, FY19→2019-04-12, FY20→2020-04-20, FY21→2021-04-14 (from Infosys press release)
- SRF: FY14→2014-05-09, FY15→2015-05-12, FY16→2016-05-10, FY17→2017-05-22, FY18→2018-05-17, FY19→2019-05-13; FY20→None (exact NSE date not recovered; post-scoring for both srf name-dates)
- LT: FY16→2016-05-25, FY17→2017-05-29, FY18→2018-05-28, FY19→2019-05-10, FY20→2020-06-05, FY21→2021-05-14, FY22→2022-05-12 (from L&T board intimation)
- ENDURANCE: FY17→2017-05-10, FY18→2018-05-15, FY19→2019-05-14, FY20→2020-06-25; FY15/FY16→None (pre-listing, Oct 2016 IPO); FY21→None (exact NSE date not recovered; post-scoring)
- SBIN: FY18→2018-05-22, FY19→2019-05-10, FY20→2020-06-05, FY21→2021-05-21

**63-day PIT assertion:** All scoring-FY results_published dates ≤ d0−63d (verified 2026-10-01).

### CA/CL (audited results PDFs, consolidated)
From NSE-published audited results PDFs (₹ cr):
- INFY: FY18 50,017/14,105; FY19 52,878/18,638; FY20 54,576/20,856
- SRF: FY17 2,079.44/2,010.19 (from FY18 PDF comparative — FY17 PDF scanned/unextractable); FY18 2,450.14/2,532.21; FY19 3,172.29/3,198.68
- LT: FY19 166,976.33/134,585.82; FY20 178,322.68/142,745.04; FY21 194,960.59/137,404.81
- ENDURANCE: FY18 2,150.11/1,757.14; FY19 2,162.18/1,784.30; FY20 2,147.56/1,564.45 (PDFs in ₹ million, ÷10)
- SBIN: not applicable (financial; D3/D4 use CAMEL)

All pairs verified as CONSOLIDATED via statement headings.

### Pledge
Format: `{quarter_end, pledged_pct, basis, promoter_holding_pct}` (engine reads `pledged_pct`, NOT `pct`).

**PIT rule:** Mar-YYYY SHP/AR unpublished at d0=Mar 31, YYYY (filed ~Apr) → excluded. D1 scoring quarter = latest PIT-valid March.

- INFY: FY17–20 promoters pledged "–" (nil), promoter ~12.9% (Tijori AR mirror)
- SRF: FY17–19 pledged 0.00%, promoter 52.38% (KAMA Holdings 52.33%)
- LT: promoter 0.00% all years (screener) → pledged 0.0 trivially
- ENDURANCE: FY17–18 pledged "–" (nil), promoter ~82.5%; **FY19/FY20 ARs contain ZERO "pledge" mentions → Mar-2019/Mar-2020 = NAMED GAP** (pledge lists use Mar-2017/Mar-2018, latest PIT-valid sourced)
- SBIN: Govt of India promoter 56.92% (FY20) / 57.13% (FY19) → pledged 0.0

### Beta (W3 _beta_table.json)
Values are dicts — extracted numeric `['beta']`:
- infy 0.7331, sbin 1.175, srf 0.7736, lt 1.2305, endurance 1.017

### Sectors
Screener "Sector" verbatim, EXCEPT sbin = "Banks" (Bablu adjudication):
- infy "Information Technology", sbin "Banks", srf "Chemicals", lt "Construction", endurance "Automobile and Auto Components"

### SBIN CAMEL (D6)
Deviation from "screener ratios" ideal — sourced from SBI ARs + secondary:
- FY20 (sbin_2021 scoring): CAR 13.06% (audited standalone Basel III), GNPA 6.15% (JM Financial), Cost/Income 48% (MPRA), ROA 0.38% (audited standalone), CASA 44.17% (tradebrains/SBI AR)
- FY21 (sbin_2022 scoring): CAR 13.74% (MPRA+JM), GNPA 4.98% (JM), Cost/Income 50% (MPRA), ROA 0.45% (MPRA), CASA 45.40% (tradebrains)
- D6 totals: FY20 = 1+0+2+1+2 = **6 → PASS**; FY21 = 1+1+2+1+2 = **7 → PASS** (veto only if ≤4)

### Mcap
From 2026-10-01 cache quotes (W2 convention): infy ₹4,03,433cr @ ₹994; sbin ₹8,85,692cr @ ₹960; srf ₹73,291cr @ ₹2,472; lt ₹5,17,337cr @ ₹3,760; endurance ₹37,367cr @ ₹2,656.

### Events
`events: []` for all 10 (winners, no blow-up E1s). Method: two-source tape check over [d0−12m, d0+24m] via (1) NSE corporate-announcements API for auditor resignations/qualifications, (2) AR/results PDF review. No E1-grade events found in any window.

### equity_increase_solely_bonus_split
- infy_2020-03-31: True (FY16, FY19 increases both 1:1 bonus-proven; FY18/FY20 decreases are buybacks)
- infy_2021-03-31: True (FY19 bonus-proven; no other increases)
- sbin_*: True (no equity capital changes FY18–FY21)
- srf_*: True (no changes FY14–FY19)
- lt_*: True (FY18 increase bonus-proven 3:2 ex 2017-07-13; FY17/FY19 small ESOP increments <1% deemed non-material)
- endurance_*: **False** (FY17 increase 18→141 was Oct 2016 IPO, not bonus/split)

## Validation
- `NameDate(**data)` construction: 10/10 OK (engine never executed)
- `schema_check.py`: 10/10 PASS, zero warnings

## Named gaps / caveats
1. **endurance Mar-2019/Mar-2020 pledged**: ARs contain zero "pledge" mentions → named gap; lists use Mar-2017/Mar-2018 (latest PIT-valid sourced). D1 will use Mar-2018 as scoring quarter.
2. **srf FY17 CA/CL**: from FY18 PDF comparative (FY17 standalone PDF scanned/unextractable).
3. **SBIN CAMEL**: secondary sources (JM Financial, MPRA, tradebrains) for GNPA/Cost-Income/CASA; not pure screener ratios. Documented deviation.
4. **srf FY20, endurance FY21 results_published**: exact NSE dates not recovered → None; both post-scoring, no PIT impact.
5. **LT FY17/FY19 equity increments**: small ESOP-driven (<1%), deemed non-material for bonus/split test.

## Files
- 10 JSONs: `<name_date>.json` in this directory
- Raw: `_raw/<slug>_series.json`, `_raw/<slug>_fy.json`, `_raw/nse/` (PDFs+txt)
