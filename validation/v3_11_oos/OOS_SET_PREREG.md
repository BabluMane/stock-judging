# v3.11 out-of-sample pre-registration — 2026-09-29

**Committed BEFORE any confirmation-run data gathering.** This is the fresh
confirmation set for `specs/V3_11_DELTA.md` (which hardens GEV — new type 7
credit-default recognition — and converts every v3.10 judgment call into a
literal rule). Same valuation machinery as v3.10, better-tested fraud screen:
hard live bar unchanged (0 blow-up fills · ≥ 3 distinct winner names · to-T
positive · 24m ≥ 0.8×), run ONCE, no refit. **v3 is NOT LIVE**; nothing here
describes any company as investable.

**No validation, backtest, usability test, QFV test, GEV evaluation or fill
simulation was run in this session.** The single, narrow exception is the
firewall exception in the delta: the frozen v3.10 valuation construction was
executed on *candidate blow-ups only* to apply the GEV-exercise filter (see
below). It computes fair value and price-vs-fair-value diagnostics; it selects
which names are tested and asserts no outcome. No QFV input, EPS series,
governance-log entry or corporate-action history was used for any winner or
mediocrity name. Category labels are pre-registered from general public market
history; a label that proves wrong once PIT data is gathered is a finding to
report, not a reason to swap a name (per `V3_11_DELTA.md`, any such
observation becomes a v3.12 proposal, never a mid-stream edit).

## Freeze rule

**No name-date is added, removed, or re-dated after this document is
committed, for any reason** — including a usability exclusion, a category
label proving wrong, a data-availability problem, a seeded event proving
wrong (handled by the C4 correction protocol: correct with source + date, log
the real events separately, never swap silently), or an inconvenient result.
A second run is a new pre-registration.

## Construction

- 25 name-dates / 13 companies: **5 winners × 2 dates = 10, 5 mediocrities
  × 2 dates = 10, 3 blow-ups (2+2+1 dates) = 5.**
- **Every scoring date ≥ 2019-03-31** (minimum 2019-03-31; maximum
  2021-03-31, leaving ≥ 24m of forward runway before this commit). 24m windows
  span the COVID stress period.
- **FY-ends: all 13 companies have a 31-March fiscal year-end**; scoring date
  = FY-end of the scoring FY. No non-standard FY-end is in this set. (ABB
  India, a December-FY name, was considered and dropped before freeze: its
  FY-end changed and its free-data history is not a clean 5-FY series. The
  Nestlé lesson is honoured by stating FY-ends explicitly per company.)
- Free data only (screener.in tables and price/PE chart API; BSE/NSE filings;
  rating-agency press releases; national business press). No new API spend.
- Blow-up bucket: all three companies are governance/solvency-collapse
  stories; thin or messy data quality is a feature of the bucket.
- Financial-variant note: `srei` is an NBFC and is expected to take the
  frozen excess-return (financial) variant, as `lvb` did in v3.10.

## Zero-overlap proof (all four prior sets)

Prior sets: in-sample 25 companies / 50 name-dates
(`validation/v3_7/corrected_verdicts_final.json`); v3.8 OOS
(`validation/v3_8_oos/`); v3.9 OOS (`validation/v3_9_oos/`); v3.10 OOS
(`validation/v3_10_oos/`). Membership lists are imported verbatim from
`validation/v3_10_oos/check_disjoint_v310.py`; the v3.11 list is in
`check_disjoint_v311.py` (committed alongside; pure membership check, no data
touched). Overlap is tested at company level (strict) and name-date level.

**Script output (`python3 validation/v3_11_oos/check_disjoint_v311.py`):**

```
prior in-sample: 25 companies / 50 name-dates
  company overlap:   []
  name-date overlap: []
prior v3.8: 13 companies / 25 name-dates
  company overlap:   []
  name-date overlap: []
prior v3.9: 13 companies / 25 name-dates
  company overlap:   []
  name-date overlap: []
prior v3.10: 13 companies / 25 name-dates
  company overlap:   []
  name-date overlap: []
union of prior sets: 64 companies / 125 name-dates
union company overlap:   []
union name-date overlap: []
v3.11: 13 companies / 25 name-dates; min scoring date 2019-03-31
DISJOINT: True
```

## The 25 name-dates

### Winners (pre-registered)

