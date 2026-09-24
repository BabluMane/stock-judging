# V3.7 in-sample sanity check — 2026-09-24

**This is NOT the live-bar test.** It runs the DCF-only entry mechanic on the
FROZEN 26-name in-sample set (seen during v3.2/v3.6 development) to calibrate
the machinery before the real out-of-sample run (task steps 3–5). A pass here
says the recompute logic is sound; it says nothing about whether v3 works on
new names.

## What was independently recomputed, and how

`insample_sanity_recompute.py` (committed alongside this report):

1. **Ratio-consistency check.** `V3_7_DELTA.md` §1 states entry is
   ACCUMULATE at −12.5% / INVEST at −30% of DCF fair value — i.e. every
   name-date's ACC trigger ÷ INV trigger should equal 0.875 ÷ 0.70 = **1.25**
   exactly. Checked against the 4 name-dates where `specs/V3_7_DCF_REVALIDATION_20260923.md`
   §2 discloses both trigger prices: **1.25 / 1.25 / 1.24999 / 1.25002 — all
   OK.** This is a real check (the ratio isn't definitionally 1.25 in the
   data — the doc could have shown a different value if the three-tier
   structure had been misapplied) and it passes.
2. **DCF fair value reconstruction.** FV = ACC trigger ÷ 0.875 = INV trigger
   ÷ 0.70, cross-computed both ways per name-date — they agree to the cent
   (735.33/735.33, 1235.37/1235.37, 970.03/970.04, 409.29/409.29), confirming
   internal consistency of the disclosed numbers.
3. **Fill mechanics replay on real price data.** Using the actual weekly
   price series in `validation/v3_6/pe_series/*.csv` (the same CSVs used
   throughout v3.6/v3.7, not re-derived), simulated first-touch fills against
   the fixed ACC/INV triggers (DCF triggers are fixed at the scoring date per
   `V3_7_DELTA.md` §2 — never rescaled, unlike the retired own-multiple
   anchor) over the 24-month window from each scoring date.

## What this does NOT do (stated up front, not discovered after the fact)

The scored-input bundle (`inputs/`: the per-name DCF assumptions — revenue,
margins, growth, WACC drivers, and each name-date's `Q`/gate/P-floor state)
is **absent from this repository** — confirmed again here
(`find . -iname "*input*"` returns only the engine's schema/sample files).
Rebuilding 26 DCF models from financial statements from scratch would not
even check the same thing: it would produce a *new* fair value, not verify
the one the frozen validation used. So this script does not attempt that. It
reconstructs FV **algebraically from the disclosed trigger prices** (a real,
falsifiable check per point 1 above) and replays **fill mechanics only** — it
has no P-floor gate (P is a function of Q and other quality-dimension scores
this bundle doesn't have), so it cannot independently confirm any fill the
source doc itself flags as P-floor-dependent.

## Results vs the published cross-check

| Name-date | Leg | My fill date / price | My fwd_24m | Published fwd_24m | Match? |
|---|---|---|---|---|---|
| persistent_2019-03-29 | ACC | 2019-04-05 / ₹313.33 | 3.117× | 3.12× | **Yes** (source doc: "exact carry-over") |
| persistent_2019-03-29 | INV | 2019-04-05 / ₹313.33 | 3.117× | 3.12× | **Yes** |
| wipro_2015-03-31 | ACC | 2015-04-01 / ₹118.73 | 0.814× | 0.81× | **Yes** (source doc: "exact carry-over") |
| wipro_2015-03-31 | INV | 2015-04-01 / ₹118.73 | 0.814× | 0.81× | **Yes** |
| wipro_2017-03-31 | ACC | 2017-04-07 / ₹95.98 | 1.365× | 1.37× | **Yes** (source doc: "exact carry-over") |
| wipro_2017-03-31 | INV | 2017-04-07 / ₹95.98 | 1.365× | 1.37× | **Yes** |
| lichf_2018-03-31 | ACC | 2020-02-28 / ₹320.25 | 1.460× | 1.67× (date "2020-03-13?") | **No** — see below |
| lichf_2018-03-31 | INV | 2020-03-13 / ₹280.25 | 1.669× | 2.08× (date "2020-03-20?") | **No** — see below |
| piind_2016-03-31 | both | no fill (ACC trg 210.38 never touched; INV inferred 168.30 never touched) | — | no fill | **Yes** (matches "DCF trg 210.38 never reached (min ~561)") |

The three "exact carry-over" legs the source doc says are provable
bit-identical (persistent_2019, wipro_2015, wipro_2017) **independently
reproduce to 3 decimal places** on real price data with no P-floor logic at
all — consistent with the source doc's own claim that these three needed no
P-floor check because they were never blocked.

**lichf_2018 does not reproduce, and this is expected, not a new problem.**
The source doc itself marks lichf's fill dates with a "?" and states
explicitly: *"LIC Housing's two legs relocate to the COVID-crash weeks of
March 2020 **if** the P floor passes there... this name had 64 P-blocked
weeks — the floor binds hard here"* and flags the leg **"P floor
unverifiable."** My recompute has no P-floor gate, so it fires the moment
price crosses the trigger (Feb 28 for ACC) — earlier than the P-floor-gated
fills the source doc tentatively reports (Mar 13/20). The direction of the
discrepancy (my ungated fill is earlier, not later, and lands on a different
trigger than the published leg it's closest to in date) is exactly what a
missing P-floor gate would produce. This is not a contradiction of the
frozen result; it's the same limitation the source doc already disclosed,
now demonstrated mechanically rather than asserted.

**hero_2018, lupin_2017, symphony_2018:** the source doc states "DCF trg
never reached" for all three but discloses no trigger price, so this script
cannot independently confirm those no-fills. Reported `NOT_INDEPENDENTLY_VERIFIABLE`,
not silently assumed correct.

**persistent_2021, mnm_2016:** source doc states NOT COMPUTABLE (DCF fair
value unknown without the missing inputs). Reported the same way here — no
value invented.

## Bottom line

The fill/outcome **mechanics** the live-bar run will depend on (first-touch
trigger crossing, fixed DCF triggers, ACC/INV ratio = 1.25, to-T and 24m
ratio computation) check out against real price data everywhere they can be
checked. The one non-reproduction (lichf) fails for the same disclosed
reason the original report already flagged (missing P-floor inputs), not for
a new reason found here — which is itself a form of confirmation, not a
contradiction. **This calibrates the machinery used for the OOS run in task
steps 4–5; it does not and cannot substitute for it.** v3 remains NOT LIVE
pending the actual out-of-sample result.

Raw output: `validation/v3_7/insample_sanity_results.json`.
