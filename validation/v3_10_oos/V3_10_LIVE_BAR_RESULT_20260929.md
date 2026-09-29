# v3.10 OOS live-bar validation result — 2026-09-29

**One locked run, no refit** (`specs/V3_7_DELTA.md` §5). Frozen spec:
`specs/V3_10_DELTA.md` (only delta vs v3.9), `specs/V3_9_DELTA.md` (QFV, GEV,
usability unchanged), `validation/v3_10_oos/OOS_SET_PREREG.md` (25 name-dates,
13 companies, QFV windows, governance template). `engine/`, `cross_engine/`,
`specs/` and prior `validation/` dirs were not touched. Runner, fetched data
and all 13 governance logs were committed **before** the run
(`run_v310_validation.py` is the exact code that produced the numbers); the
run happened once and nothing was changed afterwards.

## Scorecard

| Leg | Bar | Result | Verdict |
|---|---|---|---|
| Blow-up fills | 0 (hard) | **0** (0 of 5 blow-up name-dates filled) | **PASS — with a caveat, see below** |
| Distinct winner names with ≥1 fill | ≥ 3 | **3** — Bharat Electronics, Coforge, HAL | **PASS — zero slack** |
| To-T (fill → latest 2026-09-29) | clearly positive | mean **5.51×** over 17 fills (every leg > 1.18×) | **PASS** |
| 24-month forward | ≥ 0.8× | mean **1.72×** over 17 fills (worst leg 0.955×) | **PASS** |

On the locked, pre-committed rules all four legs pass. **Read the two
caveats before treating that as a clean pass — they are the honest content of
this result, not footnotes:**

1. **The blow-up PASS depends on a classification call.** The only blow-up
   name-date that could have filled is `gensol_2024-03-31`, and GEV
   (not the valuation) is what stopped it. Its price fell from ₹880.65 at
   scoring to ₹133.2 by 2025-04-11, crossing the 0.875× ACC trigger (₹159.48)
   on that date. The veto at that fill rests on the **2025-03-03 CARE
   downgrade-to-D row** — a pre-registered *seeded* event
   ("Q1-CY2025 rating-agency downgrades and lender defaults"), which I kept as
   qualifying per the rule fixed before the run (below). A rating-agency
   downgrade is not literally one of the six §2.1 types. **Under a strict
   literal §2.1 reading the ACC leg fills on 2025-04-11 at ₹133.2 and is at
   0.115× today — a blow-up fill, bar FAIL** (`sensitivity_v310.json`,
   S1). Only the INV leg stays vetoed then (SEBI order 2025-04-15).
2. **Winner names = exactly 3 (the bar), and the valuation does not separate
   winners from mediocrities.** Fills came at the *first weekly close after
   scoring* for **all 8** filled name-dates (at least one leg already at or below trigger on day one).
   Mediocrities filled too — Bajaj Auto 2019, Petronet 2019 and 2021, Power
   Grid 2021 — 9 of 17 fill legs. Winner legs average 9.43× to-T / 2.36× 24m;
   mediocre legs 2.02× / 1.15×. Both aggregates are helped by 2019–21
   entries into the COVID trough, so the 5.51× / 1.72× headline is not a
   clean measure of the mechanism.

I am not calling v3.10 "live". The PR is open for review, not merged.

## Step A — usability (frozen v3.7 test, applied first)

**17 / 25 usable.** Check (a): audited FY EPS (screener `EPS in Rs`) vs the
vendor TTM at the FY results week (median results-week..+21d), ±15%. Check
(b): >8% implied-EPS step outside ±30d of an EPS publication, evaluated over
the name-date's trailing-5-FY window. Basis check (CONVENTIONS §4): for every
name with a split/bonus after the scoring FY-end, the audited row was already
on the vendor's post-action basis (implied shares constant across each
ex-date), so **no restatement was applied anywhere**. Financial variant (LVB):
exempt from (a)/(b).

