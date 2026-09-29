# v3.9 OOS live-bar validation result — 2026-09-29

**Verdict: FAIL.**

**One run, no refit** (`specs/V3_7_DELTA.md` §5). Real data only: screener.in
weekly price/PE/EPS chart series + audited P&L/balance-sheet/cash-flow
tables, fetched fresh this session (`fetch_full_financials_v39.py`,
`pe_series/*.csv`, `eps_series/*.json`, `full_financials_raw_v39.json`,
`top_ratios_v39.json` — all committed alongside this doc). `engine/`,
`cross_engine/`, `specs/V3_7_DELTA.md`, and `validation/v3_8_oos/` were not
touched. **No company below is investable; v3 is NOT live.**

## The four-line scorecard

| Bar | Requirement | Result |
|---|---|---|
| Blow-up fills | 0 (hard) | **0** — PASS |
| Winner names with ≥1 fill | ≥ 3 distinct | **0** — FAIL |
| To-T (to-latest) | clearly positive | no fills at all — N/A |
| 24-month forward return | ≥ 0.8× | no fills at all — N/A |

**Zero fills occurred on any leg (QFV/ACC/INV) for any of the 25
name-dates.** The hard 0-blow-ups bar is met only because nothing filled at
all, not because GEV or QFV successfully separated good entries from bad
ones on live data — that mechanism was never exercised. This is a clean
FAIL on the live bar, stated plainly, and the reasons are structural, not
a parameter-tuning problem (per the anti-fitting discipline, no threshold
was adjusted after seeing this).

## Step A — usability (frozen v3.7 test, `validation/v3_7/CONVENTIONS.md`)

**11 / 25 name-dates usable.**

| Name-date | Verdict | Reason |
|---|---|---|
| asianpaint_2014-03-31 | EXCLUDED | structural — FY2014 audited P&L not in the fetched table (see "Data-horizon ceiling" below) |
| asianpaint_2016-03-31 | **USABLE** | (a) −7.6% gap, within ±15% |
| hdfcbank_2014-03-31 | EXCLUDED | structural — FY2014 not fetched |
| hdfcbank_2016-03-31 | **USABLE** | financial variant, exempt from (a)/(b) per `V3_7_DELTA.md` §4 |
| nestleind_2015-03-31 | EXCLUDED | structural — Nestlé's FY-end is **31 December**, not 31 March (pre-reg assumed Mar uniformly; per `CONVENTIONS.md` §2 the reference FY for scoring date 2015-03-31 is FY-Dec-2014, which is outside the fetched Dec2015→ window) |
| nestleind_2017-03-31 | **USABLE** | reference FY = FY-Dec-2016 (§2 off-FY convention); (a) +4.0% gap |
| britannia_2015-03-31 | EXCLUDED | (a) −15.5% gap, just outside ±15% |
| britannia_2017-03-31 | **USABLE** | (a) −4.5% gap |
| havells_2014-03-31 | EXCLUDED | structural — FY2014 not fetched |
| havells_2016-03-31 | EXCLUDED | (a) −57.3% gap |
| bhartiartl_2016-03-31 | EXCLUDED | (a) +28.7% gap |
| bhartiartl_2018-03-31 | EXCLUDED | (a) −38.5% gap (price-war-era exceptional items) |
| tatasteel_2015-03-31 | EXCLUDED | (a) sourced FY EPS non-positive (−3.48, European ops write-down years) vs vendor TTM +3.39 |
| tatasteel_2017-03-31 | EXCLUDED | (a) sourced FY EPS non-positive (−3.76) vs vendor TTM +3.64 |
| ntpc_2015-03-31 | **USABLE** | (a) +3.9% gap |
| ntpc_2017-03-31 | **USABLE** | (a) −4.8% gap |
| tatamotors_2015-03-31 | EXCLUDED | (a) −134.0% gap — see "Tata Motors chart-series note" below |
| tatamotors_2017-03-31 | EXCLUDED | (a) −135.1% gap — same note |
| bankbaroda_2015-03-31 | **USABLE** | financial variant, exempt |
| bankbaroda_2017-03-31 | **USABLE** | financial variant, exempt |
| zeel_2017-03-31 | EXCLUDED | (a) −57.2% gap |
| zeel_2018-03-31 | EXCLUDED | (a) +29.3% gap |
| relcapital_2016-03-31 | **USABLE** | financial variant, exempt (reclassified — see below) |
| relcapital_2018-03-31 | EXCLUDED | sourced FY EPS non-positive (−183.38) vs vendor TTM −227.94 — both negative, basis-defect exclusion still applies per `CONVENTIONS.md` §1 (financial-variant exemption is for check (a)/(b) tolerance only, not for the structural non-positive-basis exclusion) |
| ilfstransport_2017-03-31 | **USABLE** | (a) +2.9% gap |