| # | Name-date | Company | NSE symbol | FY-end | One-line thesis for the category |
|---|---|---|---|---|---|
| 1 | tvsmotor_2019-03-31 | TVS Motor Company | TVSMOTOR | 31 Mar | Two-wheeler major; well-documented multi-year share gains and premium/EV-mix-led re-rating. |
| 2 | tvsmotor_2020-03-31 | TVS Motor Company | TVSMOTOR | 31 Mar | Two-wheeler major; well-documented multi-year share gains and premium/EV-mix-led re-rating. |
| 3 | jublfood_2019-03-31 | Jubilant FoodWorks | JUBLFOOD | 31 Mar | Domino's India master franchisee; well-documented store-expansion and delivery-led re-rating. |
| 4 | jublfood_2020-03-31 | Jubilant FoodWorks | JUBLFOOD | 31 Mar | Domino's India master franchisee; well-documented store-expansion and delivery-led re-rating. |
| 5 | tiindia_2020-03-31 | Tube Investments of India | TIINDIA | 31 Mar | Diversified engineering/mobility group; well-documented multi-year re-rating on segment scale-up after the 2020 lows. |
| 6 | tiindia_2021-03-31 | Tube Investments of India | TIINDIA | 31 Mar | Diversified engineering/mobility group; well-documented multi-year re-rating on segment scale-up after the 2020 lows. |
| 7 | kei_2019-03-31 | KEI Industries | KEI | 31 Mar | Cables and wires; well-documented multi-year compounding on volume growth and retail/EHV mix. |
| 8 | kei_2020-03-31 | KEI Industries | KEI | 31 Mar | Cables and wires; well-documented multi-year compounding on volume growth and retail/EHV mix. |
| 9 | pidilite_2019-03-31 | Pidilite Industries | PIDILITIND | 31 Mar | Adhesives/consumer-chemicals leader; well-documented steady multi-year earnings compounding. |
| 10 | pidilite_2021-03-31 | Pidilite Industries | PIDILITIND | 31 Mar | Adhesives/consumer-chemicals leader; well-documented steady multi-year earnings compounding. |

### Mediocrities (pre-registered)

| # | Name-date | Company | NSE symbol | FY-end | One-line thesis for the category |
|---|---|---|---|---|---|
| 11 | emami_2019-03-31 | Emami | EMAMILTD | 31 Mar | Personal-care/wellness; well-documented price de-rating and flat-to-lower multi-year return through 2019-20. |
| 12 | emami_2020-03-31 | Emami | EMAMILTD | 31 Mar | Personal-care/wellness; well-documented price de-rating and flat-to-lower multi-year return through 2019-20. |
| 13 | marico_2019-03-31 | Marico | MARICO | 31 Mar | Coconut-oil/edible-oil FMCG; well-documented range-bound price 2019-21. |
| 14 | marico_2021-03-31 | Marico | MARICO | 31 Mar | Coconut-oil/edible-oil FMCG; well-documented range-bound price 2019-21. |
| 15 | ongc_2019-03-31 | Oil & Natural Gas Corporation | ONGC | 31 Mar | Upstream oil PSU; well-documented flat-to-lower price on crude volatility and subsidy-sharing overhang. |
| 16 | ongc_2021-03-31 | Oil & Natural Gas Corporation | ONGC | 31 Mar | Upstream oil PSU; well-documented flat-to-lower price on crude volatility and subsidy-sharing overhang. |
| 17 | sunpharma_2019-03-31 | Sun Pharmaceutical Industries | SUNPHARMA | 31 Mar | Large pharma; well-documented range-bound price on US generics erosion and regulatory overhang. |
| 18 | sunpharma_2020-03-31 | Sun Pharmaceutical Industries | SUNPHARMA | 31 Mar | Large pharma; well-documented range-bound price on US generics erosion and regulatory overhang. |
| 19 | nhpc_2019-03-31 | NHPC | NHPC | 31 Mar | Regulated hydro PSU; well-documented range-bound shareholder return. |
| 20 | nhpc_2021-03-31 | NHPC | NHPC | 31 Mar | Regulated hydro PSU; well-documented range-bound shareholder return. |

### Blow-ups / frauds (pre-registered)

