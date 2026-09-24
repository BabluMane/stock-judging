#!/usr/bin/env python3
"""
Equity Review Standard v2 — deterministic calculation engine.

Every mechanical computation in the standard lives here so the model never
spends tokens reasoning arithmetic. Fill one JSON input file, run this, read
the results.

    python3 engine.py input.json > results.json
    python3 engine.py input.json --pretty     # human-readable summary

Missing inputs are handled: a check with missing data returns "unverifiable"
(not a pass, not a fail) and is reported as a scored gap.
"""

import json, sys, math
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

def today_ist():
    """All review dates are IST (Standard v2 s.3)."""
    return datetime.now(timezone.utc).astimezone(IST).strftime("%Y-%m-%d")

# ── Macro block (Standard v2 §3) — fixed per results season ────────────────
RF = 0.0695            # India 10-yr G-Sec, Trading Economics 4 Sep 2026
ERP = 0.060            # INR terms
TAX = 0.2517           # s.115BAA
TERMINAL_G_CAP = 0.06   # <= risk-free rate (6.95%); see Standard v2 s.3


def g(d, *path, default=None):
    """Safe nested get."""
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur or cur[k] is None:
            return default
        cur = cur[k]
    return cur


def pct(x):
    return None if x is None else round(x * 100, 2)


# ══════════════════════════════════════════════════════════════════════════
# 1. FORENSIC BATTERY (§6) — 10 checks
# ══════════════════════════════════════════════════════════════════════════

def beneish(f):
    """8-component Beneish M-score. Returns (M, components) or (None, reason)."""
    need = ["revenue", "receivables", "cogs", "current_assets", "ppe_net",
            "securities", "total_assets", "depreciation", "sga", "debt", "cfo", "ni"]
    for period in ("t", "t1"):
        for k in need:
            if g(f, period, k) is None:
                return None, f"missing {period}.{k}"
    t, p = f["t"], f["t1"]

    dsri = (t["receivables"] / t["revenue"]) / (p["receivables"] / p["revenue"])
    gm_t = (t["revenue"] - t["cogs"]) / t["revenue"]
    gm_p = (p["revenue"] - p["cogs"]) / p["revenue"]
    gmi = gm_p / gm_t
    soft_t = 1 - (t["current_assets"] + t["ppe_net"] + t["securities"]) / t["total_assets"]
    soft_p = 1 - (p["current_assets"] + p["ppe_net"] + p["securities"]) / p["total_assets"]
    aqi = soft_t / soft_p if soft_p else 1.0
    sgi = t["revenue"] / p["revenue"]
    dep_t = t["depreciation"] / (t["depreciation"] + t["ppe_net"])
    dep_p = p["depreciation"] / (p["depreciation"] + p["ppe_net"])
    depi = dep_p / dep_t
    sgai = (t["sga"] / t["revenue"]) / (p["sga"] / p["revenue"])
    lvgi = ((t["debt"]) / t["total_assets"]) / ((p["debt"]) / p["total_assets"]) if p["debt"] else 1.0
    tata = (t["ni"] - t["cfo"]) / t["total_assets"]

    m = (-4.84 + 0.920*dsri + 0.528*gmi + 0.404*aqi + 0.892*sgi
         + 0.115*depi - 0.172*sgai + 4.679*tata - 0.327*lvgi)
    return round(m, 4), {"DSRI": round(dsri,4), "GMI": round(gmi,4), "AQI": round(aqi,4),
                         "SGI": round(sgi,4), "DEPI": round(depi,4), "SGAI": round(sgai,4),
                         "LVGI": round(lvgi,4), "TATA": round(tata,4)}


