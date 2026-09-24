# data/ — fetcher layer (placeholder)

Each fetcher produces per-company raw data that feeds the review pipeline's
input JSON (conforming to `../engine/input_schema_v3.json`).

Planned fetchers:
- `financials/` — P&L, balance sheet, cash flow, ratios (free-first; source TBD)
- `prices/` — price history, corporate-action-adjusted
- `corporate_actions/` — splits, bonuses, buybacks (structured)
- `concalls/` — concall transcripts (8 quarters FULL / 4 SCREEN-lite)
- `annual_reports/` — annual report extraction

Rules:
- Every fetcher gets a reliability check. No fabricated data, ever.
- No forward-fill, no interpolation of fundamentals.
- Split/bonus basis normalized before any ratio math.