| Name-date | Verdict | Fired check / reason |
|---|---|---|
| dixon_2019-03-31 | USABLE | (a) +0.0% (TTM 11.19 vs 11.19); (b) none |
| dixon_2021-03-31 | USABLE | (a) +0.4%; (b) none |
| hal_2019-03-31 | USABLE | (a) −7.3% (results week resolved to 2019-08-13, see notes) |
| hal_2021-03-31 | USABLE | (a) +0.1% |
| bel_2019-03-31 | **EXCLUDED** | **(a) −24.0%** — vendor TTM 1.96 @ 2019-05-29 vs audited 2.58; vendor point is stale (unchanged from Jan-2019, updated 2019-08-23) |
| bel_2021-03-31 | USABLE | (a) +0.0% |
| coforge_2019-03-31 | USABLE | (a) +1.3% |
| coforge_2021-03-31 | USABLE | (a) +2.5% |
| tatapower_2020-03-31 | **EXCLUDED** | **(a) −20.7%** (TTM 2.98 vs audited 3.76) |
| tatapower_2021-03-31 | USABLE | (a) +6.8% |
| hul_2021-03-31 | USABLE | (a) +2.2% |
| hul_2022-03-31 | USABLE | (a) +0.3% |
| bajajauto_2019-03-31 | USABLE | (a) −4.9% |
| bajajauto_2021-03-31 | USABLE | (a) +0.0% |
| petronet_2019-03-31 | USABLE | (a) −5.3% |
| petronet_2021-03-31 | USABLE | (a) +0.0% |
| bpcl_2019-03-31 | **EXCLUDED** | **(a) +15.8%** (TTM 20.82 vs 17.98) — 0.8pp outside tolerance |
| bpcl_2021-03-31 | **EXCLUDED** | **(a) −26.5%** (TTM 27.37 vs 37.26) |
| powergrid_2019-03-31 | **EXCLUDED** | **(a) −50.9%** (TTM 5.30 vs 10.79; vendor point is a partial/erroneous TTM) |
| powergrid_2021-03-31 | USABLE | (a) +6.0% |
| coffeeday_2019-03-31 | **EXCLUDED** | **(a) −35.9%** (TTM 3.87 vs 6.04) |
| coffeeday_2020-03-31 | **EXCLUDED** | **(a) −125.6%** (TTM −22.79 vs audited 89.16) |
| gensol_2023-03-31 | **EXCLUDED** | **(a) +26.8%** (TTM 8.08 vs 6.37) |
| gensol_2024-03-31 | USABLE | (a) +10.8% |
| lvb_2019-03-31 | USABLE | financial variant — exempt from (a)/(b) |

Check (b) fired for no name-date. The 8 exclusions are all check (a); none
was adjusted after the fact. **Excluded name-dates were still valued in a
labelled SHADOW pass (non-decisional) so an exclusion cannot hide a fill:**
no shadow blow-up name-date fills (below). Shadow winner/mediocre fills exist
(bel_2019, bpcl_2019, powergrid_2019) but would not change the winner-name
count (BEL already counted via 2021).

## Step B — v3.10 valuation (as implemented)

`g = min(ROE_avg3 × (1 − payout), 15%)`, 10-year explicit horizon, margin fade
years 1–5 then flat, terminal at year 10 (g 4%), Rf 6.95%, ERP 4.0%, tax
25.17%, capex ≈ depreciation, WC 5% of incremental revenue, net cash =
investments − borrowings; financial variant = 10-year excess-return with
BVPS growth = same g. QFV bar, entry tiers (1.00/0.875/0.70), GEV taxonomy,
usability tests unchanged.

### Conventions where the delta is silent (fixed before the run, uniform)

| # | Silent point | Convention |
|---|---|---|
| C1 | ROE_avg3 construction | Mean over the last 3 FYs of PAT_t ÷ (Equity Capital_t + Reserves_t), each on its own year-end book — the per-year-ratio construction the frozen v3.9 bank code already used. (Sensitivity only: avg PAT ÷ scoring-FY book.) |
| C2 | Payout | Scoring-FY screener `Dividend Payout %`, used as-is: >100% ⇒ (1−payout) < 0; negative payout ⇒ (1−payout) > 1; blank ⇒ 0%. No clipping. |
| C3 | Floor on g | None (formula has none): negative ROE or payout >100% ⇒ negative g, applied for all 10 years. |
| C4 | < 3 FYs of history | Mean over available FYs (≥ 1); none ⇒ not computable. (Never triggered.) |
| C5 | Negative/zero book | Ratio computed literally when book ≠ 0; book = 0 ⇒ year skipped. (Never triggered.) |
| C6 | Usability | v3.9 harness rule kept: sourced FY EPS ≤ 0 ⇒ EXCLUDED as basis defect. Check (b) window = trailing-5-FY window. |
| C7 | Usability-excluded names | Also valued in a shadow pass (non-decisional, excluded from the scorecard). |
| C8 | GEV mechanics | Scoring-date veto blocks the whole 24m window (v3.9 harness); fill-date veto blocks that fill only. Cooling-off = later of event+365d and the first annual (Q4) results publication after the event; no publication on record ⇒ still active. |
| C9 | Sector betas | Fixed pre-run in the style of v3.8/v3.9: dixon 1.10, hal 0.90, bel 0.90, coforge 0.95, tatapower 1.10, hul 0.55, bajajauto 0.85, petronet 0.80, bpcl 1.00, powergrid 0.75, coffeeday 1.15, gensol 1.30, lvb 1.15. |
| C10 | GEV event classification | Pre-registered seeded events count as qualifying with their seeded tag; every other logged row is judged by literal §2.1 wording, borderline calls go to the non-qualifying table. |

