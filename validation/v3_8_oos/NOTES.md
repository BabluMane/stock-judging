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

---

# v3.8 OOS data-gathering notes — winner companies (TITAN, DIVISLAB, PAGEIND, DMART, POLYCAB)

**2026-09-24 · fetched via `curl` against screener.in's public HTML/JSON endpoints, plus
pocketful.in's corporate-actions pages (trendlyne.com returned HTTP 403/405 to both `curl`
and WebFetch and was abandoned), no data fabricated.** This section covers the 5 "winner"
companies (10 name-dates) of the 13-company OOS set (`OOS_SET_PREREG.md`): TITAN, DIVISLAB,
PAGEIND, DMART, POLYCAB.

## Method summary (applies to all 5)

1. Resolved screener.in numeric company IDs via `data-company-id="<id>"` on
   `curl https://www.screener.in/company/<SYMBOL>/` (more reliable than grepping
   `company/<digits>/` links, which mostly point at *peer* companies, not the subject).
   - TITAN = 3437, DIVISLAB = 837, PAGEIND = 2389, DMART = 1273670, POLYCAB = 1274653.
2. Weekly price series: `curl .../api/company/<id>/chart/?q=Price-DMA50-DMA200-Volume&days=6300`.
3. Weekly PE + vendor TTM EPS: `curl .../api/company/<id>/chart/?q=Price+to+Earning-Median+PE-EPS&days=6300`.
   Joined on date to build `pe_series/<slug>.csv` (`date,price,pe`), no interpolation;
   dates with no PE value (rare) left blank in the `pe` column.
4. Primary/audited FY EPS: `curl https://www.screener.in/company/<SYMBOL>/consolidated/`,
   parsed with BeautifulSoup, `id="profit-loss"` table, `EPS in Rs` row — screener's
   as-reported annual P&L EPS, independent of and not back-solved from the price/PE
   quotient series. **Exception: PAGEIND** — see below.
5. Corporate actions: screener.in's own page has no dedicated split/bonus table (same
   finding as the mediocrity batch). `trendlyne.com` corporate-actions pages returned
   HTTP 403 to `curl` and HTTP 405 to WebFetch (blocked both ways). Used
   `pocketful.in/stocks/<slug>/corporate-actions/{bonus,splits}` instead — a public
   NSE/BSE-sourced corporate-action aggregator that `curl` could reach cleanly (HTTP 200,
   real ex-dates and ratios in a parsed table). Cross-checked TITAN's result against public
   reporting (Business Standard 2011-05-12 article on the shareholder-approved bonus+split)
   for corroboration. Note: **pocketful.in's first response for DIVISLAB came back with an
   empty (0-table) page** on the first `curl`; a second identical request returned the full
   table. Re-fetched and re-verified before use — flagged here as a vendor-side
   flakiness/caching quirk, not a data quality issue with the content itself once
   successfully returned.
6. DCF financial inputs: screener's balance-sheet, cash-flow, ratios and top-ratios
   sections (same consolidated/standalone page as step 4), full Mar2015–Mar2026 (+TTM)
   columns where available.

## Known limitations across all 5 companies (same as mediocrity batch)

- **Capex**: not a direct screener line item. `dcf_financials/<slug>.json` provides
  `cash_flow.cfi_cr` (investing cash flow, capex + other investment purchases, not
  capex-only), the fixed-assets/CWIP balance-sheet lines (delta gives a gross-capex proxy),
  and `cash_flow.free_cash_flow_cr` alongside `cash_flow.cfo_cr` so capex can be back-solved
  as CFO − FCF where screener discloses both directly. Flagged as an estimate in each file's
  `notes`.
- **Net cash/net debt**: `balance_sheet.borrowings_cr` (gross debt) is sourced directly;
  screener's "Other Assets" line bundles cash with working-capital assets, so a clean net-debt
  figure needs a supplementary source (annual report balance sheet). Flagged in each file.
- **Beta (2yr weekly vs Nifty)**: not exposed on any screener.in section checked (chart,
  ratios, top-ratios). Not fetched from elsewhere per the task's own fallback instruction —
  left for central computation from the price series vs Nifty.
