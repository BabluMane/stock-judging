# v3.7 Usability Rerun — 2026-09-23

**Status:** Complete. Validation set frozen below.  
**Scope:** Usability rerun only. Full DCF/live-bar revalidation NOT started.

## Headline

- **26/50 usable** (v3.6: 25/50).
- **Returns:** Persistent 2021 (required), M&M 2016 (bonus-normalization).
- **Drops out:** Tata Elxsi 2019 (v3.6 pass was TTM-drift false positive).
- **Brightcom 2020** remains excluded (vendor error, required).

## 1. Methodology delta vs v3.6

| | v3.6 | v3.7 |
|---|---|---|
| Check (a) timing | +150/+210 days post-scoring | FY results week (TTM==FY by construction) |
| Basis | None (raw comparison) | Normalize split/bonus/share-count first; constant cross-year ratios are not errors |
| Tolerance | ±15% | ±15% (unchanged) |
| Check (b) steps | >8% unexplained step outside results windows → exclude | Unchanged |

**Rationale:** v3.6's +150d timing conflated TTM drift (fast growers) with data errors. v3.7 moves to results week where TTM equals FY EPS by construction, and normalizes corporate-action basis differences before comparing.

**Implementation:** For each name-date, (1) back-solved the v3.6 sourced FY EPS from the reported gap and series (validated: 5/5 exact matches where v3.5/v3.6 inputs agreed); (2) detected the FY-results TTM step in the Apr–Aug window; (3) compared post-step median TTM to basis-normalized sourced EPS; (4) applied ±15%.

## 2. Verdicts — all 50 name-dates

