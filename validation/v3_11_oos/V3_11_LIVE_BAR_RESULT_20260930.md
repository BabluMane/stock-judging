# v3.11 OOS confirmation live-bar result — 2026-09-30

**VERDICT: FAIL.** Two of the four live-bar legs fail on the locked rules: one
blow-up name-date filled (bar: 0, hard) and only one distinct winner name filled
(bar: ≥ 3). v3 stays **NOT LIVE**. No company here is described as investable.

**One locked run, no refit** (`specs/V3_7_DELTA.md` §5). Frozen spec:
`specs/V3_11_DELTA.md`, `specs/V3_10_DELTA.md` (DCF), `specs/V3_9_DELTA.md`
(§1 QFV, §2 GEV, §3 bar); frozen set: `validation/v3_11_oos/OOS_SET_PREREG.md`
(PR #9). `engine/`, `cross_engine/`, `specs/` and all prior `validation/` dirs
were not touched. Fetched data, the runner (`run_v311_validation.py`) and all 13
governance logs were committed **before** the run (lock commit `eafa841`, pushed);
the run happened once (`run_output_v311.txt`, `oos_results_v311.json`) and nothing
was changed afterwards. Sensitivities (`sensitivity_v311.py`) ran after the locked
run and are non-decisional.

## Scorecard

| Leg | Bar | Result | Verdict |
|---|---|---|---|
| Blow-up fills | 0 (hard) | **1** name-date filled — `srei_2020-03-31`, ACC and INV legs, both 2020-04-03 @ ₹4.05 | **FAIL** |
| Distinct winner names with ≥ 1 fill | ≥ 3 | **1** — TVS Motor | **FAIL** |
| To-T (fill → latest 2026-09-29) | clearly positive | mean **6.38×** over 13 fills (includes the two Srei legs at 0.519×, last vendor print 2023-08-11) | numerically positive — see caveat |
| 24-month forward | ≥ 0.8× | mean **1.74×** over 13 fills (worst leg 1.014×) | numerically pass — see caveat |

Caveat on the last two lines: 8 of the 13 legs were entered inside the COVID
trough (2020-03-13 → 2020-04-30) and average 8.73× to-T / 1.93× 24m; the other 5
legs average 2.61× / 1.44×. Excluding the two blow-up legs the means are
7.44× / 1.82×. These two lines are passing numbers that do not rescue the verdict:
the bar requires all four legs.

**Neither failing leg rests on a judgment call**:

- **Blow-up leg.** `srei_2020` filled at the first weekly close after scoring,
  **before any qualifying governance event in its log**: the first qualifying
  event is the 2021-03-05 default rating (type 7); the fill is 2020-04-03. No
  reading of the §2.1 taxonomy, and no borderline row in any log, changes that
  (there is no earlier event to reclassify). The pre-reg flagged exactly this risk
  for `srei_2020`. Usability exempted it (financial variant), fair value was
  positive (₹29.35/share vs price ₹3.90), and no GEV event was active.
- **Winner leg.** Even with GEV switched off entirely only **two** winner names
  would fill (TVS Motor and KEI Industries) — sensitivity S0/S1b — so the winner bar
  cannot be reached by any GEV reading. The other winners did not touch a trigger
  (P/FV at scoring: Jubilant 2.72/2.33, Tube Investments 1.13/4.11, Pidilite
  1.56/2.26; QFV-qualified Jubilant 2019 and Pidilite never came within 1.00× FV in
  the window).

## GEV: what stopped what (blow-up leg, stated plainly)

The requirement was an explicit count of blow-up fills stopped by GEV versus by
valuation/usability. Five blow-up name-dates:

| Name-date | Usability | Fair value | Trigger touched if GEV off? | GEV | Outcome / primary stopper |
|---|---|---|---|---|---|
| gayatri_2019-03-31 | EXCLUDED — (a) TTM −5.22 vs audited 8.55 (−161%) | +181.19 | yes (ACC 2019-05-10, INV 2019-08-23) | not active at fills (next event 2019-11-13 comes later) | **usability gate** |
| gayatri_2020-03-31 | EXCLUDED — sourced FY EPS non-positive (−3.1) | +92.63 | yes (2020-04-03) | **veto at scoring** (2019-11-13 pledge invocation; also 2019-11-15 type 7) | **usability gate** (GEV would independently have stopped it) |
| sadbhav_2020-03-31 | EXCLUDED — (a) TTM −11.11 vs 46.21 (−124%) | +604.71 | yes (2020-04-03) | **veto at scoring** (2019-06-26 type 7, RHTPL D) | **usability gate** (GEV would independently have stopped it) |
| sadbhav_2021-03-31 | EXCLUDED — sourced FY EPS non-positive (−9.03) | +220.71 | yes (2021-04-01) | **veto at scoring** (2020-04-01 type 7, Rohtak-Panipat D) | **usability gate** (GEV would independently have stopped it) |
| srei_2020-03-31 | USABLE (financial variant, exempt) | +29.35 | yes (2020-04-03) | none active | **NOT STOPPED — filled** |

**Tally.** Blow-up fills: **1** name-date (2 legs). Decisional blow-up name-dates
stopped by **GEV: 0**; by **usability: 4**; by **valuation (no positive FV / no
touch): 0**; not stopped: 1. GEV was genuinely exercised end-to-end on three
blow-up name-dates (gayatri_2020, sadbhav_2020, sadbhav_2021), each of which would
have filled with GEV off — but all three were already usability-excluded, so
they are shadow name-dates and GEV's stops do not enter the scorecard. On the one
usable blow-up with a fill opportunity, GEV had nothing to act on. Type 7 fired at
scoring on two name-dates (both Sadbhav, both shadow); **decisional type-7 vetoes: 0**.
`gayatri_2019` is the fragile one: with the audited share count (see Deviations) its
fills precede the seeded default and GEV cannot stop them; with the frozen
market-cap share count its fair value is 2.5× lower and GEV blocks both legs at
fill (sensitivity S3). Either way usability, not GEV, is what kept it off the
scorecard.

**What GEV would NOT have caught** (§5 residual risk, confirmed): a distressed
name that is cheap before its first public red flag. `srei_2020` and `gayatri_2019`
(audited-share basis) both fill weeks after scoring, months before the first
qualifying default. GEV blocks entries after the first public event; it does not
predict it. The pre-reg's GEV-exercise filter selected names with positive FV and
a touched trigger but did not include the usability gate, so it did not make GEV
the deciding mechanism on any decisional name-date — usability again stopped 4 of 5
blow-ups, the same structure as v3.10.

## Step A — usability (frozen v3.7 test, applied first)

**19 / 25 usable.** Excluded (all check (a) or the non-positive-EPS harness rule;
none adjusted): ongc_2019 (−29.5%), sunpharma_2019 (+35.5%), gayatri_2019 (−161.1%),
gayatri_2020 (audited EPS ≤ 0), sadbhav_2020 (−124.0%), sadbhav_2021 (audited EPS ≤ 0).
Check (b) fired for no name-date. Srei exempt (financial variant). Full per-name
reasons: `run_output_v311.txt`. Excluded name-dates were valued in a labelled SHADOW
pass (non-decisional); shadow fills: ongc_2019, gayatri_2019 (both would fill),
sunpharma_2019/gayatri_2020/sadbhav_2020/sadbhav_2021 (GEV-vetoed at scoring).

## Step B — v3.10 valuation (verbatim), per name-date

`g = min(ROE_avg3 × (1 − payout), 15%)`, 10-year horizon, margin fade years 1–5,
terminal at year 10 (g 4%), Rf 6.95%, ERP 4.0%, tax 25.17%, capex ≈ depreciation,
WC 5% of incremental revenue, net cash = investments − borrowings; financial variant
(Srei) = 10-year excess-return with BVPS growth = same g. Valuation conventions
V310-C1…C9 are unchanged from v3.10 (listed in the runner docstring). Sector betas
fixed pre-run: tvsmotor 1.10, jublfood 0.85, tiindia 1.05, kei 1.00, pidilite 0.70,
emami 0.70, marico 0.60, ongc 1.00, sunpharma 0.85, nhpc 0.75, gayatri/sadbhav/srei
1.15. `*` = 15% cap binding; [shadow] = usability-excluded, non-decisional.

| Name-date | Usability | g | ROE_avg3 | payout | FV/share | Price@d0 | P/FV | QFV | GEV@score | Fills |
|---|---|---|---|---|---|---|---|---|---|---|
| tvsmotor_2019-03-31 | USABLE | 15.0%* | 23.5% | 24% | 382.6 | 470.9 | 1.23 | no — (b) median OCF/PAT=0.53 < 0.85 | no | ACC 2020-03-27, INV 2020-04-03 |
| tvsmotor_2020-03-31 | USABLE | 15.0%* | 22.5% | 27% | 384.4 | 303.9 | 0.79 | no — (b) median OCF/PAT=0.58 < 0.85 | no | ACC 2020-04-03, INV 2020-04-03 |
| jublfood_2019-03-31 | USABLE | 13.9% | 17.6% | 21% | 106.2 | 288.8 | 2.72 | yes | no | none |
| jublfood_2020-03-31 | USABLE | 15.0%* | 23.4% | 28% | 121.5 | 282.8 | 2.33 | no — (c) D/E=1.4884135472370768 > 0.5 | no | none |
| tiindia_2020-03-31 | USABLE | 12.5% | 15.8% | 21% | 272.7 | 307.7 | 1.13 | no — (a) ROIC/ROCE trailing-5FY series unavailable -- not QFV-qua | no | none |
| tiindia_2021-03-31 | USABLE | 11.9% | 15.8% | 25% | 271.3 | 1116.5 | 4.11 | no — (c) D/E=0.8529411764705882 > 0.5 | no | none |
| kei_2019-03-31 | USABLE | 15.0%* | 22.5% | 5% | 885.4 | 425.6 | 0.48 | no — (a) ROIC/ROCE trailing-5FY series unavailable -- not QFV-qua | **yes** (2019-02-28 regulatory_probe) | ACC vetoed@scoring, INV vetoed@scoring |
| kei_2020-03-31 | USABLE | 15.0%* | 21.4% | 5% | 1058.4 | 255.2 | 0.24 | no — (d) market cap at scoring date ~Rs2440cr < Rs5,000cr | **yes** (2019-05-16 regulatory_probe) | ACC vetoed@scoring, INV vetoed@scoring |
| pidilite_2019-03-31 | USABLE | 15.0%* | 24.8% | 36% | 398.7 | 623.1 | 1.56 | yes | **yes** (2018-06-01 promoter_conduct) | ACC vetoed@scoring, INV vetoed@scoring, QFV vetoed@scoring |
| pidilite_2021-03-31 | USABLE | 14.0% | 22.6% | 38% | 397.8 | 900.2 | 2.26 | yes | no | none |
| emami_2019-03-31 | USABLE | 6.6% | 16.4% | 60% | 184.0 | 400.0 | 2.17 | yes | **yes** (2018-05-18 regulatory_probe) | ACC vetoed@scoring, INV vetoed@scoring, QFV vetoed@scoring |
| emami_2020-03-31 | USABLE | 6.2% | 15.4% | 60% | 151.0 | 156.4 | 1.04 | yes | no | none |
| marico_2019-03-31 | USABLE | 15.0%* | 35.1% | 55% | 300.9 | 345.2 | 1.15 | yes | no | ACC 2020-03-13, QFV 2020-02-28 |
| marico_2021-03-31 | USABLE | 6.2% | 36.5% | 83% | 187.3 | 401.9 | 2.15 | yes | no | none |
| [shadow] ongc_2019-03-31 | EXCLUDED | 10.3% | 14.5% | 29% | 738.4 | 159.8 | 0.22 | no — (a) median ROIC=14.0% min=13.0% -- fails 15%/10% bar | no | ACC 2019-04-05, INV 2019-04-05 |
| ongc_2021-03-31 | USABLE | 7.4% | 10.3% | 28% | 267.5 | 102.4 | 0.38 | no — (a) median ROIC=14.0% min=9.0% -- fails 15%/10% bar | no | ACC 2021-04-01, INV 2021-04-01 |
| [shadow] sunpharma_2019-03-31 | EXCLUDED | 8.9% | 11.9% | 25% | 443.4 | 478.9 | 1.08 | yes | **yes** (2019-03-05 regulatory_probe) | ACC vetoed@scoring, INV vetoed@scoring, QFV vetoed@scoring |
| sunpharma_2020-03-31 | USABLE | 5.9% | 7.9% | 25% | 378.6 | 338.2 | 0.89 | no — (a) median ROIC=10.0% min=10.0% -- fails 15%/10% bar | **yes** (2019-09-04 regulatory_probe) | ACC vetoed@scoring, INV vetoed@scoring |
| nhpc_2019-03-31 | USABLE | 4.5% | 10.2% | 56% | 28.6 | 24.7 | 0.86 | no — (a) median ROIC=9.0% min=8.0% -- fails 15%/10% bar | no | ACC 2019-04-05, INV 2020-03-27 |
| nhpc_2021-03-31 | USABLE | 5.2% | 10.2% | 49% | 29.9 | 23.2 | 0.78 | no — (a) median ROIC=9.0% min=8.0% -- fails 15%/10% bar | no | ACC 2021-04-01 |
| [shadow] gayatri_2019-03-31 | EXCLUDED | 3.9% | 3.9% | 0% | 181.2 | 159.6 | 0.88 | no — (a) median ROIC=8.0% min=3.0% -- fails 15%/10% bar | no | ACC 2019-05-10, INV 2019-08-23 |
| [shadow] gayatri_2020-03-31 | EXCLUDED | 1.8% | 1.8% | 0% | 92.6 | 8.6 | 0.09 | no — (a) median ROIC=9.0% min=4.0% -- fails 15%/10% bar | **yes** (2019-11-13 promoter_conduct) | ACC vetoed@scoring, INV vetoed@scoring |
| [shadow] sadbhav_2020-03-31 | EXCLUDED | 15.0%* | 16.6% | 0% | 604.7 | 29.6 | 0.05 | no — (a) median ROIC=11.0% min=9.0% -- fails 15%/10% bar | **yes** (2019-06-26 credit_default_recognition) | ACC vetoed@scoring, INV vetoed@scoring |
| [shadow] sadbhav_2021-03-31 | EXCLUDED | 15.0%* | 15.4% | 0% | 220.7 | 62.1 | 0.28 | no — (a) median ROIC=11.0% min=8.0% -- fails 15%/10% bar | **yes** (2020-04-01 credit_default_recognition) | ACC vetoed@scoring, INV vetoed@scoring |
| srei_2020-03-31 | USABLE | 8.0% | 8.0% | 0% | 29.3 | 3.9 | 0.13 | no — financial variant -- QFV gate not defined for bank/NBFC bala | no | ACC 2020-04-03, INV 2020-04-03 |


QFV-qualified: jublfood_2019, pidilite_2019/2021, emami_2019/2020, marico_2019/2021
(+ sunpharma_2019 shadow). **QFV fills: 1 name-date — marico_2019 (QFV leg
2020-02-28 @ ₹298.55 = 0.99× FV)**. ROIC = screener `ROCE %`; the series was not
available for 5 FYs for kei_2019 and tiindia_2020 (recorded as not QFV-qualified,
never substituted).

## Fill table (decisional; usable name-dates only)

Discount depth = 1 − fill price / fair value. QFV legs are fair-value entries; ACC/INV
legs are discount entries (V3_9_DELTA §1.3).

| Name-date | Category | Tier | Fill date | Fill price | Trigger | Fill/FV | Discount vs FV | to-T | 24m fwd |
|---|---|---|---|---|---|---|---|---|---|
| tvsmotor_2019-03-31 | winner | ACC (discount entry) | 2020-03-27 | 303.95 | 334.77 | 0.79 | 21% | 13.46× | 1.984× |
| tvsmotor_2019-03-31 | winner | INV (discount entry) | 2020-04-03 | 252.95 | 267.82 | 0.66 | 34% | 16.174× | 2.486× |
| tvsmotor_2020-03-31 | winner | ACC (discount entry) | 2020-04-03 | 252.95 | 336.33 | 0.66 | 34% | 16.174× | 2.486× |
| tvsmotor_2020-03-31 | winner | INV (discount entry) | 2020-04-03 | 252.95 | 269.07 | 0.66 | 34% | 16.174× | 2.486× |
| marico_2019-03-31 | mediocre | ACC (discount entry) | 2020-03-13 | 260.8 | 263.29 | 0.87 | 13% | 3.041× | 1.945× |
| marico_2019-03-31 | mediocre | QFV (fair-value entry) | 2020-02-28 | 298.55 | 300.9 | 0.99 | 1% | 2.656× | 1.658× |
| ongc_2021-03-31 | mediocre | ACC (discount entry) | 2021-04-01 | 104.35 | 234.08 | 0.39 | 61% | 2.204× | 1.448× |
| ongc_2021-03-31 | mediocre | INV (discount entry) | 2021-04-01 | 104.35 | 187.26 | 0.39 | 61% | 2.204× | 1.448× |
| nhpc_2019-03-31 | mediocre | ACC (discount entry) | 2019-04-05 | 24.3 | 25.06 | 0.85 | 15% | 3.017× | 1.014× |
| nhpc_2019-03-31 | mediocre | INV (discount entry) | 2020-03-27 | 19.4 | 20.05 | 0.68 | 32% | 3.779× | 1.405× |
| nhpc_2021-03-31 | mediocre | ACC (discount entry) | 2021-04-01 | 24.65 | 26.15 | 0.82 | 18% | 2.974× | 1.631× |
| srei_2020-03-31 | blowup | ACC (discount entry) | 2020-04-03 | 4.05 | 25.68 | 0.14 | 86% | 0.519× | 1.321× |
| srei_2020-03-31 | blowup | INV (discount entry) | 2020-04-03 | 4.05 | 20.54 | 0.14 | 86% | 0.519× | 1.321× |

Fills came at the first weekly close after scoring for 5 of the 7 filled
name-dates (tvsmotor_2020, ongc_2021, nhpc_2019 ACC, nhpc_2021, srei_2020). Mediocrities filled too (Marico, ONGC 2021, NHPC ×2): 7 of 13 legs, so
the valuation still does not separate winners from mediocrities.

## Component hit rates

- **QFV fills by name:** marico (1 leg). QFV-qualified names that never reached
  1.00× FV in-window: jublfood_2019, pidilite_2021, emami_2020, marico_2021; vetoed
  by GEV at scoring: pidilite_2019, emami_2019 (and shadow sunpharma_2019).
- **GEV vetoes by name (decisional), cited event and type:**

| Name-date | Event date | Type | Event |
|---|---|---|---|
| kei_2019-03-31 | 2019-02-28 | regulatory_probe | SEBI settlement order, promoter/KMP, 2005 GDR issue |
| kei_2020-03-31 | 2019-05-16 | regulatory_probe | SEBI settlement order against the company (cooling-off runs past scoring) |
| pidilite_2019-03-31 | 2018-06-01 | promoter_conduct | off-market promoter-family gift (one of nine gift rows) |
| emami_2019-03-31 | 2018-05-18 | regulatory_probe | SEBI adjudication order on promoter-group insider-trading SCN, no penalty — logged BORDERLINE, kept qualifying |
| sunpharma_2020-03-31 | 2019-09-04 | regulatory_probe | press report of SEBI-ordered forensic audit |

  Shadow vetoes: sunpharma_2019 (2019-03-05), gayatri_2020 (2019-11-13 pledge
  invocation; type 7 default 2019-11-15 also active), sadbhav_2020 (2019-06-26, type 7),
  sadbhav_2021 (2020-04-01, type 7). Fill-date vetoes: none fired anywhere.
- **GEV cost on the winner side:** GEV blocked KEI (both dates, ACC + INV) — the
  only other winner-side name that would have filled — and Pidilite 2019 (which would not have
  filled anyway). With every GEV row ignored the winner count is still 2.
- **C5 reporting:** GEV was evaluated for every name-date before any eligibility
  return; all 25 results carry a GEV report and a GEV-off counterfactual. It did
  not alter any fill.

## Step D — governance logs (`governance_logs/<company>.md`, 13 logs, rulebook `README.md` fixed pre-run)

Qualifying-row counts: tvsmotor 0, jublfood 1, tiindia 2, kei 2, pidilite 9, emami 1,
marico 0, ongc 0, sunpharma 6, nhpc 0, gayatri 14, sadbhav 8, srei 5.

**Method limits, stated plainly.** BSE/NSE announcement pages were not browsable
(403/CAPTCHA); the C3 fallback hierarchy (SEBI/RBI/rating-agency documents, then
national press with WEAK-SOURCE marking) was used throughout and logged. The
session-wide web-search budget (200) was exhausted partway, so several logs are
thinner than the checklist calls for: **Emami** had no search at all before I added
a direct SEBI title-search (which surfaced the 2018-05-18 order, now in the log);
**ONGC** has no dedicated group-level rating-D sweep and FY20–23 audit reports were
not read; **NHPC** had no dedicated ED/SFIO/auditor-resignation searches; **Pidilite**
promoter gifts after 2020-03 were not sourced (annual reports stop listing them);
Sadbhav/Gayatri: ICRA/India Ratings/Brickwork/Acuité D histories not reachable.
Empty qualifying tables (TVS, Marico, ONGC, NHPC) are therefore weaker than the
non-empty ones. Absence of hits is not proof of absence. This weakens every
"no veto" outcome, but it cannot rescue the blow-up leg: the Srei fill precedes
every event that exists in the log, and any event found later than 2020-04-03 is
irrelevant to that fill.

**Seeded events (C4 status):**

| Seeded event | Status |
|---|---|
| Gayatri: CARE BB+ → D ~2019-11-15 | **Sourced**, CARE press release 2019-11-15 (BS report 2019-11-18) |
| Gayatri: ~Mar-2021 further rating action | **Sourced** — CARE B → D on 2021-03-01 (a genuine second D; CARE had upgraded D → B on 2021-01-19) |
| Sadbhav: Rohtak-Hissar Tollway CARE BB+ → D ~Jun-2019 | **Sourced**, 2019-06-26; the seed's "wholly-owned" is unverified (company audit reports call the SPV a step-down subsidiary — consolidated group, so type 7 applies) |
| Sadbhav Mar-2020 CARE A−, Jul-2021 India Ratings BBB+, Sep-2022 CARE ISSUER-NOT-COOPERATING | Confirmed non-qualifying (above D / not-cooperating alone); Sadbhav's own D is 2023-05-11 |
| Srei: CARE and Acuité to D "early 2021" | **Sourced with an entity correction:** Acuité D 2021-03-05 was on Srei *Equipment Finance* NCDs (no Acuité rating found on SIFL); CARE moved every SIFL and SEFL facility to D on 2021-03-06; Brickwork 2021-04-06. Earliest D = 2021-03-05 (type 7) |
| Srei: RBI board supersession 2021-10-04 | **Sourced** (regulatory_probe) |
| Srei: NCLT insolvency admission 2021-10-08 | **Sourced**; logged non-qualifying by the rulebook (insolvency admission alone). No effect on any outcome |

**Unseeded findings that mattered:** Gayatri had an earlier **type-7 event on
2018-03-12** (CARE BB− → D, upgraded 2018-06-21); its cooling-off ended 2019-03-12,
19 days before the first scoring date, so it did not veto `gayatri_2019`. The pre-reg
premise for Tube Investments was wrong: TI became linked to CG Power only in
2020 (subscription agreement 2020-08-07, subsidiary 2020-11-26), so the 2019
CG Power SEBI/SFIO actions are non-qualifying for TI (BORDERLINE) — a C4-style
correction, no name swapped. The pre-reg's "≥ 2 blow-up name-dates with dated events
inside their 24m windows" requirement is met (gayatri_2019: 2019-11-15 default;
srei_2020: 2021-03-05 default, 2021-10-04 RBI; sadbhav_2020/2021: 2020-04-01,
2022-05-30 qualified opinion, 2022-06-08 default).

