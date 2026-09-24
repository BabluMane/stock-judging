# Workflow 1 — concall/release promise extraction rubric

**Status: production rubric (workflows/ item 7).** Feeds the promise register
(`PROMISE_REGISTER_SPEC.md`). Ports the USA pathway's minimum guidance classes to
the Indian pathway and adds the two classes Indian reviews already extract in
practice (debt path, ETR/timelines) but never wrote down as a rubric. Does not
change C5's scoring bands — those are unchanged; this is the extraction
checklist that feeds C5's inputs.

## 1. Minimum guidance classes — extract a promise record whenever management
makes a forward-looking, checkable statement in any of these classes. A
statement that is not checkable against a later fact (pure sentiment, "we are
confident in the business") is not a promise and is not extracted.

| Class | What qualifies | Example trigger phrase |
|---|---|---|
| `revenue` | A stated revenue growth rate, absolute revenue figure, or revenue range for a future period | "we expect 15-18% revenue growth in FY25" |
| `margin` | A stated EBITDA/operating/net margin level or range for a future period | "margins should normalize to 22-23% by H2" |
| `eps_kpi` | A stated EPS figure, or any named non-margin KPI the company itself tracks and reports (utilization, same-store sales, ARPU, order book, etc.) | "we target 30% utilization by Q4" |
| `capex` | A stated capex amount, capex-to-revenue ratio, or capacity-addition timeline | "₹500 Cr capex planned over the next two years" |
| `multi_year_target` | Any target with a horizon of more than one year (ROCE targets, 3-5 year revenue/margin ambitions, market-share goals) | "25% ROCE by FY27" |
| `debt` | A stated net-debt level, deleveraging pace, or debt/EBITDA target | "we will be net-debt-free by FY26" |
| `etr_timeline` | A stated effective tax rate expectation, **or** any dated timeline for a specific corporate event (plant commissioning, regulatory approval, litigation resolution, product launch) | "ETR should settle around 25% once the new plant is operational, expected Q3 FY25" |

Every extracted statement gets one promise record per the schema in
`PROMISE_REGISTER_SPEC.md` §1. A single sentence covering two classes (e.g. "15%
revenue growth with margins holding at 20%") is extracted as **two** promise
records, one per class, sharing the same `verbatim_quote` and `source`.

## 2. What is not extracted

- Statements about the past ("we grew 15% last quarter") — the promise register
  tracks forward-looking statements only; historical results belong in the
  review's ordinary financial-analysis sections, not the register.
- Industry-level or macro commentary not tied to a company-specific number
  ("the sector should see tailwinds").
- Analyst-question restatements where management merely agrees with a number
  the analyst suggested without independently committing to it — extract only
  when management's own words assert the figure (a bare "yes, that's fair"
  in response to an analyst's number is not company-committed; "yes, and I'd
  add that we see it holding through H2" is, because management extended it).

## 3. Withdrawal precedent — codified, not silent

The Musey review flagged "withdrawal = honest (1)" as unwritten precedent.
It is now a written rule, not a discretionary call, at
`specs/V3_8_DELTA.md` §5, and the promise register's `withdrawn` status
(`PROMISE_REGISTER_SPEC.md` §2) implements it. Workflow 1's job with respect to
withdrawal is purely extraction: when a call or release contains a statement
that revises or retracts an earlier promise, extract it as a
`status_history` entry on the **original** promise record (transition it per
§2 of the register spec), not as a new standalone promise — a withdrawal
statement is evidence about an existing promise, not a new promise of its own,
unless it also contains a fresh forward-looking commitment (e.g. "we're
lowering FY25 margin guidance to 20%" both withdraws the old 22% promise and
makes a new one — extract both: the withdrawal evidence on the old record, and
a new `active` promise record for the 20% figure).
