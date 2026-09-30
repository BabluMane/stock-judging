# v4 out-of-sample pre-registration R2 (Phase C retry) — 2026-09-30

## STATUS: VOID at Gate 1 (V4_SPEC §8.2 void rule) — 0 of 5 blow-up name-dates certified

**Gate 1 count: 0 name-dates fully certified / 0 companies.** The retry had the sources the first
attempt (`V4_OOS_PREREG.md`, PR #12, VOID) lacked, and the failure this time is *not* data access:
the eight candidate leads fail on the frozen conditions themselves. The required 2+2+1 shape needs
**two** companies whose single first-qualifying event E1 sits in two consecutive scoring windows;
on the verified record **no such second company exists** (§3.3), so the 5-name-date decisional set
cannot be assembled from this pool however the open items resolve.

Per the task's Gate rule and §8.2, nothing is frozen: **no winners or mediocrities are
pre-registered** (freezing names around a dead decisional set only burns them), **no v4 OOS set
exists, and no locked run may start on anything recorded here.** The system is NOT LIVE; nothing
in this document describes any company as investable.

This document is additive history next to the first attempt, which is untouched and read-only. No
engine, spec, `engine_v4/` or `validation/v3_*` file was modified. No validation, distress screen,
full usability, event-lane evaluation, exit scan, fill simulation or aggregation was run. The two
permitted computations were run and nothing else: (i) the frozen `engine_v4.anchor` via the existing
`fill_plausibility_firewall.py`, emitting only `P_d0`, `P_G1` and their ratio (§8.2 cond 2);
(ii) the U1/U2 input checks (named basis; sign of the sourced audited-FY EPS) — no U3 numeric check.
No bar, threshold, band or parameter was touched; no dead design is used (§9 below).

**What the research changed relative to the sweep's orientation tags** (each re-fetched, not trusted):

| Lead claim | What the re-fetched record shows |
|---|---|
| Simplex is first-ever with E1 = 2019-12-11 | **False.** Simplex's FY19 audited statements (standalone *and* consolidated) carry a qualified opinion from joint auditor S.R. Batliboi & Co. LLP (Board's explanation, Annual Report 2018-19, dated 30-May-2019): a T2(b) MODERATE event ≤ 2019-05-30, four months before the 2019-09-30 window start. Also, CARE cut BBB → BB+ on 2019-11-25 (sub-investment-grade, T7 MODERATE in `engine_v4/events.py`) before the D. |
| FEL / Future Consumer are fill-plausible | **False.** `P_G1 < 0` on all four dates for both (negative tier-1 trigger, cond 2 fails by construction). Future Consumer's consolidated FY18/19/20 EPS are also all negative (U2). |
| FLFL 2019-03-31 and 2020-03-31 | 2019 **fails cond 2** (P_d0/P_G1 = 3.421). 2020 passes cond 1/2 and the rating-tape window, single date only. |
| Omaxe 2019-03-31 and 2020-03-31 | **Fails cond 2** on both (4.175; `P_G1 < 0`). Also CARE's first sub-IG cut was 2020-04-03 (BBB- → BB+), not the 2021-03-05 D. |
| MEP 2021-03-31 | **VETOED-DATA (U2):** scoring-FY (FY20) consolidated EPS = −4.21. Dropped on input conditions alone. |
| Adani Ports: qualified opinion 2023-05-03 | Date is wrong: FY23 results and Deloitte's qualified opinion are 2023-05-30 (BusinessToday 2023-05-31). 2021-03-31 therefore fails cond 3 (window ends 2023-03-31), so Adani cannot be a double-carrier. |
| FSC 2019-03-31 | **Fails cond 2** (7.918). 2020-03-31 passes cond 2 but E1 (2020-09-10) is 20 days before the window start. |
| PFS "T1-first" 2022-01-19 director resignations | Independent-director resignations are **not a §5.1 type** (T2 covers *auditors*). E1 is unresolved between a contested SEBI direction (≈2022-03-03, press only) and MSKA's qualified opinion dated 2022-11-16 — which fixes which two dates PFS could carry. |

---

## 1. Frozen rules hash