### Data-horizon ceiling (structural finding, not a bug)

screener.in's free-tier company page exposes roughly a rolling 12-year
annual window as of the fetch date. Fetched today (2026-09-29), the
earliest annual P&L/balance-sheet column for every company in this set is
**FY ending March 2015** (Nestlé: Dec 2015, on its own Dec fiscal year).
Three of the pre-registered scoring dates (`asianpaint_2014-03-31`,
`hdfcbank_2014-03-31`, `havells_2014-03-31`) reference FY2014, one FY
earlier than this ceiling, and are **excluded structurally** — not a
judgment call, the data literally isn't retrievable from this free source.
`nestleind_2015-03-31` is excluded for the analogous reason once the
Dec-FY-end correction is applied (its reference FY, Dec-2014, is also one
year earlier than the fetched window). The same ceiling separately blocks
QFV evaluation for several otherwise-usable name-dates (§ "QFV" below) —
their scoring FY sits too close to the window's start to assemble a full
trailing-5-FY history.

### Tata Motors chart-series note

Tata Motors demerged its commercial-vehicle business into a new listed
entity (`TMCV`) in 2024; the original listed entity was renamed **Tata
Motors Passenger Vehicles Ltd** (`TMPV`, screener id 3370) and retained the
pre-demerger consolidated history used here for FY2015/FY2017. Its audited
"EPS in Rs" P&L row for those years is strongly positive (+48.44, +25.82)
and matches the whole pre-demerger consolidated business, but screener's
own price/PE/EPS **chart** series for the same id returns a strongly
**negative** TTM EPS at the same dates (−16.47, −9.06) — a large, clean
(a)-test-failing gap that is a genuine vendor-side artifact of the
demerger-era chart-series restatement, not a code defect (both figures
were pulled from the same fetch, same company id, same session). Both
name-dates are excluded structurally on this basis; no attempt was made to
"fix" the mismatch by picking whichever series passes, per
`CONVENTIONS.md` §4.1 point 1's discipline of transforming only the
non-conforming side onto a named basis — here there is no way to tell
which side is non-conforming, so both are left excluded.

### Financial-variant reclassification

`specs/V3_7_DELTA.md` §4 defines "financial-variant" as **banks/NBFCs**,
scored on the excess-return/DDM model. Reliance Capital's screener page
uses the standard non-bank Sales/OPM% P&L template (not the dedicated bank
template HDFC Bank/Bank of Baroda use), but Reliance Capital **is** an
NBFC/diversified-financial-services holding company by business — running
its raw "Sales" (₹9,941cr FY16, driven by investment/insurance-subsidiary
income, not a comparable industrial revenue line) through the FCFF DCF
below produced a fair value more than 5× too high relative to the excess-
return model's result for the same FY (see the "why zero fills" section) —
confirming that Sales/OPM-based FCFF is the wrong tool for this company
regardless of screener's page template. Reliance Capital is treated as
financial-variant throughout this run.

## Step B — fair value construction

**Non-financial names** (`asianpaint`, `nestleind`, `britannia`, `ntpc`,
`ilfstransport`): standalone 5-year FCFF DCF, identical construction to
`validation/v3_8_oos/run_oos_validation.py` (`Rf`=6.95%, `ERP`=4.0%,
sector-typical beta, terminal growth 4%, tax 25.17%, capex≈depreciation,
working capital = 5% of incremental revenue, revenue growth = trailing
CAGR capped at 12%) — same disclosed simplifications, unchanged.

**Financial-variant names** (`hdfcbank`, `bankbaroda`, `relcapital`):
`engine_v3.py`'s financial variant expects this value **pre-supplied** by
the Record (it does not compute it), so this task reimplements a
standalone excess-return / residual-income model, same spirit as the FCFF
reimplementation: `FV/share = BVPS₀ + Σ₁⁵ (ROE−r)·BVPS_{t-1}/(1+r)ᵗ +
terminal`, with ROE = trailing-3-year average return on book value, BVPS
growth capped at 12% (same cap convention as the FCFF side), and
`r = Rf + β·ERP` (no debt-weight blending, matching `engine_v3.py`'s own
`debt_wt=0` treatment for this variant). **Disclosed new construction,
not previously validated** — Phase 3+ should scrutinize it before reuse.

## Step C — QFV qualification (§1.1, all four AND-gated)

