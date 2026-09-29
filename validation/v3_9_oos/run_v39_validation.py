#!/usr/bin/env python3
"""
V3.9 OOS live-bar validation -- the one run.

Extends validation/v3_8_oos/run_oos_validation.py's method (frozen v3.7
usability test, FCFF DCF-only entry, real weekly-price fill replay) with:
  - QFV tier (specs/V3_9_DELTA.md Sec1): ROIC/OCF-PAT/D-E/mcap AND-gate,
    fills at 1.00x fair value.
  - GEV veto (specs/V3_9_DELTA.md Sec2): governance-event log, PIT,
    evaluated at scoring AND at each candidate fill date.
Financial-variant names (HDFC Bank, Bank of Baroda) use a standalone
excess-return/residual-income fair value in place of FCFF DCF (banks have
no Sales/OPM/Capex line items) -- exempt from usability check(a)/(b) per
V3_7_DELTA Sec4 sector_variant=="financial" carve-out. QFV's ROIC/OCF-PAT
gate does not apply to the bank balance-sheet shape either -- financial-
variant names are scored ACC/INV only, never QFV (disclosed scope limit).

ONE run. No refit.
"""
import json
from datetime import date, timedelta

DAYS24M = timedelta(days=int(2 * 365.25))
TODAY = date(2026, 9, 29)

RF = 0.0695
ERP = 0.040
TG = 0.04
TAX_DEFAULT = 0.2517

SECTOR_BETA = {
    "asianpaint": 0.65, "hdfcbank": 0.90, "nestleind": 0.55, "britannia": 0.60, "havells": 0.90,
    "bhartiartl": 0.85, "tatasteel": 1.15, "ntpc": 0.80, "tatamotors": 1.30, "bankbaroda": 1.15,
    "zeel": 1.10, "relcapital": 1.30, "ilfstransport": 1.20,
}

# ---------------------------------------------------------------------------
# Pre-registered set (validation/v3_9_oos/OOS_SET_PREREG_v39.md)
# key -> (slug, scoring FY column [as it exists in the raw table], scoring date, category, financial_variant)
# ---------------------------------------------------------------------------
NAME_DATES = [
    ("asianpaint_2014-03-31", "asianpaint", "Mar 2014", "2014-03-31", "winner", False),
    ("asianpaint_2016-03-31", "asianpaint", "Mar 2016", "2016-03-31", "winner", False),
    ("hdfcbank_2014-03-31", "hdfcbank", "Mar 2014", "2014-03-31", "winner", True),
    ("hdfcbank_2016-03-31", "hdfcbank", "Mar 2016", "2016-03-31", "winner", True),
    ("nestleind_2015-03-31", "nestleind", "Dec 2014", "2015-03-31", "winner", False),
    ("nestleind_2017-03-31", "nestleind", "Dec 2016", "2017-03-31", "winner", False),
    ("britannia_2015-03-31", "britannia", "Mar 2015", "2015-03-31", "winner", False),
    ("britannia_2017-03-31", "britannia", "Mar 2017", "2017-03-31", "winner", False),
    ("havells_2014-03-31", "havells", "Mar 2014", "2014-03-31", "winner", False),
    ("havells_2016-03-31", "havells", "Mar 2016", "2016-03-31", "winner", False),
    ("bhartiartl_2016-03-31", "bhartiartl", "Mar 2016", "2016-03-31", "mediocre", False),
    ("bhartiartl_2018-03-31", "bhartiartl", "Mar 2018", "2018-03-31", "mediocre", False),
    ("tatasteel_2015-03-31", "tatasteel", "Mar 2015", "2015-03-31", "mediocre", False),
    ("tatasteel_2017-03-31", "tatasteel", "Mar 2017", "2017-03-31", "mediocre", False),
    ("ntpc_2015-03-31", "ntpc", "Mar 2015", "2015-03-31", "mediocre", False),
    ("ntpc_2017-03-31", "ntpc", "Mar 2017", "2017-03-31", "mediocre", False),
    ("tatamotors_2015-03-31", "tatamotors", "Mar 2015", "2015-03-31", "mediocre", False),
    ("tatamotors_2017-03-31", "tatamotors", "Mar 2017", "2017-03-31", "mediocre", False),
    ("bankbaroda_2015-03-31", "bankbaroda", "Mar 2015", "2015-03-31", "mediocre", True),
    ("bankbaroda_2017-03-31", "bankbaroda", "Mar 2017", "2017-03-31", "mediocre", True),
    ("zeel_2017-03-31", "zeel", "Mar 2017", "2017-03-31", "blowup", False),
    ("zeel_2018-03-31", "zeel", "Mar 2018", "2018-03-31", "blowup", False),
    ("relcapital_2016-03-31", "relcapital", "Mar 2016", "2016-03-31", "blowup", True),
    ("relcapital_2018-03-31", "relcapital", "Mar 2018", "2018-03-31", "blowup", True),
    ("ilfstransport_2017-03-31", "ilfstransport", "Mar 2017", "2017-03-31", "blowup", False),
]

