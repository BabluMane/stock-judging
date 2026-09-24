# v3.8 out-of-sample live-bar result — 2026-09-24

**Verdict: FAIL. v3 stays NOT LIVE.**

The live bar (`specs/V3_7_DELTA.md` §5, `validation/README.md`): 0 blow-up
fills (hard), ≥ 3 distinct winner names filled, to-T clearly positive, 24m
≥ 0.8×. Run **once**, on the frozen pre-registration
(`validation/v3_8_oos/OOS_SET_PREREG.md`), no refit.

| Criterion | Result | Verdict |
|---|---|---|
| (a) Blow-up fills = 0 (hard) | **3** name-dates filled (pcjeweller_2017, pcjeweller_2018, fretail_2019) | **FAIL** |
| (b) Winner names ≥ 3 distinct | **2** (divislab, polycab) | **FAIL** |
| (c) to-T clearly positive | See caveat below — not independently decisive | not scored as a tiebreaker |
| (d) 24m ≥ 0.8× | **1.415×** mean over 14 fills (2 truncated) | PASS, but see caveat |

Two of the four criteria fail outright, one of them the hard bar. The
verdict does not depend on any judgment call about (c) or (d) — **DCF-only
entry fired on real, pre-registered fraud names it should have kept out of,
and it did not reach a third winner name.** That is the finding.

---

## 1. What was actually run

Real data, gathered after network access was unblocked mid-task (see prior
turn): weekly price series, publication-dated vendor TTM EPS, and audited
annual P&L data (revenue, operating margin, depreciation, borrowings,
investments, EPS) for all 13 pre-registered companies, fetched directly from
screener.in (`validation/v3_8_oos/pe_series/`, `eps_series/`,
`full_financials_raw.json`, `top_ratios.json`). Three research agents did
the initial gather (their notes: `validation/v3_8_oos/NOTES.md`); a
second, direct pass by this session refetched the P&L/balance-sheet tables
because the mediocrity-group agent's `dcf_financials/*.json` had only
captured the last 5 fiscal years (2022–2026) instead of full history back to
2015 — that bug is why `full_financials_raw.json` and
`fetch_full_financials.py` exist as the actual source of record for the DCF
inputs, not the original `dcf_financials/*.json` files (kept in the repo as
part of the audit trail of what the agents produced, but superseded for
computation).

