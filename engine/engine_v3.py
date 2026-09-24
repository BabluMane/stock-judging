#!/usr/bin/env python3
"""
Equity Review Standard v3 — deterministic scoring engine (engine v3.0).

Implements "Equity Review Standard v3 — Full Scoring Spec" (approved 23 Sep 2026).
The v2 engine (engine_v2.py) is kept unchanged and runnable for the archive;
v2 and v3 scores are never blended or ranked together.

    python3 engine_v3.py input.json            # full JSON results
    python3 engine_v3.py input.json --pretty   # readable summary (refuses on any mismatch)

Design rules
  * Two rates: r_val (market-consistent, values the business) and r_hurdle (15%,
    sets the entry trigger only). Every use is explicit in the code and output.
  * Quality Q and Price P are separate. P is computed at the trigger (tiering)
    and at today's price (timing).
  * Unverifiable forensic checks are excluded from B's denominator, never zeroed.
  * Every numeric threshold interpolates inside its knife-edge band (spec §8).
  * Dimension totals are recomputed from test scores and checked; the engine
    refuses to render on any mismatch or out-of-range score.
  * Missing inputs are never guessed. A required input that is absent is an error,
    not a default (beta, beta_source, net_cash, bear_triggers). A net-debt name with no
    debt_wt / D/E is weighted at market values (net debt vs market cap) — the actual structure.
"""

import json, sys, math
from datetime import datetime, timezone, timedelta

ENGINE_VERSION = "engine v3.0"
STANDARD = "Standard v3"

# ══════════════════════════════════════════════════════════════════════════
# 0. MACRO BLOCKS (spec §1, §11) — fixed per results season; overridable via input["macro"]
# ══════════════════════════════════════════════════════════════════════════

MACRO = {
    "IN": {
        "jurisdiction": "IN", "currency": "INR", "money_unit": "Rs Cr", "sym": "₹",
        "rf": 0.0695,              # India 10-yr G-Sec; re-run every DCF if it moves >= 25bp
        "erp_val": 0.040,          # r_val = rf + beta x 4.0%  (spec §1)
        "hurdle": 0.15,            # r_hurdle — entry decision only
        "tax_floor": 0.2517,       # tax = max(company, 25.17%)
        "tax_terminal": None,      # None = same as explicit-period tax
        "terminal_g_cap": 0.04,    # one rule: <= 4%, default 4%
        "terminal_g_default": 0.04,
        "kd_spread": 0.02,         # pre-tax cost of debt = rf + 2%
        "liq_ref": 1.0,            # Rs 1 Cr reference position (comparability constant)
        "pit_abs_threshold": 50.0, # C6: net promoter buy > Rs 50 Cr scores 2
        "beta_benchmark": "Nifty 500, two-year weekly",
        "tbill_3m": None,
        "calibration": "v3.0",
    },
    "US": {
        "jurisdiction": "US", "currency": "USD", "money_unit": "USD m", "sym": "US$",
        "rf": 0.0496,              # UST 10-yr, 21 Sep 2026
        "erp_val": 0.040,          # r_val = 4.96% + beta x 4.0%
        "hurdle": 0.15,            # same personal bar in USD — FLAGGED for Bablu's review (spec §11)
        "tax_floor": 0.21,         # USA engine rule retained: max(company, 21%) explicit
        "tax_terminal": 0.25,      # 25% terminal
        "terminal_g_cap": 0.04,
        "terminal_g_default": 0.04,
        "kd_spread": 0.02,
        "liq_ref": 125000.0,       # USD reference position (in USD, not millions)
        "pit_abs_threshold": 6.0,  # C6 absolute limb, USD m (~Rs 50 Cr) — FLAGGED: not in spec
        "beta_benchmark": "S&P 500, two-year weekly",
        "tbill_3m": 0.0417,
        "calibration": "USA-cal v3.0",
    },
}

WEIGHTS = {"A": 0.15, "B": 0.20, "C": 0.20, "D": 0.15, "E": 0.20, "F": 0.10}
Q_DIMS, P_DIMS = ("A", "B", "C", "F"), ("D", "E")
TEST_COUNT = {"A": 6, "C": 6, "D": 5, "E": 5, "F": 5}
PLEDGE_FLOOR = 0.005            # check 9 materiality floor: 0.5% of shares outstanding
G1_MIN_PASS_RATE = 0.60
G1_MIN_VERIFIED = {10: 7, 8: 6}  # 8-check financial variant: 6 of 8 (interpretation — see notes)
BEAR_BASE, BEAR_STEP, BEAR_CAP = 0.25, 0.05, 0.45

# Tests the engine owns outright — a manual score for these is refused (spec §3 "Engine" mode)
ENGINE_ONLY = {"A1", "D1", "D3", "E1", "E2", "E3", "E4"}
# Price-dependent tests: scored separately at the trigger and at today's price
PRICE_TESTS = {"D1", "D2", "D3", "D4", "E1", "E2", "E3", "E4"}


class RenderRefused(Exception):
    """Raised when the engine must not render (spec §9 item 10 and input-integrity rules)."""


def g(d, *path, default=None):
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur or cur[k] is None:
            return default
        cur = cur[k]
    return cur


def pct(x, nd=2):
    return None if x is None else round(x * 100, nd)


def today_ist():
    return datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d")


def today_et():
    now = datetime.now(timezone.utc)
    y = now.year
    def nth_sunday(month, n):
        d = datetime(y, month, 1, tzinfo=timezone.utc)
        return d + timedelta(days=(6 - d.weekday()) % 7) + timedelta(weeks=n - 1)
    start = nth_sunday(3, 2) + timedelta(hours=7)
    end = nth_sunday(11, 1) + timedelta(hours=6)
    off = -4 if start <= now < end else -5
    return now.astimezone(timezone(timedelta(hours=off))).strftime("%Y-%m-%d")


# ══════════════════════════════════════════════════════════════════════════
# 1. ANTI-KNIFE-EDGE LADDER (spec §8)
# ══════════════════════════════════════════════════════════════════════════

def ladder(x, thresholds, levels, higher_better=True, mode="rel", pp=0.01, interpolate=True):
    """Score x against ordered thresholds.

    thresholds: ascending in the *better* direction's measurement (for lower-better tests pass
                them ascending in raw units; they are handled by negation).
    levels:     len(thresholds)+1 scores, worst to best.
    mode:       "rel" -> band [0.9T, 1.1T] (by |T|);  "pp" -> band T ± pp (percentage-point quantities).
    Inside a band the score interpolates linearly between the two adjacent levels and is reported
    to one decimal; outside, the level. A band never extends past the midpoint to its neighbour.
    """
    if x is None:
        return None
    if not higher_better:
        x = -x
        thresholds = sorted(-t for t in thresholds)
        # levels remain worst -> best
    ts = list(thresholds)
    if ts != sorted(ts):
        raise ValueError("thresholds must be ascending")
    # step value
    lvl = levels[0]
    for i, t in enumerate(ts):
        if x >= t:
            lvl = levels[i + 1]
    if not interpolate:
        return float(lvl)
    for i, t in enumerate(ts):
        h = abs(t) * 0.10 if mode == "rel" else pp
        if i > 0:
            h = min(h, (t - ts[i - 1]) / 2)
        if i < len(ts) - 1:
            h = min(h, (ts[i + 1] - t) / 2)
        if h <= 0:
            continue
        lo, hi = t - h, t + h
        if lo < x < hi:
            a, b = levels[i], levels[i + 1]
            return round(a + (b - a) * (x - lo) / (hi - lo), 1)
    return float(lvl)


def all_limbs(limbs):
    """limbs: list of (label, True|False|None). Fail if any available limb fails; pass only if all
    limbs are available and pass; otherwise unverified."""
    if any(v is False for _, v in limbs):
        return "fail"
    if all(v is True for _, v in limbs):
        return "pass"
    return "unverified"


# ══════════════════════════════════════════════════════════════════════════
# 2. FORENSIC BATTERY — retrieval-aware (spec §3 B, §6 G1)
# ══════════════════════════════════════════════════════════════════════════

def beneish(f):
    need = ["revenue", "receivables", "cogs", "current_assets", "ppe_net",
            "securities", "total_assets", "depreciation", "sga", "debt", "cfo", "ni"]
    for period in ("t", "t1"):
        for k in need:
            if g(f, period, k) is None:
                return None, f"missing {period}.{k}"
    t, p = f["t"], f["t1"]
    try:
        dsri = (t["receivables"] / t["revenue"]) / (p["receivables"] / p["revenue"])
        gm_t = (t["revenue"] - t["cogs"]) / t["revenue"]
        gm_p = (p["revenue"] - p["cogs"]) / p["revenue"]
        gmi = gm_p / gm_t
        soft_t = 1 - (t["current_assets"] + t["ppe_net"] + t["securities"]) / t["total_assets"]
        soft_p = 1 - (p["current_assets"] + p["ppe_net"] + p["securities"]) / p["total_assets"]
        aqi = soft_t / soft_p if soft_p else 1.0
        sgi = t["revenue"] / p["revenue"]
        depi = (p["depreciation"] / (p["depreciation"] + p["ppe_net"])) / (t["depreciation"] / (t["depreciation"] + t["ppe_net"]))
        sgai = (t["sga"] / t["revenue"]) / (p["sga"] / p["revenue"])
        lvgi = (t["debt"] / t["total_assets"]) / (p["debt"] / p["total_assets"]) if p["debt"] else 1.0
        tata = (t["ni"] - t["cfo"]) / t["total_assets"]
    except ZeroDivisionError as e:
        return None, f"division by zero ({e}); Beneish not meaningful"
    m = (-4.84 + 0.920 * dsri + 0.528 * gmi + 0.404 * aqi + 0.892 * sgi
         + 0.115 * depi - 0.172 * sgai + 4.679 * tata - 0.327 * lvgi)
    comp = {"DSRI": dsri, "GMI": gmi, "AQI": aqi, "SGI": sgi, "DEPI": depi, "SGAI": sgai, "LVGI": lvgi, "TATA": tata}
    return round(m, 4), {k: round(v, 4) for k, v in comp.items()}


def altman(f, model="Z"):
    a = f.get("altman", {}) or {}
    need = ["working_capital", "retained_earnings", "ebit", "total_assets", "total_liabilities"]
    if model == "Z":
        need += ["market_cap", "revenue"]
    for k in need:
        if a.get(k) is None:
            return None, None
    ta = a["total_assets"]
    if model == "Z":
        z = (1.2 * a["working_capital"] / ta + 1.4 * a["retained_earnings"] / ta + 3.3 * a["ebit"] / ta
             + 0.6 * a["market_cap"] / a["total_liabilities"] + 1.0 * a["revenue"] / ta)
        return round(z, 3), 2.99
    z = (6.56 * a["working_capital"] / ta + 3.26 * a["retained_earnings"] / ta + 6.72 * a["ebit"] / ta
         + 1.05 * (ta - a["total_liabilities"]) / a["total_liabilities"])
    return round(z, 3), 2.60


