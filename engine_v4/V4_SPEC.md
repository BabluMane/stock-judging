# v4 Frozen Spec — stock-judging mega-rebuild (Phase A)
Date: 2026-09-30. Synthesized by coordinator from four Phase-A workers:
anchor (W1_anchor.md), distress screen (W2_distress.md), event lane
(W3_event_lane.md), OOS plan (W4_oos_plan.md). Builds on
ARCHITECTURE_REVIEW.md and arch_review/W1–W4 without re-deriving them.

Nothing here describes any company as investable. "Fill" means a mechanical
trigger event in the validation runner only. Live bar unchanged. Any change
to a number, band, or definition in this document = a new pre-registration
version.

## §0 — Frozen premises (not re-argued)

- v3 (v3.7→v3.11) failed its live bar 3 of 4 OOS runs (v3.8, v3.9, v3.11 FAIL;
  v3.10 fragile technical PASS). The bar was never the problem; the mechanisms
  were (ARCHITECTURE_REVIEW §1).
- Bablu 2026-09-30 override: **no kill option** — if a v4-family run fails,
  diagnose and iterate with a FRESH pre-registered design + FRESH set. The
  override removes the review's one-shot-kill commitment; it does NOT license
  patch loops (see §9).
- Defaults: inverse-DCF implied-growth hurdle as entry anchor; free-data-only
  validation; QFV quality conditions NOT re-justified → **dropped entirely**
  (§2.6, §12-A).
- v3 history stays frozen: engine/, cross_engine/, specs/, validation/v3_*/
  are read-only for the v4 build. engine_v4/ and validation/v4_oos/ are the
  only writable trees.

## §1 — The live bar (unchanged + the (a′) exercise condition)

- Leg (a): **0 blow-up fills (hard).**
- Leg (b): **≥3 distinct winner names with fills.**
- Leg (c): to-T aggregate clearly positive.
- Leg (d): 24m aggregate ≥0.8×.
- **Leg (a′) exercise condition:** the distress screen is decisional on **≥3**
  of the 5 certified decisional-test-set name-dates (§8.2). **Leg (a) PASS
  requires (a′).** An unexercised 0 is UNTESTED, not PASS (learned from v3.11).

## §2 — Entry anchor: inverse-DCF implied-growth hurdle (frozen)

Replaces the killed DCF level comparison. Price becomes an input; the
decision compares two growth rates computed under ONE frozen structure, so
structural mis-specification cancels instead of vetoing (expectations-investing
inversion; Mauboussin & Rappaport).

### §2.1 Structure — 2-stage fade FCFF, growth is the solved parameter

For growth parameter g, with r_0 = rev0 (trailing-FY sales, ₹cr):

- Years 1–10: g_t = g.
- Years 11–19: g_t = g + (TG − g)·(t−10)/10 (linear fade to terminal).
- Year 20+: g_t = TG (4%).
- r_t = r_{t−1}·(1+g_t).
- FCFF_t = r_t·(m−dp)·(1−TAX) − (r_t − r_{t−1})·wc, where m = trailing-5FY
  average OPM (**flat across the whole forecast — no margin fade**; the v3
  fade taxed margin expanders and is killed per the review), dp =
  trailing-5FY avg depreciation/sales, capex_pct = dp (capex≈depreciation,
  carried simplification; the +r·dp −r·cp terms cancel — write the
  cancellation out so it is auditable, not assumed), wc = 5% of incremental
  revenue (carried).
- w = Rf + β·ERP (Rf 6.95%, ERP 4.0%, sector β frozen pre-run — carried);
  TAX = 25.17% (carried).
- EV(g) = Σ_{t=1}^{20} FCFF_t/(1+w)^t + TV/(1+w)^20, TV = FCFF_21/(w−TG)
  with FCFF_21 computed at g_21 = TG.
- V(g) = (EV(g) + netcash)/shares; netcash = investments − borrowings;
  shares = mcap ÷ price at scoring (carried basis convention).
- Degenerate guard carried: w ≤ TG+0.5pp → not valued.

### §2.2 Sustainable growth (frozen family)

g_sus = min(ROE_avg3 × (1 − payout), 0.15).

- ROE_avg3 = mean of 3 annual PAT ÷ (Equity Capital + Reserves)
  (v3.10 C1 per-year-ratio construction, carried).
- payout = Dividend Payout % ÷ 100, **unclipped** (v3.10 C2 literalism,
  carried — >100% payout ⇒ negative factor).
- **No floor** on raw g_sus (v3.10 C3, carried — negative allowed).
- Cap **15%**: carried accidental-but-frozen (explicitly non-fitted round
  choice). Structural footnote, not a fit: decade-plus 15%+ growth is
  empirically exceptional (Mauboussin base-rate/fade literature). FLAGGED:
  the cap binds on nearly every name — it is the highest-leverage accidental
  constant in the design; the pre-reg carries a named cap-sensitivity as
  reporting-only.

### §2.3 Hurdle and fill tiers (exact trigger definitions)

Sign-preserving hurdle growth: **g_h(k) = g_sus − (1−k)·|g_sus|**
(= k·g_sus whenever g_sus ≥ 0; a naive k·g_sus would *loosen* the hurdle for
shrinking businesses — resolved).

- **Tier G1** (ACC analog): trigger P_G1 = V(g_h(0.875)), fixed at scoring.
- **Tier G2** (INV analog): trigger P_G2 = V(g_h(0.70)), fixed at scoring.
- **Fill**: first weekly close ≤ trigger inside (d0, d0+24m]; one leg per
  tier per name-date (fill mechanics carried from v3).
- k = 0.875 / 0.70 are **structural-role, accidental-value**: margin of
  safety belongs on the growth rate (the highest-variance value driver —
  Mauboussin & Rappaport; Damodaran value-of-growth). The round 12.5%/30%
  values are carried from v3's ACC/INV tiers (explicitly non-empirical, never
  backtested). **Never fitted on any OOS set** — the stress test shows
  k=1.00 admits Titan 2016 / Page 2015 / Britannia 2017 / Tiindia 2020; k is
  the whole game for premium names, which is why it stays frozen.
- **Entry rule (frozen primary): the trigger-price comparison.** The
  diagnostic g_implied solves V(g) = P_d0 by bisection on [−0.50, w−0.01]
  and is reported as ">w−1pp" when V(w−0.01) < P_d0 or at the −50% floor when
  V(−0.50) > P_d0. The diagnostic is **reporting only**. The price
  comparison *is* the inequality g_implied ≤ g_h(k) wherever V is monotone
  in g, and remains exact where the solver hits its convergence bound
  (making the bound decisional would veto names whose hurdle status is
  exactly computable). V(0.875·g) ≠ 0.875·V(g) — value is convex in growth;
  triggers are recomputed through the structure, never scaled from a level.

