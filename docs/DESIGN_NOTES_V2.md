# DESIGN_NOTES_V2 — "Desk" (2026-10-07)

## Committed direction
**Editorial Trading Desk (Swiss) × Linear dark.**

- **Master lineage:** Swiss/International Typographic Style (Müller-Brockmann) — hairline rules, numbered sections, grid discipline, tabular numerals. No other lineage is mixed in.
- **Modern system:** Linear dark — near-monochrome canvas, luminance ladder (not translucency), one accent used as ink.
- **Why:** Bablu's feedback on round 1 was "too minimal, looks AI-generated and boring, too text-centric." The anti-AI-slop pass (design-doctor skill) showed round 2's card grid was itself an AI tell (bento grid, aurora gradients, glow, sans-only). The fix isn't *more* decoration — it's a committed editorial voice: a research desk's ledger, not a dashboard of cards.

## What changed from v2-round-2
- **Leaderboard:** card grid → **ledger rows**. Each row: index number, identity (flat serif-initial tile + name/ticker/date/star), flat verdict marker (8px square + label), serif composite score + mini bar, serif price + FV, sparkline (flat 1.5px line + endpoint dot), metric chips (MoS / Q / 3M / sector). Hairline-divided, sortable via header or pills.
- **Signature elements:** (1) masthead with `Stock-Judging®` serif wordmark + `ENGINE V6 · RESEARCH DESK` mono tag + LIVE indicator; (2) **ticker strip** — all 23 covered names with price ±3M% in a slow marquee (pauses on hover, disabled under reduced-motion); (3) **numbered section indices** (`01 / Leaderboard`, `02 / Investor Activity`).
- **Company page:** hero flattened (no radial-gradient blobs) — 3px category top-rule, kicker line, serif display name, dials as flat rings beside big serif numbers with plain-English notes. Thesis in serif at reading size. Risks as hairline rows with red square markers (no red wash). Score/SHP bars are 3–4px flat bars.
- **Type:** `ui-serif` (New York/Georgia) for display — company names, scores, prices, headlines. System grotesk for UI. `ui-monospace` for labels/tickers/dates. **Tabular numerals on all data** (`font-variant-numeric`).
- **Color discipline:** one accent (`#58a6ff`, Linear blue) used as ink — active filter underline, links, focus, sort arrows, section indices. Category colors kept (green/amber/blue/gray/red) but **flat** — no glow, no gradient backgrounds; they appear as markers and text only. Sparkline up/down color encodes direction only. Zero gradients in the entire stylesheet except the skeleton shimmer.
- **Motion:** card entrance animation **removed** (it hid content at `opacity:0` — a fatal bug). Score rings still draw on load (additive: rings render at 0 and animate to value). Row hover is a 3% luminance lift. Ticker marquee 90s loop.
- **Logo tiles:** were per-symbol rainbow gradients → now flat raised tiles with serif initials and a hairline border. Color on logos carried no meaning, so it was removed.

## Bug fixed along the way (design depended on it)
`categoryMeta()` keyed on `"INVEST_NOW"` but data carries `"INVEST NOW"` (space) — badges rendered gray `badge-unknown`, hero category classes missed, and the decision note fell through to "Category not set". Added `catKey()` normalizer (space/hyphen → underscore, uppercase) used in `categoryMeta`, row classes, hero classes, and the note lookup. **Note: the live `frontend/` (v1) has the same bug** — its badges are gray and its decision notes read "Category not set". Flagged to parent; v2 is fixed.

## design-doctor rubric self-score
- Direction committed (Swiss × Linear): 1/1
- Type pairing (serif display + grotesk + mono, tabular numerals): 1/1
- Visible structure (hairlines, numbered sections, felt grid): 1/1
- Spacing rhythm (non-uniform scale, intentional density): 0.5/1
- One disciplined accent (single blue as ink): 1/1
- Signature element (masthead + ticker + indices): 1/1
- Product centerpiece (ledger as the data surface): 1/1
- Depth (luminance ladder, hairlines, no glow): 1/1
- Motion (no content-hiding animation; additive rings; reduced-motion safe): 1/1
- Interaction states (hover/focus-visible/active, no decoration-only states): 1/1
**≈ 9.5/10.** No auto-fails: no aurora, no glow, no bento, no sans-only, no hidden-at-rest animation.

## Tradeoff vs the original brief
The brief asked for "company cards, not just rows." The ledger *is* rows — but each row carries the card's content (logo, badge, score ring→number+bar, sparkline, chips) in a denser, more distinctive editorial form. The bento-card alternative scored as AI-slop under the audit rubric; the ledger is the more premium-fintech answer (Bloomberg terminal > Dribbble shot). If Bablu wants cards back, that's a taste call, not a quality gap.

## QA
- Served via `python3 -m http.server`, screenshot via CDP (file:// harness with inlined data, since Chrome blocks loopback).
- Verified: leaderboard 1280px, 768px, 390px; company page 1280px, 390px (KKCL).
- All functionality preserved: filters, sort (pills + header), stars, investor section, news/deals, SHP, moves, calibration, best-today/overall, run page. Logic untouched — only CSS + presentational markup + the catKey bugfix.
- `node --check` clean on all JS.

## Files
- `frontend-v2/css/styles.css` — full rewrite (Desk system)
- `frontend-v2/index.html` — masthead, ticker host, numbered sections
- `frontend-v2/js/data.js` — `catKey()`, `verdictHTML()`, flat `scoreRingHTML`/`sparklineHTML`/logo
- `frontend-v2/js/leaderboard.js` — ledger rows, ticker render, header sorting
- `frontend-v2/js/company.js` — flat hero, dial text, catKey fixes
