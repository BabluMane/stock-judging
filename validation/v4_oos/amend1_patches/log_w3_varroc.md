# W3 log — varroc_2019-03-31 (Varroc Engineering Ltd, NSE VARROC / BSE 541578), scoring FY18, d0=2019-03-31

## Patched values

### fy[2018].current_assets = 3060.44 (Rs.cr), fy[2018].current_liabilities = 3173.03 (Rs.cr)
- Source (tier-1): FY18 audited consolidated balance sheet, Varroc Engineering Ltd Annual Report 2017-18.
  Raw figures: Total current assets **Rs 30,604.38 million**; Total current liabilities **Rs 31,730.31 million**.
  Component check: CA = 4,429.54+2,051.60+11,958.68+4,383.03+1,110.99+1,119.88+22.17+5,528.49 = 30,604.38 ✓;
  CL = 8,720.63+16,664.93+3,075.48+1,036.05+105.58+2,127.64 = 31,730.31 ✓.
- Auditor: Price Waterhouse & Co Chartered Accountants LLP, report signed **2018-06-06** — matches input `results_published: 2018-06-06`. PIT OK (pre-d0 by >63 days).
- Cross-confirmation: FY19 AR comparative column (signed 2019-05-24) prints FY18 CA **30,604.38M** / CL **31,730.31M** — exact agreement, two independent AR prints.
- ARs downloaded from Tijori Finance (tier-2 mirror of company ARs):
  `files.tijorifinance.com/insight/india/5925/Annual%20Report/AR-18.pdf` (72MB) and `AR-19.pdf`. Verified `%PDF`, 2018 report covers FY ended 31-Mar-2018.
- PIT note: input audited_prints fy_end 2018-03-31 / results_date 2018-06-06 consistent with the AR used.

### Basis caveat (flagged for parent adjudication — does not block the patch)
- Input fy[2018] is **screener-truncated consolidated**: verified live at screener.in/company/VARROC/consolidated/ —
  Equity Capital 12, Total Assets 6,802 match input exactly.
- AR-18 prints equity capital Rs 134.81M (=13.48cr) and total assets Rs 68,523.92M (=6,852.39cr).
- Partial reconciliation: AR-19 comparative reclassifies FY18 equity capital as Rs 123.13M (=12.31cr → screener's 12) + CCPS Rs 11.68M.
  Residual ~50.4cr total-assets gap (6,802 vs 6,852.39) unexplained — vendor-side, not a wrong-AR signal.
- Verdict: correct company, correct year, correct consolidated basis, correct auditor date. CA/CL are the doubly-confirmed right numbers.
  But the engine's Z''/O will mix AR-basis CA/CL with input-basis total_assets (6802.0). Parent decides whether to accept.

## Pledge series — NOT patched (tier-1 unobtainable by W3); gap honestly named

Per-quarter outcome:
- **2017-03-31 … 2018-03-31**: no SHP filings exist — company unlisted until 6-Jul-2018 (R7 dossier / input build log). Structural gap.
- **2018-06-30**: quarter ended pre-listing; no filed SHP. Structural gap.
- **2018-09-30, 2018-12-31, 2019-03-31**: tier-1 SHP not retrievable by W3:
  1. BSE `shpSecurities.aspx?scripcd=541578&qtrid=100.00` — fetch failed; runtime directive: do not retry via browser or other endpoints.
  2. varroc.com investor uploads — no SHP PDFs indexed or found (only financial_results/ and press releases).
  3. nsearchives.nseindia.com — only `SHP_VARROC_260321.pdf` (Mar-2021) indexed; dated filenames not guessable per URL rules.
- Tier-3 corroboration (NOT banked as patch values): Trendlyne quarter pages
  (trendlyne.com/equity/share-holding/93226/VARROC/Q3-2018, Q4-2018, Q1-2019) show pledged **0 shares / 0.00%**
  for every promoter in all three post-listing quarters; R7 dossier asserts "Pledge: 0.00%, no invocation".
- Consequence: D1 (2019-03-31) uncomputable on tier-1 evidence; D2 needs scoring quarter + ≥4 priors — maximum 3
  post-listing priors exist, so **D2 is unachievable by construction for this name-date** and stays honestly N/A.
  D3 (Altman Z''/O) computable from patched CA/CL. Even if tier-1 pledge were later confirmed at 0.00%,
  the pledge legs would be non-triggering — varroc's decisional contribution rides on D3 firing.

## Files
- Patch: `~/workspace/stock-judging/v3/validation/v4_oos/amend1_patches/varroc_2019-03-31.patch.json`
- Input (untouched): `~/workspace/stock-judging/v3/validation/v4_oos/phase_d_inputs/varroc_2019-03-31.json`
- AR PDFs were in /tmp (ephemeral) — re-download from the Tijori URLs above if needed.