**Classification rulings (fixed pre-run, each a call):** rows judged by literal §2.1
wording; borderline rows go to the non-qualifying table, except routine SEBI
penalties/settlements and one exonerating SCN order that meet the literal wording,
which were kept as qualifying with a BORDERLINE flag: KEI settlement orders
(2019-02-28, 2019-05-16), Sun Pharma rows (2017-08-10 … 2021-02-11), Emami
2018-05-18, Tube Investments 2022-12-23 (`associate_contagion`), and nine Pidilite
promoter-family gifts (literal "gifts of promoter shares"). Non-qualifying by rule:
CBI/Income-tax/FDA/exchange-fine actions, insolvency admissions, rating moves above D.

## Sensitivities (non-decisional; `sensitivity_v311.py`, run after the locked run)

| # | Alternative reading | Effect on the bar legs |
|---|---|---|
| S0 | GEV switched off entirely | Winner names 2 (KEI, TVS) — still < 3; blow-up leg unchanged (srei fills either way) |
| S1a | KEI settlement orders not counted | Company order (2019-05-16) alone dropped: kei_2020 fills 2020-04-03 (ACC+INV), kei_2019 stays vetoed by the 2019-02-28 promoter order. Both dropped: both fill (ACC+INV 2019-04-05 / 2020-04-03). Winner names 2 either way |
| S1b | Pidilite gifts not counted / only out-of-group gifts counted | Pidilite still has no fill (P/FV 1.56, 2.26); winner names unchanged |
| S1c | Emami 2018-05-18 order not counted | emami_2019 QFV/ACC fill 2020-03-27 (mediocre; no bar effect) |
| S1d | Sun Pharma rows not counted | All rows dropped: sunpharma_2019 (shadow) would fill (QFV 2019-05-10, ACC 2019-06-21); sunpharma_2020 has no fill even then. Dropping only the 2019-03-05/2020-02-21 press rows leaves 2020 vetoed by 2019-09-04. No bar effect |
| S1e | Tube Investments 2022-12-23 not counted | No fill either way |
| S2 | Usability gate ignored | Blow-up name-dates that fill: 5 of 5 with GEV off; **2 of 5 with GEV on** (gayatri_2019: ACC 2019-05-10 @₹156.95, INV 2019-08-23 @₹109.15, to-T 0.14×/0.21×; and srei). GEV would stop the other three at scoring. Ignoring usability makes the blow-up leg worse, not better |
| S3 | Gayatri under the frozen mcap/price share count (guard off) | FV 72.06/36.84; gayatri_2019 both legs vetoed **at fill**; gayatri_2020 vetoed at scoring |
| S4 | Srei delisted terminal | Fill legs 0.519× to-T at the last vendor print (2023-08-11); zero terminal would be 0× — not decisional |
| S5 | Aggregates | winner legs 15.50× / 2.36×; mediocre legs 2.84× / 1.51×; blow-up legs 0.52× / 1.32× |

