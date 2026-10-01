# engine_v5 — build notes (v5 spec: V5_SPEC.md)

Implements `engine_v5/V5_SPEC.md` (frozen 2026-10-01; SHA-256 pinned per §13 in
`tests/test_constants.py`: the pin is the hash of the file with the single pin line
`^Spec-SHA-256: [0-9a-fx]{64}$` removed). Clean-room: nothing under `engine/`, `specs/`,
`validation/` was touched. **No prior validation set was run through this engine; nothing
was tuned, gridded or calibrated.** The v5 mechanism delta vs v4 is exactly §3.1 (E1–E5
earnings-quality vetoes unioned with the retained D-suite); everything else is carried frozen.

Run the tests (stdlib only, no new dependencies):

    python3 -m unittest discover -s engine_v5/tests -t .

## What is built

| Module | Spec | Notes |
|---|---|---|
| `constants.py` | §11, §1 | one definition per number; 9 new E-rule constants + zero-overlap 6/7 |
| `anchor.py` | §2 | carried frozen (2-stage fade FCFF, triggers `P_G1`/`P_G2`, financial variant, reporting-only `g_implied`) |
| `distress.py` | §3 | D1–D7 + E1–E5 (§3.1), class split, UNCOMPUTABLE ⇒ VETOED-DATA, reporting-only Beneish/RPT fields |
| `usability.py` | §4 | carried frozen |
| `events.py` | §5 | carried frozen (closed taxonomy T1–T7, SEVERE/MODERATE/WATCH, entry veto, cooling-off, exit scan) |
| `run.py` | §6, §7 | carried frozen (parallel gates, fills, mandatory `exit_scan`, shadow pass) |
| `aggregate.py` | §1, §5.5, §6, §7 | carried frozen; decisional count already keys on `VETOED-DISTRESS` — E<n> labels feed (a′) automatically |

Input is a `run.NameDate` record (FY tables, weekly adjusted closes, shareholding quarters, unlagged EPS
series, corporate actions, event tape, audited prints). The engine never fetches anything and invents no field.
New per-FY fields read by `distress.py`: `tax_expense`, `receivables`, `ppe_net`, `rpt_loans`
(assembly must reconstruct `tax_expense` as an absolute ₹cr value — screener Tax % × PBT — never the ratio;
the engine reads it as-is and has no `1−NI/PBT` path anywhere).

## §11 constants — spec value vs implemented value

