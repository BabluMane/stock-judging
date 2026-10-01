# v4 Phase-D Amendment-1 re-run — AUDIT (Musey, 2026-10-01)

**Verdict: FAIL. System NOT LIVE.**

The re-run executed cleanly (25/25, frozen engine `6ea7e7a1…`, spec hash
matches pin, 20/20 unchanged inputs bit-identical to the VOID run —
determinism proven). With complete blow-up data, the distress screen judged
all five name-dates on the merits. It vetoed one (PBM 2020, genuine D1 trip),
passed three through usability/data gates, and **filled two certified
blow-ups**. Per the frozen bar, scored at entry: the fills stand.

## Bar

| Leg | Bar | Result |
|---|---|---|
| (a) | 0 blow-up fills (hard) | **4 filled legs on 2 blow-up name-dates — FAIL** |
| (a′) | distress decisional ≥3/5 (frozen §8.2: tripped rules only) | **1/5 — FAIL** |
| (b) | ≥3 distinct winner companies with fills | 4 (infy, srf, lt, endurance) — PASS |
| (c) | to-T aggregate clearly positive | +1.432 mean over 13 filled legs — PASS |
| (d) | 24m aggregate ≥0.8× | 1.970× mean multiple — PASS |

## Per-name mechanics (phase_d_results_r2/)

- **supremeeng_2020-03-31 — FILLED G1+G2** (fill 2020-04-01 @ ₹1.61). Distress:
  D1 PASS (pledge 10.75% < 25%), D2 PASS (pledge present since Dec-2018, not
  first-time at scoring), D3 PASS (Z″=2.81), D4/D5 PASS. Exit scan fired
  exactly as designed: SEVERE T2 2021-11-03 (auditor resignation) → exit
  2021-11-04 @ ₹2.03, realized +24.8%. **The bar is scored at entry (§6): an
  exit does not un-fail a fill.**
- **supremeeng_2021-03-31 — FILLED G1+G2** (fill 2021-04-01 @ ₹2.75). Same
  distress picture (pledge 11.13%, Z″=2.43). Same exit event → exit @ ₹2.03,
  realized −26.9%.
- **pbm_2020-03-31 — decisional distress VETO** (`distress_decisional=true`,
  deciding_stop="distress"). D1 TRIPPED: 100% of promoter holding pledged in
  Sep-2019 and Dec-2019 (30/30 promoter shareholders, verified from the
  primary Reg-31 SHP filing), released by Mar-2020 — months before the
  Sep-2020 auditor-resignation disclosure. D2 did not trip (pledge already
  100% the prior quarter — correctly not "first-time"). This is the screen
  working as designed: 1/5 decisional.
- **pbm_2019-03-31 — excluded, deciding_stop="usability".** Distress all-PASS
  (pledge 0%, Z″=10.05). The usability data veto stands (untouched by the
  amendment).
- **varroc_2019-03-31 — excluded, deciding_stop="distress" (VETOED-DATA).**
  D1/D2 UNCOMPUTABLE — no tier-1 pledge series exists (listed Jul-2018;
  NSE/BSE/company sources yielded nothing honest). D3/D4/D5 PASS (Z″=2.96).
  Per frozen §8.2 a data veto is not decisional.

## Why this is a DESIGN failure, not a data failure

Every scoped value was parent-verified from primary sources (PBM Dec-2019
100% pledge from the filed SHP; SupremeEng FY19 CA/CL 161.10/121.84 from the
AR balance sheet to the paisa; AR/vendor TA residuals ≤1.15%, immaterial —
hand-computed Z″ values sit 2.2–9× above the 1.1 veto). The screen had the
facts and rendered its verdicts. Supreme Engineering's fraud was **clean at
scoring**: pledged 10.75% (below the 25% veto), balance sheet healthy
(Z″ 2.4–2.8), no first-time-pledge at the scoring quarter. All 13
state-based rules passed a company whose auditor would resign 19 months
later citing a fee dispute.

The spec anticipated this exact residual (§5.6 honest-residual-risk clause:
"fraud clean at scoring passes every rule; the hard 0-blow-ups bar prices
it in"). The bar priced it in. The event lane contained the damage
post-fill (both exits fired on the resignation), which is all §5.4 promises —
but containment is not the bar.

## Consequences (standing rule)

Per Bablu's rule — failed designs need a **fresh mechanism**,
pre-registration, and **fresh OOS evidence** (no amendment to this set).
Candidate directions for the next design (not pre-registered, not decided):
pledge-level sensitivity below 25%, auditor-tenure/fee-dispute signals,
resignation-history features — i.e., a mechanism that sees concealed fraud,
not just stated distress. The v4 engine, set, and bar are retired as a
failed pre-registered design. Nothing about this verdict softens the bar.

## Provenance

- Amendment: V4_OOS_PREREG_AMENDMENT_1.md (pre-registered before any re-run).
- Patches: validation/v4_oos/amend1_patches/ (5 patch JSONs + completion log
  + 3 worker logs). Parent audit: A4 (d0-quarter Mar SHPs excluded per the
  standing pledge-PIT convention, uniform with the 20 winner/mediocrity
  inputs); A1–A3 accepted (basis residuals immaterial, documented).
- Diff audit: exactly the scoped fields changed on exactly the 5 name-dates;
  other 20 inputs byte-identical; schema_check 25/25 PASS.
- Runner: one argv-only harness change (results-dir override, default
  reproduces the VOID run); engine_v4 untouched (tree 6ea7e7a1…).
- VOID run preserved in phase_d_results/; re-run in phase_d_results_r2/.
