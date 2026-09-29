#!/usr/bin/env python3
"""
v3.10 OOS live-bar validation -- the one run (specs/V3_10_DELTA.md,
validation/v3_10_oos/OOS_SET_PREREG.md). No refit, no post-result changes.

Frozen inputs reused from validation/v3_9_oos/run_v39_validation.py (same
construction, same simplifications): usability check (a) at the results week,
FCFF DCF skeleton, excess-return skeleton for financial variants, QFV gate,
GEV veto, weekly-close fill replay, scorecard aggregation.

v3.10 changes (only these):
  1. g = min(ROE_avg3 * (1 - payout), 15%) replaces trailing revenue CAGR
     (floored 0, capped 12%).
  2. Explicit horizon 5 -> 10 years; margin fade still over years 1-5, flat
     after; terminal value at year 10; terminal g 4%.
  3. Financial variant: horizon 10y; BVPS growth = the same g.

CONVENTIONS ADOPTED WHERE THE DELTA IS SILENT (fixed before any figure was
computed; applied uniformly to every name-date; never tuned to results):
  C1  ROE_avg3 = mean over the last three FYs (scoring FY and the two before)
      of PAT_t / (Equity Capital_t + Reserves_t), each year on its own
      year-end book -- the same per-year-ratio construction the frozen v3.9
      financial-variant code already used for "trailing-3yr average ROE".
      Non-decisional sensitivity recorded: avg PAT / scoring-FY book.
  C2  Payout = screener "Dividend Payout %" of the scoring FY / 100, used
      as-is: >100% -> (1-payout) negative; negative payout -> (1-payout) > 1.
      No clipping. Missing/blank payout -> 0.0 (no dividend disclosed).
  C3  No floor on g (formula has none). Negative ROE_avg3 or payout >100%
      gives negative g, applied literally over the 10 explicit years.
  C4  Fewer than 3 FYs of history: mean over the FYs available (>= 1). Zero
      computable FYs -> fair value not computable -> no entry.
  C5  Negative or zero book equity in a year: ratio computed literally when
      book != 0 (sign included); book == 0 -> that year is skipped (C4).
  C6  Usability (a): the v3.9 harness rule (sourced FY EPS <= 0 -> EXCLUDED as
      basis defect) is kept. Check (b) (>8% implied-EPS step outside +-30d of
      an EPS publication, CONVENTIONS.md s3) is implemented and evaluated on
      the price/PE-implied EPS over the trailing-5-FY window of the name-date.
  C7  Usability-excluded name-dates are additionally valued in a clearly
      labelled SHADOW pass (non-decisional) so an exclusion can never hide a
      fill; shadow numbers do not enter the scorecard.
  C8  GEV: a scoring-date veto blocks the whole 24m window (v3.9 harness
      behaviour); a fill-date veto blocks only that fill. Cooling-off per
      s2.3: event active while d < max(event+365d, first Q4/annual-results
      publication date after the event); no such publication on record by d
      -> still active. Annual print = first vendor EPS publication after a
      31-Mar FY-end.
  C9  Sector betas below, fixed pre-run in the style of the v3.8/v3.9 tables.
"""
import csv
import json
import os
import re
import statistics
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
DAYS24M = timedelta(days=int(2 * 365.25))
TODAY = date(2026, 9, 29)

RF = 0.0695
ERP = 0.040
TG = 0.04
TAX = 0.2517
G_CAP = 0.15
HORIZON = 10
FADE_YEARS = 5
TIERS = {"acc": 0.875, "inv": 0.70, "qfv": 1.00}

SECTOR_BETA = {  # C9
    "dixon": 1.10, "hal": 0.90, "bel": 0.90, "coforge": 0.95, "tatapower": 1.10,
    "hul": 0.55, "bajajauto": 0.85, "petronet": 0.80, "bpcl": 1.00, "powergrid": 0.75,
    "coffeeday": 1.15, "gensol": 1.30, "lvb": 1.15,
}

TAGS = {"regulatory_probe", "auditor_event", "promoter_conduct",
        "withdrawn_capital_action", "criminal_legal", "associate_contagion"}

