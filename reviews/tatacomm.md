# Tata Communications Ltd (NSE: TATACOMM) — Live Review

**As of:** 2026-10-08 · **Status:** validated · **Tier:** FULL
**Verdict: PASS** (conviction 0.45) · **DCF fair value:** Rs 2159.54 (BETA-DISTORTED — see below) · **Price:** Rs 1818.80

## Engine summary

| Gate | Result |
|---|---|
| Distress | **VETOED-DATA** (deciding gate). D1/D2 PASS (pledge 0%), E1/E2/E3/E4/E6 all PASS, D4 PASS, D5 PASS. D3 UNCOMPUTABLE — current_assets/current_liabilities missing from input (same structural AR gap as all 23) |
| Usability | **STOP — U3**: vendor TTM EPS Rs 26.93 vs sourced Rs 35.14, gap 23.4% > 15% (results week 2026-06-18). U1 PASS (no action after FY-end), U2 PASS (sourced EPS 35.14 > 0) |
| Event lane | PASS — no taxonomy events at d0 |
| Anchor | VALUED — 2-stage fade FCFF 20y, g_sus 15% (capped), margin 15% (5yr avg), w 6.63% (beta −0.079). FV Rs 2159.54; G1 (ACC) Rs 1647.80, G2 (INV) Rs 1095.30. Price sits 15.8% below FV, 10.4% above G1, 66% above G2. Legs NO_TOUCH (live review). **WARNING: w=6.63% is beta-distorted — at w=9% FV=Rs 711, at w=11% FV=Rs 280. Mechanical FV is not usable as fair value.** |

Excluded: yes (distress veto). Scores: composite 5.15 · A 5.00 · B 3.75 · C 7.00 · D 5.00 · E 5.00 · F 5.00.

## Thesis

Tata Group's telecom-infrastructure arm (subsea cables, data centers, enterprise networking) carries the best governance in the new batch — credibility 7.4/10 → C5=2, zero pledge, promoter 58.9% in the 40-75 band. ROCE 19% clears cost of capital (A1=2). But the business is mediocre (A=5.0): 7.7% 5yr sales CAGR with a down year in window, net profit halved FY25→FY26 (Rs 1,837 cr → Rs 997 cr), and other income was 45% of PBT in FY25. The valuation case is the real problem — the negative beta (−0.08) produces w=6.63%, and any sane discount rate (9–11%) puts fair value 60–85% below the Rs 1,819 CMP. The market prices in growth the business isn't delivering. PASS.

## Key metrics

FY26: sales Rs 24,803 cr · PAT Rs 997 cr · EPS Rs 35.14 · EBITDA margin 20.1% · net margin 4.0% · promoter 58.86% (pledge 0%) · borrowings Rs 12,249 cr · mcap Rs 48,151 cr · P/E (TTM) 51.8 · beta −0.08 (59m)

## Promise tracker

Credibility 7.4/10 → C5=2 (7 calls, 56 promises). Selected:
- **Debt-to-EBITDA under 2x** — DELIVERED: 1.99x at Q4 FY26 (net debt Rs 9,601 cr), though it overshot the original deadline by two quarters
- **ROCE bottomed, gradual recovery** — DELIVERED: Q4 FY26 ROCE 14.9% (+51bp QoQ)
- **Double-digit EBITDA growth FY27** (new CEO) — PENDING (Q1 FY27 call)
- **Rs 28,000 cr revenue North Star FY27** — CUT before period end: moved to FY28 in Investor Day deck
- **23–25% EBITDA margin ambition** — CUT: pushed to FY28 in corporate presentation
- **CapEx 11–12% of sales** — MISSED: FY26 cash capex Rs 2,433 cr = 9.8% of revenue

Pattern: operational promises (deleveraging, ROCE) delivered; ambitious growth/margin targets quietly pushed out.

## Risks

- **Valuation rests on a statistical artifact**: beta −0.079 → w=6.63%; at w=11% FV=Rs 280 vs CMP Rs 1,819. There is no margin of safety at any reasonable discount rate
- **Earnings collapse FY26**: PAT Rs 1,837→997 cr (−46%), EPS 64.43→35.14; U3 usability STOP on 23% vendor/sourced EPS gap
- **Growth anemic**: 7.7% 5yr CAGR vs 12% bar; down year in window; core connectivity guided only "low to mid-single-digit"
- **Leverage**: borrowings Rs 12,249 cr (25% of mcap); net debt Rs 9,601 cr even after deleveraging
- **Earnings quality**: other income 45% of PBT in FY25; FY22 other income was 92% of PBT
- **G1 VETOED-DATA** (structural D3 gap — same as all 23)

## What would change this

1. **A sane valuation entry** — the mechanical triggers (G1 Rs 1,648 / G2 Rs 1,095) are beta-distorted and unusable. A real entry would need the price to fall toward Rs 700–900 (roughly 9–10% discount rate FV range) with earnings stabilized.
2. **Earnings recovery** — two consecutive FYs of PAT growth with ETR normalization would repair the quality case; FY27 double-digit EBITDA growth guidance is the test.
3. **G1 clearing** — D3 needs current_assets/current_liabilities from the annual report (the binding AR deep-dive requirement).

## Data notes

- Input: port/data/inputs/tatacomm.json (FY15–FY26, screener basis). results_published null → scoring FY = latest (2026).
- Beta −0.0788, 59 months, corr −0.031 — economically meaningless; flagged throughout.
- Prices: TATACOMM_NS parquet through 2026-07-21; p_d0 Rs 1818.80. 52w high Rs 2061.70 (−11.8%), low Rs 1335.75 (+36.2%).
- Pledge 0% (8 quarters, Sep-2024→Jun-2026). SHP Jun-2026: promoter 58.86%, FII 13.75%, DII 19.85%.
- No splits/bonuses in window; dividends only.
