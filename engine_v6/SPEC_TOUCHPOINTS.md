# SPEC_TOUCHPOINTS.md — exact code touch points for W-implement (v6 build)

Spec: `engine_v6/V6_SPEC.md` (frozen; Spec-SHA-256 self-declared per §13
procedure). v5-only mechanism delta: §3.1 E6 (receivables–cash-collection
veto) replacing the retired E5. Everything else (§2 anchor, §3 D-suite and
E1–E4, §4 usability, §5 event lane, §6–§9 machinery) is carried frozen.

## New input fields (per-FY, on `run.NameDate.fy[year]` dicts)

The fy dict is free-form (`{field: value|None, results_published: date}`),
so no dataclass change is needed — but these field names must be produced by
assembly and read by `distress.py`:

| Field | Used by | Source | Notes |
|---|---|---|---|
| `tax_expense` (₹cr) | E4 | screener static P&L (Tax % row × PBT, or direct where published) | **NEW — was NOT in v4 inputs** (verified against `validation/v4_oos/phase_d_inputs/*.json` FY dicts, which have `net_profit, cfo, total_assets, pbt, interest, ...` but no tax field). G1 forbids the `1−NI/PBT` construction. |
| `receivables` (₹cr) | E6 | AR balance sheet (D4 F_ΔLIQUID precedent — one AR bundle, ≥63d PIT) | Carried from v5. Missing ⇒ UNCOMPUTABLE-DATA (non-financials). |
| `ppe_net` (₹cr) | reporting DEPI only | AR balance sheet | NEW. Missing ⇒ DEPI uncomputable → stored as null, logged (reporting-only, never a veto). |
| `rpt_loans` (₹cr) | reporting only | AR notes (RPT/subsidiary loans) | NEW. Missing ⇒ stored null, logged. |

Already-verified present in v4 inputs (no assembly change): `net_profit`,
`cfo`, `total_assets`, `pbt`, `interest`, `sales`, `borrowings`,
`current_assets`, `current_liabilities`, `depreciation`, `equity_capital`,
`reserves` — E1 (NI, CFO, TA), E2 (CFO, NI), E3 (PBT, Interest) need nothing
new. **But note:** screener publishes a Tax % row; assembly must reconstruct
`tax_expense` as an absolute ₹cr value (Tax % × PBT), not store the ratio.

## Files to change

1. **`constants.py`** — add one §11-row block per new constant (mirror the
   existing `# ---- §11 row: ... ----` comment style):
   - `SLOAN_E1_THRESHOLD = 0.10`, `E1_POSITIVE_ONLY = True`, `E1_FY_WINDOW = 1`
   - `E2_CFO_PCT = 0.5`, `E2_PERSISTENCE_FY = 2`
   - `E3_IC_VETO_BELOW = 1.5` (EBIT := PBT + Interest — **deliberately
     distinct from D3's PBT+Interest+Depreciation**; keep both, document the
     coexistence in a comment citing §3.1/§11)
   - `E4_ETR_VETO_BELOW = 0.15`, `E4_PERSISTENCE_FY = 2`
   - `E6_DAYS_VETO_ABOVE = 90` (strict >; 90d carried from E5 as a disclosed definitional constant),
   - `E6_CFO_TRIP_AT_OR_BELOW = 0` (veto iff CFO_t ≤ 0 — inclusive; CFO exactly 0 trips, literalism stated)
   - `E_SCOPE_NONFINANCIAL_ONLY = True`
   - Reporting-formula comment block for SGI/DEPI/LVGI/TATA (§11 rows added
     to the spec table — the constants test must cover the new rows).

2. **`distress.py`** — the core change:
   - New functions `e1_sloan`, `e2_cash_conversion`, `e3_interest_coverage`,
     `e4_etr`, `e6_receivables_cash_collection` returning the existing `_r(...)`
     PASS/STOP/UNCOMPUTABLE triple with `VETOED-DISTRESS:E<n>` labels.
   - Guards per §3.1: E1 `TotalAssets_t ≤ 0` ⇒ UNCOMPUTABLE; E3
     `Interest_t ≤ 0` ⇒ no trip (infinite coverage, logged); E4 either year's
     `PBT ≤ 0` ⇒ no trip for that pair (logged); E6 `Sales_t ≤ 0` ⇒
     uncomputable; `receivables_t`/`cfo_t` missing ⇒ UNCOMPUTABLE-DATA;
     any missing required field ⇒ UNCOMPUTABLE-DATA
     ⇒ VETOED-DATA (v4 convention, never silent pass).
   - E4 uses the `tax_expense` field only — assert/no-path for a
     `1−NI/PBT` construction (the PBM-FY18 trap).
   - Evaluation order: extend D7 to
     `D1 → D2 → E1 → E2 → E3 → E4 → E6 → D3/D6 → D4 → D5` — first tripped
     rule owns attribution.
   - Financial-variant class: skip E1–E6 entirely (N/A by construction);
     record `e_rules: "N/A (financial variant)"` in the trace.
   - Reporting-only: compute SGI/DEPI/LVGI/TATA per §3.1 frozen formulas and
     store on the name-date result (never veto); `rpt_loans` passthrough.

