# Validation history

Historical record of the v3 calibration / validation work. Read-only reference
for validation sessions. Do not modify — new validation rounds write new
dated files alongside, never edit these.

## v3_6/ — widened validation (2026-09-23, FAILED the live bar)

- `calibration_report_v3_6_validation.md` — full report: 0 blow-ups (weakened
  by data attrition), 1 winner name via DCF (bar needs ≥3), anchor-only
  to-T 0.89× (FAIL), 24m 0.95× anchor-only (PASS).
- `calib_v36.py` — the calibration harness (no lookahead; verdicts replicated
  independently).
- `usability_v36.json` — per-name-date usability verdicts under the v3.6 test.
- `pe_series/` — vendor P/E series per name used by the usability test.
- `AUDIT_V36.md` — independent audit: PASS with caveats (truncated 24m
  outcomes, price-basis anomalies, usability code not in bundle).
- `EPS_FORENSICS_20260923.md` — Brightcom FY20 = vendor data error (correctly
  excluded); Persistent FY21 = NO data error (TTM-vs-FY timing + constant
  2.09× share-count basis; the test excluded the best winner over legitimate
  growth).

Structural finding: Q ≥ 7 anchor is anti-selective (4/10 winner name-dates
vs 8/12 mediocrities). Retired in v3.7.

## v3_7/ — usability fix + frozen set (2026-09-23)

- `V3_7_USABILITY_RERUN_20260923.md` — the v3.7 usability rerun: check (a)
  moved to FY results week (TTM==FY by construction), split/bonus/share-count
  basis normalized first, ±15% tolerance kept, check (b) 8% step rule kept.
  Result: **26/50 usable** (v3.6: 25/50). Persistent 2021 re-admitted (required);
  M&M 2016 re-admitted (bonus normalization); Tata Elxsi 2019 dropped out
  (v3.6 pass was TTM-drift false positive); Brightcom 2020 stays excluded
  (vendor error). **This 26-name set is FROZEN.**
- `corrected_verdicts_final.json`, `recomputed_fills.json` — DCF revalidation
  groundwork on the frozen set.

## v3_7/CONVENTIONS.md + INSAMPLE_SANITY — conformance + machinery check (2026-09-24)

- `v3_7/CONVENTIONS.md` — resolves 4 open usability conventions (ESOP/share-
  count residual, off-FY scoring dates, check(b) certification window,
  same-basis/timing algorithm) left implicit by the v3.7 rerun. Conforms;
  no method change.
- `v3_7/INSAMPLE_SANITY_20260924.md` — independently recomputes DCF-only
  fills on the frozen 26 from real price data + disclosed trigger prices.
  Sanity check only, not a live-bar substitute.

## v3_8_oos/ — THE live-bar test (2026-09-24, FAILED)

- `v3_8_oos/OOS_SET_PREREG.md` — 25 name-dates, 13 NEW companies (zero
  overlap with the in-sample 25), frozen and committed before any OOS data
  was gathered.
- `v3_8_oos/V3_8_LIVE_BAR_RESULT_20260924.md` — the result: **FAIL.**
  20/25 usable. DCF-only entry fired on 3 blow-up name-dates (need 0,
  hard bar) and reached only 2 distinct winner names (need ≥3). v3 stays
  **NOT LIVE.** Per `V3_7_DELTA.md` §5 this returns to the spec document,
  not the parameter grid — no refit performed.
- `v3_8_oos/run_oos_validation.py`, `fetch_full_financials.py` — the
  computation (usability test + DCF construction + fill replay), real
  data throughout (`pe_series/`, `eps_series/`, `sourced_eps/`,
  `corp_actions/`, `full_financials_raw.json`, `top_ratios.json`).

## Live bar (unchanged, now resolved — see v3_8_oos/ above)

v3 goes LIVE only when, on a genuinely out-of-sample set, run ONCE with no
refit: 0 blow-ups, ≥3 winner names, to-T positive, 24m ≥0.8×.

The 26-name frozen set is in-sample (seen during v3.2/v3.6 development). The
live-bar test had to be a THIRD, freshly assembled, pre-registered set of
new name-dates — that is `v3_8_oos/`, and it failed.
