# V3.7 usability — conformance check and resolved conventions

**2026-09-24 · conformance pass against `V3_7_USABILITY_CORRECTED_20260923.md` §4.1/§4.2**

Scope: this document does not change the frozen 26-name usable set and does not
re-run usability. It (1) resolves four conventions the corrected-series rerun
left implicit rather than stated as a rule, so the same rule can be applied
mechanically to the OOS set without re-deriving it per name, and (2) records
the conformance check against the spec text itself (`V3_7_DELTA.md` §4,
`V3_7_USABILITY_CORRECTED_20260923.md` §4.1/§4.2). No method changes. Where
the rerun deviates from the spec, the spec wins and the deviation is reported
here, not silently corrected.

## Verdict

**Conforms**, with one disclosed data-substitution the rerun already flagged
and this document now makes a standing rule (§2 below) rather than a
per-name judgment call. No new deviation found.

---

## 1. Persistent-style residual (ESOP / share-count basis)

**Question:** when audited FY EPS restated for splits/bonuses still disagrees
with the vendor series by a small, *constant* factor across years (Persistent:
audited÷sourced ≈ 2.09–2.10×, vs the pure 2.0× split factor — a ~1.045×
residual), does that residual get corrected, or documented and left alone?

**Resolution (standing rule):** **restate audited EPS only for splits and
bonuses; never for anything else.** A residual ratio is diagnosed by
recomputing the audited÷sourced ratio at ≥ 2 independent points in time
(different years). If the ratio is constant (±2pp) across those points, it is
a *basis convention difference* (ESOP/diluted-share-count treatment, or a
similar constant offset between the audited and vendor series) — it is
**documented as a named residual factor and left uncorrected**, because it
cancels in the fair-price = EPS × multiple math the usability check and the
DCF/anchor math both do. If the ratio drifts between years, it is **not**
a basis issue — it is either genuine earnings growth/decline (§2 below) or a
vendor data defect, and is handled there instead.

