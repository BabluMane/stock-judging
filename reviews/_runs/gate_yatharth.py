#!/usr/bin/env python3
"""Phase-D computability gate for yatharth_live. Read-only engine import; no writes to inputs/engine."""
import json, os, sys
from datetime import date
PORT = os.path.expanduser("~/workspace/stock-judging/port")
sys.path.insert(0, PORT)
from engine_v6.run import NameDate, run_name_date
from engine_v6 import distress, usability, anchor, events
from engine_v6.pit import select_scoring_fy, last_close_on_or_before

def parse(d): return date.fromisoformat(d) if isinstance(d, str) else d
def load(path):
    data = json.load(open(path))
    return NameDate(**{**data,
        "d0": parse(data["d0"]),
        "as_of": parse(data["as_of"]) if data.get("as_of") else None,
        "fy": {int(y): {**r, "results_published": parse(r["results_published"]) if r.get("results_published") else None}
               for y, r in data["fy"].items()},
        "prices": [(parse(d), float(p)) for d, p in data["prices"]],
        "pledge": [{**q, "quarter_end": parse(q["quarter_end"])} for q in (data.get("pledge") or [])],
        "eps_series": [(parse(d), v) for d, v in data.get("eps_series", [])],
        "corp_actions": [{**a, "ex_date": parse(a["ex_date"])} for a in data.get("corp_actions", [])],
        "events": [{**e, "event_date": parse(e["event_date"])} for e in data.get("events", [])],
        "audited_prints": data.get("audited_prints", [])})

nd = load(os.path.join(PORT, "data/inputs/yatharth.json"))
fy_scoring = select_scoring_fy(nd.fy, nd.d0)
print("scoring_fy:", fy_scoring)
dis = distress.evaluate(nd.fy, fy_scoring, nd.sector, nd.prices, nd.pledge, nd.d0, nd.equity_increase_solely_bonus_split)
use = usability.evaluate(nd.fy, fy_scoring, nd.eps_series, nd.corp_actions, nd.audited_eps_by_fy)
anc = anchor.value_anchor(nd.fy, fy_scoring, distress.is_financial(nd.sector), nd.beta, nd.mcap_cr, nd.mcap_price,
                          last_close_on_or_before(nd.prices, nd.d0)[1])
print("\n--- DISTRESS:", dis["verdict"], "|", dis.get("label"))
for k, v in dis.get("checks", {}).items():
    print(f"  {k}: {v.get('status')} {v.get('reason','')}")
print("\n--- USABILITY:", use["verdict"], "|", use.get("label"))
for k, v in use.get("checks", {}).items():
    print(f"  {k}: {v.get('status')} {v.get('reason','')}")
print("\n--- ANCHOR: valued =", anc.get("valued"), "| reason:", anc.get("reason"))
print("  triggers:", json.dumps({t: anc["trigger"][t] for t in ("G1","G2")}, default=str))
print("  DCF_FV:", anc.get("dcf_fv"), "| P_G1:", anc.get("p_g1"))