### §2.4 Financial variant (frozen)

V_fin(g) = [Book_0 + Σ_{t=1}^{20} (ROE_t − w)·Book_{t−1}/(1+w)^t +
Book_20/(1+w)^20] / shares; ROE_t = ROE_avg3 + (w − ROE_avg3)·t/20;
Book_t = Book_{t−1}·(1+g); Book_0 = Equity Capital + Reserves at scoring FY.
Same hurdle/trigger mechanics as §2.3. Judgmental-but-frozen; flagged for
pre-reg review (§12-R).

### §2.5 Stress-test verdict (inherited, not re-run)

Retrospective stress test on the 34 computable winner name-dates (v3.8–v3.11):
**8 distinct winner names with fills** (Divi's, Polycab, Asian Paints, HAL,
BEL, Coforge, TVS Motor, KEI); 7 ex-GEV-veto (KEI vetoed under v3's GEV;
v4 event lane re-adjudicates). Per set: 2 / 1 / 3 / 2. The anchor expands
coverage into the P/FV 1.1–2.24× band (v3's ceiling was 1.11×). Known failure
modes: premium franchises at P/FV_v3 ≳ 2.5× (Titan, Page, DMart, Jubilant,
Pidilite, Dixon 2021) still excluded — the anchor holds
*reasonable-implied-growth*, not compounders at any price (§12-P); COVID-trough
dependence persists; knife-edges at trigger boundaries are disclosed, not
smoothed.

### §2.6 QFV verdict

The QFV 1.00× entry tier is **killed** (zero compounder entries in two OOS
runs). The four AND-gated quality conditions (ROIC 15%/10%, OCF/PAT 0.85,
D/E 0.5, mcap ₹5,000cr) are **not re-justified as a v4 gate and are dropped
entirely** (§12-A). Quality discipline is carried by the Piotroski strength
veto (D4) and the anchor's sustainable-growth input — both with their own
evidence bases, neither carried frozen from QFV.

## §3 — Distress screen (the blow-up-leg mechanism; replaces event-only GEV)

State-based, evaluated ONCE at the scoring date d0, BEFORE any entry.
Applies symmetrically to all name-dates (winner, mediocre, blow-up). A veto
blocks entry for the entire (d0, d0+24m] window. No re-evaluation at fill,
no cooling-off re-admission (v3's cooling-off never released a name in four
runs — removed, not carried).

- **Input vintage (PIT):** all filing inputs from the latest FY whose results
  were published ≥63 days before d0 (standing 63d PIT lag). Price inputs use
  the d0 close on the continuously-adjusted series (same corporate-action
  basis as everything else).
- **Class split:** each name-date gets exactly ONE of {Z''+Piotroski} or
  {CAMEL}. Financial-variant class = screener.in Sector ∈ {Banks, Finance}
  (covers banks, NBFCs, HFCs). All other sectors = non-financial.
- **UNCOMPUTABLE-DATA:** a required input missing (not zero — missing) ⇒
  the name-date is vetoed and reported as VETOED-DATA (data defect, never a
  fraud judgment). Missing data never silently passes.

### D1 — Promoter pledge level gate
Pledged % = % of *promoter shareholding* pledged, screener.in → Shareholding
Pattern → most recent reported quarter ≤ d0. Frozen normalization: if a
source reports pledged as % of total equity, convert: pledged_of_promoter =
pledged_of_equity / promoter_holding_pct. **Veto if ≥ 50%.** Justification:
no published cutoff exists in the replication literature (Kalia 2024;
Chauhan-Mishra-Spahr 2021; Mantri et al 2025 model pledge continuously) —
50% is a round structural bar at the invocation-cascade level (a margin-call
invocation mechanically transfers control-sized blocks, the crash-risk
mechanism the literature identifies). Not fitted. Raw pledged % is stored as
a reporting field for every name-date regardless of veto.

### D2 — First-time-pledge transition trigger
pledged % = 0.0 for **all 8 trailing reported quarters** (from the
scoring-quarter print backward), AND scoring-quarter pledged % > 0 ⇒
FIRST-TIME-PLEDGE ⇒ veto. If fewer than 8 quarters of shareholding data
exist: require all available quarters at 0.0 with a **minimum of 4**; if <4
quarters exist, the transition trigger is N/A (D1 still applies). A name
listed already pledging (>0 at first available quarter) is NOT first-time —
D1 only. Justification: NSE-NYU White Paper #3 (Asija–Marisetty–Rangan 2014):
pledging *reduces* accrual earnings-management on average (lender
monitoring), but **first-time pledgers spike discretionary accruals
(+1.03% vs −0.62% for continuing pledgers)**. The EM-risk signal is the
transition, not the level. Source: same as D1; cross-check BSE/NSE
encumbrance disclosures under SEBI Takeover Reg 31.

### D3 — Altman Z'' distress gate (non-financial names only)
Frozen formula (Altman–Hartzell–Peck 1995, **no +3.25 EMS constant**):
Z'' = 6.56·X1 + 3.26·X2 + 6.72·X3 + 1.05·X4, where X1 = Working Capital /
Total Assets (WC = Current Assets − Current Liabilities); X2 = Reserves &
Surplus / Total Assets (free-data proxy for Retained Earnings — disclosed
deviation; subtract revaluation reserve only if separately disclosed);
X3 = EBIT / Total Assets (EBIT = Profit Before Tax + Interest +
Depreciation); X4 = Book Equity / Total Liabilities (Book Equity = Share
Capital + Reserves; Total Liabilities = Total Assets − Book Equity). All
fields screener.in **except the Current Assets / Current Liabilities split for X1, which comes from the AR PDF (BSE announcements / company IR, free) per D4's precedent for F_ΔLIQUID ("the 1-of-9 not on screener"); AR unretrievable ⇒ the missing-field rule below applies (UNCOMPUTABLE-DATA veto)**. **Veto if Z'' < 1.1** (Altman's published distress
boundary). The 1.1–2.6 grey zone PASSES (veto on clear distress only).
Justification: literature cutoff, never fitted on our sets. The +3.25
emerging-market constant is deliberately EXCLUDED (re-scales the score and
breaks the boundary — a second judgment call). One version for all
non-financials; X5 (Sales/TA) excluded (penalizes asset-heavy industrials,
distorts asset-light services; avoids a per-name sector-classification
judgment call). Ohlson O considered and REJECTED: its SIZE term needs a GNP
price-level deflator unavailable on free data; any proxy re-scales the
published coefficients and silently breaks the literature cutoff. Fallbacks:
Book Equity ≤ 0 ⇒ automatic distress veto (negative book equity is itself
the distress state); any missing X-component field ⇒ UNCOMPUTABLE-DATA veto.
Evidence-tier caveat: Z is published-once for India (Lakra et al 2025);
carried as the best available literature gate with its tier disclosed, not
as a proven India-distress classifier.

