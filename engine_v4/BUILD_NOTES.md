# engine_v4 — build notes (PR description)

Implements `engine_v4/V4_SPEC.md` (byte-identical copy of the frozen spec; SHA-256 pinned in
`tests/test_constants.py`). Clean-room: nothing under `engine/`, `specs/`, `validation/` was touched.
**No prior validation set was run through this engine; nothing was tuned, gridded or calibrated.**

Run the tests (stdlib only, no new dependencies):

    python3 -m unittest discover -s engine_v4/tests -t .

## What is built

| Module | Spec | Notes |
|---|---|---|
| `constants.py` | §11, §1 | one definition per number |
| `anchor.py` | §2 | 2-stage fade FCFF, flat trailing-5y margin, triggers `P_G1 = V(g_h(0.875))`, `P_G2 = V(g_h(0.70))`, financial variant, reporting-only `g_implied` solver |
| `distress.py` | §3 | D1–D7, class split, UNCOMPUTABLE ⇒ VETOED-DATA |
| `usability.py` | §4 | U1 basis assertion, U2, U3 (check (b) and the financial exemption are absent, tested) |
| `events.py` | §5 | closed taxonomy T1–T7, SEVERE/MODERATE/WATCH, press-only cap, entry veto, cooling-off + 2-source search log, exit scan |
| `run.py` | §6, §7 | all four gates evaluated in parallel, fills, mandatory `exit_scan`, shadow pass |
| `aggregate.py` | §1, §5.5, §6, §7 | leg-weighted means, bar incl. (a′)/UNTESTED/VOID, lane-exercise tabulation, gate-trace table |

Input is a `run.NameDate` record (FY tables, weekly adjusted closes, shareholding quarters, unlagged EPS
series, corporate actions, event tape, audited prints). The engine never fetches anything and invents no field.

## §11 constants — spec value vs implemented value

| §11 constant | Spec value | Implemented value | Where it acts |
| --- | --- | --- | --- |
| Rf / ERP / TAX / TG | 6.95% / 4.0% / 25.17% / 4% | RF=0.0695, ERP=0.04, TAX=0.2517, TG=0.04 | carried |
| Anchor horizon | 20y (10y @g + 10y linear fade + terminal yr 20) | GROWTH_YEARS=10, FADE_YEARS=10, HORIZON_YEARS=20 | `growth_path`, `enterprise_value` |
| Fade shape | linear to TG | FADE_SHAPE='linear' | `growth_path` (t=11..19 linear, t>=20 = TG) |
| Margin | trailing-5y avg OPM, flat | MARGIN_WINDOW_FY=5; one `margin` used for all years | `dcf_inputs`, `fcff_flow` |
| WC / capex / netcash / shares / beta | 5% incr rev; capex≈dep; inv−borr; mcap÷price; sector β pre-run | WC_PCT=0.05; CAPEX_EQUALS_DEP=True; netcash & shares in `value_anchor`; β is an input | cancellation written out in `fcff_flow`, audited by `fcff_flow_uncancelled` |
| g_sus family incl. C1/C2/C3 | §2.2, cap 15% | G_CAP=0.15, ROE_YEARS=3 | `sustainable_growth`; parity with the v3.11 runner in `test_anchor.CarriedParity` |
| k | 0.875 / 0.70 | K_G1=0.875, K_G2=0.7 | `hurdle_growth`, `TIERS` |
| g_implied solver bounds | [−0.50, w−0.01] | SOLVER_LO=-0.5, hi=w−0.01 | `solve_implied_growth` (reporting only) |
| Fill mechanics | first weekly close, 24m, 1 leg/tier | FILL_WINDOW_DAYS=730, LEGS_PER_TIER=1 | `run._first_touch` |
| Pledge D1 | ≥50% of promoter holding | PLEDGE_VETO_PCT=50.0 | `d1_pledge_level` |
| First-time pledge D2 | 0.0% × 8 trailing quarters → >0, min 4 | D2_LOOKBACK_QUARTERS=8, D2_MIN_QUARTERS=4 | `d2_first_time_pledge` |
| Altman Z'' D3 | 6.56/3.26/6.72/1.05, no +3.25; veto <1.1; grey 1.1–2.6 passes | Z_COEF=(6.56, 3.26, 6.72, 1.05), Z_VETO_BELOW=1.1, Z_GREY_TOP=2.6 | `d3_altman` |
| Piotroski F D4 | veto ≤ 2 | PIOTROSKI_VETO_AT_OR_BELOW=2 | `d4_piotroski` |
| Crash veto D5 | ≥60% drawdown from trailing-52w high | CRASH_VETO_DRAWDOWN=0.6 (52w window; <52w use max available; <26w UNCOMPUTABLE) | `d5_crash` |
| CAMEL D6 | bands per §3; total ≤4; floors GNPA>12 / CAR<9 | CAMEL_VETO_AT_OR_BELOW=4, GNPA floor 12.0, CAR floor 9.0, `CAMEL_BANDS` | `d6_camel` |
| Usability U3 | ±15%; median results-week..+21d; >10% jump skip | U3_TOLERANCE=0.15, U3_MEDIAN_WINDOW_DAYS=21, U3_JUMP_SKIP=0.1 | `u3_check_a_prime` |
| Event window §5.3 | trailing 12 months | EVENT_WINDOW_MONTHS=12 | `entry_veto` |
| Cooling-off §5.3 | 12m + 1 audited print (results date AND FY-end strictly post-event) | COOLING_OFF_MONTHS=12, COOLING_OFF_PRINTS=1, 2-of-3 search | `cooling_off`, `validate_search_log` |
| Exit slippage §5.4 | 0.99 | EXIT_SLIPPAGE=0.99 | `exit_scan`, `run.leg_outcome` |
| Delisting staleness §5.4 | last print >20 trading days before event ⇒ UNEXECUTED | DELIST_STALE_TRADING_DAYS=20 | `exit_scan` |
| Fill-plausibility §8.2 | P_d0 ≤ 2.0 × P_G1 | FILL_PLAUSIBILITY_MULT=2.0 | `anchor.fill_plausible` (certification helper) |
| Decisional test set §8.2 | 5 certified; decisional ≥3; void rules | DECISIONAL_SET_SIZE=5, DECISIONAL_MIN=3 | `aggregate.bar` |
| Aggregation | leg-weighted means, price return only | AGGREGATION='leg-weighted means, price return only' | `aggregate.aggregates` |
| Zero-overlap §8.3 | vs 5 prior sets (v4), vs 6 (iterations) | 5 / 6 (constants only; the check script is validation/v4_oos, out of scope here) | constant asserted |

