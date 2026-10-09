# AU Small Finance Bank Ltd (NSE: AUBANK) — Live Review

**As of:** 2026-10-08 · **Status:** validated · **Tier:** FULL
**Verdict: WATCH** (conviction 0.5) · **DCF fair value:** Rs 1607.82 (BETA-DISTORTED — see below) · **Price:** Rs 1003.30

## Engine summary

| Gate | Result |
|---|---|
| Distress | **VETOED-DATA** (financial variant, deciding gate). D1/D2 PASS (pledge 0%), D5 PASS. D6 CAMEL UNCOMPUTABLE — car_pct/casa_pct/cost_to_income/gnpa/roa missing. E-rules N/A by construction |
| Usability | PASS — U1 no-restatement (1:1 bonus ex 2022-06-09 pre-dates scoring FY), U2 sourced EPS 35.30 > 0, U3 gap 0.2% (vendor TTM 35.37 vs sourced 35.30, results week 2026-04-27) |
| Event lane | PASS — no taxonomy events at d0 |
| Anchor | VALUED (financial) — inverse excess-return 20y, book0 Rs 19,973 cr, ROE_avg3 12.6%, g_sus 12.6%, w 5.24% (beta −0.43). FV Rs 1607.82; G1 (ACC) Rs 1322.48, G2 (INV) Rs 1027.55. Price Rs 1003.30 is 37.6% below FV and 2.4% BELOW G2. Legs NO_TOUCH (live review). **WARNING: w=5.24% is beta-distorted — at w=8% FV=Rs 1042 (≈CMP), at w=11% FV=Rs 675 (33% overvalued), at w=12% FV=Rs 589. The mechanical 'cheapness' is a discount-rate artifact.** |

Excluded: yes (distress veto). Scores: composite 5.15 · A 8.00 · B 1.25 · C 6.00 · D 6.67 · E 5.00 · F 5.00.

## Thesis

The best-quality franchise in the new batch (A=8.0): 30.4% 5yr CAGR, RoE 13.2% clearing a (flattered) 4.4% COE, credibility 8.9/10 → C5=2 — the highest promise-keeping score we've recorded (153 promises, 7 calls). Zero pledge, clean usability, 78 branches added in FY26 as guided. But the valuation case collapses on inspection: the 37.6% "discount to fair value" is entirely a negative-beta artifact. At a sane 11% cost of equity — the minimum for an Indian bank — fair value is ~Rs 675, making the Rs 1,003 CMP about 33% overvalued. Promoter holds only 22.7% (below the 40–75 band); the register is FII 36% + DII 32.8%, i.e. flow-driven. Quality is real; price is not attractive. **WATCH** — revisit on a meaningful correction toward Rs 675–700.

## Key metrics

FY26: "sales" (total income) Rs 18,636 cr · PAT Rs 2,641 cr · EPS Rs 35.30 · net margin 14.2% · RoE 13.2% · credit cost 0.96% · cost-to-income 57.9% · promoter 22.74% (pledge 0%) · mcap Rs 73,409 cr · P/E (TTM) 28.4 · beta −0.43 (60m)

## Promise tracker

Credibility 8.9/10 → C5=2 (7 calls, 153 promises). Selected:
- **20–22% GLP growth FY26** — DELIVERED: +21% YoY to Rs 1,40,327 cr (2.36x nominal GDP, within guided 2–2.5x)
- **Credit cost ~1% FY26** — DELIVERED: 0.96% of average assets
- **Cost-to-income below 60%** — DELIVERED: 57.9%
- **70–80 new branches FY26** — DELIVERED: 78 added
- **CoF guidance 7.10–7.15%** — DELIVERED: 7.07%
- **Deposit growth 23–24%** — DELIVERED: +27% YoY to Rs 1,24,269 cr
- **NIM protected near 6%** — DELIVERED: 5.94% (Q1 FY27: 5.9%, down 7bp)

Pattern: exceptional delivery across growth, cost, and margin guidance — the most reliable management we've scored.

## Risks

- **Valuation illusion**: beta −0.43 → w=5.24%; at w=11% FV=Rs 675 vs CMP Rs 1,003. The DCF "upside" inverts to ~33% downside at sane rates. Do not anchor on Rs 1,608.
- **Price below mechanical G2**: Rs 1,003 < G2 (INV) Rs 1,027.55 — a naive trigger-follower would buy here. The trigger is beta-distorted and must be ignored.
- **Margin compression**: net margin 14.2% vs 10yr avg 21.1% (−7pp); NIM drifting down (5.94% → 5.9%)
- **Register structure**: promoter 22.74% — no anchor shareholder; FII/DII flows drive the price
- **SFB-to-universal-bank transition**: execution risk on the next charter step; branch expansion opex front-loaded
- **G1 VETOED-DATA** (structural D6 CAMEL gap — same as all 23)

## What would change this

1. **Price correction to Rs 675–700** — at a sane 11% COE this is roughly fair value; a dip below Rs 650 would open a genuine accumulation thesis on the best-quality lender in coverage.
2. **Beta normalization** — if the 60m beta reverts toward +0.8–1.2, the mechanical DCF would re-rate downward to honest levels and the trigger ladder would become usable.
3. **Universal bank license** — would structurally re-rate the franchise multiple; watch RBI communications.
4. **G1 clearing** — D6 needs CAR/CASA/cost-to-income/GNPA/RoA from filings (the binding AR deep-dive requirement).

## Data notes

- Input: port/data/inputs/aubank.json (FY15–FY26). Screener /consolidated/ only carries pre-SFB FY14–17; bank-era data from base page (documented, no mixing).
- Beta −0.4282, 60 months — economically meaningless for a bank; flagged throughout. Sensitivity table in anchor section.
- Prices: AUBANK_NS parquet through 2026-07-21; p_d0 Rs 1003.30. 52w high Rs 1072.10 (−6.4%), low Rs 694.30 (+44.5%). 20d avg volume ~21 lakh shares.
- Pledge 0% (8 quarters). SHP Jun-2026: promoter 22.74%, FII 35.98%, DII 32.81%.
- 1:1 bonus ex 2022-06-09 (pre-dates scoring FY; U1 no-restatement). Dividends Rs 0.25–1.00 across FY18–FY26.
