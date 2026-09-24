# EPS forensics — Brightcom FY20 & Persistent FY21
**2026-09-23 · Musey · reconciled audited annual reports vs Screener implied TTM EPS**

## Question
The v3.6 usability test excluded 18/50 name-dates on EPS-basis drift (Screener TTM
implied EPS vs independently sourced FY EPS > ±15%). Which source is wrong, and why —
stale TTM, restatements, or share-count changes?

## Method
- Extracted audited consolidated EPS from the annual reports held in
  `annual_reports/` (pdftotext + manual verification of the P&L and EPS notes).
- Recomputed Screener implied TTM EPS = price ÷ PE from the bundle's weekly
  `pe_series/*.csv` at the usability check dates.
- Cross-checked Persistent's corporate actions via web (split/bonus history).

## Finding 1 — Brightcom FY20: Screener's data was garbage (vendor error)
| Source | FY20 EPS | Basis |
|---|---|---|
| Audited consolidated (annual report, PAT ₹440.1 cr ÷ 47.6 cr shares) | **₹9.24** | as-filed (pre-bonus) |
| Engine's sourced input (₹440.10 cr ÷ 99.2191 cr bonus-adjusted shares; documented in the project inputs) | **₹4.44** | post-bonus |
| Screener implied TTM at +150d (2021-01-15: 3.94 ÷ 17.1) | **₹0.23** | post-bonus (Screener-adjusted) |

- Like-for-like discrepancy: ₹4.44 ÷ ₹0.23 ≈ **19.3×**
  (₹9.24 ÷ ₹0.48 on the as-filed basis — same 19.3×).
  *Correction 2026-09-23: this doc originally reported 40×, which mixed
  the as-filed ₹9.24 with the adjusted ₹0.23 — the basis factor 2.0833
  inflated the headline. 19.3× is the correct like-for-like figure.*
- No split, bonus, or restatement explains 19.3×.
- The Screener series itself is incoherent: implied EPS jumps 0.23 → 0.06
  overnight on 2021-02-12 (PE 15.0 → 61.7) with no commensurate price move —
  a vendor feed break, not economics.
- **Verdict: the usability test was right to exclude Brightcom. Genuine data
  defect on an illiquid small-cap.** (Resolved: the input's sourced FY EPS
  was ₹4.44 — audited PAT on bonus-adjusted shares — not the audited ₹9.24.
  The earlier ~₹4.26 back-solve from the rounded −94.6% gap was an unstable
  artifact of rounding, not a distinct source.)
- *Firmed 2026-09-24 (Claude re-check):* ₹4.44 is not a derivation at all —
  `brightcom_2020-08-21.json` in the project inputs carries `"eps_ttm": 4.44`
  as a stored field, reconciling two ways (440.10 ÷ 99.2191 = 4.4356;
  9.24 ÷ 2.0833 = 4.4353). Brightcom's exclusion is over-determined anyway:
  the v3.6 validation report already lists it at −95% on the EPS-basis drift
  check, failing usability independently of the 19.3× headline.

## Finding 2 — Persistent FY21: no data error; the test is miscalibrated
Corporate action (confirmed): **1:2 split, FV ₹10 → ₹5, ex-date 28 Mar 2024**
(plus 1:1 bonus Mar 2015). Screener's chart price series is retroactively
split-adjusted; its implied TTM EPS is therefore on the **post-split** basis.
The annual report EPS is on the **as-was** basis. The stored inputs' sourced
FY EPS was on the post-split basis.

| | FY19 | FY21 |
|---|---|---|
| Audited EPS (as-was basis) | 43.99 | 58.97 |
| ÷ 2 (split-adj) | 22.00 | 29.49 |
| Sourced FY EPS in input (post-split basis) | 20.94 | 28.26 |
| Ratio audited ÷ sourced | 2.10× | 2.09× |

The 2.09–2.10× ratio is **identical across two different years** — a constant
share-count basis difference (2.0 split × ~1.045 ESOP share-count drift), not
drifting data. A constant basis error cancels exactly in the anchor's
fair-price = EPS × median(P/E) math (prereg §1 says this explicitly).

The reported gaps recompute exactly from this model:
- 2019: implied 19.35 at +150d ÷ sourced 20.94 → **−7.6%** ✓ (USABLE)
- 2021: implied 35.95 at +150d ÷ sourced 28.26 → **+27.2%** ✓ (NOT USABLE)

Decomposing the +27.2%: on a like-for-like post-split basis, sourced 28.26 vs
implied TTM 35.95. The residual is **TTM-vs-FY timing, not data error**: at
+150d post-results the TTM is Q2FY21+Q3FY21+Q4FY21+Q1FY22 — Q1FY22 (blowout)
has replaced Q1FY21 (COVID-depressed). The Screener series itself is clean:
implied TTM steps up monotonically at every results date through FY21
(26.6 → 29.1 → 29.9 → 32.2 → 33.0 → 36.0), the signature of real earnings
growth, not vendor noise.

**Verdict: neither source is lying. The +27.2% is legitimate earnings growth
plus a constant share-count convention difference — both benign for the
anchor — yet the test excluded the single best winner observation
(Persistent 2021, the 12.72× DCF fill).**

## The test conflates three things; only one matters
1. **Genuine vendor data errors** (Brightcom 19.3×, APL's +50% off-results step)
   → correctly excluded.
2. **Share-count basis mismatches** (Persistent 2.09×) → constant, cancels in
   anchor math, harmless — but flagged.
3. **TTM-vs-FY timing on fast growers** (Persistent's +27%: TTM at +150d
   contains a new blowout quarter) → legitimate growth — but flagged.

## Proposed fix for the v3.7 usability check
1. **Normalize basis first.** Pull splits/bonuses 2010→T per name; restate the
   sourced FY EPS to the Screener series' (post-action) basis. Verify the
   audited÷sourced ratio is constant across years; document any residual
   convention factor instead of failing on it.
2. **Move check (a) to the results week.** Compare Screener-implied TTM in the
   week the FY results were declared (median over results-week..+21d), when
   TTM == that FY by construction — instead of +150d, which injects a quarter
   of growth into the comparison. Keep ±15%.
3. **Keep check (b)** (8% unexplained steps) unchanged.
4. Re-run over all 50 name-dates. Expected: Persistent 2021 re-admitted;
   Brightcom/APL stay out; borderline growers (Hero/ITC/Lupin T−5, Deepak,
   Navin, Safari, Trent) re-examined rather than auto-failed.

## Implication for v3.7
The anchor is retired, but the DCF entry also consumes EPS — and the widened
validation's "winner fills ≥ 3 names" bar needs usable winner observations.
**Re-run usability with the fixed check before freezing the v3.7 validation
set**; the recovered names (starting with Persistent 2021) directly change
the validation math.