# (key, slug, scoring FY column, scoring date, category, financial_variant)
NAME_DATES = [
    ("dixon_2019-03-31", "dixon", "Mar 2019", "2019-03-31", "winner", False),
    ("dixon_2021-03-31", "dixon", "Mar 2021", "2021-03-31", "winner", False),
    ("hal_2019-03-31", "hal", "Mar 2019", "2019-03-31", "winner", False),
    ("hal_2021-03-31", "hal", "Mar 2021", "2021-03-31", "winner", False),
    ("bel_2019-03-31", "bel", "Mar 2019", "2019-03-31", "winner", False),
    ("bel_2021-03-31", "bel", "Mar 2021", "2021-03-31", "winner", False),
    ("coforge_2019-03-31", "coforge", "Mar 2019", "2019-03-31", "winner", False),
    ("coforge_2021-03-31", "coforge", "Mar 2021", "2021-03-31", "winner", False),
    ("tatapower_2020-03-31", "tatapower", "Mar 2020", "2020-03-31", "winner", False),
    ("tatapower_2021-03-31", "tatapower", "Mar 2021", "2021-03-31", "winner", False),
    ("hul_2021-03-31", "hul", "Mar 2021", "2021-03-31", "mediocre", False),
    ("hul_2022-03-31", "hul", "Mar 2022", "2022-03-31", "mediocre", False),
    ("bajajauto_2019-03-31", "bajajauto", "Mar 2019", "2019-03-31", "mediocre", False),
    ("bajajauto_2021-03-31", "bajajauto", "Mar 2021", "2021-03-31", "mediocre", False),
    ("petronet_2019-03-31", "petronet", "Mar 2019", "2019-03-31", "mediocre", False),
    ("petronet_2021-03-31", "petronet", "Mar 2021", "2021-03-31", "mediocre", False),
    ("bpcl_2019-03-31", "bpcl", "Mar 2019", "2019-03-31", "mediocre", False),
    ("bpcl_2021-03-31", "bpcl", "Mar 2021", "2021-03-31", "mediocre", False),
    ("powergrid_2019-03-31", "powergrid", "Mar 2019", "2019-03-31", "mediocre", False),
    ("powergrid_2021-03-31", "powergrid", "Mar 2021", "2021-03-31", "mediocre", False),
    ("coffeeday_2019-03-31", "coffeeday", "Mar 2019", "2019-03-31", "blowup", False),
    ("coffeeday_2020-03-31", "coffeeday", "Mar 2020", "2020-03-31", "blowup", False),
    ("gensol_2023-03-31", "gensol", "Mar 2023", "2023-03-31", "blowup", False),
    ("gensol_2024-03-31", "gensol", "Mar 2024", "2024-03-31", "blowup", False),
    ("lvb_2019-03-31", "lvb", "Mar 2019", "2019-03-31", "blowup", True),
]


def D(s):
    return date.fromisoformat(s)


def num(s):
    if s is None or s == "":
        return None
    try:
        return float(str(s).replace(",", "").replace("%", "").replace("₹", "").strip())
    except ValueError:
        return None


def fy_end(fy_col):
    return date(int(fy_col.split()[1]), 3, 31)


def fy_shift(fy_col, k):
    return f"Mar {int(fy_col.split()[1]) + k}"


# ---------------------------------------------------------------- table access
def cell(tbl, row, fy_col):
    """Value of `row` at FY column label `fy_col`, aligned by the table's own
    year header (ratio tables repeat the header list for embedded sub-tables)."""
    if not tbl or row not in tbl["rows"]:
        return None
    vals = tbl["rows"][row]
    yrs = tbl["years"][:len(vals)]
    if fy_col not in yrs:
        return None
    return num(vals[yrs.index(fy_col)])


def window_cols(fy_col, n, tbl):
    """The last n FY labels ending at fy_col that exist in tbl's header."""
    cols = [fy_shift(fy_col, -k) for k in range(n - 1, -1, -1)]
    return [c for c in cols if c in tbl["years"]]


