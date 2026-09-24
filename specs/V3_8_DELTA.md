# v3.8 spec delta — mechanical rubrics for A6, C4, C6, C3(buyback), C5(withdrawal); SCREEN-tier decision

**2026-09-24 · scope: forward-looking rubric mechanics only, no engine/entry-logic change**

Base: `EQUITY_REVIEW_V3_SPEC.md` §3 (Dimension A/C), §7 (SCREEN vs FULL) + `V3_7_DELTA.md`
(DCF entry, unchanged). This document changes only what it names; everything else,
including the v3.7 DCF-entry machinery, the historical-calibration bar (§12), and
every scored threshold not listed below, carries over unmodified.

**Why a version bump for what looks like paperwork:** A6, C4, C5(withdrawal) and
C6-retrieval were previously scored or practiced on undocumented analyst judgment.
Writing the judgment down as a rule is a scoring-logic change — it can move a
label (and therefore a score) that pure discretion would have set differently. Per
the repo's non-negotiable ("no silent edits to scored logic"), every item below is
versioned and requires the revalidation note at the end.

---

## 1. A6 quarterly trajectory — mechanical per-series labels (replaces manual "vibes")

Applies to A6 (`specs/EQUITY_REVIEW_V3_SPEC.md` §3, Dimension A). The 2/1/0 point
bands are **unchanged** ("all three improving or stably strong" / "mixed" / "2+ of
three deteriorating"). What changes: each of the three series (revenue, EBITDA
margin, CFO) now gets a mechanical **improving / flat / deteriorating** label with
zero analyst discretion. Discretion is confined to the write-up (why it happened),
never to which label attaches.

Inputs: the last **4–6 quarters** of revenue, EBITDA margin, and CFO, each compared
**YoY** (same calendar quarter, prior year) to strip seasonality — never
quarter-on-quarter, which conflates seasonality with trend.

| Series | Improving | Flat | Deteriorating |
|---|---|---|---|
| Revenue | YoY growth positive in **≥ 3 of the last 4** quarters | positive in exactly 2 of 4 | positive in ≤ 1 of 4 |
| EBITDA margin | **≥ 100 bps** YoY expansion, averaged over the last 4 quarters | between −50 bps and +100 bps | **≤ −50 bps** YoY contraction, averaged over the last 4 quarters |
| CFO | CFO YoY growth positive **or** CFO/PAT ratio strengthening (current 4-quarter CFO/PAT ≥ prior 4-quarter CFO/PAT), in ≥ 3 of the last 4 quarters | mixed — neither the improving nor the deteriorating condition met | CFO YoY growth negative **and** CFO/PAT weakening, in ≥ 3 of the last 4 quarters |

Seasonal-name rule: every comparison above is already YoY by construction (same
quarter, prior year), so no separate seasonal adjustment is needed. If a company
changed its fiscal quarter boundaries or reporting calendar within the lookback
window, use the closest calendar-equivalent quarter and flag the substitution in
the write-up; do not silently drop it from the count.

Data insufficiency: fewer than 4 quarters of comparable data available (e.g. recent
listing, restated financials) ⇒ A6 is `[unverified]`, excluded from Dimension A's
denominator per the retrieval-aware pattern already used for Dimension B (§3.B),
not defaulted to 1.

**A6 label → score:**
- All three series **improving** or **flat-and-strong** (flat with revenue growth
  ≥ 8% and EBITDA margin ≥ industry median) → **2**.
- Mixed (any combination not hitting the "2" or "0" rule) → **1**.
- **≥ 2 of 3 series deteriorating** → **0**.

**Worked example (mechanical, no judgment call left open):**
Revenue YoY: +9%, +11%, +6%, +14% (4/4 positive) → **improving**.
EBITDA margin YoY delta: +120bps, +80bps, +140bps, +60bps → average +100bps →
**improving** (at the ≥100bps line — apply §8 interpolation if the average lands
inside [90, 110] bps; here it is exactly at the threshold, so label improving,
score 2 for this series, no interpolation needed since it is not inside the
open interval).
CFO YoY growth: +5%, −2%, +8%, +3% → positive in 3/4 quarters, and current
4-quarter CFO/PAT (0.92) ≥ prior 4-quarter CFO/PAT (0.88) → **improving**.
All three improving → **A6 = 2**.

---

## 2. SCREEN-tier decision — SCREEN runs the full spec, with only the two named exceptions

**Decision (governance, resolves the spec-vs-practice gap Musey flagged): SCREEN
runs the full v3 spec.** There is no SCREEN-specific subset of dimensions or
tests. The only SCREEN-specific mechanics are the two already written into the
base spec:

