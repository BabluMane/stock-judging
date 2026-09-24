# STATE.md — repo state log

Append an entry after every piece of repository work. Newest at bottom.

## 2026-09-24 — Phase 1 port bundle assembled
- Ported engine_v3.py, engine_v2.py, input_schema_v3.json,
  sample_input_v3.json, standard_v3_scoring_spec.md, test_engine_v3.py →
  `engine/` (engine_v3 audited 59/59 passing before port).
- Ported specs: EQUITY_REVIEW_V3_SPEC.md, V3_7_DELTA.md, AUDIT.md,
  CLAUDE_WORKFLOWS_REVIEW_20260923.md, CLAUDE_REVIEW_RESPONSE_20260923.md,
  V3_7_USABILITY_CORRECTED_20260923.md, V3_7_DCF_REVALIDATION_20260923.md →
  `specs/`.
- Workflows dir seeded from review/response docs, marked DRAFT — rubric fixes
  (promise register, A6 thresholds, SCREEN-tier decision, C4 trend, buyback
  fields) still pending.
- Stubs created: data/, reviews/ (with review_card.schema.json stub),
  frontend/, leaderboard.json (empty seed).
- v3 status: NOT LIVE. No investable calls until the live bar passes.

## 2026-09-24 — Frontend v1 built (`claude/frontend-v1` branch)
- Step 0 check on the ported tree: 58/59 engine_v3 tests pass. The one
  failure (`test_v2_engine_still_runs`) is `FileNotFoundError` for
  `engine/sample_input_v2.json`, a v2 fixture never included in the Phase 1
  port — not an engine_v3 logic bug. Flagged to Bablu; proceeded to frontend
  work per his direction.
- Built `frontend/`: static, no-build-step HTML/CSS/vanilla JS (no
  framework — justified in `frontend/README.md`). Pages: `index.html`
  (leaderboard, sortable + filterable), `best-overall.html`
  (conviction-ranked), `best-today.html` (conviction × distance-to-trigger,
  v3.7 entry tiers), `company.html` (review card, score breakdown, promise
  tracker, thesis, risks, inline-SVG price-vs-trigger chart), `run.html`
  (company input → downloads a run-request file, local queue tracker).
  Shared `css/styles.css` (category-color tokens) and `js/data.js`
  (fetch/normalize, shared across pages).
- `leaderboard.json` and `reviews/` untouched — every page currently renders
  its honest empty state ("no reviews yet"), verified against real (empty)
  data; a throwaway local fixture was used during development to verify
  rendering/sorting/interactions, then discarded before commit.
- Added `runs/queue/` (+ `runs/README.md`) as the chosen run-request path;
  documented as a phase-4 proposal, not a locked spec.
- Schema gaps flagged in `frontend/README.md` (not invented): no confirmed
  `quality`/`composite` field names in `scores` (inferred from
  `engine_v3.py`'s `q_score`/`p_score` as `Q`/`P_today`), no numeric
  margin-of-safety field (derived client-side from `dcf.fair_value` vs.
  `dcf.current_price`), no trigger-history series field for the chart, no
  `promises` item shape.
- Validated: zero console errors on load and on every sort/filter/link
  interaction, on both `file://` and `python3 -m http.server`, desktop and
  mobile viewports (Chromium via Playwright). Fixed two bugs found in
  review: a double-escaped `&minus;` entity rendering literally in trigger
  labels, and the score-breakdown panel overflowing off-screen on mobile
  (was a fixed-width table cell; rebuilt as a flexible row layout).
- Every page carries the PROVISIONAL / v3-not-live banner; no live
  execution hooks anywhere.
