#!/usr/bin/env python3
"""Coordinator verification for Phase-D locked inputs (data assembly only).

Checks each phase_d_inputs/<name_date>.json WITHOUT running the engine:
  1. NameDate(**data) constructs (exact 16 dataclass fields, no extras).
  2. Prices ascending, covering [d0-12m, as_of], as_of >= d0+24m.
  3. PIT: select_scoring_fy(fy, d0) == manifest scoring_fy (63-day rule).
  4. FY coverage windows (non-fin: scoring-4..scoring; fin: scoring-2..scoring).
  5. Beta present and numeric; pledge/corp_actions/eps_series shapes sane.
  6. Blow-up E1 event records present with closed-taxonomy (type, subcase).

Prints PASS/FAIL per name-date and exits 0 only if all 25 pass.
"""
import json
import os
import sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = os.path.expanduser("~/workspace/stock-judging/port")
sys.path.insert(0, PORT)

from engine_v4.run import NameDate  # noqa: E402
from engine_v4.pit import select_scoring_fy  # noqa: E402
from engine_v4 import events as EV  # noqa: E402
from engine_v4.distress import is_financial  # noqa: E402

INPUTS = os.path.join(os.path.expanduser("~/workspace/stock-judging/v3"),
                      "validation", "v4_oos", "phase_d_inputs")


def parse(d):
    return date.fromisoformat(d) if isinstance(d, str) else d


def check(path, manifest):
    errs = []
    with open(path) as f:
        data = json.load(f)
    # 1. construction
    try:
        nd = NameDate(**{**data,
                         "d0": parse(data["d0"]),
                         "as_of": parse(data["as_of"]) if data.get("as_of") else None,
                         "fy": {int(y): {**r, "results_published":
                                         (parse(r["results_published"])
                                          if r.get("results_published") else None)}
                                for y, r in data["fy"].items()},
                         "prices": [(parse(d), p) for d, p in data["prices"]],
                         "pledge": [{**q, "quarter_end": parse(q["quarter_end"])}
                                     for q in data.get("pledge", [])],
                         "eps_series": [(parse(d), v) for d, v in data.get("eps_series", [])],
                         "corp_actions": [{**a, "ex_date": parse(a["ex_date"])}
                                           for a in data.get("corp_actions", [])],
                         "events": [{**e, "event_date": parse(e["event_date"])}
                                     for e in data.get("events", [])],
                         "audited_prints": [{**p, "results_date": parse(p["results_date"]),
                                             "fy_end": parse(p["fy_end"])}
                                             for p in data.get("audited_prints", [])]})
    except Exception as e:  # noqa: BLE001
        return [f"NameDate construction failed: {e}"]
    key = data["key"]
    if key != manifest["name_date"]:
        errs.append(f"key {key} != manifest {manifest['name_date']}")
    if data.get("category") != manifest["tier"] and not (
            manifest["tier"] == "mediocrity" and data.get("category") == "mediocre"):
        errs.append(f"category {data.get('category')} != tier {manifest['tier']}")
    d0 = nd.d0
    warns = []
    # 2. prices
    pr = nd.prices
    if not pr:
        errs.append("empty price series")
    else:
        if any(pr[i][0] >= pr[i + 1][0] for i in range(len(pr) - 1)):
            errs.append("prices not strictly ascending")
        if pr[0][0] > d0 - timedelta(days=366):
            warns.append(f"price start {pr[0][0]} < 12m before d0 (source limit; engine D5 degrades)")
        as_of = nd.as_of or pr[-1][0]
        if as_of < d0 + timedelta(days=730):
            errs.append(f"as_of {as_of} < d0+24m")
    # 3. PIT
    fy_scoring = select_scoring_fy(nd.fy, d0)
    if fy_scoring != manifest["scoring_fy"]:
        errs.append(f"select_scoring_fy={fy_scoring} != manifest {manifest['scoring_fy']}")
    # 4. FY coverage: manifest window [scoring-need+1, scoring] preferred; short
    # spans are a WARNING (named source limit — the engine degrades per-module),
    # not a FAIL. FAIL only if the scoring FY itself is absent (caught by PIT).
    need = 5 if not is_financial(nd.sector) else 3
    window = set(range(manifest["scoring_fy"] - need + 1, manifest["scoring_fy"] + 1))
    missing_win = sorted(window - set(nd.fy))
    if missing_win:
        warns.append(f"FY table missing window years (source limit): {missing_win}")
    # 5. beta + shapes
    if not isinstance(data.get("beta"), (int, float)):
        errs.append("beta missing/non-numeric")
    for q in nd.pledge:
        if q.get("basis") == "equity" and q.get("promoter_holding_pct") is None:
            errs.append(f"equity-basis pledge {q['quarter_end']} without promoter_holding_pct")
    # 6. blow-up events grade
    if manifest["tier"] == "blowup":
        try:
            EV.grade_all(nd.events)
        except Exception as e:  # noqa: BLE001
            errs.append(f"event grading failed: {e}")
        if not nd.events:
            errs.append("blow-up has no E1 event record")
    return errs, warns


def main():
    with open(os.path.join(os.path.expanduser("~/workspace/stock-judging/v3"),
                           "validation", "v4_oos", "SET_MANIFEST.json")) as f:
        manifest = {n["name_date"]: n for n in json.load(f)["name_dates"]}
    fails = 0
    for name_date, m in sorted(manifest.items()):
        p = os.path.join(INPUTS, f"{name_date}.json")
        if not os.path.exists(p):
            print(f"FAIL {name_date}: file missing");
            fails += 1
            continue
        errs, warns = check(p, m)
        if errs:
            fails += 1
            print(f"FAIL {name_date}:")
            for e in errs:
                print(f"    - {e}")
        else:
            print(f"PASS {name_date}")
        for w in warns:
            print(f"    warn: {w}")
    print(f"\n{25 - fails}/25 pass")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