def load_prices(slug):
    rows = []
    with open(f"{HERE}/pe_series/{slug}.csv", newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["price"]:
                rows.append((D(r["date"]), float(r["price"]), num(r["pe"])))
    rows.sort()
    return rows


def load_eps_series(slug):
    d = json.load(open(f"{HERE}/eps_series/{slug}.json"))
    return sorted((D(dt[:10]), v) for dt, v in d["values"])


# ------------------------------------------------------------------- usability
def results_week_ttm(eps_series, fyend):
    """Median vendor TTM over results-week..+21d, where results week = the
    first publication-dated EPS point after the FY-end (within 183d)."""
    cands = [(d, v) for d, v in eps_series if fyend < d <= fyend + timedelta(days=183)]
    if not cands:
        return None
    r0 = cands[0][0]
    win = [v for d, v in eps_series if r0 <= d <= r0 + timedelta(days=21)]
    return r0, statistics.median(win)


def basis_diagnostic(fin, slug, fy_col, actions):
    """CONVENTIONS s4 step 1-2: is the audited EPS row already on the vendor's
    (post-action) basis?  Implied shares = NP/EPS at fy_col vs at the first FY
    ending after the last action ex-date that follows fy_col.  Nearest of
    {1, cumulative factor F} decides; ties/indeterminate -> no restatement."""
    fe = fy_end(fy_col)
    later = [a for a in actions if D(a["ex_date"]) > fe]
    if not later:
        return {"actions_after_fy_end": [], "factor": 1.0, "restate": False, "basis": "no action after FY-end"}
    F = 1.0
    for a in later:
        F *= a["numerator"] / a["denominator"]
    last_ex = max(D(a["ex_date"]) for a in later)
    pnl = fin[slug]["profit_loss"]
    ref = next((c for c in pnl["years"] if c.startswith("Mar") and fy_end(c) > last_ex), None)
    out = {"actions_after_fy_end": [(a["ex_date"], a["ratio_text"]) for a in later], "cumulative_factor": round(F, 4)}
    if ref is None:
        return {**out, "factor": 1.0, "restate": False, "basis": "indeterminate: no FY after last ex-date; no restatement"}
    s0 = (cell(pnl, "Net Profit&nbsp;+", fy_col) or 0) / (cell(pnl, "EPS in Rs", fy_col) or float("nan"))
    s1 = (cell(pnl, "Net Profit&nbsp;+", ref) or 0) / (cell(pnl, "EPS in Rs", ref) or float("nan"))
    ratio = s1 / s0 if s0 and s0 == s0 and s1 == s1 else None
    if ratio is None or ratio <= 0:
        return {**out, "factor": 1.0, "restate": False, "basis": "indeterminate (non-positive NP/EPS); no restatement"}
    if abs(ratio - 1) <= abs(ratio - F):
        return {**out, "implied_shares_ratio": round(ratio, 3), "factor": 1.0, "restate": False,
                "basis": f"already on vendor post-action basis (implied shares {fy_col}->{ref} x{ratio:.2f} ~ 1, not x{F:.2f})"}
    return {**out, "implied_shares_ratio": round(ratio, 3), "factor": F, "restate": True,
            "basis": f"unadjusted: implied shares x{ratio:.2f} ~ cumulative factor {F:.2f}; audited EPS restated /F"}


def check_b(prices, eps_series, d0, fy_col):
    start = fy_end(fy_shift(fy_col, -5)) + timedelta(days=1)  # Apr-1 of FY(N-4)
    pub = [d for d, _ in eps_series]
    pts = [(d, p / pe) for d, p, pe in prices if pe and pe > 0 and start <= d <= d0]
    fired = []
    for (da, ea), (db, eb) in zip(pts, pts[1:]):
        step = eb / ea - 1
        if abs(step) > 0.08 and not any(abs((db - x).days) <= 30 for x in pub):
            fired.append((db.isoformat(), round(step * 100, 1)))
    return fired


def usability(fin, slug, fy_col, d0, is_fin, prices, eps_series, actions):
    pnl = fin[slug]["profit_loss"]
    if fy_col not in pnl["years"]:
        return "EXCLUDED", "structural", f"FY column {fy_col} not in fetched P&L years", {}
    if is_fin:
        return "USABLE", "exempt", "financial variant -- exempt from check (a)/(b) per V3_7_DELTA s4", {}
    diag = basis_diagnostic(fin, slug, fy_col, actions)
    sourced = cell(pnl, "EPS in Rs", fy_col)
    if sourced is None:
        return "EXCLUDED", "(a)-structural", "no sourced audited EPS at this FY", {"basis": diag}
    if diag["restate"]:
        sourced = sourced / diag["factor"]
    rw = results_week_ttm(eps_series, d0)
    if rw is None:
        return "EXCLUDED", "(a)-structural", "no PIT vendor EPS within 6mo after FY-end", {"basis": diag}
    rw_date, rw_val = rw
    b = check_b(prices, eps_series, d0, fy_col)
    extra = {"basis": diag, "check_b_unexplained_steps": b, "sourced_eps": sourced,
             "vendor_ttm": rw_val, "results_week": rw_date.isoformat()}
    if sourced <= 0:
        return "EXCLUDED", "(a)", (f"sourced FY EPS non-positive ({sourced}) while vendor TTM {rw_val} @ {rw_date} "
                                    "-- basis defect (v3.9 harness rule)"), extra
    gap = (rw_val / sourced - 1) * 100
    if abs(gap) > 15:
        return "EXCLUDED", "(a)", f"(a) {gap:+.1f}% @pub {rw_date} TTM={rw_val} src={sourced} (>15%)", extra
    if b:
        return "EXCLUDED", "(b)", f"(a) ok ({gap:+.1f}%) but unexplained >8% implied-EPS step(s): {b}", extra
    return "USABLE", "none", f"(a) {gap:+.1f}% @pub {rw_date} TTM={rw_val} src={sourced}; (b) no unexplained step", extra


# ------------------------------------------------------------------- valuation
def roe_terms(fin, slug, fy_col):
    pnl, bs = fin[slug]["profit_loss"], fin[slug]["balance_sheet"]
    per_year, pats = [], []
    for c in window_cols(fy_col, 3, pnl):
        pat = cell(pnl, "Net Profit&nbsp;+", c)
        ec, res = cell(bs, "Equity Capital", c), cell(bs, "Reserves", c)
        if pat is None or ec is None or res is None or (ec + res) == 0:
            continue
        per_year.append({"fy": c, "pat": pat, "book": ec + res, "roe": pat / (ec + res)})
        pats.append(pat)
    return per_year, pats


def sustainable_growth(fin, slug, fy_col):
    per_year, pats = roe_terms(fin, slug, fy_col)
    if not per_year:
        return None, "no computable ROE year (C4)"
    roe_avg3 = sum(y["roe"] for y in per_year) / len(per_year)
    pnl = fin[slug]["profit_loss"]
    payout_raw = cell(pnl, "Dividend Payout %", fy_col)
    payout = 0.0 if payout_raw is None else payout_raw / 100
    g = min(roe_avg3 * (1 - payout), G_CAP)
    book_end = per_year[-1]["book"] if per_year[-1]["fy"] == fy_col else None
    alt_roe = (sum(pats) / len(pats)) / book_end if book_end else None
    alt_g = min(alt_roe * (1 - payout), G_CAP) if alt_roe is not None else None
    return {"roe_avg3": roe_avg3, "payout": payout, "payout_raw": payout_raw, "g": g,
            "roe_years": per_year, "alt_roe": alt_roe, "alt_g": alt_g,
            "g_cap_binding": roe_avg3 * (1 - payout) > G_CAP}, None


def dcf_inputs(fin, slug, fy_col):
    pnl = fin[slug]["profit_loss"]
    if fy_col not in pnl["years"]:
        return None, "FY column missing"
    cols = window_cols(fy_col, 5, pnl)
    sales = [cell(pnl, "Sales&nbsp;+", c) for c in cols]
    opm = [cell(pnl, "OPM %", c) for c in cols]
    dep = [cell(pnl, "Depreciation", c) for c in cols]
    rev0 = sales[-1]
    if rev0 is None or rev0 <= 0:
        return None, "non-positive/missing revenue in the scoring FY"
    opm_vals = [x / 100 for x in opm if x is not None]
    ms = opm_vals[-1] if opm_vals else 0.15
    me = (sum(opm_vals) / len(opm_vals)) if len(opm_vals) >= 3 else ms
    dep_vals = [d / s for d, s in zip(dep, sales) if d is not None and s]
    dep_pct = (sum(dep_vals) / len(dep_vals)) if dep_vals else 0.03
    sg, err = sustainable_growth(fin, slug, fy_col)
    if sg is None:
        return None, err
    beta = SECTOR_BETA[slug]
    return {"rev0": rev0, "growth": sg["g"], "sg": sg, "margin_start": ms, "margin_end": me,
            "capex_pct": dep_pct, "dep_pct": dep_pct, "wc_pct": 0.05,
            "r_val": RF + beta * ERP, "beta": beta, "fy_cols_used": cols}, None


def dcf_value_pv(v, w, growth=None):
    g_ = v["growth"] if growth is None else growth
    rev0, ms, me = v["rev0"], v["margin_start"], v["margin_end"]
    cp = v["capex_pct"]
    dp = v["dep_pct"]
    wc = v["wc_pct"]
    r, pv = rev0, 0.0
    for i in range(1, HORIZON + 1):
        prev = r
        r = prev * (1 + g_)
        m = ms + (me - ms) * (min(i, FADE_YEARS) / FADE_YEARS)
        nopat = r * (m - dp) * (1 - TAX)
        fcff = nopat + r * dp - r * cp - (r - prev) * wc
        pv += fcff / (1 + w) ** i
    if w <= TG + 0.005:
        return None
    nopat_n = r * (me - dp) * (1 - TAX)
    fcff_norm = nopat_n - (r * TG / (1 + TG)) * wc
    tv = fcff_norm * (1 + TG) / (w - TG)
    return pv + tv / (1 + w) ** HORIZON


def excess_return_inputs(fin, slug, fy_col):
    sg, err = sustainable_growth(fin, slug, fy_col)
    if sg is None:
        return None, err
    last = sg["roe_years"][-1]
    if last["fy"] != fy_col:
        return None, "scoring-FY book value unavailable"
    beta = SECTOR_BETA[slug]
    return {"bv0_total_cr": last["book"], "roe": sg["roe_avg3"], "g": sg["g"], "sg": sg,
            "r_val": RF + beta * ERP, "beta": beta}, None


def excess_return_per_share(v, growth=None):
    g_ = v["g"] if growth is None else growth
    bv, roe, r = v["bv0"], v["roe"], v["r_val"]
    if r <= TG + 0.005:
        return None
    pv = bv
    for t in range(1, HORIZON + 1):
        prev = bv
        bv = bv * (1 + g_)
        pv += (roe - r) * prev / (1 + r) ** t
    tv = (roe - r) * bv * (1 + TG) / (r - TG)
    return pv + tv / (1 + r) ** HORIZON


# ------------------------------------------------------------------------- QFV
def qfv_check(fin, slug, fy_col, shares_cr, prices, d0):
    pnl, bs, cf = fin[slug]["profit_loss"], fin[slug]["balance_sheet"], fin[slug]["cash_flow"]
    rt = fin[slug]["ratios_table"]
    cols = window_cols(fy_col, 5, pnl)
    if len(cols) < 5 or cols[-1] != fy_col:
        return False, f"only {len(cols)} trailing FYs available in the fetched P&L (need 5) -- not evaluable"
    roic = [cell(rt, "ROCE %", c) for c in cols]
    if any(x is None for x in roic):
        return False, "(a) ROIC/ROCE trailing-5FY series unavailable -- not QFV-qualified"
    roic = sorted(x / 100 for x in roic)
    med, mn = roic[2], roic[0]
    if not (med >= 0.15 and mn >= 0.10):
        return False, f"(a) median ROIC={med:.1%} min={mn:.1%} -- fails 15%/10% bar"
    pat = [cell(pnl, "Net Profit&nbsp;+", c) for c in cols]
    if any(x is None or x <= 0 for x in pat):
        return False, f"(b) PAT not positive in all 5 trailing FYs ({pat})"
    cfo = [cell(cf, "Cash from Operating Activity&nbsp;+", c) for c in cols]
    if any(x is None for x in cfo):
        return False, "(b) OCF trailing-5FY series unavailable"
    med_ratio = sorted(c / p for c, p in zip(cfo, pat))[2]
    if med_ratio < 0.85:
        return False, f"(b) median OCF/PAT={med_ratio:.2f} < 0.85"
    borrow = cell(bs, "Borrowings&nbsp;+", fy_col)
    ec, res = cell(bs, "Equity Capital", fy_col), cell(bs, "Reserves", fy_col)
    if ec is None or res is None or borrow is None:
        return False, "(c) balance sheet equity/borrowings unavailable"
    eq = ec + res
    de = borrow / eq if eq > 0 else None
    if de is None or de > 0.5:
        return False, f"(c) D/E={de} > 0.5"
    p0 = [p for d, p, _ in prices if d <= d0]
    if not p0:
        return False, "(d) no price at/near scoring date"
    mcap0 = shares_cr * p0[-1]
    if mcap0 < 5000:
        return False, f"(d) market cap at scoring date ~Rs{mcap0:.0f}cr < Rs5,000cr"
    return True, (f"QFV-qualified: median ROIC={med:.1%} (min {mn:.1%}), median OCF/PAT={med_ratio:.2f}, "
                  f"D/E={de:.2f}, mcap@d0~Rs{mcap0:.0f}cr")


# ------------------------------------------------------------------------- GEV
def load_gev(slug):
    path = f"{HERE}/governance_logs/{slug}.md"
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"##\s+Qualifying events.*?\n(.*?)(?=\n##\s|\Z)", txt, re.S)
    events = []
    for line in (m.group(1) if m else "").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells[0]):
            tag = cells[1].strip("` ")
            assert tag in TAGS, (slug, cells[0], tag)
            events.append((cells[0], tag, cells[2]))
    return sorted(events)