# ---------------------------------------------------------------------------
# Governance-event log (PIT, per specs/V3_9_DELTA.md Sec2.1 taxonomy)
# Sourced from national business press (Business Standard etc.) via web
# search this session, corroborating well-documented dated events. Method
# limitation disclosed in the result doc: this is a press-search pass, not
# a full BSE/NSE filing crawl -- same honesty standard as Sec2.5's
# "specified but not fully operable" note.
# Each entry: (event_date, tag, qualifies: bool, note)
# ---------------------------------------------------------------------------
GEV_LOG = {
    "asianpaint": [],
    "hdfcbank": [
        ("2016-07-25", "regulatory_probe", False,
         "RBI Rs 2cr penalty for KYC/AML lapses (advance import remittances) -- routine compliance fine, "
         "not a probe/enforcement action against the company/promoter/KMP in the taxonomy's intended sense; judged non-qualifying."),
    ],
    "nestleind": [],
    "britannia": [],
    "havells": [],
    "bhartiartl": [],
    "tatasteel": [
        ("2016-11-08", "regulatory_probe", True,
         "Post Cyrus Mistry's Oct-2016 removal as Tata Sons chairman and his public allegations of governance "
         "lapses (Tata Steel Europe write-downs among the cited items), SEBI directed the stock exchanges to "
         "scrutinise Tata Steel's own listing/disclosure compliance (Business Standard, 2016-11-08)."),
    ],
    "ntpc": [],
    "tatamotors": [
        ("2016-11-08", "regulatory_probe", True,
         "Same Cyrus Mistry-allegations fallout; SEBI directed exchanges to scrutinise Tata Motors' own "
         "disclosure compliance (Nano project losses cited) alongside Tata Steel (Business Standard, 2016-11-08)."),
    ],
    "bankbaroda": [
        ("2015-10-09", "regulatory_probe", False,
         "CBI/ED/SFIO raids and arrests over the ~Rs 6,172cr Ashok Vihar branch forex remittance scam "
         "(Oct 2015). Action targeted branch-level officials (AGM + forex officer), not the company as a "
         "whole or named promoter/KMP -- PSU with no promoter; judged non-qualifying under Sec2.1.1's "
         "'against the company, its promoters, or KMP' wording. Logged, not vetoed -- disclosed judgment call."),
    ],
    "zeel": [
        ("2019-01-25", "promoter_conduct", True,
         "Essel Group promoter-linked entity (Nityank Infrapower, tied to demonetisation-era suspicious "
         "deposits per a Wire report) link disclosed; ZEEL stock fell ~33% same day on promoter-debt fears."),
        ("2019-02-03", "promoter_conduct", True,
         "Lenders (Bank of Baroda, Credit Suisse) invoked and sold Essel-Group-pledged ZEEL shares."),
    ],
    "relcapital": [
        ("2019-06-11", "auditor_event", True,
         "PwC resigned as statutory auditor of Reliance Capital (and Reliance Home Finance), effective "
         "2019-06-11, citing an unsatisfactory management response to audit observations for FY19; "
         "announced/disclosed 2019-06-12."),
    ],
    "ilfstransport": [
        ("2018-09-06", "associate_contagion", True,
         "Parent IL&FS Group's first disclosed default (missed Aug-28 commercial-paper payment, settled "
         "2018-08-31, disclosed 2018-09-06), the start of the IL&FS Group default cascade through Sep-2018 "
         "-- documented in the parent's own filings/press and directly implicating this subsidiary."),
    ],
}


