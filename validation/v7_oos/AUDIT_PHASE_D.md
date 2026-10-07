# v7 Phase-D Audit — PASS, engine LIVE (2026-10-07)

## Chain
- e8e83ba: Amendment 1 frozen (bar (a′) 3/4→2/2, set 24→22).
- Assembly: coordinator + 3 workers → 22/22 inputs.
- Parent audit: securkloud ratio 2.047 adjudicated ACCEPT (trigger met in-window
  2018-07-20; pre-condition purpose satisfied); blow-up E1 events mapped to
  closed taxonomy (gitanjali→T1 SEVERE, securkloud→T2 SEVERE).
- 44e8236: inputs frozen. First locked run: 19/22 VETOED-DATA (assembly gaps).
- a760256: Amendment 2 (data completion, closed scope) + computability-gate
  standing rule + phase-d-computability-gate skill.
- Data completion: 75/75 fields, 0 unretrievable. Gate: 20/22 → W4 fixed KVB
  casa_pct (bank L-metric) → gate 22/22 PASS.
- Inputs re-frozen. Second locked run (frozen engine_v6, one-shot).

## Locked run
- engine_tree d5ebd2efd0609ef7d90cc675bdeeb64e392d86a6 (matches frozen).
- 22/22 executed exactly once. Results in phase_d_results/.

## Bar scoring (leg-weighted means, price return only, §6.4)
- (a) 0 blow-up fills — both blow-up legs BLOCKED by distress veto → PASS.
- (a′) 2/2 decisional — gitanjali VETOED-DISTRESS:E3 (E3+E4 trips, tiers
  G1/G2 touched, first touch 2016-04-01); securkloud VETOED-DISTRESS:E1
  (E1 trip, tiers touched, first touch 2018-07-20) → PASS.
- (b) 4 winner companies filled (granules, karurvysya, nationalum, recltd),
  14 filled legs → PASS (≥3).
- (c) aggregate to-T +261.6% → PASS (clearly positive).
- (d) aggregate 24m 1.83× → PASS (≥0.8×).
- Mediocrity fills: 0 (informational).

## Verdict: PASS — engine_v6 is LIVE.

## Disclosures
- E6 unexercised on this set (0 trips; both blow-ups E6-impossible by
  construction: CFO>0). Certification deferred, not abandoned (Amendment 1).
- Winner returns skew toward trough-derated cyclicals/PSU re-rating (sweep
  §noted). The bar measures what it measures; no reinterpretation.
- Securkloud ratio 2.047 vs 2.0 pre-condition: parent-adjudicated ACCEPT,
  documented above. Trigger met in-window; decisionality genuine.
- Tier-2 pledge sources (trendlyne) used where tier-1 unreachable; flagged
  per-field. KVB cost_to_income: headline 58.16 (as-filed). REC
  cost_to_income: computed via documented formula.
