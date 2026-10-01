# v4 OOS pre-reg R6 — Gate 1 blow-up sweep: CERTIFICATION DOSSIER

**Date:** 2026-09-30 · **Verifier:** Musey (R6 coordinator) + 3 parallel evidence subagents
**Verdict: SHAPE-COMPLETE — 2 new certified name-dates / 1 company (PBM Polytex double-carrier).** Certified total: 4/5 (Supreme Engineering 2020∩2021 + PBM Polytex 2019∩2020). One single-carrier still missing. Nothing below names any company investable; the system remains NOT LIVE.

Scope discipline: evidence-only research. No engine/spec changes, no validation runs, no repo commits/pushes. All work in `~/workspace/stock-judging/v3/oos_candidates/`. R3/R4/R5 files untouched.

Target shape: **2+2+1** — five blow-up name-dates = two double-carriers + one single. R6 needed one more double-carrier + one single. Found: the double-carrier. The single remains open.

---

## 1. Worker axes and funnels

| Worker | Axis | Names examined | Firewall runs | Survivors |
|---|---|---|---|---|
| W1 | First-ever qualified annual opinions, mainboard small-caps, long screener histories | ~24 | 140 (batch) | 0 (2 near-misses: DCW, Vivimed — both U2-vetoed) |
| W2 | Forensic-AR mining, textiles/apparel sector cut | ~24 | 16 | 1 (PBM Polytex, 2 name-dates) |
| W3 | Pledge-invocation T3 remnants + T4 withdrawn capital actions (coordinator's choice) | ~18 + T4 sweep | 8 | 0 |

Firewall ran BEFORE any tape walk on every lead — zero tape walks wasted on firewall-dead names (R3/R4/R5 rule held).

---

## 2. CERTIFIED: PBM Polytex Ltd (BSE 514087; textiles)

**Name-dates:** `pbm_2019-03-31` + `pbm_2020-03-31` — **double-carrier 2019∩2020.**

**E1 (T2): statutory auditor resignation** — M/s. Chandulal M. Shah & Co. (FRN 101698W) resigned vide letter dated **18-Jul-2020**; company intimation to BSE filed **30-Sep-2020** (Reg 30(2) LODR, through BSE Listing Centre). Rinkesh Shah & Co. (FRN 129690W) appointed at the 101st AGM 30-Sep-2020.

Primary evidence:
- BSE intimation 30-Sep-2020 (company letterhead, MD Gopal Patodia): https://cdn.financialreports.eu/financialreports/media/filings/61511/2020/RNS/61511_rns_2020-09-30_e8e51e87-9b35-44f0-8b05-ccb4b37d65b9.pdf (independently confirmed via web search: company letter dated 30.09.2020 through BSE Listing Centre, scrip code 514087)
- Resignation letter (18-Jul-2020) uploaded on company site: https://pbmpolytex.com/upload/investor_lodr_reg/intimation-of-resignation-of-statutory-auditor.pdf (cached text: "letter dated July 18, 2020")

**E1 dating convention (coordinator adjudication):** E1 is dated by FIRST EXCHANGE DISCLOSURE (30-Sep-2020), consistent with the R3 Supreme Engineering precedent (E1 = 2021-11-03 NSE filing date, not the letter date) and Bablu's "first ever on the tape" framing — the resignation only becomes a market event on the disclosure record. The 2.5-month letter→disclosure gap is documented; no earlier (July/August 2020) disclosure surfaced in searches.

**Band math:** 30-Sep-2020 ∈ d0-2019 window [2019-09-30, 2021-03-31] ✓ and ∈ d0-2020 window [2020-09-30, 2022-03-31] ✓ (boundary inclusive) → double-carrier 2019∩2020 (B1 band). Under letter-date it would be a d0-2019 single only.

**Firewall (frozen engine_v4 anchor, read-only; coordinator re-verified from raw JSON):**
- pbm_2019: scoring FY18, P_d0=78.65, P_G1=106.66, ratio=0.737 → PASS
- pbm_2020: scoring FY19, P_d0=28.85, P_G1=133.55, ratio=0.216 → PASS
- (pbm_2021 ratio 1.204 PASS but no in-band E1; pbm_2022 ratio 19.32 FAIL — both irrelevant)

**First-ever tape walk (FY17–FY20, official ARs from pbmpolytex.com; coordinator spot-checked cache):**
- FY17 (98th AR), FY18 (99th AR), FY19 (100th AR): all unmodified ("true and fair view"); FY19 AR explicitly states "There has been no Audit Qualification / Modified Opinion(s) in the Audit Reports by the Auditor." The "qualification" text hits are secretarial-audit/director boilerplate, not audit qualifications.
- FY20 audited results (board 31-Jul-2020): Reg 33(3)(d) declaration — unmodified opinion.
- No earlier qualifying §5.1 event on the walked tape (no SEBI orders, no NCLT/CIRP, no rating-D). The 09-Aug-2022 second resignation (Rinkesh Shah) cannot be E1 — first-ever rule.

**Usability (worker ran exact frozen engine_v4.usability; parent to re-run for official record):**
- pbm_2019 (FY18): U1 PASS (no restatement; audited/sourced 0.998), U2 PASS (sourced EPS 4.69)
- pbm_2020 (FY19): U1 PASS (audited/sourced 1.000), U2 PASS (sourced EPS 3.94)
- No bonus/split corporate actions (audited EPS matches screener to 3 decimals; consolidated P&L used — standalone headline EPS differs, worker used the consolidated figure)

**Listing date:** BSE 514087, incorporated 1919, BSE filings from May 2018 — listed well before d0-2019 (traded P_d0 at d0-2019 confirms).

**Disjointness:** absent from r4_excluded_companies.txt, all prior sets, R3/R4/R5 dossiers, sibling W1 firewall cache. Company never touched before.

---

## 3. Firewall kill table (W2 near-misses + W3 leads)

| name-date | E1 lead | P_d0 | P_G1 | ratio | Kill |
|---|---|---|---|---|---|
| morarjee_2019-03-31 | going-concern qualification (unpinned year) | 23.4 | 29.68 | 0.788 | PASS firewall but E1 year never pinned — NOT certified |
| morarjee_2020/2021/2022 | same | 7.05/14.15/24.95 | −93.14/−87.29/−87.68 | — | non-positive P_G1 |
| svpglobal_2019–2022 | none in-band | — | — | — | UNCOMPUTABLE: no screener P&L table |
| 532886_2019/2020/2022 (SEL Mfg) | "Basis for Qualified Opinion" | 1.2/0.43/368.8 | −1671.98/−1682.42/−1147.65 | — | non-positive P_G1 |
| 532886_2021 | same | — | — | — | listing gap |
| id/3490_2019-03-31 (Tulip Star) | 18-Nov-2019 Yes Bank invocation | — | — | — | UNCOMPUTABLE: no close within 10d (BSE-suspended) |
| id/3490_2020/2021 (Tulip Star) | same | 27.0/38.5 | −305.19 | — | non-positive P_G1 |
| ansalhsg_2019–2022 (Ansal Hsg) | 13-Dec-2021 HDFC invocation | 12.1/2.75/5.2/7.13 | −59.86/−68.68/−86.68/−84.17 | — | non-positive P_G1 |

---

## 4. Notable non-firewall kills

- **Sical Logistics** (15-Jan-2020 invocation, d0-2019 single candidate): EXCLUDED (`sicallog`) — untouched.
- **MEP Infrastructure** (03-Apr-2020 promoter-group invocation, textbook T3): EXCLUDED (`mep`) — untouched.
- **Sankhya Infotech** (13-Dec-2020 invocation): R5 W3 already examined — untouchable.
- **KPR Mill** (12-Jul-2019 buyback withdrawal): pre-band + tax-driven, healthy — T4 axis effectively empty in-band.
- W2 triage: Spentex (CIRP 2017 pre-band), Nandan Denim (2024 post-band), Filatex (order was against Filatex *Fashions*, different company), Soma (EOM, unmodified), Himatsingka (BBB+ ≠ D), Indo Rama (non-E1 type), Sarla (2026 qualification post-band), Samtex (negative net worth, unwalkable); Siyaram/Vishal/Ashima/Sreeleathers/Donear clean.
- **T3 track: FULLY EXHAUSTED** (W3) — every in-band invocation is excluded, already examined, or firewall-dead. **T4: effectively empty in-band** — withdrawn buybacks/rights are rare and tax/regulatory-driven, not distress-driven.

---

## 5. Disjointness (V4_SPEC §8.3)

`check_disjoint_r6.py` imports all prior canon lists (never retyped); R4 leads loaded from `r4_firewall_results.json` at runtime. R6 lead companies asserted against every prior set (in-sample, v3.8–v3.11, R1-examined, R2-examined, R3-certified, R4-leads, R5-leads): **DISJOINT: True**. No names burned.

---

## 6. Structural findings (fourth straight round)

1. **The profitable-resignation profile is the only cond-2 survivor.** Supreme Engineering (R3) and PBM Polytex (R6) are both profitable companies with mid-term auditor resignations — the inverse-DCF anchor prints positive triggers for them while pricing every distressed name ≤0. Future sweeps should target this profile first.
2. **cond-2 remains the binding constraint** on every axis: distressed textile names (Morarjee, SEL, Samtex), pledge-invocation names (Tulip Star, Ansal Housing) all die at non-positive P_G1.
3. **T3 fully exhausted; T4 structurally thin.** Remaining unexhausted axes are getting scarce — the 2+2+1 shape's last single-carrier will likely come from the profitable-resignation profile, not from distressed-event axes.

---

## 7. Verdict and what would un-void it

**SHAPE-COMPLETE at the double-carrier level; Gate 1 needs one more single-carrier.** Certified: 4/5 name-dates (supremeeng 2020∩2021, pbm 2019∩2020). The second double-carrier requirement is now SATISFIED — PBM Polytex is the second double-carrier. Still missing: ONE single-carrier name-date.

**R7 axes** (suggestions): first-ever mid-term auditor resignations at profitable mainboard small-caps (the proven profile — e.g. BSE/NSE resignation filings 2019–2023 cross-checked against profitability); forensic-AR mining in another sector (auto-ancillaries, packaging/paper) restricted to profitable names. The distressed-event axes are exhausted.

---

## Appendix A — W1 findings (qualified annual opinions, mainboard small-caps)

**Verdict: 0 certified.** ~24 names touched, ~90 AR PDFs walked (Tijori + Wayback). Firewall ran first on all leads.

**Near-miss 1 — DCW Ltd:** FY21 qualified annual opinion (Chhajed & Doshi, Mumbai 21-May-2021; basis: trade receivables subject to confirmation); first-ever on tape (FY17–FY20 clean). E1 21-May-2021 ∈ B1 [2020-09-30, 2021-03-31] → 2019∩2020 double-carrier shape. Exact frozen `engine_v4.usability`: U1 PASS both, **U2 STOP** (scoring FY18 EPS −0.91; FY19 EPS −0.19). Recomputed P_G1 13.85/15.51, ratios 1.574/0.493 → fill-plausible but usability-vetoed. **Data-integrity note:** the batch-1 firewall cache for DCW was truncated (P&L only Mar 2008–Mar 2015 → scoring_fy 2015 artifact, P_G1=10.08); all DCW numbers are the worker's rebuild from a fresh screener fetch, not the batch record.

**Near-miss 2 — Vivimed Labs Ltd:** FY23 qualified annual opinion (P C N & Associates, Hyderabad 30-May-2023; 6 bases incl. bank defaults ₹3,762.80M, P&M impairment ₹892.80M, inventory write-down ₹809.3M; "Frequency of Qualification: 1st Time"); first-ever on tape (FY18–FY22 clean). E1 30-May-2023 ∈ d0-2022 window → d0-2022 single-carrier. Exact frozen engine: U1 PASS, **U2 STOP** (scoring FY EPS −13.16). P_G1 24.88 fill-plausible.

**Structural lesson from this axis:** it produces real in-band first-ever qualifications that die at U2 — distressed names with qualified opinions almost always have non-positive scoring-FY EPS. Here U1/U2 (not the firewall) is the binding constraint — the reverse of R4/R5.

**Other W1 kills:** HCC (first-ever ≤ FY19, pre-window), Hubtown (first-ever FY18, pre-window), PBA Infra (NPA since 2013, pre-window), Patel Engineering / Subex / Shemaroo / SPIC / Kopran / Atul Auto / Sunflag / Shilpa / Nectar / Indoco / Nelcast / Morepen / Mukand / Anuh Pharma / SML Mahindra (clean, no E1), 3i Infotech (no in-band first-ever), Mindteck (IFC-only qualification, financials unmodified), Sequent (delisted), rpglife (uncomputable). Label correction: screener slug `neclife` = Nectar Lifesciences Ltd (NSE: NECTAR).
