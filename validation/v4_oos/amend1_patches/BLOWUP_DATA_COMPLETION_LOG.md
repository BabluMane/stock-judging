# Amendment-1 blow-up data completion log (coordinator merge, 2026-10-01)

Governing doc: `port/validation/v4_oos/V4_OOS_PREREG_AMENDMENT_1.md`. Workers were
evidence-only: patch JSONs in this directory, input JSONs untouched, engine never run.
Full per-worker detail: `log_w1_supremeeng.md`, `log_w2_pbm.md`, `log_w3_varroc.md`.

## Patched values

| name-date | scoring FY | current_assets (cr) | current_liabilities (cr) | CA/CL source |
|---|---|---|---|---|
| supremeeng_2020-03-31 | 2019 | 161.10 | 121.84 | FY19 audited standalone B/S p.52, AR 2018-19 (NSE SME_AR ZIP 04-Sep-2019; auditor R.T. Jain & Co, report 29-May-2019, unmodified). No consolidated results exist (R3). Cross-check: BWR rationale 01-Jul-2019 current ratio 1.322 = 161.10/121.84 exact. Basis gate: AR equity 24.995cr / TA 191.58cr = input values EXACT. |
| supremeeng_2021-03-31 | 2020 | 204.36 | 160.03 | FY20 audited standalone B/S, AR 2019-20 (supremesteels.com investors page, PDF created 28-Nov-2020 < d0). Cross-check: BWR 20-Nov-2020 current ratio 1.277 = 204.36/160.03 exact. Basis gate: equity PASS (24.995~25.0); TA DIVERGES 233.18 vs input 230.53 (~1.15% screener truncation — see adjudication A3). |
| pbm_2019-03-31 | 2018 | 74.19 | 17.36 | FY18 (99th) audited consolidated B/S, pbmpolytex.com (PDF created 2018-08-21; results published 2018-05-21). Arithmetic check 11,286.30+909.73+1,736.33=13,932.36 lakhs ✓. Basis gate: AR TA 139.32cr = input 139.0 exact-to-crore (standalone 137.99 would have failed). |
| pbm_2020-03-31 | 2019 | 88.85 | 27.33 | FY19 (100th) audited consolidated B/S, pbmpolytex.com. Basis gate: TA residual 148.78 vs input 150.0 (0.8% — see adjudication A3). |
| varroc_2019-03-31 | 2018 | 3060.44 | 3173.03 | FY18 audited consolidated B/S, AR 2017-18 (Price Waterhouse, signed 2018-06-06 = input results_published). Raw 30,604.38M/31,730.31M, component-summed; cross-confirmed exact in FY19 AR comparative column. Basis gate: input is screener-truncated (equity 12 vs 13.48cr, TA 6802 vs 6852.39cr — see adjudication A3). |

## Pledge series

| name-date | quarters (PIT) | D1 scoring quarter | D1 read | D2 |
|---|---|---|---|---|
| supremeeng_2020-03-31 | 5: Sep-18 (0.0), Dec-18→Dec-19 (10.75) | Dec-2019: 10.75% | PASS (<50%) | 4 priors, not all zero → PASS |
| supremeeng_2021-03-31 | 8: Sep-18 (0.0), Dec-18→Mar-20 (10.75), Sep-20→Dec-20 (11.13) | Dec-2020: 11.13% | PASS | 8 priors, not all zero → PASS |
| pbm_2019-03-31 | 9 PIT: Mar-17→Dec-18 (all 0.0; Mar-19 excluded per A4) | Dec-2018: 0.0% | PASS | scoring 0 → PASS |
| pbm_2020-03-31 | 12 PIT: Mar-17→Jun-19 (0.0), Sep-19→Dec-19 (**100.0**); Mar-20 excluded per A4 | Dec-2019: **100.0%** | **TRIP** (pending A4) | scoring>0 but Sep-19=100 → PASS |
| varroc_2019-03-31 | 0 (gap G3) | UNCOMPUTABLE | — | N/A by construction (gap G4) |