def forensic(d):
    """Returns list of 10 checks: name, result (pass/fail/unverifiable), number."""
    f = d.get("financials", {})
    out = []

    def add(n, name, result, number):
        out.append({"n": n, "check": name, "result": result, "number": number})

    # 1 cumulative CFO/EBITDA >= 70%
    cfo = g(f, "cumulative", "cfo"); ebitda = g(f, "cumulative", "ebitda")
    if cfo and ebitda:
        r = cfo / ebitda
        add(1, "cumulative CFO/EBITDA >=70%", "pass" if r >= 0.70 else "fail", f"{pct(r)}%")
    else:
        add(1, "cumulative CFO/EBITDA >=70%", "unverifiable", "missing cumulative CFO or EBITDA")

    # 2 CFO/PAT 5-yr avg >= 80%
    v = g(f, "cfo_pat_5y_avg")
    add(2, "CFO/PAT 5-yr avg >=80%",
        "unverifiable" if v is None else ("pass" if v >= 0.80 else "fail"),
        v if v is None else round(v, 3))

    # 3 receivable days not up >10d over 3y
    a, b = g(f, "debtor_days_start"), g(f, "debtor_days_end")
    if a is not None and b is not None:
        add(3, "debtor days +<=10d over 3y", "pass" if (b - a) <= 10 else "fail",
            f"{a} -> {b} ({b-a:+.1f}d)")
    else:
        add(3, "debtor days +<=10d over 3y", "unverifiable", "missing debtor days")

    # 4 other income <10% PBT (treasury exception)
    oi, pbt = g(f, "other_income"), g(f, "pbt")
    if oi is not None and pbt:
        r = oi / pbt
        exc = d.get("treasury_income_exception", False)
        add(4, "other income <10% of PBT", "pass" if (r < 0.10 or exc) else "fail",
            f"{pct(r)}%" + (" (treasury exception, §6)" if exc and r >= 0.10 else ""))
    else:
        add(4, "other income <10% of PBT", "unverifiable", "missing other income or PBT")

    # 5 contingent liabilities <10% net worth
    cl, nw = g(f, "contingent_liabilities"), g(f, "net_worth")
    if cl is not None and nw:
        r = cl / nw
        add(5, "contingent liabilities <10% NW", "pass" if r < 0.10 else "fail", f"{pct(r)}%")
    else:
        add(5, "contingent liabilities <10% NW", "unverifiable", "AR note not retrieved")

    # 6 RPT <5% revenue; group loans <2% NW
    rpt, rev = g(f, "rpt_total"), g(f, "revenue")
    if rpt is not None and rev:
        r = rpt / rev
        add(6, "RPT <5% of revenue", "pass" if r < 0.05 else "fail", f"{pct(r)}%")
    else:
        add(6, "RPT <5% of revenue", "unverifiable", "RPT note not retrieved")

    # 7 auditor clean
    a = d.get("auditor", {})
    ok = (a.get("opinion") == "unmodified" and not a.get("resignation")
          and not a.get("adverse_caro"))
    add(7, "auditor clean, no resignation", "pass" if ok else ("unverifiable" if not a else "fail"),
        f"{a.get('name','?')}, {a.get('opinion','?')}")

    # 8 depreciation rate stable +-2pp
    ds, de = g(f, "dep_rate_start"), g(f, "dep_rate_end")
    if ds is not None and de is not None:
        add(8, "depreciation rate +-2pp", "pass" if abs(de - ds) <= 0.02 else "fail",
            f"{pct(ds)}% -> {pct(de)}%")
    else:
        add(8, "depreciation rate +-2pp", "unverifiable", "gross block not retrieved")

    # 9 cash yield >=4%, pledge 0
    cy, pl = g(f, "cash_yield"), g(d, "ownership", "pledge")
    if cy is not None and pl is not None:
        add(9, "cash yield >=4%, pledge 0", "pass" if (cy >= 0.04 and pl == 0) else "fail",
            f"yield {pct(cy)}%, pledge {pct(pl)}%")
    else:
        add(9, "cash yield >=4%, pledge 0", "unverifiable", "missing cash yield or pledge")

    # 10 Beneish
    m, comp = beneish(f)
    if m is None:
        add(10, "Beneish M < -1.78", "unverifiable", comp)
    else:
        add(10, "Beneish M < -1.78", "pass" if m < -1.78 else "fail",
            {"M": m, "components": comp, "margin_vs_bar": round(-1.78 - m, 4)})

    passes = sum(1 for c in out if c["result"] == "pass")
    unver = [c["n"] for c in out if c["result"] == "unverifiable"]
    return {"checks": out, "score": passes, "unverifiable": unver,
            "gate_G1": "pass" if passes >= 6 else "FAIL"}