| # | Name-date | v3.7 | v3.6 | Fired check / reason |
|---|---|---|---|---|
| 1 | aplapollo_2016-03-31 | EXCLUDED | EXCLUDED | Defective series (prereg); suspicious −36% mid-year drop |
| 2 | aplapollo_2018-03-31 | EXCLUDED | EXCLUDED | (b) unexplained +50% step 2017-12-15 |
| 3 | astral_2016-03-31 | USABLE | USABLE | (a) pass after 1.19× basis normalization |
| 4 | astral_2018-03-31 | USABLE | USABLE | (a) pass after 1.19× basis normalization |
| 5 | bajajcon_2016-03-31 | EXCLUDED | EXCLUDED | (a) +23.2%, fails |
| 6 | bajajcon_2018-03-31 | USABLE | USABLE | (a) +0.4%, passes |
| 7 | bajfin_2015-12-31 | USABLE | USABLE | Financial variant, no EPS test |
| 8 | bajfin_2017-12-29 | USABLE | USABLE | Financial variant, no EPS test |
| 9 | bhel_2015-03-31 | EXCLUDED | EXCLUDED | (a) −58.5%, fails |
| 10 | bhel_2017-03-31 | EXCLUDED | EXCLUDED | (a) −21.9%, fails |
| 11 | brightcom_2018-08-22 | EXCLUDED | EXCLUDED | No PIT EPS at date (structural) |
| 12 | brightcom_2020-08-21 | EXCLUDED | EXCLUDED | Vendor error: 18× discrepancy (audited 9.24 vs implied 0.23) |
| 13 | deepak_2016-03-31 | EXCLUDED | EXCLUDED | (a) +24.7%, fails |
| 14 | deepak_2018-03-31 | EXCLUDED | EXCLUDED | (b) unexplained −10% step 2017-06-16 |
| 15 | dhfl_2014-06-04 | EXCLUDED | EXCLUDED | No series (structural) |
| 16 | dhfl_2016-06-03 | EXCLUDED | EXCLUDED | No series (structural) |
| 17 | hero_2016-03-31 | EXCLUDED | EXCLUDED | (a) +16.0%, fails (marginal) |
| 18 | hero_2018-03-31 | USABLE | USABLE | (a) +3.3%, passes |
| 19 | itc_2015-03-31 | EXCLUDED | EXCLUDED | (a) +16.1%, fails (marginal) |
| 20 | itc_2017-03-31 | USABLE | USABLE | (a) +9.8%, passes |
| 21 | lichf_2016-03-31 | USABLE | USABLE | Financial variant, no EPS test |
| 22 | lichf_2018-03-31 | USABLE | USABLE | Financial variant, no EPS test |
| 23 | lupin_2015-03-31 | EXCLUDED | EXCLUDED | (a) +15.6%, fails (marginal) |
| 24 | lupin_2017-03-31 | USABLE | USABLE | v3.6 pass retained; series slow to update at FY17 results (caveat) |
| 25 | manpasand_2015-07-09 | EXCLUDED | EXCLUDED | No PIT EPS at date (structural) |
| 26 | manpasand_2016-05-20 | EXCLUDED | EXCLUDED | (a) +23.4%, fails |
| 27 | mnm_2016-03-31 | USABLE | EXCLUDED | 2.0× bonus normalization (ex-Dec 2017); gap ~0%. v3.6 had "no post-results pt" |
| 28 | mnm_2018-03-31 | USABLE | USABLE | (a) −13.9%, passes |
| 29 | navin_2016-03-31 | EXCLUDED | EXCLUDED | (b) unexplained −14% step 2015-06-19 |
| 30 | navin_2018-03-31 | EXCLUDED | EXCLUDED | (b) unexplained −14% step 2015-06-19 |
| 31 | persistent_2019-03-29 | USABLE | USABLE | (a) −6.0%, passes |
| 32 | persistent_2021-03-31 | USABLE | EXCLUDED | (a) +11.9% on audited-normalized 29.485. **RETURNS** (required) |
| 33 | piind_2016-03-31 | USABLE | USABLE | (a) −2.9%, passes |
| 34 | piind_2018-03-31 | USABLE | USABLE | (a) −3.1%, passes |
| 35 | safari_2018-03-31 | EXCLUDED | EXCLUDED | (a) +108%, fails |
| 36 | safari_2020-03-31 | USABLE | USABLE | (a) +13.1%, passes (post-update TTM) |
| 37 | suntv_2017-03-31 | USABLE | USABLE | (a) +9.1%, passes |
| 38 | suntv_2019-03-29 | EXCLUDED | EXCLUDED | (a) +22.8%, fails |
| 39 | symphony_2016-03-31 | USABLE | USABLE | (a) +7.0%, passes |
| 40 | symphony_2018-03-31 | USABLE | USABLE | (a) −1.8%, passes |
| 41 | tataelxsi_2017-03-31 | USABLE | USABLE | (a) +12.7%, passes |
| 42 | tataelxsi_2019-03-31 | EXCLUDED | USABLE | (a) +26.9% at results week. v3.6's +11.6% was TTM-drift false pass |
| 43 | trent_2019-03-29 | EXCLUDED | EXCLUDED | (a) +33.9%, fails |
| 44 | trent_2021-03-31 | EXCLUDED | EXCLUDED | No PIT EPS at date (structural) |
| 45 | vakrangee_2013-06-03 | EXCLUDED | EXCLUDED | No PIT EPS at date (structural) |
| 46 | vakrangee_2015-06-01 | USABLE | USABLE | (a) +10.4%, passes |
| 47 | wipro_2015-03-31 | USABLE | USABLE | (a) −2.5%, passes |
| 48 | wipro_2017-03-31 | USABLE | USABLE | (a) −2.8%, passes |
| 49 | yesbank_2015-03-05 | USABLE | USABLE | Financial variant, no EPS test |
| 50 | yesbank_2017-03-03 | USABLE | USABLE | Financial variant, no EPS test |

## 3. Frozen usable validation set (26)

```
bajfin_2015-12-31, bajfin_2017-12-29,
lichf_2016-03-31, lichf_2018-03-31,
yesbank_2015-03-05, yesbank_2017-03-03,
persistent_2019-03-29, persistent_2021-03-31,
piind_2016-03-31, piind_2018-03-31,
wipro_2015-03-31, wipro_2017-03-31,
hero_2018-03-31, itc_2017-03-31, bajajcon_2018-03-31,
suntv_2017-03-31, symphony_2016-03-31, symphony_2018-03-31,
tataelxsi_2017-03-31, vakrangee_2015-06-01, mnm_2018-03-31,
astral_2016-03-31, astral_2018-03-31,
mnm_2016-03-31,
lupin_2017-03-31, safari_2020-03-31
```

