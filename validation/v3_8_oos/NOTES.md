# v3.8 OOS data-gathering notes — mediocrity companies (COLPAL, ASHOKLEY, CIPLA, COALINDIA, GAIL)

**2026-09-24 · fetched via `curl` against screener.in's public API/HTML endpoints and
trendlyne.com's corporate-actions pages, no data fabricated.** This document covers the
5 "mediocrity" companies (10 name-dates) of the 13-company OOS set
(`OOS_SET_PREREG.md`): COLPAL, ASHOKLEY, CIPLA, COALINDIA, GAIL.

## Method summary (applies to all 5)

1. Resolved screener.in numeric company IDs by grepping `company/<digits>/` out of
   `curl https://www.screener.in/company/<SYMBOL>/`.
   - COLPAL = 685, ASHOKLEY = 281, CIPLA = 661, COALINDIA = 681, GAIL = 1074.
2. Weekly price series: `curl .../api/company/<id>/chart/?q=Price-DMA50-DMA200-Volume&days=6300`.
3. Weekly PE + vendor TTM EPS: `curl .../api/company/<id>/chart/?q=Price+to+Earning-Median+PE-EPS&days=6300`.
   Price and PE series share exactly the same date grid (verified: 100% date overlap for
   CIPLA, and by construction for the others), so `pe_series/<slug>.csv` is a straight
   date-join of the two, no interpolation.
4. Primary/audited FY EPS: `curl https://www.screener.in/company/<SYMBOL>/consolidated/`
   (or the plain `/company/<SYMBOL>/` page where no distinct consolidated report exists —
   see COLPAL below), parsed with BeautifulSoup, `id="profit-loss"` table, `EPS in Rs` row.
   This is screener's as-reported annual P&L EPS, independent of the price/PE quotient
   series — not back-solved.
5. Corporate actions (splits/bonuses): screener.in's own company page does **not** expose
   a dedicated split/bonus history table on the pages fetched (profit-loss, balance-sheet,
   cash-flow, ratios, top-ratios sections all checked — none). Sourced instead from
   `trendlyne.com/equity/corporate-actions/<SYM>/<id>/...` (a public NSE/BSE corporate-action
   aggregator) plus web-search corroboration (indiainfoline.com, angelone.in, hdfcsky.com,
   business-standard.com). Every action recorded has an ex-date and a named source.
6. DCF financial inputs: screener's balance-sheet, cash-flow, ratios and top-ratios
   sections (same consolidated/standalone pages as step 4), last 5 reported FY columns.

## Known limitations across all 5 companies

- **Capex** is not a direct screener line item retrievable via static HTML fetch (screener
  exposes it only via an interactive "+"-expand schedule that requires a separate,
  possibly authenticated, AJAX call not available through plain `curl`). Approximated as
  `Cash from Operating Activity − Free Cash Flow`, which matches screener's own displayed
  FCF convention (FCF = CFO − capex). Flagged per company below as an estimate, not a
  directly-sourced figure.
- **Net cash / net debt** is incomplete: screener's static balance sheet bundles bank cash
  into "Other Assets+" without a separately retrievable cash sub-line (same expand-schedule
  limitation as capex). `Borrowings+` and `Investments` are sourced directly; a clean net-debt
  figure needs either the schedule expansion (not attempted here) or a supplementary source
  (annual report balance sheet cash & bank balances line).
- **Beta (2yr weekly vs Nifty)** is not exposed anywhere on the screener.in company pages
  fetched (checked all 5 sections per company). Not fetched from an alternate source per
  the task's own fallback instruction — to be computed centrally from the price series vs
  Nifty.
- **Shares outstanding**: not a direct screener field; derivable from Equity Capital ÷ Face
  Value (both sourced) or Market Cap ÷ Current Price (both sourced, current only).
  Historical share-count changes must be inferred from `corp_actions/<slug>.json`.

---

## COLPAL (Colgate-Palmolive India)

- **Company ID:** 685. **Basis used:** standalone. Screener's `/company/COLPAL/consolidated/`
  URL loads and labels itself "Consolidated Figures" but the P&L table it returns only
  spans Mar 2006–Mar 2010 (stale/truncated — Colgate India appears to have no active
  material consolidated subsidiary in the modern window, so screener has nothing recent to
  show there). Used the plain `/company/COLPAL/` page instead, whose P&L table spans
  Mar 2015–Mar 2026 + TTM and matches the standard 10yr+TTM screener layout. All
  `sourced_eps`, `dcf_financials` figures for COLPAL are on this standalone basis.
