# Phase-D Locked-Run Input Build Log

**Date:** 2026-10-01 · **Coordinator:** Phase-D data-assembly coordinator (subagent)
**Frozen engine:** `~/workspace/stock-judging/port/engine_v4/`, HEAD `a803966` on `main` (read-only; `run_name_date` NEVER called)
**Manifest:** `../SET_MANIFEST.json` (sha256 `107997d5daf8ffe1843b29e0ee3211cb2b9e1ee56d62759695e3755fc185cfc8`) — 25 name-dates / 13 companies
**Output dir:** `~/workspace/stock-judging/v3/validation/v4_oos/phase_d_inputs/`
**Status: 25/25 assembled · `schema_check.py` 25/25 PASS** (engine never executed — data assembly only)

## Workers
- **W1** — 10 winners (infy, sbin, srf, lt, endurance ×2) → `build_log_w1.md`
- **W2** — 10 mediocrities (drreddy, dabur, maruti, cyient, auropharma ×2) → `build_log_w2.md`
- **W3** — beta table + 5 blow-ups (supremeeng ×2, pbm ×2, varroc ×1) → `build_log_w3.md`

## 1. Beta — the one judgment input (W3, loudly documented)
- Source: **Yahoo Finance 5Y-monthly adjusted closes vs NIFTY 50 (^NSEI)**; beta = cov(monthly_ret_stock, monthly_ret_nifty)/var(monthly_ret_nifty). Chosen because the Yahoo v8 chart API was fetchable for all 13 incl. SME/BSE names; investing.com bot-checks, moneycontrol unreliable.
- 13/13 slugs in `_beta_table.json`, 60-month windows, as_of 2026-09/2026-10.
- **PBM exception:** Yahoo PBMPOLY.NS had 1 overlapping month → used **PBMPOLY.BO** (BSE series, 59 months, as_of 2026-08) — named in table.
- Values: auropharma 0.8979, cyient 1.2816, dabur 0.8755, drreddy 0.4328, endurance 1.017, infy 0.7331, lt 1.2305, maruti 0.6806, pbm 1.0714, sbin 1.175, srf 0.7736, supremeeng 0.4801, varroc 1.2902.

## 2. Per-tier assembly summary

### Winners (W1) — 10/10, schema_check PASS, zero warnings
- FY tables: screener consolidated P&L/BS/CF via winmed caches; 14/14 cells spot-checked vs live screener HTML (see `_raw/_verify_cells.json`).
- **CA/CL: AR-sourced** (NSE-published audited results PDFs, consolidated, verified via statement headings) — infy FY18–20, srf FY17–19 (FY17 from FY18 comparative; FY17 standalone PDF scanned/unextractable), lt FY19–21, endurance FY18–20 (PDFs in ₹ million, ÷10). This was W1's own initiative and is what makes D3 computable for winners.
- **SBIN CAMEL (D6):** deviation from "screener ratios" ideal — CAR from audited Basel III, GNPA from JM Financial, Cost/Income from MPRA, ROA audited, CASA from tradebrains/SBI AR. D6 totals: FY20 = 6 → PASS; FY21 = 7 → PASS (veto only if ≤4). Coordinator verified values match SBI's published figures (FY20 GNPA 6.15%, CAR 13.06%; FY21 GNPA 4.98%, CAR 13.74%).
- **Pledge (AR-sourced, Tijori AR mirror):** infy 0.0 (FY17–20, promoters "–" nil), srf 0.0, lt 0.0 (promoter 0%), endurance 0.0 (FY17–18; FY19/FY20 = named gap, see §4.4), sbin 0.0 (GoI promoter ~57%).
- results_published: **NSE corporate-announcements API** (actual announcement dates); all scoring FYs ≤ d0−63d. srf FY20 / endurance FY21 → None (not recovered; post-scoring, no PIT impact).
- Prices: 901 weekly adjusted closes (2009-07-03→2026-10-01); endurance 520 (listed Oct 2016). EPS series: unlagged publication-dated TTM EPS. Corp actions: Yahoo splits feed (bonuses reported as splits).
- Events: [] for all 10 — two-source tape check (NSE corp-ann API + AR/results PDF review) over [d0−12m, d0+24m]; no E1-grade events.
- equity_increase_solely_bonus_split: True except endurance_* = False (FY17 increase was the Oct 2016 IPO).

