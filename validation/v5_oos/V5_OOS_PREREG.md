# v5 Phase-D Pre-registration — FROZEN (Musey, 2026-10-01)

v4 retired as a failed pre-registered design (Phase-D R2 FAIL: concealed fraud
filled 2 certified blow-ups). v5 = fresh mechanism (earnings-quality vetoes
E1–E5) + fresh pre-reg (this document) + fresh zero-overlap OOS set.

## Frozen engine

- Tree: `c951e3f3974cf417dd20a04824d5a85074196fdd` (`engine_v5/`).
- Spec: `engine_v5/V5_SPEC.md`, SHA-256 pin
  `f2eb5b5cfb3c97243e33fd5809e58b18a7033469133238274ea37aecd5f2f84d`
  (self-pin procedure, §13; verified).
- Tests: 167/167 green; 17/17 new-constant mutations killed.
- G1 decisions (Bablu, 2026-10-01) applied verbatim — see V5_SPEC.md §3.1.

## The live bar (§1, UNCHANGED — PASS requires all legs)

- (a) 0 blow-up fills (hard). Scored at entry; in-window exits do not un-fail.
- (a′) distress screen (D1–D7 + E1–E5) decisional on ≥3/5 blow-up name-dates.
  Decisional = frozen §8.2: a TRIPPED rule blocked a fill the anchor would
  otherwise have made. VETOED-DATA does not count. An unexercised 0 is VOID.
- (b) ≥3 distinct winner companies with fills.
- (c) to-T aggregate clearly positive. (d) 24m aggregate ≥0.8×.
- Aggregation: leg-weighted means, price return only (§6.4).

## Set shape (declared; names found by the sweep, frozen separately)

- 25 name-dates / 13 companies: 5 blow-up name-dates (≤2 per company),
  10 winner name-dates (5 companies × 2), 10 mediocrity name-dates (5 × 2).
- **Zero overlap:** no name-date from ANY v4 set (Phase-D 25, Gate-1 pools,
  R1–R7 sweep candidates). The v5 design was informed by v4 failures; the
  test set must be unseen.
- **Disjoint:** no company appears in two tiers.
- Blow-up certification: dated trigger event (auditor resignation /
  qualified opinion / fraud disclosure), clean pre-event tape, exact U1/U2
  PASS, fill-plausibility firewall ≤2.0 — same as v4 Gate 1.

## Honest residuals (named before the run)

- E3's motivating catch won by 0.01 (IC 1.49× vs 1.50 line) — threshold luck,
  not mechanism triumph. Disclosed, not hidden.
- No cheap signal catches every blow-up (v4 §5.6 lesson carried): if the
  sweep certifies a name-date no E-rule trips at scoring, the pre-reg names
  it as the residual — it does not move the bar.

## Input schema (new v5 fields)

- `tax_expense` (₹cr/FY, screener Tax % × PBT — E4; NOT in v4 inputs, verified).
- `receivables`, `ppe_net`, `rpt_loans` (₹cr/FY — E5 + Beneish/RPT reporting).
- AR-bundle rule: one extraction pass per name-date (auditor's report + BS +
  notes), never piecemeal. Missing required field ⇒ UNCOMPUTABLE-DATA veto.

## Run mechanics (locked, one-shot — same discipline as v4 §8.4)

- Frozen engine_v5 runs all 25 manifest name-dates exactly once; no
  aggregation or bar verdict in the runner; audit after.
- Same-set reruns forbidden. Amendments require Bablu's explicit
  authorization + pre-registration before execution.
- VOID/FALL rules: <3/5 decisional → VOID (then fresh set, never a patch).
  Any blow-up fill → FAIL (design failure, v5 retires the same way v4 did).
