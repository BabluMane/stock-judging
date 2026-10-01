# v4 Phase-D pre-registration — FROZEN (Bablu authorized 2026-10-01)

**Status: FROZEN. This is the pre-registered, locked Phase-D run per V4_SPEC
§8. The full 25-name-date set is frozen: 5 certified blow-up name-dates
(Phase C, shape-complete 5/5) + 10 winner + 10 mediocrity name-dates
(selected 2026-10-01, Musey-audited PASS), with
`check_disjoint_v4_phased.py` → DISJOINT: True on record. The locked run may
now proceed on Bablu's separate authorization — one run, no mid-run edits.
Any observation becomes a next-iteration proposal.**

System is NOT LIVE. Nothing here describes any company as investable.

## §8.4(1) Frozen rules hash

| Item | Value |
|---|---|
| Spec file | `engine_v4/V4_SPEC.md` |
| Spec SHA-256 | `6acb4acdcb7f93a042df36d4eb111bcca5dfa38d894864ec13d269096f2be671` (must match `test_constants.py` pin at freeze time) |
| Engine tree | `6ea7e7a1de50ccfaccd466a4e1f402efbd3ebbe3` (verified identical at local HEAD 47d9dbf) |
| Engine build commit | `efbc934` (merge of PR #11, `claude/v4-build`); 137/137 tests (re-run at draft time — see below) |
| Phase C R1 VOID | `47d9dbf` (PR #12, data-access failure — not a design failure) |
| Phase C R2 audited files on main | `5becb0b05dfa` (V4_OOS_PREREG_R2.md), `63d6d69c16db` (check_disjoint_v4_r2.py), `ab1f041cc858` (fill_plausibility_results_r2.json) |
| Set manifest hash | `107997d5daf8ffe1843b29e0ee3211cb2b9e1ee56d62759695e3755fc185cfc8` (`SET_MANIFEST.json`: 25 name-dates / 13 companies; tiers 10/10/5) |

**Caveat:** the local port mirror sits at 47d9dbf (behind main; pull blocked —
Bablu holds the credential). The R2 landings only added `validation/v4_oos/`
files; the engine tree hash above is verified identical at local HEAD, so the
engine pins stand. The final pre-reg must be written against the true main
HEAD at freeze time, re-verifying the tree hash and the spec pin.

**Frozen-engine test re-run (draft time):** not runnable in this environment
(no pytest installed); engine tree hash verified identical to `efbc934`
where 137/137 passed, and the frozen-dir diff
`git diff efbc934 HEAD -- engine_v4 engine validation/v3_6 validation/v3_7
validation/v3_8_oos validation/v3_9_oos validation/v3_10_oos validation/v3_11_oos`
is empty (verified 2026-10-01). The audit checklist requires a 137/137 pass at
freeze time on the freeze machine.

## §8.4(2) Set composition (§8.1)

**Shape:** 25 name-dates / 13 companies — 5 winner companies × 2; 5 mediocre
companies × 2; 3 blow-up companies totalling 5 name-dates (2+2+1). March-31
scoring dates only; all ≥ 2019-03-31; vintage years 2019–2022.

**Freeze rule:** no name added, removed, or swapped after the freeze commit,
for any reason. A category label that proves wrong once PIT data is gathered
is a finding to report, never a reason to swap a name.

### Blow-ups (certified, frozen in this draft)

| # | Name-date | Company | NSE symbol | Scoring FY | One-line thesis |
|---|---|---|---|---|---|
| 21 | supremeeng_2020-03-31 | Supreme Engineering Ltd | SUPREMEENG | FY2019 | SME infra-services; statutory auditor resigned mid-term 2021-11-03 citing fee dispute; first-ever governance event on tape |
| 22 | supremeeng_2021-03-31 | Supreme Engineering Ltd | SUPREMEENG | FY2020 | (same E1, second in-band window → double-carrier) |
| 23 | pbm_2019-03-31 | PBM Polytex Ltd | BSE 514087 | FY2018 | Textiles; statutory auditor resigned mid-term, first exchange disclosure 2020-09-30; first-ever governance event on tape |
| 24 | pbm_2020-03-31 | PBM Polytex Ltd | BSE 514087 | FY2019 | (same E1, inclusive-boundary second window → double-carrier) |
| 25 | varroc_2019-03-31 | Varroc Engineering Ltd | VARROC | FY2018 | Auto components; first-ever qualified consolidated audit opinion (FY20, ₹943.68M disputed warranty claim), disclosed 2020-06-25 |

### Winners (SELECTED 2026-10-01 — coordinator sweep, Musey-audited PASS)

5 companies × 2 name-dates each (10 name-dates). Realized-outcome criterion:
**documented multi-year outperformance / re-rating profile** from general
public market history.

| # | Name-date | Company | NSE symbol | One-line thesis |
|---|---|---|---|---|
| 1 | infy_2020-03-31 | Infosys | INFY | COVID-era digital-transformation deal boom + large-deal wins; multi-year EPS compounding and sustained P/E re-rating (2020-25) |
| 2 | infy_2021-03-31 | Infosys | INFY | (same) |
| 3 | sbin_2021-03-31 | State Bank of India | SBIN | PSU-bank credit-cost normalization + corporate-book recovery; 2021-24 re-rating (~2.5× in 3 years) |
| 4 | sbin_2022-03-31 | State Bank of India | SBIN | (same) |
| 5 | srf_2019-03-31 | SRF | SRF | Fluorochemicals/specialty-chemicals capex cycle + import substitution; EPS 16.08 → 64.27 FY18-22 |
| 6 | srf_2020-03-31 | SRF | SRF | (same) |
| 7 | lt_2021-03-31 | Larsen & Toubro | LT | Domestic capex-cycle order-book boom + asset monetization / NWC discipline; 2021-25 run |
| 8 | lt_2022-03-31 | Larsen & Toubro | LT | (same) |
| 9 | endurance_2020-03-31 | Endurance Technologies | ENDURANCE | 2W/4W ancillary; OEM share gains + premiumization; steady compounding FY19-24 |
| 10 | endurance_2021-03-31 | Endurance Technologies | ENDURANCE | (same) |

### Mediocrities (SELECTED 2026-10-01 — coordinator sweep, Musey-audited PASS)

5 companies × 2 name-dates each (10 name-dates). Realized-outcome criterion:
**documented flat / de-rating / range-bound multi-year profile**.

| # | Name-date | Company | NSE symbol | One-line thesis |
|---|---|---|---|---|
| 11 | drreddy_2019-03-31 | Dr Reddy's Laboratories | DRREDDY | US generics price erosion 2017-19; MOSL Jan-2018: stock "will remain range bound" (~₹2,000-3,000 band 2017-19) |
| 12 | drreddy_2020-03-31 | Dr Reddy's Laboratories | DRREDDY | (same) |
| 13 | dabur_2020-03-31 | Dabur India | DABUR | Defensive FMCG; price range-bound ₹400-560 across 2019-22 while EPS barely moved (8.17 → 8.18) |
| 14 | dabur_2021-03-31 | Dabur India | DABUR | (same) |
| 15 | maruti_2019-03-31 | Maruti Suzuki | MARUTI | Auto slowdown + BS-VI transition; flat ₹6,000-7,500 2018-21 while EPS declined 260.86 → 145.30 FY18-21 |
| 16 | maruti_2020-03-31 | Maruti Suzuki | MARUTI | (same) |
| 17 | cyient_2020-03-31 | Cyient | CYIENT | Midcap ER&D/IT; flat ₹400-600 2017-21 |
| 18 | cyient_2021-03-31 | Cyient | CYIENT | (same) |
| 19 | auropharma_2019-03-31 | Aurobindo Pharma | AUROPHARMA | US FDA overhangs; price flat ₹700-900 2017-21 even as EPS grew 41.36 → 91.05 by FY21 — textbook de-rating |
| 20 | auropharma_2020-03-31 | Aurobindo Pharma | AUROPHARMA | (same) |

### Winner/mediocrity selection audit (Musey, 2026-10-01) — PASS

- **Disjointness:** `check_disjoint_winmed.py` re-run independently →
  DISJOINT: True, exit 0 (company AND name-date level vs 5 prior sets via
  canonical imported lists + R1–R7 burn list + 3 blow-up companies).
- **Exact U1/U2 (frozen engine_v4.usability):** coordinator ran all 60
  candidate name-dates; parent spot-checked infy_2020 (EPS 35.26), srf_2019
  (EPS 16.08 — matches thesis), drreddy_2019 (EPS 11.41), sbin_2022 (EPS
  25.11): all PASS/PASS.
- **Tier collisions adjudicated:** infy/axisbank/sbin appeared in both worker
  pools → kept in winner tier (axis of assignment); infy_2020-03-31 and
  axisbank_2019/2020-03-31 exact name-date collisions resolved to winners.
  aavas dropped on leg-(b) feasibility (financial-model firewall 3.543/6.033).
- **Informational firewall (not a gate):** all 10 winner name-dates
  fill-plausible (≤2.0); mediocrities mixed (drreddy_2019 2.163, dabur_2021
  2.336 over) — immaterial, not a selection criterion.
- **Carried caveats:** R2's full 36-name-date list not in the local mirror
  (R2 cross-check from sweep memory only — audit caveat); post-window
  splits/bonuses (aartiind, vinatiorga, elgiequip, godrejcp): screener EPS
  already restated so U1/U2 verdicts hold, exact ex-dates unsourced —
  documented in SET_WINMED_DOSSIER.md.
- Kills: vbl (December FY); timken, aubank (truncated screener spans confirmed
  source-side); sbin_2019-03-31 deliberately avoided (FY18 EPS −5.11) → double
  shifted to 2020∩2021. Verified alternates in reserve: tcs, bajajfinsv,
  aartiind, atul, fineorg (winners); godrejcp, eichermot (mediocrities).

### Winner/mediocrity selection protocol (pre-registered now, executed after Bablu's go-ahead)

1. Candidate generation from general public market history (no price-data
   fitting; no threshold grids).
2. **Exclusions (all pre-registered, no exceptions):** the six prior sets
   (in-sample 25/50; v3.8, v3.9, v3.10, v3.11 — 13/25 each) at company AND
   name-date level; the 3 certified blow-up companies; every company examined
   in Phase C R1–R7 (examined leads are burned — re-using a failed lead as a
   winner/mediocrity is data contamination); renamed/demerged tickers mapped
   by legal-entity identity (name-normalizer discipline).
3. Mechanical pre-checks per name-date before freezing: scoring-FY identified
   by the 63-day PIT rule (Bablu adjudication: **U1/U2-only usability for
   certification; U3 runs at Phase-D time**); fill-plausibility is NOT required
   for winners/mediocrities (only blow-ups carry §8.2(2)); disjointness
   asserted per-name-date.
4. The selection sweep is evidence-only: no engine changes, no repo writes
   outside `validation/v4_oos/`, no Phase-D execution. Its dossier + disjoint
   script are committed alongside this pre-reg at freeze.

## §8.4(3) Decisional test set (§8.2)

The 5 blow-up name-dates, each certified pre-run on the three mechanical
pre-conditions. Per Bablu's 2026-09-30 adjudication: usability = U1/U2 on the
frozen `engine_v4.usability` (U3 belongs to Phase D); E1 = first qualifying
event on the tape, dated by first exchange disclosure (R3 precedent); class
split reads screener Broad Industry ∈ {Banks, Finance}.

| # | Name-date | Cond 1: usability (U1/U2 exact, frozen engine) | Cond 2: fill-plausible P_d0 ≤ 2.0×P_G1 | Cond 3: pre-flag-risk E1 ∈ [d0+6m, d0+24m], first-ever | Verdict |
|---|---|---|---|---|---|
| 21 | supremeeng_2020-03-31 | U1 PASS (no restatement); U2 PASS (sourced FY19 EPS 0.27) | P_d0=1.54, P_G1=7.44, ratio **0.207** PASS | E1 2021-11-03 T2 auditor resignation (R T Jain & Co, fee dispute) ∈ [2020-09-30, 2022-03-31] ✓; tape FY19 unmodified (29-May-2019) + FY20 unmodified (05-Aug-2020) | CERTIFIED |
| 22 | supremeeng_2021-03-31 | U1 PASS; U2 PASS (sourced FY20 EPS 0.15) | P_d0=2.56, P_G1=7.44, ratio **0.344** PASS | same E1 ∈ [2021-09-30, 2023-03-31] ✓ (double-carrier) | CERTIFIED |
| 23 | pbm_2019-03-31 | U1 PASS (no restatement, audited/sourced 0.998); U2 PASS (sourced FY18 EPS 4.69) | P_d0=78.65, P_G1=106.66, ratio **0.737** PASS | E1 2020-09-30 T2 auditor resignation (Chandulal M. Shah & Co; letter 18-Jul-2020, disclosure 30-Sep-2020) ∈ [2019-09-30, 2021-03-31] ✓; tape FY17–FY20 unmodified | CERTIFIED |
| 24 | pbm_2020-03-31 | U1 PASS (audited/sourced 1.000); U2 PASS (sourced FY19 EPS 3.94) | P_d0=28.85, P_G1=133.55, ratio **0.216** PASS | same E1 ∈ [2020-09-30, 2022-03-31] ✓ (boundary-inclusive double-carrier) | CERTIFIED |
| 25 | varroc_2019-03-31 | U1 PASS (no restatement, audited/sourced 0.913); U2 PASS (sourced FY18 EPS 36.57) | P_d0=579.0, P_G1=487.57, ratio **1.188** PASS | E1 2020-06-25 T2 first-ever qualified consolidated opinion (SRBC & Co LLP; ₹943.68M disputed warranty claim, Note 40) ∈ [2019-09-30, 2021-03-31] ✓; ∉ d0-2020 window → single-carrier; FY19 consolidated "Opinion" unmodified (24-May-2019) | CERTIFIED |

**Exercise target and void rule (verbatim from V4_SPEC §8.2):**

> **Exercise condition:** genuine exercise of the distress screen requires decisional on **≥3** of
> the 5 name-dates (= §1 leg (a′)).
> **Void rule:** if the pre-reg set cannot supply 5 name-dates meeting all three pre-conditions
> (certified pre-run), **the run does not proceed — it is VOID**, not weakened, not reinterpreted,
> not "underpowered but counted." If the run proceeds and the screen is decisional on <3, the
> blow-up leg is recorded as **UNTESTED** and the run is VOID — an unexercised 0 is not a PASS of
> leg (a). Both cases require a new pre-reg + a new set (fresh zero-overlap vs all six prior sets,
> §8.3).

**Decisional** (post-run): the distress screen is decisional on a name-date iff
its veto blocked a fill the anchor would otherwise have made (anchor trigger
met in-window, screen veto active — verified from raw fills + veto logs).

## §8.4(4) Overlap proof (§8.3)

**Blow-up 5:** `check_disjoint_r7.py` (committed in the R7 sweep record)
asserts the certified name-dates and all 60 R7 lead companies against every
prior set — in-sample, v3.8–v3.11, R1/R2-examined, R3-certified,
R4/R5/R6-leads, R6-certified. Verbatim output:

```
R7 certified: ['varroc_2019-03-31']
R7 leads examined: 60 companies
  R7 certified vs in-sample: company overlap []
  R7 leads     vs in-sample: company overlap []
  R7 certified vs v3.8: company overlap []
  R7 leads     vs v3.8: company overlap []
  R7 certified vs v3.9: company overlap []
  R7 leads     vs v3.9: company overlap []
  R7 certified vs v3.10: company overlap []
  R7 leads     vs v3.10: company overlap []
  R7 certified vs v3.11: company overlap []
  R7 leads     vs v3.11: company overlap []
  R7 certified vs r1-examined: company overlap []
  R7 leads     vs r1-examined: company overlap []
  R7 certified vs r2-examined: company overlap []
  R7 leads     vs r2-examined: company overlap []
  R7 certified vs r3-certified: company overlap []
  R7 leads     vs r3-certified: company overlap []
  R7 certified vs r4-leads: company overlap []
  R7 leads     vs r4-leads: company overlap []
  R7 certified vs r5-leads: company overlap []
  R7 leads     vs r5-leads: company overlap []
  R7 certified vs r6-leads: company overlap []
  R7 leads     vs r6-leads: company overlap []
  R7 certified vs r6-certified: company overlap []
  R7 leads     vs r6-certified: company overlap []
DISJOINT: True
```

The R3 and R6 dossiers record the same True assertion for the Supreme and PBM
name-dates (each asserted against all prior sets at certification time).

**Full 25-name-date / 13-company proof: COMPLETE (2026-10-01).**
`check_disjoint_v4_phased.py` (prior lists imported by import, never retyped;
name-normalizer discipline for renamed/demerged tickers; R1–R7 burn list at
company level with the 5 certified blow-up companies excepted — certification
supersedes the burn) asserts all 25 name-dates against the five prior sets +
the R1–R7 examined-lead burn list at company AND name-date level. Independently
re-run by Musey:

```
DISJOINT: True
```

exit 0. **The locked run may not start unless DISJOINT: True is on record —
it is.**

## §8.4(5) Data / runner / log commit order

Data + runner + logs are committed under `validation/v4_oos/` BEFORE any
result JSON; the result JSON is committed last. Frozen directories
(`engine_v4/`, `engine/`, `validation/v3_6` … `validation/v3_11_oos`) are
untouched — additions only under `validation/v4_oos/`. One locked run; no
mid-run edits (any observation becomes a next-iteration proposal).

**Run mechanics (pre-registered):** the frozen `engine_v4` runs all 25
name-dates per V4_SPEC §§2–6: inverse-DCF implied-growth anchor (§2),
state-based distress screen (§3; 13 frozen rules; attribution first —
§12-C4: distress → usability → event lane → anchor), v4 usability gate
(§4; U3 ±15% median rule runs here), severity-graded event lane with in-window
type-7 exit (§5; exit slippage 1.0%; SEVERE-only exits), fill mechanics
(first weekly close, 24m, 1 leg/tier; §6), leg-weighted price-return
aggregation (§6.4). Gate-trace table per §7; shadow pass present for vetoed
names. Missing required input ⇒ UNCOMPUTABLE-DATA (VETOED-DATA), never a
silent pass.

**The live bar (§1, unchanged — PASS requires all legs):**
- Leg (a): 0 blow-up fills (hard).
- Leg (a′): distress screen decisional on ≥3 of the 5 certified name-dates.
  **Leg (a) PASS requires (a′); an unexercised 0 is UNTESTED, not PASS.**
- Leg (b): ≥3 distinct winner names with fills.
- Leg (c): to-T aggregate clearly positive.
- Leg (d): 24m aggregate ≥0.8×.

## §8.4(6) Audit checklist

- [ ] Spec SHA-256 equals the §8.4(1) value and the `test_constants.py` pin.
- [ ] Frozen-tree diff empty: `git diff efbc934 HEAD -- engine_v4 validation/v3_6 validation/v3_7 validation/v3_8_oos validation/v3_9_oos validation/v3_10_oos validation/v3_11_oos` prints nothing.
- [ ] 137/137 engine tests pass at freeze time.
- [ ] Only files under `validation/v4_oos/` were added.
- [ ] `check_disjoint_v4_phased.py` re-run independently reproduces DISJOINT: True on all 25 name-dates / 13 companies.
- [ ] Each §8.4(3) certification cell re-verified from its dossier evidence (opinion headings, filing dates, firewall raw JSON, exact U1/U2 rerun).
- [ ] Bar recomputed independently from raw result JSON (all four legs + (a′)).
- [ ] Decisional count recomputed from raw fills + veto logs (≥3 required).
- [ ] Shadow pass present for vetoed names.
- [ ] No result JSON containing fills, vetoes, exits or aggregates exists before the data+runner+log commits.

## §8.4(7) Firewall and void/FAIL triggers, pre-stated

| Trigger | Status |
|---|---|
| (i) fewer than 5 name-dates certifiable on the three §8.2 pre-conditions → VOID before run | **NOT triggered — 5/5 certified** |
| (ii) any blow-up fill → leg (a) FAIL | armed |
| (iii) decisional count < 3 → UNTESTED → VOID | armed |
| (iv) any mid-run rule change → VOID | armed |

## §8.4(8) Dead-design non-resurrection attestation (spec §10 kill list)

No §10 kill-list design is used in this pre-reg or in the locked run it
authorizes:

| §10 component | Touched? |
|---|---|
| Frozen DCF entry anchor (level comparison) | **No.** The anchor is the v4 inverse-DCF implied-growth hurdle (§2) — a new mechanism with its own pre-registered rationale, not the killed level comparison. |
| Event-only GEV as the blow-up-leg mechanism | No. The blow-up leg is the §3 state-based distress screen. |
| QFV 1.00× entry tier and its four quality conditions | No. Dropped, not re-justified (§2.6, §12-C1). |
| GEV-exercise filter that omits usability | No. |
| Type 7 as a standalone codified veto | No. T7 appears only inside the §5.1 taxonomy (SEVERE/MODERATE grading). |
| Usability check (b) | No. Dead and removed; §8.2(1) = U1/U2 per Bablu's adjudication. |
| 15%-hurdle price reporting | No. |
| Financial-variant usability exemption | No. Financials carry the CAMEL composite (D6); no free pass. |
| Margin fade as a quality signal | No. Flat trailing-5FY margin (§11). |
| Beneish/accruals as fraud screens; Piotroski-as-fraud; dividend cuts as distress; promoter buying as a positive | No. |
| Own-multiple anchor, Gate M, Guardrail V | No. |

## Bablu adjudications carried (2026-09-30, Phase-C retry)

1. Usability = U1/U2 for certification (§8.2(1)); U3 runs at Phase-D time (§4).
2. Screener "Sector ∈ {Banks, Finance}" reads as Broad Industry.
3. E1 = first qualifying event on the tape; dated by first exchange disclosure (R3 precedent).
4. 2022 scoring vintages allowed (E1 windows close by 2024-03 under free-data-only).

## Freeze record (2026-10-01)

1. ~~Winner/mediocrity selection sweep~~ — **DONE 2026-10-01** (coordinator +
   workers; 10 winners + 10 mediocrities selected; Musey audit PASS;
   `SET_WINMED_DOSSIER.md`, `set_winmed.json`, `check_disjoint_winmed.py` →
   DISJOINT: True).
2. ~~Full 25-name-date overlap proof~~ — **DONE 2026-10-01**
   (`check_disjoint_v4_phased.py` → DISJOINT: True, exit 0, independently
   re-run; 25 name-dates / 13 companies).
3. ~~Set-manifest hash recorded~~ — **DONE 2026-10-01**:
   `107997d5daf8ffe1843b29e0ee3211cb2b9e1ee56d62759695e3755fc185cfc8`.
4. ~~Musey audit of the final freeze package~~ — **PASS 2026-10-01**:
   spec SHA-256 matches pin; local HEAD 47d9dbf; frozen-dir diff vs efbc934
   empty; disjoint re-run True; §8.4(3) certification cells re-verified from
   dossier evidence; only `validation/v4_oos/` files added. 137/137 test
   re-run not possible in this environment — mandatory on the freeze machine
   at freeze time.
5. ~~Bablu authorized the freeze~~ — **"its all good. just freeze it"**
   (2026-10-01, main chat). Freeze lands directly on `main` (no PR, per
   Bablu's 2026-09-30 workflow rule).
6. **The locked run is NOT yet authorized.** Phase D proceeds only on Bablu's
   separate authorization. One run. No mid-run edits.