def annual_prints(eps_series):
    out = []
    for y in range(2014, 2027):
        fe = date(y, 3, 31)
        c = [d for d, _ in eps_series if fe < d <= fe + timedelta(days=200)]
        if c:
            out.append(c[0])
    return out


def gev_active(check_date, events, prints):
    for ev_s, tag, desc in events:
        ev = D(ev_s)
        if ev > check_date:
            continue
        after = [p for p in prints if p > ev]
        end = max(ev + timedelta(days=365), after[0]) if after else None
        # `end` is the later of event+12m and the first annual print after the
        # event; a print not yet published at check_date lies after it, so the
        # veto is still active (PIT-safe). No print on record -> never clears.
        if end is None or check_date < end:
            return True, ev_s, tag
    return False, None, None


def simulate_fills(slug, d0, triggers, prices, events, prints):
    veto0 = gev_active(d0, events, prints)
    window = [(d, p) for d, p, _ in prices if d0 < d <= d0 + DAYS24M]
    latest_date, latest_price = prices[-1][0], prices[-1][1]
    out = {}
    for tier, trg in triggers.items():
        if veto0[0]:
            out[tier] = {"fill": None, "blocked_by_gev_at_scoring": True, "gev_event": veto0[1], "gev_tag": veto0[2]}
            continue
        res = {"fill": None}
        for d, p in window:
            if p <= trg:
                v = gev_active(d, events, prints)
                if v[0]:
                    res = {"fill": None, "blocked_by_gev_at_fill": True, "gev_event": v[1],
                           "gev_tag": v[2], "would_have_filled": d.isoformat()}
                else:
                    fwd = [(dd, pp) for dd, pp, _ in prices if d < dd <= d + DAYS24M]
                    res = {"fill_date": d.isoformat(), "fill_price": p, "trigger": round(trg, 2),
                           "fwd_24m": round(fwd[-1][1] / p, 3) if fwd else None,
                           "fwd_truncated": bool(fwd and fwd[-1][0] < d + DAYS24M - timedelta(days=20)),
                           "to_latest": round(latest_price / p, 3), "to_latest_date": latest_date.isoformat()}
                break
        out[tier] = res
    return out, veto0


