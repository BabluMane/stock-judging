# Workflow 4 — promoter activity retrieval procedure

**Status: production rubric (workflows/ item 6).** This document is the
**retrieval procedure** feeding the C6 counting rule already written in the base
spec (`specs/EQUITY_REVIEW_V3_SPEC.md` §3.C: "open-market plus block/bulk deals
by promoter/promoter group. Exclude ESOP allotments, warrant conversions, and
inter-se promoter transfers") and its ladder (`−0.5%/+1.0% of Mcap + ₹50 Cr
override`, base spec §3.C test table). **It does not change the counting rule or
the ladder** — those are frozen, per task scope. It specifies where to pull the
data and how to net it before the counting rule is applied.

## 1. Where to pull disclosures

For the trailing 4 quarters from the review date, pull all three of:

1. **BSE — "Insider Trading (SAST/PIT) Disclosures"** for the company's scrip
   code: covers open-market buy/sell by promoters and promoter-group entities
   under SEBI PIT regulations (Reg. 7 disclosures).
2. **NSE — "Corporate Announcements → Insider Trading"** for the same period:
   NSE frequently discloses the same PIT filings with different lag; cross-check
   both exchanges and use whichever discloses a given transaction first, but
   record every transaction only once (dedupe by transaction date + quantity +
   counterparty, not by which exchange listed it).
3. **BSE/NSE bulk and block deal reports** for the same window, filtered to
   rows where the buyer or seller name matches the promoter or a promoter-group
   entity (see §2 for name matching) — these are separate report types from PIT
   disclosures and can carry promoter transactions that PIT filings alone miss
   (block/bulk deals executed through the block window rather than open market).

Also pull the **shareholding pattern (Form SHP-1) for each quarter-end** in the
window — needed in §2 to know which entities count as "promoter group" and to
sanity-check that the netted PIT/bulk-deal total is consistent with the
quarter-over-quarter change in the promoter-group's aggregate holding.

## 2. Identifying the promoter group and netting across entities

- Start from the shareholding pattern's "Promoter and Promoter Group" table —
  it lists every entity (individuals, family trusts, holding companies) counted
  as promoter group for that company, as filed.
- Match every PIT and bulk/block-deal counterparty name against this list.
  Name variants (e.g. "Ramesh Kumar Shah" vs. "Ramesh K Shah HUF") are the same
  reporting person only if the shareholding pattern itself lists them as one
  line item, or if the PIT filing's "relationship to promoter" field states the
  connection (e.g. "HUF of promoter") — do not merge names on your own judgment
  of similarity; if the filing doesn't state the connection, treat as a
  separate, non-promoter counterparty and exclude the transaction from the C6
  numerator.
- **Net across the group, not per-entity.** If Promoter Entity A buys ₹10 Cr and
  Promoter Entity B (same promoter group) sells ₹4 Cr in the same quarter, the
  group's net for that quarter is +₹6 Cr — a single netted figure feeds the C6
  trailing-4-quarter ÷ market-cap calculation, not two separate signed entries.
- **Inter-se transfers**: a transaction where both the buyer and seller are
  promoter-group entities (per the same shareholding-pattern list) nets to
  **zero** and is excluded entirely from both the buy side and the sell side —
  it does not reduce one and increase the other; the base spec's exclusion
  means "invisible to the numerator," not "counted as an offsetting pair." A
  transaction is inter-se only when both legs are confirmed promoter-group by
  the same test as above (shareholding pattern listing or stated relationship);
  if only one leg's identity is confirmed, treat the transaction as an ordinary
  buy or sell, not inter-se.

## 3. Excluding ESOPs and warrants

- **ESOP allotments**: identify via the company's ESOP/ESPS allotment
  disclosures (stock exchange filing under SEBI SBEB regulations) and via the
  "reason for change" field in PIT disclosures, which for an allotment states
  "acquisition pursuant to exercise of stock options" or equivalent. Exclude
  the allotment transaction. If the promoter-group individual **subsequently
  sells** the shares received from an ESOP exercise, that sale **is** a
  countable open-market transaction (it is not itself an ESOP allotment) and is
  included in the C6 numerator on the sell side — only the allotment event
  itself is excluded, not everything downstream of it.
- **Warrant conversions**: identify via the company's warrant-conversion
  disclosure (typically tied to a prior preferential-allotment filing that
  specified the warrant terms). Exclude the conversion event on the same logic
  as ESOPs — a subsequent open-market sale of the converted shares is
  countable; the conversion itself is not.

## 4. Output feeding the counting rule

Produce one number per review: **net promoter-group PIT + bulk/block buying
(₹ Cr), trailing 4 quarters, after netting per §2 and excluding per §3**,
divided by market cap at the review date, plus the absolute ₹ Cr figure for
the ₹50 Cr override test. Feed both into the base spec's unchanged C6 ladder
(`net buy > 1% of Mcap or > ₹50 Cr` → 2; `−0.5% … +1%` → 1; `net sell > 0.5% of
Mcap` → 0). If BSE and NSE disclosures disagree on a transaction's quantity or
price for the same transaction date and counterparty, use the exchange filing
with the SEBI PIT disclosure format (Reg. 7) over a bulk/block deal report
when both exist for the same transaction, since the PIT filing is the
promoter's own disclosure obligation rather than an exchange-side trade report.

## 5. Buyback tracking — pointer

Buyback execution tracking (announced amount / executed value / average
execution price, and the C3 supportive/destructive sub-rule) is specified in
`specs/V3_8_DELTA.md` §4, not here — a buyback is a company-level capital
allocation action (C3), not a promoter-group PIT transaction (C6), even though
both concern insider-adjacent capital flows. Do not conflate the two: a
promoter open-market purchase during a buyback window is still a C6 PIT
transaction under this workflow's procedure, tracked separately from the
buyback's own three fields.
