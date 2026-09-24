# v3 bundle audit — 2026-09-23 (Musey)

Source: Claude project `engine_v3_bundle.zip` → `engine_v3/` (8 files).
Spec: `~/workspace/stock-judging/EQUITY_REVIEW_V3_SPEC.md` (approved).

## Verdict: PASS — matches spec, safe to calibrate

- 59/59 unit tests pass — independently re-ran here (`python3 -m unittest`), all OK.
- Locked constants verified in code: Rf 6.95%, ERP 4.0% (r_val = 6.95% + β×4%), hurdle 15%, terminal g cap 4% / default 4%.
- V-8 trigger rule enforced: INVEST AT TRIGGER requires defensible trigger; non-positive triggers refuse.
- Bank/NBFC crash fixed: financial 8-check forensic variant exists, `test_financial_variant_runs` passes.
- G1 gate matches spec §6: pass iff verified ≥ 7 (6 financial) AND pass rate ≥ 60%; coverage cap at WATCH otherwise; hard FAIL only if mathematically un-clearable.
- Tier table matches spec §2: tiers key off Q + gates; P@trigger/P@today reported, P doesn't move tier (gap-1 call stands).
- Worked example: spec mini-example test passes (trigger ≈ 63.6 at FV 100, 11% val rate).

## Notes
- Bundle does NOT include `calibration_set_v3_proposed.md` (separate Claude output) — get it before calibration.
- Engine flags US-variant constants for Bablu's review (spec §11) — India path unaffected.
- v2 archived as `engine_v2.py` in bundle; live skill still runs v2 until calibration passes (locked rule).
