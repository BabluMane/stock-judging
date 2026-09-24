# v3.8 out-of-sample pre-registration — 2026-09-24

**Committed BEFORE any OOS data gathering.** No price series, EPS series, or
corporate-action history has been fetched for any name below at the time
this document is committed. This is the live-bar test set
(`specs/V3_7_DELTA.md` §5, `validation/README.md` "Live bar"): 0 blow-ups,
≥ 3 distinct winner names, positive to-T, ≥ 0.8× 24m — run ONCE, no refit.

**The frozen 26-name set is in-sample** (seen during v3.2/v3.6 development)
and stays a sanity check only (`validation/v3_7/INSAMPLE_SANITY_20260924.md`).
None of the 25 companies below appear in it.

## Selection criteria (fixed before name selection)

1. **New companies only.** None of the 25 companies in the original 50-name-date
   set (`aplapollo, astral, bajajcon, bajfin, bhel, brightcom, deepak, dhfl,
   hero, itc, lichf, lupin, manpasand, mnm, navin, persistent, piind, safari,
   suntv, symphony, tataelxsi, trent, vakrangee, wipro, yesbank`). Checked
   name-by-name below — zero overlap.
2. **Mirror the original construction logic**
   (`engine/standard_v3_scoring_spec.md` §12: "25 names — 10 known Indian
   multi-baggers, 10 mediocrities, 5 blow-ups/frauds"). Scaled to ~25
   name-dates at 2 dates/name where the company's listing history allows:
   **5 winner companies × 2 dates = 10, 5 mediocrity companies × 2 dates =
   10, 3 blow-up companies (5 dates, one company single-dated for a stated
   reason) = 5. Total 13 companies, 25 name-dates.**
3. **Category labels are pre-registered from general, well-documented public
   market history known before this task started** — the same basis the
   original set used ("Bablu nominates names, his past winners/losers are
   ideal"; the implementer proposes the rest). No price, EPS, or corporate-action
   series has been pulled for any name here. A label can turn out wrong once
   real PIT data is gathered (task step 4) — that is a finding to report, not
   a reason to swap the name out afterward. **The list is frozen at commit
   time; it does not change based on what task step 4 finds.**
4. **Scoring dates fixed at FY-end (31 March)**, two per company spaced ~2
   fiscal years apart, chosen for (a) enough forward-return runway from the
   scoring date to today (2026-09-24) to compute a 24-month outcome without
   truncation, and (b) staying inside a company's listed history. Where a
   company's listing history doesn't support two dates with that runway, one
   date is used and the reason stated (matches the original set's practice —
   several original names are single-dated, e.g. safari_2020-03-31,
   suntv_2017-03-31 in isolation from a failed pair).
5. **Sector and vintage diversity**, deliberately different from the original
   set's mix (heavy in pipes/chemicals/auto-ancillary/finance), to reduce the
   chance that a structural quirk of one sector drives the result: consumer
   (Titan, Page, DMart, Colgate), pharma (Divi's, Cipla), electricals
   (Polycab), auto (Ashok Leyland), PSU/commodities (Coal India, GAIL),
   retail/jewellery fraud (PC Jeweller, Future Retail), industrials fraud
   (CG Power).
6. **No cherry-picking on ease of data access.** All 13 are large/mid-cap,
   long-listed (except where noted), NSE/BSE-listed names with a Screener.in
   page and full annual-report history — chosen for a fair test, not for
   convenience of a particular winner.

## The 25 name-dates

### Winners (pre-registered) — 5 companies, 10 name-dates

| # | Name-date | Company | NSE symbol | Why pre-registered a winner |
|---|---|---|---|---|
| 1 | titan_2016-03-31 | Titan Company | TITAN | Long-run compounder (jewellery/watches/eyewear); FY16–FY26 total return is a well-documented multi-bagger. |
| 2 | titan_2018-03-31 | Titan Company | TITAN | Second vintage, same thesis. |
| 3 | divislab_2016-03-31 | Divi's Laboratories | DIVISLAB | Pharma API/CRAMS compounder; FY16–FY26 a well-documented multi-bagger, with a sharp mid-decade drawdown (2022–23) as an in-window stress test. |
| 4 | divislab_2018-03-31 | Divi's Laboratories | DIVISLAB | Second vintage, same thesis. |
| 5 | pageind_2015-03-31 | Page Industries | PAGEIND | Innerwear licensee (Jockey India); strong compounder FY15 onward, well-documented very high multiple/ROCE business. |
| 6 | pageind_2017-03-31 | Page Industries | PAGEIND | Second vintage, same thesis. |
| 7 | dmart_2018-03-31 | Avenue Supermarts (DMart) | DMART | Retail compounder; IPO Mar-2017, FY18 is the first clean post-IPO FY-end. Well-documented strong re-rating post-listing. |
| 8 | dmart_2019-03-31 | Avenue Supermarts (DMart) | DMART | Second vintage, same thesis. |
| 9 | polycab_2020-03-31 | Polycab India | POLYCAB | Wires/cables; IPO Apr-2019, FY20 is the first clean post-IPO FY-end. Well-documented strong multi-year re-rating 2020–2024. |
| 10 | polycab_2021-03-31 | Polycab India | POLYCAB | Second vintage, same thesis. |

### Mediocrities (pre-registered) — 5 companies, 10 name-dates

| # | Name-date | Company | NSE symbol | Why pre-registered mediocre |
|---|---|---|---|---|
| 11 | colpal_2016-03-31 | Colgate-Palmolive (India) | COLPAL | Oral-care major; well-documented multi-year range-bound stretch, muted volume growth, share loss to smaller rivals through the back half of the 2010s. |
| 12 | colpal_2018-03-31 | Colgate-Palmolive (India) | COLPAL | Second vintage, same thesis. |
| 13 | ashokley_2016-03-31 | Ashok Leyland | ASHOKLEY | Commercial-vehicle cyclical; well-documented boom-bust CV cycle, flat-to-negative multi-year total return across several long windows starting near a cycle peak. |
| 14 | ashokley_2018-03-31 | Ashok Leyland | ASHOKLEY | Second vintage, entering the FY19 CV-cycle downturn — the more stress-tested of the two. |
| 15 | cipla_2016-03-31 | Cipla | CIPLA | Large pharma; well-documented multi-year underperformance vs peers (US FDA issues, margin pressure) through the back half of the 2010s. |
| 16 | cipla_2018-03-31 | Cipla | CIPLA | Second vintage, same thesis. |
| 17 | coalindia_2016-03-31 | Coal India | COALINDIA | PSU coal monopoly; well-documented poor long-run shareholder return (high dividend yield, weak capital appreciation) for most of the 2015–2022 window. |
| 18 | coalindia_2018-03-31 | Coal India | COALINDIA | Second vintage, same thesis. |
| 19 | gail_2016-03-31 | GAIL (India) | GAIL | PSU gas-transmission utility; well-documented range-bound/muted multi-year performance. |
| 20 | gail_2018-03-31 | GAIL (India) | GAIL | Second vintage, same thesis. |

### Blow-ups / frauds (pre-registered) — 3 companies, 5 name-dates

| # | Name-date | Company | NSE symbol | Why pre-registered a blow-up |
|---|---|---|---|---|
| 21 | pcjeweller_2017-03-31 | PC Jeweller | PCJEWELLER | Jewellery retailer; well-documented promoter/governance collapse and receivables fraud allegations from 2018, stock down >95% from its highs. |
| 22 | pcjeweller_2018-03-31 | PC Jeweller | PCJEWELLER | Second vintage, scored right as the collapse became public — a genuine stress test of whether DCF entry would have triggered into the trap. |
| 23 | fretail_2017-03-31 | Future Retail | FRETAIL | Kishore Biyani retail group; well-documented over-leveraged expansion, COVID-19 liquidity crisis, insolvency proceedings from 2022, shares extinguished. |
| 24 | fretail_2019-03-31 | Future Retail | FRETAIL | Second vintage, closer to the collapse. |
| 25 | cgpower_2016-03-31 | CG Power and Industrial Solutions | CGPOWER | Crompton Greaves industrial arm; well-documented accounting fraud discovered 2019 (undisclosed liabilities/related-party transactions), near-total equity wipeout before a 2020 promoter change and restructuring. **Single-dated**: a later (FY18/FY19) scoring date would price the name just before public disclosure of fraud already underway, which is a different (still valid, arguably harder) test than this document intends to keep clean of hindsight-adjacent picks; FY16 is used instead as the earlier, cleaner pre-crisis vintage. |

## What happens next (task steps 4–5, not started)

For each of the 25 name-dates above: fetch real EPS, price series, and
corporate-action history from primary/vendor sources (no data has been
fetched yet — see the commit timestamp of this file for the freeze point).
Apply the FROZEN v3.7 usability test (`specs/V3_7_USABILITY_CORRECTED_20260923.md`
§4.1/§4.2, conventions resolved in `validation/v3_7/CONVENTIONS.md`) exactly,
name-date by name-date, with the fired check and reason recorded regardless
of outcome. Then run the DCF-only three-tier entry ONCE on whatever survives
usability. **No name is added, removed, or re-dated after this point for any
reason**, including a name turning out to need usability exclusion, a
category label turning out wrong once real data is seen, or an inconvenient
result. A second run is a new pre-registration, not a rerun of this one.