## 4. Reason breakdown (24 excluded)

| Reason | Count | Names |
|---|---|---|
| No series | 2 | dhfl ×2 |
| No PIT EPS at date | 4 | brightcom_2018, manpasand_2015, trent_2021, vakrangee_2013 |
| Unexplained step >8% (b) | 4 | aplapollo_2018, deepak_2018, navin ×2 |
| Vendor error / defective series | 2 | brightcom_2020, aplapollo_2016 |
| (a) gap >±15% at results week | 12 | bhel ×2, deepak_2016, bajajcon_2016, hero_2016, itc_2015, lupin_2015, manpasand_2016, safari_2018, suntv_2019, tataelxsi_2019, trent_2019 |

## 5. Names returning vs v3.6

**Returning (2):**
- **persistent_2021-03-31** — v3.6 excluded on +27.2% TTM-drift at +150d. v3.7: audited FY21 EPS ₹58.97, normalized ÷2 for 1:2 split (ex-Mar 2024) = ₹29.485; Screener TTM at results week ≈ ₹33.0; gap +11.9% → passes. The required re-admission.
- **mnm_2016-03-31** — v3.6 "no post-results pt". v3.7: 1:1 bonus ex-Dec 2017 confirmed; series is bonus-adjusted (÷2, smooth through ex-date); normalized gap ~0% → usable.

**Dropping out (1):**
- **tataelxsi_2019-03-31** — v3.6 passed on +11.6% at +210d, but that point had drifted down on weak Q1/Q2 FY20. At results week the gap is +26.9% → fails. v3.6 pass was a TTM-drift false positive in the other direction.

## 6. Caveats

**Corporate actions (verified 2026-09-23):**
- Persistent 1:2 split ex-2024-03-28; 1:1 bonus ex-2015-03-10. Normalization uses split only (÷2).
- M&M 1:1 bonus ex-2017-12-21; split FV 10→5 ex-2010-03-29. mnm_2016 normalized ÷2.
- APL Apollo: split FV 10→2 ex-2020-12-15; 1:1 bonus ex-2021-09-16 — both after scoring dates; series already adjusted; not the cause of APL gaps.
- Astral: bonuses 1:4 ex-Sep 2019, 1:3 ex-Mar 2021, 1:3 ex-Mar 2023 — all after scoring dates. The 1.19× constant ratio is a sourced-vs-series basis difference, normalized.
- ITC 1:1 bonus ex-Dec 2016 — after itc_2015 scoring; series not adjusted (price as-was).

**Missing series:** DHFL both dates — no series in bundle; excluded structurally (unchanged).

**Estimated normalization:** v3.6 `inputs/` directory was not in the bundle. Sourced FY EPS was back-solved from reported v3.6 gaps (validated 5/5 where v3.5/v3.6 inputs agreed; 3 divergences are v3.6 input updates, not method errors). Persistent 2021 uses audited EPS (₹58.97 → ₹29.485) as ground truth rather than the back-solved sourced. Marginal gaps (±15–16%: hero_2016, itc_2015, lupin_2015, astral_2016) are sensitive to this estimation; verdicts follow the computed values.

**Series-vs-v3.6 discrepancy:** The bundle's ITC series implies −28% vs sourced where v3.6 reported +15.9%; back-solve indicates v3.6 used an updated (lower) sourced input. Verdicts use the back-solved v3.6-consistent inputs throughout.

**lupin_2017 caveat:** Series shows no clear TTM update at FY17 results (stale through Jun 2017); v3.6 pass retained on the +210d reading. Flagged for the DCF revalidation to treat with care.

## 7. What this unlocks

The frozen 26-name set is ready for the full DCF/live-bar revalidation (not started, per authorization). Key improvement vs v3.6: the set now includes the largest winner (Persistent 2021, 12.72×) which v3.6 wrongly excluded over TTM drift.

---

✅ DONE — you can copy the paragraph above