def D(s):
    return date.fromisoformat(s)


def num(s):
    if s is None or s == "":
        return None
    try:
        return float(str(s).replace(",", "").replace("%", ""))
    except ValueError:
        return None


def load_prices(slug):
    import csv
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
    cands = [(d, v) for d, v in eps_series if fy_end < d <= fy_end + timedelta(days=183)]
    return cands[0] if cands else None


def year_index(years, fy_col, row_len):
    """First N years correspond 1:1 with a row's values (some ratio tables
    repeat the year header list for a second embedded sub-table)."""
    yrs = years[:row_len]
    return yrs.index(fy_col) if fy_col in yrs else None


def usability(fin, slug, fy_col, d0, is_financial):
    pnl = fin[slug]["profit_loss"]
    if fy_col not in pnl["years"]:
        return "EXCLUDED", f"FY column {fy_col} not in fetched P&L years {pnl['years']}"
    if is_financial:
        return "USABLE", "financial variant -- exempt from check (a)/(b) per V3_7_DELTA Sec4"
    i = pnl["years"].index(fy_col)
    eps_row = pnl["rows"].get("EPS in Rs")
    if not eps_row or i >= len(eps_row) or eps_row[i] in ("", None):
        return "EXCLUDED", "no sourced EPS at this FY (structural)"
    sourced = num(eps_row[i])
    if sourced is None:
        return "EXCLUDED", f"unparseable sourced EPS '{eps_row[i]}'"

    eps_series = load_eps_series(slug)
    rw = results_week_ttm(eps_series, d0)
    if rw is None:
        return "EXCLUDED", "no PIT EPS at date (structural) -- no vendor TTM point within 6mo of FY-end"
    rw_date, rw_val = rw

    if sourced <= 0:
        return "EXCLUDED", (f"(a) sourced FY EPS is non-positive ({sourced}) while vendor TTM is "
                             f"{rw_val} @ {rw_date} -- basis defect, not adjudicated further")
    gap = (rw_val / sourced - 1) * 100
    verdict = "USABLE" if abs(gap) <= 15 else "EXCLUDED"
    return verdict, f"(a) {gap:+.1f}% @pub {rw_date} TTM={rw_val} src={sourced}"


