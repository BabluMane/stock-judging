# frontend/tools/ — dashboard data builders

## moves.json — the Big Moves feed (cron contract)

**Concept:** News = routine company updates (results, dividends, deals).
Big Moves = significant price moves (±10% over any rolling 5 trading days)
WITH a "why did this happen" explanation. Separate sections, separate purposes.

**File:** `frontend/data/moves.json` (mirrored to `docs/data/moves.json`)

**Schema (stable — do not change without updating both renderers):**
```json
{
  "updated_at": "2026-10-07",
  "moves": [
    {
      "date": "2026-10-07",        // snapshot date (YYYY-MM-DD)
      "symbol": "TATVA",           // NSE symbol, uppercase
      "move_pct": 12.7,            // signed %, max |5-trading-day return| in window
      "window": "5d",              // always "5d" for now
      "why": "one-line explanation of what drove the move",
      "sources": ["https://..."]   // 1-2 URLs backing the explanation
    }
  ]
}
```

**Renderers:**
- `js/calibration.js` → `renderMovesFeed()` — full feed on the Calibration page's
  Forward Testing section, newest first, above the companies table.
- `js/company.js` → `renderMovesSection()` — compact per-symbol block
  (max 5) on each company page, after "Price vs. trigger history".

**Writer (the weekly forward-tracking cron):**
1. `~/workspace/stock-judging/forward_tracking/snapshot.py` detects a ±10%
   move over any rolling 5-trading-day window and prints an ALERT line.
2. On ALERT, the cron worker researches the driver (recent news, last 2 weeks),
   writes the one-line "why" + 1-2 source URLs, and **appends** a new entry to
   `moves` in BOTH `frontend/data/moves.json` and `docs/data/moves.json`.
3. Entries are append-only — never edit or delete history. Newest first is
   handled by the renderers' sort, not by file order.
4. If no clear driver is found, write "No single clear driver found in recent
   news" and list what was found — never invent a reason.

**Other builders in this folder:**
- `build_calibration_json.py` — rebuilds `data/calibration.json` and
  `data/forward.json` from the CSVs. (Does NOT touch moves.json — that's
  cron-owned.)

## shp.json — shareholding & flows (cron contract)

**Concept:** promoter/FII/DII buying and selling, quarter over quarter, for
every reviewed company. Bablu's standing interest: who is accumulating and
who is distributing.

**Files:**
- History: `~/workspace/stock-judging/forward_tracking/shp_history.csv`
  (append-only: `date,symbol,quarter,promoter,fii,dii,public,pledge_pct`)
- Dashboard: `frontend/data/shp.json` (mirrored to `docs/data/shp.json`) —
  per symbol: latest quarter values + QoQ pp-changes + `flag` when any
  |change| >= 1pp.

**Writer:** `~/workspace/stock-judging/forward_tracking/shp_snapshot.py`
- Resolves each leaderboard symbol to its screener.in slug via the search API
  (slugs differ: ASMTEC → `526433`, ARE&M → `ARE&M`, J&KBANK → `J&KBANK`).
- Parses the Shareholding section table (latest two quarters) + the
  "pledged X% of their holding" line.
- Skips symbols with no data (logged, never fatal). SME names may lag a
  quarter (SAHASRA seeded at Mar-2026 while the rest are Jun-2026).

**Schedule:** quarterly, mid-Feb / mid-May / mid-Aug / mid-Nov — after the
SHP filing window closes. The run appends to shp_history.csv and rebuilds
shp.json in both mirrors.

**Renderer:** `js/company.js` → `renderShpSection()` — "Shareholding & flows"
on each company page: promoter/FII/DII/public bars, QoQ pp badges
(green/red at >= 1pp), one-line read ("DIIs added 12.05pp last quarter"),
pledge when present. Silent when shp.json is missing or lacks the symbol.
