#!/usr/bin/env python3
"""NON-DECISIONAL post-hoc sensitivities on the single locked v3.11 run.

Reads oos_results_v311.json (written by run_v311_validation.py) and re-plays
fills under alternative readings. Nothing here feeds the scorecard or changes any
parameter; it exists so the result doc can state how fragile each leg is. It
never re-runs the locked run and never edits a log.
"""
import importlib.util
import json
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("run", f"{HERE}/run_v311_validation.py")
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)

res = json.load(open(f"{HERE}/oos_results_v311.json"))
NAMEDATES = {k: (slug, fy, d0, cat, fin) for k, slug, fy, d0, cat, fin in run.NAME_DATES}
DEC = lambda k: not res["results"][k]["shadow"]  # noqa: E731


def replay(key, triggers, events_filter=None, events_override=None):
    slug, fy, d0, cat, fin = NAMEDATES[key]
    prices = run.load_prices(slug)
    events = run.load_gev(slug) if events_override is None else events_override
    if events_filter:
        events = [e for e in events if events_filter(e)]
    prints = run.annual_prints(run.load_eps_series(slug))
    fills, veto0 = run.simulate_fills(slug, run.D(d0), triggers, prices, events, prints)
    return fills


def brief(fills):
    return {t: (f.get("fill_date") or ("VETO@fill" if f.get("blocked_by_gev_at_fill") else ("VETO@score" if f.get("blocked_by_gev_at_scoring") else None))) for t, f in fills.items()}


def names_filled(fill_map):
    return sorted({k.split("_")[0] for k, f in fill_map.items() if NAMEDATES[k][3] == "winner" and any(v.get("fill_date") for v in f.values())})


out = {}

# S0 baseline winner fills, and fills with GEV switched off entirely (mechanism attribution for winners/mediocre)
base, nog = {}, {}
for k, r in res["results"].items():
    if r.get("status") != "ok":
        continue
    if DEC(k):
        base[k] = r["fills"]
        nog[k] = r["fills_if_gev_off"]
out["S0_winner_names_baseline"] = names_filled(base)
out["S0_winner_names_if_GEV_off"] = names_filled(nog)
out["S0_name_dates_where_GEV_blocked_at_least_one_leg"] = {
    k: sorted(t for t, f in nog[k].items() if f.get("fill_date") and not base[k][t].get("fill_date")) for k in base
    if any(f.get("fill_date") and not base[k][t].get("fill_date") for t, f in nog[k].items())}

# S1 borderline / judgement readings on the GEV log (each toggled alone), effect on winner-name count
def toggled(slug_key, drop):
    def go(k):
        r = res["results"][k]
        if r.get("status") != "ok" or not r.get("triggers"):
            return None
        return brief(replay(k, r["triggers"], lambda e: e[0] not in drop))
    return go

S1 = {}
tests = {
    "kei_settlements_not_counted (2019-02-28, 2019-05-16)": ("kei", {"2019-02-28", "2019-05-16"}),
    "kei_only_company_order_not_counted (2019-05-16)": ("kei", {"2019-05-16"}),
    "pidilite_intra_family_gifts_not_counted (all 9 gift rows)": ("pidilite", {"2017-09-02", "2018-06-01", "2019-03-18", "2019-04-08", "2019-06-28", "2019-07-26", "2019-12-02", "2019-12-27", "2020-02-26"}),
    "pidilite_only_out_of_group_gifts_counted (2017-09-02, 2018-06-01, 2019-12-02)": ("pidilite", {"2019-03-18", "2019-04-08", "2019-06-28", "2019-07-26", "2019-12-27", "2020-02-26"}),
    "emami_exonerating_SCN_order_not_counted (2018-05-18)": ("emami", {"2018-05-18"}),
    "sunpharma_all_events_not_counted": ("sunpharma", {"2017-08-10", "2019-03-05", "2019-09-04", "2020-02-21", "2020-07-27", "2021-02-11"}),
    "sunpharma_2019-03-05_and_2020-02-21_not_counted (press-report/letter rows)": ("sunpharma", {"2019-03-05", "2020-02-21"}),
    "tiindia_2022-12-23_associate_row_not_counted": ("tiindia", {"2022-12-23"}),
}
for label, (slug, drop) in tests.items():
    row = {}
    for k in NAMEDATES:
        if NAMEDATES[k][0] == slug and res["results"][k].get("triggers"):
            row[k] = toggled(slug, drop)(k)
    S1[label] = row