**Why not "correct" the residual:** picking the basis that makes a name-date
pass would be re-deriving the test around the desired outcome — exactly what
`V3_7_DELTA.md` §4.1 rules out ("fix by preregistered rule which basis is
authoritative … never by choosing whichever basis passes"). The rule is
fixed once, before looking at which names it passes.

**Conformance:** the rerun applied this correctly for Persistent 2021
(audited ₹58.97 ÷ 2 for the 1:2 split only = ₹29.485; the further ~1.045×
gap to the v3.6-stored ₹28.26 is named, not corrected — `corrected series`
doc §"Sensitivity"). **Confirms.**

---

## 2. Off-FY scoring dates

**Question:** check (a) is defined "at FY results week." Roughly a third of
the 50 name-dates score mid-year, at quarter-ends, or essentially at FY-end
itself (before that year's results are even out) rather than shortly after a
results announcement. Which FY does the check reference, and what happens
when results for that FY aren't out yet at the scoring date?

**Resolution (standing rule):**
1. Identify the **most recently completed fiscal year as of the scoring
   date** — the FY whose FY-end date is ≤ the scoring date. This holds even
   when the scoring date sits on or within days of that FY-end, before
   results are declared (e.g. `trent_2019-03-29`, `manpasand_2016-05-20`
   scored ~3–6 weeks before their FY's results week).
2. Check (a) is evaluated at **that** FY's results week (median TTM over
   results-week..+21d on the unlagged, publication-dated series), never
   rolled forward to the following FY even if the scoring date is much
   closer to the next FY's results.
3. If the scoring date falls **before any FY the company has reported has a
   results week reachable in the series** — i.e. no PIT EPS observation
   exists at or before the scoring date at all — the name-date is EXCLUDED
   as structurally unusable ("no PIT EPS at date"), not scored against a
   future FY and not rolled back to an older FY that predates the intended
   entry window.
4. Financial-variant names (banks/NBFCs scored on the excess-return/DDM
   model, not EPS) are exempt from check (a)/(b) entirely — this was already
   explicit in the frozen set (`bajfin`, `lichf`, `yesbank`: "no EPS test").

**Conformance:** matches the rerun's actual treatment — `trent_2019-03-29`
was checked against FY19's results week (pub 2019-04-29) despite scoring
essentially at FY19-end; `manpasand_2016-05-20` against FY16's results week
(pub 2016-06-30) despite scoring 6 weeks earlier; `manpasand_2015-07-09` and
`vakrangee_2013-06-03` were excluded structurally (no PIT EPS at date) rather
than checked against a stale prior FY. **Confirms.**

---

## 3. Check (b): what counts as a "certified" / explained step

**Question:** check (b) excludes a name-date on an unexplained implied-EPS
step of > 8% "outside a results window." How wide is that window, and what
"certifies" a step as explained rather than unexplained?

**Resolution (standing rule):** a step is **explained** — and does not fire
check (b) — iff it falls within **±30 calendar days of a confirmed EPS
publication event** in the company's own quarterly/annual results calendar
(sourced from the EPS dataset or filing calendar, not inferred from the
price/PE quotient series alone). A step outside that ±30-day window, or one
inside the window but not corroborated by an actual results publication on
record, is **unexplained** and fires (b).

This is the rule the rerun already applied in practice: APL Apollo 2018's
+50.5% step (quotient dated 2017-12-15) was reclassified EXPLAINED because
the EPS dataset shows a genuine +50.5% Q2FY18 results jump on 2017-12-11 — 4
days inside the window, i.e. a dating artifact of the quotient series, not a
real anomaly. Deepak Nitrite 2018's −10.4% step was left UNEXPLAINED because
no EPS publication exists within 30 days of it.

**Note on precedence:** in the frozen set, every case where check (b) would
fire is also independently excluded by check (a) — so (b) has never yet been
the sole reason for an exclusion. For the OOS set this will not necessarily
hold; (b) is applied as its own independent check per this rule, not treated
as redundant by default.

**Conformance: confirms**, now stated as a standing rule instead of a
per-case judgment.

---

## 4. Same-basis / timing implementation (the mechanical algorithm)

**Question:** `V3_7_DELTA.md` §4.1 point 1 states the principle ("assert a
common basis first, transform only the non-conforming side") at a level a
rerun could satisfy several different ways. What is the exact algorithm the
rerun used, so it can be applied identically to new names?

**Resolution (standing rule) — the algorithm, stated explicitly:**
1. **Basis:** name the corporate-action basis explicitly per company (e.g.
   "post the 2024-03-28 1:2 split"). Pull every split/bonus 2010→T for the
   name. Determine whether the **vendor (Screener) series** is already
   retroactively adjusted for a given action (it usually is — Screener
   back-adjusts its chart series) — if so, that series defines the named
   basis. Restate the **sourced/audited** EPS onto that same basis by
   dividing by the cumulative split/bonus factor for every action whose
   ex-date is between the FY-end being tested and "today." Never restate the
   vendor series backwards to an as-was basis — always transform the sourced
   side onto the vendor's basis, per §4.1 point 1's "transform only the side
   that isn't on it."
2. **Constancy check:** after restatement, compute audited÷sourced (or
   sourced÷vendor-implied) at ≥ 2 years. If constant, it's a basis residual
   (→ §1 above). If not constant, treat as timing (below) or a vendor defect.
3. **Timing:** identify the FY's **results week** from the **unlagged**,
   publication-dated EPS series — never from the 63-day-PIT-lagged series,
   whose calendar position is shifted 63 days from the real publication date
   and would misidentify which price/PE points belong to "results week."
   Compare the median TTM over results-week..+21d (unlagged) against the
   basis-normalized sourced FY EPS. This is what makes TTM == FY "by
   construction" — comparing at any other point injects a partial quarter of
   growth/decline from the following period, which is exactly the v3.6
   defect this fix targets.
4. **Tolerance:** ±15%, unchanged, applied after steps 1–3, never before.

**Conformance:** this is exactly the sequence documented in
`V3_7_USABILITY_CORRECTED_20260923.md` (§"Corrected PIT EPS series" +
per-name notes) and `V3_7_USABILITY_RERUN_20260923.md` §1/§6. **Confirms.**

---

## 5. One disclosed deviation, now made a standing rule (not a new finding)

The rerun's "sourced FY EPS" for most of the 50 name-dates was **back-solved
from the 63-day-lagged `eps_pit` at the v3.6 check dates**, not re-sourced
independently from fresh annual-report retrieval — because the original
`v3.6/inputs/` bundle (the scored input JSONs) is absent from this repository
(confirmed again here: `find . -iname "*input*"` under this checkout returns
only the engine's schema/sample files, no per-name scored inputs). This was
already disclosed in `V3_7_USABILITY_RERUN_20260923.md` §6 ("Estimated
normalization") and is **not** a new deviation from spec — the spec's basis
algorithm (§4 above) was still applied; only the *source* of one input
(sourced FY EPS, for names other than Persistent 2021 and Astral, where
ground-truth audited/normalized values were used directly) is a
best-available proxy rather than a fresh primary pull.

**Standing rule for the OOS set (§4, task step 4):** no such proxy is
available for genuinely new names — there is no v3.6 back-solve to fall back
on. Every OOS name-date's sourced FY EPS must come from a primary source
(company annual report / exchange filing / audited financials), never
back-solved from the vendor series itself (that would make check (a)
circular — comparing the vendor series to itself). This is not a change to
the check; it closes the one avenue the frozen-set rerun had to use out of
necessity and the OOS set does not.

---

## 6. Summary table

| # | Convention | Resolution | Conforms? |
|---|---|---|---|
| 1 | Persistent-style ESOP/share-count residual | Restate only for splits/bonuses; constant residual → document, never correct | Yes |
| 2 | Off-FY scoring dates | Reference the most-recently-completed FY as of the scoring date, checked at that FY's results week; no PIT EPS at all → structural exclusion | Yes |
| 3 | Check (b) certification window | ±30 days of a confirmed EPS publication event certifies a step as explained | Yes |
| 4 | Same-basis/timing algorithm | Basis-normalize sourced EPS onto the vendor's (already-adjusted) basis; identify results week from the unlagged series; compare at results-week..+21d; ±15% | Yes |

No threshold, tolerance, or window value was changed. Gate M and Guardrail V
remain retired and are not referenced by any of the above.
