# v3.7 DCF Revalidation — 2026-09-23

**Verdict: FAILS the live bar.** 3 of 4 criteria pass. The failure is structural and does not depend on any unknown: winner fills reach at most 2 names vs the required 3.

| Bar for live (unchanged) | Result | |
|---|---|---|
| (a) Blow-up fills = 0 (hard) | **0** | **✓ PASS** |
| (b) Winner fills across ≥ 3 names | **1 (Persistent); max 2 even if Persistent 2021 fills** | **✗ FAIL** |
| (c) Aggregate to-T clearly positive | **4.82× mean** (6 exact legs) | **✓ PASS** |
| (d) Aggregate 24m ≥ 0.8× | **1.77× mean** (6 exact legs; no truncations) | **✓ PASS** |

v3 stays **NOT LIVE**.

## 1. Method

- **Frozen set:** the 26 usable name-dates from `V3_7_USABILITY_RERUN_20260923.md` §3. No re-admissions, no tweaks.
- **Engine rules (V3_7_DELTA.md):** own-multiple anchor retired; entry = v3.2 DCF three-tier for every name (ACC −12.5%, INV −30% of DCF fair value); E1 benchmark = DCF fair value; Gate M and Guardrail V retired (both were recorded-only in v3.6, never fed back into the engine, so their retirement changes nothing mechanically).
- **Reproduction status — read this before the numbers.** The bundle's `inputs/` directory is missing (noted in `AUDIT_V36.md`), so `calib_v36.py` cannot be re-run end-to-end: Q, DCF fair values, gates and the P floor all need the scored input JSONs. Instead this revalidation is a **DCF-only counterfactual reconstruction** on top of v3.6's audited `outputs_v36.json`:
  - **Exact carry-over (provable):** every fill v3.6 tagged `anchor: dcf` used the DCF trigger as its effective trigger. Retiring the anchor leaves DCF triggers, DCF fair values, eligibility inputs and fill weeks **bit-identical** — these 6 legs are v3.7 fills by construction, not by approximation.
  - **No-new-fills theorem (provable):** under DCF-only, every trigger is ≤ its v3.6 combined trigger (`max(DCF, multiple)`), and eligibility can only narrow (armed eligibility additionally requires entry usable; Q is anchor-independent — re-anchoring touches D1/D4, i.e. P dims only). Any name-date with no v3.6 fill and zero P-floor blocks therefore has no v3.7 fill. Verified name by name.
  - **Recomputed (trigger mechanics exact; P floor assumed):** the 7 legs v3.6 tagged `anchor: multiple`. The fill loop was replicated verbatim from `calib_v36.py` (quarterly basis rescaling, vintage = opening scoring date per v3.6 §4 — DCF triggers are quarter-invariant for a fixed vintage since `prep()` never touches DCF inputs). Validation: with v3.6's combined triggers the replication reproduces the exact v3.6 fill dates wherever the P floor didn't bind (hero, lupin: exact match). The P floor at recomputed fill prices needs the engine + inputs and is **flagged, not assumed**, per leg.
  - **Not computable:** `persistent_2021-03-31` and `mnm_2016-03-31` (excluded in v3.6, no recorded fills; DCF fair value and Q unknowable without inputs). Stated as unknown — no numbers invented.

## 2. Per-name fill table (frozen 26, DCF-only)

Tiers: ACC = accumulate leg, INV = invest leg. Outcomes are price ratios (basis-free).

| Name-date | Bucket | Leg | Fill date | Entry basis | to-T | 24m | Status |
|---|---|---|---|---|---|---|---|
| persistent_2019-03-29 | winner | ACC | 2019-04-05 | DCF 643.41 | **12.72×** | 3.12× | exact carry-over |
| persistent_2019-03-29 | winner | INV | 2019-04-05 | DCF 514.73 | **12.72×** | 3.12× | exact carry-over |
| wipro_2015-03-31 | mediocre | ACC | 2015-04-01 | DCF 1080.95 | 0.77× | 0.81× | exact carry-over |
| wipro_2015-03-31 | mediocre | INV | 2015-04-01 | DCF 864.76 | 0.77× | 0.81× | exact carry-over |
| wipro_2017-03-31 | mediocre | ACC | 2017-04-07 | DCF 848.78 | 0.96× | 1.37× | exact carry-over |
| wipro_2017-03-31 | mediocre | INV | 2017-04-07 | DCF 679.03 | 0.96× | 1.37× | exact carry-over |
| lichf_2018-03-31 | mediocre | ACC | 2020-03-13? | DCF 358.13 | 1.50×? | 1.67×? (15.4m, trunc) | **P floor unverifiable** |
| lichf_2018-03-31 | mediocre | INV | 2020-03-20? | DCF 286.50 | 1.87×? | 2.08×? (15.2m, trunc) | **P floor unverifiable** |
| hero_2018-03-31 | mediocre | — | no fill | DCF trg never reached | — | — | exact (anchor artifact removed) |
| lupin_2017-03-31 | mediocre | — | no fill | DCF trg never reached | — | — | exact (anchor artifact removed) |
| symphony_2018-03-31 | mediocre | — | no fill | DCF trg never reached | — | — | exact (anchor artifact removed) |
| persistent_2021-03-31 | winner | ? | unknown | inputs missing | ? | ? | **not computable** |
| mnm_2016-03-31 | mediocre | ? | unknown | inputs missing | ? | ? | **not computable** |
| piind_2016-03-31 | winner | — | no fill | DCF trg 210.38 never reached (min ~561) | — | — | exact (16 wks P-blocked vs rescaled mult trigger; DCF trigger never in range) |
| all other 16 name-dates | — | — | no fill | — | — | — | exact (no v3.6 fill, 0 P-blocks) |

