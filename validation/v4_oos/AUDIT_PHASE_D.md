# v4 Phase-D locked run — AUDIT (Musey, 2026-10-01)

**Verdict: VOID (UNTESTED).** The run executed cleanly (25/25, frozen engine,
frozen inputs), but the blow-up leg is unexercised: the distress screen was
decisional on **0/5** certified blow-up name-dates. Per V4_OOS_PREREG_PHASED.md
§8.2/§8.4, an unexercised 0 is not a PASS of leg (a). The system is NOT LIVE.

## What the run produced (raw, from phase_d_results/)

| Leg | Bar | Result |
|---|---|---|
| (a) | 0 blow-up fills (hard) | 0 fills — numerically met |
| (a′) | distress decisional ≥3/5 | **0/5 — FAIL → leg (a) UNTESTED** |
| (b) | ≥3 distinct winner companies with fills | 4 (infy, srf, lt, endurance) — PASS |
| (c) | to-T aggregate clearly positive | +2.073 mean over 9 filled legs — PASS |
| (d) | 24m aggregate ≥0.8× | 2.406× mean multiple — PASS |

Legs (b), (c), (d) pass on their own merits. The void comes solely from (a′).

## Why (a′) failed — the exact mechanism

All 5 blow-ups: anchor **valued** the company, triggers were **touched**
in-window (fills would have occurred), and the distress gate returned
**STOP / VETOED-DATA** — `tripped: []`, `uncomputable: ['D1','D2','D3']` on all
five. The fills were blocked by **missing inputs**, not by fired rules:

- D1/D2 (promoter pledge): shareholding-pattern series empty/insufficient.
- D3 (Altman): current assets / current liabilities missing from screener tables.

Per the frozen engine's §8.2 implementation (`run.py`: "the headline counts
VETOED-DISTRESS (a tripped rule) only; VETOED-DATA is reported apart"), a data
veto is not a genuine exercise of the screen. `distress_decisional` = 0/5.

Per-name detail:
- supremeeng_2020/2021: blocked_by=['distress'] only (usability PASS, event PASS).
- pbm_2019/2020: blocked_by=['distress','usability'] (usability also VETOED-DATA).
- varroc_2019: blocked_by=['distress'] only.

Note: had the data been complete and no rule tripped, the anchor would have
filled these names — the data veto is the only thing standing between this run
and blow-up fills. The screen never rendered a judgment on the merits.

## Root cause

Data-assembly gap, not a design failure and not a set failure. The Phase-D
assembly (INPUT_BUILD_LOG.md §4.1) deliberately did not extend the AR-sourcing
pass to blow-ups ("no bar leg needs their fills") — wrong: the blow-up leg
needs their *data*. The 5 blow-ups are small/BSE names whose pledge and CA/CL
sit outside screener's static HTML; the values exist in ARs/BSE filings.

## What was NOT the problem

- Engine: frozen tree 6ea7e7a1…, spec hash matches pin, 137/137 tests pre-run.
- Inputs: 25/25 schema PASS, 63-day PIT asserted, disjointness holds.
- Runner: one-shot, 25/25 executed, no mid-run edits (two pre-run path fixes,
  zero result influence).
- Legs (b)–(d): genuine passes, 9 filled legs, no exits fired.

## Path forward (Bablu decides)

- **Option A (pre-reg letter):** new pre-reg + new 5 blow-ups, fresh
  zero-overlap vs all six prior sets. Expensive; same data risk recurs.
- **Option B (recommended):** complete the data — AR/BSE-source pledge + CA/CL
  for the 5 blow-up name-dates (mechanical, auditable, no tuning knob: the
  frozen rules either trip on the real numbers or they don't) — under a
  pre-registered amendment, re-run the same frozen set. Bar unchanged (≥3/5).

Option B needs explicit approval: it amends the governing pre-reg post-result.
Either way, this VOID stands as recorded and the system is NOT LIVE.
