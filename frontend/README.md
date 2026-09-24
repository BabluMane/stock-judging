# frontend/ — static frontend (v1)

Static, no-build-step site: plain HTML/CSS/vanilla JS, no framework, no
bundler. One inline-SVG chart, hand-rolled — not worth a charting library for
a single line chart with four series. Everything renders client-side from
JSON fetched at load time.

Why no framework: five pages, no client-side routing beyond query params, no
shared component state beyond "load some JSON, render a table/list/detail
view." A framework buys nothing here and costs a build step, which breaks the
`file://` requirement.

## Running it

- **Directly**: open `frontend/index.html` from disk. Most browsers (Chrome,
  Edge) block `fetch()` of local JSON files from a `file://` page for
  cross-origin reasons, so the pages will render but show a "could not load"
  notice instead of data — this is handled gracefully (no console errors, no
  crash), not silently broken.
- **Static server** (recommended, and required to actually see data): from
  the repo root, `python3 -m http.server 8000`, then open
  `http://localhost:8000/frontend/`.

## Pages

| File | Purpose |
|---|---|
| `index.html` | Leaderboard — every reviewed company, sortable table, category filter |
| `best-overall.html` | Conviction-ranked list, regardless of price |
| `best-today.html` | Conviction × distance-to-trigger — what's actually buyable now |
| `company.html?symbol=SYM` | Review card: metrics, score breakdown, promise tracker, thesis, risks, price-vs-trigger chart |
| `run.html` | Company input → generates and downloads a run-request file, tracks local queue state |

Shared: `css/styles.css` (design tokens, category colors), `js/data.js`
(fetch + normalize), `js/nav.js` (provisional banner + top nav, injected on
every page).

## Data contract (read-only)

The frontend reads, and never writes:
- `../leaderboard.json`
- `../reviews/<SYMBOL>.json`
- (indirectly, for field reference) `../engine/sample_input_v3.json`

Both are currently empty (`leaderboard.json` is the seeded stub
`{"companies": [], "generated_at": null}`; `reviews/` has no cards yet), so
every page's primary state today is its **empty state** — "no reviews yet",
never a fabricated row. Empty states were verified by temporarily loading a
throwaway local review card during development; no fake data is committed.

### Leaderboard entry shape — inferred, not locked

`leaderboard.json`'s per-company shape has never been defined beyond the
empty seed. Rather than invent and lock a new schema, `frontend/js/data.js`'s
`normalizeEntry()` accepts either a lightweight leaderboard-row object *or* a
full `review_card.schema.json` object with the same field names, and reads
defensively (optional-chains everything, never throws on a missing field).
It expects, when present:

```
symbol, name, tier, as_of, status
verdict: { category, conviction, best_today_rank }
scores:  { Q, P_today }              // see "Schema gaps" below
dcf:     { current_price, fair_value, acc_trigger, inv_trigger }
```

Recommendation for phase 5 (leaderboard generator): emit `leaderboard.json`
company entries in exactly this shape (a flat projection of the fields
above) so the leaderboard table doesn't need to fetch every review card
individually.

## Schema gaps (flagged, not invented)

Fields the pages want but `review_card.schema.json` doesn't yet define:

1. **`quality` / `composite` score fields.** `scores` is typed only as
   `"engine v3 scored dimensions"` with no sub-schema. The frontend reads
   `scores.Q` as quality and `scores.P_today` (falling back to
   `verdict.conviction`) as composite, based on `engine_v3.py`'s `q_score()`
   / `p_score()` output — Q = quality dimension average, P = price-adjusted
   composite. **Not confirmed as the final field names for the review card.**
2. **Margin of safety (numeric %).** The engine only exposes `mos_nod`
   (boolean: did price clear the 0.8× DCF-midpoint line). The frontend
   derives `marginOfSafetyPct = (fair_value - price) / fair_value * 100`
   client-side. If a canonical numeric MoS field is added to the review
   card, prefer it over this derived value.
3. **Price-vs-trigger history.** The schema has only point-in-time
   `dcf.current_price` / `acc_trigger` / `inv_trigger` / `fair_value` as of
   `as_of` — no history series. The chart on `company.html` looks for an
   optional `trigger_history: [{date, price, acc_trigger, inv_trigger,
   fair_value}, ...]` array and renders an honest "no history yet" state
   when it's absent (which is every card today). This field name is a
   frontend proposal, not something read from any spec — confirm or rename
   before the pipeline starts writing it.
4. **`promises` item shape.** Schema says `"items": {"type": "object"}` with
   no properties. The tracker reads `promise/title/what`,
   `status/delivery_status`, `quarter/period/made_on`, and
   `detail/notes/outcome`, falling back gracefully if none match. Needs a
   real shape from phase 4 (promise register).

## Run-request contract (company input page)

`run.html` has no backend, so it cannot write into the repo directly. On
submit it downloads a JSON file the person commits into `runs/queue/` (see
`runs/README.md` for the exact path and shape); a future pipeline watcher
picks it up from there. The page also tracks requests it has made in this
browser's `localStorage` purely as a per-viewer "what did I ask for"
convenience — never presented as the real queue, and "done" is only ever
shown once `reviews/<SYMBOL>.json` is confirmed to exist by fetch.

## Category colors (consistent across every page)

Defined once as CSS custom properties in `styles.css` and consumed via
`categoryBadgeHTML()` in `data.js`:

- **INVEST NOW** — green
- **INVEST AT TRIGGER** — amber
- **WATCH** — blue
- **PASS** — grey

## Non-negotiables honored

- Every page renders a **PROVISIONAL — v3 is NOT LIVE** banner (`js/nav.js`,
  `renderChrome()`), independent of data state.
- No live execution hooks anywhere — `run.html` only ever produces a local
  file download plus a `localStorage` marker.
- All fetches are wrapped in try/catch; no unhandled rejections, no
  console errors on load or on interaction (verified via `file://` and via
  `python3 -m http.server`, clicking every sort/filter/link).

## Planned later module — not built in v1

**Investor tracking**: Kacholia, Mukul Agrawal, Quant, and other tracked
investors' holdings/fresh-buys/fresh-sells, mapped against review cards and
the leaderboard (per `PLATFORM_SCOPE.md` "Planned modules (beyond v1)"). No
page, route, or placeholder link exists for this yet by design — it needs
its own data source and schema before a UI slot makes sense.
