# Equity Review Standard v3 — Full Scoring Spec

**Status:** approved for build by Bablu, 23 Sep 2026. Paste-ready for the Claude project.
**Supersedes:** Standard v2 (locked 6 Sep 2026). Unchanged v2 pipeline (SCREEN→FULL flow, Note/Record/League Table artifacts, evidence-density rule, cost rule, reverse screen, developments) is not restated here — this spec covers everything that changes plus every test definition.
**Basis:** the 23 Sep 2026 technical briefing (52 reviews audited) and the approved v3 rebuild proposal.
**Build status:** engine v3.0 built 23 Sep 2026 (`v3/engine_v3.py.md`); **not live** — §12 historical calibration is blocking.

---

## 0. What changes and why

1. **One rate becomes two.** v2's 13–17% COE did two jobs — valuing the business and setting your required return — and the conflict zeroed out the entire price half of the scorecard (D1 = 0 in 53 of 53 scorecards). v3 values at a market-consistent rate and applies your personal hurdle only to the entry decision.
2. **Quality and Price are scored separately and tiered honestly.** A great business at the wrong price is now INVEST AT TRIGGER with a named price, not PASS.
3. **Forensics stop punishing retrieval failures.** Unverifiable checks are excluded, never zeroed.
4. **Your factors are scored.** Promoter buying/selling direction and quarterly trajectory become tests; the credibility audit runs in lite form at SCREEN.
5. **Engine defects fixed, knife-edges smoothed, spec contradictions resolved.**
6. **Historical calibration is blocking.** v3 does not judge live candidates until it has been tested against history (§12).

---

## 1. The two rates

| Rate | Symbol | Job | Value (India) |
|---|---|---|---|
| Valuation rate | `r_val` | Discount rate for fair value. Must be market-consistent. | **6.95% + β × 4.0%** (≈ 10.95% at β = 1) |
| Hurdle rate | `r_hurdle` | Your required return. Decides the trigger, never the valuation. | **15%** |

- **Beta:** measured, two-year weekly vs Nifty 500, ≥ 40 observations. Fallback is the **industry** beta (Damodaran or equivalent), never an assumed ≥ 1.0.
- **WACC:** uses the company's actual or target capital structure. Pre-tax cost of debt = Rf + 2% spread, post-tax × (1 − tax). Net-cash companies stay all-equity. The all-equity default is deleted.
- **Terminal growth:** one rule — **≤ 4%**, engine default 4%. All v2 contradictions (§3 vs §7 vs instructions vs engine) resolve to this.
- **Risk-free / tax:** Rf 6.95% (India 10-yr G-Sec, re-run rule at ±25bp moves stays). Tax = max(company rate, 25.17%).
- **Quality tests** (A1, A5, C3) benchmark against `r_val`. **Entry tests** (trigger, E1) benchmark against `r_hurdle`.

---

## 2. Quality / Price split and tiers

Every dimension is scored 0–10. Then:

- **Quality Q** = (0.15·A + 0.20·B + 0.20·C + 0.10·F) ÷ 0.65 — *how good is this business?*
- **Price P** = (0.15·D + 0.20·E) ÷ 0.35 — *is it buyable, and at what price?* Computed **at the trigger** for tiering, and separately **at today's price** for timing. Both are reported: e.g. "Q 6.8 · P@trigger 7.2 · P@today 3.1 — wait for ₹X."

| Tier | Rule |
|---|---|
| **INVEST NOW** | Gates pass · Q ≥ 7.0 · today's price ≤ trigger · trigger defensible |
| **INVEST AT TRIGGER** | Gates pass · Q ≥ 6.0 · trigger defensible |
| **WATCH** | Q 5.0–5.9, or Q ≥ 6.0 with no defensible trigger, or coverage-capped (§6 G1) |
| **PASS** | Q < 5.0, or any gate failed |

Dimension weights are unchanged. The League Table gains `v3` tags and Q / P@trigger / P@today columns. The "one test that moves the tier" line stays.

---

## 3. Test-by-test scoring

Interpolation rule (§8) applies to every numeric threshold below. Engine = auto-scored; Manual = judgement with cited numbers.

### Dimension A — business quality (15%), 6 tests, each 0–2, rescaled to /10

