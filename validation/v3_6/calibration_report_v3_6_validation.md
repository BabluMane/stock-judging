# v3.6 Widened Validation — the out-of-sample result

**23 Sep 2026 · engine v3.5 unchanged (94 tests) · runner `calib_v36.py` · 24 weekly price + TTM P/E series, 12 newly retrieved and 12 extended to reach T · v3 stays not-live · threshold adjustment UNSPENT · no threshold, band or dimension weight changed.**

Everything scored here was fixed in `preregistration_v3_6.md` **before** these series were retrieved. Nothing below has been re-fitted.

---

## 1. Verdict: the validation FAILS the bar, and the diagnosis has moved again

| Bar for live (yours) | Result | |
|---|---|---|
| **Blow-up fills = 0 (hard)** | **0** — but see §5: only 3 blow-up name-dates survived the data test, so this condition has little power | **✓ (weakly)** |
| **Winner fills across ≥ 3 names** | **1 name** — Persistent, and it filled through the **DCF**, not the anchor. Zero winner names filled through the own-multiple anchor | **✗ FAILS** |
| **to-T aggregate clearly positive** | All fills 2.70× mean, but the **median is 0.96×** and the mean is entirely Persistent. **Own-multiple anchor fills alone: 0.89×** | **✗ for the anchor** |
| **24-month aggregate ≥ 0.8×** | All fills 1.32×; anchor fills alone 0.95× | **✓** |

**The own-multiple anchor does not work, and the widened set says why: the Q ≥ 7 universe rule is anti-selective.**

| Of the 25 scored name-dates | In the anchor universe (Q ≥ 7) | Outside it |
|---|---|---|
| **Winners (10)** | **4** — PI T−5 7.69, Tata Elxsi T−5 7.53, Bajaj Finance 7.27 ×2. **None filled.** | 6 — including **Persistent at Q 6.05, which filled via the DCF and returned 12.72×** |
| **Mediocrities (12)** | **8** — and 5 of them filled, every one through the anchor or the DCF | 4 |
| **Blow-ups (3)** | 1 — Yes Bank T−5 7.59, no fill | 2 |

A Q ≥ 7 name-date in this set is **twice as likely to be a mediocrity as a winner** (8 against 4). The gate the anchor sits behind is selecting the wrong population. And the single largest winner in the whole exercise sat at Q 6.05 — the anchor was never even offered it.

**Meanwhile the plain DCF path keeps working.** Persistent filled through the DCF in v3.2, and again here: 12.72× to T, 3.12× in 24 months. Six of the thirteen fills are DCF-anchored and they average 4.82× to T; the seven own-multiple fills average 0.89×.

---

## 2. Both pre-registered proposals fail out of sample

### Gate M — rejected (near-inert, and it blocks the wrong thing)

| | legs | to-T mean | mediocrity to-T |
|---|---|---|---|
| Without Gate M | 13 | 2.70× | 0.88× |
| With Gate M | 11 | 3.02× | 0.86× |

Gate M blocked exactly one name-date out of sample — **Wipro T−3, which returned 0.96× to T and 1.36× at 24 months**, i.e. a middling call, not a value trap. It passed all four anchor mediocrities, **including Lupin at 0.39×** — the clearest value trap in either set, and the case M1 was designed around.

**M1's trend test does not separate.** The pre-registered form (EPS ≥ 0.875 × its own 36-month log-trend) is satisfied by essentially everything the anchor selects. As predicted in the pre-registration, that is itself the finding: the thesis condition — *multiple derating on intact fundamentals* — is true of nearly every fill, so it cannot be where the discrimination comes from. I am not adjusting the 0.875. An adjusted M1 would be a new hypothesis needing a third out-of-sample test, and there is no third set.

### Guardrail V — rejected decisively

It blocks **9 of 13 legs, including both Persistent legs**, taking winner fills to zero and the to-T aggregate from 2.70× to 0.67×. The in-sample case for V was that it removed weak mediocrity fills; out of sample it removes the only winner. That is what fitting to eleven mediocrity legs produces, and it is why V was kept secondary rather than folded in.

