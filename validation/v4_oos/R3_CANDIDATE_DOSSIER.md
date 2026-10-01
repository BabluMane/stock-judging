# v4 OOS pre-reg R3 — Gate 1 blow-up sweep: CERTIFICATION DOSSIER

**Date:** 2026-09-30 · **Verifier:** Musey (coordinator) + 3 parallel evidence subagents
**Verdict: VOID — 2 certified name-dates / 1 company (updated 2026-09-30).**
SUPREMEENG 2020-03-31 + 2021-03-31 certified (first-ever tape completed:
FY19/FY20 unmodified verified; exact U1/U2 run on frozen engine). Nothing below
names any company investable.

Scope discipline: evidence-only research. No engine/spec changes, no validation
runs, no repo commits/pushes. All work in `~/workspace/stock-judging/v3/oos_candidates/`.

Target shape: **2+2+1** — five blow-up name-dates = two double-carriers (first
qualifying event E1 inside a double-carrier band) + one single-carrier.

Scoring dates and E1 bands (§8):
| d0 | band |
|---|---|
| 2019-03-31 | [2019-09-30, 2021-03-31] |
| 2020-03-31 | [2020-09-30, 2022-03-31] |
| 2021-03-31 | [2021-09-30, 2023-03-31] |
| 2022-03-31 | [2022-09-30, 2024-03-31] |

Double-carrier bands: [2020-09-30, 2021-03-31], [2021-09-30, 2022-03-31], [2022-09-30, 2023-03-31].

Certification conditions per name-date:
1. **usable** — U1/U2 input conditions (U3 ±15% is locked Phase D, never applied).
2. **fill-plausible** — P_d0 ≤ 2.0 × P_G1 (fill_plausibility_firewall.py anchor math only).
3. **first-ever** — E1 is the first qualifying event (T1–T7) on the company's tape.

Prior-round lessons applied: full agency rating-history columns; consolidated
(not just standalone) audit opinions walked back to FY18/19; "Reaffirmed" PRs
hiding earlier D dates; Jan-2019 Essel pledge-invocation group kills; subsidiary/
SPV ≠ listed parent; listing-date-before-tape-walk. Every "fetched and read"
evidence item carries its exact URL.

---

## 1. Certification table

| name-date | E1 (date / type / severity) | cond 1 usable | cond 2 fill-plausible | cond 3 first-ever | verdict |
|---|---|---|---|---|---|
| supremeeng_2020-03-31 | 2021-11-03 auditor resignation (T2) | **pass** exact U1/U2 (frozen engine_v4.usability, 2026-09-30) | **pass** P_d0=1.54 P_G1=7.44 ratio=0.207 | **CLEAR** — FY19 unmodified (R.T. Jain, 29-May-2019) + FY20 unmodified (Reg 33(3)(d) decl. 05-Aug-2020) | **CERTIFIED** |
| supremeeng_2021-03-31 | 2021-11-03 auditor resignation (T2) | **pass** exact U1/U2 (frozen engine_v4.usability, 2026-09-30) | **pass** P_d0=2.56 P_G1=7.44 ratio=0.344 | **CLEAR** — FY19 unmodified + FY20 unmodified | **CERTIFIED** |
| indostar_2021-03-31 | 2022-08-05 Deloitte qualified opinion FY22 (T2 MODERATE) | pass (proxy*) | **FAIL** P_d0=316.30 P_G1=107.09 ratio=2.954 > 2.0 | clean (FY20 and earlier positive; FY21 AR positive-confirmation pending) | **FAILED** |

\* cond-1 proxy (superseded 2026-09-30): exact U1/U2 was run against the frozen
engine_v4.usability module on both name-dates — U1 PASS (no restatement; implied
shares x0.988/x1.00 vs split factor 10; audited/sourced 11.30 FY19 / 12.04 FY18,
split-adjusted residual 1.13/1.20 = weighted-avg vs year-end shares convention,
IPO Sep-2018 mid-year — documented, gates nothing) + U2 PASS (sourced FY EPS
0.27 / 0.15 > 0). U3 locked per Bablu adjudication (2026-09-30), never applied.

### CERTIFIED — Supreme Engineering (NSE: SUPREMEENG)
- **E1 = 2021-11-03, T2.** Statutory auditor R T Jain & Co. LLP resigned —
  fee dispute ("nonagreement on terms and conditions w.r.t our remuneration").
  Company filing ref SEL/NSE/CA/21-22/9; NSE archive 03-Nov-2021.
  URL: `https://nsearchives.nseindia.com/corporate/SUPREMEENG_03112021150108_CA9.pdf`
