# Anant Raj Ltd (ANANTRAJ) — Live Review

**as_of:** 2026-10-07 | **tier:** FULL | **status:** validated

## Verdict: PASS — conviction 0.75

Excluded by the engine (distress STOP). Real business, real execution, but the
spec's distress screen fires on paper-profits-without-cash and the price is ~6x
the sustainable-growth fair value. Not investable at current levels.

## Engine trace

| Gate | Verdict | Detail |
|---|---|---|
| distress | **STOP (VETOED-DISTRESS:E1)** | Sloan accruals +14.5% > 10%: FY26 PAT Rs 559 cr vs CFO Rs **−435 cr** |
| usability | PASS | U1 basis clean; U2 EPS 15.42 > 0; U3 gap 0% (results week 2026-05-11) |
| event_lane | PASS | No vetoes at d0 |
| anchor | valued → NO_TOUCH | FV Rs 95.05 (g_sus 9.1%, w 13.3%, beta 1.579); triggers G1 Rs 84.42 / G2 Rs 71.46; p_d0 Rs 577.85 |

Deciding gate: **distress**. Legs: G1/G2 NO_TOUCH (no post-d0 bars in live review;
price 8.1x the invest trigger anyway). Computability gate: 0 VETOED-DATA (D3
CA/CL filled from the AR balance sheet: CA 3,667 / CL 376; identity-checked).

## Key numbers (FY26, consolidated)

- Sales Rs 2,512 cr (+22%), PAT Rs 559 cr (+31%), EPS Rs 15.42, net margin 22.3%
- ROE 9.7%, ROCE ~12%, P/E 37.5x, P/B 3.6x (BV Rs 160.66)
- Total debt Rs 606 cr, D/E 0.10; cash Rs 911 cr; promoter 57.42%, pledge **0%**
- Mcap ~Rs 20,800 cr at d0 price

## Thesis

Anant Raj is executing — FY26 revenue +22%, PAT +31%, near-zero net debt, zero
pledge, and a credible data-centre pivot (28 MW operating, 357 MW planned with
the Andhra MoU, $2.1bn capex). But two hard facts dominate: **(1)** the distress
screen vetoes it on E1 — FY26 generated Rs 559 cr of profit and Rs −435 cr of
operating cash, a 14.5% Sloan accrual gap that is exactly the
paper-profits-without-cash signature the spec was built to catch (FY25 CFO was
+Rs 253 cr, so this is volatility, not proven fraud); **(2)** the inverse-DCF
anchor values the sustainable business at Rs 95/share vs Rs 578 market — the
data-centre dream is priced for flawless execution.

## Risks

- E1 veto: cash conversion must re-prove itself; negative FY26 CFO is the
  single largest fact against the name
- Valuation: ~6x FV; implied growth > hurdle+1pp — no margin of safety
- $2.1bn DC capex execution: 28 MW operating is ~8% of the FY32 target
- Realty lumpiness + QIP dilution (promoter 60.1%→57.4%)
- FII/MF selling (13.68%→10.74% / 4.46%→3.04% in a year)

## What would change it

1. CFO turning durably positive alongside profits (E1 clears)
2. Price falling to the trigger ladder (Rs 71–84) — an ~87% decline
3. Data-centre revenue crossing ~25–30% of sales with contracted cash flows
   (re-rates the growth narrative, not the engine verdict)

## Promises (tracker)

| Promise | Status | Delivery |
|---|---|---|
| FY26 performance (rev +21.9%, PAT +30.8%) | delivered | HIT — margins expanded to 28.04% |
| Rs 1,100 cr QIP (Oct-2025) | delivered | Completed; cash Rs 911 cr Mar-2026 |
| Final dividend Rs 1/share FY26 | delivered | Recommended May-11-2026 |
| DC roadmap: 28 MW → 117 MW FY28 → 357 MW FY32 | in-progress | On track; Ashok Cloud + Submer tie-ups |
| DC/cloud demerger evaluation | pending | Committee formed May-2026, no outcome |
| NCR residential execution | in-progress | 228 Birla Navya units handed over |

## Data notes

- Consolidated basis throughout (screener /consolidated/, full tables)
- Beta 1.579 (60m weekly, ISO-week join, same-interval endpoints)
- p_d0 Rs 577.85 (strict PIT: last bar ts ≤ d0−7d); shares 36 cr (FV Rs 2)
- Receivables FY26 Rs 179 cr (= Sundry Debtors, smart-investing.in BS; backout agreed)
- QIP Oct-2025 confirmed → equity_increase_solely_bonus_split = false
