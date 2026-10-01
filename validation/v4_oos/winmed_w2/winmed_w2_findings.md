# W2 findings — mid/small-cap winner selection (Phase-D, evidence-only)

Worker W2, axis: chemicals / auto ancillaries / capital goods / specialty manufacturing / niche financials.
NOT LIVE: no company is called investable. No engine/spec changes, no Phase-D execution, no price-data fitting, no tuning.

## Funnel

| Stage | Count |
|---|---|
| Ideas brainstormed | 14 |
| Exclusion triage (burn 243 + prior 77 company tokens, symbol-normalized lowercase/strip-spaces/&-to-and) | 12 pass, 0 kills |
| Slug resolution (screener search API) + March-FY confirm + listed-at-d0 | 12 pass |
| Firewall batch (informational only, NOT a gate) + P&L year-span assertion | 10 leads, 2 data-wall kills |
| Final leads | 10 companies, 20 name-dates (9× 2020∩2021 doubles, 1× 2021∩2022 double) |

## Exclusion kills

Zero. All 12 ideas passed burn_list_winmed.json (243 tokens) and prior_sets_winmed.json (77 company tokens) at symbol level. Renamed/demerged map checked: no identity collisions with R1–R7 blow-up companies (e.g. Uno Minda/Minda Industries deliberately NOT used — burn contains mindacorp (Minda Corporation) and the name similarity is a confusion hazard; Timken killed on data, not exclusion).

## Leads (one-line theses)

| # | Company | Sector | Name-dates (scoring FY / consol EPS) | Thesis |
|---|---|---|---|---|
| 1 | Aarti Industries (AARTIIND) | Specialty chemicals | 2020-03-31 (FY19/14.18), 2021-03-31 (FY20/15.39) | Benzene-derivatives leader; China+1 import substitution + capex-led earnings drove multi-year compounding FY19–FY24. |
| 2 | Vinati Organics (VINATIORGA) | Specialty chemicals | 2021-03-31 (FY20/32.48), 2022-03-31 (FY21/26.20) | Global leader in niche organics (IBB/ATBS), dominant share, high ROCE; multi-bagger FY19–FY22. |
| 3 | Atul (ATUL) | Chemicals (diversified) | 2020-03-31 (FY19/145.72), 2021-03-31 (FY20/224.69) | Diversified chemicals major; ~20%+ earnings compounding FY18–FY22 re-rated it as a core specialty-chemicals compounder. |
| 4 | Balkrishna Industries (BALKRISIND) | Auto ancillary (OHT tires) | 2020-03-31 (FY19/40.02), 2021-03-31 (FY20/49.64) | Off-highway tire leader; export-driven volume + margin expansion compounded ~4–5× FY19–FY24. |
| 5 | Endurance Technologies (ENDURANCE) | Auto ancillary | 2020-03-31 (FY19/35.19), 2021-03-31 (FY20/40.20) | 2W/4W ancillary (aluminium casting/suspension); OEM share gains + premiumization drove steady compounding FY19–FY24. |
| 6 | Cummins India (CUMMINSIND) | Capital goods (power gen) | 2020-03-31 (FY19/26.79), 2021-03-31 (FY20/25.45) | Power-gen/data-center demand + CPCB-IV norms drove a FY20–FY24 re-rating multi-bagger. |
| 7 | Elgi Equipments (ELGIEQUIP) | Capital goods (compressors) | 2020-03-31 (FY19/3.25), 2021-03-31 (FY20/1.34) | Air-compressor re-rating FY20–FY24 on export growth and margin expansion off a weak FY20 earnings base. |
| 8 | Aavas Financiers (AAVAS) | Niche financial (HFC) | 2020-03-31 (FY19/22.54), 2021-03-31 (FY20/31.80) | Affordable-housing NBFC; 30%+ AUM/PAT CAGR FY18–FY22, re-rated as a quality retail lender post Oct-2018 listing. |
| 9 | Fine Organic (FINEORG) | Specialty chemicals | 2020-03-31 (FY19/44.43), 2021-03-31 (FY20/53.74) | Oleo-chemicals/food-additives leader; high-ROCE compounding FY19–FY24 post Jul-2018 listing. |
| 10 | Grindwell Norton (GRINDWELL) | Specialty mfg (abrasives) | 2020-03-31 (FY19/15.10), 2021-03-31 (FY20/16.48) | Saint-Gobain abrasives/ceramics arm; consistent 20%+ compounding, defensive industrial compounder FY19–FY24. |

## Per-lead scoring FY + EPS + corp actions

(All consolidated EPS ₹, from screener cache; corp actions from Yahoo Finance chart-events feed; scoring FY per 63-day PIT rule.)