| # | Name-date | Company | NSE symbol | FY-end | One-line thesis for the category |
|---|---|---|---|---|---|
| 21 | gayatri_2019-03-31 | Gayatri Projects | GAYAPROJ | 31 Mar | Hyderabad EPC/infrastructure contractor; well-documented stretched receivables, CARE downgrade to D on debt-servicing delays (Nov-2019) and prolonged lender defaults; stock collapse. |
| 22 | gayatri_2020-03-31 | Gayatri Projects | GAYAPROJ | 31 Mar | Hyderabad EPC/infrastructure contractor; well-documented stretched receivables, CARE downgrade to D on debt-servicing delays (Nov-2019) and prolonged lender defaults; stock collapse. |
| 23 | sadbhav_2020-03-31 | Sadbhav Engineering | SADBHAV | 31 Mar | Road/infrastructure EPC developer; well-documented liquidity stress, D-rated toll-road subsidiaries and non-cooperating rating status; stock collapse. |
| 24 | sadbhav_2021-03-31 | Sadbhav Engineering | SADBHAV | 31 Mar | Road/infrastructure EPC developer; well-documented liquidity stress, D-rated toll-road subsidiaries and non-cooperating rating status; stock collapse. |
| 25 | srei_2020-03-31 | Srei Infrastructure Finance | SREINFRA | 31 Mar | Infrastructure/equipment NBFC; well-documented rating slide to default category (early 2021) and RBI board supersession plus NCLT insolvency (Oct-2021). Single-dated. |

## Blow-up dated governance events inside 24m windows

Requirement: ≥ 2 blow-up name-dates with dated governance events inside the
24-month window after the scoring date. Seeded candidate events come from
public record in the free sources named (rating-agency press releases, SEBI/RBI
material, national business press), at the precision stated, and are **not yet
verified PIT**; the validation session must source and date each from BSE/NSE
filings or rating-agency/SEBI/RBI documents and press per the fallback
hierarchy below. A wrong seed is corrected per C4, never swapped. The freeze
covers name-dates, not these event dates.

| Name-date | 24m window | Seeded dated events (tag) |
|---|---|---|
| gayatri_2019-03-31 | 2019-04-01 → 2021-03-31 | ~2019-11-15 CARE press release: BB+ → **D** on delays in debt servicing (type 7); ~Mar-2021 further rating action citing debt-servicing delays (type 7 only if D — to verify) |
| gayatri_2020-03-31 | 2020-04-01 → 2022-03-31 | ~Mar-2021 rating action on debt-servicing delays (type 7 only if D — to verify). The Nov-2019 D pre-dates this scoring date: PIT-known at scoring, logged, not counted toward the ≥ 2 requirement |
| sadbhav_2020-03-31 | 2020-04-01 → 2022-03-31 | No in-window type-7 seed established. Jun-2019 CARE D on wholly-owned subsidiary Rohtak-Hissar Tollway is PIT-known at scoring (type 7 via consolidated group): logged, not counted. Mar-2020 CARE and Jul-2021 India Ratings actions stayed above D and do NOT count |
| sadbhav_2021-03-31 | 2021-04-01 → 2023-03-31 | Sep-2022 CARE "issuer not co-operating" tag does NOT count standing alone. Jun-2019 subsidiary D is history: logged, not counted |
| srei_2020-03-31 | 2020-04-01 → 2022-03-31 | ~early-2021 CARE and Acuité downgrades to default category (type 7); 2021-10-04 RBI supersedes the boards of Srei Infrastructure Finance and Srei Equipment Finance citing governance concerns and payment defaults (`regulatory_probe`); 2021-10-08 NCLT admits insolvency (tag to be settled) |

Requirement met on seeded events by gayatri_2019 and srei_2020 (two name-dates
with dated events inside their windows), with gayatri_2020 a possible third
if the Mar-2021 action verifies. If the validation session cannot date events
for at least two, that is reported as a finding, not fixed by swapping names.

## GEV-exercise filter (per `specs/V3_11_DELTA.md`, new rule)

**Purpose.** The v3.10 set under-tested GEV: four of five blow-up name-dates
were stopped by negative fair value or usability before GEV was evaluated.
Blow-up name-dates are therefore chosen where the frozen v3.10 valuation would
plausibly produce a fill, so GEV — not valuation or usability — must be the
stopping mechanism.

**Firewall.** `gev_exercise_filter.py` (committed) imports the frozen v3.10
valuation functions unmodified and computes fair value/share plus
price-vs-fair-value only. It runs no usability, QFV, GEV or fill logic and
asserts no outcome. Data were fetched to a scratch directory outside the repo
(screener.in) and are not committed; only the filter result table
(`gev_exercise_filter_results.json`) is.

**Filter rule (fixed before candidates were screened).** A candidate
name-date PASSES iff fair value/share > 0 AND the minimum weekly close in the
24m window ≤ 1.10 × the ACC trigger (0.875 × FV; the QFV tier is not
evaluated). The "first close ≤ 0.875·FV" date is a diagnostic only, not a fill.
Filter-only assumption: beta 1.15 for every candidate; the validation session
fixes its own betas before any run.

