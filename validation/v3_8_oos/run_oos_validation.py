#!/usr/bin/env python3
"""
V3.8 OOS live-bar validation -- the one run.

Step A: apply the frozen v3.7 usability test (spec Sec 4.1/4.2, conventions
resolved in validation/v3_7/CONVENTIONS.md) to all 25 pre-registered
name-dates, using:
  - sourced FY EPS: screener.in's audited "EPS in Rs" P&L row (real audited
    PAT / CURRENT continuously-adjusted share count -- empirically verified
    against GAIL's PAT/share-count/EPS relationship: NOT back-solved from
    the vendor quotient series, and already on the SAME continuously-
    adjusted basis as the vendor TTM series, so no further corp-action
    restatement is needed -- see the methodology note in the report).
  - vendor results-week TTM EPS: first publication-dated eps_series point
    strictly after the FY-end (skips the exact FY-end point, which is
    usually a stale pre-results value -- matches the v3.7 rerun's own
    "skip a stale Mar-31 point" rule).
Step B: for usable non-financial name-dates, build a DCF fair value from
real financial-statement data (point-in-time: only data reported BEFORE the
scoring date is used), apply the v3.2/v3.7 three-tier entry
(ACC = 0.875 x FV, INV = 0.70 x FV), and replay fills on the real weekly
price series -- exactly as the in-sample sanity check did.
Step C: score the four-line live bar.

ONE run. No refit. No second attempt on a disappointing number.
"""
import csv
import json
from datetime import date, timedelta

DAYS24M = timedelta(days=int(2 * 365.25))
TODAY = date(2026, 9, 24)

# ---------------------------------------------------------------------------
# Pre-registered set (validation/v3_8_oos/OOS_SET_PREREG.md)
# ---------------------------------------------------------------------------
NAME_DATES = [
    # (key, slug, FY column in full_financials_raw, scoring date, category)
    ("titan_2016-03-31", "titan", "Mar 2016", "2016-03-31", "winner"),
    ("titan_2018-03-31", "titan", "Mar 2018", "2018-03-31", "winner"),
    ("divislab_2016-03-31", "divislab", "Mar 2016", "2016-03-31", "winner"),
    ("divislab_2018-03-31", "divislab", "Mar 2018", "2018-03-31", "winner"),
    ("pageind_2015-03-31", "pageind", "Mar 2015", "2015-03-31", "winner"),
    ("pageind_2017-03-31", "pageind", "Mar 2017", "2017-03-31", "winner"),
    ("dmart_2018-03-31", "dmart", "Mar 2018", "2018-03-31", "winner"),
    ("dmart_2019-03-31", "dmart", "Mar 2019", "2019-03-31", "winner"),
    ("polycab_2020-03-31", "polycab", "Mar 2020", "2020-03-31", "winner"),
    ("polycab_2021-03-31", "polycab", "Mar 2021", "2021-03-31", "winner"),
    ("colpal_2016-03-31", "colpal", "Mar 2016", "2016-03-31", "mediocre"),
    ("colpal_2018-03-31", "colpal", "Mar 2018", "2018-03-31", "mediocre"),
    ("ashokley_2016-03-31", "ashokley", "Mar 2016", "2016-03-31", "mediocre"),
    ("ashokley_2018-03-31", "ashokley", "Mar 2018", "2018-03-31", "mediocre"),
    ("cipla_2016-03-31", "cipla", "Mar 2016", "2016-03-31", "mediocre"),
    ("cipla_2018-03-31", "cipla", "Mar 2018", "2018-03-31", "mediocre"),
    ("coalindia_2016-03-31", "coalindia", "Mar 2016", "2016-03-31", "mediocre"),
    ("coalindia_2018-03-31", "coalindia", "Mar 2018", "2018-03-31", "mediocre"),
    ("gail_2016-03-31", "gail", "Mar 2016", "2016-03-31", "mediocre"),
    ("gail_2018-03-31", "gail", "Mar 2018", "2018-03-31", "mediocre"),
    ("pcjeweller_2017-03-31", "pcjeweller", "Mar 2017", "2017-03-31", "blowup"),
    ("pcjeweller_2018-03-31", "pcjeweller", "Mar 2018", "2018-03-31", "blowup"),
    ("fretail_2017-03-31", "fretail_standalone", "Mar 2017", "2017-03-31", "blowup"),
    ("fretail_2019-03-31", "fretail", "Mar 2019", "2019-03-31", "blowup"),
    ("cgpower_2016-03-31", "cgpower", "Mar 2016", "2016-03-31", "blowup"),
]
PRICE_SLUG = {  # price/PE series file to use per name-date (fretail has one series regardless of which financials table)
    "fretail_standalone": "fretail",
}


