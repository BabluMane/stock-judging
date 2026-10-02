# v7 Phase-D Pre-registration — FROZEN (Musey, 2026-10-02)

v6 Phase-D VOID pre-run (2026-10-02, AUDIT_PHASE_D_VOID.md): KTL's beta was
null in the frozen input → anchor unvaluable → (a′) capped at 2/4 < 3/4 →
the spec's pre-run void rule fired. The one-shot was never executed. E6's
mechanism is UNTESTED, not refuted. v7 = the same frozen engine + fresh
pre-reg (this document) + fresh zero-overlap set + one new sweep screen.

## Frozen engine (carried, unchanged)

- Tree: `d5ebd2efd0609ef7d90cc675bdeeb64e392d86a6` (`engine_v6/`).
- Spec: `engine_v6/V6_SPEC.md`, SHA-256 pin
  `173f902a7ad637387e32eba93dbbb3a4d32987891d87a89fca74d5a9fa1d717e`
  (parent-verified 2026-10-01; untouched since).
- Tests: 171/171 green. 5/5 E6 mutations killed. 7/7 E6 boundary probes
  (parent-run).
- No engine change in v7. The VOID was a set defect, not a design failure.

## The live bar (§1, UNCHANGED — PASS requires all legs)

- (a) 0 blow-up fills (hard). Scored at entry; in-window exits do not un-fail.
- (a′) distress screen (D1–D7 + E1–E4 + E6) decisional on ≥3/4 blow-up
  name-dates. Decisional = frozen §8.2: a TRIPPED rule blocked a fill the
  anchor would otherwise have made (anchor trigger met in-window, screen
  veto active). VETOED-DATA does not count. An unexercised 0 is VOID.
- (b) ≥3 distinct winner companies with fills.
- (c) to-T aggregate clearly positive. (d) 24m aggregate ≥0.8×.
- Aggregation: leg-weighted means, price return only (§6.4).

## Set shape (declared; names found by the sweep, frozen separately)

- 24 name-dates / 14 companies: 4 blow-up name-dates, 10 winner
  name-dates (5 companies × 2), 10 mediocrity name-dates (5 × 2).
- **Zero overlap:** no name-date or company from ANY v4 set, ANY v5 set,
  or the v6 VOID set (frozen SET_MANIFEST.json — a frozen certified set
  counts as prior even though VOID; reusing its names would contaminate).
- **Disjoint:** no company appears in two tiers.
- Blow-up certification: dated trigger event, clean pre-event tape, exact
  U1/U2 PASS, fill-plausibility firewall ≤2.0 — same as v4/v5/v6 Gate 1,
  PLUS the new screen below.
- **NEW — beta-availability screen (the v6 lesson):** every blow-up
  name-date must have ≥12 months of price history at d0, so a PIT-valid
  trailing beta is computable for the frozen input. Screened at the
  FIREWALL (from price-history length, before dossier work), not at
  assembly. A null beta kills decisionality (§8.2 needs the anchor trigger);
  the sweep must never certify a name the frozen input cannot anchor.
  (Winners/mediocrities: beta null ⇒ assembly reject, same doctrine.)
- **Derating-aware winner selection (G1 carried):** P_d0/P_G1 ≤ ~1.2
  (zyduslife_2022 template). Eligibility ≠ fillability.

## Honest residuals (named before the run — carried from v6)

- The 90d in E6 is a carried definitional constant, disclosed, not re-fit.
- CFO≤0 inclusive (CFO exactly 0 trips — literalism doctrine).
- E6's marginal decisionality on v5 data was nil; its certification happens
  on THIS fresh set. The bar, not backtest, judges it.
- No cheap signal catches every blow-up: if the sweep certifies a name-date
  no E/D rule trips at scoring, the pre-reg names it as the residual.

## Input schema (unchanged from v5/v6)

- `tax_expense` (₹cr/FY, screener Tax % × PBT). `receivables`, `ppe_net`,
  `rpt_loans` (₹cr/FY). `beta`: required float — null ⇒ assembly reject.
- AR-bundle rule: one extraction pass per name-date, never piecemeal.
  Missing required field ⇒ UNCOMPUTABLE-DATA veto.

## Run mechanics (locked, one-shot — same discipline as v4/v5/v6 §8.4)

- Frozen engine_v6 runs all 24 manifest name-dates exactly once; no
  aggregation or bar verdict in the runner; audit after.
- Same-set reruns forbidden. Amendments require Bablu's explicit
  authorization + pre-registration before execution.
- VOID/FALL rules: <3/4 decisional → VOID (then fresh set, never a patch).
  Any blow-up fill → FAIL (design failure, v6/v7 retires the same way v4/v5 did).