- **Band mapping:** 2021-11-03 ∈ [2021-09-30, 2022-03-31] = d0 2020-03-31 ∩ d0 2021-03-31
  → double-carrier (arithmetically recomputed from band table, 2026-09-30).
- **First-ever tape (verified, COMPLETE):**
  - FY21 audit unmodified (R T Jain, 30-Jun-2021, "Our opinion is not modified") —
    URL: `https://www.stockscans.in/document/35woqdu0l2j6nozcz0g71qly.pdf`;
  - **FY20 unmodified** — Reg 33(3)(d) declaration filed with annual results,
    NSE 05-Aug-2020, "Declaration for audit reports with unmodified opinion(s)" —
    URL: `https://nsearchives.nseindia.com/corporate/SUPREMEENG_05082020222700_DECLARATIONFINAL.pdf`
    (verified live-browser 2026-09-30; note: declaration is standalone-only and
    company had no consolidated results);
  - **FY19 unmodified** — Independent Auditor's Report, FY19 annual report
    (pp. 45–47): "In our opinion ... the financial statements ... give a true
    and fair view" — no qualification, no emphasis of matter. Auditor R T Jain &
    Co. LLP, FRN 103961W/W100182, signed Mumbai, May 29, 2019 (CA Bankim Jain,
    Mem No. 139447). Audited basic EPS ₹3.05 (FY19) / ₹3.25 (FY18), FV ₹10.
    Source: official NSE annual-report ZIP
    `https://nsearchives.nseindia.com/annual_reports/SME_AR_15709_SUPREMEENG_2018_2019_04092019103810_04092019110003.zip`
    (downloaded + text-extracted 2026-09-30);
  - BWR: BBB- (25-Oct-2019) → reaffirmed BBB- (18-Dec-2020) → BB+ (17-Mar-2021)
    → **D 26-Mar-2022** (banker-confirmed NPA) — post-E1, so D is not the E1;
    no pledge invocations found pre-Nov-2021. Listed 06-Sep-2018 (listed at all d0).
- **Corporate actions:** one 1:10 split ex 03-Mar-2022 (FV ₹10→₹1); no bonus
  ever; no rights. (Trendlyne/ET Money/marketsmojo agree.)
- **Exact U1/U2 (frozen engine_v4.usability, 2026-09-30):**
  scoring FY = 2019 (d0 2020-03-31) / 2020 (d0 2021-03-31) per 63d PIT.
  U1 PASS both (no restatement; sourced series already post-action basis);
  U2 PASS both (sourced FY EPS 0.27 / 0.15 > 0). Audited/sourced residual
  1.13 (FY19) / 1.20 (FY18) split-adjusted = weighted-average vs year-end
  shares convention (Sep-2018 IPO mid-year) — documented, gates nothing.
  U3 locked (Phase D), not applied.
- **Certified name-dates: supremeeng_2020-03-31, supremeeng_2021-03-31.**
  Gate 1 still VOID overall (2/5; need a second double-carrier + one single).

### FAILED — Indostar Capital Finance (NSE: INDOSTAR)
- E1 = 2022-08-05, T2 MODERATE (Deloitte qualified FY22 standalone+consolidated;
  board-meeting outcome filing) — valid, first-ever tape clean, single-carrier
  (2021-03-31 band only).
  Evidence URLs: `https://files.tijorifinance.com/insight/india/7408/Earnings%20Release/ER-Mar22.pdf`,
  `https://www.indostarcapital.com/assets/pdfs/Disclosures As Per Regulation 30/IndoStar-Q4FY22-Results-Update-3.pdf`,
  ICRA `https://www.careratings.com/upload/CompanyFiles/PR/10102022072312_IndoStar_Capital_Finance_Limited.pdf`,
  FY23 AGM transcript `https://www.indostarcapital.com/assets/pdfs/Investor Services/AGMEGM/2022-2023/Transcript-of-the-AGM-September-2023.pdf`.
- **Killed by cond 2:** firewall ratio 2.954 > 2.0 — the system could never have
  filled it (price at d0 nearly 3× the G1 trigger), so it cannot be a decisional
  exercise of the distress screen. Evidence-quality lesson: even the strongest
  paper candidate dies at the anchor.
- (Moot now: FY21 AR positive-confirmation of unmodified opinion never obtained.)

---

## 2. Near-misses (do not re-examine without new primary evidence)