# ══════════════════════════════════════════════════════════════════════════
# 2. VALUATION (§7)
# ══════════════════════════════════════════════════════════════════════════

def wacc(beta, debt_wt=0.0, kd=0.0):
    ke = RF + beta * ERP
    return ke * (1 - debt_wt) + kd * (1 - TAX) * debt_wt


def dcf(v, w):
    """Single DCF run. v = valuation inputs dict."""
    rev = v["revenue"]; margin = v["margin_start"]; me = v["margin_end"]
    growth = v["growth"]; years = v.get("years", 5)
    tg = min(v.get("terminal_g", 0.05), TERMINAL_G_CAP, RF)  # never above risk-free
    capex_pct = v.get("capex_pct", 0.01); wc_pct = v.get("wc_pct", 0.0)
    tax = v.get("tax", TAX); dep_pct = v.get("dep_pct", capex_pct)
    shares = v["shares"]; net_cash = v.get("net_cash", 0.0)

    pv = 0.0; r = rev
    for i in range(1, years + 1):
        r *= (1 + growth)
        m = margin + (me - margin) * (i / years)
        ebitda = r * m
        dep = r * dep_pct
        ebit = ebitda - dep
        nopat = ebit * (1 - tax)
        fcff = nopat + dep - r * capex_pct - (r * growth) * wc_pct
        pv += fcff / ((1 + w) ** i)
    tv = fcff * (1 + tg) / (w - tg)
    pv += tv / ((1 + w) ** years)
    return (pv + net_cash) / shares


def dcf_grid(v):
    """DCF with WACC +-1pp sensitivity. Returns range and grid."""
    beta = v.get("beta", 1.0)
    base = wacc(beta, v.get("debt_wt", 0.0), v.get("kd", 0.0))
    grid = {}
    for label, w in (("low", base - 0.01), ("base", base), ("high", base + 0.01)):
        grid[label] = {"wacc": round(w, 4), "value": round(dcf(v, w), 0)}
    vals = [grid[k]["value"] for k in grid]
    return {"base_wacc": round(base, 4), "grid": grid,
            "range": [min(vals), max(vals)], "central": grid["base"]["value"],
            "band_width_pct": round((max(vals) - min(vals)) / min(vals) * 100, 1)}


def reverse_dcf(v, price):
    """Solve for the growth the current price implies."""
    beta = v.get("beta", 1.0)
    w = wacc(beta, v.get("debt_wt", 0.0), v.get("kd", 0.0))
    lo, hi = -0.20, 1.00
    for _ in range(200):
        mid = (lo + hi) / 2
        trial = dict(v); trial["growth"] = mid
        if dcf(trial, w) < price:
            lo = mid
        else:
            hi = mid
    implied = (lo + hi) / 2
    unsolvable = implied > 0.95 or implied < -0.15
    # implied discount rate at delivered growth
    lo2, hi2 = 0.01, 0.50
    for _ in range(200):
        mid2 = (lo2 + hi2) / 2
        if dcf(v, mid2) > price:
            lo2 = mid2
        else:
            hi2 = mid2
    res = {"implied_growth": None if unsolvable else pct(implied),
           "wacc_used": round(w, 4),
           "implied_discount_rate": pct((lo2 + hi2) / 2)}
    if unsolvable:
        # growth does not add value (incremental ROIC <= WACC): restate on margin
        lo3, hi3 = 0.05, 0.95
        for _ in range(200):
            mid3 = (lo3 + hi3) / 2
            trial = dict(v); trial["margin_end"] = mid3
            if dcf(trial, w) < price: lo3 = mid3
            else: hi3 = mid3
        res["unsolvable_on_growth"] = True
        res["implied_terminal_margin"] = pct((lo3 + hi3) / 2)
        res["note"] = ("Growth does not solve: incremental returns at or below WACC, "
                       "so faster growth does not raise value. Restated on margin - "
                       "state the implied terminal margin against delivered and guided.")
    return res


