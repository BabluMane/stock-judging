# Workflow 2 — delivery tracking

**Status: production rubric.** Delivery tracking's mechanics (what it reads,
what it resolves, what it writes back) are specified in full in
`PROMISE_REGISTER_SPEC.md` §4 — this document is a pointer, not a
duplicate, so the procedure is defined in exactly one place.

Run Workflow 2 once per review round, after Workflow 1 (extraction, see
`WORKFLOW_1_EXTRACTION_RUBRIC.md`) has appended any new promises made in the
current quarter's call/release to `reviews/<company-slug>/promise_register.json`.
Workflow 2 then resolves the due subset of `active` promises per
`PROMISE_REGISTER_SPEC.md` §4, feeding the resolved statuses into that round's
C5 score under the withdrawal rule at `specs/V3_8_DELTA.md` §5.

Order matters: Workflow 1 appends this quarter's new promises and any
withdrawal evidence for existing promises **before** Workflow 2 resolves the
due set, so a promise withdrawn in the same call whose horizon also happens to
land this quarter is correctly resolved `withdrawn` rather than `missed` —
Workflow 2 must see the withdrawal evidence Workflow 1 just extracted, not the
register state as of the start of the round.