def _check10(f, add):
    m, comp = beneish(f)
    lev = g(f, "leveraged", default=False)
    if m is None:
        add(10, "Beneish M < -1.78" + (" and Altman Z > bar" if lev else ""), "unverified", comp)
        return
    limbs = [("beneish", m < -1.78)]
    number = {"M": m, "components": comp, "margin_vs_bar": round(-1.78 - m, 4)}
    if lev:
        model = g(f, "altman_model", default="Z")
        z, bar = altman(f, model)
        limbs.append(("altman", None if z is None else z > bar))
        number["altman"] = "not retrieved" if z is None else {"model": model, "Z": z, "bar": bar}
    add(10, "Beneish M < -1.78" + (" and Altman Z > bar (leveraged)" if lev else ""), all_limbs(limbs), number)


def forensic_in(d):
    """India 10-check battery (spec §3 B)."""
    f = d.get("financials", {}) or {}
    out = []
    def add(n, name, result, number, note=None):
        out.append({"n": n, "check": name, "result": result, "number": number, **({"note": note} if note else {})})

    # 1 cash conversion
    cfo, eb = g(f, "cumulative", "cfo"), g(f, "cumulative", "ebitda")
    if cfo is not None and eb:
        r = cfo / eb
        add(1, "cum. CFO / cum. EBITDA >= 70% (5-6 yrs)", "pass" if r >= 0.70 else "fail", f"{pct(r)}%")
    else:
        add(1, "cum. CFO / cum. EBITDA >= 70% (5-6 yrs)", "unverified", "cumulative CFO or EBITDA not retrieved")

    # 2 earnings backing
    v = g(f, "cfo_pat_5y_avg")
    add(2, "CFO/PAT 5-yr avg >= 80%", "unverified" if v is None else ("pass" if v >= 0.80 else "fail"),
        "not retrieved" if v is None else round(v, 3))

    # 3 receivables — BOTH limbs (v2 tested only the first)
    a, b = g(f, "debtor_days_start"), g(f, "debtor_days_end")
    rg, vg = g(f, "receivables_growth_3y"), g(f, "revenue_growth_3y")
    l1 = None if (a is None or b is None) else (b - a) <= 10
    l2 = None if (rg is None or vg is None) else rg <= vg
    num = []
    if l1 is not None: num.append(f"debtor days {a} -> {b} ({b - a:+.1f}d)")
    if l2 is not None: num.append(f"receivables {pct(rg)}% vs revenue {pct(vg)}% (3y)")
    missing = [n for n, l in (("debtor days", l1), ("receivables-vs-revenue growth", l2)) if l is None]
    add(3, "debtor days +<=10d over 3y AND receivable growth <= revenue growth",
        all_limbs([("days", l1), ("growth", l2)]), "; ".join(num) or "not retrieved",
        ("limb not retrieved: " + ", ".join(missing)) if missing else None)

    # 4 other income, treasury exception for net-cash companies
    oi, pbt = g(f, "other_income"), g(f, "pbt")
    nc = g(d, "valuation", "net_cash")
    if oi is not None and pbt:
        r = oi / pbt
        exc = bool(d.get("treasury_income_exception", False)) and (nc is None or nc >= 0)
        res = "pass" if (r < 0.10 or exc) else "fail"
        add(4, "other income < 10% of PBT", res, f"{pct(r)}%",
            "treasury income of a net-cash company — noted, not failed" if (exc and r >= 0.10) else
            ("treasury exception claimed but company is net-debt — not applied" if d.get("treasury_income_exception") and not exc else None))
    else:
        add(4, "other income < 10% of PBT", "unverified", "other income or PBT not retrieved")

    # 5 contingent liabilities
    cl, nw = g(f, "contingent_liabilities"), g(f, "net_worth")
    if cl is not None and nw:
        r = cl / nw
        add(5, "contingent liabilities < 10% of net worth", "pass" if r < 0.10 else "fail", f"{pct(r)}%")
    else:
        add(5, "contingent liabilities < 10% of net worth", "unverified", "AR note not retrieved")

    # 6 related parties — both limbs
    rpt, rev = g(f, "rpt_total"), g(f, "revenue")
    gl = g(f, "group_loans")
    l1 = None if (rpt is None or not rev) else (rpt / rev) < 0.05
    l2 = None if (gl is None or not nw) else (gl / nw) < 0.02
    num = []
    if l1 is not None: num.append(f"RPT {pct(rpt / rev)}% of revenue")
    if l2 is not None: num.append(f"group loans {pct(gl / nw)}% of NW")
    add(6, "RPT < 5% of revenue AND group loans < 2% of NW", all_limbs([("rpt", l1), ("loans", l2)]),
        "; ".join(num) or "RPT note not retrieved",
        None if l2 is not None else "group-loans limb not retrieved")

    # 7 auditor
    au = d.get("auditor") or {}
    if not au:
        add(7, "auditor reputable, unmodified, clean CARO, no resignation, fee growth <= revenue growth", "unverified", "auditor block not supplied")
    else:
        fg, rg3 = au.get("fee_growth_3y"), au.get("revenue_growth_3y")
        limbs = [("reputable", au.get("reputable")),
                 ("unmodified", None if au.get("opinion") is None else au.get("opinion") == "unmodified"),
                 ("clean CARO", None if au.get("adverse_caro") is None else not au.get("adverse_caro")),
                 ("no resignation", None if au.get("resignation") is None else not au.get("resignation")),
                 ("fee growth", None if (fg is None or rg3 is None) else fg <= rg3 + 1e-9)]
        miss = [n for n, l in limbs if l is None]
        failed = [n for n, l in limbs if l is False]
        add(7, "auditor reputable, unmodified, clean CARO, no resignation, fee growth <= revenue growth",
            all_limbs(limbs), f"{au.get('name', '?')}, {au.get('opinion', '?')}" + (f"; fails: {failed}" if failed else ""),
            ("not retrieved: " + ", ".join(miss)) if miss else None)

    # 8 depreciation
    ds, de = g(f, "dep_rate_start"), g(f, "dep_rate_end")
    limbs = [("rate +-2pp", None if (ds is None or de is None) else abs(de - ds) <= 0.02),
             ("no capitalised opex", None if f.get("capitalised_opex") is None else not f.get("capitalised_opex")),
             ("no profit-lifting policy change", None if f.get("profit_lifting_policy_change") is None else not f.get("profit_lifting_policy_change"))]
    miss = [n for n, l in limbs if l is None]
    add(8, "depreciation rate +-2pp over 5 yrs; no capitalised opex; no profit-lifting policy change", all_limbs(limbs),
        f"{pct(ds)}% -> {pct(de)}%" if ds is not None and de is not None else "gross block not retrieved",
        ("not retrieved: " + ", ".join(miss)) if miss else None)

    # 9 cash is real; pledge de minimis (< 0.5% of shares outstanding)
    cy = g(f, "cash_yield")
    pl = g(d, "pledge", "pledge_pct_shares")
    if pl is None:
        pl = g(d, "ownership", "pledge_pct_shares")
    limbs = [("cash yield >= 4%", None if cy is None else cy >= 0.04),
             ("pledge < 0.5% of shares", None if pl is None else pl < PLEDGE_FLOOR)]
    add(9, "cash yield >= 4% AND pledge < 0.5% of shares outstanding", all_limbs(limbs),
        f"yield {pct(cy)}%, pledge {pct(pl, 4)}% of shares",
        None if all(l is not None for _, l in limbs) else "limb not retrieved")

    # 10 Beneish (+ Altman if leveraged)
    _check10(f, add)
    return out