**Methodology finding, verified not assumed:** screener.in's audited
"EPS in Rs" P&L row is computed as (audited PAT) ÷ (TODAY's continuously
split/bonus-adjusted share count) — confirmed empirically on GAIL, whose
2015 PAT of ₹3,160cr against its displayed EPS of ₹4.67 implies ~677cr
shares outstanding, matching *today's* post-four-bonus share count (~5.3×
the ~127cr shares GAIL actually had in FY2015), not the as-filed FY2015
count. This means the sourced FY EPS gathered here is **already on the same
continuously-adjusted basis as the vendor TTM series** — no manual
corporate-action restatement was needed, resolving the basis-mismatch flags
several research agents raised (GAIL's mid-window bonus, Ashok Leyland's
2025 bonus, PC Jeweller's 2017 bonus) without further adjustment.

### Usability test (`validation/v3_7/CONVENTIONS.md`, applied exactly)

| Name-date | Verdict | Fired check / reason |
|---|---|---|
| titan_2016-03-31 | USABLE | (a) +11.6% |
| titan_2018-03-31 | USABLE | (a) +8.5% |
| divislab_2016-03-31 | USABLE | (a) +3.7% |
| divislab_2018-03-31 | USABLE | (a) −0.8% |
| pageind_2015-03-31 | USABLE | (a) +4.3% |
| pageind_2017-03-31 | USABLE | (a) +6.5% |
| dmart_2018-03-31 | USABLE | (a) −2.7% |
| dmart_2019-03-31 | USABLE | (a) +3.7% |
| polycab_2020-03-31 | USABLE | (a) +0.4% |
| polycab_2021-03-31 | USABLE | (a) −5.7% |
| colpal_2016-03-31 | USABLE | (a) +1.7% |
| colpal_2018-03-31 | USABLE | (a) +1.2% |
| ashokley_2016-03-31 | USABLE | (a) +13.3% |
| ashokley_2018-03-31 | USABLE | (a) −4.3% |
| **cipla_2016-03-31** | **EXCLUDED** | (a) −23.1% (fails ±15%) |
| cipla_2018-03-31 | USABLE | (a) +8.4% |
| coalindia_2016-03-31 | USABLE | (a) +12.9% |
| **coalindia_2018-03-31** | **EXCLUDED** | (a) +32.0% (fails ±15%) |
| **gail_2016-03-31** | **EXCLUDED** | (a) +49.3% (fails ±15%) |
| gail_2018-03-31 | USABLE | (a) −4.1% |
| pcjeweller_2017-03-31 | USABLE | (a) +8.5% |
| pcjeweller_2018-03-31 | USABLE | (a) +8.1% |
| **fretail_2017-03-31** | **EXCLUDED** | (a) +10,400% — sourced FY EPS ₹0.09 (near-zero, comparability broken by the Bharti Retail demerger scheme effective 31-Oct-2015, per `corp_actions/fretail.json`) vs vendor TTM ₹9.45. Structural, not a marginal miss. |
| fretail_2019-03-31 | USABLE | (a) +0.8% |
| **cgpower_2016-03-31** | **EXCLUDED** | (a) sign conflict — sourced audited EPS **−7.33** (loss-making) vs vendor TTM +4.87 (positive). This is the CG Power vendor-vs-audited discrepancy the blow-up research agent flagged as genuinely unresolved; it fails the constant-residual harmless-basis test in `CONVENTIONS.md` §1 outright (a sign flip cannot be a basis residual), so it is excluded as a basis defect rather than adjudicated further. Independently, CG Power's own fundamentals were already loss-making/margin-collapsed at this date per the research agent's PIT read — a company DCF-entry would not have wanted to buy regardless. |

**20/25 usable (80%).** Substantially better retention than the in-sample
frozen set's 52% (26/50) — expected, since this set skews toward large/
mid-cap names with cleaner reporting, and the frozen set intentionally
included several structurally-broken series (DHFL, Manpasand) that this set
has no equivalent of. The 5 exclusions are all real, checkable failures
(2 marginal ±15% misses, 1 clean corporate-action/demerger break, 1 marginal
miss, 1 genuine data conflict) — none manufactured to hit a target.

---

## 2. DCF construction and fill mechanics

**Entry mechanism** (`V3_7_DELTA.md` §1): ACCUMULATE trigger = 0.875 × DCF
fair value/share, INVEST trigger = 0.70 × DCF fair value/share, fixed at the
scoring date, first weekly close at/below a trigger fills that leg once.
This exact three-tier structure is **not implemented in `engine/engine_v3.py`**
in this repository (that engine implements the current spec's single-trigger
IRR-based `range_rule`/`trigger_block`, a different, later mechanism) — this
was already true for the in-sample sanity check and is reconfirmed here.
`run_oos_validation.py` reimplements the DCF value function
(`engine_v3.dcf_value`'s FCFF/terminal-normalization logic, spec §4.1) and
the fixed three-tier bands directly, since real financial-statement inputs
(not a quality-scored input dict) are what's available and all that's
needed for a DCF-only entry test.

**Point-in-time discipline:** revenue/margin/depreciation history for each
DCF uses only the fiscal years up to and including the FY ending at the
scoring date (trailing 5 FYs where available); growth = min(5-yr revenue
CAGR, 12%), capped at 0 on the downside (no negative growth assumed).
Net cash/debt uses the **same FY's** balance sheet (not today's) — an
earlier bug in this run used today's balance sheet uniformly and produced
nonsensical negative fair values for Titan and Ashok Leyland (large current
borrowings for gold-loan/working-capital financing swamped a 2016-dated
valuation); this was caught and fixed before the results below, not after.
Shares outstanding for the per-share conversion uses **today's** continuously
adjusted count (market cap ÷ current price), matching the basis of the price
series being tested against.

**Disclosed simplifications (real limitations, not fabricated numbers):**
- Capex assumed ≈ depreciation throughout (screener has no clean historical
  capex line via static fetch; agents proxied it as CFO−FCF, which this
  script did not use directly — a capex=dep steady-state assumption was used
  instead, understating near-term reinvestment for still-scaling names like
  Polycab/Divi's and probably modestly overstating their FCFF/fair value).
- Working capital assumed at a flat 5% of incremental revenue (no clean WC
  series was fetchable).
- Beta: screener.in exposes no measured 2yr-weekly-vs-Nifty beta on any of
  the 13 company pages (checked). Used informed, disclosed sector-typical
  betas (e.g. FMCG ~0.55–0.7, pharma ~0.65–0.75, industrials/jewellery
  ~1.05–1.25) rather than an assumed 1.0, per spec's "never assume ≥1.0"
  instruction — but these are not Damodaran-sourced precisely, only
  directionally reasonable.
- "to-T": the OOS names are live, ongoing listings with no natural
  resolution date the way the historical frozen-set multibaggers had a
  known outcome. Operationally, to-T here means "to the latest price in
  each name's fetched series" — for most names that is 2026-09-24 (today),
  but for `fretail` specifically the committed price series
  (`pe_series/fretail.csv`) only runs to 2020-09-11 (211 weekly rows), well
  short of both today and even a full 24-month window from its March-2020
  fills. **This makes the "to-T" line, and the 2 fretail legs inside the
  24m aggregate, partial/truncated data, not a completed outcome** — flagged
  in the fill table below and excluded from being treated as decisive.
  Separately, the PC Jeweller "to-latest" ratios are actively *misleading*:
  they show positive (1.74×/2.28×) only because of a speculative 2025–26
  rally years after the real 24-month outcome (0.179×/0.255× — a genuine
  ~75–82% loss) already happened. This is exactly why the scorecard below
  is built from the real fwd_24m window, not the to-latest proxy.

## 3. Fill table (20 usable name-dates, ONE run)

| Name-date | Category | ACC trg | INV trg | ACC fill | INV fill | fwd_24m (ACC) | fwd_24m (INV) |
|---|---|---|---|---|---|---|---|
| titan_2016-03-31 | winner | 79.32 | 63.46 | no fill | no fill | — | — |
| titan_2018-03-31 | winner | 193.12 | 154.50 | no fill | no fill | — | — |
| **divislab_2016-03-31** | **winner** | 797.20 | 637.76 | **2016-12-30 @ 783.70** | **2017-03-24 @ 623.45** | **1.872×** | **2.668×** |
| divislab_2018-03-31 | winner | 690.41 | 552.33 | no fill | no fill | — | — |
| pageind_2015-03-31 | winner | 3671.15 | 2936.92 | no fill | no fill | — | — |
| pageind_2017-03-31 | winner | 5875.18 | 4700.14 | no fill | no fill | — | — |
| dmart_2018-03-31 | winner | 215.33 | 172.26 | no fill | no fill | — | — |
| dmart_2019-03-31 | winner | 280.57 | 224.46 | no fill | no fill | — | — |
| **polycab_2020-03-31** | **winner** | 665.45 | 532.36 | **2020-05-22 @ 627.30** | no fill | **4.075×** | — |
| polycab_2021-03-31 | winner | 746.04 | 596.83 | no fill | no fill | — | — |
| colpal_2016-03-31 | mediocre | 338.38 | 270.71 | no fill | no fill | — | — |
| colpal_2018-03-31 | mediocre | 389.13 | 311.30 | no fill | no fill | — | — |
| ashokley_2016-03-31 | mediocre | 32.77 | 26.21 | no fill | no fill | — | — |
| **ashokley_2018-03-31** | mediocre | 44.76 | 35.81 | **2019-01-25 @ 41.30** | **2019-08-02 @ 32.20** | 1.480× | 2.062× |
| cipla_2018-03-31 | mediocre | 298.56 | 238.85 | no fill | no fill | — | — |
| **coalindia_2016-03-31** | mediocre | 290.70 | 232.56 | **2016-04-01 @ 287.00** | no fill | 0.987× | — |
| **gail_2018-03-31** | mediocre | 69.54 | 55.64 | **2020-03-13 @ 56.37** | **2020-03-20 @ 53.87** | 1.802× | 1.872× |
| **pcjeweller_2017-03-31** | **blowup** | 8.71 | 6.96 | **2018-07-20 @ 8.19** | **2018-09-28 @ 6.24** | **0.179×** | **0.255×** |
| **pcjeweller_2018-03-31** | **blowup** | 9.87 | 7.89 | **2018-07-20 @ 8.19** | **2018-09-21 @ 7.18** | **0.179×** | **0.221×** |
| **fretail_2019-03-31** | **blowup** | 137.90 | 110.32 | **2020-03-20 @ 112.50** | **2020-03-27 @ 87.20** | 0.945×‡ | 1.220×‡ |

‡ truncated — series ends 2020-09-11, ~5.5 months into the 24m window, not
the full window. Not a completed outcome.

Raw output: `validation/v3_8_oos/oos_results.json`. Script:
`validation/v3_8_oos/run_oos_validation.py` (usability + DCF + fill
mechanics), `validation/v3_8_oos/fetch_full_financials.py` (raw data
refetch).

## 4. The four-line scorecard

1. **Blow-up fills: 3 (need 0). FAIL — hard bar.** Both PC Jeweller
   name-dates and Future Retail's single usable name-date all fired a DCF
   entry. PC Jeweller's real 24-month outcome after entry is a 75–82% loss
   (0.179×/0.221×/0.255×) — this is not a marginal or ambiguous case. DCF-only
   entry, run once on real pre-registered fraud names with real financial
   statements, bought into two of the three.
2. **Winner names filled: 2 (divislab, polycab). Need ≥3. FAIL.** Of the 5
   pre-registered winner companies (10 name-dates), only 2 distinct names
   ever filled a leg. Titan, Page Industries, and DMart never touched
   their ACC/INV triggers in the 24-month window from either scoring date —
   consistent with the same structural finding as the in-sample DCF
   revalidation (`specs/V3_7_DCF_REVALIDATION_20260923.md` §3): triggers
   set 12.5–30% below a DCF fair value are frequently never reached by
   names that simply re-rate steadily upward without a large drawdown, so
   DCF-only entry systematically underfills genuine long-run compounders.
3. **to-T: not decisive either way** (see §2's caveat — no clean
   resolution date exists for live OOS names, and the one directly
   computable proxy is demonstrably misleading for PC Jeweller specifically).
   Not needed to reach a verdict since (a) and (b) already fail.
4. **24m ratio: 1.415× mean over 14 fills (need ≥0.8×). Nominally PASS**,
   but 2 of the 14 fills (both Future Retail legs) are truncated
   mid-window, and the 2 clean PC Jeweller fills inside this same average
   are real, catastrophic losses (0.179×–0.255×) that the average absorbs
   only because 3 of the 4 non-blowup name-dates that filled did well
   (divislab +87%/+167%, polycab +307%, ashokley +48%/+106%). A PASS on
   this line next to a hard FAIL on blow-ups is not a mitigating signal —
   it is the same fact restated: the engine buys good names and bad names
   on the same trigger logic, and this aggregate only looks fine because
   the good names it did buy outnumber the fraud names it also bought.

## 5. Verdict and what it means for v3-live status

**v3 (DCF-only entry, v3.7) FAILS the live bar on a genuinely out-of-sample,
pre-registered, real-data set.** This is the first result under the actual
live-bar protocol — everything before this (`v3_6`, `v3_7` frozen-26,
`insample_sanity`) was in-sample or a machinery check, explicitly not a
substitute for this run. **v3 stays NOT LIVE.**

Per the hard rules stated in this task and in `V3_7_DELTA.md` §5: this is
ONE run. No refit, no second attempt, no threshold tweak in response to this
outcome. A failure here returns to the spec document (`V3_7_DELTA.md`), not
to the parameter grid — exactly the same discipline that applied to the
v3.6→v3.7 transition after Gate M/Guardrail V failed. **Gate M and
Guardrail V remain dead and are not touched or resurrected by this
result — nothing here revisits them; they were never a candidate fix for
what failed today** (DCF-only entry firing on fraud names is a different
failure mode than the own-multiple anchor's anti-selectivity that motivated
their retirement in the first place).

The failure has two independent, non-overlapping causes, both real
findings from real data, not an artifact of a marginal call:
- **Blow-ups get bought.** A DCF-derived trigger 12.5–30% below fair value
  is a statement about price relative to a model's estimate of value; it
  says nothing about whether the underlying earnings/cash-flow assumptions
  feeding that model are trustworthy. PC Jeweller's FY17/FY18 audited
  numbers (revenue growing, EPS growing, nothing yet visibly broken in the
  headline P&L two years before the collapse became public) produced a
  perfectly ordinary-looking DCF fair value and a trigger that a genuine
  price decline later crossed — DCF-only entry has no mechanism to
  distinguish "cheap because a temporary drawdown" from "cheap because
  heading toward zero." This is the same class of finding the v3.6 EPS
  forensics work made about Brightcom (a fraud that *looked* fine in
  vendor data until it didn't) — except this time it isn't a data-quality
  artifact, it's the entry mechanism itself buying into a real fraud on
  real, correctly-usability-tested audited numbers.
- **Genuine compounders get skipped.** Steady re-raters (Titan, Page
  Industries, DMart) never pulled back 12.5%+ below a rising DCF fair value
  inside a 24-month window, so DCF-only entry never engages with them at
  all — the same "trigger rescaling asymmetry" structural point
  `V3_7_DELTA.md` §2 already logged for the in-sample set reproduces here
  on brand-new names.

## 6. Assumptions flagged for the record

- Sourced FY EPS uses screener.in's own "EPS in Rs" P&L row (verified to be
  PAT ÷ today's share count, not back-solved from the vendor quotient
  series — see §1).
- DCF capex≈depreciation, WC=5% flat, sector-typical (not measured) betas —
  all disclosed in §2, all real simplifications given data availability,
  none chosen to move a result.
- Three-tier entry mechanism reimplemented outside `engine/engine_v3.py`
  (which does not contain it) — same situation as the in-sample sanity
  check, not new to this run.
- Future Retail's price series is incomplete (ends 2020-09-11); its 2
  blow-up fills are directionally real (both triggers were crossed on real
  March-2020 prices) but their 24m outcome is a partial-window estimate,
  not confirmed — not that this changes anything: it is a real blow-up fill
  either way, and its inclusion or exclusion does not move (a) below FAIL
  (PC Jeweller alone already fails the hard 0-blow-ups bar) or (b) below FAIL.
- CG Power's cgpower_2016-03-31 sourced-vs-vendor sign conflict is reported,
  not resolved — it is excluded from the usable set on that basis, per
  `CONVENTIONS.md` §1's rule that only a *constant* residual is waved
  through, never adjudicated to make a name usable.
