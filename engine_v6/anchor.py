"""§2 entry anchor: inverse-DCF implied-growth hurdle.

Decisional rule = trigger-price comparison (§2.3). g_implied is REPORTING ONLY.
Valuation skeleton, g_sus construction (C1/C2/C3/C4/C5), margin/dep definitions,
net cash and the degenerate guard are carried verbatim from
validation/v3_11_oos/run_v311_validation.py (the v3.10 family).
"""
from . import constants as C
from .pit import cell, window_years


# ------------------------------------------------------------------ §2.2 g_sus
def roe_terms(fy, scoring_fy):
    """V310-C1: mean over the last three FYs of PAT_t / (EquityCapital_t + Reserves_t),
    each year on its own year-end book. V310-C5: zero (or missing) book -> year
    skipped; negative book computed literally."""
    per_year, pats = [], []
    for y in window_years(fy, scoring_fy, C.ROE_YEARS):
        pat = cell(fy, y, "net_profit")
        ec, res = cell(fy, y, "equity_capital"), cell(fy, y, "reserves")
        if pat is None or ec is None or res is None or (ec + res) == 0:
            continue
        per_year.append({"fy": y, "pat": pat, "book": ec + res, "roe": pat / (ec + res)})
        pats.append(pat)
    return per_year, pats


def sustainable_growth(fy, scoring_fy, cap=None):
    """g_sus = min(ROE_avg3 x (1 - payout), 0.15).
    C2: payout = Dividend Payout % / 100 as-is (unclipped; blank -> 0).
    C3: no floor (negative allowed). C4: <3 FYs -> mean of those available (>=1)."""
    cap = C.G_CAP if cap is None else cap     # `cap` override is reporting-only (§2.2 sensitivity)
    per_year, _ = roe_terms(fy, scoring_fy)
    if not per_year:
        return None, "no computable ROE year (C4)"
    roe_avg3 = sum(y["roe"] for y in per_year) / len(per_year)
    payout_raw = cell(fy, scoring_fy, "dividend_payout_pct")
    payout = 0.0 if payout_raw is None else payout_raw / 100
    raw = roe_avg3 * (1 - payout)
    return {"roe_avg3": roe_avg3, "payout": payout, "payout_raw": payout_raw,
            "g_sus_uncapped": raw, "g_sus": min(raw, cap), "cap": cap,
            "cap_binding": raw > cap, "roe_years": per_year}, None


def hurdle_growth(g_sus, k):
    """g_h(k) = g_sus - (1-k)|g_sus|  (= k*g_sus when g_sus >= 0; never loosens a
    shrinking business's hurdle)."""
    return g_sus - (1 - k) * abs(g_sus)


# ----------------------------------------------------------------- §2.1 FCFF
def growth_path(g, tg=C.TG):
    """g_t for t = 1..21.  t<=10: g.  t=11..19: g + (TG-g)(t-10)/10.  t>=20: TG."""
    out = []
    for t in range(1, C.HORIZON_YEARS + 2):
        if t <= C.GROWTH_YEARS:
            out.append(g)
        elif t < C.HORIZON_YEARS:
            out.append(g + (tg - g) * (t - C.GROWTH_YEARS) / C.FADE_YEARS)
        else:
            out.append(tg)
    return out


def fcff_flow(r_prev, r_t, m, dp):
    """FCFF_t = r_t (m - dp)(1 - TAX) - (r_t - r_{t-1}) wc.

    Cancellation, written out (capex_pct = dp, carried simplification):
      FCFF_t = NOPAT_t + D&A_t - Capex_t - dWC_t
             = r_t(m - dp)(1-TAX) + r_t*dp - r_t*cp - (r_t - r_{t-1})*wc
      with cp = dp:  + r_t*dp - r_t*dp = 0
             = r_t(m - dp)(1-TAX) - (r_t - r_{t-1})*wc.
    `fcff_flow_uncancelled` keeps the long form so a test/audit can check equality."""
    return r_t * (m - dp) * (1 - C.TAX) - (r_t - r_prev) * C.WC_PCT


def fcff_flow_uncancelled(r_prev, r_t, m, dp, cp):
    return (r_t * (m - dp) * (1 - C.TAX) + r_t * dp - r_t * cp
            - (r_t - r_prev) * C.WC_PCT)


