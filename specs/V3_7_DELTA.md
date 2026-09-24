# v3.7 spec delta — anchor retired, DCF entry only
**2026-09-23 · Bablu approved ("anchor retired") · v3 remains NOT LIVE until re-validation passes**

Base: `EQUITY_REVIEW_V3_SPEC.md` + engine v3.5. This document changes only what
it names; everything else carries over.

## 1. The own-multiple anchor is retired
- The v3.3 `multiple_anchor` path (entry from EPS_ttm × own 5-yr median P/E,
  Q ≥ 7 names) is **removed**. There is no Q-gating on entry anymore.
- Entry for **all** names reverts to the v3.2 `entry_block`: DCF-anchored
  three-tier — WATCH / ACCUMULATE at −12.5% / INVEST at −30% of DCF fair value
  (financial variant: supplied conservative central). This is the configuration
  that filled Persistent twice (v3.2 and v3.6), returning 12.72×.
- Rationale (v3.6 widened validation): the anchor admitted 4/10 winner
  name-dates vs 8/12 mediocrities, produced **zero** winner fills through its
  own triggers, and both its pre-registered repairs (Gate M, Guardrail V)
  failed out of sample without refit.

## 2. Consequential reversions
- **E1 benchmark**: v3.5's "fair value of the anchor that generated the fill"
  collapses to the DCF fair value (v3.2 behaviour) — there is no other anchor.
- **v3.4 re-anchoring**: the D1/D4 re-anchor-on-multiple-anchor path is dead;
  D1/D4 stay on the DCF basis. No other test moves.
- **Trigger rescaling asymmetry (stated explicitly, 2026-09-24):** the retired
  own-multiple trigger rescaled quarterly with EPS while the DCF trigger is
  fixed at the scoring date. "The DCF trigger was never reached" is therefore
  close to structural for any name that re-rated through the entry window —
  most winners. Same family as the §4 basis problem; logged, not patched.
- The 15%-hurdle price continues to be reported for continuity only, not used
  for entry (unchanged since v3.2).

## 3. Gate M and Guardrail V are retired, not refit
- Both were pre-registered with unchosen parameters and **failed out of
  sample** (Gate M blocked Wipro ~0.96× and passed Lupin ~0.39×; Guardrail V
  blocked both Persistent winner legs). No refit was performed — correct.
- Neither ships in v3.7. Neither may be resurrected without a new
  pre-registration document and fresh out-of-sample data.

## 4. Usability check fixed (from EPS forensics 2026-09-23)
The v3.6 check conflated vendor data errors with share-count basis mismatches
and TTM-vs-FY timing on growers, and excluded the best winner observation
(Persistent 2021) over legitimate earnings growth. The v3.7 check:
1. **Assert a common basis first — transform only the side that isn't on it.**
   Name the basis explicitly (e.g. post-2024-split). Pull splits/bonuses
   2010→T per name and check whether the sourced FY EPS is already on the
   Screener series' (post-action) basis — if it is (stored inputs are often
   already post-bonus/post-split), DO NOT restate it again. Restate only the
   side that is not on the named basis, and store every adjustment factor and
   corporate action (with ex-dates) as structured fields, not prose. Verify
   the audited÷sourced ratio is constant across years; document any residual
   convention factor (e.g. ESOP drift) instead of failing on it — and fix by
   preregistered rule which basis is authoritative (audited restated only for
   splits/bonuses), never by choosing whichever basis passes.
2. **Check (a′) at the results week, on the publication-dated (unlagged)
   series.** Compare Screener-implied TTM in the week the FY results were
   declared (median over results-week..+21d), when TTM == that FY by
   construction — not +150d, which injects a quarter of growth into the
   comparison. Note: the 63-day PIT lag used elsewhere shifts calendar dates —
   identify the results week from publication events (or the unlagged series),
   never from the lagged series' calendar position. Tolerance stays ±15%.
3. **Check (b) unchanged**: no implied-EPS step > 8% outside a results window.
- The DCF entry also consumes EPS, so this fix is load-bearing for v3.7, not
  just anchor archaeology.

## 5. Re-validation protocol (BLOCKING — v3.7 judges nothing live until this passes)
1. Re-run the fixed usability check over all 50 name-dates → recovered usable set.
2. Re-run the widened validation on the v3.7 engine (DCF entry only).
3. **Live bar (unchanged):** blow-up fills 0 (hard) · winner fills across
   ≥ 3 names · to-T aggregate clearly positive · 24-month aggregate ≥ 0.8×.
4. **Audit ordering is pre-registered (2026-09-24):** the frozen set and the
   ≥3-winner-names bar are not independent — rewritten §4 rules change which
   series are usable, which moves the eligible winner population. The bar is
   re-derived AFTER the usability audit, and the audit is one-shot:
   re-running usability after seeing which rule admits a name is re-fitting
   under another name. Ordering fixed here, before the re-run.
5. No threshold, band, or weight changes during re-validation; any failure
   returns to this document, not to the parameter grid.

## 6. Explicitly unchanged from v3.5
Two rates (15% hurdle / ~11% valuation) · Quality/Price split with honest
re-tiering · retrieval-aware forensics (G1: verified ≥ 7 AND pass rate ≥ 60%,
else WATCH) · C6 promoter-direction and A6 quarterly-trajectory tests · lite
credibility audit at SCREEN · threshold interpolation · bank/NBFC variant ·
all engine defects fixed per AUDIT.md.
