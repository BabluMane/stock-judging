# v4 Phase-D Amendment 1 — blow-up data completion + re-run (PRE-REGISTERED 2026-10-01)

Status: PRE-REGISTERED (Bablu authorized Option B, 2026-10-01). No result from
the re-run exists at the time of writing.

## Trigger
Phase-D locked run of 2026-10-01 returned **VOID (UNTESTED)**
(port/validation/v4_oos/AUDIT_PHASE_D.md): 0 blow-up fills numerically, but
distress decisional 0/5 — all five fills blocked by VETOED-DATA
(D1/D2/D3 uncomputable), zero tripped rules. Root cause: data-assembly gap
(the AR-sourcing pass was not extended to the 5 blow-up name-dates), not a
design or set failure.

## Scope (closed — nothing else changes)
- **Name-dates:** exactly the 5 certified blow-ups
  (supremeeng_2020-03-31, supremeeng_2021-03-31, pbm_2019-03-31,
  pbm_2020-03-31, varroc_2019-03-31).
- **Fields:** `fy[scoring_FY].current_assets`, `fy[scoring_FY].current_liabilities`
  (D3 Altman), and `pledge[]` quarterly promoter-pledge % series (D1/D2).
- **Everything else byte-identical:** verified by diff of the 25 input JSONs
  pre-run; any diff outside the listed fields aborts the re-run.

## Sourcing rules
- Tier-1 only: company annual reports (audited balance sheet for CA/CL) and
  BSE/NSE shareholding-pattern filings (quarterly promoter pledge %).
- PIT: CA/CL from the scoring-FY AR (published before d0 by the 63-day rule);
  pledge quarters ≤ d0 (the engine's `_quarters_upto` enforces this).
- No interpolation, no proxies, no "not visible = zero": a genuinely
  unavailable value stays missing → the rule stays UNCOMPUTABLE (honest).
- Per-value source recorded in the completion log (which AR page / which
  filing date).

## Re-run mechanics
- Same frozen engine (`engine_v4` tree 6ea7e7a1de50ccfaccd466a4e1f402efbd3ebbe3 —
  verified unchanged), same 25 name-dates, same locked runner, **one**
  execution. Results go to `phase_d_results_r2/`; the VOID run's
  `phase_d_results/` is preserved untouched.
- Pre-run gates (same as before): spec hash pin, 25/25 schema_check PASS,
  63-day PIT, input diff confined to the scoped fields, engine tree check.

## Bar (UNCHANGED — all five legs)
(a) 0 blow-up fills; (a′) distress decisional ≥3/5 (tripped rules only —
VETOED-DATA does not count, per the frozen §8.2 implementation);
(b) ≥3 distinct winner companies filled; (c) to-T aggregate clearly positive;
(d) 24m aggregate ≥0.8×.

## If the re-run still yields <3 decisional
The blow-up leg is UNTESTED and the re-run is VOID; the project proceeds to
Option A (new pre-reg + 5 fresh blow-ups, full zero-overlap). No further
amendments to this set.

## Why this amendment is legitimate (not bar-softening, not tuning)
The added values are objective audited/filed facts the assembly should have
contained; the rules are frozen and have no tuning knob — they trip on the
real numbers or they don't. The bar, the set, and the engine are untouched.
