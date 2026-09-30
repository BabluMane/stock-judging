# v4 out-of-sample pre-registration (Phase C) — 2026-09-30

## STATUS: VOID at pre-registration (V4_SPEC §8.2 void rule)

**Five blow-up name-dates could not be certified on the three §8.2 pre-conditions.
Per §8.2, "the run does not proceed — it is VOID, not weakened, not reinterpreted, not
'underpowered but counted.'" No v4 OOS set is frozen by this document and no locked run
may proceed on anything recorded here.** Nothing here describes any company as investable;
the system is NOT LIVE.

This document follows `engine_v4/V4_SPEC.md` (frozen; SHA-256 below) and the §8.4 section order
(file name `V4_OOS_PREREG.md` per the Phase-C task; the spec's own name is `OOS_SET_PREREG.md`).
No §8.2 condition was weakened, reinterpreted or amended. No validation, backtest, distress
screen, usability check, event-lane evaluation, exit scan, fill simulation or aggregation was
run in this session. The single exception is the firewall exception (§3 below): the frozen
`engine_v4.anchor` was run on candidate blow-up name-dates solely to test `P_d0 ≤ 2.0 × P_G1`.

Two honest caveats up front, because they bear on how far the VOID can be trusted:

1. The research behind the event tapes used a US-only web-search tool. Business Standard, PIB and
   SEBI order-listing pages returned 403 to fetch; there was no access to the NSE/BSE announcement
   archives, IBBI/NCLT lists, SEBI order databases or rating-agency default lists. Evidence below is
   tagged **[V]** (seen by this session in a retrieved search result) or **[A]** (reported by a
   delegated research sub-agent with a source URL; the page was not re-fetched here). A VOID that
   rests on thin search is a statement about *reachable evidence*, not proof that no certifiable
   set exists. A future pre-reg with proper sources may find one.
2. One near-miss I initially read as a failure (Simplex) is **not** established as one — see §3.

---

## 1. Frozen rules hash

| Item | Value |
|---|---|
| Spec file | `engine_v4/V4_SPEC.md` |
| Spec SHA-256 (computed this session) | `6acb4acdcb7f93a042df36d4eb111bcca5dfa38d894864ec13d269096f2be671` |
| Pin in `engine_v4/tests/test_constants.py` (`SPEC_SHA256`) | `6acb4acdcb7f93a042df36d4eb111bcca5dfa38d894864ec13d269096f2be671` — **match** (checked before any work; a mismatch would have stopped the session) |
| Base commit (branch cut from `main` at) | `efbc934ce89e20285d81bb5038237e2c0cda3cde` (merge of PR #11, `claude/v4-build`) |
| `engine_v4/` tree at base | `6ea7e7a1de50ccfaccd466a4e1f402efbd3ebbe3` (`git rev-parse efbc934:engine_v4`) |
| `validation/v4_oos/fill_plausibility_firewall.py` SHA-256 | `84e0dbd5fbe6c4b8a73138c02db0836e97796b9484df189c67aa8d650e8ae64d` |
| `validation/v4_oos/fill_plausibility_results.json` SHA-256 | `00d33b06c296f0c426bc74e3bf82d1703f7eb993df39ed277c6e48f71db4b3e3` |
| `validation/v4_oos/check_disjoint_v4.py` SHA-256 | `0e57b796c9a5935d662bf88b667c575bb043847efc9347da935fc8dd45f11d39` |
| Set manifest hash | **none — no set is frozen** |

The pre-registration commit is the commit that first adds this file
(`git log --diff-filter=A --format=%H -- validation/v4_oos/V4_OOS_PREREG.md`); a document cannot
contain its own commit hash. The auditor verifies the hashes above with `sha256sum`.

## 2. Set composition (§8.1) — no set frozen

The spec shape (25 name-dates / 13 companies: 5 winners × 2, 5 mediocre × 2, 3 blow-up companies
totalling 5 name-dates as 2+2+1; March 31 scoring dates, all ≥ 2019-03-31) is **unchanged and
not met**. Scoring-date window for this session was set by the Phase-C task to 2019-03-31 …
2021-03-31 (a subset of the spec's "vintage years 2019–2022"; see §10-1).

- **Blow-up side:** 0 of 5 name-dates certified (§3).
- **Winners and mediocrities: deliberately NOT pre-registered.** A frozen name-date cannot be
  added, removed or re-dated (§8.1 freeze), and §8.2 makes the whole run void when the decisional
  set is short; freezing 20 non-blow-up name-dates around a void decisional set would only burn
  names for the fresh set the void rule requires (§8.2: "a new pre-reg + a new set"). No data of any
  kind was fetched for any winner or mediocre candidate.
- **Freeze rule:** nothing is frozen, so nothing is bound. The candidates named in this document are
  *examined* names, not set members. A later pre-reg must account for the fact that their tier-1
  anchor triggers were computed here (firewall-permitted for blow-ups; it asserts no outcome).
  Any future pre-reg carries its own freeze rule from the moment of its commit.

## 3. Decisional test set (§8.2) — certification attempt: 0 of 5

### 3.1 Conditions and how each was (and was not) evaluated

1. **Usable (post-v4-usability).** Requires a recorded usability verdict per name-date. **Not
   evaluated for any candidate:** the task firewall forbids running usability for selection, and
   this session did not read any candidate's EPS sign, EPS series or corporate-action history. The
   U1–U3 checks (`engine_v4/usability.py`) were not run. Condition 1 is therefore *uncertified for
   every candidate*. (Open tension: §8.2 wants this verdict pre-run, the task firewall bars running
   the check to get it. I followed the stricter firewall; it is flagged for Bablu in §10-2.)
2. **Fill-plausible: `P_d0 ≤ 2.0 × P_G1`.** Computed with the frozen `engine_v4.anchor.value_anchor`
   via `fill_plausibility_firewall.py` — only `P_d0` (last adjusted close at or before d0) and
   `P_G1 = V(g_h(0.875))` are emitted; `g_implied` and the other `value_anchor` outputs are
   dropped. Full table: `fill_plausibility_results.json` (171 name-dates). Conventions: shares =
   screener Market Cap ÷ Current Price; scoring FY = `pit.select_scoring_fy` with *nominal*
   `results_published` = FY-end + 60 days (screener has no publication dates), which for 31-Mar-N
   selects FY(N−1); β = 1.15 uniform (blow-up bucket, carried V310-C9); class split by screener
   Broad Industry ∈ {Banks, Finance} (see §10-3). Result across the pool: 46 plausible, 96 not
   plausible (of which 23 companies have non-positive `P_G1` on all three dates), 29 not computable
   (no screener table, or no close within 10 days of d0).
3. **Pre-flag-risk.** `scoring + 6m ≤ E1 ≤ scoring + 24m`, E1 = the first qualifying §5.1
   (T1–T7) event date. Read literally as the first qualifying event on the name's tape: a qualifying
   event dated **before d0** therefore fails the condition for that date (the spec's gloss is
   "scoring precedes the first flag by ≥6 months"). This reading was not relaxed. (Whether E1 should
   instead mean "first qualifying event after d0" is a spec-level question, §10-4; it was **not**
   applied.)

### 3.2 Search methodology and sources

- **Candidate generation:** my own list of 57 listed March-FY blow-up candidates (excluding every
  company in the five prior sets), plus names surfaced by two parallel web-research passes (one per
  vintage window) that were told to exclude the prior 77 companies and to search for a clean record
  before E1. Tool limits are in the caveats above. The passes returned 0 candidates meeting the
  full bar (vintage 2019: four names, none high-confidence; vintage 2020/21: none).
- **Firewall:** run on all 57 symbols × {2019, 2020, 2021}-03-31 (171 name-dates); see
  `fill_plausibility_results.json`. It was used to test condition 2 only. (A first pass used an
  earlier revision of the script whose only difference was the financial-class detection; the
  committed results are from the final script.)
- **Event evidence:** exchange filings and agency documents were not reachable; evidence is news
  and search snippets, hence WEAK-SOURCE in §5.1 terms for anything tagged [V]/[A] below.

### 3.3 Per-candidate dated evidence (every named near-miss and open lead)

Legend: d0 = scoring date; "window" = [d0+6m, d0+24m]; P-ratio = `P_d0 / P_G1` (≤ 2.0 passes).

| Candidate (NSE) | d0 tried | P-ratio (cond. 2) | Earliest qualifying event found (date · type · source) | §8.2 condition failed / status |
|---|---|---|---|---|
| **Eros International Media** (EROSMEDIA) | 2019-03-31 | 0.197 ✓ | 2019-06-05 · T7: CARE cut long- and short-term bank facilities from BBB−/A3 to **D** for debt-servicing delay · **[V]** BusinessToday "Flop show…18 straight sessions"; Business Standard "Eros International slumps after CARE downgrades ratings" (2019-06-06) | **Cond. 3 FAILS:** E1 ≤ 2019-06-05 < window start 2019-09-30 |
| | 2020-03-31 | 0.020 ✓ | same event | **Cond. 3 FAILS:** E1 precedes d0 |
| | 2021-03-31 | n/a (P_G1 < 0) | — | Cond. 2 FAILS |
| **Cox & Kings** (screener `COX&KINGS`) | 2019-03-31 | 0.202 ✓ | CARE downgrade 2019-06-17; BWR to D 2019-06-28; CARE to D 2019-07-11 (T7) · **[A]** Business Standard PTI 2019-07-11 (page 403 to fetch) | **Cond. 3 FAILS:** E1 ≤ 2019-07-11 < 2019-09-30 |
| | 2020-03-31 | 0.001 ✓ | same events | **Cond. 3 FAILS:** E1 precedes d0 |
| | 2021-03-31 | n/a (P_G1 < 0) | — | Cond. 2 FAILS |
| **HDIL** | 2019-03-31 | **2.582 ✗** | 2013-03-20 · T7: CARE cut NCDs to D · **[A]** Business Standard/Reuters; 2019-09-30 · T5 named FIR on promoters (PMC Bank), arrests 2019-10-03 · **[A]** | **Cond. 2 FAILS** (P-ratio > 2.0) **and cond. 3 FAILS** (2013 D precedes d0; the 2019-09-30 FIR sits exactly on the window boundary but is not E1) |
| | 2020-03-31, 2021-03-31 | 0.027 / 0.100 ✓ (scoring FY shown as FY2019 in both — filing gap, see results) | events precede d0 | **Cond. 3 FAILS** |
| **McLeod Russel India** | 2019, 2020, 2021 | n/a — P_G1 < 0 on all three dates | 2019-06-12 · T3(b) lenders begin invoking pledged shares · **[A]** Business Standard; 2019-07-04 · T7 ICRA to D · **[A]** Business Standard/ANI | **Cond. 2 FAILS** (non-positive trigger) on every date; also cond. 3 (events < 2019-09-30 and pre-d0 thereafter) |
| **Simplex Infrastructures** (SIMPLEXINF) | 2019-03-31 | 0.641 ✓ | **E1 not established.** 2019-06-11/12: CARE revised *outlook* to negative, rating unchanged at A− (not a §5.1 event) · **[V]** Business Standard; 2019-11-25: CARE cut NCDs BBB → BB+ (not D; not T7) · **[V]** search summary. Later: CARE D (date not found), qualified audit opinion (year not established), two independent directors (incl. audit-committee chair) resigned Feb-2021 (directors ≠ auditor; not a §5.1 event) · **[V]** search summary | **Cond. 3 UNCERTIFIED** (no dated E1 evidence reachable). *Not* shown to fail. Cond. 1 unevaluated |
| | 2020-03-31 | 0.060 ✓ | as above | Cond. 3 UNCERTIFIED (would need E1 ≥ 2020-09-30 and nothing qualifying earlier; a FY2019-20 qualified opinion or default dated before that would fail it) |
| | 2021-03-31 | n/a (P_G1 < 0) | — | Cond. 2 FAILS |
| **Sintex Industries** | 2019, 2020, 2021 | n/a — P_G1 < 0 on all three | June-2019 NCD default / CARE non-cooperating · **[A]** | Cond. 2 FAILS on every date |
| **Thomas Cook (India)** | 2019-03-31 | 0.390 ✓ | 2020-09-28 · T4 board withdrew the Rs 150 cr buyback approved 2020-02-26 · **[A]** Business Standard | **Open lead.** Inside window; nothing earlier found **[A]**, not verified; cond. 1 unevaluated. The withdrawal was COVID-driven and the collapse was a demand shock, not a governance/solvency failure — a §8.1 category question ("well-documented distress"), not decided here |
| | 2020-03-31 | 0.110 ✓ | same | **Cond. 3 FAILS:** E1 = 2020-09-28 is two days before window start 2020-09-30 |
| **Dhani Services** (ex-Indiabulls Ventures; Finance class) | 2020-03-31 | 0.587 ✓ | 2021-05 · T1 SEBI adjudication penalty on the company · **[A]** from a search summary of the FY22 annual report — unverified | **Open lead, unverified:** E1 unverified; earlier Indiabulls-group scrutiny (Sept-2019 Delhi HC PIL notices to SEBI/MCA/SFIO, Indiabulls Housing) not ruled out as T6; cond. 1 unevaluated; realized-price profile did not fall below the Mar-2020 level **[A]** (category question) |
| | 2021-03-31 | 0.001 ✓ | May-2021 penalty precedes window start 2021-09-30 | **Cond. 3 FAILS** (if the date is right) |
| **PNB Housing Finance** | 2020-03-31 | 0.214 ✓ | 2021-06 · SEBI halts the Carlyle preferential-allotment deal · **[A]** | **Weak lead:** whether a SEBI direction of this kind is a §5.1 T1 instrument naming the company is unverified; the later price path was not a collapse **[A]** |
| **Talwalkars Better Value Fitness** | 2019-03-31 | 3.235 ✗ | 2019-08-28 · T2(a) auditor resigned · **[V]** Business Standard headline | Cond. 2 FAILS; cond. 3 FAILS (< 2019-09-30). 2020/2021: scoring FY shown as FY2018 (filing gap) |
| **Eveready Industries** | 2019-03-31 | 0.626 ✓ | 2019-07-01 · T2(a) PwC resigned · **[V]** Business Standard headline | **Cond. 3 FAILS** (< 2019-09-30); not a solvency collapse |
| **Indiabulls Housing Finance** | — | no screener table under `IBULHSGFIN` (renamed Sammaan Capital) | Delhi HC PIL notices 2019-09-27 (court-directed, not a named regulator instrument); ED case April 2021, raids Feb 2022 · **[A]** | Not computable here; E1 unresolved **[A]** |
| **Jain Irrigation Systems** | — | no close within 10d of d0 under `JISLJALEQS` | S&P (not a SEBI-registered agency) to D 2020-03-05 · **[A]** | Not a T7 event; not computable |
| Others in the pool (Kwality 2019: 0.022 ✓; Sical Logistics, Nitesh Estates: P_G1 < 0; RHFL, IFCI, Religare, Union Bank and ~40 more) | see results JSON | see results JSON | — | Not pursued: each either failed cond. 2 or had events dated before any workable window on the evidence reached (e.g. Kwality: CBI case 2020-09-21 **[A]**, defaults from 2018; RHFL: D in Jul-2019 **[A]**) |

### 3.4 Why the set cannot be assembled on this evidence

- Condition 3 removes almost every textbook blow-up: the famous names are in the five prior sets
  (Yes Bank, DHFL, Reliance Capital, Srei, Future Retail, PC Jeweller, Coffee Day, Sadbhav, Gayatri,
  Zee, IL&FS Transportation, CG Power, …) and nearly all the rest carry a qualifying event dated
  2018–mid-2019 (the near-misses above).
- Condition 2 removes most of the rest: 23 of 57 candidate companies have a non-positive tier-1
  trigger on all three dates (leveraged balance sheets).
- **Shape:** a company can only carry two name-dates if a single E1 falls in both windows, i.e.
  consecutive dates with E1 in a six-month band — [d2 + 6m, d1 + 24m]. On the evidence gathered,
  only Simplex is a candidate for that, and even it is uncertified. The 2+2+1 shape needs two such
  companies, so it cannot be met from the leads above even if every open item resolved favourably.
- Conditions not evaluated (usability for everyone; unverified [A] dates) mean every statement
  above is at best "not certifiable on reachable evidence".

### 3.5 Restated from the spec (verbatim)

> **Exercise condition:** genuine exercise of the distress screen requires decisional on **≥3** of
> the 5 name-dates (= §1 leg (a′)).
> **Void rule:** if the pre-reg set cannot supply 5 name-dates meeting all three pre-conditions
> (certified pre-run), **the run does not proceed — it is VOID**, not weakened, not reinterpreted,
> not "underpowered but counted." If the run proceeds and the screen is decisional on <3, the
> blow-up leg is recorded as **UNTESTED** and the run is VOID — an unexercised 0 is not a PASS of
> leg (a). Both cases require a new pre-reg + a new set (fresh zero-overlap vs all six prior sets,
> §8.3).

## 4. Overlap proof (§8.3)

Because no v4 set is frozen, `check_disjoint_v4.py` verifies the **candidate pool** (57 companies /
171 name-dates in `fill_plausibility_results.json`) against the five prior sets; it inherits the
prior lists **by import** (`check_disjoint_v311` → `check_disjoint_v310`), retyping nothing, and
states that the §8.3 25/13 shape assertion is not applicable. Company identity: the `co()`
convention (token before the last underscore), lower-cased screener symbol, `&` → `and`. Renamed /
demerged tickers checked against prior companies: Dhani Services (ex-Indiabulls Ventures),
Reliance Home Finance / Reliance Infra / Reliance Power (distinct legal entities from `relcapital`),
Future Lifestyle Fashions and Future Enterprises (distinct from `fretail`), Sammaan Capital
(ex-Indiabulls Housing): none maps to a prior company.

Verbatim output of `python3 validation/v4_oos/check_disjoint_v4.py`:

```
v4 frozen set: NONE (VOID per V4_SPEC s8.2; s8.3 25/13 shape assertion not applicable)
candidates examined: 57 companies / 171 name-dates; scoring dates 2019-03-31 .. 2021-03-31
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
prior v3.11: 13 companies / 25 name-dates
  company overlap:   []
  name-date overlap: []
union of prior sets: 77 companies / 150 name-dates
union company overlap:   []
union name-date overlap: []
DISJOINT: True
```

`DISJOINT: True` here attests that no examined candidate overlaps a prior set. It is **not** the
§8.3 gate ("the locked run may not start unless DISJOINT: True is on record") for a v4 set, because
there is no set; a future pre-reg must produce its own.

## 5. Data / runner / log commit order

No data, runner, log or result JSON exists for a run. Committed here, additions only under
`validation/v4_oos/`: this document; `fill_plausibility_firewall.py` and its result table (inputs
were fetched to a scratch directory outside the repo and are not committed); `check_disjoint_v4.py`.
No event logs exist (templates in §7 are empty). A future run commits data → runner → logs before
any result JSON.

## 6. Audit checklist

- [ ] Spec SHA-256 equals the §1 value and the `test_constants.py` pin.
- [ ] Frozen-tree diff empty: `git diff efbc934 HEAD -- engine engine_v4 specs validation/v3_6 validation/v3_7 validation/v3_8_oos validation/v3_9_oos validation/v3_10_oos validation/v3_11_oos` prints nothing (`cross_engine/` does not exist in this repo).
- [ ] Only files under `validation/v4_oos/` were added.
- [ ] `check_disjoint_v4.py` re-run independently reproduces the §4 output.
- [ ] `fill_plausibility_firewall.py` imports only `engine_v4.anchor`/`constants`/`pit` and emits only the `OUT_FIELDS`; no distress/usability/events/run/aggregate module is imported; no forward price (> d0) enters any emitted number.
- [ ] No result JSON containing fills, vetoes, exits or aggregates exists anywhere in the change.
- [ ] Every evidence row in §3.3 tagged [A] is re-verified from an exchange filing or agency document before anything builds on it.

## 7. Phase-D input specifications and templates (for a future frozen set)

No name-date is frozen, so these are **not bound to any name-date**. They are the per-name-date
templates the task asked for, written so a future pre-reg can instantiate them verbatim. They
assert nothing about any company.

### 7.1 Distress-screen input spec (§3; 63-day PIT rule)

For d0 = 31-Mar-N, the scoring FY is the latest FY whose results were published ≥ 63 days before
d0 (cutoff 27-Jan-N); in the normal case that is FY(N−1) (FY-end 31-Mar-(N−1), results by
~30-May-(N−1)). A name that filed FY(N−1) after 27-Jan-N falls back to FY(N−2) — a per-name-date
verification item against the **BSE/NSE results filing date**, not screener.

| Rule | Inputs | Audited FY / quarter vintage | Source (free) |
|---|---|---|---|
| D1 pledge level | % of promoter holding pledged | most recent reported shareholding quarter ≤ d0 | BSE/NSE shareholding-pattern filings (LODR Reg 31); Takeover-Reg 31 encumbrance disclosures |
| D2 first-time pledge | pledged % for the 8 quarters before the scoring quarter, and the scoring quarter | 8 (min 4) quarters back from the scoring quarter | same |
| D3 Altman Z'' (non-fin.) | CA, CL (AR PDF), Reserves, Total Assets, PBT, Interest, Depreciation, Share Capital | scoring FY | screener P&L / balance sheet; **CA/CL split from the AR PDF** (BSE announcements / company IR) |
| D4 Piotroski F (non-fin.) | 9 criteria on scoring FY vs prior FY (both ≥ 63d-published); CA/CL from AR; corporate-action history for F_EQ | FY(N−1) and FY(N−2) | screener; AR PDFs; corp-action feed |
| D5 crash veto | adjusted closes, trailing 52 weeks to d0 | price through d0 only | screener chart price series |
| D6 CAMEL (Banks/Finance) | CAR, GNPA, cost-to-income, ROA, CASA (banks) or leverage (NBFC/HFC) | scoring FY | screener ratios / AR |

Class split: screener **Broad Industry** ∈ {Banks, Finance} → D6; otherwise D3+D4 (§10-3). Missing
required input ⇒ UNCOMPUTABLE-DATA (VETOED-DATA), never a silent pass.

**Data-depth findings (2026-09-30 fetches) that a future pre-reg must plan for:** the public screener
page lists only the most recent 12 shareholding quarters (Sep-2023 … Jun-2026 for the page sampled),
so D1/D2 for any 2019–2021 d0 must come from BSE/NSE filings; the screener P&L/balance sheet starts
at Mar-2015, so a 2019 d0 (scoring FY2018) has a 4-FY trailing window (the spec's ≥3-point OPM rule
and C4 ROE rule still apply); some names have no screener table under the historical symbol
(renamed or delisted: e.g. Indiabulls Housing, Reliance Naval, Lanco, Ricoh India).

### 7.2 Usability input spec (§4)

- **EPS series:** screener chart API `Price to Earning – Median PE – EPS` ("EPS" = publication-dated
  TTM EPS, unlagged), on the same consolidated/standalone basis as the chosen P&L (consolidated if
  it parses with a Net Profit row, else standalone — the v3.11 uniform variant rule).
- **Audited FY EPS:** screener P&L "EPS in Rs" row, same basis, scoring FY(N−1) per §4 U2/U3; the
  independent audited series (AR PDF) for the U1 audited÷sourced ratio report.
- **Corporate-action history:** Yahoo chart-events feed (splits and bonuses, reported alike as split
  events), cross-checked against BSE/NSE corporate actions; documented per use.
- **Checks:** U1 basis assertion (named basis: vendor post-action series) → U2 non-positive sourced
  FY EPS ⇒ VETOED-DATA → U3 results-week..+21d median vs audited FY EPS, ±15 % (first publication in
  [Mar 31, Aug 31] with the >10 %-jump skip rule). Check (b) and the financial-variant exemption do not
  exist (§10).

### 7.3 Event-log template (§5; empty at pre-registration)

One log per company, filled point-in-time in Phase D (only events disclosed on or before the
evaluation date count for that evaluation). All logs are **empty** here.

```
# <company> event log (PIT; empty at pre-registration)

## Qualifying events (closed taxonomy §5.1; grade from the record's own words, frozen at log time)

| Event date | Type (T1–T7) | Sub-case | Grade (SEVERE / MODERATE / WATCH) | One-line description | Source (link) | Source tier (1 exchange / 2 agency / 3 press); WEAK-SOURCE? |
|---|---|---|---|---|---|---|

## Cooling-off search log (§5.3 release prong; two of three sources)

| Event date | Search date | Sources searched (screener results calendar / BSE-NSE announcements / AR PDFs) | Post-event audited print found? (results date AND FY-end strictly after event) | Result |
|---|---|---|---|---|

## Seeded-event corrections

| Seeded claim | Correct fact + date | Source | Real events logged above? |
|---|---|---|---|
```

**Sources, in order (§5.1 hierarchy):** (1) BSE/NSE corporate announcements (company scrip code /
symbol) → (2) SEBI orders, RBI press releases and rating-agency rationale PDFs (CARE, ICRA, CRISIL,
India Ratings, Acuité, Brickwork; the agency publication date is the T7 event date regardless of
legal stays) → (3) national business press (Economic Times, Business Standard, Mint,
Moneycontrol, Reuters India) — a record resting on (3) alone is tagged WEAK-SOURCE and caps at
MODERATE (no forced exit). **Tags (closed list):** T1 regulatory probe/action · T2 auditor events
· T3 promoter conduct · T4 withdrawn capital actions · T5 criminal/legal · T6 associate contagion
· T7 rating downgrade to D. Non-events (never logged as qualifying): earnings restatements,
dividend cuts/omissions, promoter purchases, scheduled auditor rotation, press rumour with no
dated record.

## 8. Firewall and void/FAIL triggers (§8.4 item 7), pre-stated

| Trigger | Status |
|---|---|
| (i) fewer than 5 name-dates certifiable on the three §8.2 pre-conditions → **VOID before run** | **TRIGGERED** |
| (ii) any blow-up fill → leg (a) FAIL | not applicable (no run) |
| (iii) decisional count < 3 → UNTESTED → VOID | not applicable (no run) |
| (iv) any mid-run rule change → VOID | not applicable (no run) |

## 9. Dead-design non-resurrection attestation (§8.4 item 8; spec §10 kill list)

No §10 kill-list design is used in this work. For each listed component:

| §10 component | Touched? |
|---|---|
| Frozen DCF entry anchor (level comparison) | **No.** The only valuation run is the v4 §2 inverse-DCF hurdle structure, computed solely to read `P_G1` for the §8.2(2) band — a new mechanism with its own spec rationale, not the killed level comparison. |
| Event-only GEV as the blow-up-leg mechanism | No. No event lane was run. |
| QFV 1.00× entry tier and its four quality conditions | No. |
| GEV-exercise filter that omits usability | No. The §8.2 firewall is a different, spec-defined band test; usability is not omitted by design but deliberately not run (§3.1). |
| Type 7 as a standalone codified veto | No. T7 appears only as one of seven §5.1 types in the event tape reading. |
| Usability check (b) | No. |
| 15 %-hurdle price reporting | No. |
| Financial-variant usability exemption | No. |
| Margin fade as a quality signal | No (the anchor uses the spec's flat trailing-5FY margin). |
| Beneish/accruals as fraud screens; Piotroski-as-fraud; dividend cuts as distress; promoter buying as a positive | No. |
| Own-multiple anchor, Gate M, Guardrail V | No. |

## 10. Disclosures, open items and scoping notes (for Bablu; nothing here amends the spec)

1. **Scoring-date window.** The Phase-C task fixed 2019-03-31 … 2021-03-31; §8.1 permits vintages
   through 2022. A 2022-03-31 vintage (E1 window up to 2024-03) was therefore out of scope for this
   session and is an available input to a fresh pre-reg, not something applied here.
2. **§8.2(1) vs the firewall.** §8.2 wants a usability verdict recorded pre-run; the Phase-C firewall
   forbids running usability for selection. I did not run it; condition 1 is uncertified for all.
   Confirmation wanted on whether a fresh pre-reg may certify usability by input-conditions only
   (audited scoring-FY EPS sign, basis nameable) without the U3 numeric check.
3. **Class-split mapping.** The spec says "screener.in Sector ∈ {Banks, Finance}". Screener now uses
   Broad Sector > Sector > Broad Industry > Industry; "Banks" and "Finance" sit at **Broad Industry**
   (Sector = "Financial Services" for both). The spec's stated coverage (banks, NBFCs, HFCs) is
   preserved by reading Broad Industry. Needs a one-line confirmation before a run.
4. **E1 reading.** §8.2(3) was applied literally (first qualifying event on the tape; pre-d0 events
   fail). Whether the first event *after* d0 should define E1 is a spec-level question; it was not
   applied, and this VOID does not depend on it being answered (most near-misses fail on an event
   < d0+6m regardless).
5. **Firewall conventions.** `results_published` = FY-end + 60 days (nominal; the real filing date is
   a Phase-D verification item); β = 1.15 for every candidate (V310-C9 blow-up bucket); shares =
   screener Market Cap ÷ Current Price (carried v3.8–v3.11 method, which ignores share-count
   changes after d0).
6. **Path notes.** The task cites `validation/check_disjoint_v311.py`; the file is
   `validation/v3_11_oos/check_disjoint_v311.py`. `cross_engine/` does not exist in this repo.
7. **Leads for the next pre-reg** (needing the sources listed in caveat 1): Simplex Infrastructures
   (2019/2020 dates; the most promising lead, E1 undated), Thomas Cook India 2019 (category
   question), Dhani 2020 (unverified), plus a systematic sweep from the NSE/BSE announcement
   archive, SEBI/IBBI order lists and rating-agency default lists.
