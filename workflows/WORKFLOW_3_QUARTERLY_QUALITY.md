# Workflow 3 — quarterly quality tracking (A6 + C4)

**Status: production rubric (workflows/ items 2 and 4).** This is the
operational workflow that runs each quarter to keep the two per-quarter
inputs current: A6's three trend series and C4's disclosure-observables
checklist. The mechanical rules themselves — the actual thresholds and labels —
are specified in `specs/V3_8_DELTA.md` §1 (A6) and §3 (C4); this document does
not restate or alter those rules, it specifies what to do with them each
quarter.

## 1. A6 — quarterly update procedure

Each quarter, for each covered company:

1. Pull the quarter's YoY revenue, EBITDA margin, and CFO figures from the
   results filing (same source the review already extracts financials from —
   no new data source).
2. Append the quarter to that company's rolling 4-6 quarter window (drop the
   oldest quarter once the window exceeds 6).
3. Apply the mechanical label rules in `specs/V3_8_DELTA.md` §1 exactly — no
   analyst override on the label. If the analyst disagrees with what the
   mechanical label implies about business quality, that disagreement goes in
   the review's prose (A6's write-up), never into a different label.
4. Record the resulting label (`improving` / `flat` / `deteriorating`) per
   series, and the combined A6 score (0/1/2 per `specs/V3_8_DELTA.md` §1), in
   the review's scorecard for that quarter.

## 2. C4 — quarterly checklist procedure

Each quarter, for each covered company:

1. Answer the five checklist observables in `specs/V3_8_DELTA.md` §3 from that
   quarter's results filing and call (segment disclosure, call held,
   transcript available, KPI retired, restatement).
2. Compare to the prior quarter's answers; compute the delta (gained vs. lost)
   per `specs/V3_8_DELTA.md` §3's delta rule.
3. Record both the point-in-time band (2/1/0 from the base spec's C4 test) and
   the trend-adjusted score (per the delta rule) in the review's scorecard.
4. Store the raw five-observable checklist for the quarter alongside the
   promise register, in `reviews/<company-slug>/c4_checklist.json`, as an
   append-only array of `{quarter, segment_disclosed, call_held,
   transcript_available, kpi_retired, restatement}` objects — one object per
   quarter, never rewritten, so the next quarter's delta calculation has the
   prior quarter's answers on file rather than needing to re-derive them from
   old transcripts.

## 3. Why these two live together

A6 and C4 are the two "cheap fix" items the review identified as needing
almost no new machinery beyond a checklist and a comparison to the prior
quarter — unlike the promise register (Workflow 1/2) or promoter-activity
retrieval (Workflow 4), neither needs external data sources beyond what the
review already pulls for financial analysis. Running them as one quarterly
pass, immediately after extracting the quarter's financials, is the natural
sequencing; this document exists to make that sequencing explicit rather than
leaving A6/C4 updates to be reconstructed from scratch by an implementer.
