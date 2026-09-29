# v3.10 out-of-sample pre-registration — 2026-09-29

**Committed BEFORE any OOS data gathering.** No price series, EPS series,
QFV input data (ROIC/OCF-PAT/D-E/market-cap), governance-event log entries,
or corporate-action history has been fetched for any name below. This is the
fresh live-bar test set for `specs/V3_10_DELTA.md` (`specs/V3_7_DELTA.md` §5,
`validation/README.md` "Live bar"): 0 blow-ups, ≥ 3 distinct winner names,
positive to-T, ≥ 0.8× 24m — run ONCE, no refit.

**No valuation, backtest, or fill simulation was run in this session.** The
only script run is the pure name-membership check below. Category labels are
pre-registered from general public market history known before this task,
the same basis as the v3.8/v3.9 sets. A label that proves wrong once real PIT
data is gathered is a finding to report, not a reason to swap the name.

## Freeze rule

**No name-date is added, removed, or re-dated after this document is
committed, for any reason** — including a usability exclusion, a category
label proving wrong, a data-availability problem, or an inconvenient result.
A second run is a new pre-registration, not a rerun of this one.

## Construction

- 25 name-dates / 13 companies: **5 winners × 2 dates = 10, 5 mediocrities
  × 2 dates = 10, 3 blow-ups (2+2+1 dates) = 5.**
- **Every scoring date ≥ 2019-03-31** (minimum in set: 2019-03-31), all at a
  31 March fiscal-year-end. Every company has a 31-March FY-end; scoring
  date = FY-end of the scoring FY. Latest date 2024-03-31 leaves ≥ 24m
  forward runway before this commit (2026-09-29).
- Fresh vintage on purpose: the in-sample/v3.8/v3.9 sets are 2013–2021
  vintages dominated by 2014–2018; this set is 2019–2024 and is where the
  v3.10 10-year/sustainable-growth DCF is meant to be judged.
- All large/mid-cap NSE/BSE names with audited annual-report history,
  except the blow-up bucket, whose story *is* a governance/solvency
  collapse (a feature of the bucket, not a data-quality defect).

## Overlap check (zero overlap required)

Prior name-dates are listed in full inside `check_disjoint_v310.py`
(committed alongside; pure membership check, no data touched):

- **In-sample 25 companies / 50 name-dates:** aplapollo, astral, bajajcon,
  bajfin, bhel, brightcom, deepak, dhfl, hero, itc, lichf, lupin, manpasand,
  mnm, navin, persistent, piind, safari, suntv, symphony, tataelxsi, trent,
  vakrangee, wipro, yesbank (dates: `validation/v3_7/corrected_verdicts_final.json`).
- **v3.8 OOS 13 companies / 25 name-dates:** titan, divislab, pageind, dmart,
  polycab, colpal, ashokley, cipla, coalindia, gail, pcjeweller, fretail,
  cgpower (dates: `validation/v3_8_oos/OOS_SET_PREREG.md`).
- **v3.9 OOS 13 companies / 25 name-dates:** asianpaint, hdfcbank, nestleind,
  britannia, havells, bhartiartl, tatasteel, ntpc, tatamotors, bankbaroda,
  zeel, relcapital, ilfstransport (dates: `validation/v3_9_oos/OOS_SET_PREREG_v39.md`).

Overlap is tested at company level (strict) and name-date level. Note
Bajaj Auto is a distinct company from in-sample `bajajcon` / `bajfin`;
Bharat Electronics is distinct from in-sample `bhel`; Coforge/NIIT
Technologies is distinct from in-sample `persistent`.

