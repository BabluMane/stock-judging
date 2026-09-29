# v3.9 out-of-sample pre-registration — 2026-09-26

**Committed BEFORE any OOS data gathering.** No price series, EPS series,
QFV input data (ROIC/OCF-PAT/D-E/market-cap), governance-event log entries,
or corporate-action history has been fetched for any name below at the time
this document is committed. This is the fresh live-bar test set for
`specs/V3_9_DELTA.md` (`specs/V3_7_DELTA.md` §5, `validation/README.md`
"Live bar"): 0 blow-ups, ≥ 3 distinct winner names, positive to-T, ≥ 0.8×
24m — run ONCE, no refit, per §4 of the v3.9 delta.

**No validation, backtest, or fill simulation was run in this session.**
This document only selects names, dates, and defines input/logging
templates. Category labels below are pre-registered from general,
well-documented public market history known before this task started —
the same basis the v3.8 set used. A label can turn out wrong once real PIT
data is gathered in a later phase; that is a finding to report, not a
reason to swap the name out afterward. **The list is frozen at commit
time; it does not change based on what a later phase finds.**

## Zero-overlap requirement and disjointness proof

Two prior sets must have **zero overlap** with the 13 companies below:

1. The **25-company in-sample frozen set** (`engine/standard_v3_scoring_spec.md`
   §12, restated in `validation/v3_8_oos/OOS_SET_PREREG.md`): `aplapollo,
   astral, bajajcon, bajfin, bhel, brightcom, deepak, dhfl, hero, itc,
   lichf, lupin, manpasand, mnm, navin, persistent, piind, safari, suntv,
   symphony, tataelxsi, trent, vakrangee, wipro, yesbank`.
2. The **13-company v3.8 OOS set** (`validation/v3_8_oos/OOS_SET_PREREG.md`):
   `titan, divislab, pageind, dmart, polycab, colpal, ashokley, cipla,
   coalindia, gail, pcjeweller, fretail, cgpower`.

Verified by script (`check_disjoint.py`, reproduced below verbatim — pure
name-membership check, no data fetched):

```python
INSAMPLE_25 = {
    "aplapollo", "astral", "bajajcon", "bajfin", "bhel", "brightcom",
    "deepak", "dhfl", "hero", "itc", "lichf", "lupin", "manpasand", "mnm",
    "navin", "persistent", "piind", "safari", "suntv", "symphony",
    "tataelxsi", "trent", "vakrangee", "wipro", "yesbank",
}

V3_8_OOS_13 = {
    "titan", "divislab", "pageind", "dmart", "polycab", "colpal",
    "ashokley", "cipla", "coalindia", "gail", "pcjeweller", "fretail",
    "cgpower",
}

V3_9_OOS_13 = {
    "asianpaint", "hdfcbank", "nestleind", "britannia", "havells",
    "bhartiartl", "tatasteel", "ntpc", "tatamotors", "bankbaroda",
    "zeel", "relcapital", "ilfstransport",
}

overlap_all = sorted((INSAMPLE_25 | V3_8_OOS_13) & V3_9_OOS_13)
print(f"DISJOINT: {len(overlap_all) == 0}")
```

**Script output:**

```
in-sample frozen set size: 25
v3.8 OOS set size: 13
v3.9 OOS candidate set size: 13
overlap(v3.9, in-sample-25): []
overlap(v3.9, v3.8-OOS-13): []
overlap(v3.9, union): []
DISJOINT: True
```

## Selection criteria (fixed before name selection)

1. **New companies only**, per the disjointness proof above — 13 companies,
   none of which appear in the in-sample 25 or the v3.8 OOS 13.
2. **Mirror the original construction logic**
   (`engine/standard_v3_scoring_spec.md` §12, same scaling the v3.8 set
   used): **5 winner companies × 2 dates = 10, 5 mediocrity companies × 2
   dates = 10, 3 blow-up companies (2+2+1 dates) = 5. Total 13 companies,
   25 name-dates.**
3. **Scoring dates fixed at FY-end (31 March)**, two per company (one for
   the single-dated blow-up) spaced ~2 fiscal years apart, chosen to stay
   inside each company's listed history and leave forward-return runway
   for a 24-month outcome without truncation.