def forensic_us(d, M):
    """USA 10-check translation (USA workflow §6-US), retrieval-aware."""
    f = d.get("financials", {}) or {}
    out = []
    def add(n, name, result, number, note=None):
        out.append({"n": n, "check": name, "result": result, "number": number, **({"note": note} if note else {})})

    cfo, eb = g(f, "cumulative", "cfo"), g(f, "cumulative", "ebitda")
    if cfo is not None and eb is not None and eb <= 0:
        add(1, "substitute (cum. EBITDA <= 0): cum. CFO >= cum. EBITDA", "pass" if cfo >= eb else "fail", f"CFO {cfo} vs EBITDA {eb}")
    elif cfo is not None and eb:
        add(1, "cum. CFO / cum. EBITDA >= 70%", "pass" if cfo / eb >= 0.70 else "fail", f"{pct(cfo / eb)}%")
    else:
        add(1, "cum. CFO / cum. EBITDA >= 70%", "unverified", "not retrieved")

    if g(f, "loss_maker", default=False):
        s = g(f, "cfo_less_sbc_latest2")
        if s and len(s) == 2:
            add(2, "loss-maker: CFO-SBC >= 0 latest FY and improving", "pass" if (s[1] >= 0 and s[1] >= s[0]) else "fail", f"{s[0]} -> {s[1]}")
        else:
            add(2, "loss-maker: CFO-SBC >= 0 and improving", "unverified", "series not retrieved")
    else:
        v = g(f, "cfo_ni_5y_avg")
        add(2, "CFO/NI 5-yr avg >= 80%", "unverified" if v is None else ("pass" if v >= 0.80 else "fail"), v)

    a, b = g(f, "dso_start"), g(f, "dso_end")
    rg, vg = g(f, "receivables_growth_3y"), g(f, "revenue_growth_3y")
    add(3, "DSO +<=10d over 3y AND receivables growth <= revenue growth",
        all_limbs([("dso", None if a is None or b is None else (b - a) <= 10),
                   ("growth", None if rg is None or vg is None else rg <= vg)]),
        f"DSO {a} -> {b}; recv {pct(rg)}% vs rev {pct(vg)}%")

    oi, pbt = g(f, "nonoperating_income"), g(f, "pretax_income")
    if oi is not None and pbt:
        r = oi / pbt
        exc = bool(d.get("treasury_income_exception", False))
        add(4, "non-operating income < 10% of pretax income", "pass" if (r < 0.10 or exc) else "fail", f"{pct(r)}%",
            "net-cash interest — noted, not failed" if exc and r >= 0.10 else None)
    else:
        add(4, "non-operating income < 10% of pretax income", "unverified", "not retrieved")

    cl, eq = g(f, "contingencies"), g(f, "equity")
    if cl is not None and eq:
        add(5, "contingencies < 10% of equity", "pass" if cl / eq < 0.10 else "fail", f"{pct(cl / eq)}%")
    elif g(f, "contingencies_not_estimable_material"):
        add(5, "contingencies < 10% of equity", "fail", "material matter with no estimate")
    else:
        add(5, "contingencies < 10% of equity", "unverified", "note not retrieved")

    rpt, rev, rpl = g(f, "rpt_total"), g(f, "revenue"), g(f, "related_party_loans")
    add(6, "RPT < 5% of revenue AND related-party loans < 2% of equity",
        all_limbs([("rpt", None if rpt is None or not rev else rpt / rev < 0.05),
                   ("loans", None if rpl is None or not eq else rpl / eq < 0.02)]),
        f"RPT {pct(rpt / rev) if rpt is not None and rev else None}%")

    au = d.get("auditor") or {}
    fg, rg3 = au.get("audit_fee_growth_3y"), au.get("revenue_growth_3y")
    add(7, "auditor & ICFR clean; no 4.01/4.02; fee growth <= revenue growth",
        "unverified" if not au else all_limbs([
            ("opinion", None if au.get("opinion") is None else au.get("opinion") == "unqualified"),
            ("ICFR", None if au.get("material_weakness") is None else not au.get("material_weakness")),
            ("4.01", None if au.get("change_with_disagreement_3y") is None else not au.get("change_with_disagreement_3y")),
            ("4.02", None if au.get("restatement_4_02_3y") is None else not au.get("restatement_4_02_3y")),
            ("fees", None if fg is None or rg3 is None else fg <= rg3 + 1e-9)]),
        au.get("name", "auditor block not supplied"))

    ds, de = g(f, "dep_rate_start"), g(f, "dep_rate_end")
    cap, rg5 = g(f, "capitalised_costs_growth_5y"), g(f, "revenue_growth_5y")
    add(8, "depreciation +-2pp; no capitalised-cost build; no profit-lifting policy change",
        all_limbs([("rate", None if ds is None or de is None else abs(de - ds) <= 0.02),
                   ("capitalised", None if cap is None or rg5 is None else cap <= rg5),
                   ("policy", None if f.get("profit_lifting_policy_change") is None else not f.get("profit_lifting_policy_change"))]),
        f"{pct(ds)}% -> {pct(de)}%")

    cy, cash_pct = g(f, "cash_yield"), g(f, "cash_pct_assets")
    dil, sbc = g(f, "diluted_shares_cagr_3y"), g(f, "sbc_pct_cfo")
    tb = M.get("tbill_3m") or 0.0
    cash_limb = True if (cash_pct is not None and cash_pct < 0.05) else (None if cy is None else cy >= 0.5 * tb)
    add(9, "cash real (yield >= 50% of 3M T-bill); dilution <= 2% p.a.; SBC <= 25% of CFO",
        all_limbs([("cash", cash_limb), ("dilution", None if dil is None else dil <= 0.02),
                   ("sbc", None if sbc is None else sbc <= 0.25)]),
        f"yield {pct(cy)}%, dilution {pct(dil)}%, SBC/CFO {pct(sbc)}%")

    _check10(f, add)
    return out


def apply_verification(checks, d):
    """check_verification {n: pass|fail|unverified}: fills checks the numbers could not; a
    contradiction with a computed result refuses the render."""
    cv = d.get("check_verification") or {}
    notes = []
    for c in checks:
        sup = cv.get(str(c["n"])) or cv.get(c["n"])
        if sup is None:
            continue
        sup = "unverified" if sup in ("unverifiable", "unverified") else sup
        if sup not in ("pass", "fail", "unverified"):
            raise RenderRefused(f"check_verification[{c['n']}] = {sup!r}: must be pass | fail | unverified")
        if c["result"] == "unverified":
            if sup != "unverified":
                c["result"] = sup
                c["source"] = "check_verification (document-verified, not computed)"
                notes.append(c["n"])
        elif c["result"] != sup:
            raise RenderRefused(f"forensic check {c['n']}: numbers say {c['result']!r} but check_verification says "
                                f"{sup!r} — reconcile before rendering")
    return notes


def forensic(d, M):
    fs = d.get("sector_variant") == "financial"
    if fs:
        checks = []
        for c in d.get("forensic_fs", []) or []:
            r = c.get("result")
            checks.append({**c, "result": "unverified" if r in ("unverifiable", "unverified", None) else r})
        total = 8
        if len(checks) != 8:
            raise RenderRefused(f"financial variant needs exactly 8 checks in forensic_fs (got {len(checks)})")
    else:
        checks = forensic_us(d, M) if M["jurisdiction"] == "US" else forensic_in(d)
        total = 10
    verified_by_doc = apply_verification(checks, d)

    passes = sum(1 for c in checks if c["result"] == "pass")
    fails = sum(1 for c in checks if c["result"] == "fail")
    unver = [c["n"] for c in checks if c["result"] == "unverified"]
    verified = passes + fails
    B = round(10 * passes / verified, 2) if verified else None
    min_ver = G1_MIN_VERIFIED[total]
    # G1 (spec §6): clears iff verified >= min AND pass rate >= 60%.
    # verified < min -> coverage cap (WATCH) unless no amount of further work could clear it.
    max_possible_rate = (total - fails) / total
    if verified >= min_ver:
        gate = "pass" if passes / verified >= G1_MIN_PASS_RATE else "FAIL"
        reason = f"{passes}/{verified} verified pass = {pct(passes / verified, 1)}%"
    elif max_possible_rate < G1_MIN_PASS_RATE:
        gate = "FAIL"
        reason = (f"only {verified} verified, but {fails} fails already cap the best-case pass rate at "
                  f"{pct(max_possible_rate, 1)}% < 60% — no retrieval can clear G1")
    else:
        gate = "COVERAGE"
        reason = f"only {verified} of {total} verified (< {min_ver}) — tier capped at WATCH until checks {unver} are verified"
    reconcile = None
    c4 = next((c for c in checks if c["n"] == 4), None)
    c9 = next((c for c in checks if c["n"] == 9), None)
    if not fs and c4 and c9 and c4["result"] == "fail" and c9["result"] == "pass":
        reconcile = ("Checks 4+9 read together: yield on cash clears the bar, so the balance is real (9 passes), "
                     "but other income is too large a share of PBT — likely mark-to-market or one-off treasury gains (4 fails).")
    return {"variant": "financial 8-check" if fs else f"{M['jurisdiction']} 10-check", "checks": checks,
            "passes": passes, "fails": fails, "verified": verified, "total": total,
            "unverified": unver, "follow_ups": [f"verify check {n}" for n in unver],
            "document_verified": verified_by_doc, "B": B, "gate_G1": gate, "gate_G1_reason": reason,
            "reconcile_4_9": reconcile}


# ══════════════════════════════════════════════════════════════════════════
# 3. RATES: r_val, beta, capital structure, r_hurdle (spec §1)
# ══════════════════════════════════════════════════════════════════════════

def beta_regression(stock_w, index_w):
    def clean(s):
        seen = {}
        for row in s or []:
            if row and row[0] and row[1] is not None:
                seen[str(row[0])[:10]] = float(row[1])
        return seen
    s, m = clean(stock_w), clean(index_w)
    dates = sorted(set(s) & set(m))
    rs = [(s[dates[i]] / s[dates[i - 1]] - 1, m[dates[i]] / m[dates[i - 1]] - 1) for i in range(1, len(dates))]
    n = len(rs)
    if n < 40:
        return {"beta": None, "obs": n, "note": f"{n} aligned weekly returns < 40 — use the industry beta (beta_source='industry')"}
    ax = sum(r[1] for r in rs) / n; ay = sum(r[0] for r in rs) / n
    cov = sum((r[1] - ax) * (r[0] - ay) for r in rs) / (n - 1)
    var = sum((r[1] - ax) ** 2 for r in rs) / (n - 1)
    return {"beta": round(cov / var, 3), "obs": n, "window": f"{dates[0]} to {dates[-1]}"}


def resolve_beta(d, M):
    v = d.get("valuation") or {}
    px = d.get("prices") or {}
    if px.get("stock_weekly") and px.get("index_weekly") and not v.get("beta_override"):
        br = beta_regression(px["stock_weekly"], px["index_weekly"])
        if br["beta"] is not None:
            return br["beta"], "measured", br
        if v.get("beta") is None or v.get("beta_source") != "industry":
            raise RenderRefused(br["note"])
    beta, src = v.get("beta"), v.get("beta_source")
    if beta is None:
        raise RenderRefused("valuation.beta missing — measured (2-yr weekly vs benchmark, >= 40 obs) or the industry "
                            "beta; never assumed (spec §1)")
    if src not in ("measured", "industry"):
        raise RenderRefused("valuation.beta_source must be 'measured' or 'industry' (spec §1)")
    if src == "measured" and v.get("beta_obs") is not None and v["beta_obs"] < 40:
        raise RenderRefused(f"measured beta has {v['beta_obs']} obs < 40 — use the industry beta")
    return beta, src, None


def tax_rate(v, M):
    return max(v.get("tax") or 0.0, M["tax_floor"])


def capital_structure(v, price, M):
    """Actual/target structure (spec §1). Net-cash companies stay all-equity; the v2 all-equity
    default for net-debt companies is deleted — derived from market values if not supplied."""
    nc = v.get("net_cash")
    tax = tax_rate(v, M)
    kd_pre = v.get("kd_pre") if v.get("kd_pre") is not None else M["rf"] + M["kd_spread"]
    kd_post = kd_pre * (1 - tax)
    if nc is None:
        raise RenderRefused("valuation.net_cash missing (negative if net debt) — needed for capital structure and equity bridge")
    if nc >= 0:
        note = "net cash: all-equity" + (" (input debt_wt ignored)" if v.get("debt_wt") else "")
        return 0.0, kd_pre, kd_post, note
    if v.get("debt_wt") is not None:
        return float(v["debt_wt"]), kd_pre, kd_post, "input debt_wt (actual/target)"
    if v.get("de_ratio") is not None:
        de = float(v["de_ratio"])
        return de / (1 + de), kd_pre, kd_post, "input D/E"
    mcap = price * v["shares"]
    nd = -nc
    return nd / (nd + mcap), kd_pre, kd_post, "derived: net debt / (net debt + market cap)"


def rates(d, M):
    v = d["valuation"]
    beta, bsrc, breg = resolve_beta(d, M)
    ke = M["rf"] + beta * M["erp_val"]                       # r_val (cost of equity) — quality tests & valuation
    dw, kd_pre, kd_post, cs_note = capital_structure(v, d["price"], M)
    w_val = ke * (1 - dw) + kd_post * dw                     # WACC at r_val — valuation
    w_hurdle = M["hurdle"] * (1 - dw) + kd_post * dw         # WACC at r_hurdle — trigger only
    return {"beta": beta, "beta_source": bsrc, "beta_regression": breg, "r_val": ke,
            "r_hurdle": M["hurdle"], "debt_wt": dw, "kd_pre": kd_pre, "kd_post": kd_post,
            "capital_structure": cs_note, "wacc_val": w_val, "wacc_hurdle": w_hurdle,
            "tax": tax_rate(v, M)}


