# Promise register — schema, storage, and consumption

**Status: production rubric (workflows/ item 1).** Feeds Workflow 1 (extraction,
see `WORKFLOW_1_EXTRACTION_RUBRIC.md`) and is consumed by Workflow 2 (delivery
tracking). Scores C5 (base spec §3.C) using the withdrawal rule codified in
`specs/V3_8_DELTA.md` §5. This document does not change any scored threshold
itself — C5's bands and averaging method are unchanged — it makes the promise
data those rules operate on persistent instead of re-extracted from scratch
every review round.

## 1. Schema

Each promise is one JSON object with these fields, all required unless marked
optional:

| Field | Type | Definition |
|---|---|---|
| `id` | string | Stable identifier, format `<company-slug>-<quarter>-<seq>`, e.g. `persistent-fy24q1-03`. Assigned once at creation, never reused or renumbered. |
| `company` | string | Company slug, matching the `reviews/<company-slug>/` directory name. |
| `quarter` | string | The quarter the promise was **made**, format `FYYY QN` (e.g. `FY24 Q1`). Not the horizon quarter — that's `horizon`. |
| `speaker` | string | Named individual and title, e.g. `"Sandeep Kalra, CEO"`. If the source is a written release with no named speaker, use `"management (written release)"`. |
| `metric_class` | enum | One of: `revenue`, `margin`, `eps_kpi`, `capex`, `multi_year_target`, `debt`, `etr_timeline`, `other`. Matches the extraction classes in `WORKFLOW_1_EXTRACTION_RUBRIC.md` §1. |
| `verbatim_quote` | string | The exact quoted statement, no paraphrase. If sourced from a written release rather than a call, quote the release text verbatim instead. |
| `source` | string | Call transcript / release / investor-presentation citation: document name or URL and, for calls, approximate timestamp or page. |
| `horizon` | string | The quarter or date by which the promise is to be judged, format `FYYY QN` or an explicit date. |
| `status` | enum | One of `active`, `delivered`, `missed`, `withdrawn`, `superseded`. See §2 for transition rules. |
| `status_history` | array | Append-only list of `{status, as_of_quarter, evidence}` objects — every status change ever made to this promise, oldest first. Never rewritten, only appended. |
| `resolution_notes` | string, optional | Free-text note explaining the current status, populated when status leaves `active`. |

## 2. Status transition rules

All promises start `active` at creation. From `active`, exactly one of four
transitions applies — there is no path back to `active` once left, and no
direct transition between `delivered`/`missed`/`withdrawn`/`superseded` (a
promise that changes meaning after resolution is not re-opened; see
`superseded` below for the correct handling of a promise that gets replaced by
a newer one).

- **active → delivered**: the horizon quarter's actuals are reported, **and**
  the actual metric meets or exceeds the promised metric (for a range promise,
  meets or exceeds the low end; for a "no worse than X" promise, is no worse
  than X). Evidence required: the actual figure and its source (results
  filing, earnings release), cited in `resolution_notes`.
- **active → missed**: the horizon quarter's actuals are reported, **and**
  the actual metric falls short of the promised metric, **and** no
  `withdrawn` statement (see below) was made before the horizon lapsed.
  Evidence required: the actual figure, its source, and confirmation no
  qualifying withdrawal statement exists in the intervening quarters' calls.
- **active → withdrawn**: management makes a public statement, **before the
  horizon lapses**, that explicitly revises or retracts the specific promise,
  **with a stated reason**. This is the rule from `specs/V3_8_DELTA.md` §5 —
  apply it exactly: no stated reason means the transition is `missed` once the
  horizon lapses, not `withdrawn`. Evidence required: the verbatim withdrawal
  quote and its source, cited in `resolution_notes`.
- **active → superseded**: management restates or replaces the same
  metric/horizon with a **new promise that is not framed as a revision** (e.g.
  a multi-year target that quietly stops being mentioned and a new multi-year
  target for a different period appears without any statement that the old
  one was revised). Create a **new** promise record for the new statement and
  set this field's `resolution_notes` to the new promise's `id`. Use
  `superseded` rather than `withdrawn` when there is no explicit revision
  statement — the distinguishing test is whether management said anything
  about the old promise at all: said something (even vague) about changing it
  → `withdrawn`; said nothing, just stopped repeating it and started saying
  something else → `superseded`.

**Worked example distinguishing `withdrawn` from `superseded`:** "We are
lowering our FY25 margin target from 22% to 20% given input cost inflation" →
`withdrawn` (explicit revision, reason stated). Versus: FY23 call states a
"25% ROCE by FY26" target; by FY25 that target is never mentioned again, and
the FY25 call instead states "we target 18% EBITDA margin by FY27" with no
reference to the earlier ROCE target → the ROCE promise is `superseded` (no
statement was made about it; it was replaced without acknowledgment), and a
new promise record is created for the EBITDA margin target.

## 3. Storage

- Path: `reviews/<company-slug>/promise_register.json` — one file per company,
  living inside that company's existing review directory (this document does
  not create the directory structure; it assumes `reviews/<company-slug>/`
  already exists from that company's review process, per the top-level task
  scope which does not touch `reviews/` content — the register file is new
  content added to a company's directory the next time that company is
  reviewed, not a retroactive edit to existing review files).
- Format: a single JSON array of promise objects (schema in §1), sorted by
  `quarter` ascending, ties broken by `id`.
- Git-versioned: committed to the repository like any other `reviews/`
  artifact, one commit per review round that adds or updates promises for that
  company.
- **Append-only across review rounds:** a review round may only (a) append new
  promise objects for statements made since the last round, and (b) append to
  an existing promise's `status_history` array and update its `status` /
  `resolution_notes` fields when new evidence resolves it. A review round must
  never delete a promise object or rewrite a past `status_history` entry — if
  a status was assigned in error, append a correcting entry to
  `status_history` explaining the correction rather than editing the mistaken
  entry away, so the file remains an honest record of what was believed when.

## 4. How Workflow 2 (delivery tracking) consumes it

Workflow 2's job at each review round is to move promises whose `horizon` has
been reached out of `active`, using the transition rules in §2. Instead of
re-reading every prior transcript each round:

1. Load `reviews/<company-slug>/promise_register.json`.
2. Filter to `status == "active"` **and** `horizon` at or before the current
   review's quarter — this is the entire working set for the round; every
   other promise in the file is already resolved or not yet due and needs no
   re-reading.
3. For each promise in the working set, check the current round's fresh
   inputs (this quarter's results filing and call transcript, which the
   review is already extracting for other purposes) for: (a) the actual
   metric for a promise whose horizon is this quarter, or (b) a withdrawal
   statement for a promise whose horizon is a future quarter. Resolve per §2
   and append to `status_history`.
4. Any promise still `active` with `horizon` more than one year past the
   current review's quarter and no withdrawal statement found across every
   round since it was made is flagged for manual review in
   `resolution_notes` (likely `missed` with the horizon simply never
   discussed again) rather than silently carried forward indefinitely.
5. Write the updated array back to the same file, sorted per §3, and commit.

This bounds Workflow 2's work per round to the (typically small) set of
promises actually due, rather than re-scanning the company's entire promise
history — the persistence is the fix; the transition logic itself is
unchanged from what C5 already required.