### D4 — Piotroski F financial-strength veto (non-financial names only)
The 9 criteria (Piotroski 2000, each 1/0), all on the scoring FY vs prior FY
(both ≥63d-published): (1) F_ROA: Net Profit / beginning Total Assets > 0;
(2) F_CFO: Cash from Operating Activity > 0; (3) F_ΔROA: ROA_t > ROA_{t−1};
(4) F_ACCRUAL: CFO_t > Net Profit_t (same TA denominator); (5) F_ΔLEVER:
(Borrowings / avg Total Assets) decreased YoY (free-data proxy: total
Borrowings for LT debt — disclosed deviation); (6) F_ΔLIQUID: Current Ratio
increased YoY — **the 1-of-9 not on screener**: CA/CL split from the AR (BSE
announcements / company IR, free); **pre-registered fallback: AR not
retrievable ⇒ score 0 (fail-closed), logged**; (7) F_EQ: no common equity
issued (Equity Share Capital increase YoY AND not solely bonus/split ⇒ 0;
check screener corporate actions); (8) F_ΔMARGIN: Gross margin increased YoY
((Sales − Material Cost)/Sales; if Material Cost row absent, compute from
"Raw Material Cost/Sales %" × Sales; if neither exists ⇒ score 0,
fail-closed, logged); (9) F_ΔTURN: Sales / avg Total Assets increased YoY.
**Veto if F ≤ 2** (Piotroski's own 0–2 "loser" bucket boundary — literature
cutoff, not fitted). Evidence: Singh & Kaur 2015 (+1 F-pt → +4.93% 1-yr
market-adjusted return); Tripathy & Pani 2017; Walkshäusl 2020 (35-market
replication, EM premium ~12%). Used as a *financial-strength veto*, never as
a fraud input. Δ-terms with a missing prior FY score 0 (fail-closed), logged;
a missing direct field (no cash-flow table at all) ⇒ UNCOMPUTABLE-DATA veto.
A name with F ≤ 2 cannot enter as a winner either — the winner-side cost is
disclosed and symmetric.

### D5 — Price-action crash veto
ONE frozen definition: at scoring, H52 = trailing 52-week high of adjusted
closes, P0 = d0 close. **Crash veto if (H52 − P0)/H52 ≥ 60%.** Justification:
60% is a round structural bar set *above* index-level crash magnitudes
(2008/2020 index drawdowns ≈ 38–40%) — it fires on firm-specific collapse,
not market troughs. Distance-below-200d-MA rejected: at any defensible
margin it vetoes COVID-trough winners. H52 is directly readable from
screener.in's 52-week High/Low header — free-data computable without a price
download. **Falsifiable line (checkable on the OOS run): the COVID-trough
winner cohort must not be vetoed as a class — TVS Motor 2020 must remain
eligible**, and the run must report the full crash-veto hit-list (name-dates
vetoed, both legs) so the claim is auditable. Firm-specific collapses of the
Srei type (≈87% drawdown) trip it. Edge: <52 weeks of history ⇒ use the
maximum available; <26 weeks ⇒ UNCOMPUTABLE-DATA veto.

### D6 — CAMEL-style composite (financial-variant names ONLY — replaces the killed usability exemption; no free pass)
Financial names are exempt from D3/D4 (undefined for banks/NBFCs) and get
this instead. Five components, each scored **0–2** on pre-registered bands,
total 0–10. All fields from screener.in bank/NBFC ratios pages.
- **C — Capital (CAR %):** ≥15 → 2; 11.5–15 → 1; <11.5 → 0 (RBI NBFC floor
  15%; bank PCA trigger ≈11.5% — regulatory bars).
- **A — Asset quality (Gross NPA %):** ≤3 → 2; 3–6 → 1; >6 → 0 (round
  structural bands at half the RBI PCA severe threshold).
- **M — Management efficiency (Cost-to-Income %):** ≤50 → 2; 50–65 → 1;
  >65 → 0 (quantitative proxy for qualitative M — disclosed substitution).
- **E — Earnings (ROA %):** ≥1.0 → 2; 0–1.0 → 1; <0 → 0 (1% ROA =
  canonical bank-profitability bar).
- **L — Liquidity:** banks → CASA %: ≥40 → 2; 25–40 → 1; <25 → 0 (round
  structural bands). NBFCs/HFCs → Leverage = Total Outside Liabilities /
  Owned Funds: ≤7 → 2; 7–10 → 1; >10 → 0 (RBI scale-based framework caps
  upper-layer NBFC leverage at 7 — regulatory bar).
- **Veto if total ≤ 4.** **Hard floors (regulatory, override the total):**
  GNPA > 12% ⇒ veto; CAR < 9% ⇒ veto (RBI PCA severe/capital triggers).
  Justification: the 4/10 line and intra-component bands are round structural
  choices (worst band on a majority of components = the regulatory-distress
  profile); hard floors are RBI PCA thresholds, not fitted values; equal 0–2
  weighting is a disclosed structural choice, not an optimized one.
- Any component field missing ⇒ UNCOMPUTABLE-DATA veto. D1/D2 (pledge) and
  D5 (crash) still apply to financial names.

### D7 — Distress-screen internal precedence (reporting only)
Evaluation order at scoring: D1 → D2 → D3/D6 → D4 → D5. The first tripped
rule owns the name-date's attribution (VETOED-DISTRESS:<rule>); every tripped
rule is logged. All are hard vetoes independently.

## §4 — Usability gate narrowed to data quality (fraud-screen role KILLED)

Kept as a pure forensics-integrity / input-quality gate. It no longer decides
the blow-up leg by design — the distress screen (§3) owns blow-up stops, and
the audit order (§7) makes that attribution explicit.

