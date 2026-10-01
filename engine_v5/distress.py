"""§3 distress screen: D1 pledge level, D2 first-time pledge, E1-E5 earnings-quality
(non-financials only), D3 Altman Z'' (non-fin), D4 Piotroski F (non-fin), D5 crash,
D6 CAMEL (fin-variant names only), D7 precedence.

Every rule is evaluated and logged on every name-date (no early return). A rule ends
in TRIP (veto, distress), UNCOMPUTABLE (veto, VETOED-DATA -- a required input is
MISSING, not zero) or PASS / N/A. Missing data never silently passes.
"""
from datetime import timedelta

from . import constants as C
from .pit import cell, last_close_on_or_before

PASS, TRIP, UNCOMPUTABLE, NA = "PASS", "TRIP", "UNCOMPUTABLE", "N/A"
ORDER = ("D1", "D2", "E1", "E2", "E3", "E4", "E5", "D3", "D6", "D4", "D5")   # D7 evaluation order (D3/D6 class-exclusive; E1-E5 N/A for financials)


def is_financial(sector):
    return sector in C.FINANCIAL_SECTORS


def _r(status, **detail):
    return {"status": status, **detail}


# ----------------------------------------------------------------------- D1/D2
def _pledged_of_promoter(q):
    """Frozen normalization: pledged_of_promoter = pledged_of_equity / promoter_holding_pct.
    Returns (value|None, note)."""
    p = q.get("pledged_pct")
    if p is None:
        return None, "pledged % missing"
    if q.get("basis", "promoter") == "equity":
        ph = q.get("promoter_holding_pct")
        if ph is None:
            return None, "equity-basis pledge without promoter_holding_pct"
        if ph == 0:
            return (0.0, "promoter holding 0") if p == 0 else (None, "promoter holding 0 with pledge > 0")
        return p / ph * 100.0, "converted from % of equity"
    return float(p), "% of promoter holding"


def _quarters_upto(pledge, d0):
    return sorted((q for q in pledge if q["quarter_end"] <= d0), key=lambda q: q["quarter_end"])


def d1_pledge_level(pledge, d0):
    """Most recent reported quarter <= d0. Veto if >= 50% of promoter holding."""
    qs = _quarters_upto(pledge or [], d0)
    if not qs:
        return _r(UNCOMPUTABLE, reason="no shareholding-pattern quarter <= d0", pledged_pct=None)
    val, note = _pledged_of_promoter(qs[-1])
    if val is None:
        return _r(UNCOMPUTABLE, reason=note, pledged_pct=None, quarter=qs[-1]["quarter_end"].isoformat())
    return _r(TRIP if val >= C.PLEDGE_VETO_PCT else PASS, pledged_pct=val, note=note,
              quarter=qs[-1]["quarter_end"].isoformat())


def d2_first_time_pledge(pledge, d0):
    """Scoring quarter > 0 AND the 8 reported quarters BEFORE it all exactly 0.0.
    <8 prior quarters: all available must be 0.0 with a minimum of 4; <4 -> N/A (D1 still applies).
    SPEC-SILENT: the 8 quarters are read as the quarters preceding the scoring-quarter print;
    including the scoring quarter itself would make 'all 0.0 AND scoring quarter > 0'
    unsatisfiable."""
    qs = _quarters_upto(pledge or [], d0)
    if not qs:
        return _r(UNCOMPUTABLE, reason="no shareholding-pattern quarter <= d0")
    cur, prior = qs[-1], qs[:-1][-C.D2_LOOKBACK_QUARTERS:]
    cur_v, note = _pledged_of_promoter(cur)
    prior_v = [_pledged_of_promoter(q)[0] for q in prior]
    if cur_v is None or any(v is None for v in prior_v):
        return _r(UNCOMPUTABLE, reason=note if cur_v is None else "a prior quarter's pledge is missing")
    if len(prior) < C.D2_MIN_QUARTERS:
        return _r(NA, reason=f"{len(prior)} prior quarters < {C.D2_MIN_QUARTERS}", n_prior=len(prior))
    zeros = all(v == 0.0 for v in prior_v)
    return _r(TRIP if (zeros and cur_v > 0) else PASS, n_prior=len(prior), prior_all_zero=zeros,
              scoring_quarter_pledged_pct=cur_v)