def dcf_fcff_fair_value(fin, slug, fy_col):
    """Standalone FCFF DCF, mirrors validation/v3_8_oos/run_oos_validation.py
    dcf_fair_value/dcf_value_per_share exactly (same simplifications:
    capex ~= dep, wc_pct=5% of incremental revenue, growth cap 12%,
    margin_end = 3yr-avg-if-available else margin_start)."""
    pnl = fin[slug]["profit_loss"]
    years = pnl["years"]
    if fy_col not in years:
        return None, "FY column missing"
    idx = years.index(fy_col)
    hist_idx = [j for j in range(max(0, idx - 4), idx + 1)]
    sales = [num(pnl["rows"]["Sales&nbsp;+"][j]) if j < len(pnl["rows"]["Sales&nbsp;+"]) else None for j in hist_idx]
    opm = [num(pnl["rows"]["OPM %"][j]) if j < len(pnl["rows"]["OPM %"]) else None for j in hist_idx]
    dep = [num(pnl["rows"]["Depreciation"][j]) if j < len(pnl["rows"]["Depreciation"]) else None for j in hist_idx]
    if any(x is None for x in sales) or len(sales) < 1:
        return None, "no trailing revenue history at all"
    rev0 = sales[-1]
    n = len(sales) - 1
    if rev0 is None or rev0 <= 0:
        return None, "non-positive revenue in the scoring FY"
    if n > 0 and sales[0] and sales[0] > 0:
        cagr = (rev0 / sales[0]) ** (1 / n) - 1
        growth = max(0.0, min(cagr, 0.12))
    else:
        growth = 0.08
    opm_vals = [x / 100 for x in opm if x is not None]
    margin_start = opm_vals[-1] if opm_vals else 0.15
    margin_end = (sum(opm_vals) / len(opm_vals)) if len(opm_vals) >= 3 else margin_start
    dep_vals = [d / s for d, s in zip(dep, sales) if d is not None and s]
    dep_pct = (sum(dep_vals) / len(dep_vals)) if dep_vals else 0.03
    capex_pct = dep_pct
    wc_pct = 0.05

    beta = SECTOR_BETA.get(slug, 1.0)
    r_val = RF + beta * ERP
    return {
        "rev0": rev0, "growth": growth, "margin_start": margin_start, "margin_end": margin_end,
        "capex_pct": capex_pct, "dep_pct": dep_pct, "wc_pct": wc_pct, "r_val": r_val, "beta": beta,
    }, None


def dcf_value_pv(v, w):
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
    return pv + pv_tv


def excess_return_fair_value(fin, slug, fy_col):
    """Financial-variant (bank) fair value: residual-income / excess-return
    model on trailing book value + ROE, since screener's bank template
    exposes no Sales/OPM/Capex to run an FCFF DCF against (engine_v3.py's
    own financial variant expects this value pre-supplied by the Record,
    not computed -- this is a disclosed standalone reimplementation for
    the OOS task, same spirit as the FCFF reimplementation above).
    FV/share = BVPS0 + sum_{t=1..5} (ROE-r)*BVPS_{t-1}/(1+r)^t + terminal.
    """
    pnl = fin[slug]["profit_loss"]
    bs = fin[slug]["balance_sheet"]
    years = pnl["years"]
    bs_years = bs["years"]
    if fy_col not in years or fy_col not in bs_years:
        return None, "FY column missing"
    idx = years.index(fy_col)
    bidx = bs_years.index(fy_col)
    hist_idx = [j for j in range(max(0, idx - 4), idx + 1)]
    bhist_idx = [j for j in range(max(0, bidx - 4), bidx + 1)]
    net_profit = [num(pnl["rows"]["Net Profit&nbsp;+"][j]) if j < len(pnl["rows"]["Net Profit&nbsp;+"]) else None for j in hist_idx]
    equity_cap = [num(bs["rows"]["Equity Capital"][j]) if j < len(bs["rows"]["Equity Capital"]) else None for j in bhist_idx]
    reserves = [num(bs["rows"]["Reserves"][j]) if j < len(bs["rows"]["Reserves"]) else None for j in bhist_idx]
    if any(x is None for x in equity_cap[-2:]) or any(x is None for x in reserves[-2:]):
        return None, "insufficient balance-sheet history"
    book_value = [e + r for e, r in zip(equity_cap, reserves) if e is not None and r is not None]
    if not book_value or book_value[-1] <= 0:
        return None, "non-positive book value"
    roe_series = []
    for np_, bv_end in zip(net_profit, book_value):
        if np_ is not None and bv_end and bv_end > 0:
            roe_series.append(np_ / bv_end)
    if not roe_series:
        return None, "no computable ROE history"
    roe = sum(roe_series[-3:]) / len(roe_series[-3:])  # trailing-3yr average ROE (disclosed: no fade model)
    bv0 = book_value[-1]
    n = len(book_value) - 1
    if n > 0 and book_value[0] > 0:
        g = max(0.0, min((bv0 / book_value[0]) ** (1 / n) - 1, 0.12))
    else:
        g = 0.06
    beta = SECTOR_BETA.get(slug, 1.0)
    r_val = RF + beta * ERP
    return {"bv0_total_cr": bv0, "roe": roe, "g": g, "r_val": r_val, "beta": beta}, None