# ------------------------------------------------------------------------ main
def value_name_date(fin, top, slug, fy_col, d0, is_fin, prices):
    """Fair value/share + tiers. Returns (dict, error)."""
    mcap, px_now = num(top[slug].get("Market Cap")), num(top[slug].get("Current Price"))
    if not mcap or not px_now:
        return None, "market cap / current price unavailable on screener top-ratios"
    shares_cr = mcap / px_now
    bs = fin[slug]["balance_sheet"]
    if is_fin:
        v, err = excess_return_inputs(fin, slug, fy_col)
        if v is None:
            return None, f"FV_NOT_COMPUTABLE: {err}"
        v["bv0"] = v["bv0_total_cr"] / shares_cr
        fv = excess_return_per_share(v)
        fv_alt = excess_return_per_share(v, growth=v["sg"]["alt_g"]) if v["sg"]["alt_g"] is not None else None
        model = {"model": "excess-return 10y", "bvps0": round(v["bv0"], 2), "roe_avg3": round(v["roe"], 4),
                 "g": round(v["g"], 4), "r_val": round(v["r_val"], 4), "beta": v["beta"]}
    else:
        v, err = dcf_inputs(fin, slug, fy_col)
        if v is None:
            return None, f"DCF_NOT_COMPUTABLE: {err}"
        w = v["r_val"]
        ev = dcf_value_pv(v, w)
        if ev is None:
            return None, "DCF degenerate (WACC <= terminal g + 0.5pp)"
        net_cash = (cell(bs, "Investments", fy_col) or 0.0) - (cell(bs, "Borrowings&nbsp;+", fy_col) or 0.0)
        fv = (ev + net_cash) / shares_cr
        ev_alt = dcf_value_pv(v, w, growth=v["sg"]["alt_g"]) if v["sg"]["alt_g"] is not None else None
        fv_alt = (ev_alt + net_cash) / shares_cr if ev_alt is not None else None
        model = {"model": "FCFF DCF 10y", "wacc": round(w, 4), "beta": v["beta"], "g": round(v["growth"], 4),
                 "margin_start": round(v["margin_start"], 4), "margin_end": round(v["margin_end"], 4),
                 "dep_pct": round(v["dep_pct"], 4), "net_cash_cr": round(net_cash, 1)}
    sg = v["sg"]
    model.update({"roe_avg3": round(sg["roe_avg3"], 4), "payout": sg["payout"], "payout_raw": sg["payout_raw"],
                  "g_cap_binding": sg["g_cap_binding"], "roe_years": [(y["fy"], round(y["roe"], 4)) for y in sg["roe_years"]],
                  "shares_cr": round(shares_cr, 3)})
    p0 = [p for d, p, _ in prices if d <= d0]
    price0 = p0[-1] if p0 else None
    win = [p for d, p, _ in prices if d0 < d <= d0 + DAYS24M]
    return {"fv": fv, "fv_alt_roe_convention": fv_alt, "shares_cr": shares_cr, "model": model,
            "price_at_d0": price0, "price_over_fv_d0": (price0 / fv) if fv and fv > 0 and price0 else None,
            "min_close_24m_over_fv": (min(win) / fv) if win and fv and fv > 0 else None}, None