- **Price/PE series:** 901 weekly points, 2009-06-26 → 2026-09-24. Full coverage of both
  scoring dates (2016-03-31, 2018-03-31).
- **Vendor TTM EPS series:** 86 points, screener's own publication-dated series.
- **Sourced FY EPS:** Mar2015 20.55 → Mar2026 48.73 (full run, no gaps).
- **Corporate actions:** one 1:1 bonus, ex-date 2015-09-23 — before both scoring dates, so
  both 2016 and 2018 name-dates are already on a common (post-bonus) basis; no restatement
  needed for this pair. An older 10:1 face-value split (Rs10 → Re1) occurred before Jan 2000
  per Trendlyne's own "has not split the face value since Jan 1, 2000" note — exact date not
  confirmed from sources checked, but 25+ years before either scoring date, so irrelevant to
  this pair's basis normalization.
- **Data quality:** clean. No flags on EPS-basis constancy or corporate-action timing for
  this pair.

## ASHOKLEY (Ashok Leyland)

- **Company ID:** 281. **Basis used:** consolidated (standard screener consolidated page,
  full Mar2015–Mar2026 + TTM P&L table).
- **Price/PE series:** 878 weekly points, 2009-06-26 → 2026-09-24.
- **Vendor TTM EPS series:** 85 points.
- **Sourced FY EPS:** Mar2015 0.24 → Mar2026 5.91 (full run; note the FY21/FY22 negative EPS,
  −0.28 / −0.61, consistent with the well-documented CV-cycle + COVID downturn — expected,
  not a data defect).
- **Corporate actions:** 10:1 face-value split (2004-06-28) and 1:1 bonus (2011-08-02), both
  well before either scoring date — no restatement needed for those. **FLAG:** a further 1:1
  bonus, ex-date **2025-07-16**, falls *after* both scoring dates (2016-03-31, 2018-03-31)
  but *before* "today" (2026-09-24). Per `CONVENTIONS.md` §4, the sourced FY16/FY18 EPS must
  be checked against whether screener's vendor price/PE series is itself back-adjusted
  through this 2025 bonus; if so, the sourced FY16/FY18 EPS values above need to be halved
  before comparison. Not resolved in this pass — downstream usability-check step should
  verify by checking for a ~2x step or lack thereof in the vendor TTM EPS series around
  mid-2025.
- **Data quality:** otherwise clean; flag above is the only open item.

## CIPLA

- **Company ID:** 661. **Basis used:** consolidated.
- **Price/PE series:** 901 weekly points, 2009-06-26 → 2026-09-24.
- **Vendor TTM EPS series:** 87 points.
- **Sourced FY EPS:** Mar2015 14.71 → Mar2026 48.02 (full run). Note the FY17 dip to 12.51
  (from 16.93 in FY16) — consistent with the pre-registered thesis (US FDA issues, margin
  pressure) and the FY16/FY18 pair straddling that stretch, not a data artifact.
- **Corporate actions:** 5:1 face-value split (Rs10 → Rs2, ex-date 2004-05-11) and a 3:2
  bonus (ex-date 2006-04-24) — both well before either scoring date. **No corporate actions
  found between either scoring date and today** — CIPLA is the cleanest of the 5 on this
  dimension, both name-dates are on an identical, already-common basis.
- **Data quality:** clean, no flags.

## COALINDIA (Coal India)