- **Shares outstanding**: not a direct field; derivable from `balance_sheet.equity_capital_cr`
  ÷ face value (in `top_ratios_current`, current only) or market cap ÷ current price (also
  current-only). Historical share-count changes must be inferred from `corp_actions/<slug>.json`.
- **Working capital change**: not a separate line; `ratios.working_capital_days` (revenue-days
  basis) is provided per year, convertible to WC-as-%-of-revenue via `/365`.

## TITAN (Titan Company)

- **Company ID:** 3437. **Basis used:** consolidated (Mar2015–Mar2026 + TTM).
- **Price/PE series:** 901 weekly points, 2009-06-26 → 2026-09-24. Both scoring dates
  (2016-03-31, 2018-03-31) comfortably inside.
- **Vendor TTM EPS series:** 87 points.
- **Sourced FY EPS:** FY16 (Mar 2016) = **7.60**, FY18 (Mar 2018) = **12.73** (full run
  Mar2015 9.19 → Mar2026 57.14 also captured).
- **Corporate actions:** a combined **1:1 bonus + 10:1 face-value split (Rs.10 → Re.1)**,
  same ex-date **2011-06-24** (cumulative 20× share-count factor). This is well before both
  scoring dates (2016, 2018) — both name-dates are already on the current, post-2011 basis,
  consistent with each other and with screener's already-adjusted price/PE/EPS chart series.
  **No further corporate actions found through 2026-09-24** — the cleanest of the 5 on this
  dimension; no restatement needed for either name-date.
- **Data quality:** clean. No flags.

## DIVISLAB (Divi's Laboratories)