def run_one(key, slug, fy_col, d0s, cat, is_fin, fin, top, usab, shadow):
    d0 = D(d0s)
    prices = load_prices(slug)
    events = load_gev(slug)
    prints = annual_prints(load_eps_series(slug))
    val, err = value_name_date(fin, top, slug, fy_col, d0, is_fin, prices)
    if val is None:
        return {"status": err, "category": cat, "financial_variant": is_fin, "shadow": shadow}
    fv = val["fv"]
    if is_fin:
        qfv_ok, qfv_reason = False, "financial variant -- QFV gate not defined for bank balance sheets; ACC/INV only (v3.9 scope limit, unchanged)"
    else:
        qfv_ok, qfv_reason = qfv_check(fin, slug, fy_col, val["shares_cr"], prices, d0)
    if fv <= 0:
        return {"status": f"fair value non-positive ({fv:.2f}/share) -- no positive trigger exists", **val,
                "category": cat, "financial_variant": is_fin, "qfv_qualified": qfv_ok, "qfv_reason": qfv_reason,
                "fills": {}, "shadow": shadow}
    triggers = {t: round(m * fv, 2) for t, m in TIERS.items() if t != "qfv" or qfv_ok}
    fills, veto0 = simulate_fills(slug, d0, triggers, prices, events, prints)
    return {"status": "ok", **val, "category": cat, "financial_variant": is_fin, "triggers": triggers,
            "qfv_qualified": qfv_ok, "qfv_reason": qfv_reason,
            "gev_veto_at_scoring": veto0[0], "gev_event_at_scoring": veto0[1], "gev_tag_at_scoring": veto0[2],
            "gev_events_logged": [(e[0], e[1]) for e in events], "fills": fills, "shadow": shadow}