What the anchor retirement actually did to the 7 anchor-generated v3.6 legs: **6 of 7 vanish** — Hero (1.00×/1.13×), Lupin (0.39×/0.41×) and Symphony (1.54×) never reached their DCF triggers at any week; their v3.6 fills were pure anchor artifacts. LIC Housing's two legs relocate to the COVID-crash weeks of March 2020 **if** the P floor passes there (v3.6's fill sat exactly on the floor at P=6.00, and this name had 64 P-blocked weeks — the floor binds hard here).

## 3. Live-bar verdict

Aggregates equal-weighted per leg, as-judged (v3.6 convention).

| Criterion | Exact-6 legs | + lichf if P passes | Verdict |
|---|---|---|---|
| (a) Blow-up fills = 0 | 0 (vakrangee_2015, yesbank×2: no fills, airtight) | 0 | **PASS** |
| (b) Winner names ≥ 3 | 1 (Persistent) | 1 | **FAIL** — ceiling is exactly 1 |
| (c) to-T positive | 4.82× mean / 0.96× median | 4.03× mean | **PASS** (robust either way) |
| (d) 24m ≥ 0.8× | 1.77× mean / 1.37× median | 1.79× mean | **PASS** (robust either way) |

On (b): the 10 winner name-dates in the frozen set are piind×2, tataelxsi_2017, bajfin×2, astral×2, persistent_2019, persistent_2021, safari_2020. Only persistent_2019 fills (DCF). Of the rest: tataelxsi_2017, bajfin×2, astral×2, safari_2020 and piind_2018-03-31 have no v3.6 fill and zero P-blocks, so DCF-only cannot fill them (triggers only move down). piind_2016-03-31 had 16 accumulate weeks blocked by the P floor — but against the quarterly-rescaled own-multiple trigger; its DCF ACC trigger (₹210.38) was never reached (minimum input-basis price in the 2-year entry window ≈ ₹561), so no DCF fill is possible there either. persistent_2021 has no fill record (excluded in v3.6) — but it is the same company as persistent_2019, so even a fill could not add a winner NAME. **Exactly 1 winner name < 3 under every scenario.** The failure is not a data gap; it is the set.

*Correction 2026-09-23: this section originally claimed the other eight winner dates had zero P-blocks (false — piind_2016-03-31 had 16 accumulate weeks blocked) and that the ceiling was 2 via a persistent_2021 fill (false — same company as persistent_2019). The no-fill conclusions stand; the reasons are corrected above. The failure is worse than previously stated.*

On (d) truncations: the exact-6 legs have **zero** truncated 24m outcomes (v3.6's lichf 22.3m / symphony 14.9m truncations belonged to anchor-generated legs; symphony's is gone, lichf's is flagged above). The ≥0.8× bar passes with and without lichf.

## 4. v3.2 vs v3.6 vs v3.7 — DCF comparison

| | v3.2 (DCF entry, original validation) | v3.6 DCF-anchored legs | v3.7 DCF-only (this run) |
|---|---|---|---|
| DCF legs / names | Persistent T−5 ×2 (12.72×) | 6 legs / 2 names | 6 legs / 2 names (+lichf ×2 uncertain) |
| to-T mean | 12.72× (Persistent only) | 4.82× | **4.82×** |
| 24m mean | 3.12× (Persistent only) | 1.77× | **1.77×** |

Dropping the anchor changes DCF behavior **not at all, by construction** — verified, not assumed: the 6 DCF-tagged v3.6 legs are bit-identical under v3.7. The anchor's removal only deletes its own 7 legs (6 vanish, 1 uncertain). The "DCF keeps working" finding from v3.6 §7 is unchanged.

## 5. Caveats

1. **No full engine rerun was possible** — `inputs/` is absent from the bundle. DCF-tagged fills are provably identical; multiple-tagged legs were recomputed with replicated trigger mechanics; the P floor at recomputed prices and all of persistent_2021/mnm_2016 are honestly unknown. Nothing in §2 marked `?` should be treated as a result.
2. **Eligibility assumed constant per vintage** for recomputed legs (v3.6 recorded fills there, so it held; Q and evidence fields are quarter-invariant for a fixed vintage — documented, not verified).
3. **persistent_2021 explicitly unverified.** Its DCF fill — the largest-winner leg the v3.7 usability fix was built to recover — cannot be confirmed without the scored inputs. The (b) verdict does not depend on it.
4. **Neutral judgement not computed** (needs input dicts for `neutralise()`); the bar was evaluated as-judged, matching v3.6.
5. **Price-basis anomalies** (audit caveat 2: up to 101.85× input-vs-series mismatch) are harmless here — fill decisions are basis-invariant and outcomes are price ratios.
6. **E1 benchmark reversion** (anchor FV → DCF FV) affects test scoring, not fills or outcomes; no recomputation needed.
7. lupin_2017's series-staleness caveat from the usability rerun is moot — Lupin has no v3.7 fills.

## 6. What would change this verdict

Only a third out-of-sample set with more usable winner name-dates. Within this set the (b) failure is arithmetic: 10 winner name-dates, 8 provably unfillable under DCF-only, 1 unknown. No threshold, band or gate may be touched to fix it — per V3_7_DELTA §5, a failure returns to the spec document, not the parameter grid.