# ══════════════════════════════════════════════════════════════════════════
# 4. VALUATION MACHINERY (spec §4)
# ══════════════════════════════════════════════════════════════════════════

def terminal_g(v, M):
    tg = v.get("terminal_g")
    if tg is None:
        tg = M["terminal_g_default"]
    return min(tg, M["terminal_g_cap"])


def dcf_value(v, w, M, detail=False):
    """FCFF DCF, 5-yr explicit. Terminal year normalised (spec §4.1): working capital charged at
    TERMINAL growth, capex faded to maintenance (= depreciation). Returns value/share (or None if
    degenerate) and, with detail, the cash flows."""
    rev0 = v["revenue"]; ms = v["margin_start"]; me = v["margin_end"]
    growth = v["growth"]; years = v.get("years", 5)
    tg = terminal_g(v, M)
    cs = v.get("capex_start", v.get("capex_pct", 0.0)); ce = v.get("capex_end", cs)
    ds = v.get("dep_start", v.get("dep_pct", cs)); de = v.get("dep_end", v.get("dep_pct", ds))
    wc = v.get("wc_pct", 0.0)
    tax = tax_rate(v, M)
    tax_t = max(tax, M["tax_terminal"]) if M["tax_terminal"] is not None else tax
    shares = v["shares"]; nc = v.get("net_cash", 0.0); minority = v.get("minority", 0.0)
    r = rev0; pv = 0.0; flows = []
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
        flows.append(fcff)
    # normalised year-5 FCFF: terminal margin, capex = depreciation, WC at terminal growth
    nopat_n = r * (me - de) * (1 - tax_t)
    fcff_norm = nopat_n - (r * tg / (1 + tg)) * wc          # capex (= r*de) cancels depreciation add-back
    if w <= tg + 0.005:
        return (None, {"degenerate": f"discount rate {pct(w)}% <= terminal g {pct(tg)}% + 0.5pp"}) if detail else None
    tv = fcff_norm * (1 + tg) / (w - tg)
    pv_tv = tv / (1 + w) ** years
    val = (pv + pv_tv + nc - minority) / shares
    if detail:
        return val, {"explicit_fcff": [round(x, 2) for x in flows], "fcff_norm_y5": round(fcff_norm, 2),
                     "fcff_y6": round(fcff_norm * (1 + tg), 2), "tv": round(tv, 2), "pv_explicit": round(pv, 2),
                     "pv_tv": round(pv_tv, 2), "tv_share_pct": round(pv_tv / (pv + pv_tv) * 100, 1) if (pv + pv_tv) else None,
                     "terminal_g": tg, "year5_revenue": round(r, 2)}
    return val


def dcf_grid(v, R, M):
    base = R["wacc_val"]
    grid = {}
    for label, w in (("low", base - 0.01), ("base", base), ("high", base + 0.01)):
        val = dcf_value(v, w, M)
        grid[label] = {"wacc": round(w, 4), "value": None if val is None else round(val, 2)}
    central, meta = dcf_value(v, base, M, detail=True)
    vals = [grid[k]["value"] for k in grid]
    flags = []
    usable = central is not None and central > 0 and all(x is not None for x in vals)
    degenerate_pts = [k for k in grid if grid[k]["value"] is None]
    if central is not None and degenerate_pts:
        flags.append(f"DEGENERATE DCF GRID at {degenerate_pts} (WACC within 0.5pp of terminal g) — range unbounded; "
                     "treated as unusable: D1 = 0, no defensible trigger")
    if central is None:
        flags.append("DEGENERATE DCF: " + meta.get("degenerate", ""))
    elif central <= 0:
        flags.append(f"NEGATIVE DCF: central value {round(central, 2)} <= 0 — D1 = 0, no defensible trigger")
    if usable and min(vals) <= 0:
        flags.append("DCF range lower bound <= 0 at WACC +1pp — range is fragile")
    rng = [min(vals), max(vals)] if all(x is not None for x in vals) else None
    return {"wacc_val": round(base, 4), "grid": grid, "range": rng,
            "central": None if central is None else round(central, 2), "usable": usable, "flags": flags,
            "meta": meta, "band_width_pct": round((rng[1] - rng[0]) / rng[0] * 100, 1) if (rng and rng[0] > 0) else None}


def _scan_solve(fn, target, lo, hi, increasing=True, n=161):
    """Monotonicity-guarded solver (spec §4.3). Scans [lo, hi]; solves by bisection only inside the
    first bracket where fn crosses target moving in the expected direction. Returns (x, info)."""
    xs = [lo + (hi - lo) * i / (n - 1) for i in range(n)]
    ys = [fn(x) for x in xs]
    finite = [(x, y) for x, y in zip(xs, ys) if y is not None and math.isfinite(y)]
    info = {"bounds": [lo, hi]}
    if len(finite) < 2:
        return None, {**info, "reason": "function undefined across bounds"}
    # monotonicity diagnostics
    fys = [y for _, y in finite]
    if increasing:
        peak_i = max(range(len(fys)), key=lambda i: fys[i])
        info["monotone"] = all(fys[i + 1] >= fys[i] - 1e-12 for i in range(len(fys) - 1))
        if not info["monotone"]:
            info["turning_point"] = round(finite[peak_i][0], 4)
            info["max_value"] = round(fys[peak_i], 2)
    else:
        info["monotone"] = all(fys[i + 1] <= fys[i] + 1e-12 for i in range(len(fys) - 1))
    for i in range(len(finite) - 1):
        (x0, y0), (x1, y1) = finite[i], finite[i + 1]
        right_dir = (y1 >= y0) if increasing else (y1 <= y0)
        if right_dir and (y0 - target) * (y1 - target) <= 0 and y0 != y1:
            a, b = x0, x1
            for _ in range(100):
                mid = (a + b) / 2
                ym = fn(mid)
                if ym is None:
                    break
                if (ym < target) == increasing:
                    a = mid
                else:
                    b = mid
            return (a + b) / 2, info
    info["reason"] = ("price above the maximum value reachable within bounds" if increasing and max(fys) < target
                      else "price below the minimum value within bounds" if increasing and min(fys) > target
                      else "no crossing in the monotone region")
    return None, info


GROWTH_BOUNDS = (-0.20, 0.60)


def reverse_dcf(v, price, R, M):
    w = R["wacc_val"]
    tg = terminal_g(v, M)
    def by_growth(x):
        t = dict(v); t["growth"] = x
        return dcf_value(t, w, M)
    ig, info = _scan_solve(by_growth, price, *GROWTH_BOUNDS, increasing=True)
    res = {"price": price, "wacc_val": round(w, 4), "implied_growth": pct(ig), "solver": info}
    # implied discount rate at input growth (always reported)
    def by_rate(x):
        return dcf_value(v, x, M)
    idr, _ = _scan_solve(by_rate, price, tg + 0.006, 0.60, increasing=False)
    res["implied_wacc"] = pct(idr)
    res["implied_equity_return"] = (None if idr is None else
                                    pct((idr - R["kd_post"] * R["debt_wt"]) / (1 - R["debt_wt"])))
    if ig is None:
        def by_margin(x):
            t = dict(v); t["margin_end"] = x
            return dcf_value(t, w, M)
        im, _ = _scan_solve(by_margin, price, 0.0, 0.95, increasing=True)
        res["unsolvable_on_growth"] = True
        res["implied_terminal_margin"] = pct(im)
        res["note"] = ("Unsolvable on growth within [-20%, 60%] (" + info.get("reason", "") + "). Restated two ways: "
                       f"implied terminal EBITDA margin {pct(im)}% at input growth; implied discount rate "
                       f"{pct(idr)}% at input growth. The price assumes one of these.")
    return res


def range_rule(dcf_block, mult, price):
    """Spec §4.4. Overlap -> fair value = overlap MIDPOINT. Disjoint -> both ranges side by side."""
    if not dcf_block or not dcf_block.get("range") or not mult:
        return None
    d_lo, d_hi = dcf_block["range"]; m_lo, m_hi = mult
    overlap = not (d_hi < m_lo or m_hi < d_lo)
    if overlap:
        lo, hi = max(d_lo, m_lo), min(d_hi, m_hi)
        fv = (lo + hi) / 2
        return {"disjoint": False, "overlap": [round(lo, 2), round(hi, 2)], "fair_value": round(fv, 2),
                "mos_line": round(0.80 * fv, 2), "mos_nod": price <= 0.80 * fv,
                "note": "ranges overlap; fair value = overlap midpoint"}
    mid = dcf_block["central"]
    return {"disjoint": True, "dcf_range": [d_lo, d_hi], "multiples_range": [m_lo, m_hi], "fair_value": None,
            "mos_line": None if mid is None else round(0.80 * mid, 2),
            "mos_nod": (mid is not None and price <= 0.80 * mid),
            "note": "ranges disjoint — no blended fair value; both shown side by side; MoS line from DCF midpoint"}


def trigger_block(v, R, M, dcf_block, price):
    """P_hurdle = highest price earning >= r_hurdle on the DCF base-case cash flows (spec §4.4)."""
    if not dcf_block or not dcf_block["usable"]:
        return {"trigger": None, "defensible": False,
                "reason": "DCF unusable (<= 0 or degenerate) — no defensible entry; tier caps at WATCH"}
    p_h = dcf_value(v, R["wacc_hurdle"], M)
    if p_h is None or p_h <= 0:
        return {"trigger": None, "defensible": False, "p_hurdle": None if p_h is None else round(p_h, 2),
                "reason": "the DCF cash flows cannot earn the 15% hurdle at any positive price — no defensible entry"}
    out = {"trigger": round(p_h, 2), "p_hurdle": round(p_h, 2), "defensible": True,
           "wacc_hurdle": round(R["wacc_hurdle"], 4),
           "discount_to_dcf_central_pct": round((p_h / dcf_block["central"] - 1) * 100, 1),
           "distance_from_price_pct": round((p_h / price - 1) * 100, 1)}
    d_hi = dcf_block["range"][1]
    if p_h > d_hi:
        out["unhealthy"] = True
        out["note"] = (f"UNHEALTHY: the 15% entry price {round(p_h, 2)} sits above the conservative DCF ceiling {d_hi} "
                       f"(r_val WACC -1pp {pct(R['wacc_val'] - 0.01)}% exceeds the hurdle WACC {pct(R['wacc_hurdle'])}%).")
    else:
        out["unhealthy"] = False
    return out


