# E-rule Catch Table — v5 certified blow-ups (screener-based, pre-assembly)

Computed 2026-10-01 by the sweep coordinator via `e_rule_catch.py` (W4's tested script).
Inputs: screener.in consolidated P&L/BS/CF. tax_expense = Tax% × PBT (screener integer Tax% row).
E5 UNCOMPUTABLE for all 4 — screener BS tables do not break out receivables; needs AR bundle at assembly.

| name-date | scoring FY | E1 accruals/TA | E2 CFO<0.5NI 2yr | E3 IC | E4 ETR 2yr | E5 | VETO? |
|---|---|---|---|---|---|---|---|
| addshop_2023-03-31 | FY2022 | **TRIP** 0.196 | **TRIP** (9<9.5, 1<4) | no (24.0) | no (19%, 25%) | UNCOMP | **YES** (E1+E2) |
| whiteorganic_2023-03-31 | FY2021 | no (0.073) | **TRIP** (degen, see n.1) | no (int=0) | no (25%; t−1 PBT≤0 guard) | UNCOMP | **YES** (E2) |
| ranasug_2023-03-31 | FY2022 | no (−0.005) | no | no (4.76) | no (22%, 0%) | UNCOMP | no |
| mishtann_2024-03-31 | FY2023 | **TRIP** 0.205 | UNCOMP (n.2) | no (16.4) | UNCOMP (n.2) | UNCOMP | **YES** (E1) |

Notes:
1. White Organic E2 is a degenerate-but-literal trip: NI=0 both years, CFO=−9/−4 < 0 = 0.5×0. Spec applies literally, no sign special-casing (v5 engine-build lesson). Verdict stands; flagged for G2 adjudication.
2. Mishtann FY2022 was never published (screener jumps Mar 2018 → Mar 2023) → E2/E4/E5-yoy uncomputable from screener. **VETOED-DATA risk at assembly**: per §3.1 missing ⇒ VETOED-DATA, and VETOED-DATA vetoes are NON-decisional for bar (a′) (v4 R2 precedent: only rule-trips count). If assembly confirms FY2022 truly unpublishable, Mishtann contributes 0/1 decisional — the set then needs 3/4 decisional among the rest + the 5th blow-up. AR hunt at assembly may still recover FY2022 numbers (company published FY2023, so FY2022 comparatives exist in the FY2023 AR).
3. Rana Sugars trips nothing — the set's honest-residual candidate (spec's pbm_2019-03-31 analog). Certifiable per pre-reg ("sweep certifies a name-date no E-rule trips at scoring…").
4. E1 boundary check: Add-Shop E2 t-leg is near-boundary (9 < 9.5) — literal pass, recorded as-is.
5. All values to be re-verified from AR bundles at assembly (screener Tax% is integer-rounded; W4 recipe prefers the AR P&L tax-expense line).