`tests/test_constants.py` asserts every row three ways: the literal, the *behaviour* of the code that is
supposed to use it (a copied-but-unused constant fails), and coverage (the test parses §11 from the spec file and
fails if a row is added or renamed). I also mutation-checked it: 46 single-constant perturbations, all caught.

## §12 open items — how each was carried (none resolved)

The spec's lettered cross-references (§12-A … §12-R) do not match the numbered §12 list; I read the letter as
its alphabet position (A=1 … R=18), which is consistent everywhere they appear. (The spec's `§2.7` citation in §0 was corrected to §2.6 by amendment 4.)

| # | Item | Carried as |
|---|---|---|
| 1 | QFV dropped | No QFV code; only tiers G1/G2 exist (`constants.TIERS`) |
| 2 | No-kill iteration (§9) | Process rule, nothing to implement. The only cap override (`value_anchor(g_cap=…)`) is the reporting-only sensitivity §2.2 names; the decisional path never passes it |
| 3 | Fill-plausibility 2.0× | `FILL_PLAUSIBILITY_MULT`, `anchor.fill_plausible` |
| 4 | Attribution order | `run.ATTRIBUTION_ORDER = distress → usability → event_lane → anchor` |
| 5 | Z'' for all non-financials, 1.1, grey passes, no Ohlson | `d3_altman` |
| 6 | Piotroski ≤ 2 | `PIOTROSKI_VETO_AT_OR_BELOW = 2` |
| 7 | 8-quarter first-time-pledge lookback | `D2_LOOKBACK_QUARTERS = 8` |
| 8 | CAMEL equal 0–2 weights | `d6_camel` sums unweighted components |
| 9 | No cooling-off / re-admission for distress | distress evaluated once at d0, blocks the whole window, never re-run at fill |
| 10 | Fail-closed-0 for F_ΔLIQUID / F_ΔMARGIN | logged in `fail_closed_log` |
| 11 | Slippage 1.0% | `EXIT_SLIPPAGE = 0.99` |
| 12 | Press-only SEVERE cap | `grade_event` caps at MODERATE, tags WEAK-SOURCE; never forces exit (tested) |
| 13 | Exit on SEVERE only | `exit_scan` ignores MODERATE/WATCH |
| 14 | T7 date = agency publication date | `grade_event` uses `agency_publication_date`, ignores court stays |
| 15 | Release-skeptical cooling-off | no qualifying post-event print ⇒ block persists; search log validated and recorded |
| 16 | Premium franchises still excluded | no special path exists; nothing added |
| 17 | 15% cap binds almost universally | carried; `cap_binding` reported on every name-date |
| 18 | Financial-variant anchor | `excess_return_value` exactly as §2.4 |

## Amendment log (pre-run finalization, approved by Bablu; no v4 validation has run)

`V4_SPEC.md` was amended before merge (log also appended to the spec itself; pinned SHA-256 updated in
`tests/test_constants.py` to `c61d6646…a795ead`). Four items:

1. **§5.2** — three formerly ungraded sub-cases are MODERATE: T1 order that is neither a fraud/cheating/misstatement finding nor a trading/registrant ban; T2 resignation with other stated reasons (no CARO fraud flag); T5 named FIR alone. `events.GRADES` updated.
2. **§5.1 T6** — underlying MODERATE downgraded one grade ⇒ WATCH (log only, no veto); underlying WATCH stays WATCH. The §5.2 MODERATE entry is narrowed to "T6 contagion (SEVERE underlying, downgraded)" so the two sections agree. The T6 case is removed from the gap list.
3. **§3 D3** — X1's CA/CL split comes from the AR PDF (D4's F_ΔLIQUID precedent); AR unretrievable ⇒ UNCOMPUTABLE-DATA veto. No code change (already behaved this way); now tested explicitly.
4. **§0** — "§2.7" → "§2.6".