- **Company ID:** 681. **Basis used:** consolidated.
- **Price/PE series:** 830 weekly points, 2010-11-05 → 2026-09-24 (shorter history than the
  other 4 — Coal India IPO'd Nov 2010, so this is the full listed history, not a data gap).
  Both scoring dates (2016-03-31, 2018-03-31) are comfortably inside this window.
- **Vendor TTM EPS series:** 79 points.
- **Sourced FY EPS:** Mar2015 21.73 → Mar2026 50.46 (full run). Note FY17→FY18 dip
  (14.95 → 11.34) and FY18→FY19 jump (11.34 → 28.34) — large swings, consistent with the
  pre-registered "weak capital appreciation, high dividend yield" thesis and worth a closer
  look in the downstream usability check (results timing / one-off items), but not flagged
  as a vendor data defect here since both figures come from the same audited P&L series.
- **Corporate actions: none found.** Trendlyne's corporate-actions page for COALINDIA (id
  275) returns only dividend-history and results-calendar tables — no bonus or split table
  at all. Face value confirmed Rs10 (screener top-ratios), unchanged since IPO. Consistent
  with a PSU that IPO'd in 2010 and has not altered its capital structure since — this is
  the one company in this batch of 5 where **no basis normalization is needed at all**
  (no corporate actions to restate for, over the company's entire listed history).
- **Data quality:** clean on corporate actions; the FY17–FY19 EPS swing is a content flag
  for the usability check, not a sourcing flag.

## GAIL (GAIL India)

- **Company ID:** 1074. **Basis used:** consolidated.
- **Price/PE series:** 901 weekly points, 2009-06-26 → 2026-09-24.
- **Vendor TTM EPS series:** 87 points.
- **Sourced FY EPS:** Mar2015 4.67 → Mar2026 11.53 (full run).
- **Corporate actions — the most active of the 5, multiple FLAGS:** GAIL has issued bonus
  shares **five** times: 1:2 (2008-10-06), 1:3 (2017-03-09), 1:3 (2018-03-27), 1:1
  (2019-07-09), 1:2 (2022-09-06). No face-value splits (Rs10 unchanged throughout).
  - The 2008 bonus predates both scoring dates — no issue.
  - **The 2017-03-09 1:3 bonus falls between gail_2016-03-31 and gail_2018-03-31** — the
    two OOS name-dates for this company straddle a corporate action. This means the
    2016-03-31 name-date's sourced FY16 EPS and the 2018-03-31 name-date's sourced FY18 EPS
    are **not** automatically on the same per-share basis as each other, and need explicit
    restatement per `CONVENTIONS.md` §4 before use.
  - **The 2018-03-27 1:3 bonus** falls 4 days before the 2018-03-31 FY-end — already inside
    FY18's as-filed EPS by construction, but close enough to the period boundary to warrant
    care when identifying FY18's "results week" for the usability check (make sure the
    results-week EPS pulled is unambiguously post- this bonus, matching the vendor series'
    basis).
  - The 2019-07-09 and 2022-09-06 bonuses fall after both scoring dates but before "today" —
    both sourced FY16 and FY18 EPS need restatement onto the current (post-2022) basis if
    the vendor price/PE series is itself fully back-adjusted through 2022 (screener
    typically back-adjusts its own chart series for all such actions retroactively — this
    should be confirmed, not assumed, downstream).
  - **This is flagged as the single highest-risk name in this batch of 5 for the
    usability/basis-normalization step** — not because the data is bad, but because the
    cumulative bonus multiple between 2016-03-31 and today is large (roughly 2016 shares ×
    4/3 × 4/3 × 2 × 3/2 ≈ 8× share count, exact multiple to be computed downstream from the
    ex-dates above, not attempted here to avoid circularity with the usability test itself).
- **Data quality:** underlying series (price, PE, vendor EPS, sourced EPS) are all cleanly
  fetched and complete; the flag is entirely about basis normalization across the frequent
  bonus history, which is exactly what `corp_actions/gail.json` is for.

---

## Files written (this batch of 5)

- `pe_series/{colpal,ashokley,cipla,coalindia,gail}.csv` — `date,price,pe`, weekly, full
  listed history to 2026-09-24.
- `eps_series/{...}.json` — raw vendor (screener) publication-dated TTM EPS series.
- `sourced_eps/{...}.json` — primary/audited annual FY EPS from the P&L table, per company,
  with basis (standalone/consolidated) noted.
- `corp_actions/{...}.json` — full split/bonus history with ex-dates and sources, flags for
  actions falling between/near the two OOS scoring dates called out explicitly.
- `dcf_financials/{...}.json` — revenue, EBITDA margin (OPM%), depreciation, net profit,
  capex (estimated), CFO, FCF, working-capital days, equity capital, reserves, borrowings,
  investments, current market cap/price/face value/book value — last 5 reported FYs, with
  units and source noted; capex/net-debt/beta/shares-outstanding gaps explicitly flagged
  in each file's own notes fields.

No files outside `validation/v3_8_oos/` were touched. `OOS_SET_PREREG.md` was not modified.
Nothing was committed — files are left for review per the task instructions.