3. **`run.py`** — no dataclass change needed (fy dict is free-form), but:
   - Update the `NameDate` docstring to name the four new per-FY fields and
     their PIT requirement (receivables/tax_expense follow the same ≥63d
     vintage as every filing input).
   - Gate-trace column "distress screen" must carry E-attributions;
     `VETOED-DISTRESS:E<n>` labels must flow into `aggregate.bar`'s
     decisional count (decisional headlines VETOED-DISTRESS only — unchanged,
     now including E-rules).

4. **`aggregate.py`** — verify only: `(a′)` decisional count already keys on
   `VETOED-DISTRESS` labels; E<n> labels are included automatically if the
   prefix convention holds. Add an explicit test asserting an E1-vetoed
   name-date counts as decisional when the anchor would have filled.

5. **`tests/test_constants.py`** — W-test wiring:
   - `SPEC = os.path.join(HERE, "..", "V5_SPEC.md")`.
   - `SPEC_SHA256 = "f2eb5b5cfb3c97243e33fd5809e58b18a7033469133238274ea37aecd5f2f84d"`
     with the §13 pin procedure: read file, drop the single line matching
     `^Spec-SHA-256: [0-9a-fx]{64}$`, hash the remainder.
   - Extend `S11_ROWS` with the 9 new rows (exact first-column text from
     §11): "Sloan accruals E1", "Cash conversion E2", "Interest coverage E3",
     "ETR E4", "Receivables-cash-collection E6", "E-rule scope",
     "Reporting-only fields", "New v5 input fields", and update
     "Zero-overlap §8.3" row text (now "vs 7 prior sets (v6); vs 8
     (iterations)").
   - Add literal + behavior tests per new constant (v4 pattern: literal,
     behavior, coverage — 46-mutation-tested).
   - Update docstring + the `Run: python3 -m unittest discover -s engine_v4/tests`
     line → `engine_v5`.

6. **`tests/test_distress.py` + `tests/fixtures.py`** — fixtures for each
   E-rule trip / no-trip / guard case (E1 positive-only non-trip when CFO>NI;
   E3 Interest=0 no-trip; E4 PBT≤0 no-trip; E4 missing tax_expense ⇒
   VETOED-DATA; E6 receivables/cfo-missing ⇒ VETOED-DATA; financial-variant
   E N/A).
   Include the Phase-1 catch anchors as regression fixtures where feasible
   (supremeeng_2020 E1 +12.2%, supremeeng_2021 E3 1.49× — synthetic
   reconstructions, documented as such).

7. **`__init__.py`** — `ENGINE_VERSION = "engine v5.0"`,
   `SPEC = "V5_SPEC.md (frozen 2026-10-01)"`, module docstring → engine_v5.

8. **`events.py` line 10** — comment cites `V4_SPEC.md "Amendment log"` for
   the closed §5.1 gaps; repoint to `V5_SPEC.md §5.1/§5.6` (the v4 amendment
   text is carried into the v5 taxonomy body verbatim; no amendment log in
   v5 yet).

9. **All test files' imports** — `from engine_v4 import ...` →
   `from engine_v5 import ...` (7 files: test_anchor, test_constants,
   test_distress, test_events, test_run, test_usability, fixtures).

10. **`BUILD_NOTES.md`** — header updated to v5 (done); W-implement rewrites
    the body: §11 spec-vs-implemented table gains the 9 new rows; the
    SPEC-SILENT list gains the §3.1 guards (E3/E4 denominator guards, E4
    PBT≤0 non-trip, E6 Sales≤0 / CFO-inclusivity, tax_expense reconstruction
    method); the
    amendment log starts empty; the spec pin (`SPEC_SHA256` above) replaces
    the v4 literal.

## v4-spec cross-references to repoint (grep `V4_SPEC` / `engine_v4`)

- `__init__.py` (2 refs), `constants.py` docstring (1), `events.py` (1),
  `tests/test_constants.py` (docstring + SPEC path + run line + SPEC_SHA256).
- Docstrings in `run.py`, `aggregate.py`, `usability.py`, `pit.py` that say
  "v4" or reference "V4_SPEC §" — repoint to "V5_SPEC §".
- `BUILD_NOTES.md` body still describes the v4 build in full — W-implement
  regenerates it against V5_SPEC.md; do not leave v4 content claiming to
  describe the v5 engine.

## Deliberate spec decisions W-implement must NOT "fix"

- Two EBIT definitions coexist (D3: PBT+Interest+Depreciation frozen
  EBITDA-like; E3: PBT+Interest per G1 literal). §11 carries both. Unifying
  them is a parameter touch — forbidden.
- E2's `CFO < 0.5×NI` applied literally even when NI ≤ 0 (no sign
  special-casing — G1 wording exact).
- E4 non-trip (not UNCOMPUTABLE) when either year's PBT ≤ 0; but missing
  `tax_expense` ⇒ UNCOMPUTABLE-DATA ⇒ VETOED-DATA.
- E5's AR-sourced receivables share the ≥63d PIT vintage; AR unretrievable
  ⇒ VETOED-DATA by design (same fail-closed philosophy as D3/D4).
- The pin line (`Spec-SHA-256: ...`) is part of the file but excluded from
  the hash — never "verify" the file by hashing it whole.