Conventions that visibly bite (applied literally, not tuned): `hul_2021`
payout 119% ⇒ g = −11.1% (FV 219.6/share vs price 2,218); `gensol` ROE
17–18% with zero payout ⇒ cap binding; LVB ROE_avg3 −20.1% ⇒ g −20.1% and a
perpetual negative excess return ⇒ **negative fair value (−6.69/share)** — a
property of the frozen excess-return construction with no residual-income
fade, not a data error.

### Per name-date (usable; * = 15% cap binding)

| Name-date | g | ROE_avg3 | payout | FV/share | Price@d0 | P/FV | QFV | GEV@score | Fills (leg → date) |
|---|---|---|---|---|---|---|---|---|---|
| dixon_2019 | 15.0%* | 20.1% | 4% | 288.4 | 470.2 | 1.63 | no — (d) mcap ₹2,877cr | no | none |
| dixon_2021 | 15.0%* | 20.2% | 4% | 770.7 | 3,624.6 | 4.70 | yes | no | none |
| hal_2019 | 14.7% | 20.4% | 28% | 973.6 | 353.2 | 0.36 | no — ROCE series unavailable | no | ACC, INV → 2019-04-05 |
| hal_2021 | 14.3% | 20.7% | 31% | 1,435.4 | 493.5 | 0.34 | no — OCF/PAT −0.15 | no | ACC, INV → 2021-04-01 |
| bel_2021 | 10.4% | 19.2% | 46% | 71.2 | 40.8 | 0.57 | no — OCF/PAT 0.80 | no | ACC, INV → 2021-04-01 |
| coforge_2019 | 15.0%* | 18.0% | 0% | 273.5 | 265.2 | 0.97 | **yes** | no | **QFV → 2019-04-05; ACC → 2020-03-20** |
| coforge_2021 | 15.0%* | 19.6% | 17% | 345.5 | 559.2 | 1.62 | yes | **yes** (2020-11-12) | vetoed at scoring |
| tatapower_2021 | 5.1% | 9.1% | 44% | 41.3 | 103.5 | 2.51 | no — ROIC 8% | no | none |
| hul_2021 | −11.1% | 58.6% | 119% | 219.6 | 2,218.4 | 10.10 | yes | no | none |
| hul_2022 | 3.9% | 39.0% | 90% | 736.8 | 1,869.2 | 2.54 | yes | no | none |
| bajajauto_2019 | 14.0% | 21.6% | 35% | 5,730.7 | 2,911.1 | 0.51 | no — OCF/PAT 0.80 | no | ACC, INV → 2019-04-05 |
| bajajauto_2021 | 3.6% | 21.0% | 83% | 2,912.3 | 3,600.1 | 1.24 | no — OCF/PAT 0.74 | no | none |
| petronet_2019 | 7.1% | 21.5% | 67% | 277.0 | 251.6 | 0.91 | no — ROCE series unavailable | no | ACC → 2019-04-05; INV → 2020-03-27 |
| petronet_2021 | 9.7% | 23.7% | 59% | 332.9 | 224.1 | 0.67 | **yes** | no | **QFV**, ACC, INV → 2021-04-01 |
| powergrid_2021 | 8.2% | 17.1% | 52% | 268.0 | 120.7 | 0.45 | no — ROIC 10% | no | ACC, INV → 2021-04-01 |
| gensol_2024 | 15.0%* | 16.9% | 0% | 182.3 | 880.7 | 4.83 | no — ROIC min 12% | no | ACC/INV **vetoed at fill** |
| lvb_2019 (fin.) | −20.1% | −20.1% | 0% | −6.69 | 71.0 | n/a | n/a | — | none (no positive trigger) |

