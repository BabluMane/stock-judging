# Musey's review of Claude's four-workflow audit (2026-09-23)

## Spot-check: consistent with the v3 spec
- C6 (promoter direction) and A6 (quarterly trajectory) exist in
  `EQUITY_REVIEW_V3_SPEC.md` as new v3 tests, with the C6 counting rule
  (open-market + block/bulk; exclude ESOP/warrant/inter-se) and the
  −0.5%/+1.0% ladder + ₹50 Cr override. Claude's description matches.
- The spec-vs-practice gaps he flags (SCREEN cards skipping C5/C6 against
  the v3.5 "no more defaulting to 1" line; live v2 reviews not carrying
  A6/C6) are stated precisely. They are governance issues: **either change
  the spec or change practice, and write the decision down.** Spec says
  one thing while cards do another is the worst option.

## Where I'd sharpen or add

1. **Workflow 1 extraction rubric — cheap fix.** The USA file already
   lists the minimum guidance classes (revenue, margin, EPS/KPI, capex,
   multi-year targets). Port that list to the Indian pathway, plus debt
   path and ETR/timelines which the Indian reviews already extract in
   practice. A 10-line rubric addition, not a research project.
2. **"Withdrawal = honest (1)" is precedent, not a rule.** Codify it in
   the spec or stop doing it. Silent precedent is how backtests lie.
3. **A6 labels need thresholds.** Propose per-series definitions, e.g.:
   revenue improving = YoY growth positive in ≥3 of last 4 quarters;
   margin improving = ≥100bps EBITDA-margin expansion over 4 quarters;
   CFO improving = CFO growth or CFO/PAT strengthening; YoY comparison
   for seasonal names. Without this, A6 is three vibes driving 1/6 of
   dimension A.
4. **C4 trend — cheapest real fix.** Record C4 observables per quarter
   (segments disclosed? call held? transcript available? KPI retired?
   restatement?) and score the *delta*: deterioration = observables lost.
   A trend with almost no new machinery.
5. **Buyback tracking — three fields.** Announced amount, executed value,
   average execution price; C3 sub-rule: executed below the conservative
   ceiling = supportive, above = destructive. Port the USA diluted-share
   bridge concept to the Indian pathway.
6. **Promise register — highest-leverage build.** Schema: company,
   quarter, speaker, metric class, verbatim quote, horizon, status
   (active/delivered/missed/withdrawn/superseded). Persist per company
   across chats. Kills the re-read-everything tax and makes Workflow 2
   continuous instead of episodic.

## Priority order (my recommendation)
1. Promise register schema + storage — unlocks everything downstream.
2. A6 label rubric — removes the biggest judgment hole in a scored test.
3. SCREEN-tier decision — spec or practice, pick one, write it down.
4. C4 trend checklist + buyback fields — small additions.
5. "Fidelity" aggregation — explicitly defer; the components are enough
   if each is honest.

## What I did not do
- Did not rewrite any scoring logic (C1/C6 ladders, credibility
  weighting/banding, trend_score) — Claude's to change, with calibration
  evidence.
- Did not verify the Record §9 tables or the screen cards (his project
  files, not available locally).
- v3 remains NOT LIVE; none of this is gated on the Path A/B/C decision.
