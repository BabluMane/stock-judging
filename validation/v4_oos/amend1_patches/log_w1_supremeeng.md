# W1 log — Supreme Engineering (supremeeng_2020-03-31, supremeeng_2021-03-31)
Worker: W1 | Date: 2026-10-01 | Brief: v4 Phase-D Amendment-1 data-completion. Input JSONs NOT edited; engine NOT run.

## 1. FY19 CA/CL (scoring FY for d0=2020-03-31) — PATCHED, verified
- Source: FY19 audited STANDALONE balance sheet as at 31-Mar-2019, Annual Report 2018-19, p.52. Company has no consolidated results (standalone-only, per R3 dossier).
- URL: `https://nsearchives.nseindia.com/annual_reports/SME_AR_15709_SUPREMEENG_2018_2019_04092019103810_04092019110003.zip` (NSE annual-reports archive). Download recipe (from PBM sibling lesson): plain curl got empty replies; worked with browser UA + `Referer: https://www.nseindia.com/`.
- Raw: Current assets Rs 1,61,10,08,836; Current liabilities Rs 1,21,84,09,306 -> **CA=161.10, CL=121.84 (Rs.cr)**.
- Sanity vs input JSON: share capital Rs 24,99,50,000 = 24.995cr ~ input equity_capital 25.0 PASS; balance-sheet total Rs 1,91,58,09,031 = 191.58cr = input total_assets 191.58 EXACT PASS.
- Audit: R.T. Jain & Co (FRN 103961W), report signed 29-May-2019; opinion heading "Opinion" = unmodified (SWSOLAR lesson: read the heading, not inner sentences). AR filed 04-Sep-2019 < d0. 63-day rule satisfied.
- Independent corroboration: Brickwork Ratings rationale BWR/NCD/HO/CRC/0340/19-20 (01-Jul-2019): FY19 current ratio 1.32x = 161.10/121.84 = 1.322 exact; total debt 88.32cr = AR ST borrowings 72.15 + LT 16.17 exact. Aggregators (AlphaSpread/Marketcap): FY19 total CA ~Rs 1.6B = ~160cr consistent.
- FY19 AR does NOT exist on NSE's new annual-reports API (lists only 2020-21+); the SME_AR ZIP was the route. FY20 AR (company site) contains FY19 comparatives confirming these figures.

## 2. FY20 CA/CL (scoring FY for d0=2021-03-31) — PATCHED, with basis-caveat flag
- Source: FY20 audited standalone balance sheet as at 31-Mar-2020, Annual Report 2019-20 (78 pages).
- URL: `https://supremesteels.com/investors/annual_reports/annual_report_2019-2020.pdf` (company site investors page; flipbook shortcode source). Site serves 403/empty-reply to plain curl intermittently; worked with browser UA + Referer, retrying. PDF created 28-Nov-2020 -> before d0=2021-03-31. PIT OK.
- Raw: Current assets Rs 2,04,35,58,199; Current liabilities Rs 1,60,03,16,507 -> **CA=204.36, CL=160.03 (Rs.cr)**.
- Sanity vs input JSON: equity capital 24.995cr ~ 25.0 PASS. total_assets: AR 233.18cr vs input 230.53cr -> DIVERGES by 2.65cr (~1.15%). Screener-truncation basis gap (not a wrong AR): screener prints non-current investments 0.01 / reserves 25.68; audited AR shows investments Rs 7.20cr / reserves Rs 28.72cr. Same AR's FY20 comparative column confirms the FY19 figures (191.58cr). FLAGGED in patch as parent adjudication (varroc-style): the engine will mix AR-basis CA/CL with input-basis total_assets in Z''.
- Audit: R.T. Jain & Co; opinion heading "Opinion" = unmodified; consistent with dossier (Reg 33(3)(d) unmodified-opinion declaration filed with annual results 05-Aug-2020).
- Independent corroboration: BWR rationale 20-Nov-2020: FY20 current ratio 1.28x = 204.36/160.03 = 1.277 exact; total debt 87.46cr = AR ST 70.70 + LT 16.75 = 87.45 exact. Aggregators: FY20 total CA ~Rs 2.0B = ~200cr consistent.
- Failed routes before finding it: NSE announcements API Aug-2020..Aug-2021 has no "Annual Report" desc for this symbol; NSE annual-reports API lists only FY2020-21+; tickertape shows FY2020 AR as "Pending"; screener annual-reports section lists FY2021+ only; supremesteels.com homepage has no direct AR link (investors page does).

