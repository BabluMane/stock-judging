# v3.10 delta — APPROVED 2026-09-29

## Problem (v3.9 OOS diagnostic)

Zero fills: price sat 1.3–2.9x above the frozen DCF estimate on every computable name-date. The 12% growth cap was never binding; the binding constraint is the trailing-CAGR growth methodology plus the 5-year horizon, which structurally cannot value durable excess returns.

## Change 1 — DCF growth input: trailing CAGR → sustainable growth rate

Was: g = trailing 4-yr revenue CAGR, floored 0%, capped 12%.

Now: g = min(ROE_avg3 × (1 − payout), 15%), where ROE_avg3 = trailing-3-FY average PAT ÷ (Equity Capital + Reserves), payout = scoring-FY Dividend Payout %. All inputs PIT from audited statements.

## Change 2 — explicit forecast horizon: 5 → 10 years

Margin fade (margin_start → margin_end) still over years 1–5, flat thereafter. Terminal value at year 10, terminal g still 4%. Applied uniformly to all non-financial names.

## Change 3 — financial-variant parallel change

Excess-return model: horizon 5 → 10 years; BVPS growth = min(ROE_avg3 × (1 − payout), 15%), replacing the 12% cap. Discount rate and terminal treatment unchanged.

## Unchanged

Rf 6.95%, ERP 4.0%, sector betas, terminal g 4%, tax 25.17%, capex≈depreciation, WC 5% of incremental revenue, net-cash treatment.

QFV quality bar, entry tiers (1.00/0.875/0.70), GEV taxonomy, usability tests, live bar — all untouched.