def scorecard(results):
    winners, bu, bu_detail, to_t, m24, qfv, vetoes = set(), 0, [], [], [], [], []
    for key, r in results.items():
        if r.get("shadow") or "fills" not in r:
            continue
        if r.get("gev_veto_at_scoring"):
            vetoes.append((key, "at_scoring", r["gev_event_at_scoring"]))
        any_fill = False
        for tier, f in r["fills"].items():
            if f.get("blocked_by_gev_at_fill"):
                vetoes.append((key, f"at_fill({tier})", f["gev_event"], f["would_have_filled"]))
            if f.get("fill_date"):
                any_fill = True
                if tier == "qfv":
                    qfv.append(key)
                if f.get("fwd_24m") is not None:
                    m24.append(f["fwd_24m"])
                to_t.append(f["to_latest"])
        if any_fill and r["category"] == "winner":
            winners.add(key.split("_")[0])
        if any_fill and r["category"] == "blowup":
            bu += 1
            bu_detail.append(key)
    return {"blowup_fills": bu, "blowup_fill_name_dates": bu_detail, "winner_names_filled": sorted(winners),
            "n_fills_to_t": len(to_t), "mean_to_t": (sum(to_t) / len(to_t)) if to_t else None,
            "n_fills_24m": len(m24), "mean_24m": (sum(m24) / len(m24)) if m24 else None,
            "qfv_fills": qfv, "gev_vetoes": vetoes}


