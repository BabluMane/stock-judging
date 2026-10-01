# v5 Phase-D Audit — FAIL, system NOT LIVE (Musey, 2026-10-01)

## Run integrity
- Engine: `c951e3f3` (frozen 5138436), spec pin `f2eb5b5c…84d` verified.
- Inputs: 24/24 frozen (259a19a); parent audit: 24/24 parse, E-trips
  independently recomputed, beta spot-check sane, tax_expense per spec
  (Tax% × PBT, 99 fields).
- Runner: one-shot `run_name_date` × 24, `phase_d_results/`, RUN_LOG with
  per-file SHA-256. No aggregation in runner. Zero v4 overlap, disjoint —
  machine-verified.

## Bar verdict
- **(a) PASS** — 0 blow-up fills. addshop/whiteorganic/mishtann all
  VETOED-DISTRESS (E1/E2/E1), ranasug PASS-distress but legs BLOCKED.
- **(a′) PASS** — 3/4 decisional (addshop, whiteorganic, mishtann;
  ranasug = named honest residual). Meets Amendment-1 ≥3/4.
- **(b) FAIL** — 1/3 winner companies filled (zyduslife only).
- (c) PASS — to-T mean +1.771 (2 legs). (d) PASS — 24m mean 1.771×.
- **Verdict: FAIL. v5 retires as a failed pre-registered design.**

## Why (b) failed — design failure, not data failure
1. **E5 false-positive rate (frozen-design property).** E5 vetoed 3 of 5
   winner companies, all spec-literal but economically dubious:
   - lauruslabs×2: 99–102d receivables — structural, industry-normal for
     pharma API; the rule has no industry calibration.
   - eichermot×2: receivables YoY 1.82× — COVID-base effect (FY20→FY21
     rebuild), not manipulation.
   - zyduslife_2024: 93.5d — 3.5 days over a hard 90d line.
   The Phase-1 FP screen (10 names) never tested E5 — AR fields didn't
   exist. The fire rate on real winners was unknowable until now.
2. **Anchor conservatism (v4's "0 compounder entries," unresolved).**
   balkrisind×2, godrejcp×2: distress PASS, usability PASS, valued —
   but triggers 60–70% below market (inverse-DCF hurdle vs priced
   compounders). NO_TOUCH. The one fill (zyduslife_2022) was a derated
   pharma name already below its trigger at d0.

## Consequences
- E1–E4 worked as designed on blow-ups (3/4 decisional, 0 fills). The
  failure is E5's winner fire rate + the anchor's entry scarcity.
- Any successor needs: (i) a recalibrated E5 (industry-relative days or
  higher bar — NOT a post-hoc tweak of this set), (ii) fresh pre-reg,
  (iii) fresh zero-overlap set. v5's mechanism is dead; its data is not
  reusable for validating a successor.