- **U1 — Basis assertion (carried from V3_7 §4.1, unchanged):** name the
  corporate-action basis explicitly. Transform ONLY the side not on the named
  basis; audited EPS restated only for splits/bonuses; verify the
  audited÷sourced ratio is constant across years and document any residual
  convention factor (e.g. ESOP drift) instead of failing on it. **Never choose
  whichever basis passes.**
- **U2 — Non-positive sourced FY EPS ⇒ excluded (data-defect flag):** the
  sourced (basis-corrected) FY EPS ≤ 0 ⇒ VETOED-DATA — a sign flip cannot be
  a basis residual. A data-defect flag, explicitly NOT a fraud judgment; the
  distress judgment lives in §3.
- **U3 — Check (a′) at the results week (carried from V3_7 §4.2 + v3.8
  publication-dating):** on the **publication-dated (unlagged)** screener EPS
  series: compare the screener-implied TTM EPS in the results week — **median
  over results-week..+21d** — against audited FY EPS. FY-TTM identification:
  the first publication in [Mar 31, Aug 31] applying the **>10%-jump skip
  rule** (a Mar-31 point that jumps >10% to the next point is stale/pre-results
  and skipped; a small-jump Mar-31 point is the back-dated FY value). Identify
  the results week from publication events (or the unlagged series), never
  from the 63d-lagged series' calendar position. **Tolerance ±15%** on
  |TTM − audited| / audited (carried from v3.7 — round, load-bearing for
  input integrity). Fail ⇒ VETOED-DATA. Check order within usability:
  U1 → U2 → U3.
- **U4 — Check (b) KILLED.** "No implied-EPS step >8% outside ±30d of a
  results window" never fired in four validations. Dead rule; removed, not
  carried.
- **U5 — Financial-variant exemption KILLED.** Financial names face U1–U3
  on the same mechanics as everyone else; the exemption Srei walked through
  is gone, replaced by the CAMEL screen (D6). If screener publishes no EPS
  series for a financial name, U3 is UNCOMPUTABLE-DATA ⇒ VETOED-DATA (missing
  data excludes; it does not exempt).

## §5 — Event lane (severity-graded governance events; secondary lane + in-window exit)

KILLED as the blow-up-leg entry mechanism (reactive by construction,
decisional ~0 across two confirmations). KEPT as a severity-graded secondary
lane: entry veto on SEVERE/MODERATE events + in-window exit on SEVERE. The
lane contains losses; it does not predict them.

### §5.1 Taxonomy (closed list, pre-registered)

Seven types. A qualifying event is a **dated public record** matching the
exact condition. Closed list = a record matching no type is not an event,
however alarming. Explicit non-events (never qualifying, never veto):
earnings restatements; dividend cuts/omissions as distress signals (perverse
in India — Agarwal et al 2024); promoter share *purchases* as a positive;
auditor rotation (scheduled); media rumor with no dated record (WATCH-logged
only); any event whose only evidence is inference from press juxtaposition.

Source hierarchy (per record): (1) BSE/NSE exchange filing; (2)
regulator/agency document (SEBI order PDF, rating rationale PDF, court
filing); (3) national business press. Any record resting on (3) alone is
tagged WEAK-SOURCE. Seeded events count as qualifying; seeded-event
correction: correct with source + date, log separately, never silently swap.

| # | Type | Exact qualifying condition (the dated record that counts) |
|---|---|---|
| T1 | Regulatory probe/action | Dated record of a SEBI / ED / SFIO / CBI probe, show-cause notice, adjudication or enforcement order, or interim direction **naming the company, its promoters, or its KMPs**. A press report that an agency "may" act, with no named instrument, does not qualify. |
| T2 | Auditor events | (a) Dated auditor resignation (resignation letter filed with the exchange / SAST); (b) qualified opinion, adverse opinion, or disclaimer in the audited FY report. Scheduled auditor rotation is explicitly not an event. A resignation citing disagreement, suspected fraud, or unpaid fees, or a CARO paragraph flagging suspected fraud, is the SEVERE sub-case. |
| T3 | Promoter conduct | (a) Dated off-market transfer or gift of promoter shares (SAST Reg 29/30 disclosure); (b) dated lender **invocation of pledged shares** (pledge-invocation disclosure under SAST Reg 31). Plain creation/pledge of encumbrance without invocation is not an event (pledge level is the distress screen's input, not the lane's). |
| T4 | Withdrawn capital actions | Dated company/board announcement **withdrawing** a previously announced buyback, dividend, or fundraise. A never-announced action, or routine non-declaration of dividend, is not an event. |
| T5 | Criminal/legal | Arrest, charge-sheet / named FIR, or conviction of a promoter or KMP (dated agency/court record or exchange disclosure). MCA-ordered investigation or inspection (no charge-sheet) is the MODERATE sub-case. |
| T6 | Associate contagion | Regulatory action against a **named** associate or group company where the link is documented in the company's own filings or in the regulatory order itself — never inferred from press juxtaposition. Severity = the severity of the underlying action, downgraded one grade (SEVERE→MODERATE) unless the order names the company directly. Explicitly: an underlying MODERATE action, downgraded one grade, is **WATCH** (log only, no veto); an underlying WATCH stays WATCH. |
| T7 | Rating downgrade to D | A SEBI-registered agency downgrades the company's long-term instruments to **'D' with default/payment-delay rationale** (dated rating rationale PDF). Folds the v3.11 type 7 into this lane (standalone veto killed per the kill list): it is the most objective SEVERE trigger — a D certifies a realized payment default (Dichev & Piotroski 2001), not a judgment call. Legal stays barring agencies from recognizing default (cf. NCLT 2020-12-30 in the Srei case) do not change the rule: **the event date is the agency's publication date** (§12-N). |

### §5.2 Severity grades (Cogent 2022: fraud/cheating/default >> disclosure lapses)

- **SEVERE**: T1 order finding fraud, cheating, or misstatement, or imposing
  a trading/registrant ban · T2 adverse opinion or disclaimer; resignation
  citing disagreement/fraud/CARO fraud flag; T2 auditor resignation citing
  unpaid fees → SEVERE (per §5.1) · T3 pledge invocation · T5
  arrest / charge-sheet / conviction · T7 downgrade to D.