def range_rule(dcf_rng, mult_rng):
    """§7 range rule. Returns verdict, fair value, trigger."""
    d_lo, d_hi = dcf_rng; m_lo, m_hi = mult_rng
    overlap = not (d_hi < m_lo or m_hi < d_lo)
    if overlap:
        lo, hi = max(d_lo, m_lo), min(d_hi, m_hi)
        return {"disjoint": False, "fair_value": [round(lo), round(hi)],
                "trigger": round(min(lo, hi) * 0.80),
                "note": "ranges overlap; overlap is the range"}
    trig = round(m_lo * 0.80)
    excess = (trig - d_hi) / d_hi
    healthy = trig <= d_hi
    base = {"disjoint": True, "dcf_range": [round(d_lo), round(d_hi)],
            "multiples_range": [round(m_lo), round(m_hi)],
            "fair_value": None,
            "trigger_vs_dcf_ceiling_pct": round(excess * 100, 1),
            "healthy": healthy}
    if excess > 0.50:
        base.update({
            "trigger": None,
            "no_defensible_entry": True,
            "note": ("NO DEFENSIBLE ENTRY PRICE — the computed trigger sits "
                     f"{excess*100:.0f}% above the conservative ceiling. The methods "
                     "disagree by more than any margin of safety can bridge (§7). "
                     "Report Trigger: none, Distance: n/a; state which method must be "
                     "wrong, and by how much, for an entry to exist.")})
        return base
    base.update({"trigger": trig,
                 "no_defensible_entry": False,
                 "note": ("trigger at or below the conservative ceiling — healthy"
                          if healthy else
                          "trigger ABOVE the conservative ceiling — unhealthy (§7): "
                          "not defensible on the cash-flow method even at entry")})
    return base


# ══════════════════════════════════════════════════════════════════════════
# 3. SCENARIOS (§8)
# ══════════════════════════════════════════════════════════════════════════

def scenarios(cases, price):
    tot = 0.0; rows = []
    for c in cases:
        val = c["exit_eps"] * c["exit_multiple"] + c.get("dividends", 0)
        ret = val / price - 1
        tot += ret * c["weight"]
        rows.append({"case": c["name"], "weight": c["weight"], "value": round(val),
                     "return_pct": pct(ret)})
    bear = next((r for r in rows if r["case"].lower().startswith("bear")), None)
    bull = next((r for r in rows if r["case"].lower().startswith("bull")), None)
    ud = None
    if bear and bull and bear["return_pct"] < 0:
        ud = round(bull["return_pct"] / abs(bear["return_pct"]), 3)
    bw = next((c["weight"] for c in cases if c["name"].lower().startswith("bear")), 0)
    return {"cases": rows, "ev_3yr_pct": pct(tot), "ev_annual_pct": pct((1+tot)**(1/3)-1),
            "reporting_note": "Quote EV and COE both annualised: 'EV x.x% p.a. vs COE y.y%'.",
            "bear_drawdown_pct": bear["return_pct"] if bear else None,
            "bear_weight": bw,
            "prob_weighted_drawdown_pct": round(abs(bear["return_pct"]) * bw, 2) if bear else None,
            "upside_downside": ud}


# ══════════════════════════════════════════════════════════════════════════
# 4. SCORECARD (§5) — 30 tests, weighted composite, gates
# ══════════════════════════════════════════════════════════════════════════

WEIGHTS = {"A": 0.15, "B": 0.20, "C": 0.20, "D": 0.15, "E": 0.20, "F": 0.10}


