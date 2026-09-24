# Workflows — DRAFT

Status: **DRAFT**. The two review documents below are the Claude-built workflow
specs as of 2026-09-23. The fixes required before any real automated company
review are tracked below; all have now landed as of 2026-09-24
(`specs/V3_8_DELTA.md` + the new `workflows/` documents listed under Contents).

1. **Promise register** — DONE. Schema, storage, and Workflow-2 consumption
   pattern written in `PROMISE_REGISTER_SPEC.md`.
2. **A6 thresholds** — DONE. Mechanical per-series label rules in
   `specs/V3_8_DELTA.md` §1; quarterly update procedure in
   `WORKFLOW_3_QUARTERLY_QUALITY.md` §1.
3. **SCREEN-tier decision** — DONE. Decided and written in
   `specs/V3_8_DELTA.md` §2: SCREEN runs the full spec; the only SCREEN-specific
   mechanics are C5 lite mode and F5 exclusion, both already in the base spec.
4. **C4 trend checklist** — DONE. Five-observable checklist + delta rule in
   `specs/V3_8_DELTA.md` §3; quarterly procedure in
   `WORKFLOW_3_QUARTERLY_QUALITY.md` §2.
5. **Buyback fields** — DONE. Three structured fields + C3 sub-rule +
   diluted-share bridge in `specs/V3_8_DELTA.md` §4.

Also resolved in this pass (flagged by the review, not originally itemized
above):

6. **Promoter retrieval/netting procedure** — DONE. BSE/NSE retrieval,
   promoter-group netting, inter-se/ESOP/warrant exclusion procedure in
   `WORKFLOW_4_PROMOTER_ACTIVITY.md`. The C6 counting rule itself is
   unchanged.
7. **Workflow 1 extraction rubric + withdrawal precedent** — DONE. Guidance
   classes (including debt path and ETR/timelines) in
   `WORKFLOW_1_EXTRACTION_RUBRIC.md`; "withdrawal = honest (1)" codified as an
   explicit rule in `specs/V3_8_DELTA.md` §5, with the withdrawn/missed/
   superseded distinction in `PROMISE_REGISTER_SPEC.md` §2.

This directory stays **DRAFT** until a review is actually run end-to-end
against these rubrics and confirmed workable — the DRAFT banner tracks
"exercised in production," not just "written down." Remove the banner only
after that first live run.

## Contents
- `CLAUDE_WORKFLOWS_REVIEW_20260923.md` — Musey's review of the Claude workflows
- `CLAUDE_REVIEW_RESPONSE_20260923.md` — Claude's response / corrections
- `PROMISE_REGISTER_SPEC.md` — item 1: schema, storage, Workflow-2 consumption
- `WORKFLOW_1_EXTRACTION_RUBRIC.md` — item 7: extraction rubric + withdrawal
  precedent pointer
- `WORKFLOW_2_DELIVERY_TRACKING.md` — delivery-tracking procedure (pointer to
  `PROMISE_REGISTER_SPEC.md` §4)
- `WORKFLOW_3_QUARTERLY_QUALITY.md` — items 2 and 4: A6/C4 quarterly update
  procedures (pointers to `specs/V3_8_DELTA.md` §1/§3)
- `WORKFLOW_4_PROMOTER_ACTIVITY.md` — item 6: C6 retrieval/netting procedure,
  plus a pointer to buyback tracking (item 5, in `specs/V3_8_DELTA.md` §4)

See `specs/V3_8_DELTA.md` for every spec-level rule change (A6, C4, C5
withdrawal, C3 buyback, SCREEN-tier decision) and its revalidation note. The
base spec `specs/EQUITY_REVIEW_V3_SPEC.md` is not edited — it stays frozen per
the version-bump rule; `V3_8_DELTA.md` is the amendment.