- **MODERATE**: T1 probe / SCN opened with no adverse finding yet; T1
  regulatory order that is neither a fraud/cheating/misstatement finding nor a
  trading/registrant ban · T2
  qualified opinion (not adverse/disclaimer); resignation with no stated
  reasons; resignation citing reasons other than disagreement, suspected
  fraud or unpaid fees, with no CARO fraud flag · T5 named FIR on its own (no
  arrest, charge-sheet or conviction yet) · T3 off-market transfers/gifts · T4 withdrawn
  buyback/dividend/fundraise · T5 MCA-ordered investigation/inspection · T6
  contagion (SEVERE underlying, downgraded). T7 sub-investment-grade cut below D (e.g. BB and
  lower, not D) is MODERATE.
- **WATCH**: disclosure lapses with no order, RBI special-audit /
  forensic-auditor appointment with no adverse conclusion, SEBI settlement
  with no admission — logged with date and source, **no veto power,
  exit-monitor context only**.
- Grade assignment is per-event, from the record's own words, at log time;
  the grade is frozen then; later upgrades/downgrades are logged as new
  dated records, never edits.
- **Source–severity rule (frozen):** a SEVERE grade requires at least one
  exchange-filing or agency-document source. A record resting on press alone
  (WEAK-SOURCE) caps at MODERATE — it may veto entry but may never force a
  position exit (§12-L).

Which grades act: **SEVERE + MODERATE ⇒ entry veto** (§5.3).
**SEVERE only ⇒ in-window exit** (§5.4). WATCH ⇒ log only.

### §5.3 Entry-veto mechanics

- **Event window (kept: trailing 12 months).** An event vetoes entry if its
  event-date lies in the trailing 12 months before the evaluation date.
  Evaluation dates: the scoring date d0, and each fill date. This keeps the
  v3 locked rule unchanged (continuity; lengthening it would be an
  unjustified accidental tweak). The new exit lane (§5.4) and the operable
  cooling-off provide the loss containment the stricter C8 deviation was
  reaching for — **the C8 harness deviation (scoring veto blocks the whole
  24m window) is retired**: §2.2's literal text (event-local windows) is the
  load-bearing spec; C8 made the §5.3 cooling-off release unreachable, and
  the protective intent is now carried honestly by the exit scan.
- **Cooling-off (rewritten — release prong made operable).** The block from
  an event persists until **12 months after the event date AND one audited
  annual earnings print published after the event**, whichever is later. A
  new qualifying event on the same name resets the clock from the new event
  date. Exact mechanical definitions: "one audited annual print after the
  event" = one FY audited annual report / annual results whose (i) results
  publication date is strictly after the event date AND (ii) FY-end is
  strictly after the event date (meeting only (i) does not count). "No
  publication on record" = after a documented search of **two of**:
  (a) screener.in results calendar, (b) BSE/NSE corporate announcements,
  (c) the company's published AR PDFs, zero post-event audited prints are
  locatable — the operator records the search (sources named, search date,
  zero hits). Result: the release prong is **not satisfied** — the block
  persists, logged as WEAK-SOURCE search. Deliberately release-skeptical
  (§12-O). Vs the distress screen: parallel, union blocks, trace records
  both (§7). Vs the anchor: the lane's entry veto applies before anchor
  entry; once a leg is filled, the anchor no longer governs the holding —
  only the exit lane (§5.4) and delisting rules do.

### §5.4 In-window exit (the lane's new core)

- **Evaluation cadence.** For **every filled leg**, the harness must run an
  exit scan and log it — no scan may be absent from the result JSON. The
  scan: weekly price dates w1 < w2 < … from the week **after the fill date**
  through d0+24m. The leg exits at the **first** wi such that there exists a
  **SEVERE** event with event-date ∈ (fill_date, wi]. MODERATE and WATCH
  events never trigger exit (§12-M). The result JSON must carry, per leg, a
  non-optional field: `exit_scan: {fired: bool, exit_date: <weekly
  date|null>, exit_price: <₹|null>, triggering_event: <type+date|null>}`. A
  leg with fired: false must still log triggering_event: null and a one-line
  "no SEVERE event in (fill, d0+24m]" — so "never fired" is an observable,
  auditable fact rather than an absence.
- **Slippage (pre-registered, uniform):** exit executes at the **next weekly
  close ≥ the triggering event's evaluation week**, times **0.99** (1.0%
  slippage provision: forced exit in distressed names). Uniform; no per-name
  adjustment; pre-registered, not fitted (§12-K).
- **Delisting / suspension handling:** if the scheduled exit week has **no
  weekly close** (suspended, delisted, series truncated): (1) use the **last
  available weekly close** in the frozen price series as the exit price (the
  last-print rule, same convention as the 24m endpoint); (2) if that last
  print **predates the triggering event date by more than 20 trading days**,
  the exit is marked **UNEXECUTED**: the position could not be exited on
  market terms; the leg's return is computed at the 24m endpoint value (last
  print), flagged `exit_unexecuted` in the JSON; no mark-to-model recovery
  permitted; (3) if the name is relisted inside the window after an
  UNEXECUTED mark, the exit executes at the next weekly close after
  relisting — UNEXECUTED is provisional until d0+24m, final at the endpoint.
- **Return computation and the bar:** a leg exited in-window has return
  (exit_price × 0.99 − fill_price) / fill_price, used identically in the to-T
  and 24m aggregates (leg-weighted means, price return only — carried).
  **The 0-blow-ups bar leg is scored at entry.** An in-window exit does NOT
  un-fail a blow-up fill: the fill happened, the bar stays hard and
  unchanged. The exit's job is loss containment in the to-T / 24m aggregates
  and the blow-up-leg structural analysis — exactly what an event screen can
  honestly promise (§12-M).

### §5.5 Decisionality guarantee (pre-registered, falsifiable)

- The pre-reg must name, with dates: (1) **entry-veto targets:** ≥3
  name-dates carrying a SEVERE or MODERATE event in [d0−12m, d0], each with a
  pre-reg line stating the expected pass-through of the other gates
  (usability pass / distress-screen pass / anchor fill-plausible); (2)
  **in-window exit targets:** ≥2 expected held legs where a SEVERE event is
  named with an event date inside (fill, d0+24m].
- The confirmation report must tabulate from the gate-trace table: (a)
  name-dates where the event lane was the *deciding* stop and all other gates
  passed (clean entry-veto decisional); (b) legs where the exit scan fired
  on a SEVERE event (clean exit decisional); (c) name-dates/legs where the
  lane stopped/held a position the other gates alone would have filled/held
  (shadow decisional). The lane is "genuinely exercised" iff (a)+(b)+(c) ≥ 1
  **with at least one in (a) or (b)** — a shadow-only lane is not exercised.
  If zero in (a) and (b), the confirmation cannot claim the lane was tested
  (the genuineness check governs what the run may claim, not whether the bar
  passed).