def score(d, computed):
    """Scores what can be scored mechanically; the rest come from `manual_scores`."""
    s = d.get("manual_scores", {})     # {"A1":2,"A2":1,...} agent supplies judgement calls
    auto = {}

    coe = RF + g(d, "valuation", "beta", default=1.0) * ERP

    # A1 ROCE vs COE
    roce = g(d, "financials", "roce_5y")
    if roce is not None:
        auto["A1"] = 2 if roce > coe + 0.05 else (1 if roce > coe else 0)
    # A2 revenue CAGR
    cagr = g(d, "financials", "revenue_cagr_5y")
    if cagr is not None:
        auto["A2"] = 2 if cagr >= 0.12 else (1 if cagr >= 0.08 else 0)
    # B = forensic score, mapped 0-10 -> dimension score
    auto["B"] = computed["forensic"]["score"]
    # D1 price vs DCF midpoint
    price = d["price"]
    if computed.get("dcf"):
        mid = computed["dcf"]["central"]
        gap = price / mid - 1
        auto["D1"] = 2 if gap <= -0.20 else (1 if abs(gap) <= 0.10 else 0)
    # D3 implied vs delivered growth
    rd = computed.get("reverse_dcf")
    if rd and cagr is not None:
        if rd.get("unsolvable_on_growth"):
            auto["D3"] = 0   # price implies a margin the business has never earned
        elif rd.get("implied_growth") is not None:
            auto["D3"] = 2 if rd["implied_growth"] <= cagr * 100 else 0
    # E1 EV vs COE
    sc = computed.get("scenarios")
    if sc:
        ev = sc["ev_annual_pct"] / 100
        auto["E1"] = 2 if ev >= coe + 0.05 else (1 if ev >= coe else 0)
        dd = abs(sc["bear_drawdown_pct"] or 0)
        auto["E2"] = 2 if dd <= 20 else (1 if dd <= 35 else 0)
        ud = sc["upside_downside"]
        if ud is not None:
            auto["E3"] = 2 if ud >= 3 else (1 if ud >= 1.5 else 0)
        auto["E4"] = 2 if sc["bear_weight"] <= 0.25 else (1 if sc["bear_weight"] <= 0.35 else 0)

    merged = {**auto, **s}   # manual overrides auto where the agent has judged

    dims = {}
    for dim in "ABCDEF":
        if dim == "B":
            dims["B"] = merged.get("B", 0)
            continue
        tests = [merged[k] for k in merged if k.startswith(dim) and len(k) == 2 and k[1].isdigit()]
        dims[dim] = sum(tests) if tests else None

    composite = None
    if all(dims[k] is not None for k in dims):
        composite = round(sum(dims[k] * WEIGHTS[k] for k in dims), 2)

    gates = d.get("gates", {})
    gates.setdefault("G1", computed["forensic"]["gate_G1"])
    failed = [k for k, v in gates.items() if str(v).upper().startswith("FAIL")]

    if failed:
        tier = "PASS (gate failed: " + ", ".join(failed) + ")"
    elif composite is None:
        tier = "incomplete"
    elif composite >= 7.0 and computed.get("trigger") and price <= computed["trigger"]:
        tier = "INVEST NOW"
    elif composite >= 6.0:
        tier = "INVEST AT TRIGGER"
    elif composite >= 5.0:
        tier = "WATCH"
    else:
        tier = "PASS"

    return {"dimensions": dims, "auto_scored": auto, "composite": composite,
            "conviction": composite, "gates": gates, "gates_failed": failed,
            "tier": tier, "coe": round(coe, 4)}


# ══════════════════════════════════════════════════════════════════════════
# 5. LIQUIDITY (§5 E5 / gate G3)
# ══════════════════════════════════════════════════════════════════════════

def liquidity(d):
    mdv = g(d, "ownership", "median_daily_value_cr")
    if not mdv:
        return {"result": "unverifiable"}
    sessions = 1.0 / (0.25 * mdv)      # ₹1 Cr at 25% of median daily value
    return {"median_daily_value_cr": mdv, "sessions_to_exit_1cr": round(sessions, 3),
            "E5": 2 if sessions <= 5 else (1 if sessions <= 10 else 0),
            "gate_G3": "pass" if sessions <= 10 else "FAIL"}