def irr_at(v, R, M, px):
    """Equity return a buyer at px earns on the DCF base-case cash flows (perpetuity IRR)."""
    idr, _ = _scan_solve(lambda x: dcf_value(v, x, M), px, terminal_g(v, M) + 0.006, 0.80, increasing=False)
    if idr is None:
        return None
    return pct((idr - R["kd_post"] * R["debt_wt"]) / (1 - R["debt_wt"]))


# ══════════════════════════════════════════════════════════════════════════
# 5. SCENARIOS AND THE BEAR WEIGHT (spec §5)
# ══════════════════════════════════════════════════════════════════════════

def bear_weight(d):
    bt = d.get("bear_triggers")
    if bt is None:
        raise RenderRefused("bear_triggers[] missing — list each documented independent bear trigger "
                            "(an empty list means none: bear weight 25%) (spec §5)")
    if not isinstance(bt, list):
        raise RenderRefused("bear_triggers must be a list of documented trigger descriptions")
    uniq = list(dict.fromkeys(str(x).strip() for x in bt))
    return min(BEAR_BASE + BEAR_STEP * len(uniq), BEAR_CAP), uniq


def scenario_set(d):
    cases = d.get("scenarios") or []
    if not cases:
        return None
    bw, bt = bear_weight(d)
    bear = [c for c in cases if c["name"].lower().startswith("bear")]
    others = [c for c in cases if not c["name"].lower().startswith("bear")]
    if len(bear) != 1 or not others:
        raise RenderRefused("scenarios need exactly one Bear case plus Base/Bull")
    osum = sum(c.get("weight", 0) for c in others)
    if osum <= 0:
        raise RenderRefused("Base/Bull weights must be positive (their ratio is preserved)")
    out = []
    for c in cases:
        w = bw if c in bear else c["weight"] / osum * (1 - bw)
        metric = c.get("exit_eps", c.get("exit_metric"))
        out.append({"name": c["name"], "weight": round(w, 4), "input_weight": c.get("weight"),
                    "value": metric * c["exit_multiple"] + c.get("dividends", 0)})
    return {"cases": out, "bear_weight": bw, "bear_triggers": bt}


def scenarios_at(ss, px):
    if not ss:
        return None
    tot = 0.0; rows = []
    for c in ss["cases"]:
        ret = c["value"] / px - 1
        tot += ret * c["weight"]
        rows.append({"case": c["name"], "weight": c["weight"], "value": round(c["value"], 2), "return_pct": pct(ret)})
    bear = next(r for r in rows if r["case"].lower().startswith("bear"))
    bull = next((r for r in rows if r["case"].lower().startswith("bull")), None)
    dd = max(0.0, -bear["return_pct"])
    no_loss = dd == 0
    ud = None if (bull is None or no_loss) else round(bull["return_pct"] / dd, 3)
    ann = (1 + tot) ** (1 / 3) - 1 if tot > -1 else -1.0
    return {"price": px, "cases": rows, "ev_3yr_pct": pct(tot), "ev_annual_pct": pct(ann),
            "bear_drawdown_pct": round(dd, 2), "bear_weight": ss["bear_weight"], "upside_downside": ud,
            "bear_no_loss": no_loss}


# ══════════════════════════════════════════════════════════════════════════
# 6. TEST SCORING (spec §3)
# ══════════════════════════════════════════════════════════════════════════

def trend_score(q):
    if not q:
        return None
    t = [q.get("rev_trend"), q.get("margin_trend"), q.get("cfo_trend")]
    if any(x is None for x in t):
        return None
    ok = {"improving", "stable_strong"}
    if all(x in ok for x in t):
        return 2.0
    if sum(1 for x in t if x == "deteriorating") >= 2:
        return 0.0
    return 1.0


def credibility(d, mode):
    c = d.get("credibility")
    if not c:
        return None, None
    if c.get("executable") is False:
        return "not_executable", None
    if c.get("score_10") is not None:
        return float(c["score_10"]), None
    qs = c.get("quarters") or []                  # most recent first; score 0..2, None = no outcome yet
    n = 4 if mode == "lite" else 8
    qs = qs[:n]
    rows = [(s, n - i) for i, s in enumerate(q.get("score") for q in qs) if s is not None]
    if not rows:
        return "not_executable", None
    sw = sum(w for _, w in rows)
    sc = sum(s * w for s, w in rows) / (2 * sw) * 10
    return round(sc, 2), {"mode": mode, "quarters_used": len(rows), "weights": [w for _, w in rows]}


def score_price_tests(d, px, R, M, dcfb, rdcf, ss):
    """D1-D4, E1-E4 at price px. Returns (scores, evidence)."""
    s, ev = {}, {}
    f = d.get("financials", {}) or {}
    v = d.get("valuation", {}) or {}
    # D1 — price vs conservative DCF midpoint (base-WACC central)
    if dcfb:
        if not dcfb["usable"]:
            s["D1"] = 0.0; ev["D1"] = "DCF negative/degenerate — D1 = 0 with flag (never 2)"
        else:
            gap = px / dcfb["central"] - 1
            s["D1"] = ladder(gap, [-0.20, 0.10], [0, 1, 2], higher_better=False)
            ev["D1"] = f"price {px} vs DCF midpoint {dcfb['central']}: {pct(gap, 1)}%"
    # D2 — price vs peer-multiple range
    mr = v.get("multiples_range")
    if mr:
        s["D2"] = ladder(px, [mr[0], mr[1]], [0, 1, 2], higher_better=False)
        ev["D2"] = f"price {px} vs peer range {mr[0]}–{mr[1]}"
    # D3 — reverse-DCF implied growth vs delivered / guidance x 0.7
    cagr = g(f, "revenue_cagr_5y"); guided = g(f, "guided_growth")
    if rdcf is not None and cagr is not None:
        if rdcf.get("unsolvable_on_growth"):
            s["D3"] = 0.0; ev["D3"] = "unsolvable on growth — 0 (restated on margin and discount rate)"
        else:
            ig = rdcf["implied_growth"] / 100
            t2 = cagr
            if guided is not None and 0.7 * guided > cagr:
                s["D3"] = ladder(ig, [t2, 0.7 * guided], [0, 1, 2], higher_better=False)
            else:
                s["D3"] = ladder(ig, [t2], [0, 2], higher_better=False)
            ev["D3"] = (f"implied {pct(ig)}% vs delivered {pct(cagr)}%"
                        + (f", guidance x0.7 {pct(0.7 * guided)}%" if guided is not None else ", no guidance"))
    # D4 — P/E vs own 10-yr median (within = +-20%; missing median = 1)
    med, eps = g(d, "valuation", "pe_10y_median"), g(d, "valuation", "eps_ttm")
    if med is None:
        s["D4"] = 1.0; ev["D4"] = "own 10-yr median not available — neutral 1 by rule (scored gap)"
    elif eps is None or eps <= 0:
        s["D4"] = 1.0; ev["D4"] = "no positive TTM EPS — P/E not meaningful, neutral 1 by rule (scored gap)"
    else:
        pe = px / eps
        gap = pe / med - 1
        s["D4"] = ladder(gap, [-0.20, 0.20], [0, 1, 2], higher_better=False)
        ev["D4"] = f"P/E {round(pe, 2)}x vs own median {med}x: {pct(gap, 1)}%"
    # E1-E4 — scenarios at px
    sc = scenarios_at(ss, px)
    if sc:
        ev_a = sc["ev_annual_pct"] / 100
        h = R["r_hurdle"]
        s["E1"] = ladder(ev_a, [h, h + 0.05], [0, 1, 2])
        ev["E1"] = f"EV {sc['ev_annual_pct']}% p.a. vs hurdle {pct(h)}% (+5pp {pct(h + 0.05)}%)"
        s["E2"] = ladder(sc["bear_drawdown_pct"] / 100, [0.20, 0.35], [0, 1, 2], higher_better=False)
        ev["E2"] = f"bear drawdown {sc['bear_drawdown_pct']}%"
        ud = sc["upside_downside"]
        if sc["bear_no_loss"]:
            s["E3"] = 2.0; ev["E3"] = "bear case shows no loss from this price — U/D unbounded, 2"
        elif ud is not None:
            s["E3"] = ladder(ud, [1.5, 3.0], [0, 1, 2]); ev["E3"] = f"U/D {ud}x"
        # E4 — discrete by construction (25% + 5pp steps): not interpolated, so 25% => 2 as spec §5 states
        bw = sc["bear_weight"]
        s["E4"] = 2.0 if bw <= 0.25 + 1e-9 else (1.0 if bw <= 0.35 + 1e-9 else 0.0)
        ev["E4"] = f"bear weight {pct(bw)}% ({len(ss['bear_triggers'])} documented trigger(s))"
    return s, ev, sc


