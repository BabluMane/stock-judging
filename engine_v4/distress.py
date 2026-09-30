"""§3 distress screen: D1 pledge level, D2 first-time pledge, D3 Altman Z'' (non-fin),
D4 Piotroski F (non-fin), D5 crash, D6 CAMEL (fin-variant names only), D7 precedence.

Every rule is evaluated and logged on every name-date (no early return). A rule ends
in TRIP (veto, distress), UNCOMPUTABLE (veto, VETOED-DATA -- a required input is
MISSING, not zero) or PASS / N/A. Missing data never silently passes.
"""
from datetime import timedelta

from . import constants as C
from .pit import cell, last_close_on_or_before

PASS, TRIP, UNCOMPUTABLE, NA = "PASS", "TRIP", "UNCOMPUTABLE", "N/A"
ORDER = ("D1", "D2", "D3", "D6", "D4", "D5")      # D7 evaluation order (D3/D6 are class-exclusive)


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


# ----------------------------------------------------------------------- screen
def evaluate(fy, scoring_fy, sector, prices, pledge, d0, equity_increase_solely_bonus_split=None):
    """Evaluate every applicable rule (D7: all logged), attribute per D7 order.
    Class split: Sector in {Banks, Finance} -> D6 (CAMEL); else D3 + D4. D1, D2, D5 apply to all."""
    fin = is_financial(sector)
    rules = {
        "D1": d1_pledge_level(pledge, d0),
        "D2": d2_first_time_pledge(pledge, d0),
        "D3": _r(NA, reason="financial-variant name") if fin else d3_altman(fy, scoring_fy),
        "D4": _r(NA, reason="financial-variant name") if fin else d4_piotroski(fy, scoring_fy, equity_increase_solely_bonus_split),
        "D5": d5_crash(prices, d0),
        "D6": d6_camel(fy, scoring_fy, sector) if fin else _r(NA, reason="non-financial name"),
    }
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
            "tripped": tripped, "uncomputable": uncomp,
            "raw_pledged_pct": rules["D1"].get("pledged_pct")}