# --------------------------------------------------------------------------- D3
def d3_altman(fy, scoring_fy):
    """Z'' = 6.56 X1 + 3.26 X2 + 6.72 X3 + 1.05 X4 (no +3.25). Veto if Z'' < 1.1.
    X1 = (CA - CL)/TA; X2 = Reserves/TA (less revaluation reserve only if separately
    disclosed); X3 = EBIT/TA with EBIT = PBT + Interest + Depreciation (AS WRITTEN in §3);
    X4 = Book Equity / Total Liabilities, BE = Capital + Reserves, TL = TA - BE.
    BE <= 0 -> automatic veto. Any missing component -> UNCOMPUTABLE."""
    if scoring_fy is None:
        return _r(UNCOMPUTABLE, reason="no scoring FY")
    g = lambda f: cell(fy, scoring_fy, f)
    ec, res = g("equity_capital"), g("reserves")
    if ec is not None and res is not None and (ec + res) <= 0:
        return _r(TRIP, reason="book equity <= 0 (automatic distress veto)", book_equity=ec + res)
    need = {"total_assets": g("total_assets"), "current_assets": g("current_assets"),
            "current_liabilities": g("current_liabilities"), "reserves": res, "pbt": g("pbt"),
            "interest": g("interest"), "depreciation": g("depreciation"), "equity_capital": ec}
    missing = sorted(k for k, v in need.items() if v is None)
    if missing:
        return _r(UNCOMPUTABLE, reason=f"missing fields: {missing}")
    ta = need["total_assets"]
    be = ec + res
    tl = ta - be
    if ta <= 0 or tl <= 0:
        return _r(UNCOMPUTABLE, reason=f"total assets {ta} / total liabilities {tl} not positive")
    reval = g("revaluation_reserve")          # None = not separately disclosed -> no subtraction
    x1 = (need["current_assets"] - need["current_liabilities"]) / ta
    x2 = (res - (reval or 0.0)) / ta
    x3 = (need["pbt"] + need["interest"] + need["depreciation"]) / ta
    x4 = be / tl
    a, b, c, d = C.Z_COEF
    z = a * x1 + b * x2 + c * x3 + d * x4
    return _r(TRIP if z < C.Z_VETO_BELOW else PASS, z=z, x=(x1, x2, x3, x4),
              zone="distress" if z < C.Z_VETO_BELOW else ("grey" if z <= C.Z_GREY_TOP else "safe"))