| Test | 2 | 1 | 0 | Mode |
|---|---|---|---|---|
| A1 ROCE, 5-yr avg | > r_val + 5pp | > r_val | else | Engine |
| A2 Revenue CAGR, 5-yr | ≥ 12% with no down year | ≥ 8% | else | Engine on CAGR; manual override for the down-year condition |
| A3 EBITDA-margin range, 5 yrs | ≤ 5pp | ≤ 10pp | else | Manual |
| A4 Concentration | Top-5 < 20% of revenue and no relationship > 10% of profit | top-5 < 40% | else | Manual |
| A5 Incremental ROIC, 3-yr (ΔNOPAT ÷ Δcapital employed) | > r_val | positive | else; deliberate annuity payer with no reinvestment = 1 | Manual |
| A6 **Quarterly trajectory (new)** — last 4–6 quarters of revenue, EBITDA margin, CFO | all three improving or stably strong | mixed | 2+ of the three deteriorating | Manual |

### Dimension B — accounting quality (20%): the retrieval-aware forensic battery

- **B = 10 × (passes ÷ verified).** Continuous, not an integer count.
- **Unverifiable ≠ fail.** A check that cannot be verified is marked `[unverified]`, excluded from the denominator, and listed as a follow-up. It never scores zero silently.
- Every outright fail is at least a Moderate flag (unchanged).

| # | Check | Pass condition | Input |
|---|---|---|---|
| 1 | Cash conversion | Cum. CFO ÷ cum. EBITDA, 5–6 yrs ≥ 70% | cumulative CFO, EBITDA |
| 2 | Earnings backing | CFO ÷ PAT, 5-yr avg ≥ 80% | cfo_pat_5y_avg |
| 3 | Receivables | Debtor days up ≤ 10 days over 3 yrs **AND** receivable growth ≤ revenue growth (engine must test **both** limbs — v2 tested only the first) | debtor days start/end; receivables & revenue growth |
| 4 | Other income | < 10% of PBT. Exception: treasury income of a net-cash company (noted, not failed) | other_income, pbt, treasury exception flag |
| 5 | Contingent liabilities | < 10% of net worth | contingent_liabilities, net_worth |
| 6 | Related parties | RPT sales + purchases < 5% of revenue; group loans < 2% of net worth | rpt_total, revenue |
| 7 | Auditor | Reputable, unmodified opinion, clean CARO, no resignation; fee growth ≤ revenue growth over 3 yrs | auditor fields |
| 8 | Depreciation | Rate within ±2pp over 5 yrs; no capitalised opex; no profit-lifting policy change | dep rate start/end (needs gross block) |
| 9 | Cash is real, pledge de minimis | Yield on cash ≥ 4% **and** pledge **< 0.5% of shares outstanding** (materiality floor — v2 failed names on 0.0035%) | cash_yield, pledge_pct |
| 10 | Beneish | M-score < −1.78 (8-variable, last 2 yrs); leveraged names also need Altman Z > 2.99 | t, t1 blocks |

- **Checks 4 + 9 read together** (unchanged): yield far above deposit rates ⇒ balance is real (9 passes) but income is mark-to-market (4 fails). State the reconciliation in one line.
- **Financial-sector variant:** same retrieval-aware denominator logic on the 8-check battery; B = 10 × pass rate.

### Dimension C — governance and alignment (20%), 6 tests, each 0–2, rescaled to /10

| Test | 2 | 1 | 0 |
|---|---|---|---|
| C1 Promoter holding + pledge | 40–75%, zero material pledge (MNC parent at 75% = 2) | pledge < 10% of holding, or holding outside band | else |
| C2 Board and audit | Independent chair or lead ID, independent AC, reputable auditor, normal tenure, no resignation | one weakness | else (non-independent promoter-family chair caps at 1 — the Indian norm, scored honestly) |
| C3 Capital allocation, 5 yrs | M&A/buybacks/dividends with incremental ROIC > r_val, no goodwill impairment | mixed | destructive |
| C4 Disclosure | Segment data, calls held, trackable guidance, no restatement | partial | opaque |
| C5 Credibility audit (promise vs delivery) | ≥ 7/10 | 5–6.9, or not executable when C4 > 0 | < 5, or not executable when C4 = 0 |
| C6 **Promoter direction (new)** — net PIT buying/selling, trailing 4 quarters ÷ market cap | net buy > 1% of Mcap or > ₹50 Cr | −0.5% … +1% (neutral / modest) | net sell > 0.5% of Mcap |