### Mediocrities (W2) — 10/10, schema_check PASS
- FY tables: screener consolidated via winmed_w3 caches. **CA/CL = None for 13/15 FYs** (screener static HTML JS-gates them; only Dabur FY19/FY20 from real AR: Mar-2020 CA 4,880.26/CL 2,463.88; Mar-2019 CA 3,586.23/CL 2,660.31). → D3 UNCOMPUTABLE → VETOED-DATA expected on affected name-dates (honest; mediocrities need no fills).
- results_published: sourced via browser.search (press releases, broker notes, BSE filings) — all scoring FYs comfortably ≤ d0−63d. Weaker sourcing than W1's NSE API but PIT holds with wide margin.
- Prices: 901 weekly adjusted closes/company. Pledge: drreddy/dabur/maruti/cyient 0%, auropharma 3.49%/4.99% (D1 PASS). Sectors verbatim.
- Events: [] — two-source check; findings logged but non-qualifying (Dr Reddy's FCPA probe Nov 2020 disclosed, closed 2026 — not a §5.1 subcase; Maruti ex-MD personal case; Aurobindo 2024 FIR — outside windows/non-company).

### Blow-ups (W3) — 5/5, schema_check PASS
- FY tables: screener P&L (standalone for SUPREMEENG per R3; consolidated for PBM/VARROC). Sectors verbatim: supremeeng "Capital Goods", pbm "Textiles", varroc "Automobile and Auto Components" (all non-financial).
- **E1 events (tier-1 sources, `events.grade_all` verified by coordinator):**
  - supremeeng_2020/2021: 2021-11-03, T2 `resignation_citing_disagreement_fraud_or_unpaid_fees` → **SEVERE** (NSE filing, R T Jain & Co fee-dispute resignation).
  - pbm_2019/2020: 2020-09-30, T2 `resignation_no_stated_reasons` → **MODERATE** (BSE intimation scrip 514087; underlying 18-Jul-2020 letter URL now serves the 2022 successor filing, unrecoverable).
  - varroc_2019: 2020-06-25, T2 `opinion_qualified` → **MODERATE** (FY20 audited-results filing, SRBC & Co consolidated "Qualified Opinion", ₹943.68M disputed warranty claim).
  - NOTE: W3's prose/table said varroc → SEVERE; coordinator re-ran `grade_all` on the frozen engine — `opinion_qualified` grades **MODERATE**. The JSON data was correct; the prose was wrong.
- results_published = board-meeting/AR-signing proxy; all scoring FYs ≥63d PIT. Post-E1 FY extension present (cooling-off windows verified).
- Pledge: [] = "not visible in static HTML", not zero. CA/CL, material_cost, revaluation_reserve: None (JS-gated).
- **PBM prices:** screener chart API served only ~25 recent points server-side (verified source-side) → Yahoo PBMPOLY.BO weekly adjusted closes, 320 weeks from 2000-01-31, as_of 2026-08-31; cross-checked ±12% vs R6's screener-sourced P_d0.
- **PBM EPS series:** 1 point only (2026-09-15, 2.67) → U3 UNCOMPUTABLE (honest engine outcome; U1/U2 unaffected).
- Corp actions: SUPREMEENG.NS 1:10 ex 2022-03-03 (post-window); varroc FY18 ₹10→₹1 subdivision has no Yahoo record (named note); pbm none.

## 3. Coordinator verification (all 25)
- `schema_check.py` (in this dir): **25/25 PASS** — exact 16-field NameDate construction (no engine execution), prices strictly ascending with ≥12m pre-d0 coverage (varroc excepted, named) and as_of ≥ d0+24m, `select_scoring_fy` == manifest scoring_fy for all 25 (63-day PIT), FY-window coverage, beta present, blow-up `events.grade_all` passes.
- **Cross-validation spot-checks** (W3 closed before running job 3; coordinator ran them directly):
  1. drreddy FY18 net_profit 947.0 / eps 11.41 in JSON == live screener consolidated P&L Mar-2018 (947 / 11.41). ✅
  2. infy FY19 CA ₹52,878cr / CL ₹18,638cr — plausible vs Infosys published consolidated BS; internally consistent. ✅
  3. sbin FY20/FY21 CAMEL values match SBI's published figures (GNPA 6.15%/4.98%, CAR 13.06%/13.74%). ✅
  4. Pledge lists PIT-valid (quarter_end ≤ d0, AR-sourced for winners). ✅
- **Corrections made by coordinator:** (a) varroc grading prose (above); (b) 2 bugs in `schema_check.py` found by W3 — None-date parse crash, FY-window-vs-tail check — both fixed (see AGENTS.md).

## 4. Named gaps & caveats (never interpolated)
1. **CA/CL absent for W2 mediocrities (13/15 FYs) and all W3 blow-ups** → D3 UNCOMPUTABLE → VETOED-DATA expected there. Winners got the AR pass (W1 initiative); the AR pass was NOT extended because no bar leg requires mediocrity fills and blow-up decisionality runs through D4/D5 trips (D3 would PASS, not trip, for these profitable names).
2. **Mcap convention:** all workers used 2026-10-01 quote pairs (mcap_cr @ mcap_price); the engine uses only the ratio (shares outstanding). AR-derived cross-check: infy −6.5%/−4.4% (buybacks), lt −2.1%, sbin +3.4% — worst case ±7% on per-share triggers, mild pro-fill bias on infy. Uniform, pre-run, spec-silent, documented.
3. **SBIN CAMEL from secondary sources** (JM Financial/MPRA/tradebrains for GNPA/Cost-Income/CASA) — values verified against SBI published figures; documented deviation from pure-primary ideal.
4. **endurance Mar-2019/Mar-2020 pledge:** ARs contain zero "pledge" mentions → named gap; lists use Mar-2017/Mar-2018 (latest PIT-valid sourced). D1 verdict unaffected (0.0 → PASS either way).
5. **PBM:** 1-point EPS series → U3 UNCOMPUTABLE; Yahoo-BSE price basis (±12% vs screener P_d0).
6. **Varroc:** listed 2018-07-06 → 38 pre-d0 weeks (<12m); FY14 absent at screener span limit.
7. **Short FY spans at screener's span limit:** supremeeng FY15, pbm FY14, maruti/drreddy FY14–15, dabur FY15–16, cyient FY16 — engine delta() fail-closed handles missing priors.
8. **material_cost = None** (W2/W3) → F_dMARGIN fail-closed 0 (spec-sanctioned). **audited_eps_by_fy = None** (all) — Gate-1 audited/sourced ≈1.0 stands.
9. **srf FY20 / endurance FY21 results_published = None** (post-scoring, no PIT impact). **srf FY17 CA/CL** from FY18 comparative.

## 5. Adjudication items for parent (pre-run)
- (a) Mcap convention (§4.2): accept as-is, or require AR-derived shares (13 face values to source)? Coordinator recommends accept — bounded, uniform, documented.
- (b) SBIN CAMEL secondaries (§4.3): accept (values verified sane) or require Pillar-3/AR-only re-source?
- (c) W2's results_published via search snippets (weaker than W1's NSE API): all comfortably PIT-valid; accept.
- (d) The AR-sourcing question from the interim report is RESOLVED for winners (W1 did it); not extended to others per §4.1 rationale.