def D(s):
    return date.fromisoformat(s)


def load_prices(slug):
    rows = []
    with open(f"pe_series/{slug}.csv", newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["price"]:
                rows.append((D(r["date"]), float(r["price"])))
    rows.sort()
    return rows


def load_eps_series(slug):
    d = json.load(open(f"eps_series/{slug}.json"))
    vals = [(D(dt[:10]), v) for dt, v in d["values"]]
    vals.sort()
    return vals


def results_week_ttm(eps_series, fy_end):
    """First vendor TTM point strictly after FY-end, skipping the exact
    FY-end-dated point (usually stale/pre-results), within a 6-month window."""
    cands = [(d, v) for d, v in eps_series if fy_end < d <= fy_end + timedelta(days=183)]
    return cands[0] if cands else None


# ---------------------------------------------------------------------------
# Step A: usability
# ---------------------------------------------------------------------------
def usability(financials, key, slug, fy_col, d0):
    price_slug = PRICE_SLUG.get(slug, slug)
    pnl = financials[slug]["profit_loss"]
    if fy_col not in pnl["years"]:
        return "EXCLUDED", f"FY column {fy_col} not in fetched P&L years {pnl['years']}"
    i = pnl["years"].index(fy_col)
    eps_row = pnl["rows"].get("EPS in Rs")
    if not eps_row or eps_row[i] in ("", None):
        return "EXCLUDED", "no sourced EPS at this FY (structural)"
    try:
        sourced = float(eps_row[i].replace(",", ""))
    except ValueError:
        return "EXCLUDED", f"unparseable sourced EPS '{eps_row[i]}'"

    eps_series = load_eps_series(price_slug)
    rw = results_week_ttm(eps_series, d0)
    if rw is None:
        return "EXCLUDED", "no PIT EPS at date (structural) -- no vendor TTM point within 6mo of FY-end"
    rw_date, rw_val = rw

    if sourced <= 0:
        return "EXCLUDED", (f"(a) sourced FY EPS is non-positive/negative ({sourced}) while vendor TTM is "
                             f"{rw_val} @ {rw_date} -- fails the constant-residual harmless-basis test "
                             f"(CONVENTIONS.md sec 1); treated as a basis defect, not adjudicated further")
    gap = (rw_val / sourced - 1) * 100
    verdict = "USABLE" if abs(gap) <= 15 else "EXCLUDED"
    return verdict, f"(a) {gap:+.1f}% @pub {rw_date} TTM={rw_val} src={sourced}"


# ---------------------------------------------------------------------------
# Step B: DCF fair value + three-tier fill replay
# ---------------------------------------------------------------------------
RF = 0.0695
ERP = 0.040
HURDLE = 0.15
TG = 0.04
TAX_DEFAULT = 0.2517

SECTOR_BETA = {  # informed sector-typical beta, used only where screener exposes no measured beta
    "titan": 0.85, "divislab": 0.75, "pageind": 0.70, "dmart": 0.90, "polycab": 1.05,
    "colpal": 0.55, "ashokley": 1.15, "cipla": 0.65, "coalindia": 0.85, "gail": 0.90,
    "pcjeweller": 1.25, "fretail_standalone": 1.20, "cgpower": 1.20,
}


def num(s):
    if s is None or s == "":
        return None
    return float(str(s).replace(",", "").replace("%", ""))


def dcf_fair_value(financials, balance, slug, fy_col):
    """Point-in-time 5-yr explicit FCFF DCF (engine/engine_v3.py dcf_value
    logic, reimplemented standalone since the repo's engine module expects a
    full quality-scored input dict this task does not need -- entry is
    DCF-only per V3_7_DELTA, no Q gate). Uses only data reported in FY
    columns UP TO AND INCLUDING fy_col (the FY ending at/adjacent to the
    scoring date) -- no lookahead."""
    pnl = financials[slug]["profit_loss"]
    years = pnl["years"]
    if fy_col not in years:
        return None, "FY column missing"
    idx = years.index(fy_col)
    hist_idx = [j for j in range(max(0, idx - 4), idx + 1)]  # trailing 5 FYs ending at fy_col
    sales = [num(pnl["rows"]["Sales&nbsp;+"][j]) for j in hist_idx]
    opm = [num(pnl["rows"]["OPM %"][j]) for j in hist_idx]
    dep = [num(pnl["rows"]["Depreciation"][j]) for j in hist_idx]
    if any(x is None for x in sales) or len(sales) < 1:
        return None, "no trailing revenue history at all"
    rev0 = sales[-1]
    n = len(sales) - 1
    if rev0 <= 0:
        return None, "non-positive revenue in the scoring FY"
    if n > 0 and sales[0] > 0:
        cagr = (rev0 / sales[0]) ** (1 / n) - 1
        growth = max(0.0, min(cagr, 0.12))
    else:
        # <2 years of fetched history (name near the start of its P&L table, e.g. pageind_2015 is the
        # first column available, fretail_2019 the first post-demerger consolidated column) -- no CAGR
        # is computable. Conservative disclosed fallback: 8% (spec's "unless delivered history justifies
        # more" default), not the 12% cap, since there IS no delivered history here to justify the cap.
        growth = 0.08
    opm_vals = [x / 100 for x in opm if x is not None]
    margin_start = opm_vals[-1] if opm_vals else 0.15
    margin_end = (sum(opm_vals) / len(opm_vals)) if len(opm_vals) >= 3 else margin_start
    dep_vals = [d / s for d, s in zip(dep, sales) if d is not None and s]
    dep_pct = (sum(dep_vals) / len(dep_vals)) if dep_vals else 0.03
    capex_pct = dep_pct  # simplifying assumption, disclosed: capex ~= depreciation (steady-state)
    wc_pct = 0.05  # simplifying assumption: 5% of incremental revenue, disclosed (no clean WC series available)

    beta = SECTOR_BETA.get(slug, 1.0)
    r_val = RF + beta * ERP
    bs = balance["rows"]
    face_value = None
    # shares outstanding: current equity capital / current face value (as-of-today, continuously-adjusted basis
    # matching the price series and the EPS row -- see methodology note). Face value not in BS table; use
    # current market cap / current price as a cross-check-free direct measure instead (avoids needing FV at all).
    return {
        "rev0": rev0, "growth": growth, "margin_start": margin_start, "margin_end": margin_end,
        "capex_pct": capex_pct, "dep_pct": dep_pct, "wc_pct": wc_pct, "r_val": r_val, "beta": beta,
    }, None


def dcf_value_per_share(v, w):
    """FCFF DCF, 5-yr explicit + terminal, mirrors engine_v3.dcf_value (spec 4.1),
    on a PER-SHARE basis directly (rev0 etc supplied in Rs crore per share-equivalent
    by dividing by current shares before calling)."""
    rev0 = v["rev0"]; ms = v["margin_start"]; me = v["margin_end"]; growth = v["growth"]
    years = 5; tg = TG; cs = ce = v["capex_pct"]; ds = de = v["dep_pct"]; wc = v["wc_pct"]
    tax = TAX_DEFAULT
    r = rev0; pv = 0.0
    for i in range(1, years + 1):
        prev = r
        r = prev * (1 + growth)
        f = i / years
        m = ms + (me - ms) * f
        cp = cs + (ce - cs) * f
        dp = ds + (de - ds) * f
        nopat = r * (m - dp) * (1 - tax)
        fcff = nopat + r * dp - r * cp - (r - prev) * wc
        pv += fcff / (1 + w) ** i
    nopat_n = r * (me - de) * (1 - tax)
    fcff_norm = nopat_n - (r * tg / (1 + tg)) * wc
    if w <= tg + 0.005:
        return None
    tv = fcff_norm * (1 + tg) / (w - tg)
    pv_tv = tv / (1 + w) ** years
    return pv + pv_tv  # value of the whole enterprise's operating cash flows, in same units as rev0


def simulate_fill(slug, d0, acc_trg, inv_trg):
    prices = load_prices(PRICE_SLUG.get(slug, slug))
    window = [(d, p) for d, p in prices if d0 < d <= d0 + DAYS24M]
    if not prices:
        return {}
    latest_date, latest_price = prices[-1]
    out = {}
    for leg, trg in (("accumulate", acc_trg), ("invest", inv_trg)):
        fill = next(((d, p) for d, p in window if p <= trg), None)
        if not fill:
            out[leg] = {"fill": None}
            continue
        fd, fp = fill
        fwd = [(d, p) for d, p in prices if fd < d <= fd + DAYS24M]
        out[leg] = {
            "fill_date": fd.isoformat(), "fill_price": fp, "trigger": round(trg, 2),
            "fwd_24m": round(fwd[-1][1] / fp, 3) if fwd else None,
            "fwd_months": round((fwd[-1][0] - fd).days / 30.44, 1) if fwd else None,
            "fwd_truncated": bool(fwd and fwd[-1][0] < fd + DAYS24M - timedelta(days=20)),
            "to_latest": round(latest_price / fp, 3),
            "to_latest_date": latest_date.isoformat(),
        }
    return out


def main():
    financials = json.load(open("full_financials_raw.json"))
    top_ratios = json.load(open("top_ratios.json"))

    usability_results = {}
    for key, slug, fy_col, d0s, cat in NAME_DATES:
        v, r = usability(financials, key, slug, fy_col, D(d0s))
        usability_results[key] = {"verdict": v, "reason": r, "category": cat}

    print("=== USABILITY ===")
    n_usable = 0
    for key, res in usability_results.items():
        print(f"  {key:26s} {res['verdict']:9s} {res['reason']}")
        if res["verdict"] == "USABLE":
            n_usable += 1
    print(f"\n{n_usable}/{len(NAME_DATES)} usable\n")

    print("=== DCF + FILLS (usable only) ===")
    fill_results = {}
    for key, slug, fy_col, d0s, cat in NAME_DATES:
        if usability_results[key]["verdict"] != "USABLE":
            continue
        bs = financials[slug]["balance_sheet"]
        v, err = dcf_fair_value(financials, bs, slug, fy_col)
        if v is None:
            fill_results[key] = {"status": f"DCF_NOT_COMPUTABLE: {err}"}
            print(f"  {key:26s} DCF NOT COMPUTABLE ({err})")
            continue
        w = v["r_val"]
        ev_per_unit_revenue = dcf_value_per_share(v, w)
        if ev_per_unit_revenue is None:
            fill_results[key] = {"status": "DCF degenerate (WACC <= terminal g + 0.5pp)"}
            continue
        # net cash/debt: point-in-time, from the SAME fiscal year as the DCF's revenue/margin base (a
        # company's absolute debt/cash pile is not affected by later stock splits/bonuses, unlike EPS or
        # price -- so this must NOT use today's balance sheet, only shares-outstanding gets that treatment,
        # for consistency with the continuously-adjusted price series it's compared against).
        bs_years = bs["years"]
        bs_idx = bs_years.index(fy_col) if fy_col in bs_years else None
        if bs_idx is not None:
            borrow = num(bs["rows"].get("Borrowings&nbsp;+", [None] * len(bs_years))[bs_idx]) or 0.0
            invest = num(bs["rows"].get("Investments", [None] * len(bs_years))[bs_idx]) or 0.0
        else:
            borrow = invest = 0.0
        net_cash = invest - borrow  # crude proxy (screener bundles cash into Other Assets; disclosed limitation)

        tr = top_ratios[slug]
        mcap, price_now = num(tr["market_cap_cr"]), num(tr["current_price"])
        shares_cr = mcap / price_now  # current (today's), continuously-adjusted basis -- matches the price series

        fv_total_cr = ev_per_unit_revenue + net_cash  # enterprise value of operating CFs + net cash, Rs crore
        fv_per_share = fv_total_cr / shares_cr
        acc_trg = round(0.875 * fv_per_share, 2)
        inv_trg = round(0.70 * fv_per_share, 2)
        fills = simulate_fill(slug, D(d0s), acc_trg, inv_trg)
        fill_results[key] = {
            "fair_value_per_share": round(fv_per_share, 2), "acc_trigger": acc_trg, "inv_trigger": inv_trg,
            "wacc": round(w, 4), "growth": round(v["growth"], 4), "beta": v["beta"],
            "margin_start": round(v["margin_start"], 4), "margin_end": round(v["margin_end"], 4),
            "shares_cr": round(shares_cr, 2), "net_cash_cr": round(net_cash, 1), "category": cat,
            "fills": fills,
        }
        print(f"  {key:26s} FV/sh={fv_per_share:>9.2f}  ACC={acc_trg:>9.2f}  INV={inv_trg:>9.2f}  "
              f"acc_fill={fills.get('accumulate', {}).get('fill_date')}  inv_fill={fills.get('invest', {}).get('fill_date')}")

    json.dump({"usability": usability_results, "results": fill_results},
               open("oos_results.json", "w"), indent=2, default=str)
    print("\nWrote oos_results.json")

    # ---- four-line scorecard ----
    winner_names_filled = set()
    blowup_fills = 0
    to_t_ratios = []  # informational (to-latest-series-date proxy, see sanity-check note)
    m24 = []
    for key, r in fill_results.items():
        if "fills" not in r:
            continue
        cat = r["category"]
        any_fill = False
        for leg in ("accumulate", "invest"):
            f = r["fills"].get(leg) or {}
            if f.get("fill_date"):
                any_fill = True
                if f.get("fwd_24m") is not None:
                    m24.append(f["fwd_24m"])
                if f.get("to_latest") is not None:
                    to_t_ratios.append(f["to_latest"])
        if any_fill:
            if cat == "winner":
                winner_names_filled.add(key.split("_")[0])
            if cat == "blowup":
                blowup_fills += 1
    print("\n=== SCORECARD ===")
    print(f"  Blow-up fills: {blowup_fills} (need 0)")
    print(f"  Winner names with a fill: {len(winner_names_filled)} {sorted(winner_names_filled)} (need >=3 distinct)")
    print(f"  Mean to-latest-series-date ratio (informational proxy for to-T): "
          f"{sum(to_t_ratios)/len(to_t_ratios):.3f}x over {len(to_t_ratios)} fills" if to_t_ratios else "  no fills")
    print(f"  Mean 24m ratio: {sum(m24)/len(m24):.3f}x over {len(m24)} fills (need >=0.8x)" if m24 else "  no fills")


if __name__ == "__main__":
    main()