def enterprise_value(v, w, g, audit=False):
    """EV(g) = sum_{t=1..20} FCFF_t/(1+w)^t + TV/(1+w)^20, TV = FCFF_21/(w-TG),
    FCFF_21 at g_21 = TG. None if w <= TG + 0.5pp (degenerate guard)."""
    if w <= C.TG + C.DEGENERATE_MARGIN:
        return None
    m, dp = v["margin"], v["dep_pct"]          # m flat across the whole forecast
    gs = growth_path(g)
    r_prev, pv = v["rev0"], 0.0
    for t in range(1, C.HORIZON_YEARS + 1):
        r = r_prev * (1 + gs[t - 1])
        f = fcff_flow(r_prev, r, m, dp)
        if audit:
            f_long = fcff_flow_uncancelled(r_prev, r, m, dp, cp=dp)
            assert abs(f - f_long) <= 1e-9 * max(1.0, abs(f)), (t, f, f_long)
        pv += f / (1 + w) ** t
        r_prev = r
    r21 = r_prev * (1 + gs[C.HORIZON_YEARS])
    tv = fcff_flow(r_prev, r21, m, dp) / (w - C.TG)
    return pv + tv / (1 + w) ** C.HORIZON_YEARS


def dcf_inputs(fy, scoring_fy, beta, g_cap=None):
    """Carried v3.10 input construction (run_v311 `dcf_inputs`): trailing-5FY average
    OPM (mean if >=3 points, else latest available, else 0.15), trailing-5FY avg dep/sales."""
    if scoring_fy not in fy:
        return None, "FY column missing"
    yrs = window_years(fy, scoring_fy, C.MARGIN_WINDOW_FY)
    sales = [cell(fy, y, "sales") for y in yrs]
    opm = [cell(fy, y, "opm_pct") for y in yrs]
    dep = [cell(fy, y, "depreciation") for y in yrs]
    rev0 = sales[-1]
    if rev0 is None or rev0 <= 0:
        return None, "non-positive/missing revenue in the scoring FY"
    opm_vals = [x / 100 for x in opm if x is not None]
    latest = opm_vals[-1] if opm_vals else C.OPM_FALLBACK
    m = (sum(opm_vals) / len(opm_vals)) if len(opm_vals) >= 3 else latest
    dep_vals = [d / s for d, s in zip(dep, sales) if d is not None and s]
    dp = (sum(dep_vals) / len(dep_vals)) if dep_vals else C.DEP_FALLBACK
    sg, err = sustainable_growth(fy, scoring_fy, cap=g_cap)
    if sg is None:
        return None, err
    return {"rev0": rev0, "margin": m, "dep_pct": dp, "sg": sg, "fy_used": yrs,
            "w": C.RF + beta * C.ERP, "beta": beta}, None


# ------------------------------------------------------ §2.4 financial variant
def excess_return_value(book0_cr, roe_avg3, w, g, shares_cr):
    """SPEC-SILENT: the w <= TG+0.5pp degenerate guard is stated under §2.1 (FCFF); V_fin does not use TG,
    so the guard is NOT applied here (§2.4 says 'same hurdle/trigger mechanics', not the guard).
    V_fin(g) = [Book_0 + sum_{t=1..20} (ROE_t - w) Book_{t-1}/(1+w)^t
                   + Book_20/(1+w)^20] / shares;
    ROE_t = ROE_avg3 + (w - ROE_avg3) t/20; Book_t = Book_{t-1}(1+g)."""
    book_prev, pv = book0_cr, book0_cr
    for t in range(1, C.HORIZON_YEARS + 1):
        roe_t = roe_avg3 + (w - roe_avg3) * t / C.HORIZON_YEARS
        pv += (roe_t - w) * book_prev / (1 + w) ** t
        book_prev = book_prev * (1 + g)
    pv += book_prev / (1 + w) ** C.HORIZON_YEARS
    return pv / shares_cr


