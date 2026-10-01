# W1 — Large-Cap Winner Candidates (v4 Phase-D winner set selection)

Axis: large-cap winners. Evidence-only. System NOT LIVE; no company is ever called investable.
Cache: `winmed_w1/cache/` (10 symbols, consolidated screener variant, 13 P&L years each).
Deliverables: `winmed_w1_leads.json`, `winmed_w1_firewall.json` (44 rows: 11 symbols × 4 d0s).

## Funnel

| Stage | Count |
|---|---|
| Initial shortlist (public-history winner theses) | 11 |
| Exclusion triage (burn list 243 + prior sets 77 company tokens) | 0 killed |
| March-FY / listing check | 1 killed (VBL — December FY) |
| **Proposed candidates** | **10 companies / 20 name-dates** |

## Exclusion kills (with reasons)

1. **Varun Beverages (VBL)** — December financial year (cache P&L years Dec 2014–Dec 2026). Fails the March-FY constraint; all 4 d0s returned "no FY published ≥63d before d0" in the firewall. Killed, not a near-miss.
2. R2/PR#13 residue: 6 of 9 R2 companies are in the local burn list (flfl, simplexinf, omaxe, adaniports, fsc, pfs+variants); the 3 unknown R2 names are from distressed/blow-up-examined Phase-C sweeps — all 10 W1 picks are healthy, continuously-listed large caps, so no overlap is plausible. None of the W1 names appears in any Phase-C blow-up dossier.
3. Demerger/rename identity check: TATACONSUM = Tata Global Beverages renamed (Feb 2020, same legal entity; Tata Chemicals consumer-business merger is an acquisition, not a phantom); BAJAJFINSV demerged from Bajaj Auto in 2008 (pre-window); LT's LTI carve-out 2016 (pre-window). No phantoms.

## Proposed candidates (one-line theses; doubles per company)

| # | Company (slug) | d0s | Scoring FYs | Consol. EPS | Corp actions | Firewall P_d0/P_G1 (informational) | Thesis |
|---|---|---|---|---|---|---|---|
| 1 | Infosys (infy) | 2020, 2021 | FY19 35.26, FY20 38.96 | 1:1 bonus ex 04-Sep-2018 (pre-window) | 0.862 ✓, 1.196 ✓ | COVID-era digital-transformation deal boom + large-deal wins → multi-year EPS compounding and sustained P/E re-rating (2020-25). |
| 2 | TCS (tcs) | 2019, 2020 | FY18 67.46, FY19 83.87 | 1:1 bonus ex 31-May-2018 (pre-window) | 0.934 ✓, 0.722 ✓ | Steady double-digit growth, buyback-supported capital return, margin discipline compounded through 2019-25. |
| 3 | ICICI Bank (icicibank) | 2020, 2021 | FY19 6.60, FY20 14.78 | none in window | 1.888 ✓, 2.999 ✗ | Post-2018 NPA-cleanup turnaround; retail/SME-led balance-sheet compounding → multi-year re-rating ~1.5×→~3× book (2020-25). |
| 4 | SBI (sbin) | 2021, 2022 | FY20 22.15, FY21 25.11 | none in window | 1.879 ✓, 1.73 ✓ | PSU-bank credit-cost normalization + corporate-book recovery drove the 2021-24 re-rating (~2.5× in 3 years). |
| 5 | Bajaj Finserv (bajajfinsv) | 2019, 2020 | FY18 16.65, FY19 20.23 | 5:1 split + 1:1 bonus ex 13-Sep-2022 (POST-window) | 1.734 ✓, 1.017 ✓ | Bajaj Finance + insurance twins compounding; holding-company value creation; 2020 d0 caught the COVID crash (P_d0 489 vs 703). |
| 6 | UltraTech (ultracemco) | 2020, 2021 | FY19 87.51, FY20 199.40 | none in window | 1.789 ✓, 2.761 ✗ | Consolidation-wave pricing power + capacity additions; post-COVID infra demand drove 2020-24 outperformance. |
| 7 | SRF (srf) | 2019, 2020 | FY18 16.08, FY19 22.33 | 4:1 bonus ex 13-Oct-2021 (POST-window); NO split ever | 1.357 ✓, 1.111 ✓ | Fluorochemicals/specialty-chemicals capex cycle + import substitution → multi-year re-rating (EPS 16→64 FY18-22). |
| 8 | L&T (lt) | 2021, 2022 | FY20 68.02, FY21 82.47 | none in window | 0.766 ✓, 1.209 ✓ | Domestic capex-cycle order-book boom + asset-monetization/NWC discipline drove the 2021-25 run. |
| 9 | Tata Consumer (tataconsum) | 2020, 2021 | FY19 6.23, FY20 4.80 | none (name change Feb 2020, same entity) | 4.574 ✗, 8.517 ✗ | Tata Chemicals consumer-business merger (Feb 2020) + branded-foods premiumization → D2C-era re-rating (~₹280→₹620 in a year). |
| 10 | Axis Bank (axisbank) | 2019, 2020 | FY18 1.78, FY19 19.59 | none in window | 3.226 ✗, 1.894 ✓ | Chaudhry-era cleanup + retail franchise rebuild → 2019-25 multi-year compounding from stressed-book lows. |

Notes:
- Scoring FY = latest FY with results published ≥63d before d0 (nominal FY-end+60d rule) = FY(N-1) for d0=31-Mar-N; firewall-confirmed per name-date.
- All scoring-FY consolidated EPS positive (U2 proxy); exact U1/U2 + per-name PIT verification are the coordinator's job.
- Firewall is **informational only** — NOT a selection gate; winners need not be fill-plausible. Several proposed name-dates exceed 2.0 (e.g. tataconsum's pathological 4.6-8.5: the inverse-DCF prices this low-EPS-growth name far below market — an anchor observation, not a data defect; cache year-span verified Mar 2015–Mar 2027).
- Theses from public market history only; no price-data fitting, no threshold grids, no tuning to engine outputs.

## Near-misses (considered, dropped)

jswsteel, hindzinc, abbottindia, indianhotels, cholafin, muthootfin, ltts, bluestar, cumminsind, balkrishnaind, atul, jkcement, kajaria, aiaeng, dlf, godrejprop, unitedspirits, eichermotors, techmahindra, hcltech — dropped for the 10-name axis budget / axis-diversity (kept IT:2, banks:3, NBFC/holding:1, cement:1, chemicals:1, infra:1, FMCG:1); all clear of exclusion lists and available as coordinator alternates.

## Data notes for the coordinator

- Truncated-cache check: all 10 caches show 13 P&L years (Mar 2015–Mar 2027) covering every d0; no truncated-cache artifacts.
- SRF: worker initially assumed a 5:1 split — search-verified it was a **4:1 bonus (Oct 2021)**, no split ever (Motilal Oswal corp-action log + Upstox split history).
- Bajaj Finserv: 5:1 split (FV ₹5→₹1) + 1:1 bonus, ex 13-Sep-2022, record 14-Sep-2022 — post-window for the 2019/2020 d0s.
- Infosys/TCS bonuses (Sep-2018 / May-2018) are pre-window; screener EPS series is already adjusted.