Consequence: `SpecGapError` and the gap machinery are removed; every §5.1 sub-case is graded, so the engine no longer raises on any closed-list event. Tests: 135 → **137** (removed the two "gap raises" tests, added amendment tests for the three newly graded sub-cases, T6→WATCH, and D3 AR-unretrievable).

## Spec silences / readings (every one is tagged `SPEC-SILENT` in the code; please confirm or veto)

- **Scoring FY vs d0 (§3 PIT vintage).** The literal rule — latest FY published ≥63 days before d0 — means a 31-March d0 scores on the *previous* FY (e.g. d0 = 2019-03-31 ⇒ FY Mar-2018). The v3.x runners scored the FY ending *at* d0. The engine follows §3 literally (`pit.select_scoring_fy`); each FY record needs `results_published`. U3's window is [Mar 31, Aug 31] of the scoring FY's year.
- **Event lane vs §7 "blocked by the union" vs "C8 retired".** Read as: the lane is evaluated at d0 (reported) and at each fill date (this is what blocks a fill); a scoring-date veto does not block the whole 24m window. The lane's trace column is STOP if the veto is active at d0 *or* blocked a tier's fill.
- **T2 "unpaid fees"** is SEVERE in §5.1 but absent from the §5.2 SEVERE list; carried as SEVERE per §5.1 (an omission, not a contradiction). Not part of the approved amendment, so still flagged.
- **Blocked first touch is not retried** (carried from the v3 runner's `simulate_fills`).
- **D3 CA/CL** now documented in the spec as AR-sourced (amendment 3). Practical note for Prompt B: every non-financial name whose AR can't be retrieved is VETOED-DATA on D3, by design.
- **D3 EBIT = PBT + Interest + Depreciation** is implemented *as written*; that is EBITDA-like, not EBIT.
- **D2**: "8 trailing quarters … AND scoring quarter > 0" is unsatisfiable if the 8 include the scoring quarter, so the 8 are the quarters *before* it.
- **D7/label**: if a rule trips and another is uncomputable, the tripped rule owns the label (`VETOED-DISTRESS:<rule>`); the data defect is still logged.
- **D4 missing fields**: F_ROA's beginning total assets and F_EQ's prior capital (not Δ-terms) missing ⇒ UNCOMPUTABLE (§3 general rule); equity capital increased with bonus/split provenance unknown ⇒ UNCOMPUTABLE.
- **(a′) decisional count** headlines VETOED-DISTRESS only; VETOED-DATA vetoes are reported separately (`decisional_incl_data_vetoes`).
- **Leg (c)** "clearly positive" has no numeric definition and §9 forbids redefining it: the mean is reported, `pass` is `None`.
- **U3**: ">10% jump" read as absolute relative change; "trailing 12 months" read as (E−12m, E].
- **Exit scan**: w_i are the frozen series' own weekly dates; exit price = close at w_i; UNEXECUTED is `fired: true` with null exit date/price and `mark_price`; trading days = Mon–Fri (no calendar in the free-input list).
- **Financial variant** does not apply the `w ≤ TG+0.5pp` guard (stated under §2.1 only). The v3.11 share-count integrity guard is not carried (not in §2/§11).
- **Carried silent defaults** (v3.10/3.11 verbatim, worth a look): OPM = 0.15 and dep = 0.03 when a whole trailing series is absent; missing investments/borrowings → 0 in net cash; blank payout → 0 (C2).
- **Sector β** is an input (the pre-reg freezes it per name); no β table is shipped.

## Not in this PR (out of scope for this prompt)

Data fetchers, `validation/v4_oos/` (pre-reg, disjointness script, locked runner) and any run on real data. `check_disjoint_v4.py` and the pre-registered set are Prompt-B work.

## Audit checklist

- [x] Frozen trees untouched: `git diff origin/main -- engine specs validation` is empty (`cross_engine/` does not exist in this repo).
- [x] No prior validation set re-run. `tests/test_anchor.py::CarriedParity` imports `validation/v3_11_oos/run_v311_validation.py` read-only and compares its g_sus/margin/dep functions on *synthetic* tables; it calls no `main()` and reads no data.
- [x] Check (b) and the financial exemption are not implemented (`test_no_check_b_and_no_financial_exemption_exist`).
- [x] No early-return between gates (`ParallelGates` tests); `exit_scan` present on every filled leg; in-window exit never un-fails a blow-up fill.
- [x] 137 tests, all passing; stdlib `unittest` only.
