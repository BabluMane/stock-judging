"""§6 aggregation + §1 bar + §5.5 lane-exercise tabulation + §7 gate-trace table.

Leg-weighted means, price return only. Only decisional (FILLED) legs count; shadow legs
never do. An in-window exit feeds the aggregates as a realized exit but never un-fails a
fill: blow-up fills are counted at entry (§5.4/§6).
"""
from . import constants as C
from .run import ATTRIBUTION_ORDER


def _legs(results):
    for r in results.values():
        for tier, leg in r["legs"].items():
            if leg["status"] == "FILLED":
                yield r, tier, leg


def aggregates(results):
    legs = [leg for _, _, leg in _legs(results)]
    t = [l["ret_to_t"] for l in legs if l["ret_to_t"] is not None]
    m = [l["ret_24m"] for l in legs if l["ret_24m"] is not None]
    mean = lambda x: sum(x) / len(x) if x else None
    return {"n_legs": len(legs), "n_legs_to_t": len(t), "n_legs_24m": len(m),
            "mean_return_to_t": mean(t), "mean_return_24m": mean(m),
            "mean_mult_to_t": None if not t else 1 + mean(t),
            "mean_mult_24m": None if not m else 1 + mean(m),
            "n_realized_exits": sum(1 for l in legs if l["realized_exit"]),
            "n_unexecuted_exits": sum(1 for l in legs if l["exit_scan"].get("exit_unexecuted"))}


def decisional_count(results, decisional_test_set):
    """§8.2 exercise condition: distress screen decisional on >= 3 of the 5 certified set name-dates.
    Headline counts VETOED-DISTRESS only; data vetoes are reported separately (PR: reading flagged)."""
    rows = {k: results[k] for k in decisional_test_set if k in results}
    return {"n_certified": len(decisional_test_set),
            "decisional": sorted(k for k, r in rows.items() if r["distress_decisional"]),
            "decisional_incl_data_vetoes": sorted(k for k, r in rows.items() if r["distress_decisional_incl_data_vetoes"])}


def bar(results, decisional_test_set):
    """§1 live bar, recomputed mechanically from raw results.
    (c) 'to-T clearly positive' has no numeric definition anywhere in the spec (§9 forbids
    redefining it), so the mean is reported and the verdict is left to the reviewer (None)."""
    agg = aggregates(results)
    blow_nd = sorted(r["key"] for r in results.values() if r["category"] == "blowup"
                     and any(l["status"] == "FILLED" for l in r["legs"].values()))
    winners = sorted({r["company"] for r in results.values() if r["category"] == "winner"
                      and any(l["status"] == "FILLED" for l in r["legs"].values())})
    dc = decisional_count(results, decisional_test_set)
    void = len(decisional_test_set) < C.DECISIONAL_SET_SIZE
    exercised = len(dc["decisional"]) >= C.DECISIONAL_MIN
    leg_a_zero = len(blow_nd) <= C.BAR_MAX_BLOWUP_FILLS
    if void:
        leg_a = "VOID"
    elif not exercised:
        leg_a = "UNTESTED"          # an unexercised 0 is UNTESTED, not PASS -> run VOID
    else:
        leg_a = "PASS" if leg_a_zero else "FAIL"
    # SPEC-SILENT: multiples = 1 + mean leg return (the v3 runners reported multiples; the spec defines returns).
    m24 = agg["mean_mult_24m"]
    return {"leg_a": leg_a, "leg_a_blowup_fill_name_dates": blow_nd, "leg_a_prime": dc,
            "run_void": void or not exercised,
            "leg_b": {"winner_names_filled": winners, "pass": len(winners) >= C.BAR_MIN_WINNER_NAMES},
            "leg_c": {"mean_mult_to_t": agg["mean_mult_to_t"], "pass": None,
                      "note": "'clearly positive' is not numerically defined in the spec; reviewer judgment"},
            "leg_d": {"mean_mult_24m": m24, "pass": None if m24 is None else m24 >= C.BAR_MIN_24M_MULT},
            "aggregates": agg}


def event_lane_exercise(results):
    """§5.5 tabulation from the gate traces. (a) clean entry-veto decisional: distress and usability
    PASS, anchor touched, the lane blocked the fill; (b) decisional legs whose exit scan fired on a
    SEVERE event; (c) shadow decisional: the lane would have blocked/exited in the shadow pass of a
    name-date another gate had already stopped. Exercised iff (a)+(b)+(c) >= 1 with >= 1 in (a) or (b)."""
    a, b, c = [], [], []
    for k, r in results.items():
        g = r["gates"]
        for tier, leg in r["legs"].items():
            if leg["status"] == "BLOCKED" and leg["blocked_by"] == ["event_lane"]:
                a.append((k, tier))
            if leg["status"] == "FILLED" and leg["exit_scan"]["fired"]:
                b.append((k, tier))
        for tier, leg in (r.get("shadow") or {}).get("legs", {}).items():
            other_stop = [x for x in leg["blocked_by"] if x != "event_lane"]
            if other_stop and (("event_lane" in leg["blocked_by"]) or leg["exit_scan"]["fired"]):
                c.append((k, tier))
    return {"a_clean_entry_veto": a, "b_clean_exit": b, "c_shadow": c,
            "exercised": (len(a) + len(b) + len(c) >= 1) and (len(a) + len(b) >= 1)}


def trace_table(results):
    """§7 per-name-date gate-trace table: distress | usability | event lane | anchor + deciding stop."""
    hdr = ["name-date", "distress", "usability", "event lane", "anchor", "deciding stop", "fills"]
    rows = []
    for k, r in results.items():
        g = r["gates"]
        cell = lambda n: f'{g[n]["verdict"]} ({g[n]["label"]})'
        fills = ",".join(t for t, l in r["legs"].items() if l["status"] == "FILLED") or "-"
        rows.append([k] + [cell(n) for n in ATTRIBUTION_ORDER] + [r["deciding_stop"] or "-", fills])
    out = ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
    out += ["| " + " | ".join(x) + " |" for x in rows]
    return "\n".join(out)