1. **C5 lite mode** (§3.C: "Lite at SCREEN: last 4 quarters, weights 4→1, same
   bands — no more defaulting to 1").
2. **F5 exclusion when the marquee screen is skipped** (§3.F: F5 excluded, F
   rescales from the remaining four tests ÷8×10).

**C6 (promoter direction) and A6 (quarterly trajectory) run at SCREEN, full
weight, same as FULL.** Neither has a lite mode in the base spec, so "skip C5/C6
at SCREEN" was never a written option — it was undocumented practice diverging
from the spec, and per the governing instruction ("spec says one thing, cards do
another is the worst option") practice is the thing that changes, not the spec.
Any SCREEN card produced before this date that scored C6 as 1 (neutral) or A6 as 1
(mixed) by default rather than by evaluating the rule is not a valid SCREEN score
under this decision and must be re-run before it is cited in any review, Note, or
League Table entry — this applies to future cards; per the task scope, no existing
`reviews/` content is edited by this delta.

If a future engine version needs a genuinely cheaper SCREEN — e.g. because C6
retrieval (§6 below) is too slow to run on every SCREEN candidate — that requires
a **new, explicit SCREEN-subset clause added to the base spec's §7 with its own
version bump**, not a silent skip. This delta does not create that clause; it
closes the gap by making the written spec authoritative as-is.

---

## 3. C4 disclosure-quality — point-in-time becomes a trend

Applies to C4 (base spec §3, Dimension C). The 2/1/0 bands are **unchanged**
("Segment data, calls held, trackable guidance, no restatement" / "partial" /
"opaque"). What's added: a per-quarter observables checklist and a **delta rule**
that turns the point-in-time judgment into a trend, per the review's "almost no
new machinery" framing.

**Per-quarter checklist (five yes/no observables, recorded every quarter):**
1. Segment-level revenue/margin disclosed (not just consolidated)?
2. Earnings call held (not just a written release)?
3. Call transcript or recording publicly available?
4. Previously-disclosed KPI or guidance metric silently retired (no longer
   reported, no explanation)?  — **note: "yes" here is a loss**, i.e. it
   counts against disclosure quality, unlike observables 1–3 where "yes" is
   good. Score it inverted: retired = lost.
5. Restatement of a prior period's financials this quarter?  — same inversion:
   a restatement is a loss.

**Delta rule:** compare the current quarter's checklist to the prior quarter's.
- **Deterioration** = net observables lost (any of 1–3 flips yes→no, or 4/5
  flips no→yes) exceeds net observables gained, over the trailing 4 quarters.
- **Improvement** = net gained exceeds net lost over the trailing 4 quarters.
- **Stable** = net gained equals net lost (including the common case of zero
  change both ways).

**C4 label → score**, combining the point-in-time base spec bands with the trend:
- Base spec band is "2" (segment data + calls + trackable guidance + no
  restatement) **and** trend is stable or improving → **2**.
- Base spec band is "2" but trend shows deterioration in the trailing 4
  quarters (an observable was lost even though the current-quarter snapshot
  still clears the "2" bar) → **1** — the trend downgrades a clean snapshot,
  because a name mid-slide toward opacity is not equivalent to one that has
  been consistently transparent.
- Base spec band is "1" (partial) → **1** regardless of trend direction (there
  is no room below 1 for "partial but improving" under the unchanged base
  bands; trend among partial-disclosure names is noted in the write-up, not
  scored, until a future version adds a fourth band).
- Base spec band is "0" (opaque) → **0**.

Fewer than 2 quarters of checklist history (new coverage) ⇒ trend is
`[unverified]`; score on the point-in-time band alone and flag the missing
trend as a follow-up, same retrieval-aware pattern as Dimension B.

---

## 4. Buyback tracking — three structured fields, C3 sub-rule

Applies to C3 (base spec §3, Dimension C: "Capital allocation, 5 yrs"). C3's
2/1/0 bands are unchanged. Buybacks were one unstructured input inside C3's
judgment call; this delta makes buyback execution quality mechanical, porting the
USA pathway's diluted-share-bridge concept (base spec §11 references the USA
pathway as the same v3 architecture with a different macro block; the bridge
concept — track shares outstanding before and after against the announced
authorization — applies unchanged to the Indian pathway).

**Three fields, tracked per buyback program, per company, alongside the promise
register (§ below — same storage pattern, same file):**

| Field | Definition | Source |
|---|---|---|
| `announced_amount` | Board-approved buyback size in ₹ Cr (or % of net worth, whichever the announcement states — record both if both are stated) | Board/exchange announcement |
| `executed_value` | Cumulative ₹ Cr actually spent, as of the review date, from exchange disclosures (BSE/NSE buyback status reports) or the subsequent annual report | Exchange buyback closure filing |
| `avg_execution_price` | `executed_value ÷ shares bought back`, from the same closure filing | Exchange buyback closure filing |

**C3 sub-rule (buyback component only — combine with the existing M&A/dividend
judgment for the overall C3 band, do not let buyback execution alone move C3
outside the band the other capital-allocation evidence supports):**
- `avg_execution_price` **below** the conservative DCF fair value at the time of
  execution (the same D1 conservative-DCF midpoint the review already computes,
  §4.1) → buyback execution is **supportive** — retiring shares below fair value
  is accretive to remaining holders.
- `avg_execution_price` **above** that conservative ceiling → buyback execution is
  **destructive** — the company spent cash to retire shares above what its own
  conservative valuation says they were worth, i.e. the same test as overpaying
  for an acquisition.
- If `executed_value` is materially below `announced_amount` (< 50% executed by
  the authorization's expiry) with no stated reason, note it as a credibility
  observation feeding C5 (promise vs. delivery — an announced-but-unexecuted
  buyback is exactly the kind of promise the promise register tracks, see § below)
  rather than scoring it inside C3.

**Diluted-share bridge (ported from USA pathway):** for any company running a
buyback, report shares outstanding at the start and end of the trailing 12
months, split into the reduction attributable to the buyback vs. any offsetting
issuance (ESOP exercises, warrant conversion, QIP/preferential allotment). A
buyback that is fully offset by fresh issuance nets to zero share-count reduction
and should be reported as such, not credited as if it were accretive.

---

## 5. C5 "withdrawal = honest (1)" — codified as an explicit rule

Applies to C5 (base spec §3, Dimension C: "Credibility audit (promise vs
delivery)"). This closes the "silent precedent" flagged in
`workflows/CLAUDE_WORKFLOWS_REVIEW_20260923.md` item 2 — the rule is now written,
not inferred from past practice.

**Rule:** when scoring an individual promise inside the C5 promise-vs-delivery
average (base spec §3.C, "C5 method"), a promise that management **explicitly
and publicly withdrew or revised before its stated horizon**, with a stated
reason, scores as **1 (partial/honest)**, not 0 (broken) and not excluded from
the denominator. Rationale: withdrawing a guidance number ahead of the deadline,
with a reason given, is a different act of governance than silently missing it —
it is worse than delivering (2) but materially better than an unexplained miss
(0), and averaging it in at 1 reflects that without either rewarding the miss or
punishing the disclosure.

**Distinguishing withdrawn from missed, in the promise register's terms (see
schema below): a promise is `withdrawn`, not `missed`, only if** management
made a public statement revising or retracting the specific promise **before**
the promise's stated horizon lapsed, **and** the statement cites a reason
(demand environment, regulatory change, M&A, etc. — any stated reason qualifies;
"no reason given" does not). A promise whose horizon simply lapses with no
delivery and no withdrawal statement is `missed` (scores 0), full stop — silence
past the horizon is not a discretionary call.

**Worked example:** FY24 guidance of "18-20% revenue growth" stated at Q1 FY24
call; at Q3 FY24 call management says "we are revising full-year growth guidance
to 10-12% given a slower-than-expected export recovery." This is `withdrawn`
(stated reason, before horizon) → scores **1** in the C5 average. Contrast: same
guidance, no Q3 mention, FY24 actual growth comes in at 11% → `missed` (horizon
lapsed, no withdrawal statement) → scores **0**, even though the same slower
export environment might explain the miss — C5 scores disclosure behavior, not
whether the underlying cause was sympathetic.

---

## 6. Revalidation note

None of the above changes the v3.7 DCF-entry machinery, the tier/gate logic
(§2, §6), or the historical-calibration bar (§12) — this delta touches only A6,
C4, C5(withdrawal-only), C3(buyback-only), and the SCREEN/FULL test coverage
decision. Per §12's calibration protocol, the blocking bar is scored on tier
outcomes (INVEST AT TRIGGER or better on winners, PASS on blow-ups), which are
far more sensitive to Dimension D/E (valuation, entry) than to A6/C4/C6/C3
labels feeding Dimension A/C — **so this delta does not by itself require a
re-run of the §12 historical-calibration set.** It does, however, change what a
future calibration run will score for A6/C4/C6/C3 on those 25 names relative to
whatever undocumented judgment produced the existing (pre-v3.8) scores for those
tests — so the next full calibration re-run (whenever §12 is re-triggered for any
other reason, e.g. a future DCF-entry change) **must** re-score A6/C4/C6/C3 under
this delta's mechanical rules rather than carrying forward the old judgment-based
labels, and must note in its report if that changes any name's tier.

**v3.8 does not touch:** `engine/`, `validation/`, `leaderboard.json`,
`frontend/`, or any `reviews/` content file. It amends `EQUITY_REVIEW_V3_SPEC.md`
by addition only (this delta document); the base file itself is not edited, per
the "frozen except via version bump" rule — a version-bump amendment is exactly
this kind of dated delta document, same pattern as `V3_7_DELTA.md`.