def excess_return_value_per_share(v):
    bv = v["bv0"]; roe = v["roe"]; g = v["g"]; r = v["r_val"]; tg = TG
    if r <= tg + 0.005:
        return None
    pv = bv
    for t in range(1, 6):
        prev_bv = bv
        bv = bv * (1 + g)
        excess = (roe - r) * prev_bv
        pv += excess / (1 + r) ** t
    tv = (roe - r) * bv * (1 + tg) / (r - tg)
    pv += tv / (1 + r) ** 5
    return pv


def qfv_check(fin, slug, fy_col, top_ratios, prices, d0):
    """Sec1.1 of specs/V3_9_DELTA.md, all four AND-gated."""
    pnl = fin[slug]["profit_loss"]
    bs = fin[slug]["balance_sheet"]
    cf = fin[slug]["cash_flow"]
    years = pnl["years"]
    bs_years = bs["years"]
    cf_years = cf["years"] if cf else []
    if fy_col not in years:
        return False, "FY column missing from P&L"
    idx = years.index(fy_col)
    hist_idx = [j for j in range(max(0, idx - 4), idx + 1)]
    if len(hist_idx) < 5:
        return False, f"only {len(hist_idx)} trailing FYs available (need 5)"

    rt = fin[slug].get("ratios_table")
    roic_vals = None
    if rt and "ROCE %" in rt["rows"]:
        roce_row = rt["rows"]["ROCE %"]
        ry = year_index(rt["years"], fy_col, len(roce_row))
        if ry is not None:
            rh = [j for j in range(max(0, ry - 4), ry + 1)]
            roic_vals = [num(roce_row[j]) / 100 if j < len(roce_row) and num(roce_row[j]) is not None else None for j in rh]
    if not roic_vals or any(x is None for x in roic_vals) or len(roic_vals) < 5:
        return False, "(a) ROIC/ROCE trailing-5FY series unavailable -- not QFV-qualified"
    roic_vals = sorted(roic_vals)
    median_roic = roic_vals[2]
    min_roic = min(roic_vals)
    if not (median_roic >= 0.15 and min_roic >= 0.10):
        return False, f"(a) median ROIC={median_roic:.1%} min={min_roic:.1%} -- fails 15%/10% bar"

    net_profit = [num(pnl["rows"]["Net Profit&nbsp;+"][j]) if "Net Profit&nbsp;+" in pnl["rows"] and j < len(pnl["rows"]["Net Profit&nbsp;+"]) else None for j in hist_idx]
    if any(x is None or x <= 0 for x in net_profit):
        return False, f"(b) PAT not positive in all 5 trailing FYs ({net_profit})"
    cfo = None
    if cf and "Cash from Operating Activity&nbsp;+" in cf["rows"]:
        cfo_row = cf["rows"]["Cash from Operating Activity&nbsp;+"]
        cy = year_index(cf_years, fy_col, len(cfo_row))
        if cy is not None:
            ch = [j for j in range(max(0, cy - 4), cy + 1)]
            cfo = [num(cfo_row[j]) if j < len(cfo_row) else None for j in ch]
    if not cfo or any(x is None for x in cfo) or len(cfo) < 5:
        return False, "(b) OCF trailing-5FY series unavailable"
    ratios = sorted(c / p for c, p in zip(cfo, net_profit))
    median_ocf_pat = ratios[2]
    if median_ocf_pat < 0.85:
        return False, f"(b) median OCF/PAT={median_ocf_pat:.2f} < 0.85"

    borrow = num(bs["rows"].get("Borrowings&nbsp;+", [None] * len(bs_years))[bs_years.index(fy_col)]) if "Borrowings&nbsp;+" in bs["rows"] and fy_col in bs_years else 0.0
    eq_cap = num(bs["rows"].get("Equity Capital", [None] * len(bs_years))[bs_years.index(fy_col)]) if fy_col in bs_years else None
    reserves = num(bs["rows"].get("Reserves", [None] * len(bs_years))[bs_years.index(fy_col)]) if fy_col in bs_years else None
    if eq_cap is None or reserves is None:
        return False, "(c) balance sheet equity unavailable"
    equity = eq_cap + reserves
    de = (borrow or 0.0) / equity if equity > 0 else None
    if de is None or de > 0.5:
        return False, f"(c) D/E={de} > 0.5"

    mcap_today = num(top_ratios[slug].get("Market Cap", "").replace("₹", "").strip())
    price_today = num(top_ratios[slug].get("Current Price", "").replace("₹", "").strip())
    if mcap_today is None or price_today is None or price_today <= 0:
        return False, "(d) current market cap/price unavailable"
    shares_cr = mcap_today / price_today
    price_at_d0 = None
    for d, p in prices:
        if d <= d0:
            price_at_d0 = p
        else:
            break
    if price_at_d0 is None:
        return False, "(d) no price at/near scoring date"
    mcap_at_d0 = shares_cr * price_at_d0
    if mcap_at_d0 < 5000:
        return False, f"(d) market cap at scoring date ~Rs{mcap_at_d0:.0f}cr < Rs5,000cr"

    return True, (f"QFV-qualified: median ROIC={median_roic:.1%} (min {min_roic:.1%}), "
                  f"median OCF/PAT={median_ocf_pat:.2f}, D/E={de:.2f}, "
                  f"mcap@d0~Rs{mcap_at_d0:.0f}cr")


