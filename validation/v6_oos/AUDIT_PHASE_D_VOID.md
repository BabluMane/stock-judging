# v6 Phase-D — VOID PRE-RUN (Musey, 2026-10-02)

The locked one-shot was NOT executed. The v6 set, as frozen, cannot meet the
§8.2 exercise pre-conditions. This is a VOID under the spec's pre-run void
rule, not a design failure and not a patchable data defect.

## The defect (parent-verified from the frozen patch)

`v6_assembly/w1/patches/ktl_2024-03-31.json`: **beta = null**.
- KTL (Textiles SME) listed Feb-2024; d0=2024-03-31. ~1 month of price
  history (137 price points, all post-listing). A 60-month trailing beta
  vs ^NSEI is uncomputable. The assembly correctly nulled it (not invented).
- KTL is otherwise E6-decisive on paper: scoring FY2023, receivables ₹54.63cr,
  sales ₹184.17cr → 108.3 days, CFO −₹0.68cr → **E6 TRIPS** (parent-recomputed).
- 24/24 patches parse into NameDate; KTL is the ONLY null beta.

## Why this voids the run (doctrine, not convenience)

1. **Anchor cannot be valued.** `NameDate.beta` is a required float
   (run.py). `anchor.value_anchor` computes `w = C.RF + beta * C.ERP` —
   beta=None raises TypeError. Per the spec's missing-data doctrine
   (§3 UNCOMPUTABLE-DATA: "missing never silently passes"; §2.1:
   valued=False "when the structure cannot be evaluated"), the anchor is
   not valued → NO_TRIGGER on all tiers → no fill mechanically possible.
   (The runner will not crash; it records anchor-not-valued. This is a
   runner behavior note, not an engine change.)
2. **KTL cannot be decisional.** §8.2 decisional (post-run) requires
   "anchor trigger met in-window, screen veto active". No trigger exists.
   E6's trip on KTL proves the rule fires, not that it blocked a fill.
3. **KTL fails §8.2 pre-condition 2.** "Fill-plausible under the anchor:
   P_d0 ≤ 2.0 × P_G1, both computed at scoring **from frozen inputs**."
   P_G1 is uncomputable from the frozen input (beta null). The sweep's
   firewall ratio (0.724) used a provisional beta — not the frozen input.
4. **(a′) is unachievable.** Needs ≥3/4 decisional. synoptics_2024 (E6
   trips, anchor valued) + ptc_2022 (E6 passes; decisional only via another
   rule, uncertain) = max 2/4. indusindbk_2024 is the named honest residual.
   2 < 3 in every scenario.

## Verdict

**VOID pre-run** per §8.2: "if the pre-reg set cannot supply [the]
name-dates meeting all three pre-conditions (certified pre-run), **the run
does not proceed — it is VOID**, not weakened, not reinterpreted."

The one-shot was not executed. No bar legs were scored. v6 the *design*
(E6 mechanism) is not failed by this — the *set* is uncertifiable.

## What this is not

- Not a v6 design failure (E6's mechanism is untested, not refuted).
- Not patchable: inventing a beta (sector proxy, short-window) violates the
  fail-closed doctrine and the frozen input. "Never a patch."
- Not a re-runnable set: KTL cannot be made decisional on this input.

## Path forward (per §8.2)

Fresh pre-reg + fresh set (v7): new zero-overlap sweep vs all prior sets,
with a beta-availability screen in the blow-up certification (SME names
with <12m history cannot supply a PIT-valid beta — screen them out at the
firewall, not at assembly). The E6 mechanism carries forward; only the set
was void.