**Candidate pool.** 28 blow-up candidates, scoring dates 2019–2023 where
screener data permitted: SREI, Religare, Reliance Infra, Reliance Power, Rolta,
Jaiprakash Associates, Fortis, RCom, Eros, Suzlon, Unitech, Ballarpur, HDIL,
Reliance Home Finance, Sintex, Dish TV, Sadbhav Engg, Gayatri Projects, Aban,
GTL Infra, McLeod Russel, Parsvnath, Educomp, KSK, IFCI, Kohinoor, Jyoti
Structures, Punj Lloyd. Most fail on non-positive FV (leveraged balance
sheets) or lack a scoring-FY column — the same fact that explains v3.10's
result. Full table: `gev_exercise_filter_results.json`. Passed but not
selected: Eros 2019, HDIL 2019 (weekly-close touch precedes the seeded
insolvency/PMC events), Reliance Home Finance 2019 (touch precedes its Jul-2019
D; also a Reliance Capital (v3.9) subsidiary — group contagion), Dish TV
(category label weak: not a collapse), Gayatri 2021/2022 (two-date limit per
company), and degenerate-FV artefacts (Religare 2023, RHFL 2023), discarded.

**Selected blow-up name-dates (filter diagnostics; not outcomes):**

| Name-date | Model | FV/share | Price@d0 | P/FV@d0 | Min close/FV (24m) | First close ≤ 0.875·FV | Filter |
|---|---|---|---|---|---|---|---|
| gayatri_2019-03-31 | DCF | 72.1 | 159.55 | 2.21 | 0.119 | 2019-11-22 | **PASS** |
| gayatri_2020-03-31 | DCF | 36.8 | 8.55 | 0.23 | 0.247 | 2020-04-03 | **PASS** |
| sadbhav_2020-03-31 | DCF | 604.7 | 29.65 | 0.05 | 0.041 | 2020-04-03 | **PASS** |
| sadbhav_2021-03-31 | DCF | 220.7 | 62.10 | 0.28 | 0.039 | 2021-04-01 | **PASS** |
| srei_2020-03-31 | ER | 29.4 | 3.90 | 0.13 | 0.128 | 2020-04-03 | **PASS** |

Stated plainly, so the set is not misread as engineered to pass:

- **gayatri_2019**: price at scoring is above FV; the first weekly close at/below
  the ACC trigger falls on 2019-11-22 — after the seeded Nov-2019 CARE D. If the
  event verifies, this is the case where GEV at the fill date, not valuation,
  must stop the fill.
- **gayatri_2020, sadbhav_2020, sadbhav_2021**: the trigger is touched at the
  start of the window; the seeded D events pre-date scoring, so the mechanism
  under test is the scoring-date veto and the §2.3 cooling-off clock (event+365d
  or first annual results print). Sadbhav's D is on a wholly-owned subsidiary —
  it exercises the "company or its consolidated group" clause of type 7.
  Sadbhav FV is inflated by the 15% growth cap; the frozen formula is not
  altered.
- **srei_2020**: the trigger is touched at the start of the window, **before**
  the seeded early-2021 D. If no earlier qualifying event is found PIT, GEV
  cannot prevent a fill and it would count against the live bar. Retained
  deliberately as an honest test; no outcome is asserted.
- Event-vs-touch timing above uses month/day-precision seeds and weekly vendor
  closes; the validation session's PIT log is authoritative.

## QFV input windows (frozen; `specs/V3_9_DELTA.md` §1.1, untouched)

Per name-date, pull PIT the **trailing 5 audited FYs** and the market-cap
check. Window = FY(N−4) … FY(N) for scoring date 31-Mar-N. If fewer than 5
audited FYs exist, the available audited FYs are used and the shortfall
recorded — never substituted. v3.10 additionally needs ROE_avg3 and
scoring-FY Dividend Payout % from the same window; no new window is added.

| Name-date | Trailing 5 audited FYs | Market-cap check date |
|---|---|---|
| tvsmotor_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| tvsmotor_2020-03-31 | FY16, FY17, FY18, FY19, FY20 | 2020-03-31 |
| jublfood_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| jublfood_2020-03-31 | FY16, FY17, FY18, FY19, FY20 | 2020-03-31 |
| tiindia_2020-03-31 | FY16, FY17, FY18, FY19, FY20 | 2020-03-31 |
| tiindia_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| kei_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| kei_2020-03-31 | FY16, FY17, FY18, FY19, FY20 | 2020-03-31 |
| pidilite_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| pidilite_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| emami_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| emami_2020-03-31 | FY16, FY17, FY18, FY19, FY20 | 2020-03-31 |
| marico_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| marico_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| ongc_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| ongc_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| sunpharma_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| sunpharma_2020-03-31 | FY16, FY17, FY18, FY19, FY20 | 2020-03-31 |
| nhpc_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| nhpc_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| gayatri_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| gayatri_2020-03-31 | FY16, FY17, FY18, FY19, FY20 | 2020-03-31 |
| sadbhav_2020-03-31 | FY16, FY17, FY18, FY19, FY20 | 2020-03-31 |
| sadbhav_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| srei_2020-03-31 | FY16, FY17, FY18, FY19, FY20 | 2020-03-31 |