---

## 3. Fills — both horizons, full outcome windows

Every outcome window below reaches T; the truncation that distorted the first pass of this run (11 of 13 fills cut short) was fixed by extending all 24 series.

| Bucket | Name-date | Leg | Fill | Anchor | P | Gate M | V | **to T** | **24m** |
|---|---|---|---|---|---|---|---|---|---|
| **winner** | Persistent T−5 (Q 6.05) | ACC + INV | 2019-04-05 | **dcf** | 6.86 | PASS | BLOCK | **12.72×** | **3.12×** |
| mediocre | Symphony T−3 | ACC | 2020-03-27 | multiple | 6.26 | PASS | BLOCK | 1.54× | 1.25× |
| mediocre | Hero T−3 | ACC | 2018-09-28 | multiple | 6.57 | PASS | PASS | 1.00× | 1.02× |
| mediocre | Hero T−3 | INV | 2019-03-22 | multiple | 6.57 | PASS | BLOCK | 1.13× | 1.20× |
| mediocre | Wipro T−3 | ACC + INV | 2017-04-07 | dcf | 6.69 | **FAIL** | BLOCK | 0.96× | 1.36× |
| mediocre | LIC Housing T−3 | ACC + INV | 2019-08-16 | multiple | 6.00 | PASS | ACC only | 0.87× | 0.97× |
| mediocre | Wipro T−5 | ACC + INV | 2015-04-01 | dcf | 6.57 | PASS | BLOCK | 0.77× | 0.81× |
| mediocre | Lupin T−3 | ACC | 2017-04-07 | multiple | 6.31 | PASS | PASS | **0.39×** | 0.56× |
| mediocre | Lupin T−3 | INV | 2017-04-28 | multiple | 6.31 | PASS | PASS | **0.41×** | 0.65× |
| **blow-up** | — | | **none** | | | | | | **✓** |

**Aggregates, equal-weighted per leg:**

| Set | legs | names | to-T mean | to-T median | 24m mean | 24m median |
|---|---|---|---|---|---|---|
| All fills | 13 | 6 | 2.70× | 0.96× | 1.32× | 1.02× |
| **Own-multiple anchor fills** | 7 | 4 | **0.89×** | 0.87× | 0.95× | 0.97× |
| **DCF-anchored fills** | 6 | 2 | **4.82×** | 0.96× | 1.77× | 1.36× |
| Winners | 2 | 1 | 12.72× | — | 3.12× | — |
| Mediocrities | 11 | 5 | 0.88× | 0.87× | 1.00× | 0.97× |
| Blow-ups | 0 | 0 | — | — | — | — |

The anchor is not destroying capital — its mediocrity fills come out roughly flat. It simply is not finding winners.

**Under neutral judgement:** anchor fills drop to 3 legs across 2 names (LIC Housing, Symphony), to-T 1.10×. Persistent still fills via the DCF at Q 6.12 and still returns 12.72×. **Winner fills through the anchor: zero on both bases.**

---

## 4. The harness staleness fix worked

Each simulated week now scores against the latest stored input whose scoring date is at or before that week (no lookahead). Every fill in the table above carries `vintage` equal to its own opening scoring date, meaning no fill occurred after the next vintage became available — so the v3.5 pathology (a 2016 bear case judged against a 2017 anchor) does not arise in any accepted fill.

**PI Industries remains the one case where it still bites, and it is now clearly not a harness artefact.** PI T−5 was 49% *above* its own median multiple at the scoring date; its price never fell to the ₹334 trigger. Its 16 in-zone weeks exist only because the refreshed anchor's fair value rose past a price that never fell — ₹381 → ₹934 in fifteen months. The P floor blocks all 16. On the merits that is the right answer: it is momentum, not margin of safety.

---

## 5. Data attrition is the second finding, and it is serious