### §5.6 Carry-overs and explicit kills

- Carried over frozen: closed taxonomy; absolute entry veto on qualifying
  grades (now grade-scoped); seeded events qualify; seeded-event correction
  protocol; source hierarchy + WEAK-SOURCE marking; §5 honest-residual-risk
  clause — fraud clean at scoring passes every rule; the hard 0-blow-ups bar
  prices it in.
- Killed: C8 (scoring veto blocks whole 24m — superseded); the old GEV
  fill-date re-evaluation as an *entry* block (its job is done by the literal
  §2.2 fill-date window + the exit scan); type 7 as a standalone codified veto
  (folded into T7/SEVERE per the kill list); GEV as the blow-up-leg entry
  mechanism (distress screen owns that now).

## §6 — Fill mechanics + aggregation

- Fill: first weekly close ≤ trigger inside (d0, d0+24m]; one leg per tier
  per name-date (carried, W4 #21 — the fill is the experiment's unit of
  observation). Tier G1 trigger = P_G1 = V(g_h(0.875)); Tier G2 trigger =
  P_G2 = V(g_h(0.70)); both fixed at scoring. Each tier is a leg in the
  aggregation (same as v3.10/v3.11 ACC/INV).
- In-window exits feed the aggregates as realized exits: a leg's return is
  entry→exit (exit_price × 0.99 per §5.4), or entry→to-T / entry→24m if never
  exited. An exit does NOT delete the fill: a blow-up name that fills and
  later exits still counts as a blow-up FILL for leg (a) (§5.4).
- **Aggregation: leg-weighted means, price return only** (carried — W4: this
  is accidental-but-continuity-load-bearing; every prior verdict is
  denominated in these aggregates; dividend-adjusting re-baselines all
  comparability).
- 15%-hurdle price reporting is dead and removed (not carried — kill list).

## §7 — Gate-trace table + audit ordering (the FM2 fix)

To stop one gate silently eating another's test set (FM2: usability fired
first, GEV decisional ~0), **all gates are evaluated in parallel on every
name-date** — no gate may early-return before the others are evaluated. Each
gate reports PASS or STOP with its reason; the fill is blocked by the union.

- The confirmation report must carry a per-name-date gate-trace table with
  one column each for: distress screen · usability · event lane · anchor.