# --------------------------------------------------------------------------- D4
def d4_piotroski(fy, scoring_fy, equity_increase_solely_bonus_split=None):
    """9 criteria, scoring FY t vs prior t-1 (t-2 only for beginning-TA of t-1). Veto if F <= 2.
    Fallbacks (spec): F_dLIQUID with no CA/CL split -> 0 logged; F_dMARGIN with neither
    material cost nor raw-material % -> 0 logged; any delta-term with a missing prior FY -> 0 logged.
    Missing DIRECT field (scoring-FY net profit / CFO; beginning total assets; equity capital)
    -> UNCOMPUTABLE (§3 general rule; SPEC-SILENT for F_ROA's beginning-TA and F_EQ's prior capital)."""
    if scoring_fy is None:
        return _r(UNCOMPUTABLE, reason="no scoring FY")
    t, p, pp = scoring_fy, scoring_fy - 1, scoring_fy - 2
    g = lambda y, f: cell(fy, y, f)
    np_t, cfo_t = g(t, "net_profit"), g(t, "cfo")
    ta_t, ta_p, ta_pp = g(t, "total_assets"), g(p, "total_assets"), g(pp, "total_assets")
    ec_t, ec_p = g(t, "equity_capital"), g(p, "equity_capital")
    direct = {"net_profit[t]": np_t, "cfo[t]": cfo_t, "total_assets[t-1]": ta_p, "equity_capital[t]": ec_t,
              "equity_capital[t-1]": ec_p}
    missing = sorted(k for k, v in direct.items() if v is None)
    if missing:
        return _r(UNCOMPUTABLE, reason=f"missing direct fields: {missing}")
    if ta_p <= 0:
        return _r(UNCOMPUTABLE, reason=f"beginning total assets {ta_p} not positive")
    if ec_t > ec_p and equity_increase_solely_bonus_split is None:
        return _r(UNCOMPUTABLE, reason="equity capital increased; bonus/split provenance (corporate actions) missing")
    logged, comp = [], {}

    def delta(name, fn):
        try:
            val = fn()
        except (TypeError, ZeroDivisionError):
            val = None
        if val is None:
            logged.append(f"{name}: missing prior-FY input -> 0 (fail-closed)")
            comp[name] = 0
        else:
            comp[name] = int(val)

    comp["F_ROA"] = int(np_t / ta_p > 0)
    comp["F_CFO"] = int(cfo_t > 0)
    delta("F_dROA", lambda: (np_t / ta_p) > (g(p, "net_profit") / ta_pp))
    comp["F_ACCRUAL"] = int(cfo_t > np_t)
    avg = lambda a, b: (a + b) / 2
    delta("F_dLEVER", lambda: (g(t, "borrowings") / avg(ta_t, ta_p)) < (g(p, "borrowings") / avg(ta_p, ta_pp)))

    def liquid():
        cr_t = g(t, "current_assets") / g(t, "current_liabilities")
        cr_p = g(p, "current_assets") / g(p, "current_liabilities")
        return cr_t > cr_p
    delta("F_dLIQUID", liquid)          # AR-derived CA/CL; not retrievable -> 0 (logged)
    comp["F_EQ"] = 0 if (ec_t > ec_p and not equity_increase_solely_bonus_split) else 1

    def gross_margin(y):
        s = g(y, "sales")
        mc = g(y, "material_cost")
        if mc is None:
            rm = g(y, "raw_material_pct")
            mc = None if rm is None or s is None else rm / 100 * s
        return (s - mc) / s
    delta("F_dMARGIN", lambda: gross_margin(t) > gross_margin(p))
    delta("F_dTURN", lambda: (g(t, "sales") / avg(ta_t, ta_p)) > (g(p, "sales") / avg(ta_p, ta_pp)))
    f = sum(comp.values())
    return _r(TRIP if f <= C.PIOTROSKI_VETO_AT_OR_BELOW else PASS, f=f, components=comp, fail_closed_log=logged)


# --------------------------------------------------------------------------- D5
def d5_crash(prices, d0):
    """H52 = trailing-52-week high of adjusted closes, P0 = d0 close; veto if (H52-P0)/H52 >= 60%.
    <52 weeks of history -> use what exists; <26 weeks -> UNCOMPUTABLE."""
    hist = [(d, p) for d, p in prices if d <= d0]
    if not hist:
        return _r(UNCOMPUTABLE, reason="no closes <= d0")
    weeks = (d0 - hist[0][0]).days / 7
    if weeks < C.CRASH_MIN_WEEKS:
        return _r(UNCOMPUTABLE, reason=f"{weeks:.1f} weeks of history < {C.CRASH_MIN_WEEKS}")
    start = d0 - timedelta(weeks=C.CRASH_FULL_WINDOW_WEEKS)
    h52 = max(p for d, p in hist if d >= start)
    p0 = hist[-1][1]
    dd = (h52 - p0) / h52
    return _r(TRIP if dd >= C.CRASH_VETO_DRAWDOWN else PASS, h52=h52, p0=p0, drawdown=dd, weeks_of_history=weeks)


# --------------------------------------------------------------------------- D6
def _band(metric_value, spec):
    if spec["higher_better"]:
        return 2 if metric_value >= spec["two"] else (1 if metric_value >= spec["one"] else 0)
    return 2 if metric_value <= spec["two"] else (1 if metric_value <= spec["one"] else 0)