4. **Prefer large/mid-cap names with clean reporting**, per the task
   instruction — the v3.8 set showed materially higher usability there
   (80%) than in-sample (52%). All 13 below are large/mid-cap, long-listed,
   NSE/BSE names with a Screener.in page and full annual-report history.
   Structurally broken series (multi-year trading suspensions with no
   resumption, index/ticker discontinuities unrelated to the company's own
   fundamental story) are avoided for the winner and mediocrity buckets. The
   blow-up bucket, by construction, includes names whose story *is* a
   governance/solvency collapse — that is the point of the bucket, not a
   data-quality defect, mirroring how the v3.8 set used Future Retail
   (shares later extinguished in insolvency) as a valid blow-up name.
5. **Sector and vintage diversity**, deliberately different from both the
   in-sample mix (pipes/chemicals/auto-ancillary/finance) and the v3.8 OOS
   mix (consumer/pharma/electricals/PSU-commodities/retail-jewellery-fraud):
   paints (Asian Paints), private banking (HDFC Bank), packaged foods
   (Nestlé India, Britannia), consumer electricals (Havells), telecom
   (Bharti Airtel), core steel (Tata Steel), PSU power generation (NTPC),
   autos/CV+PV (Tata Motors), PSU banking (Bank of Baroda), media/broadcast
   governance fraud (Zee Entertainment), NBFC/group-holding governance
   collapse (Reliance Capital), infrastructure-finance/IL&FS-group
   contagion (IL&FS Transportation Networks).
6. **No cherry-picking on ease of data access.** All 13 are NSE/BSE-listed
   with a Screener.in page and (for winners/mediocrities) full,
   uninterrupted annual-report history.

## The 25 name-dates

### Winners (pre-registered) — 5 companies, 10 name-dates

| # | Name-date | Company | NSE symbol | Why pre-registered a winner |
|---|---|---|---|---|
| 1 | asianpaint_2014-03-31 | Asian Paints | ASIANPAINT | Decorative-paints category leader; well-documented long-run compounder through the 2010s on the back of distribution reach and pricing power. |
| 2 | asianpaint_2016-03-31 | Asian Paints | ASIANPAINT | Second vintage, same thesis. |
| 3 | hdfcbank_2014-03-31 | HDFC Bank | HDFCBANK | Private-sector banking franchise; well-documented multi-decade compounder on retail-liability funding cost advantage and asset-quality discipline. |
| 4 | hdfcbank_2016-03-31 | HDFC Bank | HDFCBANK | Second vintage, same thesis. |
| 5 | nestleind_2015-03-31 | Nestlé India | NESTLEIND | Packaged-foods major; well-documented strong re-rating and volume recovery in the years following the 2015 Maggi-noodles ban/recall episode. |
| 6 | nestleind_2017-03-31 | Nestlé India | NESTLEIND | Second vintage, post-recovery. |
| 7 | britannia_2015-03-31 | Britannia Industries | BRITANNIA | Biscuits/bakery major; well-documented strong multi-year re-rating on distribution expansion and margin improvement through the back half of the 2010s. |
| 8 | britannia_2017-03-31 | Britannia Industries | BRITANNIA | Second vintage, same thesis. |
| 9 | havells_2014-03-31 | Havells India | HAVELLS | Consumer electricals/switchgear major; well-documented strong multi-year compounder through the 2010s on brand premiumisation and distribution growth. |
| 10 | havells_2016-03-31 | Havells India | HAVELLS | Second vintage, same thesis. |

### Mediocrities (pre-registered) — 5 companies, 10 name-dates

| # | Name-date | Company | NSE symbol | Why pre-registered mediocre |
|---|---|---|---|---|
| 11 | bhartiartl_2016-03-31 | Bharti Airtel | BHARTIARTL | Telecom incumbent; well-documented multi-year price-war margin/ARPU pressure and muted-to-negative total return through 2016–2020 following new-entrant disruption. |
| 12 | bhartiartl_2018-03-31 | Bharti Airtel | BHARTIARTL | Second vintage, scored deeper into the price-war stretch. |
| 13 | tatasteel_2015-03-31 | Tata Steel | TATASTEEL | Core cyclical steel major; well-documented flat-to-negative multi-year total return through commodity-down-cycle and high-leverage stretches of the mid-to-late 2010s. |
| 14 | tatasteel_2017-03-31 | Tata Steel | TATASTEEL | Second vintage, same thesis. |
| 15 | ntpc_2015-03-31 | NTPC | NTPC | PSU power-generation utility; well-documented range-bound/muted long-run shareholder return, similar in kind to other regulated PSU utilities. |
| 16 | ntpc_2017-03-31 | NTPC | NTPC | Second vintage, same thesis. |
| 17 | tatamotors_2015-03-31 | Tata Motors | TATAMOTORS | Auto major (domestic CV/PV + JLR); well-documented high-volatility, weak long-run equity-holder return driven by JLR capital intensity and cyclicality. |
| 18 | tatamotors_2017-03-31 | Tata Motors | TATAMOTORS | Second vintage, same thesis. |
| 19 | bankbaroda_2015-03-31 | Bank of Baroda | BANKBARODA | PSU bank; well-documented multi-year asset-quality stress (corporate NPA cycle) and weak long-run shareholder return through the mid-to-late 2010s. |
| 20 | bankbaroda_2017-03-31 | Bank of Baroda | BANKBARODA | Second vintage, same thesis. |