- **C5 method (unchanged):** last 8 quarterly calls at FULL, recency weights 8→1, score = Σ(score×weight) ÷ (2×Σweight) × 10; quarters without an outcome yet are excluded and weights re-based; no calls ⇒ score the last investor forum and mark not executable. **Lite at SCREEN:** last 4 quarters, weights 4→1, same bands — no more defaulting to 1.
- **C6 counting rule:** open-market plus block/bulk deals by promoter/promoter group. Exclude ESOP allotments, warrant conversions, and inter-se promoter transfers.

### Dimension D — valuation and margin of safety (15%), computed at r_val

| Test | 2 | 1 | 0 | Mode |
|---|---|---|---|---|
| D1 Price vs conservative DCF midpoint | ≥ 20% below | 10–20% below **or** within ±10% (the v2 gap, now defined) | > 10% above | Engine |
| D2 Price vs peer-multiple range | below | inside | above | Manual |
| D3 Reverse-DCF implied growth vs delivered | implied ≤ delivered 5-yr | implied ≤ guidance × 0.7 (**engine must implement this band — v2 returned only 2/0**) | above, or unsolvable | Engine |
| D4 P/E vs own 10-yr median | ≥ 20% below | within | above. **Missing median = 1 (neutral), consistently** — v2 scored 0 or 1 at random | Manual |
| D5 Cycle position | Current EBITDA margin ≤ 10-yr avg | within +3pp | at/above peak | Manual |

### Dimension E — risk/reward (20%), scenarios run at the **trigger** price for tiering

| Test | 2 | 1 | 0 | Mode |
|---|---|---|---|---|
| E1 Probability-weighted 3-yr return, annualised, at trigger | ≥ r_hurdle + 5pp | ≥ r_hurdle | below | Engine |
| E2 Bear-case drawdown from trigger | ≤ 20% | ≤ 35% | worse | Engine |
| E3 Upside ÷ downside at trigger | ≥ 3 | ≥ 1.5 | else | Engine |
| E4 Bear probability | ≤ 25% | ≤ 35% | else — **reachable again now that the bear weight is derived from a 25% base (§5)** | Engine |
| E5 Liquidity: ₹1 Cr at 25% of median daily value | ≤ 5 sessions | ≤ 10 sessions | else | Engine-computed, entered manually |

### Dimension F — thesis and catalysts (10%)

| Test | 2 | 1 | 0 |
|---|---|---|---|
| F1 Variant perception | stated and falsifiable | stated but consensus-adjacent | none |
| F2 Return decomposition | ≥ 60% of 3-yr expected return from EPS growth + dividends | ≥ 40% | multiple-dependent |
| F3 Dated catalyst | within 12 mo, with confirm/deny evidence | within 36 mo | none |
| F4 Confirm/deny observable | quarterly, public data | annually | not observable |
| F5 Archetype fit + marquee | 4/4 **and** priority name (Nomura / Kacholia / M. Agrawal) present and adding or holding | 3/4, or marquee present but trimming | ≤ 2/4, **or** a priority name exiting |

- **At SCREEN, if the marquee screen is skipped, F5 is excluded** and F rescales from the other four (÷8×10). Not looking is not a negative signal. At FULL the full rule applies.

---

## 4. Valuation machinery

### 4.1 Conservative DCF (FCFF, 5-yr explicit)

- Growth ≤ min(industry CAGR, 12%) unless delivered history justifies more. Margin fades linearly to the 10-yr average. Tax = max(company, 25.17%).
- **Terminal normalisation (defect fix):** year-5 FCFF is normalised before capitalising — working capital charged at **terminal** growth (not explicit-period growth; v2 understated value ~18%), capex faded to maintenance (= depreciation, per the USA engine v1.1 fix).
- TV = FCFF_norm × (1+g) ÷ (w − g), g ≤ 4%. Value/share = (ΣPV + PV(TV) + net cash − minority adjustments) ÷ shares.
- Discount = WACC at **r_val** with real capital structure (§1). Sensitivity grid WACC ±1pp; reported range = min–max.
- **Negative/degenerate DCF:** D1 = 0 with a flag. Never auto-2 (the v2 Vodafone Idea/DMart bug).

### 4.2 Peer multiples (unchanged method)

6–7 peers + industry leader; EV/EBITDA for capital-intensive, P/E for stable earners, EV/Sales pre-profit, P/B–P/ABV for financials; justified = peer median ± named adjustments; band ±15%; applied to FY+1 earnings from a stated source; same operating forecast as the DCF.