def d6_camel(fy, scoring_fy, sector):
    """Five 0-2 components (C, A, M, E, L), total 0-10; veto if total <= 4.
    Hard floors override: GNPA > 12% or CAR < 9% -> veto. L: Banks -> CASA, Finance -> leverage.
    A missing component field -> UNCOMPUTABLE (floors are still evaluated on what exists)."""
    if scoring_fy is None:
        return _r(UNCOMPUTABLE, reason="no scoring FY")
    L = "L_banks" if sector == "Banks" else "L_nbfc"
    keys = {"C": "C", "A": "A", "M": "M", "E": "E", "L": L}
    vals = {k: cell(fy, scoring_fy, C.CAMEL_BANDS[b]["metric"]) for k, b in keys.items()}
    floors = []
    car, gnpa = vals["C"], vals["A"]
    if gnpa is not None and gnpa > C.CAMEL_GNPA_HARD_FLOOR:
        floors.append(f"GNPA {gnpa} > {C.CAMEL_GNPA_HARD_FLOOR}")
    if car is not None and car < C.CAMEL_CAR_HARD_FLOOR:
        floors.append(f"CAR {car} < {C.CAMEL_CAR_HARD_FLOOR}")
    missing = sorted(C.CAMEL_BANDS[keys[k]]["metric"] for k, v in vals.items() if v is None)
    scores = {k: _band(v, C.CAMEL_BANDS[keys[k]]) for k, v in vals.items() if v is not None}
    total = sum(scores.values()) if not missing else None
    detail = {"scores": scores, "total": total, "hard_floors_tripped": floors, "values": vals}
    if floors:
        return _r(TRIP, reason="; ".join(floors), missing=missing, **detail)
    if missing:
        return _r(UNCOMPUTABLE, reason=f"missing fields: {missing}", **detail)
    return _r(TRIP if total <= C.CAMEL_VETO_AT_OR_BELOW else PASS, **detail)


# ---------------------------------------------------------------------- E-rules
# §3.1 earnings-quality vetoes (the v5 mechanism; non-financials only -- the caller
# gates them out for financial-variant names). Each is an independent hard veto.


def e1_sloan(fy, scoring_fy):
    """(NI_t - CFO_t) / TA_t > 0.10 -> veto. Positive direction ONLY: CFO_t > NI_t
    (conservatism) never trips -- the strict > 0.10 encodes this. Scoring FY only
    (G1: 1-yr spike, not the 2-yr literature variant). TA_t <= 0 or any missing
    field -> UNCOMPUTABLE."""
    if scoring_fy is None:
        return _r(UNCOMPUTABLE, reason="no scoring FY")
    g = lambda f: cell(fy, scoring_fy, f)
    ni, cfo, ta = g("net_profit"), g("cfo"), g("total_assets")
    missing = sorted(k for k, v in (("net_profit", ni), ("cfo", cfo), ("total_assets", ta)) if v is None)
    if missing:
        return _r(UNCOMPUTABLE, reason=f"missing fields: {missing}")
    if ta <= 0:
        return _r(UNCOMPUTABLE, reason=f"total assets {ta} not positive")
    sloan = (ni - cfo) / ta
    return _r(TRIP if sloan > C.SLOAN_E1_THRESHOLD else PASS, sloan=sloan,
              threshold=C.SLOAN_E1_THRESHOLD, positive_only=C.E1_POSITIVE_ONLY)


def e2_cash_conversion(fy, scoring_fy):
    """CFO_t < 0.5 x NI_t AND CFO_{t-1} < 0.5 x NI_{t-1} -> veto (2 consecutive FYs,
    applied literally -- no sign special-casing per G1). Missing any of the four
    fields -> UNCOMPUTABLE."""
    if scoring_fy is None:
        return _r(UNCOMPUTABLE, reason="no scoring FY")
    t, p = scoring_fy, scoring_fy - 1
    need = {f"{fld}[{y}]": cell(fy, y, fld) for y in (t, p) for fld in ("cfo", "net_profit")}
    missing = sorted(k for k, v in need.items() if v is None)
    if missing:
        return _r(UNCOMPUTABLE, reason=f"missing fields: {missing}")
    per_year = {y: need[f"cfo[{y}]"] < C.E2_CFO_PCT * need[f"net_profit[{y}]"] for y in (t, p)}
    return _r(TRIP if all(per_year.values()) else PASS, cfo_below_half_ni=per_year,
              persistence_fy=C.E2_PERSISTENCE_FY)


def e3_interest_coverage(fy, scoring_fy):
    """EBIT_t / Interest_t < 1.5 -> veto, with EBIT = PBT + Interest (G1 literal) --
    deliberately distinct from D3's frozen PBT+Interest+Depreciation (EBITDA-like, §3);
    §11 carries both definitions. Interest_t <= 0 -> no trip (infinite coverage, logged).
    Signed PBT used as-is. Missing field -> UNCOMPUTABLE."""
    if scoring_fy is None:
        return _r(UNCOMPUTABLE, reason="no scoring FY")
    g = lambda f: cell(fy, scoring_fy, f)
    pbt, interest = g("pbt"), g("interest")
    missing = sorted(k for k, v in (("pbt", pbt), ("interest", interest)) if v is None)
    if missing:
        return _r(UNCOMPUTABLE, reason=f"missing fields: {missing}")
    if interest <= 0:
        return _r(PASS, reason=f"interest {interest} <= 0: coverage infinite -> no trip",
                  interest_coverage=None)
    ic = (pbt + interest) / interest
    return _r(TRIP if ic < C.E3_IC_VETO_BELOW else PASS, interest_coverage=ic,
              threshold=C.E3_IC_VETO_BELOW)


