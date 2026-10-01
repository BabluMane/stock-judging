# v6 Phase-D Pre-registration — FROZEN (Musey, 2026-10-01)

v5 retired as a failed pre-registered design (Phase-D FAIL on (b): E5's
90d/YoY veto killed 3/5 winner companies; anchor never touched
balkrisind/godrejcp). v6 = fresh mechanism (E6: stock-flow consistency
veto replaces E5) + fresh pre-reg (this document) + fresh zero-overlap
OOS set.

## Frozen engine

- Tree: `d5ebd2efd0609ef7d90cc675bdeeb64e392d86a6` (`engine_v6/`).
- Spec: `engine_v6/V6_SPEC.md`, SHA-256 pin
  `173f902a7ad637387e32eba93dbbb3a4d32987891d87a89fca74d5a9fa1d717e`
  (self-pin procedure, §13; parent-verified).
- Tests: 171/171 green (parent-ran). 5/5 E6 mutations killed.
- E6 boundary probes (parent-run): 109.5d/CFO<0 → TRIP; 109.5d/CFO>0 →
  PASS; CFO=0 → TRIP (inclusive); days=90.0 exact → PASS (strict);
  missing recv/CFO/sales≤0 → UNCOMPUTABLE (never silent pass).
- G1 decisions (Bablu, 2026-10-01) applied verbatim — see V6_SPEC.md §3.1.
  Only the E5→E6 surface differs from the frozen v5 tree; D1–D7, E1–E4,
  and the anchor are byte-identical (parent-verified tree diff).

## The live bar (§1, UNCHANGED — PASS requires all legs)

- (a) 0 blow-up fills (hard). Scored at entry; in-window exits do not un-fail.
- (a′) distress screen (D1–D7 + E1–E4 + E6) decisional on ≥3/4 blow-up
  name-dates. Decisional = frozen §8.2: a TRIPPED rule blocked a fill the
  anchor would otherwise have made. VETOED-DATA does not count. An
  unexercised 0 is VOID.
- (b) ≥3 distinct winner companies with fills.
- (c) to-T aggregate clearly positive. (d) 24m aggregate ≥0.8×.
- Aggregation: leg-weighted means, price return only (§6.4).

## Set shape (declared; names found by the sweep, frozen separately)

- 24 name-dates / 14 companies: 4 blow-up name-dates, 10 winner
  name-dates (5 companies × 2), 10 mediocrity name-dates (5 × 2).
- **Zero overlap:** no name-date or company from ANY v4 set (Phase-D 25,
  Gate-1 pools, R1–R7 sweep candidates) or ANY v5 set (Phase-D 24,
  sweep kills). The v6 design was informed by v5 failures; the test
  set must be unseen. E6's marginal decisionality on v5 data is nil
  (E1/E2 already veto both v5 blow-ups) — its certification happens on
  this fresh set, per G1.
- **Disjoint:** no company appears in two tiers.
- Blow-up certification: dated trigger event (auditor resignation /
  qualified opinion / fraud disclosure), clean pre-event tape, exact
  U1/U2 PASS, fill-plausibility firewall ≤2.0 — same as v4/v5 Gate 1.
- **Derating-aware winner selection (G1):** winners are selected on
  scoring-date derating — zyduslife_2022 template (P_d0/P_G1 ≤ ~1.2).
  v6 research established eligibility ≠ fillability: E6-eligible
  winners can sit 1.5–3.2× under P_G1 with zero in-window touches.
  The sweep must screen P_d0/P_G1 as part of winner certification.

## Honest residuals (named before the run)

- The 90d in E6 is a carried definitional constant (E5's G1 rationale:
  one quarter of annual sales uncollected), disclosed, not re-fit —
  same disclosure class as v5's E3 margin.
- CFO≤0 is inclusive: CFO exactly 0 trips (literalism doctrine, same as
  v5 E2's whiteorganic NI=0 trip). Disclosed, not hidden.
- No cheap signal catches every blow-up (v4 §5.6 lesson carried): if the
  sweep certifies a name-date no E/D rule trips at scoring, the pre-reg
  names it as the residual — it does not move the bar.

## Input schema (unchanged from v5)

- `tax_expense` (₹cr/FY, screener Tax % × PBT — E4).
- `receivables`, `ppe_net`, `rpt_loans` (₹cr/FY — E6 + Beneish/RPT reporting).
- AR-bundle rule: one extraction pass per name-date (auditor's report + BS +
  notes), never piecemeal. Missing required field ⇒ UNCOMPUTABLE-DATA veto.

## Run mechanics (locked, one-shot — same discipline as v4/v5 §8.4)

- Frozen engine_v6 runs all 24 manifest name-dates exactly once; no
  aggregation or bar verdict in the runner; audit after.
- Same-set reruns forbidden. Amendments require Bablu's explicit
  authorization + pre-registration before execution.
- VOID/FALL rules: <3/4 decisional → VOID (then fresh set, never a patch).
  Any blow-up fill → FAIL (design failure, v6 retires the same way v4/v5 did).
