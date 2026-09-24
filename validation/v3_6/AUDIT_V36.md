# Independent audit — v3.6 widened validation bundle
**Date:** 2026-09-23 · **Auditor:** Musey · **Scope:** calibration_v3_6_bundle.zip + pasted tools-and-data doc
**Method:** independent recomputation from raw files (outputs_v36.json, usability_v36.json, 24 pe_series CSVs); no re-running of calib_v36.py (inputs/ not in bundle).

## Verdict: PASS with caveats
Every headline number recomputes exactly from the raw files. No lookahead found in the scoring code. The validation failure stands as reported — the anchor is anti-selective, caught zero winners, and both pre-registered fixes failed out-of-sample without re-fitting.

## Verified claims (recomputed, all match)
- Usability: 25/50 usable; 18 basis-drift exclusions; excluded keys in outputs match usability_v36.json exactly.
- Aggregates as-judged: ALL to-T 2.70/0.96, 24m 1.32/1.02; own-multiple 0.89/0.87, 0.95/0.97; DCF-anchored 4.82/0.96, 1.77/1.36; winners 12.72 (n=1 name); mediocrities 0.88/0.87; blow-up fills 0.
- Gate M: 13→11 legs (blocks wipro_2017-03-31 only, both legs). Gate M+V: winners → 0 (blocks both Persistent legs). Matches report.
- Anti-selectivity: winners 4/10 in Q≥7 universe, mediocrities 8/12. Winner fills via own-multiple anchor: 0, both as-judged and neutral.
- Unexplained steps confirmed in series: APL +50.5% on 2017-12-15, Deepak −10.3% on 2017-06-16, Navin −13.6% on 2015-06-19.
- All four "no PIT EPS at date" verdicts replicate under the engine's own load_series (63-day lag): brightcom_2018-08-22, trent_2021-03-31, vakrangee_2013-06-03 (lag-boundary row has empty pe), manpasand_2015-07-09 (series starts 2015-07-10, a day after scoring).
- Series integrity: all 24 sorted, unique dates, max gap 19d (weekly cadence), every series' last date ≥ its T. to_T_truncated = 0 everywhere — the extension fixed the to-T truncation.
- Code review of calib_v36.py: PIT EPS uses 63-day lag; vintage pairing takes latest scoring date ≤ week (no lookahead); median_5y on lagged pe_pit; Gate M evaluated at fill date on data ≤ t. Basis rescaling (input price / series price) is coherent — fill decisions are basis-invariant, outcomes are price ratios.
- Step-2 intactness table: 13/14 fills in [0.90, 1.01), only Symphony below (0.84); Lupin 1.00 → 0.42×. Prereg params (0.875, −10%, 36m) match code constants.

## New caveats (do not overturn the verdict)
1. **3 of 13 fills still have truncated 24m outcomes**: lichf acc/inv at 22.3 months (0.974), symphony acc at 14.9 months (1.254). Excluding them: as-judged ALL 24m = 1.40/1.11 (reported 1.32/1.02); own-multiple 24m = 0.86/0.84 (reported 0.95/0.97). The ≥0.8× bar still passes either way. But under **neutral** judgement, all three own-multiple 24m observations are truncated — the reported neutral 1.07/0.97 rests entirely on 22.3m/14.9m outcomes. The report's trunc column is the to-T flag; the 24m truncation lives only in the JSON.
2. **Price-basis anomalies**: input recorded price vs series price disagree by 101.85× (bajfin_2015), 10× (bajfin_2017), ~5.4× (wipro), 5× (yesbank), 2.2× (vakrangee) — split/bonus-adjustment mismatches between the input files and the Screener series. Harmless by construction (see above), but it is the same basis-mismatch family as the EPS problem, in the price field.
3. **Usability test code not in bundle** — verdicts verified by replication and internal consistency, but the ±15%/8%-step implementation itself cannot be inspected.

## Standing recommendation (unchanged)
Retire the anchor; keep v3.2's DCF entry; fix the EPS source before any re-validation. The attrition finding (25/50 unusable, 18 on basis drift) remains the binding constraint — it weakens the "0 blow-ups" claim more than any engine change can repair.