| Item | Value |
|---|---|
| Spec file | `engine_v4/V4_SPEC.md` |
| Spec SHA-256 (computed this session, before any work) | `6acb4acdcb7f93a042df36d4eb111bcca5dfa38d894864ec13d269096f2be671` |
| Pin in `engine_v4/tests/test_constants.py` (`SPEC_SHA256`) and the task's expected pin | `6acb4acdcb7f93a042df36d4eb111bcca5dfa38d894864ec13d269096f2be671` — **match** |
| Base commit (branch `claude/v4-oos-prereg-r2` cut from `main` at) | `47d9dbf4dfbba5af0ab1f13c451ecde087cea5b7` (merge of PR #12, the VOID pre-reg) |
| `engine_v4/` tree at base (`git rev-parse HEAD:engine_v4`) | `6ea7e7a1de50ccfaccd466a4e1f402efbd3ebbe3` (identical to the first attempt's base tree) |
| `validation/v4_oos/fill_plausibility_firewall.py` SHA-256 (unchanged, reused) | `84e0dbd5fbe6c4b8a73138c02db0836e97796b9484df189c67aa8d650e8ae64d` |
| `validation/v4_oos/fill_plausibility_results_r2.json` SHA-256 | `4718861a296195c413964a4fc22e12310fcd1c432c92bb7801aa65924a6e75db` |
| `validation/v4_oos/check_disjoint_v4_r2.py` SHA-256 | `06995bd767804e90303b2d4c0270268475503e61d86764d510a32ae455e88aa5` |
| `validation/v4_oos/check_disjoint_v4.py` SHA-256 (unchanged, from PR #12) | `0e57b796c9a5935d662bf88b667c575bb043847efc9347da935fc8dd45f11d39` |
| Set manifest hash | **none — no set is frozen** |

A document cannot contain its own commit hash; the pre-registration commit is the commit that first
adds this file (`git log --diff-filter=A --format=%H -- validation/v4_oos/V4_OOS_PREREG_R2.md`).

## 2. Set composition (§8.1) — no set frozen

Spec shape (25 name-dates / 13 companies; 5 winners × 2, 5 mediocre × 2, 3 blow-up companies
totalling 5 name-dates as 2+2+1; March-31 scoring dates, all ≥ 2019-03-31; vintages 2019–2022) is
**unchanged and not met**. Blow-up side: 0 of 5. **Winners and mediocrities are deliberately not
registered** (Gate 2 not entered): a frozen name-date cannot be added, removed or re-dated, and §8.2
makes the run void when the decisional set is short. No data of any kind was fetched for any
winner or mediocre candidate. No one-line theses or category criteria were written for them.

## 3. Decisional test set (§8.2) — certification attempt: 0 of 5

### 3.1 Frozen adjudications applied (Bablu, 2026-09-30, verbatim from the task)

1. **Usability at pre-reg = input conditions only (U1/U2).** Cond 1 is certified from U1 (basis
   assertion with a named basis) and U2 (sourced FY EPS sign; ≤ 0 ⇒ VETOED-DATA). The U3 ±15 %
   check is a locked Phase-D outcome risk, not a pre-reg certifier; a Phase-D U3 fail is VETOED-DATA,
   reported honestly, never a reason to swap a name. *Basis named:* screener.in **consolidated**
   view (uniform v3.11 variant rule: consolidated if it parses with a Net Profit row, else
   standalone), vendor post-action series; all nine candidates parsed consolidated. U2 uses the
   `EPS in Rs` row of that view for the scoring FY.
2. **Class split** reads screener Broad Industry ∈ {Banks, Finance}. Only PFS ("Finance") is
   financial-class (D6 CAMEL; inverse excess-return anchor); the other eight are non-financial (D3+D4).
3. **E1 = first qualifying event ever on the tape** (no spec change). A qualifying event dated before
   d0 fails cond 3 for that date.
4. **2022-03-31 scoring dates allowed** (§8.1 vintages 2019–2022).

### 3.2 How E1 was read (one stated convention, applied uniformly)

§5.1 T7 is worded "downgrade to 'D'", but §5.2 grades "T7 sub-investment-grade cut below D (e.g. BB
and lower, not D)" as **MODERATE**, and the frozen `engine_v4/events.py` carries
`("T7","downgrade_sub_investment_grade_not_D"): MODERATE` (entry-veto grade). The event lane would
therefore *veto* on such a cut, so this document treats a SEBI-registered agency's first downgrade
**into sub-investment grade** as a qualifying MODERATE E1 (engine-consistent reading), and also
reports the D-only E1 for each name. Investment-grade cuts (e.g. AA- → A+, BBB → BBB-) are not events.
**No candidate's verdict depends on this choice**: every FAIL below holds under both readings (the only
place it changes a cond-3 cell is Omaxe 2020, which fails cond 2 regardless).

Conventions carried from the first attempt, unchanged: shares = screener Market Cap ÷ Current Price;
scoring FY via `engine_v4.pit.select_scoring_fy` with nominal `results_published` = FY-end + 60 days
(so d0 = 31-Mar-N ⇒ scoring FY(N−1)); β = 1.15 uniform (blow-up bucket, carried V310-C9);
P_d0 = last adjusted close at or before d0. A per-name-date check of the real results-filing date
(vs. the nominal one) remains a Phase-D item.

### 3.3 Why the set cannot be assembled (shape proof)

A company carries two name-dates only if one E1 lies in both windows; windows are
[d+6m, d+24m], so this requires *consecutive* scoring dates d1 < d2 with
E1 ∈ [d2+6m, d1+24m] — pairs (2019,2020): [2020-09-30, 2021-03-31]; (2020,2021):
[2021-09-30, 2022-03-31]; (2021,2022): [2022-09-30, 2023-03-31]. The 2+2+1 shape needs **two**
such companies. From the table below, per company, the consecutive pairs that survive cond 1 and cond 2:

| Company | Consecutive pairs passing cond 1 **and** cond 2 | Result |
|---|---|---|
| Simplex | (2019, 2020) | E1 ≤ 2019-05-30 (and ≤ 2019-12-11 on any reading) is outside both windows → **no** |
| FEL | none (`P_G1 < 0` everywhere) | **no** |
| Future Consumer | none | **no** |
| FLFL | none: 2019 fails cond 2 (3.421); 2021 fails U2; (2020, 2021) needs E1 ≥ 2021-09-30 but E1 = 2020-10-15 (D: 2020-11-11) | **no** |
| Omaxe | none | **no** |
| MEP | none (2021 fails U2; 2020, 2022 fail cond 2) | **no** |
| Adani Ports | (2021, 2022) and (2020, 2021), (2019, 2020) pass cond 1/2; needs E1 ≤ 2023-03-31 for 2021; verified E1 = 2023-05-30 | **no** |
| FSC | none: 2019 fails cond 2 (7.918); 2021 fails U2/cond 2; 2020 alone has E1 20 days too early | **no** |
| PFS (out-of-lane) | (2020, 2021) if E1 ∈ [2021-09-30, 2022-03-31]; (2021, 2022) if E1 ∈ [2022-09-30, 2023-03-31] — **unresolved**, see §3.4 | **at most one** |

At most **one** double-carrier (PFS, unresolved) exists; the shape requires two. Even if PFS
resolved favourably (2 name-dates) plus every remaining single passed (FLFL 2020, Adani 2022), that
is one double + two singles — at most 4 name-dates as 2+1+1 over three companies, short of the spec's
5 as 2+2+1. §8.2:
"if the pre-reg set cannot supply 5 name-dates meeting all three pre-conditions … the run does not
proceed — it is VOID."

### 3.4 Per-name-date certification rows (36 name-dates: 9 companies × 2019–2022)

Legend: **Cond 1** = U2 (FY EPS sign, consolidated named basis; ✓ if > 0) — U1 basis is named
(screener consolidated, vendor post-action series); the audited÷sourced ratio report and U3 are
Phase-D. **Cond 2** = P_d0 ≤ 2.0 × P_G1 (frozen `engine_v4.anchor`, computed by
`fill_plausibility_firewall.py`; `fill_plausibility_results_r2.json`). **E1 reached** = earliest
qualifying event on the tape I was able to verify (engine-consistent reading, §3.2); "—" = not
established. **Cond 3** = d0+6m ≤ E1 ≤ d0+24m; `n/e` = not evaluated (E1 unverified); PFS shows the
two candidate E1s as `x / y`. **Result** uses only what was verified:
FAIL = a frozen condition demonstrably fails; UNCERTIFIED = nothing demonstrably fails but a required
proof (first-ever tape, pinned E1) is incomplete, so it is **not** counted as certified.

| Name-date | FY | FY EPS (U2) | P_d0 | P_G1 | P_d0/P_G1 | Cond 2 | E1 reached | Window [d0+6m, d0+24m] | Cond 3 | Result |
|---|---|---|---|---|---|---|---|---|---|---|
| simplexinf_2019-03-31 | FY2018 | 22.81 ✓ | 179.85 | 280.62 | 0.641 | ✓ | <=2019-05-30 | 2019-09-30..2021-03-31 | N | FAIL (cond3) |
| simplexinf_2020-03-31 | FY2019 | 21.40 ✓ | 20.2 | 334.95 | 0.06 | ✓ | <=2019-05-30 | 2020-09-30..2022-03-31 | N | FAIL (cond3) |
| simplexinf_2021-03-31 | FY2020 | -56.14 ✗ | 30.95 | -275.19 | n/a (P_G1<0) | ✗ | <=2019-05-30 | 2021-09-30..2023-03-31 | N | FAIL (U2, cond2, cond3) |
| simplexinf_2022-03-31 | FY2021 | -82.13 ✗ | 41.65 | -544.55 | n/a (P_G1<0) | ✗ | <=2019-05-30 | 2022-09-30..2024-03-31 | N | FAIL (U2, cond2, cond3) |
| fel_2019-03-31 | FY2018 | 0.15 ✓ | 38.75 | -62.21 | n/a (P_G1<0) | ✗ | — | 2019-09-30..2021-03-31 | n/e | FAIL (cond2) |
| fel_2020-03-31 | FY2019 | 3.19 ✓ | 9.05 | -44.94 | n/a (P_G1<0) | ✗ | — | 2020-09-30..2022-03-31 | n/e | FAIL (cond2) |
| fel_2021-03-31 | FY2020 | -7.28 ✗ | 8.37 | -83.79 | n/a (P_G1<0) | ✗ | — | 2021-09-30..2023-03-31 | n/e | FAIL (U2, cond2) |
| fel_2022-03-31 | FY2021 | -24.66 ✗ | 6.68 | -173.33 | n/a (P_G1<0) | ✗ | — | 2022-09-30..2024-03-31 | n/e | FAIL (U2, cond2) |
| fconsumer_2019-03-31 | FY2018 | -0.14 ✗ | 45.1 | -5.04 | n/a (P_G1<0) | ✗ | 2020-07-27 | 2019-09-30..2021-03-31 | Y | FAIL (U2, cond2) |
| fconsumer_2020-03-31 | FY2019 | -0.03 ✗ | 7.75 | -5.96 | n/a (P_G1<0) | ✗ | 2020-07-27 | 2020-09-30..2022-03-31 | N | FAIL (U2, cond2, cond3) |
| fconsumer_2021-03-31 | FY2020 | -1.12 ✗ | 6.49 | -3.69 | n/a (P_G1<0) | ✗ | 2020-07-27 | 2021-09-30..2023-03-31 | N | FAIL (U2, cond2, cond3) |
| fconsumer_2022-03-31 | FY2021 | -2.43 ✗ | 5.9 | -2.95 | n/a (P_G1<0) | ✗ | 2020-07-27 | 2022-09-30..2024-03-31 | N | FAIL (U2, cond2, cond3) |
| flfl_2019-03-31 | FY2018 | 6.62 ✓ | 485.75 | 141.97 | 3.421 | ✗ | 2020-10-15 | 2019-09-30..2021-03-31 | Y | FAIL (cond2) |
| flfl_2020-03-31 | FY2019 | 9.71 ✓ | 130.6 | 192.23 | 0.679 | ✓ | 2020-10-15 | 2020-09-30..2022-03-31 | Y | UNCERTIFIED (first-ever tape incomplete) |
| flfl_2021-03-31 | FY2020 | -2.63 ✗ | 54.15 | 74.48 | 0.727 | ✓ | 2020-10-15 | 2021-09-30..2023-03-31 | N | FAIL (U2, cond3) |
| flfl_2022-03-31 | FY2021 | -46.26 ✗ | 39.95 | -132.06 | n/a (P_G1<0) | ✗ | 2020-10-15 | 2022-09-30..2024-03-31 | N | FAIL (U2, cond2, cond3) |
| omaxe_2019-03-31 | FY2018 | 4.59 ✓ | 206.2 | 49.39 | 4.175 | ✗ | 2020-04-03 | 2019-09-30..2021-03-31 | Y | FAIL (cond2) |
| omaxe_2020-03-31 | FY2019 | 2.68 ✓ | 154.55 | -18.43 | n/a (P_G1<0) | ✗ | 2020-04-03 | 2020-09-30..2022-03-31 | N | FAIL (cond2, cond3) |
| omaxe_2021-03-31 | FY2020 | -5.32 ✗ | 68.65 | -29.36 | n/a (P_G1<0) | ✗ | 2020-04-03 | 2021-09-30..2023-03-31 | N | FAIL (U2, cond2, cond3) |
| omaxe_2022-03-31 | FY2021 | -12.86 ✗ | 83.5 | -79.92 | n/a (P_G1<0) | ✗ | 2020-04-03 | 2022-09-30..2024-03-31 | N | FAIL (U2, cond2, cond3) |
| mep_2019-03-31 | FY2018 | 4.37 ✓ | 41.95 | -28016855.11 | n/a (P_G1<0) | ✗ | — | 2019-09-30..2021-03-31 | n/e | FAIL (cond2) |
| mep_2020-03-31 | FY2019 | 3.07 ✓ | 13.75 | -24943976.99 | n/a (P_G1<0) | ✗ | — | 2020-09-30..2022-03-31 | n/e | FAIL (cond2) |
| mep_2021-03-31 | FY2020 | -4.21 ✗ | 16.15 | 349.97 | 0.046 | ✓ | — | 2021-09-30..2023-03-31 | n/e | FAIL (U2) |
| mep_2022-03-31 | FY2021 | -4.18 ✗ | 18.6 | -98.53 | n/a (P_G1<0) | ✗ | — | 2022-09-30..2024-03-31 | n/e | FAIL (U2, cond2) |
| adaniports_2019-03-31 | FY2018 | 17.74 ✓ | 378.15 | 502.99 | 0.752 | ✓ | 2023-05-30 | 2019-09-30..2021-03-31 | N | FAIL (cond3) |
| adaniports_2020-03-31 | FY2019 | 19.27 ✓ | 251.3 | 451.7 | 0.556 | ✓ | 2023-05-30 | 2020-09-30..2022-03-31 | N | FAIL (cond3) |
| adaniports_2021-03-31 | FY2020 | 18.52 ✓ | 703.05 | 393.6 | 1.786 | ✓ | 2023-05-30 | 2021-09-30..2023-03-31 | N | FAIL (cond3) |
| adaniports_2022-03-31 | FY2021 | 24.58 ✓ | 743.25 | 375.27 | 1.981 | ✓ | 2023-05-30 | 2022-09-30..2024-03-31 | Y | UNCERTIFIED (first-ever tape incomplete) |
| fsc_2019-03-31 | FY2018 | 7.61 ✓ | 587.2 | 74.16 | 7.918 | ✗ | 2020-09-10 | 2019-09-30..2021-03-31 | Y | FAIL (cond2) |
| fsc_2020-03-31 | FY2019 | 15.35 ✓ | 115.8 | 148.79 | 0.778 | ✓ | 2020-09-10 | 2020-09-30..2022-03-31 | N | FAIL (cond3) |
| fsc_2021-03-31 | FY2020 | -1.31 ✗ | 69.95 | -47.6 | n/a (P_G1<0) | ✗ | 2020-09-10 | 2021-09-30..2023-03-31 | N | FAIL (U2, cond2, cond3) |
| fsc_2022-03-31 | FY2021 | -42.01 ✗ | 54.05 | -188.73 | n/a (P_G1<0) | ✗ | 2020-09-10 | 2022-09-30..2024-03-31 | N | FAIL (U2, cond2, cond3) |
| pfs_2019-03-31 | FY2018 | -1.56 ✗ | 15.91 | 52.31 | 0.304 | ✓ | 2022-03-03 or 2022-11-16 | 2019-09-30..2021-03-31 | N / N | FAIL (U2) |
| pfs_2020-03-31 | FY2019 | 2.87 ✓ | 7.86 | 29.44 | 0.267 | ✓ | 2022-03-03 or 2022-11-16 | 2020-09-30..2022-03-31 | Y / N | UNCERTIFIED (first-ever tape incomplete) |
| pfs_2021-03-31 | FY2020 | 1.71 ✓ | 18.15 | 23.27 | 0.78 | ✓ | 2022-03-03 or 2022-11-16 | 2021-09-30..2023-03-31 | Y / Y | UNCERTIFIED (first-ever tape incomplete) |
| pfs_2022-03-31 | FY2021 | 0.40 ✓ | 16.1 | 29.2 | 0.551 | ✓ | 2022-03-03 or 2022-11-16 | 2022-09-30..2024-03-31 | N / Y | UNCERTIFIED (first-ever tape incomplete) |

Zero rows are "certified". The five rows that survive cond 1–3 on the record reached
(flfl 2020, adaniports 2022, pfs 2020/2021/2022 on one or both E1 readings) stay UNCERTIFIED because
the first-ever proof for T1–T7 is incomplete (see per-company notes; "not found" is not proof), and —
per §3.3 — their certification could not rescue the set.

### 3.5 Per-company evidence, identity and what was searched

**(a) Identity (all).** Each is a listed NSE company at d0 with a March FY-end, parsed on the
consolidated screener view. Renamed/demerged-ticker mapping checked against prior company tokens
(77 companies; the prior set carries `fretail` = Future Retail): `simplexinf` (Simplex Infrastructures
Ltd, the listed parent — the HDFC MF disclosure names NCDs issued by Simplex Infrastructures Limited
itself, not a subsidiary), `fel` (Future Enterprises), `fconsumer` (Future Consumer Ltd, "erstwhile
Future Consumer Enterprise Ltd." per CARE), `flfl` (Future Lifestyle Fashions), `fsc` (Future Supply
Chain Solutions), `omaxe`, `mep` (MEP Infrastructure Developers), `adaniports` (Adani Ports & SEZ),
`pfs` (PTC India Financial Services; parent PTC India is **not** a candidate). None maps to a prior
token; FEL, FCONSUMER, FLFL and FSC are distinct listed legal entities from Future Retail (separate
symbols/CARE rating entities). `check_disjoint_v4_r2.py` (§4) confirms it mechanically.

**1. Simplex Infrastructures (SIMPLEXINF).** *Fetched and read:* HDFC MF update 12-Dec-2019 (PDF;
CARE cut the NCDs BB+ → D on 2019-12-11 "due to a recent instance of delay in repayment"; it
appends the 26-Nov-2019 note: CARE BBB → BB+ on 2019-11-25); the company's Annual Report 2019-20
(Directors' Report credit-rating table: CARE A−/Stable → A− Negative 2019-06-07 → BBB Negative
2019-08-14 → BB+ 2019-11-25 → **D 2019-12-10** [AR date; the HDFC note says Dec 11 — a one-day
discrepancy to be settled from CARE's own rationale PDF in Phase D, immaterial here]; Infomerics
IVR C 2019-12-16, D 2020-02-24; FY20 auditors' qualified opinions incl. IFC material weakness);
and the Annual Report 2018-19 (296 pp.), whose Directors' Report, *Boards' Explanation on
Auditors' Qualification* (report dated **30 May 2019**), states that joint auditor **S.R. Batliboi
& Co. LLP qualified** the standalone FY19 statements (old unbilled revenue, loans/advances,
receivables, retention monies, inventories and claims; the auditors "are unable to comment upon the extent of
recoverability of Rs.1,17,772 lacs") and that the consolidated statements carry the same qualifications ("All the
qualifications on Consolidated Financial Results are similar to that of Standalone"; the other joint auditor, H.S.
Bhattacharjee & Co., differed). That is a T2(b)
qualified opinion (MODERATE) dated ≤ 2019-05-30 < 2019-09-30 ⇒ **cond 3 FAILS for 2019; and it
predates d0 for 2020–2022.** The exact signing date of the audit report itself was not separately
extracted (the board report/results date is 30-May-2019; any date in FY19's audit cycle precedes
2019-09-30). bankrupt.com TCRAP (corroboration) returned 503; not relied on.
Cond 1: FY18 EPS 22.81, FY19 21.40 (✓); cond 2: 0.641 (2019), 0.060 (2020) (✓). **Both name-dates FAIL (cond 3).**

**2. Future Enterprises (FEL).** The CARE PDF (`felindia.in/pdf/Credit_Rating_30_September_2020_CARE.pdf`)
returned **HTTP 503 twice**; E1 (lead: 2020-09-30 CARE NCD C → D) is **unverified**. Irrelevant
to the outcome: `P_G1 < 0` at all four dates ⇒ **cond 2 FAILS everywhere** (frozen anchor).

**3. Future Consumer (FCONSUMER).** *Fetched and read:* CARE press release 2020-09-08 (PDF). Confirms
the lead: NCD INE220J07113 **CARE BB → D** for delay in interest and principal due 2020-09-05
(rationale: poor liquidity, COVID); bank facilities BB → C. Annexure-2 history: A (2017–Mar-20) →
A− 2020-05-15 → **BB 2020-07-27** (first sub-IG cut; MODERATE) → D 2020-09-08; no prior D. First-ever for
T1–T6 not searched (moot). **All four dates FAIL**: `P_G1 < 0` (cond 2) and consolidated FY18/19/20/21
EPS all negative (U2).

**4. Future Lifestyle Fashions (FLFL).** *Fetched and read:* CARE press release-cum-rationale
2020-11-11 (PDF). Confirms the lead: NCD INE452O07047 (₹350 cr, issued 9-Nov-2017) **BB → D**, put
option exercised, principal ₹100 cr + interest ₹30.93 cr unserviced on 2020-11-09; promoter
pledge 99.51 % (11-Sep-2020). Full rating history read: AA− Stable 2017-18 → AA− Positive
2019-12-24 → AA− Negative 2020-04-17 → A+ Negative 2020-05-12 → BBB (watch developing) 2020-08-13 →
**BB 2020-10-15** (first sub-IG; E1 on the engine-consistent reading) → **D 2020-11-11** (D-only E1).
Both lie in the 2019 and 2020 windows. **2019: FAIL (cond 2, 3.421). 2020: cond 1 ✓ (FY19 EPS
9.71), cond 2 ✓ (0.679), cond 3 ✓ on the rating tape — UNCERTIFIED:** no T1–T6 search was completed
(promoter-share pledge invocation — the tape records 99.51 % pledged —, SEBI/ED action, group
associate contagion vs. Future Retail, auditor events; CONSOLIDATED audit opinions FY18–FY20 were not
read), so first-ever is unproven. 2021: FAIL (U2, FY20 EPS −2.63; E1 precedes the window).

**5. Omaxe (OMAXE).** *Fetched and read:* CARE press release 2021-03-05 (PDF): first CARE **D** on
all bank facilities and FDs "due to delays in servicing of debt obligations due to stressed liquidity".
Annexure-2 history: BBB− Stable 2017-10-04, 2018-06-04 → BBB− Negative 2019-01-07 → **BB+ Stable
2020-04-03** (FY19-20 column empty ⇒ no other CARE action; this is the first sub-IG cut, MODERATE) →
D 2021-03-05. **All dates FAIL on cond 2** (2019: 4.175; 2020: `P_G1 < 0`; 2021/2022 `P_G1 < 0` and
U2). The lead's E1 for the 2020 date (2021-03-05) holds only on the D-only reading; it changes nothing.

**6. MEP Infrastructure (MEP).** The Acuité PDF (`acuite.in/…/24929-RR-20230717.pdf`) returned
**HTTP 403**; searches surfaced Acuité/CARE "issuer not cooperating" actions for MEP but **no
April-2022 Acuité action**; E1 (lead: 2022-04-18 "downgraded and issuer not cooperating") is **unverified**,
and, per the lead's own caution, not default-driven (§5.2 T7-SEVERE would not attach cleanly). **2021:
VETOED-DATA — U2 FAIL (FY20 consolidated EPS −4.21)**, the only date with cond 2 ✓ (0.046). **Dropped on
input conditions alone**; all other dates fail cond 2 (`P_G1 < 0`) or U2.

**7. Adani Ports and SEZ (ADANIPORTS).** The Hindu BusinessLine URL is not fetchable from this
environment. *Fetched and read:* BusinessToday 2023-05-31 (updated 06-01): Deloitte issued a
**qualified** opinion on FY23 (could not verify three counterparties as unrelated; "evaluation
performed by the group does not constitute sufficient appropriate audit evidence"); APSEZ announced FY23
results on **2023-05-30** (BusinessToday 2023-05-30). The lead's **2023-05-03 is a date error.** The
FY23 annual report itself was **not** read (qualified vs emphasis-of-matter is asserted by press only ⇒
**WEAK-SOURCE**, tier 3); Deloitte's resignation (August 2023) is later. Scoring dates: 2019–2021 **FAIL cond 3**
(E1 after every window end ≤ 2023-03-31). **2022-03-31:** cond 1 ✓ (FY21 EPS 24.58), cond 2 ✓ at
**1.981 — 0.019 inside the 2.0 boundary** (knife-edge; β and share-count conventions carried, no
re-tuning), cond 3 ✓ (2023-05-30 ∈ [2022-09-30, 2024-03-31]). **UNCERTIFIED:** first-ever not proven
(I found no SEBI/ED/SFIO/CBI *instrument* naming the company in 2022-09 … 2023-03 — SEBI's show-cause
notices to Adani group entities surfaced are dated 2024 — but "not found" is not proof; the
Jan-2023 short-seller report and the early-2023 Supreme Court proceedings were not graded as T1 because no agency instrument naming the company was located). **§8.1
category honesty:** the pre-registered criterion is "well-documented distress" *and* a dated
qualifying event inside the window. On the record reached (no payment default, no D, no insolvency
filing found; I did not search sub-IG rating actions for APSEZ), a governance/short-seller controversy
with a qualified audit opinion is **not** well-documented distress; I do not stretch the criterion.

**8. Future Supply Chain Solutions (FSC).** The mnacritique page was fetched (article date 2022-02-03):
"IDBI Trusteeship invoked shares … on behalf of debenture holder Aion Capital on **September 10, 2020**";
promoters "now own a 23 % stake"; IDBI Trusteeship took ~24 %. The Trendlyne SAST record returned **HTTP 405**
and no exchange SAST filing was retrieved — so the invocation date is **press-confirmed only** (T3(b),
SEVERE by type, capped MODERATE as WEAK-SOURCE until the SAST filing is pinned). **2019: FAIL (cond 2,
7.918). 2020: cond 2 ✓ (0.778) but cond 3 FAILS** (E1 2020-09-10 < window start 2020-09-30). 2021/2022 FAIL (U2, cond 2).

**9. PTC India Financial Services (PFS) — out-of-lane lead, pursued because the table yields < 5.**
*Re-fetched and read:* (i) PTC India Ltd's 2022-11-24 consolidated-results filing (financialreports.eu
mirror of the exchange RNS, auditor T R Chadha & Co LLP): records that "the Independent Auditors of PFS have
given a **Qualified Opinion** on the separate audited statement of financial results of PFS for the quarter and year
ended March 31, 2022 vide their report dated **November 16, 2022**"
(MSKA; T2(b), MODERATE); (ii) independent directors Vikamsey, Mathew and Nayar resigned **2022-01-19**
citing governance lapses (Business Standard/Moneylife/Swarajya — press); (iii) SEBI **denied PFS permission to hold a
board meeting** without independent directors (Business Standard, dated ≈ 2022-03-03; press only; SEBI's
letter not located). **Classification:** director resignations are *not* a §5.1 type — the sweep's "T1-first"
label is wrong; a SEBI refusal/direction might be a T1 "interim direction … naming the company" (MODERATE) but rests on press
(WEAK-SOURCE) and is contested; the rating watch (Jan-2022) and an RBI inspection are not §5.1 events
(IG ratings; RBI is not a T1 agency; logged WATCH at most). So **E1 ∈ {≈2022-03-03 contested, 2022-11-16
verified}**, which decides whether PFS could carry (2020, 2021) or (2021, 2022) — unresolvable without the
exchange filings. U2: 2019 ✗ (FY18 EPS −1.56); 2020–2022 ✓. Cond 2 ✓ at all four dates on the financial
(inverse excess-return) anchor. **UNCERTIFIED; at most one double-carrier in the whole pool.** D6 CAMEL
inputs (CAR, GNPA, cost-to-income, ROA, leverage) would come from the BSE/NSE filings in Phase D.

### 3.6 Tooling honesty (what this environment could and could not reach)

Reached and read in full: CARE PDFs (Future Consumer, FLFL, Omaxe), HDFC MF PDF, Simplex ARs (2018-19,
2019-20) from the company site, PTC India's exchange filing mirror, screener.in (tables, price series).
**Not reachable:** felindia.in (503 ×2), acuite.in (403), thehindubusinessline.com (blocked), bankrupt.com
(503), Trendlyne (405), and — as before — the NSE/BSE announcement archives, SEBI/IBBI order lists and
rating-agency default lists. Where a lead's source could not be re-fetched, its row says so; nothing
is certified on an un-re-fetched source. Web search is US-only. PDFs were text-extracted with `pypdf`
installed into the session scratch directory (not the repo).

### 3.7 Restated from the spec (verbatim)

> **Exercise condition:** genuine exercise of the distress screen requires decisional on **≥3** of
> the 5 name-dates (= §1 leg (a′)).
> **Void rule:** if the pre-reg set cannot supply 5 name-dates meeting all three pre-conditions
> (certified pre-run), **the run does not proceed — it is VOID**, not weakened, not reinterpreted,
> not "underpowered but counted." If the run proceeds and the screen is decisional on <3, the
> blow-up leg is recorded as **UNTESTED** and the run is VOID — an unexercised 0 is not a PASS of
> leg (a). Both cases require a new pre-reg + a new set (fresh zero-overlap vs all six prior sets,
> §8.3).

(The "six prior sets" of that sentence counts a v4 set that was never frozen; the priors here are the
**five** — in-sample plus v3.8–v3.11 — as the task states.)

## 4. Overlap proof (§8.3)

No v4 set is frozen, so the §8.3 25/13 shape assertion is not applicable and `DISJOINT: True` is **not**
the §8.3 gate for a set. `check_disjoint_v4_r2.py` verifies the **R2 candidate pool** (9 companies / 36
name-dates) against the five prior sets, inheriting the prior lists **by import**
(`check_disjoint_v311` → `check_disjoint_v310`; nothing retyped), asserting 25/50 and 13/25 for the
priors and all candidate scoring dates ≥ 2019-03-31. The PR #12 script `check_disjoint_v4.py` was reused
unmodified for its own pool (57 companies / 171 name-dates; it still prints `DISJOINT: True`); it does not
contain the five new symbols (OMAXE, MEP, ADANIPORTS, FSC, PFS), hence the sibling script. A future
pre-reg runs the full §8.3 procedure on its own frozen set.

Verbatim output of `python3 validation/v4_oos/check_disjoint_v4_r2.py`:

```
v4 frozen set: NONE (R2 Gate 1 failed -> VOID; s8.3 25/13 shape assertion not applicable)
R2 candidates examined: 9 companies / 36 name-dates; scoring dates 2019-03-31 .. 2022-03-31
candidate companies: ['adaniports', 'fconsumer', 'fel', 'flfl', 'fsc', 'mep', 'omaxe', 'pfs', 'simplexinf']
prior in-sample: 25 companies / 50 name-dates
  company overlap:   []
  name-date overlap: []
prior v3.8: 13 companies / 25 name-dates
  company overlap:   []
  name-date overlap: []
prior v3.9: 13 companies / 25 name-dates
  company overlap:   []
  name-date overlap: []
prior v3.10: 13 companies / 25 name-dates
  company overlap:   []
  name-date overlap: []
prior v3.11: 13 companies / 25 name-dates
  company overlap:   []
  name-date overlap: []
union of prior sets: 77 companies / 150 name-dates
union company overlap:   []
union name-date overlap: []
DISJOINT: True
```

## 5. Data / runner / log commit order

No data, runner, log or result JSON exists for a run. Committed here, additions only under
`validation/v4_oos/`: this document; `fill_plausibility_results_r2.json` (emitted fields only — the
`OUT_FIELDS` of the existing firewall script; the scratch screener cache stays outside the repo);
`check_disjoint_v4_r2.py`. The firewall script, `check_disjoint_v4.py` and the PR #12 results are
unchanged. A future run commits data → runner → logs before any result JSON.

## 6. Audit checklist

- [ ] Spec SHA-256 equals the §1 value and the `test_constants.py` pin.
- [ ] Frozen-tree diff empty: `git diff 47d9dbf HEAD -- engine engine_v4 specs validation/v3_6 validation/v3_7 validation/v3_8_oos validation/v3_9_oos validation/v3_10_oos validation/v3_11_oos validation/v4_oos/V4_OOS_PREREG.md validation/v4_oos/fill_plausibility_firewall.py validation/v4_oos/fill_plausibility_results.json validation/v4_oos/check_disjoint_v4.py` prints nothing.
- [ ] Only files under `validation/v4_oos/` were added; exactly three.
- [ ] `check_disjoint_v4_r2.py` re-run independently reproduces the §4 output.
- [ ] Re-running `python3 validation/v4_oos/fill_plausibility_firewall.py <scratch> SIMPLEXINF,FEL,FCONSUMER,FLFL,OMAXE,MEP,ADANIPORTS,FSC,PFS 2019,2020,2021,2022 <out.json>` reproduces the P_d0/P_G1 columns of §3.4 (screener pages drift slowly; expect identical to the printed precision on the same day).
- [ ] The §3.4 EPS column equals the `EPS in Rs` row of each candidate's screener consolidated profit-loss table at the listed FY.
- [ ] Every evidence claim in §3.5 marked "fetched and read" is re-verifiable from the URL named; every "press only"/"unverified" tag is honoured (none is treated as certified).
- [ ] No distress/usability(U3)/event/exit/aggregation module was imported or run; no forward price (> d0) enters any emitted number; no result JSON with fills, vetoes, exits or aggregates exists in the change.

## 7. Phase-D input specifications and templates

Not repeated: no name-date is frozen. The per-name-date templates in `V4_OOS_PREREG.md` §7 (distress-screen
input spec with the 63-day PIT rule, usability input spec, event-log template, §5.1 source hierarchy) stand
as written and apply to a future set unchanged. Two additions learned here: (i) for any T7-anchored E1,
read the agency's **full rating-history column** (Omaxe and FLFL carried earlier sub-IG cuts that move
E1), and (ii) read the **consolidated and standalone audit opinions back to FY18/FY19** from the annual
report — Simplex's FY19 qualified opinion was the first-ever event and was invisible to press searches.

## 8. Firewall and void/FAIL triggers (§8.4 item 7), pre-stated

| Trigger | Status |
|---|---|
| (i) fewer than 5 name-dates certifiable on the three §8.2 pre-conditions → **VOID before run** | **TRIGGERED** (0 certified; shape 2+2+1 infeasible, §3.3) |
| (ii) any blow-up fill → leg (a) FAIL | not applicable (no run) |
| (iii) decisional count < 3 → UNTESTED → VOID | not applicable (no run) |
| (iv) any mid-run rule change → VOID | not applicable (no run) |

## 9. Dead-design non-resurrection attestation (§8.4 item 8; spec §10 kill list)

No §10 kill-list design is used. The only valuation computed is the v4 §2 inverse-DCF hurdle structure,
solely to read `P_G1` for the §8.2(2) band (a new mechanism with its own spec rationale, not the killed
level comparison); the financial-class anchor was used for PFS only.

| §10 component | Touched? |
|---|---|
| Frozen DCF entry anchor (level comparison) | No (see above). |
| Event-only GEV as the blow-up-leg mechanism | No. No event lane was run; the event tape is read only to date E1 (§8.2(3)). |
| QFV 1.00× entry tier and its four quality conditions | No. |
| GEV-exercise filter that omits usability | No. Usability is not omitted by design: U1/U2 are checked as input conditions (adjudication 1); U3 is deferred to Phase D. |
| Type 7 as a standalone codified veto | No. T7 appears as one of seven §5.1 types in the E1 reading (§3.2). |
| Usability check (b) | No. |
| 15 %-hurdle price reporting | No. |
| Financial-variant usability exemption | No (PFS faces U1–U2 like everyone). |
| Margin fade as a quality signal | No (the anchor uses the spec's flat trailing-5FY margin). |
| Beneish/accruals as fraud screens; Piotroski-as-fraud; dividend cuts as distress; promoter buying as a positive | No. |
| Own-multiple anchor, Gate M, Guardrail V | No. |

No threshold, band, cutoff, bar leg or parameter was changed; no parameter grid was run; no
same-set re-run (the four names shared with the first attempt — Simplex, FEL, FCONSUMER, FLFL — were
re-evaluated from sources; the anchor figures for 2019–2021 reproduce its results exactly).

## 10. Disclosures and leads for the next pre-reg (nothing here amends the spec)

1. **Shape is the binding constraint, not data access.** With cond 2 knife-edged against levered
   balance sheets (23 of the 57 first-attempt candidates had non-positive `P_G1` on all three dates) and E1 needing a
   ≥ 6-month-clean pre-history, double-carriers are rare. A future pre-reg should **search for
   double-carriers first** (E1 in [2020-09-30, 2021-03-31], [2021-09-30, 2022-03-31] or
   [2022-09-30, 2023-03-31], cond 1–2 passing on consecutive dates) before anything else.
2. **Spec wording gap (for Bablu; not acted on).** §5.1 T7 says "to 'D'", §5.2 and `events.py` also grade a
   sub-IG cut MODERATE. I applied the engine-consistent reading and reported D-only alongside; no verdict
   here depends on it. A one-line confirmation would remove the ambiguity for the next set.
3. **Director resignations** are not in the §5.1 taxonomy (T2 = auditors). If the intent is to count them,
   that is a spec change; it was not assumed.
4. **Knife-edge:** Adani Ports 2022 cond 2 = 1.981 vs the 2.0 band. Not re-tuned.
5. **PFS** is the one name whose E1 (≈2022-03-03 contested vs 2022-11-16 verified) determines which dates it
   could carry; pinning it needs the SEBI letter / exchange filing, which this environment cannot reach.
6. **Leads still worth a proper-source pass (non-binding):** FLFL 2020 and PFS (2020–2022) are the only rows
   where nothing yet fails; both need full T1–T7 first-ever tapes from exchange filings. Adani Ports'
   §8.1 category is doubtful.
7. Branch note: the task named `claude/v4-oos-prereg-r2`; work was done and pushed there.