# ══════════════════════════════════════════════════════════════════════════

def run(d):
    out = {"review_date_ist": today_ist(),
           "macro": {"risk_free": RF, "erp": ERP, "tax": TAX,
                     "terminal_g_cap": TERMINAL_G_CAP}}
    out["forensic"] = forensic(d)
    out["liquidity"] = liquidity(d)

    v = d.get("valuation")
    if v and v.get("revenue"):
        out["dcf"] = dcf_grid(v)
        out["reverse_dcf"] = reverse_dcf(v, d["price"])
        mult = v.get("multiples_range")
        if mult:
            rr = range_rule(out["dcf"]["range"], mult)
            out["range_rule"] = rr
            out["trigger"] = rr["trigger"]
            out["distance_to_trigger_pct"] = (
                None if rr["trigger"] is None
                else round((rr["trigger"] / d["price"] - 1) * 100, 1))

    if d.get("scenarios"):
        out["scenarios"] = scenarios(d["scenarios"], d["price"])
        c = out["scenarios"]
        dec = d.get("decomposition")
        if dec:
            out["decomposition"] = dec

    out["scorecard"] = score(d, out)
    return out


def summary(r):
    L = [f"REVIEW DATE (IST) {r.get('review_date_ist')}"]
    f = r["forensic"]
    L.append(f"FORENSIC {f['score']}/10 (G1 {f['gate_G1']})"
             + (f" · unverifiable: {f['unverifiable']}" if f["unverifiable"] else ""))
    for c in f["checks"]:
        mark = {"pass": "OK  ", "fail": "FAIL", "unverifiable": "??  "}[c["result"]]
        L.append(f"  {mark} {c['n']:>2}. {c['check']}: {c['number']}")
    if "dcf" in r:
        d = r["dcf"]
        L.append(f"\nDCF  WACC {pct(d['base_wacc'])}%  range {d['range'][0]:,}–{d['range'][1]:,}"
                 f"  central {d['central']:,}  (±1pp band = {d['band_width_pct']}% wide)")
        rd = r["reverse_dcf"]
        if rd.get("unsolvable_on_growth"):
            L.append(f"REVERSE DCF  UNSOLVABLE ON GROWTH - implied terminal margin "
                     f"{rd['implied_terminal_margin']}%  ({rd['note']})")
        else:
            L.append(f"REVERSE DCF  implied growth {rd['implied_growth']}%"
                     f"  implied discount rate {rd['implied_discount_rate']}%")
    if "range_rule" in r:
        rr = r["range_rule"]
        L.append(f"RANGE RULE  {'DISJOINT' if rr['disjoint'] else 'overlap'} — {rr['note']}")
        if rr.get("no_defensible_entry"):
            L.append("  TRIGGER: none - no defensible entry price. Distance: n/a")
        else:
            L.append(f"  trigger {rr['trigger']:,}  distance {r.get('distance_to_trigger_pct')}%")
    if "scenarios" in r:
        s = r["scenarios"]
        L.append(f"\nSCENARIOS  EV {s['ev_3yr_pct']}% over 3y ({s['ev_annual_pct']}% p.a.)"
                 f"  bear {s['bear_drawdown_pct']}% × {s['bear_weight']}"
                 f" = {s['prob_weighted_drawdown_pct']}pp  U/D {s['upside_downside']}x")
    sc = r["scorecard"]
    L.append(f"\nSCORECARD  {sc['dimensions']}  composite {sc['composite']}"
             f"  COE {pct(sc['coe'])}%")
    L.append(f"TIER  {sc['tier']}"
             + (f"  GATES FAILED: {sc['gates_failed']}" if sc["gates_failed"] else "  gates pass"))
    return "\n".join(L)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    data = json.load(open(sys.argv[1]))
    res = run(data)
    if "--pretty" in sys.argv:
        print(summary(res))
    else:
        print(json.dumps(res, indent=2))