Only FY windows and dates are stated. `srei` is expected financial-variant
(QFV gate not defined for bank/NBFC balance sheets; ACC/INV only, unchanged).

## Governance-event log template (frozen)

One log per company, populated PIT in the validation session (only events
disclosed before the scoring/fill date under evaluation count toward that
evaluation). This session defines the template and sources only; **all logs
are empty at this commit and no log file exists.**

```
# <company> governance log (PIT; empty at pre-registration)

## Qualifying events

| Event date | Taxonomy tag | One-line description | Source (link) | Source tier / WEAK-SOURCE |
|---|---|---|---|---|

## Fallback-use log (C3)

| Date | What fell back | Source used | Why |
|---|---|---|---|

## Seeded-event corrections (C4)

| Seeded claim | Correct fact + date | Source | Real events logged above? |
|---|---|---|---|
```

**Sources (fixed, in order — `V3_11_DELTA.md` C3 fallback hierarchy):**

1. BSE Corporate Announcements (company's scrip code) and NSE Corporate
   Announcements (own symbol) — first source for every event.
2. Fallback: SEBI orders, RBI press releases and rating-agency press releases
   (CARE, ICRA, CRISIL, India Ratings, Acuité, Brickwork) — mandatory source
   for type 7; the agency press-release date is the event date and the
   earliest D across agencies wins.
3. Fallback: national business press (Economic Times, Business Standard, Mint,
   Moneycontrol, Reuters India) for corroboration and associate contagion;
   mark WEAK-SOURCE where a primary document cannot be located.

Every fallback use is logged with source + date (C3). Corporate actions:
Screener → exchange filings → Yahoo public split feed, documented per use.

**Tags (closed list, `V3_9_DELTA.md` §2.1 as extended by `V3_11_DELTA.md` C1):**
`regulatory_probe` (1), `auditor_event` (2), `promoter_conduct` (3),
`withdrawn_capital_action` (4), `criminal_legal` (5), `associate_contagion`
(6), **`credit_default_recognition` (7)** — downgrade to D / default rating
(CARE D, ICRA D, CRISIL D, IND D) of any rated facility of the company or its
consolidated group by a SEBI-registered agency citing missed/delayed debt
servicing. Does NOT count: outlook/watch changes; downgrades staying above D;
withdrawal without default rationale; "issuer not co-operating" alone. Veto
window §2.2, cooling-off §2.3 and precedence §2.4 unchanged. (The runner's
`TAGS` set must add tag 7 — a runner task, not a spec change.)

Log files to be created in the validation session (none exist at this commit):

- `validation/v3_11_oos/governance_logs/tvsmotor.md`
- `validation/v3_11_oos/governance_logs/jublfood.md`
- `validation/v3_11_oos/governance_logs/tiindia.md`
- `validation/v3_11_oos/governance_logs/kei.md`
- `validation/v3_11_oos/governance_logs/pidilite.md`
- `validation/v3_11_oos/governance_logs/emami.md`
- `validation/v3_11_oos/governance_logs/marico.md`
- `validation/v3_11_oos/governance_logs/ongc.md`
- `validation/v3_11_oos/governance_logs/sunpharma.md`
- `validation/v3_11_oos/governance_logs/nhpc.md`
- `validation/v3_11_oos/governance_logs/gayatri.md`
- `validation/v3_11_oos/governance_logs/sadbhav.md`
- `validation/v3_11_oos/governance_logs/srei.md`

## Runner obligations carried from `V3_11_DELTA.md` (not started)

C5: GEV is evaluated before fill-eligibility early-returns (reporting-only;
must not change any fill outcome). C2: runner docstring references
`V3_11_DELTA.md`, not inline C1–C10. Data + logs + runner committed before the
result commit. One locked run.

## What happens next (not started)

Fetch EPS, price, corporate-action and QFV inputs; populate logs PIT; apply the
frozen usability test, the v3.10 valuation and entry logic (QFV / ACC / INV
gated by GEV incl. type 7), name-date by name-date, recording the fired check
and reason regardless of outcome. The freeze rule above applies throughout.
