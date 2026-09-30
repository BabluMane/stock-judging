# v3.11 governance-log rulebook (fixed BEFORE any log was written or any valuation run)

Applies to all 13 logs in this directory. Frozen sources: `specs/V3_9_DELTA.md`
§2.1–2.4, `specs/V3_11_DELTA.md` C1–C4, `validation/v3_11_oos/OOS_SET_PREREG.md`.
Log authors are blind to valuation, fills, prices vs. triggers and results. A log
records what was **publicly disclosed and when**; it never judges outcomes.

## File format (per company, exactly this structure)

```
# <Company> — governance-event log (v3.11 OOS)
<header paragraph: scrip codes, coverage window, method, sources actually reached,
 what was NOT reachable (e.g. BSE/NSE pages 403/CAPTCHA), search limits>

## Qualifying events (§2.1)
| Event date | Taxonomy tag | One-line description | Source (BSE/NSE filing or press, with link) |
|---|---|---|---|

## Logged, non-qualifying candidates
| Event date | Taxonomy tag | One-line description | Source (BSE/NSE filing or press, with link) |
|---|---|---|---|

## Seeded events (pre-registration) — status
<one line per seeded event: SOURCED (exact date) / CORRECTED per C4 (seed wrong: real fact + date;
 real events logged separately in the tables above) / NOT SOURCED>

## Fallback-use log (C3)
<one line per fallback use: date, what fell back, source used, why. WEAK-SOURCE marking
 goes in the row description of any event sourced only to an aggregator/press summary.>
```

The runner parses the `## Qualifying events` table only: column 1 must be an
ISO date `YYYY-MM-DD`, column 2 a tag from the closed list, in backticks or bare.
No other table may sit under that heading. One row per distinct event (do not
duplicate one event under two tags; pick the best tag, mention the alternative
in the description).

## Closed tag list

`regulatory_probe` (1), `auditor_event` (2), `promoter_conduct` (3),
`withdrawn_capital_action` (4), `criminal_legal` (5), `associate_contagion` (6),
`credit_default_recognition` (7).

## Classification rules (literal reading of the frozen wording; borderline → NON-qualifying)

**Event date** = the first date the event was publicly disclosed (exchange filing,
regulator/agency order or press-release date, or first credible press report).
Facts that existed earlier but were not public (e.g. a first payment default only
revealed in a later SEBI order) are non-qualifying at their private date; if
publicly disclosed later, the later public event is the qualifying row.

1. `regulatory_probe` — SEBI / ED / SFIO probe, show-cause notice, or enforcement
   (order, penalty, settlement order, restraint) against the company, its
   promoters, or KMP. Other agencies (Income Tax searches, CBI, DRI, GST,
   competition/CCI, NFRA, foreign regulators, product/quality regulators such as
   US FDA, environmental bodies, RBI actions on a non-financial company) are NOT in
   the list → non-qualifying unless they are also a SEBI/ED/SFIO action. RBI
   enforcement/supersession on an RBI-regulated entity (NBFC/bank) IS enforcement
   against the company and counts (tag `regulatory_probe`). A routine small
   disclosure-timing SEBI penalty/settlement still counts by literal wording — mark
   it `BORDERLINE (routine)` in the description so it can be sensitivity-tested,
   but keep it in the Qualifying table.
2. `auditor_event` — statutory auditor resignation before term end, or a
   qualified / adverse / disclaimer-of-opinion audit report on the company's
   statements (standalone or consolidated). NOT: auditor rotation at end of term,
   emphasis-of-matter / "material uncertainty" paragraphs alone, limited-review
   qualifications on quarterly results (log as non-qualifying with reason).
3. `promoter_conduct` — off-market transfer/gift of promoter shares (including
   inter-se transfers structured as gifts); pledge INVOCATION disclosures. NOT
   pledge creation, open-market sales, or on-market stake changes.
4. `withdrawn_capital_action` — announced-then-withdrawn buyback, dividend or
   fundraise (withdrawn by the company; regulator hold ≠ withdrawal).
5. `criminal_legal` — arrest, charge-sheet or conviction of a promoter/KMP
   (KMP = Companies Act s.2(51): CEO/MD/manager, company secretary, whole-time
   director, CFO; senior management not in that list is non-qualifying).
6. `associate_contagion` — regulatory action against a NAMED associate/group
   company where the link is documented in the company's own filings or in the
   regulatory order itself. Press juxtaposition alone is never enough.
7. `credit_default_recognition` — downgrade to 'D' (CARE D, ICRA D, CRISIL D,
   IND D, Acuité D, Brickwork D) of ANY rated facility/instrument (bank line,
   NCD, CP; long or short term) of the company OR ITS CONSOLIDATED GROUP
   (subsidiaries count) by a SEBI-registered agency where the rationale cites
   missed/delayed servicing of debt. An initial assignment of D on an already
   defaulted facility counts. Event date = the agency press-release date; with
   several agencies the earliest D date is THE event date. NOT: outlook/watch
   changes, downgrades that stay above D (BB+ → BB, C, etc.), withdrawal without a
   default rationale, "issuer not co-operating" alone.

Everything else (management exits, CIRP/insolvency admissions on their own, rating
downgrades above D, tax raids, promoter share sales, quality/regulatory product
actions, lawsuits without arrest/charge-sheet) is logged in the non-qualifying table
with a one-line reason. An insolvency admission (NCLT) is non-qualifying by
itself; log it, and log the D-rating/RBI action that preceded it separately.

**Ambiguity rule (fixed pre-run):** if in doubt whether an event meets the literal
wording, it goes in the non-qualifying table tagged `BORDERLINE:` with the reason —
never promoted. The result document runs a sensitivity for every BORDERLINE row.

**C10 / C4 (seeded events):** a pre-registered seeded event that verifies counts as
qualifying under its best-fit §2.1 tag / type 7. A seeded event that is factually
wrong is corrected with source + date; the real events are logged separately;
never silently swap or drop a seed.

## Sources (C3 fallback hierarchy, in order)

1. BSE / NSE corporate announcements for the company's scrip (usually not
   browsable through the search proxy — say so in the header).
2. SEBI orders, RBI press releases, rating-agency press releases (CARE, ICRA,
   CRISIL, India Ratings, Acuité, Brickwork).
3. National business press (Economic Times, Business Standard, Mint,
   Moneycontrol, Reuters India, Hindu BusinessLine, Financial Express).
Each fallback use is logged. Mark `WEAK-SOURCE` when an event rests only on a press
summary/aggregator without a primary document or a named national outlet.

## Search checklist per company (targeted pass; absence of hits ≠ proof of absence)

SEBI show-cause / adjudication / settlement / insider trading / order; ED / SFIO /
MCA; auditor resignation / qualified / adverse / disclaimer; promoter pledge
invocation / inter-se or off-market transfer / gift; buyback / dividend / rights /
QIP withdrawn; promoter or KMP arrest / charge-sheet / conviction; group-company
SEBI/RBI actions named in the company's filings; rating actions to D (all agencies,
incl. subsidiaries); anything dated inside each stated window and the 12 months
before each scoring date.