def score_fixed_tests(d, R, M, fx, liq, mode):
    """Price-independent auto tests: A1-A3, A5, A6, C1, C5, C6, D5, E5."""
    s, ev = {}, {}
    f = d.get("financials", {}) or {}
    rv = R["r_val"]
    roce = g(f, "roce_5y")
    if roce is not None:
        s["A1"] = ladder(roce, [rv, rv + 0.05], [0, 1, 2])
        ev["A1"] = f"ROCE 5y {pct(roce)}% vs r_val {pct(rv)}% / +5pp {pct(rv + 0.05)}%"
    cagr = g(f, "revenue_cagr_5y")
    if cagr is not None:
        a2 = ladder(cagr, [0.08, 0.12], [0, 1, 2])
        down = g(f, "down_year_5y")
        if down:
            a2 = min(a2, 1.0)
        s["A2"] = a2
        ev["A2"] = f"CAGR 5y {pct(cagr)}%" + ("; down year — capped at 1" if down else "" if down is False else "; down-year flag not supplied")
    mh = g(f, "ebitda_margin_5y")
    if mh:
        rng = max(mh) - min(mh)
        s["A3"] = ladder(rng, [0.05, 0.10], [0, 1, 2], higher_better=False, mode="pp")
        ev["A3"] = f"EBITDA-margin range {pct(rng)}pp over {len(mh)} yrs"
    iroic = g(f, "incremental_roic_3y")
    if g(f, "annuity_payer"):
        s["A5"] = 1.0; ev["A5"] = "deliberate annuity payer, no reinvestment — 1 by rule"
    elif iroic is not None:
        s["A5"] = 0.0 if iroic <= 0 else ladder(iroic, [rv], [1, 2])
        ev["A5"] = f"incremental ROIC 3y {pct(iroic)}% vs r_val {pct(rv)}%"
    ts = trend_score(d.get("quarterly"))
    if ts is not None:
        s["A6"] = ts
        q = d["quarterly"]
        ev["A6"] = f"rev {q['rev_trend']}, margin {q['margin_trend']}, CFO {q['cfo_trend']}"
    # C1 — India only (promoter band); US scored manually
    own = d.get("ownership") or {}
    pl_sh = g(d, "pledge", "pledge_pct_shares", default=own.get("pledge_pct_shares"))
    pl_h = g(d, "pledge", "pledge_pct_holding", default=own.get("pledge_pct_holding"))
    if M["jurisdiction"] == "IN" and own.get("promoter") is not None and (pl_sh is not None or pl_h is not None):
        ph = own["promoter"]
        material = (pl_sh >= PLEDGE_FLOOR) if pl_sh is not None else (pl_h > 0)
        in_band = 0.40 <= ph <= 0.75 or bool(own.get("mnc_parent") and ph >= 0.75)
        c1 = None
        if not material:
            # holding band edge at 40% interpolates (1 outside band, 2 inside); >75% non-MNC = 1
            c1 = ladder(ph, [0.40], [1, 2]) if ph <= 0.75 or in_band else 1.0
        elif pl_h is not None:
            c1 = 1.0 if pl_h < 0.10 else 0.0
        if c1 is not None:
            s["C1"] = c1
            ev["C1"] = (f"promoter {pct(ph)}%, pledge "
                        f"{'?' if pl_sh is None else pct(pl_sh, 3)}% of shares / {'?' if pl_h is None else pct(pl_h)}% of holding"
                        + (" (MNC parent)" if own.get("mnc_parent") else ""))
    # C5 — credibility audit
    c5_mode = d.get("c5_mode") or ("lite" if mode == "screen" else "full")
    if mode == "full" and c5_mode == "lite":
        raise RenderRefused("FULL review requires c5_mode = 'full' (8-quarter credibility audit)")
    cs, cinfo = credibility(d, c5_mode)
    if cs == "not_executable":
        c4 = (d.get("manual_scores") or {}).get("C4")
        if c4 is None:
            raise RenderRefused("C5 not executable: score C4 first (C5 = 1 if C4 > 0, else 0)")
        s["C5"] = 1.0 if c4 > 0 else 0.0
        ev["C5"] = f"credibility audit not executable; C4 = {c4}"
    elif cs is not None:
        s["C5"] = ladder(cs, [5.0, 7.0], [0, 1, 2])
        ev["C5"] = f"credibility {cs}/10 ({c5_mode})"
    # C6 — promoter direction (net PIT buying, trailing 4Q)
    pit = d.get("pit") or {}
    if pit.get("net_buy_mcap_pct") is not None:
        x = pit["net_buy_mcap_pct"]
        c6 = ladder(x, [-0.005, 0.01], [0, 1, 2])
        val = pit.get("net_buy_value")
        thr = M["pit_abs_threshold"]
        if val is not None and val > 0.9 * thr:
            abs_s = 2.0 if val >= 1.1 * thr else round(c6 + (2 - c6) * (val - 0.9 * thr) / (0.2 * thr), 1)
            c6 = max(c6, abs_s)
        s["C6"] = c6
        ev["C6"] = f"net PIT {pct(x, 3)}% of Mcap" + (f", {val} {M['money_unit']}" if val is not None else "") + " (trailing 4Q; ESOP/warrant/inter-se excluded)"
    # D5 — cycle position
    cm, avg, peak = g(d, "cycle", "current_margin"), g(d, "cycle", "avg_10y"), g(d, "cycle", "peak_10y")
    if cm is not None and avg is not None:
        if peak is not None and cm >= peak:
            s["D5"] = 0.0
        else:
            s["D5"] = ladder(cm - avg, [0.0, 0.03], [0, 1, 2], higher_better=False, mode="pp")
        ev["D5"] = f"margin {pct(cm)}% vs 10y avg {pct(avg)}%" + (f", peak {pct(peak)}%" if peak is not None else "")
    # E5 — liquidity
    if liq.get("sessions") is not None:
        s["E5"] = ladder(liq["sessions"], [5, 10], [0, 1, 2], higher_better=False)
        ev["E5"] = f"{liq['sessions']} sessions to exit the reference position"
    return s, ev


def liquidity(d, M):
    mdv = g(d, "ownership", "median_daily_value") or g(d, "ownership", "median_daily_value_cr") \
        or g(d, "market", "median_daily_dollar_value_usd")
    if not mdv:
        return {"result": "unverified", "gate_G3": "UNVERIFIED"}
    sessions = M["liq_ref"] / (0.25 * mdv)
    return {"median_daily_value": mdv, "reference_position": M["liq_ref"], "sessions": round(sessions, 3),
            "gate_G3": "pass" if sessions <= 10 else "FAIL"}


# ══════════════════════════════════════════════════════════════════════════
# 7. DIMENSIONS, Q / P, GATES, TIER (spec §2, §6, §7)
# ══════════════════════════════════════════════════════════════════════════

def _manual_value(ms, test, which):
    x = ms.get(test)
    if isinstance(x, dict):
        if test not in PRICE_TESTS:
            raise RenderRefused(f"{test} is price-independent — give one score, not {{today, trigger}}")
        return x.get(which)
    return x


def assemble(auto_fixed, auto_price, ms, which, fx, f5_skipped):
    """Merge auto and manual scores for one price point; returns tests, overrides."""
    tests, overrides = {}, []
    for k, v in {**auto_fixed, **auto_price}.items():
        tests[k] = v
    for k in ms:
        if k.startswith("_"):
            continue
        if k in ("B",):
            raise RenderRefused("B is computed from the forensic battery — manual B refused")
        if k in ENGINE_ONLY and k in tests:
            raise RenderRefused(f"{k} is engine-scored (spec §3) — manual override refused")
        val = _manual_value(ms, k, which)
        if val is None:
            continue
        if not isinstance(val, (int, float)) or val < 0 or val > 2:
            raise RenderRefused(f"manual score {k} = {val!r} outside 0–2")
        if k in tests and tests[k] != val:
            overrides.append({"test": k, "auto": tests[k], "manual": val})
        tests[k] = float(val)
    if f5_skipped:
        tests.pop("F5", None)
    return tests, overrides


def dimensions(tests, B, f5_skipped):
    dims, missing = {}, []
    for dim, n in TEST_COUNT.items():
        ids = [f"{dim}{i}" for i in range(1, n + 1)]
        if dim == "F" and f5_skipped:
            ids = ids[:4]
        miss = [t for t in ids if t not in tests]
        missing += miss
        if miss:
            dims[dim] = None
            continue
        raw = sum(tests[t] for t in ids)
        dims[dim] = round(raw / (2 * len(ids)) * 10, 2)
    dims["B"] = B
    if B is None:
        missing.append("B (no verified forensic checks)")
    return dims, missing


def q_score(dims):
    if any(dims[k] is None for k in Q_DIMS):
        return None
    return round(sum(WEIGHTS[k] * dims[k] for k in Q_DIMS) / sum(WEIGHTS[k] for k in Q_DIMS), 2)


def p_score(dims):
    if any(dims[k] is None for k in P_DIMS):
        return None
    return round(sum(WEIGHTS[k] * dims[k] for k in P_DIMS) / sum(WEIGHTS[k] for k in P_DIMS), 2)


def validate_dims(tests, dims, f5_skipped):
    """Spec §9 item 10: dimension totals must equal their test sums — refuse to render on mismatch."""
    for dim, n in TEST_COUNT.items():
        if dims.get(dim) is None:
            continue
        ids = [f"{dim}{i}" for i in range(1, n + 1)]
        if dim == "F" and f5_skipped:
            ids = ids[:4]
        expect = round(sum(tests[t] for t in ids) / (2 * len(ids)) * 10, 2)
        if abs(expect - dims[dim]) > 0.005:
            raise RenderRefused(f"dimension {dim} = {dims[dim]} but its tests sum to {expect}")


def check_claims(d, results):
    """Optional input `claimed` {A..F, Q, P_trigger, P_today, tier}: the narrative's numbers. D and E may be
    {"today": x, "trigger": y}. Any mismatch refuses the render (spec §9 item 10)."""
    cl = d.get("claimed") or {}
    bad = []
    def cmp(label, claimed, have):
        if claimed is None:
            return
        if have is None or abs(have - claimed) > 0.05:
            bad.append(f"{label}: claimed {claimed}, computed {have}")
    for k, v in cl.items():
        if k in ("A", "B", "C", "F"):
            cmp(k, v, results["dims_today"].get(k))
        elif k in ("D", "E"):
            if isinstance(v, dict):
                cmp(f"{k}@today", v.get("today"), results["dims_today"].get(k))
                cmp(f"{k}@trigger", v.get("trigger"), results["dims_trigger"].get(k))
            else:
                cmp(f"{k}@today", v, results["dims_today"].get(k))
        elif k in ("Q", "P_trigger", "P_today"):
            cmp(k, v, results[k])
        elif k == "tier":
            if str(results["tier"]).split(" (")[0] != str(v).split(" (")[0]:
                bad.append(f"tier: claimed {v}, computed {results['tier']}")
    if bad:
        raise RenderRefused("narrative numbers do not match the engine: " + "; ".join(bad))


def gates(d, fx, liq, jur):
    gi = {k: v for k, v in (d.get("gates") or {}).items() if not k.startswith("_")}
    out, notes = {}, []
    out["G1"] = fx["gate_G1"]
    out["G3"] = liq.get("gate_G3", "UNVERIFIED")
    au = d.get("auditor") or {}
    g4_auto = None
    if au:
        if au.get("going_concern") or au.get("ifc_qualified_2y") or au.get("resignation") \
           or (au.get("opinion") not in (None, "unmodified", "unqualified")):
            g4_auto = "FAIL — auditor: going-concern / qualified or IFC-qualified within 2 yrs / resignation"
        elif all(au.get(k) is not None for k in ("going_concern", "ifc_qualified_2y", "resignation", "opinion")):
            g4_auto = "pass (auditor fields: unmodified, no going-concern, no IFC qualification in 2 yrs, no resignation)"
    for k in ("G2", "G4", "G5", "G6"):
        manual = gi.get(k)
        if k == "G6" and d.get("pathway", "public") == "public":
            out[k] = "n/a"; continue
        if k == "G4" and g4_auto:
            if g4_auto.startswith("FAIL"):
                if manual and not str(manual).upper().startswith("FAIL"):
                    notes.append("G4: manual 'pass' overruled — auditor fields fail G4")
                out[k] = g4_auto
            else:
                out[k] = manual if (manual and str(manual).upper().startswith("FAIL")) else g4_auto
            continue
        if manual is None:
            out[k] = "UNVERIFIED"
            notes.append(f"{k} not supplied — must be stated before a tier can be issued")
        else:
            out[k] = manual
    # a manual gate can fail G1/G3 but never pass one the engine failed
    for k in ("G1", "G3"):
        m = gi.get(k)
        if m and str(m).upper().startswith("FAIL"):
            out[k] = m
    failed = [k for k, v in out.items() if str(v).upper().startswith("FAIL")]
    unverified = [k for k, v in out.items() if str(v).upper() in ("UNVERIFIED",)]
    return out, failed, unverified, notes


