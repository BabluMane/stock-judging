# V3.11 delta — GEV hardening + confirmation-run rules

**Status:** pre-registered addendum, 2026-09-29. Approved by Bablu same day.
**Scope:** spec clarifications ONLY. No valuation machinery changes.
The DCF formula, 15% growth cap, 10-year horizon, QFV checklist, tier
thresholds (1.00 / 0.875 / 0.70), usability checks, and the hard live bar
(0 blow-up fills · ≥3 winner names · to-T positive · 24m ≥0.8×) are frozen
and untouched. Dead designs (own-multiple anchor, Gate M, Guardrail V)
stay dead per `V3_7_DELTA.md` §3.

**Context:** v3.10 OOS (PR #8) is a technical PASS on locked rules but
fragile — see `v3/oos_audit/AUDIT_V310_OOS.md`. The batch below converts
every judgment call from that run into a literal rule with a permanent
home, so the Phase 2 confirmation run tests the system, not ambiguity.

---

## C1 — GEV type 7: credit default recognition (new §2.1 type)

Extends the closed taxonomy of six types (`specs/V3_9_DELTA.md` §2.1):

> **7. Credit default recognition:** a downgrade to **'D'** (or
> agency-equivalent default rating — CARE D, ICRA D, CRISIL D, IND D) of any
> rated facility or instrument of the company or its consolidated group,
> assigned by a SEBI-registered credit rating agency, where the agency's
> rationale cites missed or delayed servicing of debt obligations (default
> recognition). An initial assignment of 'D' on an already-defaulted
> facility also counts.
>
> **What counts:** any long-term or short-term facility — bank lines, NCDs,
> CP. If any rated facility of the company/group hits D, the event counts.
> With multiple agencies, the earliest D date is the event date.
>
> **What does NOT count:** outlook changes (negative outlook / rating
> watch); downgrades that stay above D (e.g. BB+ → BB); rating withdrawal
> without a default rationale; "issuer not co-operating" tags standing
> alone.
>
> **Event date:** the agency press-release date. Veto window (§2.2) and
> cooling-off (§2.3) apply unchanged. GEV precedence (§2.4: overrides
> QFV/ACC/INV) unchanged.

**Rationale:** the six existing types all describe public,
third-party-verified distress. A D rating certifies a *realized* payment
default per the agency's own default-recognition policy — it is more
objective, not less, than several existing types. It does not stretch
"regulatory_probe"; it replaces the v3.10 judgment call with a literal
rule. (Evidence: Dichev & Piotroski 2001 — negative abnormal returns
persist a year post-downgrade, worst for small junk names; the veto's job
is refusing realized-default equity, not prediction.)

**Application:** governs the confirmation run onward. Does NOT re-read
v3.10 data. The Gensol 2025-03-03 CARE D event (BB+ → D on ₹639.7cr
facilities, rationale: "ongoing delays in servicing of term loan
obligation as per feedback from lenders… in line with CARE's policy on
default recognition") is grandfathered under convention C10 and now has a
literal home under this type.

---

## C2 — Convention C10's permanent home

Convention C10 ("pre-seeded dated events count as qualifying under the
taxonomy") moves from result-doc-only into this addendum. The validation
runner docstring references this addendum instead of carrying C1–C10
inline. (Closes the `AUDIT_V310_OOS.md` docstring-gap flag.)

---

## C3 — Data-source fallback hierarchy

Codifies the v3.10 deviations as standing fallback rules, not one-off
exceptions:

- **Corporate actions:** Screener → exchange filings → Yahoo public split
  feed, documented per use.
- **Governance events:** BSE/NSE filings → SEBI/RBI/rating-agency documents
  + national business press, with WEAK-SOURCE marking where applicable.

Each fallback use is logged with source + date in the governance log.

---

## C4 — Seeded-event correction protocol

A seeded event that proves factually wrong is corrected with source +
date; the real events are logged separately; never silently swapped.
(The v3.10 Coffee Day "Jan-2020 disclosure" → actual 2020-07-24 precedent
becomes the rule.)

---

## C5 — GEV evaluated before fill-eligibility early-returns

The confirmation-run runner must evaluate GEV even when fair value ≤ 0 or
no fill is possible, so veto reporting is complete. Reporting-only: this
rule must not change any fill outcome. (The v3.10 `coffeeday_2020`
early-return stays flagged as residual risk until fixed.)

---

## Phase 2 confirmation-run test-design rules

**Fresh-set criteria (carried from the v3.10 proposal, unchanged):**

- 25 name-dates, same category structure (5 winners × 2, 5 mediocrities × 2,
  3 blow-ups × ~2).
- Scoring dates ≥ 2019-03-31 (QFV 5-FY window retrievable from free data;
  24m windows cover COVID stress).
- ≥2 blow-up name-dates with dated governance events inside their 24m
  windows.
- Zero overlap with in-sample 25, v3.8 OOS 13, v3.9 OOS 13, **and v3.10
  OOS 25**.
- Per-company FY-ends specified in the pre-reg (Nestlé lesson).
- Freeze rule unchanged: no adds/removes/re-dates after commit.

**New rule — GEV must be genuinely exercised:**

- Prefer blow-up name-dates where the frozen v3.10 DCF would plausibly
  produce a fill (positive fair value AND price dipping to/near trigger
  levels inside the 24m window), so that GEV — not valuation or
  usability — is the mechanism that must stop the fill.
- Firewall: the DCF formula is frozen; this rule only filters *which*
  names are tested. No outcome is asserted in advance. The pre-reg session
  may run the frozen DCF on candidate blow-ups to apply this filter.

**Why:** the v3.10 set under-tested GEV. Four of five blow-up name-dates
were stopped by negative fair value or usability before GEV was ever
evaluated; GEV decided exactly one case — on the disputed classification.
A fraud screen exercised once, on a judgment call, is not a tested fraud
screen.

**Phase 2 pre-reg session must NOT:** change anything in the frozen list,
even if the fresh data "suggests" one — that observation becomes a v3.12
proposal, never a mid-stream edit. One locked run: data + logs + runner
committed before the result commit.

---

*Pre-registered 2026-09-29. Scoping: `v3/V3_11_SCOPE.md`. Approved by
Bablu 2026-09-29 — full batch + all open questions as recommended.*