### Blow-ups / frauds (pre-registered) — 3 companies, 5 name-dates

| # | Name-date | Company | NSE symbol | Why pre-registered a blow-up |
|---|---|---|---|---|
| 21 | zeel_2017-03-31 | Zee Entertainment Enterprises | ZEEL | Media/broadcast major; well-documented promoter (Essel Group) share-pledge and inter-company-loan governance crisis disclosed from Jan-2019, sharp stock collapse. |
| 22 | zeel_2018-03-31 | Zee Entertainment Enterprises | ZEEL | Second vintage, scored just before the crisis became public — a genuine stress test of whether entry would have triggered into the trap. |
| 23 | relcapital_2016-03-31 | Reliance Capital | RELCAPITAL | Anil Dhirubhai Ambani Group NBFC/holding company; well-documented group-wide debt and governance collapse from 2019, insolvency admission in 2021, promoter control lost. |
| 24 | relcapital_2018-03-31 | Reliance Capital | RELCAPITAL | Second vintage, closer to the collapse. |
| 25 | ilfstransport_2017-03-31 | IL&FS Transportation Networks | ILFSTRANS | IL&FS-group infrastructure-finance arm; well-documented parent-group default and governance collapse disclosed from Sep-2018, with contagion into group listed entities per the associate-contagion criterion (§2.1.6 of `specs/V3_9_DELTA.md`). **Single-dated**: a later (FY18/FY19) scoring date would price the name after the parent-group default was already public and the stock in freefall/trading-suspension territory, which is a different (hindsight-adjacent) test than this document intends to keep clean; FY17 is used instead as the earlier, cleaner pre-crisis vintage. |

## QFV input spec pre-registration (§1.1 of `specs/V3_9_DELTA.md`)

For each name-date, Phase 2/3 must pull, PIT as of the scoring date, the
**trailing 5 audited FYs** feeding the QFV gate below, plus the market-cap
check:

| Name-date | Trailing 5 audited FYs feeding §1.1 | Market-cap check date |
|---|---|---|
| asianpaint_2014-03-31 | FY10, FY11, FY12, FY13, FY14 | 2014-03-31 |
| asianpaint_2016-03-31 | FY12, FY13, FY14, FY15, FY16 | 2016-03-31 |
| hdfcbank_2014-03-31 | FY10, FY11, FY12, FY13, FY14 | 2014-03-31 |
| hdfcbank_2016-03-31 | FY12, FY13, FY14, FY15, FY16 | 2016-03-31 |
| nestleind_2015-03-31 | FY11, FY12, FY13, FY14, FY15 | 2015-03-31 |
| nestleind_2017-03-31 | FY13, FY14, FY15, FY16, FY17 | 2017-03-31 |
| britannia_2015-03-31 | FY11, FY12, FY13, FY14, FY15 | 2015-03-31 |
| britannia_2017-03-31 | FY13, FY14, FY15, FY16, FY17 | 2017-03-31 |
| havells_2014-03-31 | FY10, FY11, FY12, FY13, FY14 | 2014-03-31 |
| havells_2016-03-31 | FY12, FY13, FY14, FY15, FY16 | 2016-03-31 |
| bhartiartl_2016-03-31 | FY12, FY13, FY14, FY15, FY16 | 2016-03-31 |
| bhartiartl_2018-03-31 | FY14, FY15, FY16, FY17, FY18 | 2018-03-31 |
| tatasteel_2015-03-31 | FY11, FY12, FY13, FY14, FY15 | 2015-03-31 |
| tatasteel_2017-03-31 | FY13, FY14, FY15, FY16, FY17 | 2017-03-31 |
| ntpc_2015-03-31 | FY11, FY12, FY13, FY14, FY15 | 2015-03-31 |
| ntpc_2017-03-31 | FY13, FY14, FY15, FY16, FY17 | 2017-03-31 |
| tatamotors_2015-03-31 | FY11, FY12, FY13, FY14, FY15 | 2015-03-31 |
| tatamotors_2017-03-31 | FY13, FY14, FY15, FY16, FY17 | 2017-03-31 |
| bankbaroda_2015-03-31 | FY11, FY12, FY13, FY14, FY15 | 2015-03-31 |
| bankbaroda_2017-03-31 | FY13, FY14, FY15, FY16, FY17 | 2017-03-31 |
| zeel_2017-03-31 | FY13, FY14, FY15, FY16, FY17 | 2017-03-31 |
| zeel_2018-03-31 | FY14, FY15, FY16, FY17, FY18 | 2018-03-31 |
| relcapital_2016-03-31 | FY12, FY13, FY14, FY15, FY16 | 2016-03-31 |
| relcapital_2018-03-31 | FY14, FY15, FY16, FY17, FY18 | 2018-03-31 |
| ilfstransport_2017-03-31 | FY13, FY14, FY15, FY16, FY17 | 2017-03-31 |