def e4_etr(fy, scoring_fy):
    """TaxExpense_t / PBT_t < 15% in BOTH of (t-1, t) -> veto. TaxExpense comes from
    the tax-expense line ONLY -- never the 1-NI/PBT construction (PBM FY18 prints -33%
    on NI > PBT; the trap is documented). Either year's PBT <= 0 -> the rule does not
    trip for that pair (PASS, logged). Missing tax_expense or PBT -> UNCOMPUTABLE."""
    if scoring_fy is None:
        return _r(UNCOMPUTABLE, reason="no scoring FY")
    t, p = scoring_fy, scoring_fy - 1
    need = {f"{fld}[{y}]": cell(fy, y, fld) for y in (t, p) for fld in ("tax_expense", "pbt")}
    missing = sorted(k for k, v in need.items() if v is None)
    if missing:
        return _r(UNCOMPUTABLE, reason=f"missing fields: {missing}")
    if need[f"pbt[{t}]"] <= 0 or need[f"pbt[{p}]"] <= 0:
        return _r(PASS, reason=f"PBT <= 0 in the pair ({need[f'pbt[{t}]']}, {need[f'pbt[{p}]']}): "
                               "ratio meaningless -> no trip for this pair", etr=None,
                  persistence_fy=C.E4_PERSISTENCE_FY)
    etr = {y: need[f"tax_expense[{y}]"] / need[f"pbt[{y}]"] for y in (t, p)}
    tripped = all(v < C.E4_ETR_VETO_BELOW for v in etr.values())
    return _r(TRIP if tripped else PASS, etr=etr, threshold=C.E4_ETR_VETO_BELOW,
              persistence_fy=C.E4_PERSISTENCE_FY)


def e5_receivables_days(fy, scoring_fy):
    """(Receivables_t / Sales_t) x 365 > 90 days OR Receivables_t / Receivables_{t-1} > 1.30
    (> 30% YoY) -> veto (non-financials only). Receivables are AR-sourced (D4 F_dLIQUID
    precedent, same >=63d PIT vintage); missing any required field -> UNCOMPUTABLE.
    Sales_t <= 0 -> UNCOMPUTABLE; Receivables_{t-1} <= 0 -> UNCOMPUTABLE (no meaningful
    YoY multiple -- fail-closed)."""
    if scoring_fy is None:
        return _r(UNCOMPUTABLE, reason="no scoring FY")
    t, p = scoring_fy, scoring_fy - 1
    rec_t, sales_t, rec_p = cell(fy, t, "receivables"), cell(fy, t, "sales"), cell(fy, p, "receivables")
    missing = sorted(k for k, v in (("receivables[t]", rec_t), ("sales[t]", sales_t),
                                    ("receivables[t-1]", rec_p)) if v is None)
    if missing:
        return _r(UNCOMPUTABLE, reason=f"missing fields: {missing}")
    if sales_t <= 0:
        return _r(UNCOMPUTABLE, reason=f"sales[t] {sales_t} not positive")
    if rec_p <= 0:
        return _r(UNCOMPUTABLE, reason=f"receivables[t-1] {rec_p} not positive (no YoY multiple)")
    days = rec_t / sales_t * 365
    yoy = rec_t / rec_p
    return _r(TRIP if (days > C.E5_DAYS_VETO_ABOVE or yoy > C.E5_YOY_VETO_ABOVE) else PASS,
              days=days, yoy=yoy, thresholds=(C.E5_DAYS_VETO_ABOVE, C.E5_YOY_VETO_ABOVE))