# --------------------------------------------------- §2.3 reporting-only solver
def solve_implied_growth(V, price, w):
    """g_implied: bisection of V(g) = price on [-0.50, w-0.01]. REPORTING ONLY --
    never consulted by any gate or fill. Bounds are reported, not hidden."""
    lo, hi = C.SOLVER_LO, w - C.SOLVER_HI_BELOW_W
    v_lo, v_hi = V(lo), V(hi)
    if v_lo is None or v_hi is None:
        return {"status": "not_valued", "g_implied": None, "reporting_only": True}
    base = {"reporting_only": True, "lo": lo, "hi": hi, "monotone_on_bounds": v_lo <= v_hi}
    if v_hi < price:
        return {**base, "status": ">w-1pp", "g_implied": None}
    if v_lo > price:
        return {**base, "status": "at_-50%_floor", "g_implied": lo}
    a, b = lo, hi
    for _ in range(C.SOLVER_ITERS):
        mid = (a + b) / 2
        if V(mid) < price:
            a = mid
        else:
            b = mid
    return {**base, "status": "solved", "g_implied": (a + b) / 2}


def fill_plausible(p_d0, p_g1):
    """§8.2 pre-condition 2 (certification helper): P_d0 <= 2.0 x P_G1."""
    return p_g1 is not None and p_g1 > 0 and p_d0 <= C.FILL_PLAUSIBILITY_MULT * p_g1


# ---------------------------------------------------------------- entry point
def value_anchor(fy, scoring_fy, is_financial, beta, mcap_cr, mcap_price, price_d0, g_cap=None):
    """Triggers P_G1 = V(g_h(0.875)), P_G2 = V(g_h(0.70)), fixed at scoring.
    Returns {'valued': False, 'reason': ...} when the structure cannot be evaluated.
    `g_cap` is for the reporting-only cap-sensitivity run; the decisional call never passes it."""
    out = {"valued": False, "reason": None, "class": "financial" if is_financial else "non-financial",
           "p_d0": price_d0}
    if scoring_fy is None:
        out["reason"] = "no FY published >=63d before d0"
        return out
    if not mcap_cr or not mcap_price:
        out["reason"] = "market cap / price unavailable (shares = mcap / price)"
        return out
    if price_d0 is None:
        out["reason"] = "no close at/before d0"
        return out
    # SPEC-SILENT: shares = mcap / price with the pair supplied by the caller. The v3.11 runner's share-count
    # integrity guard (audited capital / face value, >20% off) is a v3.11 addition, not in §2.1/§11 -> not carried.
    shares = mcap_cr / mcap_price
    w = C.RF + beta * C.ERP
    out.update({"w": w, "beta": beta, "shares_cr": shares})
    if is_financial:
        sg, err = sustainable_growth(fy, scoring_fy, cap=g_cap)
        if sg is None:
            out["reason"] = f"FV_NOT_COMPUTABLE: {err}"
            return out
        last = sg["roe_years"][-1]
        if last["fy"] != scoring_fy:
            out["reason"] = "scoring-FY book value unavailable"
            return out
        book0 = last["book"]
        V = lambda g: excess_return_value(book0, sg["roe_avg3"], w, g, shares)
        out.update({"book0_cr": book0, "sg": sg, "model": "inverse excess-return 20y"})
    else:
        v, err = dcf_inputs(fy, scoring_fy, beta, g_cap=g_cap)
        if v is None:
            out["reason"] = f"DCF_NOT_COMPUTABLE: {err}"
            return out
        if w <= C.TG + C.DEGENERATE_MARGIN:
            out["reason"] = "DCF degenerate (w <= TG + 0.5pp)"
            return out
        # netcash = investments - borrowings; missing -> 0 (carried v3.10 `or 0.0`)
        net_cash = (cell(fy, scoring_fy, "investments") or 0.0) - (cell(fy, scoring_fy, "borrowings") or 0.0)

        def V(g):
            ev = enterprise_value(v, w, g)
            return None if ev is None else (ev + net_cash) / shares
        sg = v["sg"]
        out.update({"net_cash_cr": net_cash, "margin": v["margin"], "dep_pct": v["dep_pct"],
                    "rev0": v["rev0"], "sg": sg, "model": "2-stage fade FCFF 20y"})
    g_sus = sg["g_sus"]
    hurdles = {t: hurdle_growth(g_sus, k) for t, k in C.TIERS.items()}
    triggers = {t: V(h) for t, h in hurdles.items()}
    out.update({"valued": True, "g_sus": g_sus, "hurdle_growth": hurdles, "trigger": triggers,
                "v_at_g_sus": V(g_sus),
                "implied": solve_implied_growth(V, price_d0, w)})
    return out
