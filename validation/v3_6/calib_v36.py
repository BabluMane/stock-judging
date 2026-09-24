#!/usr/bin/env python3
"""
v3.6 WIDENED VALIDATION. Engine v3.5 unchanged. Everything scored here was fixed in preregistration_v3_6.md
before these series were retrieved.

What is different from calib_v35.py:
  * USABILITY FILTER (pre-reg 1): a name-date is scored only if its weekly series passes the EPS-basis and
    step checks. usability_v36.json is read, never recomputed here.
  * VINTAGE PAIRING (pre-reg 7): at each simulated week the anchor, the DCF triggers, Q and the gates come from
    the LATEST stored input whose scoring date is <= that week. No lookahead: an input dated T-3 is only used
    from T-3 onward. This removes most of the v3.5 staleness (a 2016 bear case judged against a 2017 anchor).
    Where no nearer vintage exists the mismatch is reported as anchor_drift = refreshed FV / vintage FV.
  * GATE M (pre-reg 4) and GUARDRAIL V (pre-reg 5) are evaluated at every candidate fill and recorded, so
    results can be reported with and without them. They do not alter the engine.
  * Outcomes at BOTH horizons: 24 months from the fill, and from the fill to T.
"""
import copy, csv, json, math, os, statistics as st, sys
from datetime import date, timedelta
import engine_v3 as E

D = lambda s: date.fromisoformat(s[:10])
LAG = timedelta(days=63)
FIVE = timedelta(days=int(5 * 365.25))
WEEKS24 = timedelta(days=int(2 * 365.25))
BEAR_PCTILE = E.BEAR_FLOOR_PCTILE

# ---- pre-registered constants (preregistration_v3_6.md 4 and 5). Do not tune. ----
M1_FRACTION = 0.875      # = the standard's ACCUMULATE discount
M1_WINDOW_MONTHS = 36
M1_MIN_OBS = 60
M2_MULT_FALL = -0.10     # = the standard's FAIR band
M2_EPS_FLOOR = 0.0


def load_series(slug):
    rows = []
    for r in csv.DictReader(open(f"pe_series/{slug}.csv", newline="", encoding="utf-8-sig")):
        p = float(r["price"]) if r["price"] else None
        pe = float(r["pe"]) if r["pe"] else None
        rows.append((D(r["date"]), p, pe))
    rows.sort()
    out = [{"date": d, "price": p, "pe": pe, "eps_imp": (p / pe) if (p and pe) else None} for d, p, pe in rows]
    for r in out:
        cut = r["date"] - LAG
        prior = [x for x in out if x["date"] <= cut]
        e = prior[-1]["eps_imp"] if prior else None
        r["eps_pit"] = e
        r["pe_pit"] = (r["price"] / e) if (e and e > 0 and r["price"]) else None
    return out


def at(series, d):
    prior = [x for x in series if x["date"] <= d]
    return prior[-1] if prior else None


def _pct(vals, q):
    v = sorted(vals); n = len(v)
    if n == 1:
        return v[0]
    i = (n - 1) * q / 100.0
    lo, hi = int(i), min(int(i) + 1, n - 1)
    return v[lo] + (v[hi] - v[lo]) * (i - lo)


def median_5y(series, d):
    """Raw median PIT TTM P/E over the 5 years before d, plus the 5th percentile that floors the bear multiple."""
    w = [x for x in series if d - FIVE < x["date"] <= d and x["pe_pit"] is not None]
    if not w:
        return None, 0.0, None, 0
    vals = [x["pe_pit"] for x in w]
    return st.median(vals), round((d - w[0]["date"]).days / 365.25, 2), _pct(vals, BEAR_PCTILE), len(vals)


# ══════════════════════════════════════════════════════════════════════════
# Gate M and Guardrail V — pre-registered, evaluated but never fed back into the engine
# ══════════════════════════════════════════════════════════════════════════

def eps_trend(series, t):
    """Value at t of an OLS line through log(EPS_pit) over the prior M1_WINDOW_MONTHS."""
    cut = t - timedelta(days=int(30.44 * M1_WINDOW_MONTHS))
    w = [(x["date"], x["eps_pit"]) for x in series if cut <= x["date"] <= t and x["eps_pit"] and x["eps_pit"] > 0]
    if len(w) < M1_MIN_OBS:
        return None
    xs = [(d - cut).days / 365.25 for d, _ in w]
    ys = [math.log(e) for _, e in w]
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    den = sum((x - mx) ** 2 for x in xs)
    if den <= 0:
        return None
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den
    return math.exp((my - b * mx) + b * ((t - cut).days / 365.25))