def main():
    fin = json.load(open(f"{HERE}/full_financials_raw_v310.json"))
    top = json.load(open(f"{HERE}/top_ratios_v310.json"))
    usab_out, results = {}, {}
    for key, slug, fy_col, d0s, cat, is_fin in NAME_DATES:
        prices = load_prices(slug)
        eps = load_eps_series(slug)
        actions = json.load(open(f"{HERE}/corp_actions/{slug}.json"))["actions"]
        v, fired, reason, extra = usability(fin, slug, fy_col, D(d0s), is_fin, prices, eps, actions)
        usab_out[key] = {"verdict": v, "fired": fired, "reason": reason, "category": cat, "financial_variant": is_fin, **extra}
    print("=== USABILITY (frozen v3.7 test, applied first) ===")
    for k, u in usab_out.items():
        print(f"  {k:24s} {u['verdict']:9s} fired={u['fired']:14s} {u['reason']}")
    print(f"\n{sum(u['verdict'] == 'USABLE' for u in usab_out.values())}/{len(NAME_DATES)} usable\n")

    print("=== VALUATION / QFV / GEV / FILLS ===")
    for key, slug, fy_col, d0s, cat, is_fin in NAME_DATES:
        shadow = usab_out[key]["verdict"] != "USABLE"
        r = run_one(key, slug, fy_col, d0s, cat, is_fin, fin, top, usab_out[key], shadow)
        results[key] = r
        fills = {t: f.get("fill_date") or ("VETO@fill" if f.get("blocked_by_gev_at_fill") else ("VETO@score" if f.get("blocked_by_gev_at_scoring") else None))
                 for t, f in r.get("fills", {}).items()}
        fvs = f"{r['fv']:.2f}" if "fv" in r else "n/a"
        pr = f"{r['price_over_fv_d0']:.2f}" if r.get("price_over_fv_d0") else "n/a"
        print(f"  {'[SHADOW] ' if shadow else ''}{key:24s} FV/sh={fvs:>10} P/FV@d0={pr:>6} QFV={r.get('qfv_qualified')} "
              f"GEV@score={r.get('gev_veto_at_scoring')} fills={fills} status={r['status']}")

    sc = scorecard(results)
    print("\n=== SCORECARD (decisional, usable name-dates only) ===")
    print(json.dumps(sc, indent=1, default=str))
    json.dump({"usability": usab_out, "results": results, "scorecard": sc, "betas": SECTOR_BETA},
              open(f"{HERE}/oos_results_v310.json", "w"), indent=2, default=str)
    print("\nWrote oos_results_v310.json")


if __name__ == "__main__":
    main()