def tier_rule(Q, gates_failed, gates_unverified, coverage_capped, trig, price, missing=None):
    """Spec §2 tier table. `trig` must be the DEFENSIBLE trigger or None."""
    if gates_failed:
        return "PASS (gate failed: " + ", ".join(gates_failed) + ")"
    if Q is None or missing:
        return "incomplete" + (f" (missing: {', '.join(missing)})" if missing else "")
    if Q < 5.0:
        return "PASS"
    caps = []
    if coverage_capped:
        caps.append("forensic coverage < minimum")
    if gates_unverified:
        caps.append("gates unverified: " + ", ".join(gates_unverified))
    defensible = trig is not None
    if Q >= 7.0 and defensible and price <= trig and not caps:
        return "INVEST NOW"
    if Q >= 6.0 and defensible and not caps:
        return "INVEST AT TRIGGER"
    if Q >= 6.0 and not defensible:
        caps.append("no defensible trigger")
    return "WATCH" + (f" (capped: {'; '.join(caps)})" if caps else "")


def tier_movers(tests, dims, fx, f5_skipped, gates_failed, gates_unv, cov, trig, price):
    """The 'one test that moves the tier' line: single Q-test changes that change the tier."""
    base = tier_rule(q_score(dims), gates_failed, gates_unv, cov, trig, price)
    moves = []
    for t, v in sorted(tests.items()):
        if t[0] not in ("A", "C", "F"):
            continue
        for new in (2.0, 0.0):
            if new == v:
                continue
            tt = dict(tests); tt[t] = new
            dd, _ = dimensions(tt, dims["B"], f5_skipped)
            q2 = q_score(dd)
            tr = tier_rule(q2, gates_failed, gates_unv, cov, trig, price)
            if tr.split(" (")[0] != base.split(" (")[0]:
                moves.append({"test": t, "from": v, "to": new, "Q": q2, "tier": tr})
    if fx["verified"]:
        for dp, df in ((1, 0), (0, 1)):
            p2, f2 = fx["passes"] + dp, fx["fails"] + df
            if p2 + f2 > fx["total"]:
                continue
            b2 = round(10 * p2 / (p2 + f2), 2)
            dd = dict(dims); dd["B"] = b2
            q2 = q_score(dd)
            gf = [x for x in gates_failed if x != "G1"]
            cov2 = cov
            if p2 + f2 >= G1_MIN_VERIFIED[fx["total"]]:
                cov2 = False
                if p2 / (p2 + f2) < G1_MIN_PASS_RATE:
                    gf = gf + ["G1"]
            elif (fx["total"] - f2) / fx["total"] < G1_MIN_PASS_RATE:
                gf = gf + ["G1"]
            tr = tier_rule(q2, gf, gates_unv, cov2, trig, price)
            if tr.split(" (")[0] != base.split(" (")[0]:
                moves.append({"test": "B", "change": "one more verified pass" if dp else "one more verified fail",
                              "Q": q2, "tier": tr})
    return moves


# ══════════════════════════════════════════════════════════════════════════
# 8. RUN
# ══════════════════════════════════════════════════════════════════════════

def validate_inputs(d):
    """Refuse clearly on inputs that would otherwise crash or silently mis-scale."""
    p = d.get("price")
    if not isinstance(p, (int, float)) or p <= 0:
        raise RenderRefused("price must be a positive number")
    v = d.get("valuation") or {}
    if d.get("sector_variant") != "financial" and v:
        if not v.get("shares") or v["shares"] <= 0:
            raise RenderRefused("valuation.shares must be positive")
        if v.get("debt_wt") is not None and not (0 <= v["debt_wt"] < 0.95):
            raise RenderRefused("valuation.debt_wt must be in [0, 0.95)")
        for k in ("terminal_g", "growth", "margin_start", "margin_end", "tax", "wc_pct", "capex_pct", "dep_pct"):
            x = v.get(k)
            if x is not None and abs(x) > 1.5:
                raise RenderRefused(f"valuation.{k} = {x}: decimals expected (0.04, not 4.0)")
        for k in ("revenue", "margin_start", "margin_end", "growth"):
            if v.get(k) is None:
                raise RenderRefused(f"valuation.{k} missing")
    for c in d.get("scenarios") or []:
        miss = [k for k in ("name", "exit_multiple") if c.get(k) is None]
        if c.get("exit_eps") is None and c.get("exit_metric") is None:
            miss.append("exit_eps")
        if not str(c.get("name", "")).lower().startswith("bear") and c.get("weight") is None:
            miss.append("weight")
        if miss:
            raise RenderRefused(f"scenario {c.get('name')!r} missing {miss}")


def run(d):
    validate_inputs(d)
    jur = (d.get("jurisdiction") or "IN").upper()
    if jur not in MACRO:
        raise RenderRefused(f"jurisdiction {jur!r} not supported (IN | US)")
    M = {**MACRO[jur], **(d.get("macro") or {})}
    mode = (d.get("mode") or "screen").lower()
    f5_skipped = bool(d.get("f5_skipped", False))
    if f5_skipped and mode == "full":
        raise RenderRefused("f5_skipped is allowed at SCREEN only — FULL runs the marquee screen (spec §3 F5)")
    price = d["price"]
    out = {"standard": STANDARD, "engine": ENGINE_VERSION, "calibration": M["calibration"], "jurisdiction": jur,
           "currency": M["currency"], "mode": mode,
           "review_date": today_et() if jur == "US" else today_ist(), "macro": M, "company": d.get("company"),
           "price": price, "price_date": d.get("price_date")}
    flags = []
    if jur == "US":
        flags.append("USA: 15% hurdle applied in USD and C6 absolute limb (US$6m) are pending Bablu's review (spec §11)")

    fx = forensic(d, M)
    out["forensic"] = fx
    liq = liquidity(d, M)
    out["liquidity"] = liq

    v = d.get("valuation")
    R = dcfb = rdcf_today = rdcf_trig = rr = tb = None
    if v and v.get("revenue") and d.get("sector_variant") != "financial":
        R = rates(d, M)
        out["rates"] = {k: (round(x, 4) if isinstance(x, float) else x) for k, x in R.items()}
        dcfb = dcf_grid(v, R, M)
        out["dcf"] = dcfb
        flags += dcfb["flags"]
        rdcf_today = reverse_dcf(v, price, R, M)
        out["reverse_dcf_today"] = rdcf_today
        tb = trigger_block(v, R, M, dcfb, price)
        out["trigger"] = tb
        if tb.get("unhealthy"):
            flags.append(tb["note"])
            tb["irr_at_trigger_pct"] = pct(M["hurdle"])   # by construction
            tb["irr_at_dcf_ceiling_pct"] = irr_at(v, R, M, dcfb["range"][1])
        if tb["trigger"] is not None:
            rdcf_trig = reverse_dcf(v, tb["trigger"], R, M)
            out["reverse_dcf_trigger"] = rdcf_trig
        out["irr_at_today_pct"] = irr_at(v, R, M, price)
        rr = range_rule(dcfb, v.get("multiples_range"), price)
        out["range_rule"] = rr
    elif d.get("sector_variant") == "financial" and v:
        # financial variant: the excess-return / DDM range and trigger are supplied from the Record
        beta, bsrc, _ = resolve_beta(d, M)
        R = {"beta": beta, "beta_source": bsrc, "r_val": M["rf"] + beta * M["erp_val"], "r_hurdle": M["hurdle"],
             "debt_wt": 0.0, "kd_post": 0.0}
        out["rates"] = R
        c = v.get("conservative_central")
        dcfb = {"central": c, "range": v.get("conservative_range"), "usable": c is not None and c > 0, "flags": []}
        out["dcf"] = dcfb
        t = v.get("hurdle_price")
        ok = t is not None and t > 0 and dcfb["usable"]
        tb = {"trigger": t if ok else None, "defensible": ok,
              "reason": ("financial variant: hurdle_price = value of the excess-return model at the 15% hurdle (supplied)"
                         if ok else "financial variant: hurdle_price missing/non-positive or conservative value unusable — no defensible entry")}
        if ok:
            tb["distance_from_price_pct"] = round((t / price - 1) * 100, 1)
            tb["discount_to_dcf_central_pct"] = round((t / c - 1) * 100, 1)
        if dcfb["usable"] is False and c is not None:
            flags.append("financial variant: conservative central <= 0 — D1 = 0, no defensible trigger")
        out["trigger"] = tb
        rdcf_today = v.get("reverse_model")
        rr = range_rule(dcfb, v.get("multiples_range"), price) if dcfb["range"] else None
        out["range_rule"] = rr
    else:
        raise RenderRefused("valuation block missing — v3 cannot tier without a DCF (trigger depends on it)")

    ss = scenario_set(d)
    out["scenario_weights"] = ss and {"bear_weight": ss["bear_weight"], "bear_triggers": ss["bear_triggers"],
                                      "cases": [{k: c[k] for k in ("name", "weight", "input_weight")} for c in ss["cases"]]}
    fixed, ev_fixed = score_fixed_tests(d, R, M, fx, liq, mode)
    ms = d.get("manual_scores") or {}
    trig = tb["trigger"] if (tb and tb.get("defensible")) else None

    res = {}
    for which, px, rd in (("today", price, rdcf_today), ("trigger", trig, rdcf_trig)):
        if px is None:
            res[which] = None
            continue
        if d.get("sector_variant") == "financial":
            rd = v.get("reverse_model_trigger") if which == "trigger" else v.get("reverse_model")
            if rd is not None and "implied_growth" not in rd:
                rd = None
        ps, ev_p, sc = score_price_tests(d, px, R, M, dcfb, rd, ss)
        tests, overrides = assemble(fixed, ps, ms, which, fx, f5_skipped)
        dims, missing = dimensions(tests, fx["B"], f5_skipped)
        validate_dims(tests, dims, f5_skipped)
        res[which] = {"price": px, "tests": tests, "evidence": {**ev_fixed, **ev_p}, "overrides": overrides,
                      "dims": dims, "missing": missing, "scenarios": sc}
    base = res["today"]
    out["tests_today"] = base["tests"]; out["evidence_today"] = base["evidence"]
    out["scenarios_today"] = base["scenarios"]
    out["overrides"] = base["overrides"]
    missing_all = list(base["missing"])
    if res["trigger"]:
        missing_all += [f"{m}@trigger" for m in res["trigger"]["missing"] if m not in base["missing"] or m in PRICE_TESTS]
    out["missing_tests"] = missing_all
    out["dims_today"] = base["dims"]
    if res["trigger"]:
        out["tests_trigger"] = {k: res["trigger"]["tests"][k] for k in PRICE_TESTS if k in res["trigger"]["tests"]}
        out["evidence_trigger"] = {k: res["trigger"]["evidence"][k] for k in PRICE_TESTS if k in res["trigger"]["evidence"]}
        out["scenarios_trigger"] = res["trigger"]["scenarios"]
        out["dims_trigger"] = res["trigger"]["dims"]
    else:
        out["dims_trigger"] = {k: None for k in "ABCDEF"}
        out["dims_trigger"].update({k: base["dims"][k] for k in Q_DIMS})

    Q = q_score(base["dims"])
    out["Q"] = Q
    out["P_today"] = p_score(base["dims"])
    out["P_trigger"] = p_score(out["dims_trigger"]) if res["trigger"] else None

    gt, gfailed, gunv, gnotes = gates(d, fx, liq, jur)
    cov = fx["gate_G1"] == "COVERAGE"
    out["gates"] = gt; out["gates_failed"] = gfailed; out["gates_unverified"] = gunv
    flags += gnotes
    out["tier"] = tier_rule(Q, gfailed, gunv, cov, trig, price, missing_all)
    if cov:
        out["promotion_condition"] = f"verify forensic checks {fx['unverified']} (need >= {G1_MIN_VERIFIED[fx['total']]} verified)"
    out["tier_movers"] = tier_movers(base["tests"], base["dims"], fx, f5_skipped, gfailed, gunv, cov, trig, price) if Q is not None else []
    out["escalate_to_full"] = (mode == "screen" and Q is not None and Q >= 5.5
                               and not str(gt.get("G1")).upper().startswith("FAIL")
                               and not str(gt.get("G4")).upper().startswith("FAIL")
                               and fx["verified"] >= G1_MIN_VERIFIED[fx["total"]])
    mos = rr.get("mos_nod") if rr else None
    out["mos_nod"] = mos
    out["flags"] = flags
    sym = M["sym"]
    out["league_row"] = (f"{M['calibration']} · {jur} · {d.get('company')} · Q {Q} · P@trigger {out['P_trigger']} · "
                         f"P@today {out['P_today']} · {out['tier']} · trigger "
                         + (f"{sym}{trig:,.2f} ({tb['distance_from_price_pct']}%)" if trig else "none")
                         + f" · MoS nod {'Y' if mos else 'N'}")
    check_claims(d, out)
    out["narrative_check"] = "claimed numbers match" if d.get("claimed") else \
        "not run — pass `claimed` with the Note's numbers before publishing (render refuses on mismatch)"
    return out


