# V3_9 DELTA — spec changes after the v3.8 OOS live-bar FAIL

**Status: APPROVED 2026-09-26. Not validated.**
**Date:** 2026-09-26. **Parent:** v3.8 (v3.7 + rubrics). Base spec untouched.

## Why this delta exists

v3.8 OOS (25 fresh name-dates, one run, no refit) FAILED the live bar:
blow-up fills 3 (bar 0), winner names 2 (bar ≥3). Per V3_7_DELTA.md §5 the
failure returns to the spec document, not the parameter grid.

Two independent structural causes, two asymmetric spec fixes, pre-registered
**together** below. Gate M, Guardrail V, and the own-multiple anchor stay
dead — nothing here resurrects them.

**Anti-fitting discipline:** no threshold below was chosen by looking at the
v3.8 OOS outcomes. Values are round structural choices from
practitioner/literature standards. This draft was NOT backtested against the
v3.8 set — doing so would be fitting to the observed failure. The rules earn
their place on fresh OOS data (Phase 2/3) or not at all.

## §1 — Quality-gated fair-value entry tier (QFV)

**Problem fixed:** DCF-only entry never buys genuine compounders that never
discount 12.5–30% below fair value (Titan, Page Industries, DMart filled zero
legs in v3.8 OOS). This is a design omission, not a parameter problem.

### 1.1 Extreme-quality definition (pre-registered, ALL must hold, PIT)

A name is QFV-qualified at a scoring date iff, on audited trailing-5-FY data:

- **(a) Profitability:** median ROIC over trailing 5 FYs ≥ **15%**, with no
  single FY below **10%**. (Standard: Fundsmith/Buffett-style consistent
  earning power; 15% is the practitioner round bar, not fitted.)
- **(b) Cash conversion:** median (operating cash flow ÷ PAT) over trailing
  5 FYs ≥ **0.85**, with PAT > 0 in all 5 FYs (a near-zero PAT makes the ratio
  meaningless — such a name is not QFV-qualified, no exceptions).
- **(c) Leverage:** Debt ÷ Equity ≤ **0.5** at the scoring-date balance sheet.
- **(d) Size/liquidity:** market cap ≥ ₹5,000 cr at scoring date — the tier
  is for established compounders, not small-cap discovery.

All four are AND-gated. Any single failure → not QFV-qualified (ACC/INV tiers
still available on their own terms).

### 1.2 Entry rule

- QFV-qualified AND first weekly close at or below **1.00 × DCF fair value**
  → fills one QFV leg. No discount required, no premium allowed.
- ACC (0.875×) and INV (0.70×) tiers unchanged and still available to every
  name including QFV-qualified ones.
- One leg per tier per name-date, same fill mechanics as v3.7.

### 1.3 Discount highlighting (reporting rule, not a gate)

Review cards must display, per filled leg: entry tier (QFV / ACC / INV),
fill price vs DCF fair value, and discount depth. ACC/INV fills are labeled
**discount entries**; QFV fills are labeled **fair-value entries**. The
distinction is always visible — never buried.

## §2 — Governance-event veto (GEV)

**Problem fixed:** DCF-only entry bought PC Jeweller twice on clean-looking
audited filings while the news tape carried governance red flags. Filings
cannot catch fraud-by-future-events; the news tape is the surviving defense.
This is a new data class, not a new parameter.

### 2.1 Event taxonomy (pre-registered, closed list)

A qualifying event is a dated, sourced occurrence in any of:

1. **Regulatory probe/action:** SEBI/ED/SFIO probe, show-cause notice, or
   enforcement against the company, its promoters, or KMP.
2. **Auditor events:** auditor resignation, or qualified/adverse audit opinion.
3. **Promoter conduct:** off-market transfers/gifts of promoter shares;
   pledge invocation disclosures.
4. **Withdrawn capital actions:** announced-then-withdrawn buyback, dividend,
   or fundraise.
5. **Criminal/legal:** arrest, charge-sheet, or conviction of a promoter/KMP.
6. **Associate contagion:** regulatory action against a named associate/group
   company where the link is documented in the company's own filings or in
   the regulatory order itself — never inferred from press juxtaposition.

### 2.2 Veto rule

Any qualifying event with event-date inside the **trailing 12 months** before
a scoring or fill date → **no entry on any tier**. The veto is evaluated at
the scoring date AND re-evaluated at each fill date — an event landing
between scoring and fill blocks the fill. The veto is absolute.

### 2.3 Cooling-off

The block persists until **12 months after the event date AND one audited
annual earnings print published after the event**, whichever is later.
Then the name becomes eligible again on normal terms.

### 2.4 Precedence

GEV overrides everything: QFV, ACC, INV. No tier bypasses the veto. This is
the pre-registered answer to the separation question — expensive quality
enters through the §1 gate; distressed governance is blocked by §2 even when
the filings look clean.

### 2.5 Data input (new plumbing)

Per-company dated governance-event log. Sources: BSE/NSE exchange filings +
national business press. Each event tagged to the §2.1 taxonomy with a source
link. **Honest status:** until this feed exists in the pipeline, GEV is
specified but not operable. Building it is Phase 4 work (backend-data-engineer).

## §3 — Unchanged

- **Live bar:** 0 blow-up fills (hard) · ≥3 distinct winner names ·
  to-T clearly positive · 24m ≥0.8×. Bablu confirmed 2026-09-26: the bar
  stays hard; "0 screenable blow-ups" is rejected as a weakening.
- Dead designs stay dead (own-multiple anchor, Gate M, Guardrail V).
- One run, no refit, per V3_7_DELTA.md §5.

## §4 — v3.9 validation protocol (Phase 2/3)

- Fresh OOS name-date set, zero overlap with in-sample frozen set and v3.8
  OOS set, pre-registered before the run (OOS_SET_PREREG_v39.md).
- Report per-component hit rates: QFV fills by name; GEV vetoes by name with
  the cited event; ACC/INV fills as before.
- Honest reporting requirement: state plainly which blow-ups GEV would NOT
  have caught (leg-1-type fraud-by-future-events is the known residual risk —
  carried openly, not hidden).

## §5 — Known residual risk

A fraud whose filings are clean AND which has no governance news at scoring
time (PCJ leg-1, mid-2017) passes every rule in this spec. That is not a
defect to patch with a fitted rule — it is the boundary of what any
pre-registered screen can do, and the hard 0-blow-ups bar prices it in.