| name | E1 found | killing reason |
|---|---|---|
| Sterling and Wilson Solar (SWSOLAR) | 2020-06-23 BSR qualified opinion FY20 (T2), first-ever anchored by company's own "since March 2020" impact statement | **unlisted at d0** — listed 20 Aug 2019, no P_d0 for 2019-03-31, cond-2 uncomputable. Nearest certifiable-shaped candidate found anywhere; only resurrects if pre-reg relaxes unlisted-at-d0 mechanics |
| Adani Enterprises (ADANIENT) | 2023-02-01 ₹20,000cr FPO withdrawal (T4 MODERATE, NSE Reg-30 filing) | category honesty — market-driven (Hindenburg → crash → withdrawal), no documented default/insolvency/audited distress |
| RMC Switchgears (BSE SME 540358) | BWR D 21-Mar-2022 (double-carrier-shaped: d0 2020 ∩ 2021) | INC-category D — BWR/CRISIL both carried "Issuer Not Cooperating" D while Infomerics held BBB-/Stable through the window and the company was profitable (FY22 PAT ₹0.58cr, FY23 ₹11.74cr). Technical non-cooperation D, not documented default → category-honesty fail; BSE-SME price-data path also untested |
| Spandana | SEBI settlement order 2022-10-27, ₹25 lakh, no admission | §5.2: SEBI settlement with no admission = log only, no veto power; no documented distress |
| Equitas Small Finance Bank | SEBI adjudication order 2022-12-19 confirmed to exist | page JS-gated; substance unknown — needs live browser (only matters if a qualifying name attaches) |
| Vikas Ecotech | in-band BWR D 20-Nov-2020 (decoy) | pre-band T3 pledge invocation 09-Jul-2019 = first-ever E1, out of all bands |
| Unity Infraprojects | T2 qualified FY16 | pre-band |
| Sunshield Chemicals (2022-06-17) | Deloitte resignation, fee dispute | borderline T2 + category fail |
| RIL | SEBI ₹25cr penalty 2021-01-01 (T1 in-window) | first-ever kill (SEBI March 2017 ₹447.27cr disgorgement + 1-yr derivatives ban) + category fail |
| 16 others (infra/industrial worker) | — | Shriram EPC/SEPC, Aksh Optifibre, Kohinoor Foods, JBF Industries, Mercator, Visa Steel, Ansal Properties, Uttam Galva, IL&FS Engineering, Valecha Engineering, Garden Silk Mills, Hubtown, MBL Infrastructures, Supreme Infrastructure India, Arfin India, Le Lavoir — failed on pre-band kills / non-qualifying event types / category honesty |
| 2022-23 window sweep residue | — | RattanIndia (BB), JPVL, Ansal, TTML, Supreme Infra: no D; Aksh Optifibre D dated 2024/2025 out-of-band; Brickwork Jan-2023 D items were reaffirmations, entities unnamed |

---

## 3. Disjointness (V4_SPEC §8.3)

Extended `check_disjoint_v4.py` → `check_disjoint_r3.py` in this directory.
Prior membership lists imported, never retyped:
- in-sample 25 / v3.8 / v3.9 / v3.10 / v3.11 OOS 13×4 → **77 companies / 150 name-dates**
- R1 (v4_oos/fill_plausibility_results.json): **57 companies / 171 name-dates** examined, excluded as failed examinations
- R2 (9 companies × 4 scoring dates, reconstructed per AUDIT_PR13_V4_OOS_R2.md "36 rows / 9 names"; the R2 JSON did not land in this workspace copy): **9 companies / 36 name-dates**

R3 finalists (supremeeng 2020/2021-03-31, indostar 2021-03-31): **DISJOINT: True**
vs every prior set, every R1-examined name-date, every R2-examined name-date.

---

## 4. Verdict and what would un-void it

**VOID at Gate 1 — 2 certified name-dates / 1 company (2026-09-30 update).**
Supreme Engineering's two name-dates certified (see §2). The 2+2+1 shape is
still infeasible on current evidence: 2 certified (one double-carrier) + 0
singles; three more name-dates have no live lead (the three worker sweeps
covered ~50 names across D-rating, auditor-resignation, SEBI-order,
pledge-invocation, and default tracks; every in-window D was an excluded name
or a non-qualifying reaffirmation).

**Path to certification (for the parent):**
1. ~~Live-browser check: Supreme Engineering FY20 (and FY19) Reg 33(3)(d)
   declaration.~~ DONE 2026-09-30 — both unmodified; name-dates certified.
2. A fresh double-carrier lead is still needed for the second pair — the sweep
   found none. Options: deeper BWR/CARE/ICRA FY23 Annexure VI-A lists, or
   another worker pass on a different sector axis.

Raw worker dossiers: `r3_sweep_dossier.md` (financials + infra/industrial
sweeps, §§1–8). Firewall outputs: `firewall_indostar.json`,
`screener_cache/` (cond-2 anchor math per name-date). Machine-readable set:
`r3_candidates.json`.