- For the *reported* "deciding stop" of an excluded name-date, attribution
  order is frozen as: **distress screen → usability → event lane → anchor**
  (first failing gate in this order is named; all are recorded). This
  resolves the W2/W3 attribution-order conflict: distress first is chosen so
  usability can never again silently own a blow-up stop (W2's rationale);
  the structural fix is parallel evaluation itself (W3's mechanism).
- The bar is re-derived AFTER the veto audit; the audit is one-shot
  (V3_7 §5.4 carried: re-running any gate after seeing which rule admits a
  name is re-fitting under another name).
- **Shadow pass retained** (W4 #44 carried): vetoed name-dates are
  anchor-valued non-decisionally so exclusions cannot hide fills.

## §8 — OOS validation plan (pre-reg design)

### §8.1 Set composition
- **25 name-dates / 13 companies.** 5 winner companies × 2; 5 mediocre × 2;
  3 blow-up companies totaling 5 name-dates (2+2+1). Same shape as v3.10/v3.11.
- Scoring dates: March 31 only; **all ≥ 2019-03-31**; vintage years 2019–2022
  (24m windows close by 2024-03 under free-data-only).
- Per-name eligibility (frozen in the pre-reg doc): category labels
  pre-registered from general public market history — a label that proves
  wrong once PIT data is gathered is a finding to report, never a reason to
  swap a name; one-line thesis per name-date (company, NSE symbol, FY-end);
  max 2 name-dates per company; winners: documented multi-year
  outperformance profile (pre-reg states the realized-outcome criterion);
  mediocrities: documented flat/de-rating profile; blow-ups: dated qualifying
  governance event(s) inside the 24m window, well-documented distress, AND
  the §8.2 decisional pre-conditions. **No name added, removed, or swapped
  after commit, for any reason.**

### §8.2 Decisional test set (the core new machinery)
≥5 blow-up name-dates, each certified pre-run on three mechanical,
scoring-date-computable pre-conditions (input conditions only — the pre-reg
asserts the name-dates are *capable* of deciding, and asserts nothing about
what the screen will do):
1. **Usable (post-v4-usability):** passes the §4 gate as pre-registered
   (check-(a)-family basis discipline; check (b) dead and removed;
   non-positive-EPS = data-defect flag; **no financial-variant exemption** —
   financials carry the CAMEL composite). The usability verdict is recorded
   per name-date in the pre-reg before the run.
2. **Fill-plausible under the anchor:** **P_d0 ≤ 2.0 × P_G1** — the scoring
   price is within 2× of the tier-1 trigger (a ≤50% decline reaches it), both
   computed at scoring from frozen inputs. A round, stated, non-fitted band
   (accidental-but-frozen — §12-C): a fill is mechanically reachable
   in-window, so a non-fill is the screen's doing, not valuation's. Never
   re-tuned on any set.
3. **Pre-flag-risk:** under the §5.1 taxonomy, the first qualifying event
   date E1 satisfies **scoring + 6 months ≤ E1 ≤ scoring + 24 months**
   (scoring precedes the first flag by ≥6 months; the blow-up is observable
   inside the measurement window).
- **Decisional** (post-run): the distress screen is decisional on a name-date
  iff its veto blocked a fill the anchor would otherwise have made (anchor
  trigger met in-window, screen veto active — verified from raw fills + veto
  logs).
- **Exercise condition:** genuine exercise of the distress screen requires
  decisional on **≥3** of the 5 name-dates (= §1 leg (a′)).
- **Void rule:** if the pre-reg set cannot supply 5 name-dates meeting all
  three pre-conditions (certified pre-run), **the run does not proceed — it
  is VOID**, not weakened, not reinterpreted, not "underpowered but counted."
  If the run proceeds and the screen is decisional on <3, the blow-up leg is
  recorded as **UNTESTED** and the run is VOID — an unexercised 0 is not a
  PASS of leg (a). Both cases require a new pre-reg + a new set (fresh
  zero-overlap vs all six prior sets, §8.3).

### §8.3 Zero-overlap rule
The v4 set must be disjoint from ALL FIVE prior sets at BOTH company AND
name-date level (in-sample: 25/50; v3.8–v3.11: 13/25 each). Canonical lists:
validation/v3_10_oos/check_disjoint_v310.py (INSAMPLE, V3_8, V3_9, V3_10)
and validation/v3_11_oos/check_disjoint_v311.py (V3_11) — these scripts, not
any prose list, are the source of truth. Company identity: normalized
company token (the co() extractor convention: name-date token up to the last
underscore); the pre-reg states the identity-mapping rule for
renamed/demerged tickers (name-normalizer discipline — a demerger phantom
riding back in is a silent overlap). Procedure:
validation/v4_oos/check_disjoint_v4.py, committed pre-results, inheriting the
prior lists by import (same pattern v3.11 used): asserts 25 name-dates / 13
companies, all scoring dates ≥ 2019-03-31; prints per-prior company and
name-date overlap (must be empty) plus union overlap; prints DISJOINT: True.
Touches no price/fundamental data — pure name/date membership. **The locked
run may not start unless DISJOINT: True is on record.** Full output pasted
verbatim into the pre-reg doc; the auditor re-runs the script independently.

### §8.4 Pre-reg document structure (exact sections)
validation/v4_oos/OOS_SET_PREREG.md, in this order:
1. **Frozen rules hash.** SHA-256 (or git commit hash) of the spec delta +
   runner + set manifest, committed before any data is touched. The doc names
   the commit; the audit verifies the hash. Mid-run edits are void ab initio.
2. **Set composition** (§8.1) + one-line thesis per name-date + no-swap rule.
3. **Decisional test set** (§8.2): the 5 blow-up name-dates, each with
   usability verdict (scoring-FY computation), fill-plausibility computation
   (P_d0 ≤ 2.0 × P_G1), event tape with first-qualifying-event date E1 and
   pre-flag-risk certification. Restates the ≥3 exercise-count target and the
   void rule verbatim.
4. **Overlap proof:** check_disjoint_v4.py output pasted verbatim
   (per-prior overlaps empty, union empty, DISJOINT: True). Script committed
   under validation/v4_oos/.
5. **Data/runner/log commit order:** data + runner + logs committed BEFORE
   results; result JSON last; frozen dirs untouched (additions only under
   validation/v4_oos/).
6. **Audit checklist:** one locked run; no mid-run edits (any observation
   becomes a next-iteration proposal); bar recomputed independently from raw
   JSON; decisional count recomputed from raw fills + veto logs; shadow pass
   present for vetoed names; frozen-dir diff empty.
7. **Firewall + void/FAIL triggers, pre-stated:** (i) fewer than 5 name-dates
   certifiable on the three §8.2 pre-conditions → VOID before run; (ii) any
   blow-up fill → leg (a) FAIL; (iii) decisional count <3 → UNTESTED → VOID;
   (iv) any mid-run rule change → VOID.
8. **Dead-design non-resurrection attestation:** enumerates the §10 kill list
   and states, for each listed component, whether the design touches it and —
   if so — why the touch is a new mechanism with its own pre-registered
   rationale, not a resurrection.

## §9 — Iteration rule (the anti-loop machinery)

Bablu 2026-09-30 override: **no kill option.** Iteration continues, but as
machinery, not as license:

Fail → diagnose → **FRESH pre-registered design** → **FRESH set** (zero
overlap with all SIX prior sets: in-sample + v3.8/9/10/11 + v4, at company AND
name-date level) → **ONE locked run.**

- **Firewall — what MAY change between iterations:** exactly ONE mechanism,
  with its own pre-registered rationale written before the run.
  Mechanism-level only: e.g. replace a distress-state component, change the
  exit rule's trigger family. **A threshold value changed inside a surviving
  rule is a parameter change, not a mechanism change — forbidden outright.**
- **What may NEVER change:** the bar (four legs + the (a′) exercise
  condition); the zero-overlap rule (vs six prior sets, company AND name-date
  level); the no-refit / one-locked-run rule; frozen dirs; the
  decisional-test-set requirement; the void rule; the data→runner→logs-before-
  results commit order; the kill-list resurrection ban.
- **Explicitly forbidden:** (1) parameter grids — any search over thresholds,
  weights, bands, or cutoffs, on any data the run touches; (2) bar softening
  — including the already-rejected "0 screenable blow-ups" weakening and any
  redefinition of "clearly positive" or 0.8×; (3) same-set reruns — a failed
  set is never re-run under a new design; the new design gets a new set;
  (4) serial patch loops — more than one mechanism change per iteration, or
  the same mechanism carried forward with tweaked inputs, is not a fresh
  design; (5) resurrecting dead designs (§10).

## §10 — Kill list (dead approaches — resurrection needs a fresh design, not a touch)

- Frozen DCF entry anchor (FM1 — value anchor, systemic miss).
- Event-only GEV as the blow-up-leg mechanism (FM2/FM3 — reactive by
  construction, decisional ~0).
- QFV 1.00× entry tier (FM4 — zero compounder entries in two OOS runs); the
  four AND-gated QFV quality conditions are dropped, not re-justified (§2.6).
- GEV-exercise filter that omits usability (failed its own purpose twice).
- Type 7 as a standalone codified veto (folded into T7/SEVERE per §5.1).
- Usability check (b) (never fired in four runs).
- 15%-hurdle price reporting (dead since v3.2).
- Financial-variant usability exemption without a replacement screen (the hole
  Srei walked through — replaced by D6, no free pass).
- Margin fade as a quality signal (directionally backwards — taxes expansion).
- Beneish/accruals as fraud screens; Piotroski-as-fraud; dividend cuts as
  distress (perverse in India); promoter buying as a positive signal
  (evidence: none/ex-post/perverse).
- Own-multiple anchor, Gate M, Guardrail V (already dead; re-confirmed).

## §11 — Constant status table (every number's provenance)

| Constant | Value | Status |
|---|---|---|
| Rf / ERP / TAX / TG | 6.95% / 4.0% / 25.17% / 4% | carried accidental-but-frozen (v3.10) |
| Anchor horizon | 20y (10y @g + 10y linear fade + terminal yr 20) | structural: FM1 — 10y truncates durable excess returns; 20y ≈ franchise lifetime, two business cycles — round, flagged accidental-but-frozen |
| Fade shape | linear to TG | accidental-but-frozen (simplest auditable shape) |
| Margin | trailing-5y avg OPM, flat | carried definition; flatness is structural (kills the backwards fade) |
| WC 5% incr rev; capex≈dep; netcash = inv−borr; shares = mcap÷price; sector β pre-run | as v3.10 | carried simplifications/compromises |
| g_sus family incl. C1/C2/C3 | §2.2 | carried (v3.10); cap 15% carried accidental-but-frozen, highest-leverage accidental constant |
| k = 0.875 / 0.70 | tiers G1/G2 | structural role, accidental values; never fitted |
| g_implied solver bounds | [−0.50, w−0.01] | reporting-only bounds, frozen |
| Fill mechanics | first weekly close, 24m, 1 leg/tier | carried (v3 #21) |
| Pledge level D1 | ≥50% of promoter holding | round structural bar at invocation-cascade level; literature models continuously — no fitted cutoff exists |
| First-time pledge D2 | 0.0% for 8 trailing quarters → >0 (min 4 quarters) | NSE-NYU 2014 EM-spike evidence; lookback length is round structural |
| Altman Z'' D3 | 6.56/3.26/6.72/1.05, no +3.25; veto <1.1; grey 1.1–2.6 passes | literature coefficients + published distress boundary (Altman–Hartzell–Peck 1995); not fitted |
| Piotroski F D4 | veto ≤ 2 | Piotroski 2000's own low-bucket boundary; literature cutoff |
| Crash veto D5 | ≥60% drawdown from trailing-52w high | round structural bar above index-crash magnitudes (~38–40%) |
| CAMEL D6 | bands as §3; total ≤ 4; hard floors GNPA>12% / CAR<9% | bands round structural; floors = RBI PCA thresholds; equal 0–2 weighting disclosed structural |
| Usability U3 | ±15% tolerance; median results-week..+21d; >10%-jump skip rule | carried (v3.7); round, load-bearing for input integrity |
| Event window §5.3 | trailing 12 months | carried continuity (load-bearing per W4) |
| Cooling-off §5.3 | 12m + 1 audited print (results date AND FY-end strictly post-event) | rewritten for operability; release-skeptical by design |
| Exit slippage §5.4 | 0.99 (1.0%) | pre-registered, uniform, not fitted |
| Delisting staleness §5.4 | last print >20 trading days before event ⇒ UNEXECUTED | pre-registered convention |
| Fill-plausibility band §8.2 | P_d0 ≤ 2.0 × P_G1 | round, accidental-but-frozen, never re-tuned |
| Decisional test set §8.2 | 5 certified; decisional ≥3; void rules | learned from v3.11 (structural) |
| Aggregation | leg-weighted means, price return only | carried continuity (accidental-but-continuity-load-bearing) |
| Zero-overlap §8.3 | vs 5 prior sets (v4), vs 6 (iterations) | structural (OOS validity) |

## §12 — Open items for Bablu (veto/confirm before the build)

Structural decisions the coordinator froze on the workers' best evidence;
each is one veto away from changing:

1. **QFV quality conditions dropped entirely**, not re-justified (§2.6). Veto
   to restore any of them as a v4 gate.
2. **No-kill iteration** (§9): fail → diagnose → fresh design + fresh set,
   exactly one mechanism per iteration, threshold-tweaks forbidden, kill-list
   ban binding. This encodes Bablu's 2026-09-30 override and replaces the
   review's one-shot-kill commitment. Confirm.
3. **Fill-plausibility band** P_d0 ≤ 2.0 × P_G1 (§8.2): round,
   accidental-but-frozen, never re-tuned. Veto to change the band.
4. **Attribution order** distress → usability → event lane → anchor (§7):
   resolves the W2/W3 conflict for distress-first attribution honesty.
   Confirm.
5. **Z''-for-all-non-financials at 1.1**, grey zone (1.1–2.6) passes, Ohlson
   rejected (§3 D3): the literature cutoff is only honest on the unadjusted
   formula. Confirm.
6. **Piotroski veto F ≤ 2** vs ≤ 3 (some India papers use terciles) (§3 D4).
   Confirm ≤2.
7. **First-time-pledge lookback 8 quarters** vs 4 (§3 D2). Confirm 8Q.
8. **CAMEL equal 0–2 weighting** — confirm no differential weights (§3 D6).
9. **No cooling-off / no re-admission for distress** — scoring veto covers
   the full 24m window (§3). Confirm the simplification.
10. **Piotroski fail-closed-0 fallbacks** for F_ΔLIQUID / F_ΔMARGIN (§3 D4) —
    biases toward vetoing names with thin AR data. Confirm the fail-closed
    direction.
11. **Exit slippage 1.0%** (§5.4). Veto to change.
12. **Press-only SEVERE cap** — press-only records cap at MODERATE, may veto
    entry but never force exit (§5.2). Veto to lift.
13. **Exit fires on SEVERE only** (§5.4) — MODERATE in-window never exits.
    Veto to include MODERATE.
14. **T7 legal-stay rule** — event date = agency publication date regardless
    of court stays barring default recognition (§5.1 T7; the Srei lesson
    codified). Veto to revert to legally-effective date.
15. **Release-skeptical cooling-off** — release requires a documented
    two-source search proving a post-event audited print (§5.3). Veto to make
    release easier.
16. **Premium franchises at P/FV_v3 ≳ 2.5× still excluded** — the anchor holds
    *reasonable-implied-growth*, not compounders at any price (§2.5). This is
    a Bablu-level call on whether that satisfies the bar's intent, not a
    parameter question.
17. **15% g_sus cap binds almost universally** — highest-leverage accidental
    constant; carried with a named reporting-only sensitivity in pre-reg
    (§2.2, §11). Confirm the carry.
18. **Fin-variant anchor construction** (inverse excess-return, ROE fading to
    w, terminal = book; §2.4) — judgmental-but-frozen. Confirm.

## Amendment log (pre-run finalization, approved by Bablu; no v4 validation has run)

1. §5.2 MODERATE list gains three sub-cases: T1 order that is neither a fraud finding nor a ban; T2 resignation with other stated reasons (no CARO fraud flag); T5 named FIR alone.
2. §5.1 T6: underlying MODERATE downgraded one grade = WATCH made explicit (§5.2 T6 MODERATE entry narrowed to "SEVERE underlying, downgraded").
3. §3 D3: CA/CL split for X1 sourced from the AR PDF; unretrievable ⇒ UNCOMPUTABLE-DATA veto.
4. §0: "§2.7" corrected to "§2.6".
5. §5.2 SEVERE list gains "T2 auditor resignation citing unpaid fees" (per §5.1); closes the §5.1/§5.2 omission. No engine change (already SEVERE).
