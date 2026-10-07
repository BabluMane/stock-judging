# V7_OOS_PREREG Amendment 2 — Data Completion (parent-authorized 2026-10-07)

## Trigger
The 2026-10-07 locked one-shot (frozen engine_v6, 22 inputs) returned 19/22
VETOED-DATA. The engine worked as designed (missing never passes silently);
the assembly left required fields null. This is a data defect, not a design
defect — same class as v4 Amendment 1 (2026-10-01), which Bablu authorized
and which resolved cleanly.

## Scope (closed)
ONLY the fields below, ONLY for the name-dates listed. Everything else in the
22 frozen inputs stays byte-identical. Engine_v6 untouched. Bar unchanged.

| Field | Name-dates | Source tier |
|---|---|---|
| D1/D2 pledge[] (SHP quarter ≤ d0) | bergerpaint×2, glaxo×2, granules_2023, karurvysya_2021, lalpathlab×2, recltd×2, tataconsum×2, ubl×2 | 1 (BSE filings) / 2 |
| D3 CA/CL (scoring FY) | granules×2, lalpathlab_2024, nationalum×2, oil×2 | 1 (AR balance sheet) |
| D4 equity_increase_solely_bonus_split | bergerpaint×2, lalpathlab_2024 | 1 (AR) |
| D6 CAMEL (car_pct, gnpa_pct, roa_pct, cost_to_income_pct, leverage_x) | karurvysya×2, recltd×2 | 1 (AR) |
| E6 receivables (scoring FY) | granules×2, nationalum×2, oil×2 | 1 (AR balance sheet) |

## Rules (v4-A1 carried over)
- Tier-1 sources preferred (filed ARs, BSE SHP filings); tier-2 only if tier-1
  truly absent, flagged.
- PIT-enforced: only information public ≤ d0. No interpolation, no forward-fill.
- If a field is genuinely unretrievable: report UNRETRIEVABLE with the
  search trail (don't silently null it).
- Workers are evidence-only: patches + extraction log. Parent applies after
  audit. Workers never execute the engine.

## New: computability gate (standing rule from this amendment)
Before the re-run freeze, the coordinator MUST run the frozen engine's gate
functions on all 22 patched inputs in audit mode. Zero VETOED-DATA is required
to proceed to freeze. Any remaining gap → one more targeted worker pass
(max 2 remediation passes total), then parent adjudicates.

## Re-run discipline
- Same frozen engine_v6, same 22 name-dates, same bar (Amendment 1).
- This is a data-completion re-run, not a new design. The 2026-10-07 run's
  distress verdicts (gitanjali E3/E4, securkloud E1, oil_2022 E4) stand as
  recorded engine outputs.
- Verdict scored against the amended bar: PASS → LIVE; FAIL → retire;
  VOID only if <2/2 decisional (not expected — both blow-ups already decisional).
