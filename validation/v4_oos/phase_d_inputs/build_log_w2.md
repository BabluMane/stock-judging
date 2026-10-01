# W2 Phase-D Data Assembly Build Log — 10 Mediocrity Name-Dates

**Date:** 2026-10-01  
**Worker:** W2 (mediocrities)  
**Status:** 10/10 assembled, schema_check PASS

## Name-Dates Assembled

| key | d0 | Scoring FY | results_published | Beta |
|-----|----|------------|-------------------|------|
| drreddy_2019-03-31 | 2019-03-31 | FY2018 | 2018-05-22 | 0.4328 |
| drreddy_2020-03-31 | 2020-03-31 | FY2019 | 2019-05-17 | 0.4328 |
| dabur_2020-03-31 | 2020-03-31 | FY2019 | 2019-05-02 | 0.8755 |
| dabur_2021-03-31 | 2021-03-31 | FY2020 | 2020-05-27 | 0.8755 |
| maruti_2019-03-31 | 2019-03-31 | FY2018 | 2018-04-27 | 0.6806 |
| maruti_2020-03-31 | 2020-03-31 | FY2019 | 2019-04-25 | 0.6806 |
| cyient_2020-03-31 | 2020-03-31 | FY2019 | 2019-04-25 | 1.2816 |
| cyient_2021-03-31 | 2021-03-31 | FY2020 | 2020-05-07 | 1.2816 |
| auropharma_2019-03-31 | 2019-03-31 | FY2018 | 2018-05-28 | 0.8979 |
| auropharma_2020-03-31 | 2020-03-31 | FY2019 | 2019-05-28 | 0.8979 |

## Sources

### Beta
From `~/workspace/stock-judging/v3/validation/v4_oos/phase_d_inputs/_beta_table.json` (found 2026-10-01). Yahoo Finance 5Y-monthly adjusted closes vs NIFTY 50 (^NSEI), as_of 2026-10. Numeric values extracted from dicts.

### FY Financials
From W3 screener caches: `~/workspace/stock-judging/port/validation/v4_oos/winmed_w3/cache/*.json`. Fields: equity_capital, reserves, total_assets, borrowings, sales, interest, depreciation, pbt, net_profit, eps, cfo. Extracted to `/tmp/w2/fy_cache_data.json` (2026-10-01).

**Gaps:** current_assets, current_liabilities = None for 13/15 FYs (JS-gated on screener per AGENTS.md lesson). Only Dabur FY19/FY20 have CA/CL from real AR (see below). Consequence: D3 UNCOMPUTABLE → VETOED-DATA on affected name-dates.

**Dabur CA/CL from AR:** dabur.com AR FY20 PDF (https://www.dabur.com/img/upload-files/3244-Dabur-IR-2019-20.pdf):
- Mar 2020: CA 4,880.26 / CL 2,463.88
- Mar 2019: CA 3,586.23 / CL 2,660.31
- Note: AR total assets 9,354.01 vs screener cache 9,337 (Mar 2020) — discrepancy logged.

**material_cost:** None for all (F_dMARGIN fail-closed 0, spec-sanctioned).  
**revaluation_reserve:** None (optional).

### results_published Dates (sourced 2026-10-01 via browser.search)
- drreddy FY2018: 2018-05-22 (earnings call, biospace.com + tijorifinance transcript)
- drreddy FY2019: 2019-05-17 (press release "Hyderabad, India, May 17, 2019", drreddys.com)
- dabur FY2019: 2019-05-02 (HDFC result calendar "02-May DABUR"; broker notes May 3-4)
- dabur FY2020: 2020-05-27 (screener filing "Date: May 27, 2020"; HinduBusinessLine)
- maruti FY2018: 2018-04-27 (HinduBusinessLine "Published on April 27, 2018")
- maruti FY2019: 2019-04-25 (prior session work)
- cyient FY2019: 2019-04-25 (from cyient.com PDF filename 25042019BMoutcomeResults.pdf)
- cyient FY2020: 2020-05-07 (newswire.ca "HYDERABAD, India, May 7, 2020"; BSE filing)
- auropharma FY2018: 2018-05-28 (earnings presentation "28th May 2018")
- auropharma FY2019: 2019-05-28 (news release "28 May 2019, Hyderabad, India")

Non-scoring FYs carry results_published=None (engine filters them per pit.py).

### Prices, EPS Series, Corp Actions, Mcap
From phase-1: `/tmp/w2/raw/*_core.json` (901 weekly adjusted closes/company, TTM EPS series, corp actions). Mcap/price from 2026-10-01 fresh quotes in `phase1_report.json`:
- drreddy: ₹1,01,451 Cr @ ₹1,215
- dabur: ₹67,889 Cr @ ₹383
- maruti: ₹3,67,348 Cr @ ₹11,684
- cyient: ₹12,180 Cr @ ₹1,096
- auropharma: ₹96,839 Cr @ ₹1,683

### Pledge (sourced 2026-10-01)
- drreddy: 0%/0% | dabur: 0%/0% | maruti: 0%/0% | cyient: 0%/0% | auropharma: 3.49%/4.99%
- D1 all PASS; D2 N/A.

### Sectors (verbatim from screener)
- drreddy: "Healthcare" | dabur: "Fast Moving Consumer Goods" | maruti: "Automobile and Auto Components" | cyient: "Information Technology" | auropharma: "Healthcare"

## Events Two-Source Check

**Method:** browser.search for "[company] auditor resignation fraud 2018 2019 2020" + auditor report verification via indiainfoline.com. Search date: 2026-10-01.

**Result:** events=[] for all 10 name-dates.

**Findings logged (not qualifying events under v4 spec):**
- Dr Reddy's: US securities class action (2017-2019, settled 2020) re cGMP; FCPA investigation disclosed Nov 2020 (closed 2026). Neither is auditor resignation/qualified opinion/accounting fraud.
- Dabur: Auditor reports state "no resignation of statutory auditors" — clean.
- Maruti: Ex-MD Jagdish Khattar personal bank fraud case (Dec 2019) re his private venture Carnation Auto, not Maruti Suzuki. Auditor report notes a recent (2024/25) resignation with "no issues" — outside 2018-2021 windows.
- Cyient: "No resignation of statutory auditors" — clean.
- Aurobindo: "No resignation" + "no fraud reported to Audit Committee". 2024 FIR against non-executive director (outside windows). 2015 Natrol lawsuit: Aurobindo was plaintiff, not defendant.

## PIT Assertions

Per pit.py `select_scoring_fy` with 63-day rule (cutoff = d0 - 63d):
- All 10 have qualifying scoring FYs with results_published ≤ cutoff.
- Verified via schema_check.py: `select_scoring_fy` matches manifest scoring_fy for all 10.

## Named Gaps

1. **CA/CL missing for 13/15 FYs** (all except Dabur FY19/FY20): D3 UNCOMPUTABLE → VETOED-DATA. Source limit: screener static HTML hides behind JS.
2. **material_cost=None for all**: F_dMARGIN fail-closed 0 (spec-sanctioned).
3. **"Dr Reddy FY18 AR" from rayrc.com discarded**: was a broker report, not an Annual Report.

## Verification

- `NameDate(**data)` construction: 10/10 OK
- `schema_check.py`: 10/10 PASS (W2 name-dates only; W1/W3 files are other workers' scope)
