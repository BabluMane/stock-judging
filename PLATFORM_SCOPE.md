# Stock-Judging Platform — Build Scope

## What we're building
One GitHub repo + Claude Code + a frontend. You type a company name → a cloud
session runs the full research stack on all our metrics → review card committed
→ leaderboard updated. Two headline answers always visible: **best overall**
and **best to invest in TODAY**.

## Components

### 1. Repo (new, private)
- `engine/` — engine_v3.py, input schemas, test suite (existing, audited 59/59)
- `specs/` — v3 spec, v3.7 delta, scoring spec, all versioned in git
- `workflows/` — the four research workflows as agent playbooks: concall
  promises, delivery tracking, quarterly quality, promoter activity — plus the
  rubric fixes: A6 label thresholds, promise register schema, SCREEN
  spec-vs-practice decision, C4 trend checklist, buyback fields
- `data/` — fetchers: financials, prices, corporate actions, concall
  transcripts, annual reports → per-company input JSON matching
  input_schema_v3.json
- `reviews/` — per-company review cards (md + json), git-versioned, diffable
- `leaderboard.json` — generated from reviews

### 2. Review pipeline (one Claude Code cloud session per company)
Input: company name + tier (SCREEN/FULL) → gather data → run engine → agent
applies the judgment rubrics → writes the review card → regenerates the
leaderboard. Burns the $250 credit, not the weekly chat allowance.

### 3. Frontend
- **Company input**: type a name → queues a full research run, shows progress,
  lands the card when done
- **Leaderboard**: every reviewed company, categorized (INVEST NOW /
  INVEST AT TRIGGER / WATCH / PASS), sortable by composite, quality, price,
  margin of safety
- **Best overall view**: highest-conviction names regardless of price
- **Best TODAY view**: what's actually buyable now — INVEST NOW names,
  trigger-names within striking distance of trigger, WATCH names near ACC
  levels. This is the "don't sit out of the market for months" view.
- **Company page**: review card, metrics, promise-vs-delivery tracker, thesis,
  risks, price-vs-trigger history

### 4. "Invest today" logic (v3.7 tiers)
- Entry tiers: WATCH / ACC (−12.5%) / INV (−30%) vs DCF fair value
- Best overall = conviction rank (composite score)
- Best today = conviction × price position (distance to trigger). A great
  company 40% above fair value is not a today-buy; a good company sitting on
  its ACC trigger is.

## Build phases
1. **Repo + engine + specs port** — fast, mostly moving files
2. **Rubric fixes** — A6 thresholds, promise register, SCREEN call, C4 trend
   checklist, buyback fields (must precede real reviews)
3. **Data layer** — the big lift; every fetcher gets a reliability check
4. **Review pipeline** — playbooks + card format + one pilot company end-to-end
5. **Leaderboard generator**
6. **Frontend** — input → run → leaderboard + today-view + company pages

## Non-negotiables
- v3 stays NOT LIVE until the validation bar passes (0 blow-ups, ≥3 winner
  names, to-T positive, 24m ≥0.8×). Until then the platform produces research,
  not investable calls — the today-view stays labeled provisional.
- Rubric/threshold changes = spec version bump + revalidation note. No refits.
- No live execution hooks, ever.

## Open questions
- Canonical financial data source (Screener? paid?) — free-first, reliability
  decides
- Frontend hosting: local page vs hosted (decide in phase 6)
- Re-review triggers: quarterly results? price hits trigger? both?

## Planned modules (beyond v1)
- Investor tracking: where tracked investors (Kacholia, Mukul Agrawal, Quant,
  others) are putting money — holdings, fresh buys/sells, mapped against
  review cards and the leaderboard.
- Company deep-dive pages: click a leaderboard name → full review card,
  score breakdown, history of reviews, price vs DCF trigger chart.

## Model & effort policy (credit mechanics confirmed 2026-09-24)
- The $250 credit **auto-applies to cloud sessions first-use** (not overflow):
  "Applies automatically to cloud sessions. After it's used or expires, your
  plan's regular usage applies." $238 left as of 2026-09-24; expires Nov 5.
  Weekly limits reset Tue 6 PM; "reset for free" promo expires Oct 22.
- **Sonnet 5, medium effort** = default for company reviews and coding. It
  closes most of the quality gap to Opus on knowledge work at ~40-60% lower
  cost, and medium effort matches high-effort output on these tasks (per the
  paper Bablu cited) — the model pick matters more than the effort dial.
- **High effort**: validation-critical runs only (usability audit, OOS
  revalidation, live-bar judgment).
- **Opus 5**: reserved for final close-call verdicts where correctness is
  paramount. Never the default — ~1.7x the cost.
- Token-efficiency rules for every session: cached spec context, focused
  briefs, SCREEN before FULL, no re-reads of settled material.

## Cost model (API rates, Sept 2026 — estimates, wide bands)
Cloud sessions on Pro default to Sonnet 5 ($3/$15 per MTok); Opus 5 ($5/$25)
costs ~1.7x. Prompt caching cuts repeated context ~90%.
- Per-company FULL review: ~300k input + ~30k output → **$2-4** real-world
  (agent overhead included). SCREEN-lite: **$1-2**.
- v3 to live: usability audit **$2-5** + third OOS set (~25 names) **$25-75**
  + revalidation ~free → **~$30-80** total.
- $250 therefore covers v3-to-live plus roughly 50-100 further company
  reviews. Levers: SCREEN vs FULL depth, Sonnet vs Opus, session focus.
- After the credit exhausts: everything continues on Claude chat / Pro weekly
  limits + Musey. All state lives in git, so the handoff is lossless — no new
  API spend required, ever.
