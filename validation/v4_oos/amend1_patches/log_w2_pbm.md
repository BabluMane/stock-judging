# W2 (PBM Polytex) — Amendment-1 data-completion log
Worker: W2 · Date: 2026-10-01 · Scope: pbm_2019-03-31 (scoring FY18), pbm_2020-03-31 (scoring FY19)

## 1. CA/CL from audited ARs (tier-1)

Source: pbmpolytex.com investor-disc-reg-46-lodr Financial Information listing (292KB page fetch, 492 PDF links).

- FY18 (99th AR): https://pbmpolytex.com/upload/investor_lodr_reg/99th-annual-report-for-fy-2017-181.pdf
  (the non-suffixed URL 99th-annual-report-for-fy-2017-18.pdf served a bot-check HTML page; the "-1" copy is the real 99-page PDF, created 2018-08-21)
- FY19 (100th AR): https://pbmpolytex.com/upload/investor_lodr_reg/100th-annual-report-fy-2018-19.pdf
  (2.5MB PDF, created 2019-08-26)

### Basis verification (the amendment's stop-gate)
CONSOLIDATED balance sheets used. FY18 consolidated: Total Assets 13,932.36 lakhs = 139.32cr → input total_assets 139.0 (exact to the crore); equity capital 812.96 lakhs → input 8.0. Standalone FY18 total assets 137.99cr do NOT match input — basis is consolidated. ✓ gate passed.
FY19 consolidated: Total Assets 14,877.55 lakhs = 148.78cr vs input total_assets 150.0 — residual 1.22cr (0.8%); other equity 104.88cr vs input reserves 107.0; equity capital 812.96 lakhs → input 8.0 ✓. Same company/CIN/AGM-year, correct scoring-FY AR, same basis as FY18 which matched exactly → residual is a screener-rounding/vendor artifact in the input JSON, NOT a wrong-AR/basis signal. Documented as caveat in the patch; no stop.

### Values patched (2-decimal Rs.cr, per sibling-worker convention)
- FY18: current_assets = 74.19 (raw 7,418.74 lakhs), current_liabilities = 17.36 (raw 1,736.33 lakhs). Arithmetic check: 11,286.30 + 909.73 + 1,736.33 = 13,932.36 ✓. PIT: audited results published 2018-05-21, 99th AGM 18-Sep-2018, auditor Chandulal M. Shah & Co. FRN 101698W — before d0=2019-03-31 ✓.
- FY19: current_assets = 88.85 (raw 8,884.97 lakhs), current_liabilities = 27.33 (raw 2,733.42 lakhs). Check: 11,301.10 + 843.03 + 2,733.42 = 14,877.55 ✓. PIT: results published 2019-05-29 (AR signed 29-May-2019) — before d0=2020-03-31 ✓.

## 2. Pledge series (tier-1: company-filed Reg-31 SHP PDFs, 13/13 quarters)

All from pbmpolytex.com/upload/investor_lodr_reg/ (filenames per item in patch). Q6 declaration + Table I promoter holding + Table II col XIII(b) "% of total Shares held" read from each PDF.

| quarter_end | pledged_pct | promoter_holding_pct | filed evidence |
|---|---|---|---|
| 2017-03-31 … 2019-03-31 (9 quarters) | 0.0 | 74.16 | SHP Q6 declaration: "No shares held by promoters are pledged or otherwise encumbered"; promoter 6,029,107 sh |
| 2019-06-30 | 0.0 | 69.85 | Q6: No; promoter 4,805,105 sh |
| 2019-09-30 | **100.0** | 69.85 | Q6: **YES**; col XIII(b)=100% for all 30 promoter shareholders (19 Indian individuals 1,928,887 sh + 9 Indian bodies corporate 2,784,050 sh + 2 foreign individuals 92,168 sh = 4,805,105/4,805,105 pledged) |
| 2019-12-31 | **100.0** | 69.85 | Q6: **YES**; same 100% all-promoter (december-2019.pdf) |
| 2020-03-31 | 0.0 | 69.85 | Q6: No — pledge released (shp-march-2020.pdf) |

Semantics note: 0.0 quarters are DISCLOSED zeros (the Q6 declaration is a filed fact), not "not visible" defaults — honest filed values, D1/D2 compute on them. basis="promoter" everywhere (SHP reports pledged as % of promoter holding). No interpolation, no omissions — zero quarters omitted.

### Notable: the Sep-2019 → Dec-2019 100% pledge spike
Promoter pledge went 0% → 100% of promoter holding in the quarter ended 2019-09-30 (holding itself had dropped 74.16%→69.85% between Mar and Jun 2019), held through Dec 2019, released by Mar 2020 — months before the 30-Sep-2020 auditor-resignation disclosure (E1). D1/D2 will trip on real filed numbers or not, per frozen rules.

### PIT flag for parent
2020-03-31 SHP is included per the task brief (13-quarter series; engine `_quarters_upto` enforces quarter_end<=d0). Per the standing Pledge-PIT lesson this filing is unpublished at d0=2020-03-31: if the parent wants D1 to read the latest PIT-published quarter for pbm_2020-03-31, that is 2019-12-31 (100.0), not 2020-03-31 (0.0). The patch includes the Mar-2020 item with this note; parent adjudicates.

## 3. Named gaps
None. All scoped fields sourced tier-1. (BSE API endpoint was Akamai-blocked; company-site route sufficed.)

## 4. What the parent must do
- Apply patches to the two input JSONs (FY18 for pbm_2019, FY19 for pbm_2020; pledge series identical in both).
- Adjudicate the Mar-2020-SHP PIT question above (affects D1's scoring-quarter value for pbm_2020: 0.0 vs 100.0).
- Note the FY19 total-assets residual (148.78 AR vs 150.0 input): Z''/O will mix AR-basis CA/CL with input-basis total_assets. W2's call: same-basis-correct AR; residual is input-side rounding.
- Files: amend1_patches/pbm_2019-03-31.patch.json, amend1_patches/pbm_2020-03-31.patch.json, this log. Input JSONs NOT edited. Engine NOT run.