## 3. Pledge series — PATCHED (5 quarters for 2020-03-31; 8 quarters for 2021-03-31)
- Source class: company-filed Reg-31/31b SHP PDFs hosted on supremesteels.com/quarterly-half-yearly-compliances/ (tier-1 = company site; each PDF is the filed Reg-31 SHP). NSE announcements API indexes NO Reg-31 SHP for this symbol in any window (verified Sep-2018..Aug-2021); BSE api.bseindia.com is Akamai-403 from this environment even with session cookies.
- Basis: every pledged_% is SHP column XIII(b) "As a % of total Shares held" = % of PROMOTER holding -> basis="promoter".
- Per-quarter evidence:
  - 2018-09-30: shareholding_pattern.pdf ("Quarter ending 29-09-2018"), declaration Q5 "No" -> **pledged 0.0 (filed zero, PBM-lesson treatment)**, promoter 17,672,000 sh / 70.7021%.
  - 2018-12-31: shareholding_pattern_2.pdf, promoter 17,672,000 / 70.7021%; pledged 1,900,000 / **10.7514%** (banked 10.75), all by Sanjay Chowdhri (28.5307% of his 6,659,500 sh).
  - 2019-03-31: shp_as_on_31st_march_2019.pdf, Q5 Yes; promoter 17,672,000 / 70.70%; pledged 1,900,000 / **10.75**.
  - 2019-09-30: shp_as_on_30th_september_2019.pdf; promoter 17,672,000 / 70.7%; pledged 1,900,000 / **10.75**.
  - 2019-12-31: shp_as_on_31st_december_2019.pdf; promoter 17,672,000 / 70.7%; pledged 1,900,000 / **10.75**. -> D1 scoring quarter for d0=2020-03-31 (Mar-2020 SHP unpublished at d0 per pledge-PIT rule).
  - 2020-03-31: shp_as_on_31st_march_2020.pdf (PDF generated 22-Jul-2020; text layer garbled by custom font encoding - verified by rendering Table II to image and reading the Sub-Total (A)(1) row); promoter 17,672,000 / 70.7%; pledged 1,900,000 / **10.75**. Corroborated by NSE-archived SAST disclosures filed 24/26-Jun-2020: Reg-31(4) encumbrance declaration (no new encumbrances during FY20; encumbered 1,900,000 sh) + Reg-30(1)/(2) annual disclosure (promoter+PAC 17,672,000 sh = 70.70%). Included in 2021-03-31 patch (PIT-valid), excluded from 2020-03-31 patch (pledge-PIT rule).
  - 2020-09-30: shp_as_on_30th_september_2020.pdf; promoter 17,072,000 / **68.30%**; pledged 1,900,000 / **11.13%** (600,000 promoter shares sold vs Mar-2020).
  - 2020-12-31: shp_as_on_31st_december_2020.pdf; promoter 17,072,000 / **68.30%**; pledged 1,900,000 / **11.13%**. -> D1 scoring quarter for d0=2021-03-31 (Mar-2021 SHP unpublished at d0 per pledge-PIT rule).
  - 2021-03-31: shp_as_on_31st_march_2021.pdf; promoter 16,993,477 / 67.99%; pledged 1,900,000 / 11.18%. Banked NOWHERE (PIT-excluded from both patches); available if parent wants it.
- Cross-checks (non-tier-1): trendlyne per-quarter pages show 10.75% of promoter holding (1.9M/17.672M) constant Dec-2018..Jun-2020, promoter 70.70% - agrees with banked values; screener promoter series (Mar-19 70.70, Mar-20 70.70, Mar-21 67.99) agrees.
- Note: pledged share COUNT is constant 1,900,000 (Sanjay Chowdhri) from Dec-2018 onward; the % drift 10.75 -> 11.13 is promoter-sale dilution, not new pledging.

## 4. Named gaps (reasons + what was tried)
- Pledge 2018-03-31, 2018-06-30: STRUCTURAL - listed 06-Sep-2018 (NSE SME); no Reg-31 SHP filings exist. Same construction as the varroc D2 lesson.
- Pledge 2019-06-30: company site hosts 10 SHP files (Sep-18, Dec-18, Mar-19, Sep-19, Dec-19, Mar-20, Sep-20, Dec-20, Mar-21, Jun-21) - no Jun-19 or Jun-20; NSE announcements API has no SHP category for this symbol; BSE API Akamai-blocked. OMITTED, never interpolated. Corroboration: Reg-31(4) disclosure declares no new encumbrances during FY20 (covers Jun-19); screener promoter % flat 70.70 at both Mar-19 and Mar-20.
- Pledge 2020-06-30: same as Jun-19. OMITTED.
- FY20 total_assets basis gap: AR 233.18 vs input 230.53 (screener truncation). Flagged for parent adjudication; CA/CL doubly confirmed by independent sources.

## 5. Decisional expectation
- supremeeng_2020-03-31: D3 computable; D1 reads filed 10.75% at scoring quarter 2019-12-31; D2 has exactly 4 priors -> computable. Data legs no longer the binding constraint; firing is the engine's verdict.
- supremeeng_2021-03-31: D3 computable; D1 reads filed 11.13% at scoring quarter 2020-12-31; D2 has >=4 priors -> computable. Same caveat.
- Adjudication needed: (a) FY20 total_assets basis gap (233.18 vs 230.53) - accept patch as-is or adjust; (b) nothing on pledge PIT - both lists already PIT-filtered per the pledge-PIT rule (Mar-YYYY quarters excluded at their own d0).