def gev_veto_active(slug, check_date, log):
    """Sec2.2/2.3: any QUALIFYING event with event-date in the trailing 12mo
    before check_date, and not yet cooled off (12mo after event AND one
    audited annual print after event, whichever later -- approximated here
    as 12mo after event, since an annual print follows within a year for
    all 13 companies' regular FY cadence)."""
    for ev_date_s, tag, qualifies, note in log:
        if not qualifies:
            continue
        ev_date = D(ev_date_s)
        if ev_date <= check_date <= ev_date + timedelta(days=365):
            return True, ev_date_s, tag, note
    return False, None, None, None


def simulate_fill_with_gev(slug, d0, triggers, prices, log):
    """triggers: dict tier->price. Returns per-tier fill info, applying GEV
    at scoring date AND re-evaluated at each candidate fill date."""
    veto0, ev0, tag0, note0 = gev_veto_active(slug, d0, log)
    window = [(d, p) for d, p in prices if d0 < d <= d0 + DAYS24M]
    if not prices:
        return {}, veto0, ev0
    latest_date, latest_price = prices[-1]
    out = {}
    for tier, trg in triggers.items():
        if veto0:
            out[tier] = {"fill": None, "blocked_by_gev_at_scoring": True, "gev_event": ev0, "gev_tag": tag0}
            continue
        fill = None
        for d, p in window:
            if p <= trg:
                v, ev, tag, note = gev_veto_active(slug, d, log)
                if v:
                    out[tier] = {"fill": None, "blocked_by_gev_at_fill": True, "gev_event": ev,
                                 "gev_tag": tag, "would_have_filled": d.isoformat()}
                    fill = "VETOED"
                    break
                fill = (d, p)
                break
        if fill == "VETOED":
            continue
        if not fill:
            out[tier] = {"fill": None}
            continue
        fd, fp = fill
        fwd = [(d, p) for d, p in prices if fd < d <= fd + DAYS24M]
        out[tier] = {
            "fill_date": fd.isoformat(), "fill_price": fp, "trigger": round(trg, 2),
            "fwd_24m": round(fwd[-1][1] / fp, 3) if fwd else None,
            "fwd_months": round((fwd[-1][0] - fd).days / 30.44, 1) if fwd else None,
            "fwd_truncated": bool(fwd and fwd[-1][0] < fd + DAYS24M - timedelta(days=20)),
            "to_latest": round(latest_price / fp, 3), "to_latest_date": latest_date.isoformat(),
        }
    return out, veto0, ev0