## 6. Parent audit decisions (2026-10-01, pre-run — Musey)
- (a) **REJECTED accept-as-is; fixed.** 2026-10-01 quote pairs replaced by scoring-FY audited shares on the price series' adjusted basis: `shares = equity_capital(scoring FY)/face_value × Π(split/bonus factors with ex_date > scoring-FY end)`; `mcap_price` = last close on/before d0. Rationale: known pro-fill bias on winners (infy buybacks: −6.9% share drift) is unacceptable on a validation run; the fix is mechanical, uniform, PIT-valid, pre-result. Face values sourced: `_raw/*_series.json` top_ratios (infy 5, sbin 1, srf 10, lt 2, endurance 10); screener.in live top_ratios 2026-10-01 (drreddy 1, dabur 1, maruti 5, cyient 5, auropharma 1, varroc 1 consol+standalone agree); company/514087 (pbm 10); standalone (supremeeng 1, cross-checked vs equity_capital-implied count). Full delta log: `_mcap_fix_log.txt`.
- **Rev-1 bug caught in the same audit:** raw scoring-FY shares are on the wrong basis when a post-FY-end split/bonus exists (SRF 5:1 bonus 2021-10-13 → −80% share error). The adjustment factor (ex_date > scoring-FY end) fixes it; it also caught Dr Reddy's 5:1 split 2024-10-28 (genuine) and a **spurious Yahoo 10:1 "split" for supremeeng ex 2022-03-03 — deleted** (no price discontinuity in the adjusted series; 2026 quote pair implies 25cr shares = FY19–FY23 equity_capital-implied count; equity capital flat ₹25cr FY19–FY23; no split occurred). Deletion also protects U1/U2 restatement checks from the phantom action.
- (b) **ACCEPTED** — SBIN CAMEL values verified against published SBI figures; documented as secondary-sourced.
- (c) **ACCEPTED** — all results_published comfortably PIT-valid (wide margins); snippet precision immaterial.
- (d) Noted. Final JSONs verified clean; schema_check 25/25 PASS after the mcap fix.