QFV qualified: dixon_2021, coforge_2019/2021, hul_2021/2022, petronet_2021.
**QFV fills: 2** (coforge_2019, petronet_2021). ROIC = screener `ROCE %`
(v3.9 convention). The screener free tier reaches back to FY2015 (earliest
column), which is exactly the FY15 start the FY15–FY19 windows need, so the
v3.9 "data-horizon ceiling" did **not** bite here except: Gensol's
consolidated history begins FY17, LVB's ends FY20 (delisted), and two
name-dates lack a 5-FY ROCE series in the ratios table (HAL 2019, Petronet 2019),
recorded as not QFV-qualified, never substituted.

## Step C — blow-ups, name-date by name-date

| Name-date | Usability | Fair value | What stopped a fill |
|---|---|---|---|
| coffeeday_2019 | EXCLUDED (a) −35.9% | shadow −197.0/share | usability gate; independently, no positive trigger exists |
| coffeeday_2020 | EXCLUDED (a) −125.6% | shadow −158.6/share | usability gate; independently, no positive trigger |
| gensol_2023 | EXCLUDED (a) +26.8% | shadow 48.0/share | usability gate; independently, price never got below 3.84× FV in the window |
| gensol_2024 | USABLE | 182.3/share | **GEV veto at fill** (2025-03-03 CARE downgrade-to-D, see caveat 1) |
| lvb_2019 | USABLE (exempt) | −6.69/share | negative fair value — no positive trigger; GEV (PCA 2019-09-28) never reached |

**Which blow-ups GEV would NOT have caught, stated plainly:** GEV was
exercised end-to-end against a real fill opportunity for exactly one
name-date (`gensol_2024`), and it blocked both legs. It was never the
deciding mechanism for the other four (usability and/or negative fair value
stopped them first). At scoring date, `coffeeday_2019`, `gensol_2023`, `gensol_2024` and `lvb_2019`
carried no qualifying event inside their trailing 12 months — Gensol's first
qualifying public event (2025-03-03) came 11 months after the FY24 scoring
date, by which point the stock was collapsing. `coffeeday_2020` *would* have
been vetoed at scoring (Jul-2019 founder event, 2019-09-04 pledge invocation,
2020-01-13 exchange freeze all fall inside its trailing 12 months), but the
run never evaluated that veto because a non-positive fair value returns before
GEV is reached. That is the §5 residual risk: GEV blocks entries *after* the
first public red flag, it does not predict it. Blow-up protection here came
largely from the DCF returning ≤ 0 or an unaffordable price/FV for insolvent
or over-levered names, which is a valuation property, and (for LVB) from an
excess-return construction whose negative FV is arguably an artifact.

## Step D — governance logs (`governance_logs/<company>.md`)

Method limit stated plainly: BSE/NSE announcement pages returned
403/CAPTCHA/503, so exchange-filing dates come from SEBI/RBI/NFRA/rating-agency
documents and national press quoting the filings (links in each log); this is
a targeted search pass, not a filing crawl. Rows sourced only to an
aggregator are marked WEAK-SOURCE. Absence of hits is not proof of absence.

**Seeded events (finding-by-finding):**

| Seeded event | Status |
|---|---|
| Coffee Day Jul-2019 founder disappearance/death | **Sourced**, 2019-07-31 |
| Coffee Day Jan-2020 "disclosure of ~₹3,500 cr diverted" | **Seeded date wrong.** No source dates the disclosure to Jan-2020; the company filed the Malhotra investigation report on **2020-07-24**. Logged there. The real Jan-2020 events (exchange suspension notice, promoter-holding freeze, 2020-01-13) are logged separately. Reported as a finding; name not swapped. |
| LVB Sep-2019 RBI PCA | **Sourced**, 2019-09-28 |
| LVB Nov-2020 moratorium + DBS scheme | **Sourced**, 2020-11-17 (RBI moratorium/draft-scheme PDF sat behind a CAPTCHA; the equity write-off is sourced to press coverage) |
| Gensol Q1-CY2025 downgrades / lender defaults | **Sourced** as CARE (2025-03-03) and ICRA (2025-03-04) downgrades to D; the defaults are evidenced via those rationales — a separately dated default filing was not retrieved |
| Gensol Apr-2025 SEBI interim order | **Sourced**, 2025-04-15 (confirmatory order 2025-07-30) |