out["S1_gev_reading_toggles"] = S1

# S1b winner-name count if the KEI + Pidilite + (any other winner) readings are relaxed jointly (upper bound on the winner leg)
joint = {}
for k in NAMEDATES:
    r = res["results"][k]
    if NAMEDATES[k][3] != "winner" or not DEC(k) or not r.get("triggers"):
        continue
    joint[k] = replay(k, r["triggers"], lambda e: False)  # no GEV
out["S1b_winner_names_if_all_GEV_ignored"] = names_filled(joint)

# S2 blow-ups: usability gate ignored (shadow), GEV as logged; and both gates off
S2 = {}
for k, r in res["results"].items():
    if NAMEDATES[k][3] != "blowup":
        continue
    S2[k] = {"usability": res["usability"][k]["verdict"], "fills_gev_on": brief(r.get("fills", {})),
             "fills_gev_off": brief(r.get("fills_if_gev_off", {})),
             "fill_detail_gev_on": {t: {"date": f.get("fill_date"), "price": f.get("fill_price"), "trigger": f.get("trigger"), "to_latest": f.get("to_latest"), "fwd_24m": f.get("fwd_24m")}
                                    for t, f in r.get("fills", {}).items() if f.get("fill_date")}}
out["S2_blowups_usability_ignored"] = S2

# S3 Gayatri under the frozen mcap/price share count (guard not applied)
g = res["results"]["gayatri_2019-03-31"]
S3 = {}
for k in ("gayatri_2019-03-31", "gayatri_2020-03-31"):
    r = res["results"][k]
    fv_frozen = r["fv"] * r["shares_cr"] / r["model"]["shares_cr_frozen_method"]
    trg = {t: round(m * fv_frozen, 2) for t, m in run.TIERS.items() if t != "qfv"}
    S3[k] = {"fv_guard": round(r["fv"], 2), "fv_frozen_method": round(fv_frozen, 2), "fills_gev_on": brief(replay(k, trg))}
out["S3_gayatri_frozen_mcap_share_count"] = S3

# S4 Srei: delisted terminal value. Series ends 2023-08-11; fills counted at the last vendor price.
sr = res["results"]["srei_2020-03-31"]
out["S4_srei_fill_detail"] = {t: f for t, f in sr["fills"].items()}
out["S4_srei_zero_terminal_to_T"] = 0.0
out["S4_srei_gev_events_by_date"] = sr["gev_events_logged"]

# S5 aggregates of decisional fills (leg-weighted), by category; and excluding COVID-trough entries (fill date 2020-03-13..2020-04-30)
cat = {}
for k, r in res["results"].items():
    if r["shadow"] or "fills" not in r:
        continue
    for t, f in r["fills"].items():
        if f.get("fill_date"):
            cat.setdefault(r["category"], []).append((k, t, f["fill_date"], f["to_latest"], f["fwd_24m"]))
S5 = {}
for c, rows in cat.items():
    S5[c] = {"n_legs": len(rows), "mean_to_t": sum(x[3] for x in rows) / len(rows), "mean_24m": sum(x[4] for x in rows) / len(rows), "min_24m": min(x[4] for x in rows)}
allrows = sum(cat.values(), [])
covid = [x for x in allrows if "2020-03-13" <= x[2] <= "2020-04-30"]
non = [x for x in allrows if x not in covid]
S5["covid_trough_entries_2020-03-13_to_2020-04-30"] = {"n_legs": len(covid), "mean_to_t": sum(x[3] for x in covid) / len(covid), "mean_24m": sum(x[4] for x in covid) / len(covid)}
S5["other_entries"] = {"n_legs": len(non), "mean_to_t": sum(x[3] for x in non) / len(non), "mean_24m": sum(x[4] for x in non) / len(non)} if non else None
S5["all_legs_ex_blowup"] = {"n_legs": len(allrows) - len(cat.get("blowup", [])),
                            "mean_to_t": sum(x[3] for x in allrows if x[0].split("_")[0] != "srei") / max(1, len(allrows) - len(cat.get("blowup", []))),
                            "mean_24m": sum(x[4] for x in allrows if x[0].split("_")[0] != "srei") / max(1, len(allrows) - len(cat.get("blowup", [])))}
out["S5_aggregates"] = S5
out["S5_all_decisional_fill_legs"] = allrows

json.dump(out, open(f"{HERE}/sensitivity_v311.json", "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