## Deviations and data notes

- **Share-count guard (pre-run, uniform).** Shares = screener market cap ÷ price
  (frozen method) unless that disagrees by > 20% with audited Equity Capital ÷ Face
  Value (latest FY). Only `gayatri` triggered it (2.51×; screener implies 46.5 cr
  shares vs 18.5 cr audited). It raised Gayatri's FV/share 2.5× (72.06 → 181.19 for
  2019). Chosen because leaving a known ~2.5× input error in place would bias the
  blow-up leg toward PASS. The frozen-method alternative is S3. Gayatri is
  usability-excluded either way, so it does not enter the scorecard.
- **Pre-reg filter vs run.** The pre-reg GEV-exercise filter used the frozen share
  method and beta 1.15; the run kept beta 1.15 for the blow-ups. Under the guard the
  first `gayatri_2019` touch moved from 2019-11-22 to 2019-05-10 — before the seeded
  default, not after it. Disclosed, not altered.
- **Corporate actions:** Yahoo public split feed for all but Srei (delisted; no feed,
  no actions recorded; irrelevant — Srei is usability-exempt).
- **Variant:** consolidated screener view for all 13; chart API on the same basis.
- **Series end:** Srei's price series ends 2023-08-11 (delisted); its to-T uses that
  last print and is flagged in the JSON. The vendor price series for Srei in
  Mar–Apr 2020 (₹3.80–₹6.25) was not cross-checked against exchange data.