# ------------------------------------------------------- reporting-only (§3.1)
def reporting_fields(fy, scoring_fy):
    """§3.1 reporting-only fields (NOT vetoes): Beneish SGI/DEPI/LVGI/TATA (frozen
    formulas) + rpt_loans passthrough. Any input missing -> that field is null and
    logged. Never affects a veto."""
    if scoring_fy is None:
        return {"fields": {}, "log": ["no scoring FY"]}
    t, p = scoring_fy, scoring_fy - 1
    g = lambda y, f: cell(fy, y, f)
    log, out = [], {}
    s_t, s_p = g(t, "sales"), g(p, "sales")
    out["SGI"] = (s_t / s_p) if (s_t is not None and s_p not in (None, 0)) else None
    d_t, d_p = g(t, "depreciation"), g(p, "depreciation")
    ppe_t, ppe_p = g(t, "ppe_net"), g(p, "ppe_net")
    def depi_ratio(dep, ppe):
        return None if (dep is None or ppe is None or ppe + dep == 0) else dep / (ppe + dep)
    rt, rp = depi_ratio(d_t, ppe_t), depi_ratio(d_p, ppe_p)
    out["DEPI"] = (rp / rt) if (rt not in (None, 0) and rp is not None) else None
    def lev(y):
        cl, b, ta = g(y, "current_liabilities"), g(y, "borrowings"), g(y, "total_assets")
        return None if (cl is None or b is None or ta in (None, 0)) else (cl + b) / ta
    lt, lp = lev(t), lev(p)
    out["LVGI"] = (lt / lp) if (lp not in (None, 0) and lt is not None) else None
    ni, cfo, ta = g(t, "net_profit"), g(t, "cfo"), g(t, "total_assets")
    out["TATA"] = ((ni - cfo) / ta) if (ni is not None and cfo is not None and ta not in (None, 0)) else None
    out["rpt_loans"] = g(t, "rpt_loans")          # AR-notes passthrough; None = not disclosed
    for k, v in out.items():
        if v is None:
            log.append(f"{k}: uncomputable (missing input) -> stored null (reporting-only)")
    return {"fields": out, "log": log}


# ----------------------------------------------------------------------- screen
def evaluate(fy, scoring_fy, sector, prices, pledge, d0, equity_increase_solely_bonus_split=None):
    """Evaluate every applicable rule (D7: all logged), attribute per D7 order.
    Class split: Sector in {Banks, Finance} -> D6 (CAMEL); else D3 + D4 + E1-E5.
    E1-E5 are N/A by construction for financial-variant names. D1, D2, D5 apply to all."""
    fin = is_financial(sector)
    e_na = {e: _r(NA, reason="financial-variant name (E-rules N/A by construction)") for e in
            ("E1", "E2", "E3", "E4", "E5")}
    e_rules = {e: fn(fy, scoring_fy) for e, fn in
               (("E1", e1_sloan), ("E2", e2_cash_conversion), ("E3", e3_interest_coverage),
                ("E4", e4_etr), ("E5", e5_receivables_days))} if not fin else e_na
    rules = {
        "D1": d1_pledge_level(pledge, d0),
        "D2": d2_first_time_pledge(pledge, d0),
        **e_rules,
        "D3": _r(NA, reason="financial-variant name") if fin else d3_altman(fy, scoring_fy),
        "D4": _r(NA, reason="financial-variant name") if fin else d4_piotroski(fy, scoring_fy, equity_increase_solely_bonus_split),
        "D5": d5_crash(prices, d0),
        "D6": d6_camel(fy, scoring_fy, sector) if fin else _r(NA, reason="non-financial name"),
    }
    rep = reporting_fields(fy, scoring_fy)
    tripped = [r for r in ORDER if rules[r]["status"] == TRIP]
    uncomp = [r for r in ORDER if rules[r]["status"] == UNCOMPUTABLE]
    # SPEC-SILENT: if a rule trips AND another is uncomputable, the tripped rule owns the
    # attribution (D7: "first tripped rule owns"); the data defect is still logged.
    if tripped:
        label = f"VETOED-DISTRESS:{tripped[0]}"
    elif uncomp:
        label = "VETOED-DATA"
    else:
        label = "PASS"
    return {"verdict": "PASS" if label == "PASS" else "STOP", "label": label,
            "class": "financial" if fin else "non-financial", "rules": rules,
            "e_rules": "N/A (financial variant)" if fin else "evaluated",
            "reporting": rep["fields"], "reporting_log": rep["log"],
            "tripped": tripped, "uncomputable": uncomp,
            "raw_pledged_pct": rules["D1"].get("pledged_pct")}