**Script output (`python3 validation/v3_10_oos/check_disjoint_v310.py`):**

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
union company overlap:   []
union name-date overlap: []
min v3.10 scoring date: 2019-03-31
DISJOINT: True
```

## The 25 name-dates


### Winners (pre-registered)

| # | Name-date | Company | NSE symbol | FY-end | Why pre-registered |
|---|---|---|---|---|---|
| 1 | dixon_2019-03-31 | Dixon Technologies | DIXON | 31 Mar | Electronics-manufacturing-services leader; well-documented multi-year re-rating on PLI/scale-up in phones and appliances. |
| 2 | dixon_2021-03-31 | Dixon Technologies | DIXON | 31 Mar | Electronics-manufacturing-services leader; well-documented multi-year re-rating on PLI/scale-up in phones and appliances. |
| 3 | hal_2019-03-31 | Hindustan Aeronautics | HAL | 31 Mar | Defence PSU; well-documented order-book-driven re-rating after the 2018 listing. |
| 4 | hal_2021-03-31 | Hindustan Aeronautics | HAL | 31 Mar | Defence PSU; well-documented order-book-driven re-rating after the 2018 listing. |
| 5 | bel_2019-03-31 | Bharat Electronics | BEL | 31 Mar | Defence electronics PSU; well-documented order-book and margin-driven multi-year compounder. |
| 6 | bel_2021-03-31 | Bharat Electronics | BEL | 31 Mar | Defence electronics PSU; well-documented order-book and margin-driven multi-year compounder. |
| 7 | coforge_2019-03-31 | Coforge (listed as NIIT Technologies until 2020) | COFORGE | 31 Mar | Mid-cap IT services; well-documented strong multi-year compounding on deal wins and margin expansion. |
| 8 | coforge_2021-03-31 | Coforge (listed as NIIT Technologies until 2020) | COFORGE | 31 Mar | Mid-cap IT services; well-documented strong multi-year compounding on deal wins and margin expansion. |
| 9 | tatapower_2020-03-31 | Tata Power Company | TATAPOWER | 31 Mar | Integrated power utility; well-documented deleveraging and renewables-led re-rating from the 2020 lows. |
| 10 | tatapower_2021-03-31 | Tata Power Company | TATAPOWER | 31 Mar | Integrated power utility; well-documented deleveraging and renewables-led re-rating from the 2020 lows. |

### Mediocrities (pre-registered)

| # | Name-date | Company | NSE symbol | FY-end | Why pre-registered |
|---|---|---|---|---|---|
| 11 | hul_2021-03-31 | Hindustan Unilever | HINDUNILVR | 31 Mar | FMCG bellwether; well-documented range-bound price with earnings growth absorbed by de-rating post-2021. |
| 12 | hul_2022-03-31 | Hindustan Unilever | HINDUNILVR | 31 Mar | FMCG bellwether; well-documented range-bound price with earnings growth absorbed by de-rating post-2021. |
| 13 | bajajauto_2019-03-31 | Bajaj Auto | BAJAJ-AUTO | 31 Mar | Two-wheeler/three-wheeler major; well-documented flat multi-year price through 2019-21 on volume stagnation. Unrelated to Bajaj Consumer Care / Bajaj Finance. |
| 14 | bajajauto_2021-03-31 | Bajaj Auto | BAJAJ-AUTO | 31 Mar | Two-wheeler/three-wheeler major; well-documented flat multi-year price through 2019-21 on volume stagnation. Unrelated to Bajaj Consumer Care / Bajaj Finance. |
| 15 | petronet_2019-03-31 | Petronet LNG | PETRONET | 31 Mar | Regulated-style LNG terminal utility; well-documented range-bound price and muted total return. |
| 16 | petronet_2021-03-31 | Petronet LNG | PETRONET | 31 Mar | Regulated-style LNG terminal utility; well-documented range-bound price and muted total return. |
| 17 | bpcl_2019-03-31 | Bharat Petroleum Corporation | BPCL | 31 Mar | PSU oil marketer; well-documented flat price, margin-volatility and under-recovery/privatisation-uncertainty overhang. |
| 18 | bpcl_2021-03-31 | Bharat Petroleum Corporation | BPCL | 31 Mar | PSU oil marketer; well-documented flat price, margin-volatility and under-recovery/privatisation-uncertainty overhang. |
| 19 | powergrid_2019-03-31 | Power Grid Corporation of India | POWERGRID | 31 Mar | Regulated PSU transmission utility; well-documented range-bound shareholder return. |
| 20 | powergrid_2021-03-31 | Power Grid Corporation of India | POWERGRID | 31 Mar | Regulated PSU transmission utility; well-documented range-bound shareholder return. |

### Blow-ups / frauds (pre-registered)

| # | Name-date | Company | NSE symbol | FY-end | Why pre-registered |
|---|---|---|---|---|---|
| 21 | coffeeday_2019-03-31 | Coffee Day Enterprises | COFFEEDAY | 31 Mar | Founder V.G. Siddhartha's death (Jul-2019) and subsequent disclosure (Jan-2020) of ~INR 3,500 cr diverted to a promoter-linked entity; sharp stock collapse. |
| 22 | coffeeday_2020-03-31 | Coffee Day Enterprises | COFFEEDAY | 31 Mar | Founder V.G. Siddhartha's death (Jul-2019) and subsequent disclosure (Jan-2020) of ~INR 3,500 cr diverted to a promoter-linked entity; sharp stock collapse. |
| 23 | gensol_2023-03-31 | Gensol Engineering | GENSOL | 31 Mar | Solar/EV-leasing company; well-documented 2025 rating downgrades and lender defaults, then SEBI interim order (Apr-2025) alleging promoter fund diversion; stock collapse. |
| 24 | gensol_2024-03-31 | Gensol Engineering | GENSOL | 31 Mar | Solar/EV-leasing company; well-documented 2025 rating downgrades and lender defaults, then SEBI interim order (Apr-2025) alleging promoter fund diversion; stock collapse. |
| 25 | lvb_2019-03-31 | Lakshmi Vilas Bank | LAKSHVILAS | 31 Mar | Private bank under RBI Prompt Corrective Action from Sep-2019, moratorium and forced DBS amalgamation Nov-2020 with equity written off. Single-dated (FY19); FY20 would price after PCA was public. |

## Blow-up dated governance events inside 24m windows

Requirement: ≥ 2 blow-up name-dates with dated governance events inside the
24-month window after the scoring date. Seeded candidate events below are
from general public record at **month precision** and are **not verified**;
Phase 3 must source and date each from BSE/NSE filings or national press. The
freeze covers the name-dates, not these event dates.

| Name-date | 24m window | Candidate dated events inside window |
|---|---|---|
| coffeeday_2019-03-31 | 2019-04-01 → 2021-03-31 | Jul-2019 founder disappearance/death (`promoter_conduct`); Jan-2020 disclosure of funds diverted to promoter-linked entity (`promoter_conduct`) |
| lvb_2019-03-31 | 2019-04-01 → 2021-03-31 | Sep-2019 RBI Prompt Corrective Action (`regulatory_probe`); Nov-2020 RBI moratorium and DBS amalgamation scheme (`withdrawn_capital_action`) |
| gensol_2023-03-31 | 2023-04-01 → 2025-03-31 | Q1-CY2025 rating-agency downgrades and lender payment defaults (`auditor_event`/`regulatory_probe`, tag to be settled in Phase 3) |
| gensol_2024-03-31 | 2024-04-01 → 2026-03-31 | Q1-CY2025 rating downgrades/defaults; Apr-2025 SEBI interim order on promoter fund diversion (`regulatory_probe`, `promoter_conduct`) |
| coffeeday_2020-03-31 | 2020-04-01 → 2022-03-31 | None seeded; Jul-2019 and Jan-2020 events are PIT-known at scoring. Logged, but not counted toward the ≥ 2 requirement. |

Requirement met by four name-dates (coffeeday_2019, lvb_2019, gensol_2023,
gensol_2024) on seeded events; if Phase 3 cannot date events for at least two,
that is reported as a finding, not fixed by swapping names.

## QFV input windows (frozen; §1.1 of `specs/V3_9_DELTA.md`, untouched by v3.10)

Per name-date, pull PIT the **trailing 5 audited FYs** and the market-cap
check. Window = FY(N−4) … FY(N) for scoring date 31-Mar-N. If fewer than 5
audited FYs exist for a name (recent listing), the available audited FYs are
used and the shortfall is recorded — never substituted. v3.10 additionally
needs ROE_avg3 (trailing-3-FY, i.e. the last three FYs of the same window)
and scoring-FY DividendPayout %; no new window is added.

| Name-date | Trailing 5 audited FYs | Market-cap check date |
|---|---|---|
| dixon_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| dixon_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| hal_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| hal_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| bel_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| bel_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| coforge_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| coforge_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| tatapower_2020-03-31 | FY16, FY17, FY18, FY19, FY20 | 2020-03-31 |
| tatapower_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| hul_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| hul_2022-03-31 | FY18, FY19, FY20, FY21, FY22 | 2022-03-31 |
| bajajauto_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| bajajauto_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| petronet_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| petronet_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| bpcl_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| bpcl_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| powergrid_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| powergrid_2021-03-31 | FY17, FY18, FY19, FY20, FY21 | 2021-03-31 |
| coffeeday_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |
| coffeeday_2020-03-31 | FY16, FY17, FY18, FY19, FY20 | 2020-03-31 |
| gensol_2023-03-31 | FY19, FY20, FY21, FY22, FY23 | 2023-03-31 |
| gensol_2024-03-31 | FY20, FY21, FY22, FY23, FY24 | 2024-03-31 |
| lvb_2019-03-31 | FY15, FY16, FY17, FY18, FY19 | 2019-03-31 |

Only FY windows and dates are stated; no figures have been pulled.

## Governance-log template (frozen)

One log per company, populated PIT in Phase 3 (only events disclosed before
the scoring/fill date under evaluation count toward that evaluation).

| Event date | Taxonomy tag (§2.1.1–6) | One-line description | Source (BSE/NSE filing or press, with link) |
|---|---|---|---|

Sources (fixed): BSE Corporate Announcements (company's own scrip code); NSE
Corporate Announcements (own symbol); Economic Times, Business Standard,
Mint, Moneycontrol, Reuters India for corroboration and associate-contagion.

Tags (closed list, `specs/V3_9_DELTA.md` §2.1 — GEV taxonomy unchanged by
v3.10): `regulatory_probe`, `auditor_event`, `promoter_conduct`,
`withdrawn_capital_action`, `criminal_legal`, `associate_contagion`.

Log files to be created in Phase 3 (none exist at this commit):

- `validation/v3_10_oos/governance_logs/dixon.md`
- `validation/v3_10_oos/governance_logs/hal.md`
- `validation/v3_10_oos/governance_logs/bel.md`
- `validation/v3_10_oos/governance_logs/coforge.md`
- `validation/v3_10_oos/governance_logs/tatapower.md`
- `validation/v3_10_oos/governance_logs/hul.md`
- `validation/v3_10_oos/governance_logs/bajajauto.md`
- `validation/v3_10_oos/governance_logs/petronet.md`
- `validation/v3_10_oos/governance_logs/bpcl.md`
- `validation/v3_10_oos/governance_logs/powergrid.md`
- `validation/v3_10_oos/governance_logs/coffeeday.md`
- `validation/v3_10_oos/governance_logs/gensol.md`
- `validation/v3_10_oos/governance_logs/lvb.md`

## What happens next (not started)

Fetch EPS, price, corporate-action and QFV inputs; populate logs PIT; apply
the frozen usability test, the v3.10 valuation and entry logic (QFV / ACC /
INV gated by GEV), name-date by name-date, recording the fired check and
reason regardless of outcome. The freeze rule above applies throughout.