def gate_M(series, t):
    """Returns (m1_pass, m2_pass, detail). Missing inputs -> None (recorded as 'not evaluable', never a pass)."""
    now = at(series, t)
    w12 = [x for x in series if t - timedelta(days=365) <= x["date"] <= t and x["eps_pit"]]
    tr = eps_trend(series, t)
    det = {"eps": now["eps_pit"] if now else None, "trend": tr}
    if not (now and now.get("eps_pit") and now["eps_pit"] > 0 and tr and w12):
        return None, None, det
    old = w12[0]
    det["eps_over_trend"] = round(now["eps_pit"] / tr, 3)
    det["d_eps_12m"] = round(now["eps_pit"] / old["eps_pit"] - 1, 3)
    det["d_mult_12m"] = round((now["price"] / now["eps_pit"]) / (old["price"] / old["eps_pit"]) - 1, 3)
    m1 = det["eps_over_trend"] >= M1_FRACTION
    m2 = det["d_mult_12m"] <= M2_MULT_FALL and det["d_eps_12m"] >= M2_EPS_FLOOR
    return m1, m2, det


# ══════════════════════════════════════════════════════════════════════════

def prep(inp, ser, d0):
    """Write the point-in-time anchor inputs for scoring date d0 into a copy of inp."""
    row0 = at(ser, d0)
    if not row0 or not row0.get("eps_pit"):
        return None, None
    basis = inp["price"] / row0["price"]
    med, win, p5, nobs = median_5y(ser, d0)
    d = copy.deepcopy(inp)
    d["valuation"]["pe_median_5y"] = None if med is None else round(med, 2)
    d["valuation"]["pe_median_window_years"] = win
    d["valuation"]["pe_p5_5y"] = None if p5 is None else round(p5, 2)
    d["valuation"]["eps_ttm_pit"] = round(row0["eps_pit"] * basis, 4)
    d["valuation"]["pe_median_basis"] = f"raw median of {nobs} weekly PIT observations"
    return d, basis


def cov_neutral(r):
    pb = r["P_floor_basis"]
    return E.tier_rule(r["Q"], r["gates_failed"], r["gates_unverified"], False, r["entry"],
                       pb["P_fill_accumulate"], pb["P_fill_invest"], r["missing_tests"])


def neutralise(d):
    n = copy.deepcopy(d); ms = n.setdefault("manual_scores", {})
    for k in ["A4", "C2", "C3", "C4", "F1", "F2", "F3", "F4", "F5"] + (["C5"] if "C5" in ms else []):
        if k == "F5" and n.get("f5_skipped"):
            continue
        ms[k] = 1
    return n


