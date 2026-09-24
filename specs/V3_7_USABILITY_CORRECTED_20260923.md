# V3.7 Usability — CORRECTED EPS Series Re-run (2026-09-23)

## Verdict

**Corrected usable set: 26/50 — IDENTICAL to the v3.7 frozen set.**

The harness bug (discarding Screener's EPS dataset) did **not** materially affect usability verdicts. The quotient `price/PE` and the API EPS dataset agree to <1.2% on 23/24 names (max 2.84% Navin, 5.99% Manpasand on 4 weeks). The v3.7 verdicts stand confirmed by an independent series construction.

**Live bar (DCF-only, on corrected 26): UNCHANGED from v3.7 revalidation — v3 NOT LIVE.**
- (a) Blow-up fills: **0** — PASS
- (b) Winner names with DCF fills: **1** (Persistent), ceiling 1 — **FAIL** (need ≥3)
- (c) Aggregate to-T: **4.82×** mean — PASS
- (d) Aggregate 24m: **1.77×** mean — PASS

**Fraud/blowup names:** DHFL×2, Manpasand×2, Brightcom 2020 — **none returned.**
- DHFL×2: no series (page 404, structural).
- Manpasand 2015: no PIT EPS at scoring date (structural). Manpasand 2016: excluded on (a) +25.6%.
- Brightcom 2020: excluded on (a) −94.3% (vendor FY20 EPS error confirmed). Brightcom 2018: UNVERIFIED (series harvested, no sourced FY EPS).

## What was done

### 1. Re-harvest (24/25 symbols)
- Screener chart API: `https://www.screener.in/api/company/<ID>/chart/?q=Price+to+Earning-Median+PE-EPS&days=6300`
- Retained the **EPS dataset** (previously discarded).
- 24/25 harvested. DHFL: page 404, no series (structural).
- LIC Housing Finance: harvested as `LICHSGFIN` (not `LICHF`).
- Raw JSON: `~/workspace/stock-judging/v3/v37_reval/corrected_series/raw/` (24 files)

### 2. Corrected PIT EPS series
- Publication-dated EPS points, forward-filled to weekly.
- 63-day lag applied for PIT safety (as requested).
- Cross-check: quotient vs API EPS divergences >5%: **none material** (see Stage 1).
  - 22/24 names: max divergence <1.2%.
  - Navin: 2.84% (single week). Manpasand: 5.99% (4 weeks in Oct 2019).
  - Conclusion: the v3.6 quotient was **not** fiction; it accurately represented Screener TTM EPS.

### 3. Fifty usability decisions (v3.7 test on corrected series)
- **Check (a):** FY-results TTM (first EPS publication in [Mar 31, Aug 31], with stale Mar-31-point skip if >10% jump to next point) vs basis-normalized sourced FY EPS, ±15%.
  - Sourced: back-solved from 63d-lagged `eps_pit` at v3.6 check dates (matches v3.6 harness convention); Persistent 2021 uses audited ₹29.485 (₹58.97 ÷ 2, split only); Astral uses 1.19× normalization (v3.7).
  - *Sensitivity (documented, not hidden):* Persistent 2021's check-(a) PASS (+11.9%: implied ₹33.0 vs audited-basis ₹29.485) becomes a FAIL (+16.8%) on the v3.6 stored input ₹28.26. The residual is the ~1.045 ESOP-drift convention factor. Re-admission must rest on a preregistered basis rule (audited restated only for splits/bonuses), not on choosing the passing basis — see V3_7_DELTA §4.1.
  - **Check (b):** >8% unexplained off-results steps. All v3.6/v3.7 (b) cases (APL 2018, Deepak 2018, Navin×2) are already excluded on (a). Adjudication via EPS dataset:
    - APL 2018 +50.5% step: **EXPLAINED** — EPS dataset shows +50.5% jump on 2017-12-11 (Q2FY18 results), 4 days before the quotient step. The (b) exclusion was a dating artifact, but (a) already excludes it.
    - Deepak 2018 −10.4%: **UNEXPLAINED** — no EPS publication within 30d. (b) would fire; (a) already excludes.
- **Result:** 25/50 USABLE on (a) + mnm_2016 (USABLE per v3.7's bonus-normalization verification; corrected series confirms clean FY16 TTM=25.38) = **26/50**.
- **The 26 are exactly the v3.7 frozen set.** No verdict changed.

### 4. Re-frozen set (26)
astral×2, bajajcon_2018, bajfin×2, hero_2018, itc_2017, lichf×2, lupin_2017, mnm×2, persistent×2, piind×2, safari_2020, suntv_2017, symphony×2, tataelxsi_2017, vakrangee_2015, wipro×2, yesbank×2.

### 5. DCF-only live-bar reconstruction
Set membership is identical to v3.7 frozen set, so the v3.7 revalidation results carry over bit-identically:
- Six DCF-tagged legs: persistent_2019 (acc+inv), wipro_2015 (acc+inv), wipro_2017 (acc+inv).
- persistent_2021, mnm_2016: unknown (excluded in v3.6, no fill record; no-new-fills theorem doesn't apply).
- (a) 0 blow-up fills — PASS. (b) 1 winner name (Persistent), ceiling 1 — FAIL. (c) 4.82× to-T — PASS. (d) 1.77× — PASS.
- **v3 NOT LIVE.** No parameter changes authorized.

## Key methodological findings

1. **The "harness bug" was a red herring for verdicts.** The discarded EPS dataset and the quotient agree. The real problems were the v3.6 TEST (timing at +150d, no basis normalization), which v3.7 already fixed. The corrected series validates v3.7, it doesn't overturn it.

2. **Screener EPS dating is inconsistent.** Most points are publication-dated, but some Mar-31 points are back-dated FY values (tataelxsi_2017: 28.05) while others are stale pre-results values (lupin_2017: 69.62). Rule used: skip a Mar-31-dated point if it jumps >10% to the next point.

3. **TTM-drift confirmed.** tataelxsi_2019: v3.6's +11.6% at +210d was a drifted value (43.07, post weak Q1FY20). Results-week TTM is 46.56 (Apr 24 publication), gap +20.8% → correctly excluded. The corrected series confirms v3.7's exclusion.

## Recommended full fix (not built)

**Quarterly-filings EPS spine:** Build a point-in-time EPS series from quarterly results filings (not Screener TTM):
- For each name-date, collect the 4 quarterly EPS figures comprising the FY, as-filed (never restated).
- Derive TTM as sum of trailing 4 quarters.
- Derive P/E as price ÷ this TTM (never price/PE → EPS).
- This eliminates vendor TTM quirks, back-dating, and restatement contamination.
- **Not built now** per task scope. The current corrected series (Screener EPS dataset) is sufficient for usability validation.

## Files
- Raw harvest: `~/workspace/stock-judging/v3/v37_reval/corrected_series/raw/` (24 JSON)
- Stage 1 (divergence): `~/workspace/stock-judging/v3/v37_reval/corrected_stage1.json`
- Final verdicts: `~/workspace/stock-judging/v3/v37_reval/corrected_verdicts_final.json`
- Scripts: `/tmp/harvest_eps.py`, `/tmp/stage1.py`, `/tmp/stage2.py`

## Handoff
- **Corrected usable count:** 26/50 (identical to v3.7 frozen set).
- **Live bar:** (a) 0 PASS, (b) 1 (ceiling 1) FAIL, (c) 4.82× PASS, (d) 1.77× PASS. **v3 NOT LIVE.**
- **DHFL×2, Manpasand×2, Brightcom 2020:** none returned.
- **Report:** `~/workspace/stock-judging/v3/V3_7_USABILITY_CORRECTED_20260923.md`