| Name-date | QFV? | Reason |
|---|---|---|
| asianpaint_2016-03-31 | No | only 2 trailing FYs fetched (need 5) — **not evaluable**, not "failed" |
| hdfcbank_2016-03-31 | No | financial variant — ROIC/OCF-PAT/D-E gate not defined for a bank balance sheet (scope limit, disclosed in `specs/V3_9_DELTA.md` is silent on this; this task's judgment call) |
| nestleind_2017-03-31 | No | only 2 trailing FYs fetched — not evaluable |
| britannia_2017-03-31 | No | only 3 trailing FYs fetched — not evaluable |
| ntpc_2015-03-31 | No | only 1 trailing FY fetched — not evaluable |
| ntpc_2017-03-31 | No | only 3 trailing FYs fetched — not evaluable |
| bankbaroda_2015-03-31 | No | financial variant — scope limit as above |
| relcapital_2016-03-31 | No | financial variant — scope limit as above |
| ilfstransport_2017-03-31 | No | (a) median ROIC 12.0%, min 8.0% — **evaluated and failed** the 15%/10% bar |

**Zero QFV qualifications, and only one of the nine (`ilfstransport`) was
actually evaluated to completion** — the rest were blocked by the same
data-horizon ceiling that trimmed usability: QFV's own pre-registered
input spec (`OOS_SET_PREREG_v39.md`) called for 5 trailing audited FYs,
which for scoring dates in 2014–2017 need history back to 2010–2013 —
one to four years earlier than screener's free-tier ~12-year fetch window
reaches as of 2026. This is the single largest honest finding of this
run: **the QFV mechanism specified in `specs/V3_9_DELTA.md` could not be
exercised on real data for 8 of the 9 candidates**, for a data-availability
reason external to the spec's own design.

## Step D — GEV veto (§2, PIT)

Governance-event logs (`governance_logs/*.md`) were populated this session
via targeted national-business-press search (Business Standard), **not** a
full BSE/NSE exchange-filing crawl — disclosed method limitation, matching
`specs/V3_9_DELTA.md` §2.5's own "specified but not fully operable" caveat.
Findings:

- **Zee Entertainment**: two qualifying `promoter_conduct` events (2019-01-25
  Essel-Group/Nityank-Infrapower link disclosed, 33% one-day crash;
  2019-02-03 lenders invoke and sell pledged ZEEL shares) — but both `zeel`
  name-dates were already excluded at usability, so GEV was never reached.
- **Reliance Capital**: one qualifying `auditor_event` (PwC resignation,
  effective 2019-06-11) — `relcapital_2016-03-31`'s fill window
  (2016-03-31→2018-03-31) ends **before** this event; no veto triggers
  because the event is outside the window, not because GEV failed to catch
  it. (This is itself informative for the honest-residual-risk
  requirement — see below.)
- **IL&FS Transportation Networks**: one qualifying `associate_contagion`
  event (2018-09-06, parent IL&FS Group's first disclosed default) —
  inside `ilfstransport_2017-03-31`'s fill window (2017-03-31→2019-03-31),
  but the DCF fair value for this name-date is **negative** (−4.45/share,
  see below), so no fill was ever candidate for a veto to block.
- **Tata Steel and Tata Motors**: one qualifying `regulatory_probe` event
  each (2016-11-08, SEBI directing the exchanges to scrutinise both
  companies' disclosure compliance following Cyrus Mistry's post-ouster
  governance allegations against Tata Sons) — both name-dates for both
  companies were already excluded at usability.
- **Bank of Baroda**: one **logged, non-qualifying** candidate (2015-10-09,
  CBI/ED/SFIO raids over the Ashok Vihar branch forex-remittance scam) —
  judged non-qualifying because the action targeted branch-level officials,
  not the company/promoter/KMP as the taxonomy's §2.1.1 wording requires;
  a disclosed judgment call, not a silent omission.
- **HDFC Bank**: one **logged, non-qualifying** candidate (2016-07-25, ₹2cr
  RBI penalty for KYC/AML lapses) — judged routine/immaterial, not a
  probe/enforcement action.
- **Asian Paints, Nestlé, Britannia, Havells, Bharti Airtel, NTPC**: no
  candidate event identified in-window from this session's press search.

**GEV fired zero vetoes in practice** — not because governance risk was
absent from this OOS set (Zee, Reliance Capital, Tata Steel, Tata Motors,
and IL&FS Transportation all carry real, dated, qualifying events), but
because every name-date GEV could have blocked was already excluded by
usability or had no candidate fill to block. The mechanism is validated as
implementable (real events were found, dated, and tagged) but was not
exercised end-to-end against a live fill on this OOS set.

## Why zero fills occurred (root-cause finding, not a parameter problem)

For the 9 name-dates with a computable fair value, price at the scoring
date was **1.3×–2.9× the computed fair value** in every single case
(financial and non-financial alike):

| Name-date | Price @ scoring | Fair value/share | Price ÷ FV |
|---|---|---|---|
| asianpaint_2016-03-31 | 850.00 | 387.78 | 2.19× |
| hdfcbank_2016-03-31 | 262.34 | 116.27 | 2.26× |
| nestleind_2017-03-31 | 334.06 | 164.74 | 2.03× |
| britannia_2017-03-31 | 1687.00 | 747.08 | 2.26× |
| ntpc_2015-03-31 | 121.33 | 78.61 | 1.54× |
| ntpc_2017-03-31 | 138.33 | 51.68 | 2.68× |
| bankbaroda_2015-03-31 | 160.95 | 55.58 | 2.90× |
| relcapital_2016-03-31 | 330.27 | 254.00 | 1.30× |
| ilfstransport_2017-03-31 | 109.35 | −4.45 | n/a (negative FV) |

QFV's entire design purpose is to remove the *discount* requirement (fill
at 1.00× fair value instead of 0.70–0.875×) for extreme-quality names that
"never discount" — but here the fair-value **estimate itself** sits so far
below the market price (even for a plain PSU utility like NTPC and a bank
like Bank of Baroda, not just the "expensive compounders" QFV targets)
that even a 1.00× threshold was never reached, let alone 0.70–0.875×. This
matches the exact same conservative-DCF behavior visible in
`validation/v3_8_oos/oos_results.json` (Titan, Page Industries, DMart,
Colgate, Cipla all show the identical pattern of no fill across a 24-month
window) — confirming this is a **known, pre-existing property of the
frozen v3.7 FCFF DCF construction** (12%-capped growth, 4% terminal growth,
CAPM discount rate with a modest 4% ERP), not something introduced by this
task's reimplementation. v3.8's usable names that *did* fill (Divi's Lab,
Polycab, Ashok Leyland, Coal India, GAIL, PC Jeweller, Future Retail) all
did so during a severe drawdown inside their 24-month window (the COVID-19
crash, a cyclical trough, or a fraud collapse) — **none of this v3.9 set's
24-month windows (all ending 2016–2020, none reaching the COVID crash for
a usable name) contained a comparable drawdown**, so no fill was possible
regardless of tier.

**New finding for Phase 4 (beyond what v3.8 diagnosed):** the root cause of
"quality names never fill" is not fully explained by the *discount*
requirement that QFV removes — the fair-value **estimate** the frozen FCFF
DCF produces is itself running at roughly half of observed market price
across this entire OOS set, financial and non-financial alike. §1's fix
(discount → zero) does not address a fair-value estimate that is
structurally too low. This is a new, disclosed observation, not
backtested-in or fitted to this outcome (the DCF's parameters were not
touched after seeing this result, per the anti-fitting discipline).

## Honest residual-risk statement (§5, §4's reporting requirement)

Which blow-ups would GEV **not** have caught, and which did it never get
the chance to test?

- **Reliance Capital's leg-1-type risk is real and GEV would have missed
  it**: at `relcapital_2016-03-31`, the FCFF-style excess-return fair value
  (₹254/share) sits only 1.3× below the then-price (₹330) — the smallest
  gap of any name-date in this set — meaning a discount-tier fill was
  plausible on this name-date within reach of real triggers, and the first
  qualifying governance event (PwC's 2019-06-11 resignation) postdates
  this name-date's entire 24-month fill window (ends 2018-03-31). A fraud
  or governance collapse whose first public red flag lands **after** the
  fill window, on clean-looking FY16 filings, passes every rule in this
  spec — exactly the residual risk `specs/V3_9_DELTA.md` §5 names.
- **GEV's mechanism was never live-tested against an actual blocked fill**
  in this run — every qualifying event found (Zee, Tata Steel, Tata
  Motors, IL&FS Transportation) landed on a name-date usability had already
  excluded before GEV was reached, or on a name-date with no candidate fill
  to block. This OOS set does not demonstrate GEV successfully vetoing a
  fill that would otherwise have happened; it only demonstrates that the
  event-log mechanism can be populated with real, dated, sourced events.
  A future OOS set intentionally including a usable, fillable name-date
  with an in-window governance event is needed to test GEV end-to-end.

## Files in this submission

- `oos_results_v39.json` — full usability/fair-value/QFV/GEV/fill output.
- `run_v39_validation.py` — the one-run script (this doc's exact numbers).
- `fetch_full_financials_v39.py` — screener.in P&L/BS/CF/ratios fetch.
- `full_financials_raw_v39.json`, `top_ratios_v39.json` — raw fetched financials.
- `pe_series/*.csv`, `eps_series/*.json` — weekly price/PE/vendor-TTM-EPS series, 13 companies.
- `governance_logs/*.md` — per-company GEV log, PIT, sourced.

No validation, backtest, or fill simulation from this run was reused from
or leaked into `validation/v3_8_oos/` or the frozen in-sample set. No
company named above is described as investable.