| Lead | d0 | scoring FY | EPS (scoring FY) | EPS series FY18–FY21 | Corp actions |
|---|---|---|---|---|---|
| aartiind | 2020-03-31 | 2019 | 14.18 | 10.24 / 14.18 / 15.39 / 15.02 | 2:1 splits Aug-2019, May-2021 |
| aartiind | 2021-03-31 | 2020 | 15.39 | same | same |
| vinatiorga | 2021-03-31 | 2020 | 32.48 | FY20 32.48 / FY21 26.20 (consol starts Mar 2020) | 2:1 split Jan-2020 |
| vinatiorga | 2022-03-31 | 2021 | 26.20 | same | same |
| atul | 2020-03-31 | 2019 | 145.72 | 93.21 / 145.72 / 224.69 / 221.64 | none |
| atul | 2021-03-31 | 2020 | 224.69 | same | none |
| balkrisind | 2020-03-31 | 2019 | 40.02 | 38.06 / 40.02 / 49.64 / 60.91 | 5:1 Nov-2010, 2:1 Nov-2017 |
| balkrisind | 2021-03-31 | 2020 | 49.64 | same | same |
| endurance | 2020-03-31 | 2019 | 35.19 | 27.78 / 35.19 / 40.20 / 36.95 | none |
| endurance | 2021-03-31 | 2020 | 40.20 | same | none |
| cumminsind | 2020-03-31 | 2019 | 26.79 | 25.68 / 26.79 / 25.45 / 22.91 | 7:5 Aug-2011 |
| cumminsind | 2021-03-31 | 2020 | 25.45 | same | same |
| elgiequip | 2020-03-31 | 2019 | 3.25 | 3.01 / 3.25 / 1.34 / 3.23 | 2:1 Nov-2010, 2:1 Aug-2020 |
| elgiequip | 2021-03-31 | 2020 | 1.34 | same | same |
| aavas | 2020-03-31 | 2019 | 22.54 | 13.45 / 22.54 / 31.80 / 36.80 | none |
| aavas | 2021-03-31 | 2020 | 31.80 | same | none |
| fineorg | 2020-03-31 | 2019 | 44.43 | 31.09 / 44.43 / 53.74 / 39.24 | none |
| fineorg | 2021-03-31 | 2020 | 53.74 | same | none |
| grindwell | 2020-03-31 | 2019 | 15.10 | 13.53 / 15.10 / 16.48 / 21.60 | 2:1 Jun-2016 |
| grindwell | 2021-03-31 | 2020 | 16.48 | same | same |

## Informational firewall ratios (P_d0/P_G1, plausibility NOT a gate)

| Lead | 2020-03-31 | 2021-03-31 | (2022-03-31) |
|---|---|---|---|
| aartiind | 0.946 T | 1.469 T | — |
| vinatiorga | uncomputable | 1.565 T | 2.555 F |
| atul | 0.947 T | 1.351 T | — |
| balkrisind | 0.754 T | 2.065 F | — |
| endurance | 0.611 T | 1.397 T | — |
| cumminsind | 1.046 T | 2.736 F | — |
| elgiequip | 1.127 T | 7.985 F | — |
| aavas | 3.543 F | 6.033 F | — |
| fineorg | 1.385 T | 1.592 T | — |
| grindwell | 1.646 T | 2.917 F | — |

Notes: aavas uses the financial (excess-return) model — all ratios >2; firewall is informational, selection stands on the public-history thesis. elgiequip_2021 ratio 7.985 driven by weak FY20 P_G1 base (EPS 1.34), not a pathology of the candidate. vinatiorga 2019/2020 d0s uncomputable — consolidated series starts Mar 2020 (see near-miss section).

## Near-misses (data-wall kills, NOT economics)

1. **Timken India (TIMKEN)** — screener consolidated P&L shows only Mar 2025→TTM (FY-end-change legacy: Sept→Mar); no computable scoring FY for any 2019–2022 d0. Kill = data availability, business itself is a genuine capital-goods compounder.
2. **AU Small Finance Bank (AUBANK)** — screener /consolidated/ page stale at Mar 2014–Mar 2017 while the standalone page runs to 2025; consolidated series unusable for 2019–2022 d0s. Kill = data availability, not economics. Coordinator note: do NOT silently substitute standalone — engine usability needs consolidated EPS.

## Data-integrity note (truncated-cache drill)

First batch run produced truncated caches for vinatiorga (Mar 2020→TTM), timken (Mar 2025→TTM), aubank (Mar 2014–Mar 2017). Per the R6 truncated-cache lesson: deleted and re-fetched; re-fetch returned identical spans, and raw screener HTML confirmed the truncation is SOURCE-side (screener's consolidated pages genuinely short for these), not a fetch artifact. Records retained in winmed_w2_firewall.json with this note; timken/aubank killed on the source wall, vinatiorga kept on its computable 2021∩2022 double.

## Deliverables

- winmed_w2_leads.json — 10 leads, 20 name-dates, theses, scoring FY, EPS series, corp actions, firewall numbers, kills.
- winmed_w2_firewall.json — 48 firewall records (10 symbols × 4 d0s + fineorg/grindwell), trusted spans only.
- cache/ — 10 screener cache JSONs (timken.json/aubank.json retained as the evidence behind the data-wall kills).