def main():
    fin = json.load(open("full_financials_raw_v39.json"))
    top_ratios = json.load(open("top_ratios_v39.json"))

    usability_results = {}
    for key, slug, fy_col, d0s, cat, is_fin in NAME_DATES:
        v, r = usability(fin, slug, fy_col, D(d0s), is_fin)
        usability_results[key] = {"verdict": v, "reason": r, "category": cat, "financial_variant": is_fin}

    print("=== USABILITY ===")
    n_usable = 0
    for key, res in usability_results.items():
        print(f"  {key:26s} {res['verdict']:9s} {res['reason']}")
        if res["verdict"] == "USABLE":
            n_usable += 1
    print(f"\n{n_usable}/{len(NAME_DATES)} usable\n")

    print("=== FAIR VALUE + QFV + GEV + FILLS (usable only) ===")
    fill_results = {}
    for key, slug, fy_col, d0s, cat, is_fin in NAME_DATES:
        if usability_results[key]["verdict"] != "USABLE":
            continue
        d0 = D(d0s)
        prices = load_prices(slug)
        log = GEV_LOG.get(slug, [])

        if is_fin:
            v, err = excess_return_fair_value(fin, slug, fy_col)
            if v is None:
                fill_results[key] = {"status": f"FV_NOT_COMPUTABLE: {err}"}
                print(f"  {key:26s} FV NOT COMPUTABLE ({err})")
                continue
            tr = top_ratios[slug]
            mcap = num(tr.get("Market Cap", "").replace("₹", "").strip())
            price_now = num(tr.get("Current Price", "").replace("₹", "").strip())
            shares_cr = mcap / price_now
            v["bv0"] = v["bv0_total_cr"] / shares_cr
            fv_per_share = excess_return_value_per_share(v)
            if fv_per_share is None or fv_per_share <= 0:
                fill_results[key] = {"status": "excess-return FV degenerate"}
                continue
            qfv_ok, qfv_reason = False, "financial variant -- QFV gate (ROIC/OCF-PAT/D-E) not defined for bank/NBFC balance sheets; ACC/INV only"
            model_note = {"model": "excess-return/residual-income", "bvps0": round(v["bv0"], 2),
                          "roe": round(v["roe"], 4), "g": round(v["g"], 4), "r_val": round(v["r_val"], 4),
                          "shares_cr": round(shares_cr, 2)}
        else:
            v, err = dcf_fcff_fair_value(fin, slug, fy_col)
            if v is None:
                fill_results[key] = {"status": f"DCF_NOT_COMPUTABLE: {err}"}
                print(f"  {key:26s} DCF NOT COMPUTABLE ({err})")
                continue
            w = v["r_val"]
            ev_pv = dcf_value_pv(v, w)
            if ev_pv is None:
                fill_results[key] = {"status": "DCF degenerate (WACC <= terminal g + 0.5pp)"}
                continue
            bs = fin[slug]["balance_sheet"]
            bs_years = bs["years"]
            bs_idx = bs_years.index(fy_col) if fy_col in bs_years else None
            if bs_idx is not None:
                borrow = num(bs["rows"].get("Borrowings&nbsp;+", [None] * len(bs_years))[bs_idx]) or 0.0
                invest = num(bs["rows"].get("Investments", [None] * len(bs_years))[bs_idx]) or 0.0
            else:
                borrow = invest = 0.0
            net_cash = invest - borrow
            tr = top_ratios[slug]
            mcap = num(tr.get("Market Cap", "").replace("₹", "").strip())
            price_now = num(tr.get("Current Price", "").replace("₹", "").strip())
            shares_cr = mcap / price_now
            fv_total_cr = ev_pv + net_cash
            fv_per_share = fv_total_cr / shares_cr
            qfv_ok, qfv_reason = qfv_check(fin, slug, fy_col, top_ratios, prices, d0)
            model_note = {"model": "FCFF DCF", "wacc": round(w, 4), "growth": round(v["growth"], 4),
                          "beta": v["beta"], "net_cash_cr": round(net_cash, 1), "shares_cr": round(shares_cr, 2)}

        triggers = {"acc": round(0.875 * fv_per_share, 2), "inv": round(0.70 * fv_per_share, 2)}
        if qfv_ok:
            triggers["qfv"] = round(1.00 * fv_per_share, 2)

        fills, veto0, ev0 = simulate_fill_with_gev(slug, d0, triggers, prices, log)
        fill_results[key] = {
            "fair_value_per_share": round(fv_per_share, 2), "triggers": triggers,
            "qfv_qualified": qfv_ok, "qfv_reason": qfv_reason,
            "model": model_note, "category": cat, "financial_variant": is_fin,
            "gev_veto_at_scoring": veto0, "gev_event_at_scoring": ev0,
            "fills": fills,
        }
        tags = "+".join(t for t in triggers)
        print(f"  {key:26s} FV/sh={fv_per_share:>9.2f}  tiers={tags:12s} QFV={qfv_ok}  "
              f"GEV@scoring={veto0}  fills={ {t: fills[t].get('fill_date') for t in fills} }")

    json.dump({"usability": usability_results, "results": fill_results, "gev_log": GEV_LOG},
               open("oos_results_v39.json", "w"), indent=2, default=str)
    print("\nWrote oos_results_v39.json")

    # ---- four-line scorecard ----
    winner_names_filled = set()
    blowup_fills = 0
    blowup_fill_detail = []
    to_t_ratios = []
    m24 = []
    qfv_fills = []
    gev_vetoes = []
    for key, r in fill_results.items():
        if "fills" not in r:
            continue
        cat = r["category"]
        if r.get("gev_veto_at_scoring"):
            gev_vetoes.append((key, "at_scoring", r["gev_event_at_scoring"]))
        any_fill = False
        for tier, f in r["fills"].items():
            if f.get("blocked_by_gev_at_fill"):
                gev_vetoes.append((key, f"at_fill({tier})", f["gev_event"], f.get("would_have_filled")))
            if f.get("fill_date"):
                any_fill = True
                if tier == "qfv":
                    qfv_fills.append(key)
                if f.get("fwd_24m") is not None:
                    m24.append(f["fwd_24m"])
                if f.get("to_latest") is not None:
                    to_t_ratios.append(f["to_latest"])
        if any_fill:
            if cat == "winner":
                winner_names_filled.add(key.split("_")[0])
            if cat == "blowup":
                blowup_fills += 1
                blowup_fill_detail.append(key)
    print("\n=== SCORECARD ===")
    print(f"  Blow-up fills: {blowup_fills} {blowup_fill_detail} (need 0)")
    print(f"  Winner names with a fill: {len(winner_names_filled)} {sorted(winner_names_filled)} (need >=3 distinct)")
    print(f"  Mean to-latest-series-date ratio: "
          f"{sum(to_t_ratios)/len(to_t_ratios):.3f}x over {len(to_t_ratios)} fills" if to_t_ratios else "  no fills")
    print(f"  Mean 24m ratio: {sum(m24)/len(m24):.3f}x over {len(m24)} fills (need >=0.8x)" if m24 else "  no fills")
    print(f"\n  QFV fills: {qfv_fills}")
    print(f"  GEV vetoes: {gev_vetoes}")


if __name__ == "__main__":
    main()
