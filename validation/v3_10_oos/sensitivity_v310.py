#!/usr/bin/env python3
"""NON-DECISIONAL post-hoc sensitivities on the single locked v3.10 run.

Reads oos_results_v310.json (written by run_v310_validation.py) and re-plays
fills under alternative readings. Nothing here feeds the scorecard or changes
any parameter; it exists so the result doc can state how fragile each leg is.
"""
import importlib.util
import json
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("run", f"{HERE}/run_v310_validation.py")
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)

res = json.load(open(f"{HERE}/oos_results_v310.json"))
NAMEDATES = {k: (slug, fy, d0, cat, fin) for k, slug, fy, d0, cat, fin in run.NAME_DATES}


def replay(key, triggers, events_filter=None):
    slug, fy, d0, cat, fin = NAMEDATES[key]
    prices = run.load_prices(slug)
    events = run.load_gev(slug)
    if events_filter:
        events = [e for e in events if events_filter(e)]
    prints = run.annual_prints(run.load_eps_series(slug))
    fills, veto0 = run.simulate_fills(slug, run.D(d0), triggers, prices, events, prints)
    return fills, veto0


out = {}

# S1: Gensol -- rating-downgrade rows (2025-03-03/04) not counted (strict literal s2.1)
strict = lambda e: e[0] not in ("2025-03-03", "2025-03-04")  # noqa: E731
for k in ("gensol_2023-03-31", "gensol_2024-03-31"):
    r = res["results"][k]
    if r.get("triggers"):
        f, v = replay(k, r["triggers"], strict)
        out[f"S1_{k}_ratings_not_counted"] = {"fills": f, "veto_at_scoring": v}

# S2: alternative ROE_avg3 reading (avg PAT / scoring-FY book) -> fills for usable name-dates
S2 = {}
for k, r in res["results"].items():
    if r["shadow"] or r.get("status") != "ok" or r.get("fv_alt_roe_convention") is None or r["fv_alt_roe_convention"] <= 0:
        continue
    fva = r["fv_alt_roe_convention"]
    trg = {t: round(m * fva, 2) for t, m in run.TIERS.items() if t != "qfv" or r["qfv_qualified"]}
    f, v = replay(k, trg)
    S2[k] = {"fv_alt": round(fva, 2), "fills": {t: (x.get("fill_date") or ("VETO" if x.get("blocked_by_gev_at_fill") or x.get("blocked_by_gev_at_scoring") else None)) for t, x in f.items()}}
out["S2_alt_roe_convention"] = S2

# S3: Coforge SEBI settlements (2020-11-12 CFO, 2021-01-29 company) treated as routine
routine = lambda e: e[0] not in ("2020-11-12", "2021-01-29")  # noqa: E731
for k in ("coforge_2019-03-31", "coforge_2021-03-31"):
    r = res["results"][k]
    f, v = replay(k, r["triggers"], routine)
    out[f"S3_{k}_coforge_settlements_routine"] = {"fills": f, "veto_at_scoring": v}

# S4: shadow (usability-excluded) name-dates: what filled, ignoring the gate
out["S4_shadow_fills"] = {k: {t: f.get("fill_date") for t, f in r.get("fills", {}).items()}
                          for k, r in res["results"].items() if r["shadow"]}

# S5: per-category aggregates of the decisional fills; per-name-date weighting
cat = {}
for k, r in res["results"].items():
    if r["shadow"] or "fills" not in r:
        continue
    for t, f in r["fills"].items():
        if f.get("fill_date"):
            cat.setdefault(r["category"], []).append((k, t, f["to_latest"], f["fwd_24m"]))
S5 = {}
for c, rows in cat.items():
    S5[c] = {"n_legs": len(rows), "mean_to_t": sum(x[2] for x in rows) / len(rows),
             "mean_24m": sum(x[3] for x in rows) / len(rows), "min_24m": min(x[3] for x in rows)}
per_nd = {}
for k, t, tt, m in sum(cat.values(), []):
    per_nd.setdefault(k, []).append((tt, m))
nd_to_t = [sum(a for a, _ in v) / len(v) for v in per_nd.values()]
nd_24 = [sum(b for _, b in v) / len(v) for v in per_nd.values()]
S5["per_name_date_weighted"] = {"n_name_dates": len(per_nd), "mean_to_t": sum(nd_to_t) / len(nd_to_t), "mean_24m": sum(nd_24) / len(nd_24)}
out["S5_aggregates"] = S5

json.dump(out, open(f"{HERE}/sensitivity_v310.json", "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