**25 of 50 name-dates survived the pre-registered usability test. 25 did not.**

| Reason | Count | Names |
|---|---|---|
| EPS basis drifts > ±15% after results are public | 18 | APL Apollo ×2 (−28%, −33%), Navin ×2 (+78%, +29%), Safari T−5 (+108%), BHEL ×2, Deepak ×2, Brightcom T−3 (−95%), Trent T−5 (+34%), Persistent T−3 (+27%), Sun TV T−3, Bajaj Consumer T−5, Hero T−5, ITC T−5, Lupin T−5, Manpasand T−3 |
| No point-in-time EPS at the scoring date (negative or absent) | 4 | Brightcom T−5, Manpasand T−5, Vakrangee T−5, Trent T−3 |
| No series obtainable | 2 | DHFL ×2 — Screener now renders the entity as Piramal Capital & Housing and exposes no numeric company id, so the chart API cannot be called. Not substituted from elsewhere. |
| No usable post-results reference point | 1 | M&M T−5 |

**Consequences that must be stated plainly:**

- **The blow-up condition is nearly untested.** Three blow-up name-dates survived (Vakrangee T−3, Yes Bank ×2), and two of the three are outside the anchor universe anyway. "Blow-up fills = 0" is true but carries almost no evidential weight on this set. Brightcom, Manpasand and DHFL — the three most fraudulent names in the design — all dropped out.
- **The winner sample is halved.** Ten winner name-dates survived out of twenty, and the biggest-returning ones (APL Apollo, Navin, Trent) are exactly the ones Screener's EPS history cannot support.
- **Screener's TTM EPS is not reliable enough for this design.** Eighteen of fifty name-dates fail a ±15% agreement check against independently sourced FY EPS. That is a data-source problem, not a scoring problem, and no engine change fixes it.

---

## 6. Train / validate split, as pre-registered

| | Training set (15 Q ≥ 7 dates) | Validation set (this run) |
|---|---|---|
| Produced | Gate M, Guardrail V, the usability test | — |
| Result | Gate M near-inert in-sample; V looked favourable in-sample | **Gate M rejected · Guardrail V rejected** |
| Re-fitted after seeing this data? | **No** | — |

Nothing was tuned. Both proposals shaped on the training set failed to prove themselves, which is the outcome the split existed to detect.

---

## 7. Where this leaves v3 — my read

**The own-multiple anchor (v3.3–v3.5) has now failed three times, each time for a different reason, and the widened set gives the structural explanation: it is gated on Q ≥ 7, and Q ≥ 7 does not identify winners.** Four of ten winner name-dates clear it; eight of twelve mediocrities do. The anchor is a well-built mechanism pointed at the wrong population.

The same set shows what does work: **the plain v3.2 three-tier DCF entry.** It caught Persistent twice, at Q 6.05, for 12.72×, and its six fills average 4.82× to T against the anchor's 0.89×.

Three options. None is built, and I would not call any of them settled by this evidence:

1. **Retire the own-multiple anchor and keep v3.2's DCF entry.** The anchor has cost four rounds and produced no winner fill on any honest basis. Retiring it returns v3 to the configuration that caught the one winner it has ever caught, twice. This is the option the data supports.
2. **Re-aim the anchor at a different universe.** The Q ≥ 7 rule is the failure, not the multiple logic. But choosing a replacement universe on this set means fitting to the same 25 name-dates, and there is no third set left to validate against — so this is a decision to take on reasoning, not evidence.
3. **Fix the data before deciding anything else.** Eighteen of fifty name-dates fail a basic EPS-agreement check. Until the TTM EPS history comes from a source that agrees with audited FY figures, every version of this anchor will be validated against noise. This is the prerequisite for option 2 and it needs a data source, not engine work.

**What I would not do:** adjust Gate M's 0.875 or revive Guardrail V because this run went badly for them. Both were pre-registered and both failed. Re-fitting them now would produce a third set of numbers with no remaining set to test them on.