The "≥ 2 blow-up name-dates with dated events inside 24m" requirement is met
by coffeeday_2019, lvb_2019, gensol_2023 and gensol_2024.

**Classification rulings (fixed before the run; each is a judgment call):**
seeded tags kept (founder death is not a literal §2.1.3 sub-type; the
Gensol rating rows are not a literal §2.1 type); Coffee Day auditor
*disclaimer of opinion* logged as `auditor_event` (not literally
"qualified/adverse"); Coforge's two SEBI settlements (CFO 2020-11-12,
company 2021-01-29) logged as qualifying by literal wording; Dixon's SEBI
exemption for promoter gift of 19.90% (2023-03-28) qualifying by literal
"gifts of promoter shares"; Power Grid's CBI arrest of an *Executive
Director* (2022-07-07) logged **non-qualifying** (senior-management rank,
not verified as board director/Companies Act KMP) — falls after the
`powergrid_2021` fills, no effect; BPCL's withdrawn ₹18,000 cr rights issue
(2024-10-25) qualifying, outside every BPCL window. **Vetoes that actually
fired:** `coforge_2021` at scoring (2020-11-12); `gensol_2024` ACC and INV at
fill (2025-03-03).

## Sensitivities (non-decisional; `sensitivity_v310.py`, run after the locked run)

| # | Alternative reading | Effect on the bar legs |
|---|---|---|
| S1 | Gensol rating-downgrade rows not counted (strict §2.1) | `gensol_2024` ACC fills 2025-04-11 @₹133.2, 0.115× to-T/24m ⇒ **blow-up leg FAIL** |
| S2 | ROE_avg3 = avg PAT ÷ scoring-FY book | Fill set unchanged for winners (hal, bel_2021, coforge_2019 still fill ⇒ 3 names); petronet INV/ACC dates shift; no blow-up fills |
| S3 | Coforge settlements treated as routine | `coforge_2019` unchanged (its fills predate 2020-11-12); `coforge_2021` unblocked but has no fill (P/FV 1.62). Winner-name count unchanged |
| S4 | Usability gate ignored (shadow) | No blow-up fills (coffeeday: negative FV; gensol_2023: never < 3.84× FV). Extra winner-side fill: bel_2019 |
| S5 | Aggregation | Winner legs 9.43× / 2.36×; mediocre legs 2.02× / 1.15× (worst 0.955×); per-name-date weighted 5.78× / 1.76× |

## Deviations and data notes

- **Corporate actions:** screener has no split/bonus table, BSE/NSE APIs
  returned 403 and pocketful.in is now client-rendered. Splits/bonuses come
  from Yahoo Finance's public split-event feed (a deviation from "screener
  only"); Yahoo has no feed for delisted LVB (no actions recorded; LVB is
  usability-exempt and has none after its scoring FY).
- **Variant:** consolidated screener view for all companies except LVB
  (standalone; no consolidated statements); the chart API was queried on the
  same basis.
- **Results-week resolution:** the frozen rule picks the first vendor EPS
  publication after the FY-end. For HAL 2019 that lands on 2019-08-13 (median
  of 29.76 and 34.81), passing at −7.3%; BEL 2019 and Power Grid 2019 fail on
  stale/partial vendor points. Applied as frozen — not tuned.
- **Fill mechanics/aggregation** are the v3.9 harness's: first weekly close ≤
  trigger inside (d0, d0+24m], leg-weighted means, price return only
  (no dividends). LVB's price series ends 2020-11-25 (delisting) — irrelevant
  here (no fill), but any LVB fill's to-T would need a zero terminal value.
- Gensol's audited history stops at FY24; its price series continues to
  2026-09-29.
- Shares outstanding = screener market cap ÷ price today (frozen method);
  consistent with the split-adjusted price series.

## Files

`fetch_data_v310.py`, `run_v310_validation.py` (docstring = convention record),
`sensitivity_v310.py`, `oos_results_v310.json`, `sensitivity_v310.json`,
`fetch_meta_v310.json`, `full_financials_raw_v310.json`,
`top_ratios_v310.json`, `pe_series/`, `eps_series/`, `corp_actions/`,
`governance_logs/` (13 logs).