Each row states the FY window and check date only — no ROIC, OCF/PAT, D/E,
or market-cap figures have been pulled or computed for any row. That is
Phase 2/3 work, not this session's.

## Governance-event log template pre-registration (§2 of `specs/V3_9_DELTA.md`)

For each of the 13 companies, Phase 3 populates a per-company dated log
using the template below. The log is empty at pre-registration time and is
filled PIT (i.e., only with events whose disclosure date precedes the
relevant scoring/fill date being evaluated) in Phase 3 — this session
defines the template and sources only, per the task instruction.

**Template (one row per qualifying event, one log per company):**

| Event date | Taxonomy tag (§2.1.1–6) | One-line description | Source (BSE/NSE filing or press, with link) |
|---|---|---|---|

**Sources (fixed for all 13 companies' logs):**
- BSE Corporate Announcements (bseindia.com) for the company's own scrip code.
- NSE Corporate Announcements (nseindia.com) for the company's own symbol.
- National business press: Economic Times, Business Standard, Mint,
  Moneycontrol, Reuters India — for the associate-contagion criterion
  (§2.1.6) and for context corroborating a filing-disclosed event.

**Taxonomy tags available (closed list, from `specs/V3_9_DELTA.md` §2.1):**
`regulatory_probe`, `auditor_event`, `promoter_conduct`, `withdrawn_capital_action`,
`criminal_legal`, `associate_contagion`.

**Per-company log files to be created in Phase 3** (empty at this
pre-registration, listed here so the template scope is fixed before any
event is logged):

- `validation/v3_9_oos/governance_logs/asianpaint.md`
- `validation/v3_9_oos/governance_logs/hdfcbank.md`
- `validation/v3_9_oos/governance_logs/nestleind.md`
- `validation/v3_9_oos/governance_logs/britannia.md`
- `validation/v3_9_oos/governance_logs/havells.md`
- `validation/v3_9_oos/governance_logs/bhartiartl.md`
- `validation/v3_9_oos/governance_logs/tatasteel.md`
- `validation/v3_9_oos/governance_logs/ntpc.md`
- `validation/v3_9_oos/governance_logs/tatamotors.md`
- `validation/v3_9_oos/governance_logs/bankbaroda.md`
- `validation/v3_9_oos/governance_logs/zeel.md`
- `validation/v3_9_oos/governance_logs/relcapital.md`
- `validation/v3_9_oos/governance_logs/ilfstransport.md`

No entries have been added to any of the above yet — none of these files
exist in this commit. Their creation and population is Phase 3 work.

## What happens next (not started in this session)

For each of the 25 name-dates above: fetch real EPS, price series,
corporate-action history, and the QFV inputs tabulated above from
primary/vendor sources (no data has been fetched yet — see the commit
timestamp of this file for the freeze point). Populate the governance-event
logs PIT. Apply the FROZEN v3.7 usability test, then the v3.9 entry logic
(QFV / ACC / INV, gated by GEV per `specs/V3_9_DELTA.md`) exactly,
name-date by name-date, with the fired check and reason recorded regardless
of outcome. **No name is added, removed, or re-dated after this point for
any reason**, including a name turning out to need usability exclusion, a
category label turning out wrong once real data is seen, or an inconvenient
result. A second run is a new pre-registration, not a rerun of this one.

No validation, backtest, or fill simulation has been performed against this
set in this session.