# ══════════════════════════════════════════════════════════════════════════
# 9. SUMMARY
# ══════════════════════════════════════════════════════════════════════════

def _fmt(x):
    return "—" if x is None else (f"{x:g}" if isinstance(x, (int, float)) else str(x))


def summary(r):
    M = r["macro"]; sym = M["sym"]
    L = [f"{r['standard']} · {r['engine']} · {r['calibration']} · {r['jurisdiction']} · {r['mode'].upper()} · "
         f"review date {r['review_date']}",
         f"{r['company']} @ {sym}{r['price']:,} ({r.get('price_date')})"]
    if r.get("rates"):
        R = r["rates"]
        L.append(f"RATES  r_val {pct(R['r_val'])}% (rf {pct(M['rf'])}% + β {R['beta']} [{R['beta_source']}] × {pct(M['erp_val'])}%) · "
                 f"WACC@r_val {pct(R.get('wacc_val'))}% · r_hurdle {pct(R['r_hurdle'])}% (WACC@hurdle {pct(R.get('wacc_hurdle'))}%) · "
                 f"D/(D+E) {pct(R.get('debt_wt'))}% [{R.get('capital_structure', '')}]")
    fx = r["forensic"]
    L.append(f"\nFORENSIC ({fx['variant']})  {fx['passes']}/{fx['verified']} verified pass · B {fx['B']} · "
             f"G1 {fx['gate_G1']} — {fx['gate_G1_reason']}")
    for c in fx["checks"]:
        mark = {"pass": "OK  ", "fail": "FAIL", "unverified": "??  "}.get(c["result"], "??  ")
        extra = (" · " + c["note"]) if c.get("note") else ""
        num = c["number"] if not isinstance(c["number"], dict) else f"M {c['number'].get('M')}" + (f", Altman {c['number'].get('altman')}" if c['number'].get('altman') else "")
        L.append(f"  {mark} {c['n']:>2}. {c['check']}: {num}{extra}")
    if fx["reconcile_4_9"]:
        L.append("  " + fx["reconcile_4_9"])
    if fx["unverified"]:
        L.append(f"  follow-ups: {fx['follow_ups']}")
    d = r.get("dcf")
    if d and d.get("grid"):
        L.append(f"\nDCF @ r_val  range {sym}{_fmt(d['range'][0] if d['range'] else None)}–{_fmt(d['range'][1] if d['range'] else None)} · "
                 f"midpoint {sym}{_fmt(d['central'])} · band {d['band_width_pct']}% · TV share {d['meta'].get('tv_share_pct')}% · "
                 f"g {pct(d['meta'].get('terminal_g'))}%")
    for f in r.get("flags", []):
        L.append(f"  FLAG: {f}")
    for key, label in (("reverse_dcf_today", "today"), ("reverse_dcf_trigger", "trigger")):
        rd = r.get(key)
        if rd and "implied_growth" in rd:
            if rd.get("unsolvable_on_growth"):
                L.append(f"REVERSE DCF @{label}  {rd['note']}")
            else:
                L.append(f"REVERSE DCF @{label}  the price assumes {rd['implied_growth']}% growth for 5 yrs · "
                         f"implied WACC {rd['implied_wacc']}% (equity {rd['implied_equity_return']}%)"
                         + ("" if rd['solver'].get('monotone', True) else f" · non-monotone above g={rd['solver'].get('turning_point')}"))
    tb = r.get("trigger")
    if tb:
        if tb["trigger"] is None:
            L.append(f"TRIGGER  none — {tb['reason']}")
        else:
            L.append(f"TRIGGER  {sym}{tb['trigger']:,} (= P at 15% hurdle; {tb.get('discount_to_dcf_central_pct')}% vs DCF midpoint) · "
                     f"distance {tb.get('distance_from_price_pct')}%"
                     + (f" · UNHEALTHY — a buyer at the DCF ceiling earns {tb.get('irr_at_dcf_ceiling_pct')}% vs the 15% hurdle"
                        if tb.get("unhealthy") else ""))
    if r.get("irr_at_today_pct") is not None:
        L.append(f"RETURN ON DCF CASH FLOWS at today's price: {r['irr_at_today_pct']}% p.a. vs hurdle {pct(M['hurdle'])}%")
    rr = r.get("range_rule")
    if rr:
        if rr["disjoint"]:
            L.append(f"RANGE RULE  DISJOINT — DCF {rr['dcf_range']} | multiples {rr['multiples_range']} · no blended value · "
                     f"MoS line {sym}{_fmt(rr['mos_line'])} (0.8 × DCF midpoint) · MoS nod {'Y' if rr['mos_nod'] else 'N'}")
        else:
            L.append(f"RANGE RULE  overlap {rr['overlap']} · fair value {sym}{rr['fair_value']:,} (midpoint) · "
                     f"MoS line {sym}{rr['mos_line']:,} · MoS nod {'Y' if rr['mos_nod'] else 'N'}")
    for key, label in (("scenarios_today", "today"), ("scenarios_trigger", "trigger")):
        s = r.get(key)
        if s:
            L.append(f"SCENARIOS @{label} {sym}{s['price']:,}  EV {s['ev_annual_pct']}% p.a. · bear −{s['bear_drawdown_pct']}% × "
                     f"{pct(s['bear_weight'], 0)}% · U/D {s['upside_downside']}")
    sw = r.get("scenario_weights")
    if sw:
        L.append(f"  bear weight {pct(sw['bear_weight'], 0)}% = 25% + 5pp × {len(sw['bear_triggers'])} trigger(s)"
                 + (f": {sw['bear_triggers']}" if sw["bear_triggers"] else ""))
    lq = r["liquidity"]
    if lq.get("sessions") is not None:
        L.append(f"LIQUIDITY  reference position exits in {lq['sessions']} sessions · G3 {lq['gate_G3']}")
    L.append("\nSCORECARD (tests at today's price; D/E also at trigger)")
    tt, ev = r["tests_today"], r["evidence_today"]
    trg = r.get("tests_trigger", {})
    for dim in "ACDEF":
        ids = sorted(k for k in tt if k[0] == dim) + [k for k in r["missing_tests"] if k[0] == dim]
        cells = []
        for k in sorted(set(ids)):
            v_ = tt.get(k)
            cell = f"{k} {_fmt(v_)}"
            if k in trg:
                cell += f" (@trig {_fmt(trg[k])})"
            cells.append(cell)
        L.append(f"  {dim}: " + " · ".join(cells))
    L.append(f"  dims today   {r['dims_today']}")
    L.append(f"  dims trigger {r['dims_trigger']}")
    if r["missing_tests"]:
        L.append(f"  MISSING: {r['missing_tests']}")
    L.append(f"  narrative check: {r['narrative_check']}")
    if r["overrides"]:
        L.append(f"  manual overrides of auto scores: {r['overrides']}")
    L.append(f"\nQ {r['Q']} · P@trigger {r['P_trigger']} · P@today {r['P_today']}")
    L.append(f"GATES {r['gates']}")
    L.append(f"TIER  {r['tier']}")
    if r.get("promotion_condition"):
        L.append(f"  promotion condition: {r['promotion_condition']}")
    if r["tier_movers"]:
        L.append("  one test that moves the tier: " + "; ".join(
            f"{m['test']} {m.get('from', '')}→{m.get('to', m.get('change', ''))} ⇒ Q {m['Q']} {m['tier']}" for m in r["tier_movers"][:6]))
    else:
        L.append("  no single test moves the tier")
    L.append(f"  escalate to FULL: {'yes' if r['escalate_to_full'] else 'no'}")
    L.append(f"\nLEAGUE ROW  {r['league_row']}")
    return "\n".join(L)


def _json_default(o):
    if isinstance(o, float) and math.isinf(o):
        return "inf"
    return str(o)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    data = json.load(open(sys.argv[1]))
    try:
        res = run(data)
    except RenderRefused as e:
        print(f"RENDER REFUSED: {e}", file=sys.stderr)
        sys.exit(2)
    if "--pretty" in sys.argv:
        print(summary(res))
    else:
        print(json.dumps(res, indent=2, default=_json_default, ensure_ascii=False))