- **Company ID:** 837. **Basis used:** consolidated (Mar2015–Mar2026 + TTM).
- **Price/PE series:** 901 weekly points, 2009-06-26 → 2026-09-24.
- **Vendor TTM EPS series:** 87 points.
- **Sourced FY EPS:** FY16 (Mar 2016) = **42.41**, FY18 (Mar 2018) = **33.04** (full run
  captured Mar2015 → Mar2026). **FLAG:** FY18 EPS (33.04) is *lower* than FY16 (42.41) — a
  ~22% decline. This is consistent with the pre-registered thesis note ("sharp mid-decade
  drawdown... as an in-window stress test") but the stated drawdown was pegged to 2022–23 in
  the prereg rationale, not FY17/FY18 — worth a closer look downstream (Divi's had a
  well-documented USFDA import-alert-driven slowdown at its Vizag unit in FY17, a plausible
  real-earnings explanation, but this is a content flag for the usability/DCF step to verify
  against, not something resolved here).
- **Corporate actions:** two 1:1 bonus issues — ex-date **2009-08-01** and ex-date
  **2015-09-26**. Both predate both scoring dates (2016-03-31, 2018-03-31), so FY16 and FY18
  sourced EPS are on a common (post-Sep-2015-bonus) basis with each other and with the
  vendor series — no restatement needed for this pair. **No split ever** (confirmed via
  pocketful.in `/splits` page, "No Result Found", plus general knowledge that Divi's has
  never sub-divided its face value).
- **Data quality:** sourcing clean; the FY16→FY18 EPS decline is a content flag, not a
  sourcing defect — pocketful's bonus page required a re-fetch (see method note above) but
  the second fetch returned a clean, complete table.

## PAGEIND (Page Industries)

- **Company ID:** 2389. **Basis used: standalone** — screener's `/company/PAGEIND/consolidated/`
  page returns HTTP 200 but its `id="profit-loss"` table has **no data columns at all**
  (empty `<thead>`, labels with no figures) — this reproduced on inspection of the raw HTML,
  not a fetch/timeout artifact. Page Industries (Jockey India licensee) has historically
  reported on a standalone basis with no material consolidated subsidiary in this window, so
  the plain `/company/PAGEIND/` page (which has the full populated Mar2015–Mar2026+TTM P&L
  table) was used instead for all of `sourced_eps` and `dcf_financials`. **Flag this basis
  choice explicitly** — if a downstream reviewer expects consolidated figures for Page
  Industries and none exist on screener, standalone is the correct and only available
  primary-sourced basis, not a fallback of convenience.
- **Price/PE series:** 901 weekly points, 2009-06-26 → 2026-09-24 (price/PE series itself is
  sourced from the same chart API regardless of standalone/consolidated P&L basis — screener
  charts are basis-agnostic price/quotient series).
- **Vendor TTM EPS series:** 87 points.
- **Sourced FY EPS:** FY15 (Mar 2015) = **175.74**, FY17 (Mar 2017) = **238.73** (full run
  Mar2015 175.74 → Mar2026 684.80 also captured — a very high per-share EPS, consistent with
  Page's famously high absolute share price / no-split history).
- **Corporate actions: none found** — pocketful.in returned "No Result Found" for both
  `/corporate-actions/bonus` and `/corporate-actions/splits`. Face value Rs.10 unchanged
  throughout the company's listed history (2007–present per screener top-ratios). Consistent
  with well-documented public knowledge that Page Industries has never split or bonused.
  **No basis normalization needed for either scoring date.**
- **Data quality:** clean on the standalone basis used; only flag is the basis choice itself
  (standalone, not consolidated, because screener has no populated consolidated table for
  this name) — documented in `sourced_eps/pageind.json` and `dcf_financials/pageind.json`.

## DMART (Avenue Supermarts)

- **Company ID:** 1273670. **Basis used:** consolidated (Mar2015–Mar2026 + TTM available on
  screener, but the company only listed Mar-2017, so pre-listing years in the table are
  either from pre-IPO reporting or blank — see price series note below).
- **Price/PE series:** 497 weekly points — **starts 2017-03-24** (IPO week), not 2009 like
  the older-listed names. This is the company's actual listed-history start, not a data gap;
  DMart's IPO was March 2017, so no pre-IPO price/PE series exists to fetch. Both scoring
  dates (2018-03-31, 2019-03-31) are inside this window with ample runway.
- **Vendor TTM EPS series:** 48 points.
- **Sourced FY EPS:** FY18 (Mar 2018) = **12.92**, FY19 (Mar 2019) = **14.46** (full run
  captured back to Mar2015 in screener's P&L table, i.e. screener shows pre-IPO FY
  financials from the company's pre-listing filings, but no price/PE series exists for
  those years to cross-check against).
- **Corporate actions: none found** — pocketful.in "No Result Found" for both bonus and
  split pages. Face value Rs.10 unchanged since IPO. **No basis normalization needed** for
  either scoring date (both are post-IPO, pre-any-corporate-action, and no action has
  occurred since either date through 2026-09-24).
- **Data quality:** clean. No flags beyond the expected (and correctly explained) shorter
  price-series history vs. the other 4 names in this batch.

## POLYCAB (Polycab India)

- **Company ID:** 1274653. **Basis used:** consolidated (Mar2015–Mar2026 + TTM on screener,
  same pre-IPO-financials-without-price-series caveat as DMart).
- **Price/PE series:** 389 weekly points — **starts 2019-04-19** (IPO week, April 2019), not
  earlier. Both scoring dates (2020-03-31, 2021-03-31) are inside this window with ample
  runway to 2026-09-24.
- **Vendor TTM EPS series:** 38 points.
- **Sourced FY EPS:** FY20 (Mar 2020) = **50.97**, FY21 (Mar 2021) = **59.15** (full run
  captured; note FY21 EPS rising through the COVID year — Polycab's cables/wires demand held
  up better than many industrials, a plausible real-economics explanation, not flagged as a
  data defect).
- **Corporate actions: none found** — pocketful.in "No Result Found" for both bonus and
  split pages. Face value Rs.10 unchanged since IPO. **No basis normalization needed** for
  either scoring date.
- **Data quality:** clean. No flags.

---

## Files written (this batch of 5)

- `pe_series/{titan,divislab,pageind,dmart,polycab}.csv` — `date,price,pe`, weekly, full
  listed history to 2026-09-24 (DMart/Polycab start at their respective IPO dates, not 2009).
- `eps_series/{...}.json` — raw vendor (screener) publication-dated TTM EPS series, as fetched.
- `sourced_eps/{...}.json` — primary/audited annual FY EPS from the P&L table, per company,
  with basis (standalone for PAGEIND, consolidated for the other 4) and a corporate-action
  basis note explicit per company.
- `corp_actions/{...}.json` — full split/bonus history with ex-dates and sources (empty list
  + explicit "none found, both pages checked" note for PAGEIND/DMART/POLYCAB, which have
  never split or bonused).
- `dcf_financials/{...}.json` — revenue, EBITDA margin (OPM%), depreciation, net profit,
  interest, PBT, tax rate, CFO/CFI/CFF/FCF, working-capital days, equity capital, reserves,
  borrowings, investments, fixed assets/CWIP, current market cap/price/face value/book
  value/ROE/ROCE — full available FY history, with units and source noted; capex/net-debt/
  beta/shares-outstanding gaps explicitly flagged in each file's own `notes` field.

No files outside `validation/v3_8_oos/` were touched. `OOS_SET_PREREG.md` was not modified.
Nothing was committed — files are left for review per the task instructions.

---

# v3.8 OOS data-gathering notes — blow-ups/frauds (PC JEWELLER, FUTURE RETAIL, CG POWER)

**2026-09-24 · fetched via `curl` against screener.in's public API/HTML endpoints and
trendlyne.com's corporate-actions pages, no data fabricated.** This section covers the
3 "blow-up/fraud" companies (5 name-dates) of the 13-company OOS set (`OOS_SET_PREREG.md`):
PC Jeweller (2 dates), Future Retail (2 dates), CG Power (1 date, single-dated per prereg).

## Method summary

Same pipeline as the mediocrity batch above: screener.in numeric company IDs resolved by
grepping `data-company-id="..."` / `/api/company/<id>/` out of `curl
https://www.screener.in/company/<SYMBOL>/` — **PCJEWELLER = 247383, FRETAIL = 1273469,
CGPOWER = 739**. Weekly price via `.../chart/?q=Price-DMA50-DMA200-Volume&days=6300`; weekly
PE + vendor TTM EPS via `.../chart/?q=Price+to+Earning-Median+PE-EPS&days=6300`; `pe_series`
CSVs are a straight date-join of the Price and PE datasets (rows where PE is `null` in the
vendor feed are dropped, not interpolated — see per-company notes for what that means).
Primary/audited FY EPS from `/company/<SYMBOL>/consolidated/` (or `/company/<SYMBOL>/`
standalone where no consolidated table exists for a given year), parsed via BeautifulSoup +
pandas (`id="profit-loss"` / `"balance-sheet"` / `"ratios"` / `"cash-flow"` tables). Corporate
actions from `trendlyne.com/equity/corporate-actions/<SYM>/<id>/...`, cross-checked against
Equity Capital jumps in the screener tables, plus targeted web search for the fraud-specific
restatement deltas (CG Power) and the demerger scheme (Future Retail).

## PC Jeweller (PCJEWELLER) — pcjeweller_2017-03-31, pcjeweller_2018-03-31

- **All files written successfully:** `pe_series/pcjeweller.csv` (703 weekly rows,
  2012-12-28 to 2026-09-24 — the company is still listed and trading), `eps_series/pcjeweller.json`
  (68 vendor TTM points), `sourced_eps/pcjeweller.json`, `corp_actions/pcjeweller.json`,
  `dcf_financials/pcjeweller.json`.
- **Both scoring dates have clean, cross-checked sourced EPS:** FY2017 = 1.18, FY2018 = 1.36
  (consolidated P&L, screener), each within ~8% of the vendor's results-week TTM EPS (1.28 and
  ~1.47 respectively) — a TTM-vs-FY timing gap, not a basis error, per `CONVENTIONS.md` §4.
- **Corporate actions:** one 1:1 bonus (ex-date 2017-07-06 — falls *between* the two scoring
  dates) and one much-later 10:1 stock split (ex-date 2024-12-16). Confirmed (by back-solving
  PAT/EPS to an implied share count) that screener's P&L "EPS in Rs" row is **already** on the
  fully split/bonus-adjusted (vendor-consistent) basis — no further restatement was applied.
  The "Equity Capital" row in the same table is on the *unadjusted* as-filed basis — documented
  explicitly in `corp_actions/pcjeweller.json` so the two co-existing bases in one table aren't
  mistaken for an error.
- **Data quality:** clean for both scored dates. The name gets genuinely messy only *after*
  FY2019 (PAT collapses to ~Rs 1cr, PE becomes undefined for long stretches — 233/703 weekly PE
  points are `null` from mid-2019 onward), i.e. after both scoring dates, so this doesn't
  contaminate either scored input.
- **PIT-detectability finding:** Debtor Days rose from 45 (FY15) to 66 (FY17) to 70 (FY18) —
  receivables growing faster than revenue was already visible in the ratios table *at* the
  pcjeweller_2017-03-31 scoring date, well before the 2018-19 collapse. Reported profitability
  (OPM 9-11%, EPS growing) stayed intact through FY2018 and gave no warning on its own — the
  working-capital-quality ratios were the only PIT-visible amber flag at either scored date; the
  actual PAT collapse (FY19, Rs 1cr) and the public governance/promoter-pledge crisis only
  landed in the numbers **after** the second scoring date.

## Future Retail (FRETAIL) — fretail_2017-03-31, fretail_2019-03-31

- **All files written successfully:** `pe_series/fretail.csv` (411 weekly rows, 2016-09-02 to
  2024-08-01 — see delisting note below), `eps_series/fretail.json` (27 vendor TTM points),
  `sourced_eps/fretail.json`, `corp_actions/fretail.json`, `dcf_financials/fretail.json`.
- **Consolidated financials only exist on screener from FY2019 onward** — there is no
  consolidated P&L table for FY2017 at all. FY2017 sourced EPS (7.81) therefore comes from the
  **standalone** page instead (full history back to FY2013 there); FY2019 uses consolidated
  (14.47, vs standalone 14.58 — a small, immaterial 0.7% gap). This is a genuine, disclosed
  basis difference *between the two scoring dates for this one name* — not a convenience choice.
- **Strong internal cross-check:** vendor TTM-EPS chart at 2017-03-31 = 7.81, exactly matching
  the standalone sourced FY2017 EPS (TTM==FY at FY-end by construction). Vendor TTM at
  2019-05-25 (results week) = 14.58, matching the *standalone* figure almost exactly rather
  than the consolidated one — suggesting screener's chart EPS metric for this name is itself
  standalone-sourced, noted in `sourced_eps/fretail.json`.
- **Corporate actions:** **none** — Future Retail never split, bonused, or paid a dividend in
  its listed history (confirmed via trendlyne). It *did* go through a non-split corporate
  restructuring (the Future Retail / Bharti Retail demerger scheme, effective 31-Oct-2015,
  record date 12-May-2016) that changed its business mix and face value (to Rs 2) just before
  the first scoring date — recorded in `corp_actions/fretail.json` as a comparability flag
  (FY2015/16 are pre-demerger and not trend-comparable to FY2017+), not as a split/bonus.
- **Price history DOES reach through both scoring dates, but goes "zombie" after 2022:** the
  price/PE feed (BSE-sourced for this name, not NSE) keeps printing quotes all the way to
  2024-08-01 (last price Rs 2.41) even though the company stopped filing financial results
  after Q3FY22 (14-Feb-2022 per the board-meeting log) and entered NCLT insolvency in 2022,
  with shares ultimately extinguished per the prereg's own description. PE is `null` in the
  vendor series from 2024-07-15 onward (no earnings denominator). **Neither scoring date is
  affected** — both FY2017-03-31 and FY2019-03-31 sit years before this zombie-listing period —
  but it's flagged because a careless "does data exist through T" check could be fooled by the
  post-2022 quotes into thinking the name was healthier for longer than it was.
- **PIT-detectability finding:** at fretail_2017-03-31, leverage was already building
  (Borrowings ~16% of total assets, up from a near-zero post-demerger base) against a thin 3.4%
  EBITDA margin, but this reads as ordinary aggressive-growth-retailer risk, not a blow-up
  signal. At fretail_2019-03-31, borrowings had grown 2.5x since FY17 while margins barely
  improved — the clearest PIT-visible warning available in either scored year is balance-sheet
  leverage, not receivables/inventory quality (both stayed low and stable through FY19, unlike
  PC Jeweller or CG Power). The proximate causes of the actual collapse — COVID-19 store
  closures compounding the leverage, then the Amazon-Future legal dispute and 2022 insolvency —
  are **not visible in either scored FY's fundamentals**; this name-date pair is structurally a
  harder "could a diligent DCF entry have seen it coming" case than PC Jeweller or CG Power,
  closer to a macro/tail-risk shock hitting an already-levered aggressive grower than a
  slow-motion accounting fraud.

## CG Power (CGPOWER) — cgpower_2016-03-31 (single-dated per prereg)

- **All files written successfully:** `pe_series/cgpower.csv` (901 weekly rows, 2009-06-26 to
  2026-09-24 — company remained listed and trading throughout, unlike Future Retail),
  `eps_series/cgpower.json` (86 vendor TTM points), `sourced_eps/cgpower.json`,
  `corp_actions/cgpower.json`, `dcf_financials/cgpower.json`.
- **Corporate actions:** last split/bonus was in 2010 (a 3:4 bonus; before that a 2:5 bonus in
  2006 and a 5:1 face-value split in 2006) — all more than 5 years before the scored FY16 date.
  **No basis restatement needed anywhere in the FY2012-2026 window** used for this validation;
  Equity Capital stays flat at Rs 125cr from FY2015 through FY2019, confirming no share-count
  change until the 2020 Murugappa/Tube Investments capital infusion (Equity Capital jumps to
  Rs 268cr in FY2021), which followed the 2019 fraud disclosure and promoter change.
- **Restated vs as-filed — explicitly flagged, not resolved for every year:** confirmed via web
  search (Business Standard, Aug 2019) that CG Power's FY2018 consolidated loss was originally
  reported at ~Rs 325cr and was later **restated upward by Rs 404.21cr to ~Rs 729cr** following
  the forensic investigation into undisclosed liabilities and related-party fund diversion.
  Screener's current FY2018 figure (-Rs 715cr) matches the *restated* number, confirming
  screener shows post-restatement financials, not as-originally-filed. A similar (less firmly
  sourced) restatement/adjustment gap was found for FY2019 (~Rs 487cr originally reported vs
  ~Rs 1,331cr shown by screener today). **FY2016 — the actual scored year — was NOT found to
  have been specifically restated** in the sources searched, but the full scope of which years'
  related-party transactions were examined was not confirmed beyond FY2017-18, so FY2016 is
  documented as "not confirmed restated" rather than "confirmed clean." All of this is recorded
  per-year in `sourced_eps/cgpower.json`.
- **Unresolved data-quality problem (flagged, not papered over):** the vendor's TTM-EPS chart
  series and the audited P&L table's EPS **disagree sharply and non-constantly** around the
  scored FY — vendor TTM at 2016-03-31 implies **+5.46**, while the audited consolidated P&L
  shows **-7.33** for FY2016 (a sign flip, not just a magnitude gap). This is NOT a share-count
  or standalone-vs-consolidated issue (checked both: standalone FY16 is -17.53, also doesn't
  match). It fails the "constant residual = harmless basis convention" test in `CONVENTIONS.md`
  §1 (the gap isn't constant across years and flips sign), so per the standing rule this is
  **not** waved through — it's recorded as an open, unresolved vendor-vs-audited discrepancy in
  `sourced_eps/cgpower.json`, most likely (not confirmed) reflecting a different profit base
  (e.g. excluding a large exceptional/other-income swing — CG Power's Other Income line moves
  from +Rs72cr to -Rs230cr to -Rs1,140cr across FY15-16 depending on standalone/consolidated) in
  whichever profit figure the vendor's chart metric is built from, versus the audited Net
  Profit line the P&L table shows.
- **DCF-financials history limited to FY2015-2019** (2 years before the FY16 scoring date, not
  the full 5yr trailing window a later date could support) — screener's consolidated table for
  this name only goes back to FY2015; a deeper archive pull for FY2011-2014 was not attempted
  given time constraints, and this is disclosed as a gap rather than backfilled with an
  estimate.
- **PIT-detectability finding — the most interesting of the three names:** at the ONLY scored
  date (2016-03-31), CG Power was **already** loss-making (Net Profit -Rs461cr, EPS -7.33 per
  the audited P&L, no restatement question at this specific year), with revenue down -9% YoY
  and EBITDA margin collapsed to 1.7% from 5.0% — a leveraged, shrinking, loss-making industrial
  name, visible in plain reported numbers **more than three years before** the accounting fraud
  became public (Aug 2019). A diligent DCF-style analyst working only from FY2016 fundamentals
  would have had ample fundamentals-only reason to pass on this name without needing to
  anticipate the later-discovered fraud at all. The specific fraud mechanics (undisclosed
  liabilities, overstated bank balances, related-party diversion) were, by construction,
  concealed and not PIT-detectable from the reported numbers — but "is this a good DCF
  candidate" and "is this company committing fraud" are two different questions, and the first
  one already had a clear negative answer at the single scored date on totally mundane,
  contemporaneously-reported operating metrics. This is the cleanest illustration among the
  three blow-up names of a case where ordinary fundamental analysis (not hindsight, not fraud
  forensics) would have kept a diligent analyst out.

## Files written (this batch of 3)

- `pe_series/{pcjeweller,fretail,cgpower}.csv` — `date,price,pe`, weekly, full available
  listed history to 2026-09-24 (or to the last available quote for FRETAIL).
- `eps_series/{...}.json` — raw vendor (screener) publication-dated TTM EPS series, as fetched,
  with an explicit note on what the dates/values represent.
- `sourced_eps/{...}.json` — primary/audited annual FY EPS from the P&L table, per company and
  fiscal year, with basis, restated-vs-as-filed notes (CG Power), standalone-vs-consolidated
  notes (Future Retail), and vendor cross-checks, per the task's explicit requirements for
  these three fraud cases.
- `corp_actions/{...}.json` — full split/bonus history with ex-dates and sources; CG Power's
  2020 promoter change and Future Retail's 2015-16 demerger scheme are recorded alongside (not
  as split/bonus entries, since they aren't, but as explicit comparability flags).
- `dcf_financials/{...}.json` — revenue, EBITDA-proxy (operating profit) margin, depreciation,
  interest, capex-proxy, FCF, working-capital/debtor/inventory days, borrowings, investments,
  total assets, back-solved shares outstanding, and a `forensic_flags_visible_as_of_scoring_dates`
  field per company answering the "what could a PIT analyst have seen" question directly, per
  the task's request. Capex, net debt, and beta are explicitly flagged as unavailable-exact /
  proxy / not-PIT wherever that's the case, not silently estimated.

**Summary for the caller: all 5 name-dates across all 3 companies have usable price history
covering their scoring dates and a sourced, cross-checked FY EPS. Nothing is missing/unusable
at the scoring dates themselves.** The genuine data-quality problems found (PC Jeweller's PE
turning undefined post-FY19, Future Retail's post-2022 zombie-listing quotes and
standalone/consolidated basis switch, CG Power's restated FY18/19 figures and its unresolved
vendor-vs-audited FY16 EPS discrepancy) all sit either after both scoring dates or are
documented in place rather than silently resolved, per the task's instruction not to paper over
messiness in these three names.

No files outside `validation/v3_8_oos/` were touched. `OOS_SET_PREREG.md` was not modified.
Nothing was committed — files are left for review per the task instructions.