def run_one(key, vintages, neutral=False):
    """vintages: [(scoring_date, input_dict)] for this slug, ascending. The name-date `key` opens the window."""
    slug, ds = key.split("_")[0], key.split("_")[1]
    ser = load_series(slug)
    d0 = D(ds)
    base_inp = dict(vintages)[ds]
    if neutral:
        vintages = [(k, neutralise(v)) for k, v in vintages]
        base_inp = dict(vintages)[ds]
    T = D((base_inp.get("_calibration") or {}).get("T", "")[:10]) if (base_inp.get("_calibration") or {}).get("T") else None
    d_scored, basis = prep({k: v for k, v in base_inp.items() if k != "_calibration"}, ser, d0)
    if d_scored is None:
        return {"key": key, "scorable": False, "reason": "no point-in-time EPS at the scoring date"}
    r0 = E.run(copy.deepcopy(d_scored))
    res = {"key": key, "scorable": True, "Q": r0["Q"], "tier_cov_neutral": cov_neutral(r0),
           "zone": r0["entry"]["zone"], "anchor_used": r0["entry"].get("anchor_used"),
           "mult": {k: (r0["entry"].get("multiple_anchor") or {}).get(k) for k in
                    ("usable", "reason", "fair_price", "pe_ttm", "pe_median_5y", "window_years",
                     "discount_to_fair_pct", "zone", "accumulate_trigger", "invest_trigger")},
           "dcf": {k: (r0["entry"].get("dcf_anchor") or {}).get(k) for k in
                   ("fair_value", "zone", "discount_to_fv_pct", "accumulate_trigger", "invest_trigger")},
           "P_fill": r0["P_floor_basis"], "bear_floor_note": r0.get("bear_floor_note"),
           "e1_benchmark": r0.get("e1_benchmark"), "implied_irr": r0["entry"].get("implied_irr_pct"),
           "basis": round(basis, 6), "T": T.isoformat() if T else None}

    # scoring-date triggers, for Guardrail V
    v_acc = res["mult"]["accumulate_trigger"] if res["mult"]["usable"] else None
    v_inv = res["mult"]["invest_trigger"] if res["mult"]["usable"] else None

    fills = {"accumulate": None, "invest": None}
    blocked = {"accumulate": 0, "invest": 0}
    weeks = [x for x in ser if d0 < x["date"] <= d0 + WEEKS24 and x["price"]]
    cache = {}
    qkey = None
    for x in weeks:
        # ---- vintage pairing: latest input whose scoring date <= this week (no lookahead)
        vin = [k for k, _ in vintages if D(k) <= x["date"]]
        vds = vin[-1] if vin else ds
        k = ((x["date"] - d0).days // 91, vds)
        if qkey != k:
            qkey = k
            qd = d0 + timedelta(days=91 * k[0])
            vinp = {kk: vv for kk, vv in dict(vintages)[vds].items() if kk != "_calibration"}
            d_v, basis_v = prep(vinp, ser, qd)
            state = None
            if d_v is not None:
                rv = E.run(copy.deepcopy(d_v))
                ma = rv["entry"].get("multiple_anchor") or {}
                da = rv["entry"].get("dcf_anchor") or {}
                elig = rv["armed"]["eligible"] or (rv["Q"] is not None and rv["Q"] >= 6.0
                        and not rv["gates_failed"] and not rv["gates_unverified"] and not rv["missing_tests"])
                state = {"inp": d_v, "basis": basis_v, "elig": elig, "vds": vds,
                         "acc": rv["entry"]["accumulate_trigger"] if rv["entry"]["usable"] else None,
                         "inv": rv["entry"]["invest_trigger"] if rv["entry"]["usable"] else None,
                         "mult_ok": ma.get("usable"), "mult_fv": ma.get("fair_price"),
                         "mult_acc": ma.get("accumulate_trigger"), "mult_inv": ma.get("invest_trigger"),
                         "dcf_acc": da.get("accumulate_trigger"), "dcf_inv": da.get("invest_trigger")}
            cache[k] = state
        s = cache[k]
        if not s or not s["elig"]:
            continue
        px_in = x["price"] * s["basis"]
        for leg, trg, v_trg in (("accumulate", s["acc"], v_acc), ("invest", s["inv"], v_inv)):
            if fills[leg] or not trg or px_in > trg:
                continue
            src = "multiple" if (s["mult_ok"] and (s["mult_acc"] if leg == "accumulate" else s["mult_inv"])
                                 and abs((s["mult_acc"] if leg == "accumulate" else s["mult_inv"]) - trg) < 1e-6) else "dcf"
            rr = E.run({**copy.deepcopy(s["inp"]), "price": px_in})
            if rr["P_today"] is None or rr["P_today"] < E.P_FLOOR:
                blocked[leg] += 1
                continue
            m1, m2, det = gate_M(ser, x["date"])
            fwd = [y for y in ser if x["date"] < y["date"] <= x["date"] + WEEKS24 and y["price"]]
            pT = at(ser, T) if T else None
            fills[leg] = {"date": x["date"].isoformat(), "price_input": round(px_in, 2),
                          "trigger_input": round(trg, 2), "anchor": src, "P_at_fill": rr["P_today"],
                          "vintage": s["vds"],
                          "anchor_drift": (round(s["mult_fv"] / res["mult"]["fair_price"], 3)
                                           if (s.get("mult_fv") and res["mult"]["fair_price"]) else None),
                          "gate_M1": m1, "gate_M2": m2, "gate_M": (bool(m1 and m2) if m1 is not None else None),
                          "gate_M_detail": det,
                          "guardrail_V": (bool(v_trg and px_in <= v_trg) if v_trg else False),
                          "fwd_24m": round(fwd[-1]["price"] / x["price"], 3) if fwd else None,
                          "fwd_months": round((fwd[-1]["date"] - x["date"]).days / 30.44, 1) if fwd else None,
                          "fwd_truncated": bool(fwd and fwd[-1]["date"] < x["date"] + WEEKS24 - timedelta(days=20)),
                          "to_T": round(pT["price"] / x["price"], 3) if pT and pT["date"] >= x["date"] else None,
                          "to_T_truncated": bool(T and pT and pT["date"] < T - timedelta(days=20))}
    res["fills_24m"] = fills
    res["weeks_blocked_by_P_floor"] = blocked
    return res


if __name__ == "__main__":
    use = json.load(open("usability_v36.json"))
    by_slug = {}
    for f in sorted(os.listdir("inputs")):
        k = f[:-5]; s, ds = k.split("_")
        by_slug.setdefault(s, []).append((ds, json.load(open(f"inputs/{f}"))))
    for s in by_slug:
        by_slug[s].sort()
    out = {}
    keys = sys.argv[1:] or [f"{s}_{ds}" for s in by_slug for ds, _ in by_slug[s]]
    for key in sorted(keys):
        s = key.split("_")[0]
        if not os.path.exists(f"pe_series/{s}.csv"):
            out[key] = {"excluded": "no weekly series retrieved"}; continue
        if not use.get(key, [False])[0]:
            out[key] = {"excluded": f"series not usable: {use.get(key,['','unknown'])[1]}"}; continue
        try:
            out[key] = {"as_judged": run_one(key, by_slug[s]),
                        "neutral": run_one(key, by_slug[s], neutral=True)}
        except Exception as ex:
            out[key] = {"error": f"{type(ex).__name__}: {ex}"}
        print(key, "done", flush=True)
    json.dump(out, open("outputs_v36.json", "w"), indent=1, default=str, ensure_ascii=False)
    print("\nwrote outputs_v36.json:", len(out), "name-dates")