| §11 constant | Spec value | Implemented value | Where it acts |
| --- | --- | --- | --- |
| Rf / ERP / TAX / TG | 6.95% / 4.0% / 25.17% / 4% | RF=0.0695, ERP=0.04, TAX=0.2517, TG=0.04 | carried |
| Anchor horizon | 20y (10y @g + 10y linear fade + terminal yr 20) | GROWTH_YEARS=10, FADE_YEARS=10, HORIZON_YEARS=20 | carried |
| Fade shape | linear to TG | FADE_SHAPE='linear' | carried |
| Margin | trailing-5y avg OPM, flat | MARGIN_WINDOW_FY=5; one `margin` used for all years | carried |
| WC / capex / netcash / shares / beta | 5% incr rev; capex≈dep; inv−borr; mcap÷price; sector β pre-run | WC_PCT=0.05; CAPEX_EQUALS_DEP=True | carried |
| g_sus family incl. C1/C2/C3 | §2.2, cap 15% | G_CAP=0.15, ROE_YEARS=3 | carried |
| k | 0.875 / 0.70 | K_G1=0.875, K_G2=0.7 | carried |
| g_implied solver bounds | [−0.50, w−0.01] | SOLVER_LO=-0.5, hi=w−0.01 | carried |
| Fill mechanics | first weekly close, 24m, 1 leg/tier | FILL_WINDOW_DAYS=730, LEGS_PER_TIER=1 | carried |
| Pledge D1 | ≥50% of promoter holding | PLEDGE_VETO_PCT=50.0 | carried |
| First-time pledge D2 | 0.0% × 8 trailing quarters → >0, min 4 | D2_LOOKBACK_QUARTERS=8, D2_MIN_QUARTERS=4 | carried |
| Altman Z'' D3 | 6.56/3.26/6.72/1.05, no +3.25; veto <1.1; grey 1.1–2.6 passes | Z_COEF=(6.56, 3.26, 6.72, 1.05), Z_VETO_BELOW=1.1, Z_GREY_TOP=2.6 | carried |
| Piotroski F D4 | veto ≤ 2 | PIOTROSKI_VETO_AT_OR_BELOW=2 | carried |
| Crash veto D5 | ≥60% drawdown from trailing-52w high | CRASH_VETO_DRAWDOWN=0.6 (52w window; <26w UNCOMPUTABLE) | carried |
| CAMEL D6 | bands per §3; total ≤4; floors GNPA>12 / CAR<9 | CAMEL_VETO_AT_OR_BELOW=4, floors 12.0/9.0, `CAMEL_BANDS` | carried |
| Sloan accruals E1 | (NI−CFO)/TA > 0.10; positive-only; scoring FY only; non-financials | SLOAN_E1_THRESHOLD=0.10, E1_POSITIVE_ONLY=True, E1_FY_WINDOW=1 | `e1_sloan` (strict >; CFO>NI never trips by construction) |
| Cash conversion E2 | CFO < 0.5×NI, 2 consecutive FYs; applied literally | E2_CFO_PCT=0.5, E2_PERSISTENCE_FY=2 | `e2_cash_conversion` (no sign special-casing, incl. NI ≤ 0) |
| Interest coverage E3 | EBIT/Interest < 1.5; EBIT = PBT+Interest (G1 literal); Interest≤0 ⇒ no trip | E3_IC_VETO_BELOW=1.5 | `e3_interest_coverage` (E3 EBIT deliberately ≠ D3's PBT+Int+Dep; §3.1/§11 carry both) |
| ETR E4 | TaxExpense/PBT < 15%, 2 consecutive FYs; tax from the tax-expense line; PBT≤0 ⇒ no trip | E4_ETR_VETO_BELOW=0.15, E4_PERSISTENCE_FY=2 | `e4_etr` (no `1−NI/PBT` path anywhere in the engine) |
| Receivables days E5 | Rec/Rev×365 > 90d OR YoY > 30%; non-financials; AR-sourced | E5_DAYS_VETO_ABOVE=90, E5_YOY_VETO_ABOVE=1.30 | `e5_receivables_days` |
| E-rule scope | non-financials only; financials N/A by construction (D6 stands) | E_SCOPE_NONFINANCIAL_ONLY=True | `distress.evaluate` (financials: E-rules N/A, `e_rules="N/A (financial variant)"`) |
| Reporting-only fields | Beneish SGI/DEPI/LVGI/TATA (frozen formulas §3.1); rpt_loans stored | formulas in `reporting_fields` (no constants to pin) | `distress.evaluate` → `reporting` dict (missing → null + logged, never a veto) |
| New v5 input fields | tax_expense, receivables, ppe_net, rpt_loans (per-FY) | read via `pit.cell` in `e4_etr`/`e5_receivables_days`/`reporting_fields` | `NameDate.fy` dicts (free-form; docstring updated) |
| Usability U3 | ±15%; median results-week..+21d; >10% jump skip | U3_TOLERANCE=0.15, U3_MEDIAN_WINDOW_DAYS=21, U3_JUMP_SKIP=0.1 | carried |
| Event window §5.3 | trailing 12 months | EVENT_WINDOW_MONTHS=12 | carried |
| Cooling-off §5.3 | 12m + 1 audited print | COOLING_OFF_MONTHS=12, COOLING_OFF_PRINTS=1, 2-of-3 search | carried |
| Exit slippage §5.4 | 0.99 | EXIT_SLIPPAGE=0.99 | carried |
| Delisting staleness §5.4 | last print >20 trading days before event ⇒ UNEXECUTED | DELIST_STALE_TRADING_DAYS=20 | carried |
| Fill-plausibility §8.2 | P_d0 ≤ 2.0 × P_G1 | FILL_PLAUSIBILITY_MULT=2.0 | carried |
| Decisional test set §8.2 | 5 certified; decisional ≥3; void rules | DECISIONAL_SET_SIZE=5, DECISIONAL_MIN=3 | carried |
| Aggregation | leg-weighted means, price return only | AGGREGATION='leg-weighted means, price return only' | carried |
| Zero-overlap §8.3 | vs 6 prior sets (v5); vs 7 (iterations) | ZERO_OVERLAP_PRIOR_SETS_V5=6, ZERO_OVERLAP_PRIOR_SETS_ITERATIONS=7 | constant asserted (the check script is validation/v5_oos, out of scope here) |

`tests/test_constants.py` asserts every row three ways: the literal, the *behaviour* of the code that is
supposed to use it (a copied-but-unused constant fails), and coverage (the test parses §11 from the spec file
and fails if a row is added or renamed; the spec's `**bold**` markup on the new rows is stripped in the parse).
Note: the v4 mutation check (46 perturbations) was not re-run for v5; the new constants each carry a
literal + behavior + boundary test in `test_constants.py`/`test_distress.py` instead.

## §12 open items — how each was carried (none resolved)

Carried from the v4 build verbatim (the §12 list is unchanged between specs): QFV dropped; no-kill
iteration is process-only; fill-plausibility 2.0×; attribution order distress → usability → event lane →
anchor; Z''/Piotroski/crash/CAMEL rules; no distress re-admission; fail-closed-0 for F_ΔLIQUID/F_ΔMARGIN;
slippage; press-only SEVERE cap; exit on SEVERE only; T7 date = agency publication date;
release-skeptical cooling-off; no special path for premium franchises; 15% cap binds; financial-variant anchor.

## Amendment log

Empty. The v5 spec has no amendment log yet (`events.py` §5.1 comment cites the carried v4 amendment text in
V5_SPEC.md §5.1/§5.6 instead of the v4 amendment log).

## Spec silences / readings (every one is tagged `SPEC-SILENT` in the code; please confirm or veto)

Carried from v4: scoring-FY PIT reading; event lane at d0 vs fill dates; blocked first touch not retried;
D3 CA/CL AR-sourced; D3 EBIT = PBT+Interest+Depreciation as written; D2 8 quarters exclude the scoring
quarter; D7 trip-outranks-data; D4 missing-field conventions; (a′) headlines VETOED-DISTRESS only;
leg (c) unjudged; U3 >10% absolute jump; exit-scan weekly dates; financial variant skips the w ≤ TG+0.5pp
guard; carried silent defaults (OPM 0.15, dep 0.03, blank payout → 0); sector β is an input.

New for v5 (§3.1 guards):
- **E3/E4 denominator guards:** E3 `Interest_t ≤ 0` ⇒ no trip (PASS, logged) — not a data defect;
  E4 either year's `PBT ≤ 0` ⇒ the rule does not trip for that pair (PASS, logged) — not UNCOMPUTABLE.
- **E4 missing-ness split:** missing `tax_expense` (or PBT) ⇒ UNCOMPUTABLE-DATA ⇒ VETOED-DATA; a
  present-but-nonpositive PBT ⇒ non-trip. The asymmetry is per the spec's deliberate resolutions.
- **E5 YoY leg:** `receivables_{t−1}` missing or ≤ 0 ⇒ UNCOMPUTABLE (fail-closed — no meaningful YoY
  multiple); `sales_t` missing ⇒ UNCOMPUTABLE; `sales_t ≤ 0` ⇒ UNCOMPUTABLE.
- **E2 literalism:** `CFO < 0.5×NI` applied with no sign special-casing, even when NI ≤ 0 (G1 wording exact).
- **E1 positive-only:** encoded by the strict `> 0.10` — CFO > NI can never produce a trip.
- **tax_expense reconstruction** (Tax % × PBT) is assembly's job; the engine reads the absolute ₹cr
  field as-is and contains no `1−NI/PBT` construction anywhere (the PBM-FY18 trap is tested in
  `test_distress.E1E5`).
- **Evaluation order D7:** `D1 → D2 → E1 → E2 → E3 → E4 → E5 → D3/D6 → D4 → D5`; first tripped rule owns
  `VETOED-DISTRESS:<rule>`. E-rule labels feed `aggregate.decisional_count` (tested in test_run).
- **S11 coverage test** strips the spec's bold markup (`**…**`) from parsed first-column text so the
  v5 §11 rows match their labels.

## Not in this PR (out of scope for this prompt)

Data fetchers, `validation/v5_oos/` (pre-reg, disjointness script, locked runner) and any run on real data.
`engine_v4/` and `validation/v4_oos/` were not touched (read-only). Nothing committed.

## Audit checklist

- [x] Frozen trees untouched: `engine_v4/` and `validation/v4_oos/` read-only (imports in tests repointed to `engine_v5`; no v4 file edited).
- [x] `aggregate.py` verified: decisional count already keys on `distress_decisional` (bool of `dis["tripped"]`), so `VETOED-DISTRESS:E<n>` labels feed leg (a′) with no code change; explicit test added (`test_e_rule_veto_counts_as_decisional_for_leg_a_prime`).
- [x] Two EBIT definitions coexist (D3: PBT+Interest+Depreciation; E3: PBT+Interest) — deliberate, documented, tested.
- [x] E-rule behavior boundaries tested: E1 0.10 strict / CFO>NI non-trip / TA≤0 uncomputable; E2 2-yr / literal / missing; E3 1.5 strict / interest≤0 guard / negative PBT; E4 15%×2yr / PBT≤0 non-trip / missing tax_expense uncomputable / PBM-FY18 trap; E5 90d / 1.30 YoY / missing receivables / sales≤0; financial N/A.
- [x] Reporting fields (SGI/DEPI/LVGI/TATA/rpt_loans) stored on the name-date result, never veto; missing → null + logged.
- [x] 160 tests, all passing; stdlib `unittest` only.