- **Fill mechanics/aggregation:** first weekly close ≤ trigger inside (d0, d0+24m],
  leg-weighted means, price return only (no dividends), as v3.9/v3.10.
- The screener free tier reaches FY2015 (FY2016 for Tube Investments); no window had
  fewer than the 5 FYs the pre-reg specifies except where the ROCE series was
  missing (kei_2019, tiindia_2020).

## What happens next

Per `specs/V3_7_DELTA.md` §5 this returns to the spec/architecture level; no
parameter grid, no serial fix loop, and no change was made to any rule, log or
name-date after the run. Observations for a future proposal, not actions: (1) GEV
cannot stop entries that precede the first public red flag (Srei, Gayatri-2019 on the
audited share basis); (2) the usability gate, not GEV, decided the blow-up leg for the
second confirmation run in a row, so GEV's stops on three name-dates never reached the
scorecard; (3) the winner leg failed on price/valuation, not on the fraud screen — the
DCF still does not fill compounders. v3 remains NOT LIVE.

## Files

`fetch_data_v311.py`, `run_v311_validation.py` (docstring = convention record),
`sensitivity_v311.py`, `oos_results_v311.json`, `sensitivity_v311.json`,
`run_output_v311.txt`, `fetch_meta_v311.json`, `full_financials_raw_v311.json`,
`top_ratios_v311.json`, `pe_series/`, `eps_series/`, `corp_actions/`,
`governance_logs/` (13 logs + `README.md` rulebook).