Pledge sources: supremeeng — company-filed Reg-31 SHP PDFs on supremesteels.com
(tier-1; NSE announcements API indexes none for this SME symbol); pbm — 13/13
company-filed Reg-31 SHPs on pbmpolytex.com (tier-1; Q6 "no shares pledged" filed
zeros banked as 0.0, not gaps). PBM spike: 100% of promoter holding pledged
Sep-2019 and Dec-2019 (all 30 promoter shareholders, 4,805,105/4,805,105 shares),
back to 0.0 by Mar-2020 — months before the Sep-2020 auditor-resignation disclosure.

## Named gaps (honest, no interpolation)

- **G1** (supremeeng): quarters Mar-18, Jun-18 — structural; listed 06-Sep-2018 (NSE SME), no Reg-31 filings exist pre-listing.
- **G2** (supremeeng): Jun-19 (both name-dates) and Jun-20 (2021 name-date) — no tier-1 SHP obtainable (company site hosts 10 SHPs; NSE API indexes none; BSE API Akamai-blocked from this environment).
- **G3** (varroc): entire pledge series — tier-1 SHP unobtainable (BSE SHP fetch failed; nsearchives indexes only a 2021 file; varroc.com hosts no SHP PDFs). Tier-3 (trendlyne) + R7 dossier corroborate 0.00% — recorded as corroboration only, not banked.
- **G4** (varroc): D2 N/A by construction — listed 06-Jul-2018, max 2–3 post-listing priors < 4-prior minimum; pre-listing quarters have no filings at all.

## Coordinator adjudications

- **A1 (varroc basis caveat): ACCEPT with loud caveat.** CA/CL doubly-verified AR
  numbers; the ~50cr TA gap is vendor-side truncation, pre-existing across all
  fields; amendment scope is closed (no TA patching). Z'' will mix AR-basis CA/CL
  with input-basis TA — documented here and in the patch.
- **A2 (varroc pledge gap): ACCEPT.** D2 is N/A by construction regardless; even
  perfect pledge data (0.00%) could only make D1 PASS, never a trip — decisionality
  rides on D3 alone, and the frozen attribution gives a tripped rule ownership over
  coexisting data defects. No browser re-attempt warranted.
- **A3 (supremeeng-FY20 / pbm-FY19 TA residuals ~1%): ACCEPT with loud caveat.**
  Basis gates passed on the correct company/CIN/AGM-year/consolidated basis; residuals
  are input-side screener artifacts. Same Z'' basis-mixing note as A1.
- **A4 (Mar-quarter SHP PIT) — ESCALATED to main parent for explicit decision.**
  All 20 winner/mediocrity inputs exclude the unpublished d0-quarter SHP
  (e.g. infy_2020-03-31 ends 2019-03-31; AGENTS.md pledge-PIT lesson). The PBM patch
  as written includes Mar-2020 (and Mar-2019 for pbm_2019). Recommendation: EXCLUDE
  both d0-quarters for cross-set consistency and PIT-correctness (Mar SHP is filed in
  April, unpublished at Mar-31 d0). Impact stated plainly: exclusion makes Dec-2019
  (100.0%) the D1 scoring quarter for pbm_2020-03-31 → D1 TRIPS; inclusion makes
  Mar-2020 (0.0%) the scoring quarter → D1 PASSES. The recommendation is
  principle-based (it would hold regardless of which value helped), but the parent
  owns the call since it can move a gate.

## Decisional outlook (mechanical read, not a verdict)

D3 computable on all 5 name-dates now. Expected gate contributions: supremeeng×2 →
D3/D4/D5 (pledge PASS); pbm_2019 → D3/D4/D5; pbm_2020 → D1 TRIP (pending A4) and/or
D3/D4/D5; varroc → D3/D4/D5. Whether ≥3 trip is for the locked re-run to determine.