### 4.3 Reverse DCF

Solves for the explicit-period growth the price implies at the r_val WACC. **Solver fix:** guard the non-monotonic region above ~60% growth (v2's bisection broke there — Latent); sane bounds; if unsolvable on growth, restate as implied terminal margin **and** implied discount rate at input growth. This output stays the single most informative line in the review: *"the price assumes X."*

### 4.4 Range rule and the trigger (rebuilt)

```
DCF range [d_lo, d_hi] (WACC ±1pp grid).
Multiples range [m_lo, m_hi].
Overlap ⇒ fair value = overlap MIDPOINT (not the floor — v2 double-charged conservatism).
Disjoint ⇒ no blended fair value; both ranges shown side by side.
P_hurdle = highest price earning IRR ≥ 15% on the DCF base-case cash flows.
Trigger  = P_hurdle, when the DCF is usable.
MoS nod  = Y iff current price ≤ 0.80 × fair value (overlap) or 0.80 × DCF midpoint (disjoint).
```

- **One haircut, once.** The old stack (conservative floor × 0.8) is gone. The trigger is set by your hurdle alone; the 20% MoS survives only as the informational nod, per your stated philosophy.
- **Honest consequence:** at r_val ≈ 11%, buying 20% below fair value earns ≈ 12–13% IRR — *below* your 15% hurdle. So the hurdle binds first: expect triggers ≈ **30–40% below fair value** in typical long-duration names. That is your capital-preservation bar talking, not a bug.
- **"No defensible entry":** if the DCF is unusable (≤ 0, degenerate) ⇒ trigger = None, tier caps at WATCH. If P_hurdle > d_hi ⇒ flag "unhealthy" (your 15% entry still pays above the conservative range) and report the IRR earned at the trigger vs the hurdle.
- **INVEST AT TRIGGER requires a defensible trigger** (adopts the USA engine's V-8 rule — v2's engine didn't check).

### 4.5 Mini-example (illustrative)

Fair value ₹100 at r_val 11% ⇒ P_15% ≈ ₹60–65 ⇒ **trigger ≈ ₹62**, MoS nod line at ₹80. At ₹62 the buyer earns 15% on DCF cash flows; at today's ₹95 the P@today score says "wait."

---

## 5. Scenarios and the bear weight (E1–E4 inputs)

- Three cases (bear/base/bull); 3-yr value = exit EPS × exit multiple + dividends. Return decomposition (EPS growth + multiple change + yield) and the compact 3×3 grid with confirm/kill observables (unchanged).
- **Bear weight derivation (contradiction fix):** start at the **25%** base; **+5pp per documented independent bear trigger**, capped at 45%. The 35% schema example is deleted. Because the base is 25%, **E4 = 2 is reachable again** (no triggers ⇒ 25% ⇒ 2 points). A weight repeated unchanged across unrelated names is still a default and must be called out.

---

## 6. Gates (any failure ⇒ PASS)

| Gate | v3 rule |
|---|---|
| **G1** | **Retrieval-aware.** Compute on verified checks only. Clears iff **verified ≥ 7 AND pass rate ≥ 60%**. If **verified < 7**, the tier caps at **WATCH** with the missing checks named as the promotion condition ("do more work," not "reject"). |
| G2 | Unchanged: live formal charge/order/debarment that could end a revenue stream. |
| G3 | Unchanged: ₹1 Cr reference position must exit within 10 sessions at 25% of median daily value. |
| G4 | Unchanged: going-concern paragraph, qualified opinion, auditor resignation, or IFC qualification within 2 years. |
| G5 | Unchanged: no UPSI in the thesis. |
| G6 | Unchanged (private only). |

---

## 7. SCREEN vs FULL

- **SCREEN** runs everything above, with lite C5 (4 quarters) and F5 rescaled when the marquee screen is skipped. Target cost unchanged (~15–20% of FULL).
- **Escalation to FULL:** Q ≥ 5.5 **and** G1/G4 clearable **and** verified ≥ 7 — or the user types "full". FULL adds: full 8-quarter credibility audit, marquee screen, reverse screen, developments, peer table, growth bridge, entry/exit plan (unchanged v2 content).

---

## 8. Anti-knife-edge rule (threshold interpolation)

For every numeric threshold T separating adjacent levels: inside the band **[0.9·T, 1.1·T]** (relative) — or **±1pp** for percentage-point thresholds like margin range — the score **interpolates linearly** between the levels, reported to one decimal. Outside the band, the level. Birlasoft's 19.80%-vs-19.87% tier flip becomes a smooth ~1.5 instead of a 1-vs-2 cliff.

---

## 9. Engine v3 requirements (for the implementer)

Rewrite `engine.py` as v3 (keep v2 runnable for the archive). Must-fix list:

1. Terminal FCFF normalisation: WC at terminal growth, capex faded to maintenance (§4.1).
2. Reverse-DCF solver: monotonicity guard, sane bounds, dual restatement when unsolvable (§4.3).
3. Negative/degenerate DCF ⇒ D1 = 0 + flag; never 2.
4. D3 middle band (implied ≤ guidance×0.7 ⇒ 1); 0 only when above or unsolvable.
5. D1 one-band: 10–20% below or within ±10% ⇒ 1.
6. Forensic check 3: test **both** limbs.
7. Check 9: pledge materiality floor at 0.5% of shares outstanding.
8. `terminal_g` default 4%, hard cap 4%.
9. WACC from capital structure inputs (`debt_wt` or D/E + spread); no all-equity default.
10. **Dimension totals validated against test sums** — refuse to render on mismatch (kills the v2 arithmetic errors).
11. Tier logic requires a defensible trigger for INVEST AT TRIGGER (V-8).
12. Two-rate plumbing: every r_val use vs r_hurdle use explicit; P computed at trigger **and** at price.
13. Bear weight from a `bear_triggers[]` list (25% + 5pp each, cap 45%); schema example 35% removed.
14. Interpolation helper for §8, applied to all numeric thresholds.
15. B = 10 × pass rate over verified; `[unverified]` checks excluded with follow-up list.
16. C5 lite (4Q) vs full (8Q) mode flag; F5 excludable with F rescale.
17. New inputs: `pit_net_mcap_pct`, quarterly trajectory fields, `beta_source`, `bear_triggers[]`, `debt_wt`, `f5_skipped`.
18. Unit tests: terminal-FCFF consistency, solver monotonicity, dimension-sum validation, tier/trigger logic, interpolation boundaries.

---

## 10. Input schema changes (delta vs v2)

Added: `valuation { r_val, beta, beta_source, debt_wt }`, `hurdle_rate` (default 0.15), `c5_mode` ("lite" | "full"), `f5_skipped` (bool), `pit { net_buy_mcap_pct }`, `quarterly { rev_trend, margin_trend, cfo_trend }`, `bear_triggers[]`, `check_verification {}` per forensic check ("pass" | "fail" | "unverified"). Changed: `terminal_g` default 4.0; `pledge` gains `pledge_pct_shares`; check 3 gains the receivables-growth limb. Removed: the 35% bear-weight example.

---

## 11. USA pathway

Same v3 architecture. USA macro block: Rf 4.96% (UST 10-yr), valuation = **4.96% + β × 4.0%** (≈ 8.96% at β = 1), hurdle 15% (same personal bar, applied in USD — flagged for your review), terminal g cap stays 4%, tax rules unchanged. USA-cal tag becomes v3.0.

---

## 12. Historical calibration protocol (BLOCKING — v3 judges nothing live until this passes)

1. **Set:** 25 names — 10 known Indian multi-baggers, 10 mediocrities, 5 blow-ups/frauds, vintages 2015–2021.
2. **Method:** score each at its price **3 and 5 years before** the outcome was known, using only data available at that date. v3 engine + the then-current inputs, honestly reconstructed.
3. **Bar:** v3 reaches INVEST AT TRIGGER or better on **≥ 40% of the eventual winners** at some point in the window, while **PASSing ≥ 80% of the blow-ups**.
4. **On miss:** adjust thresholds **once**, re-run. If it still rejects nearly everything, the thresholds — not the candidates — are wrong; loosen further. If it passes junk, tighten.
5. Bablu nominates names for the set (his past winners/losers are ideal). The implementer proposes the rest.

---

## 13. Migration from v2

- The 52 existing reviews stay archived as v2 records. No mass re-scoring.
- All new reviews run v3. League Table rows carry the version tag; v2 and v3 scores are never blended or ranked together.
- The backbone v2 doc and v2 engine remain readable in the project for audit trail.

---

*End of v3 spec. Build order for the implementer: engine v3 (§9) → input schema (§10) → calibration set scoring (§12) → report calibration vs the bar → adjust once if needed → go live.*
