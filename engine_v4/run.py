"""Name-date runner: every gate evaluated in parallel (§7), fills (§6), exit scan (§5.4),
shadow pass (§7). No gate early-returns before the others are evaluated; the fill is blocked
by the union; the reported deciding stop follows distress -> usability -> event lane -> anchor.
"""
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

from . import anchor, constants as C, distress, events, usability
from .common import iso
from .pit import last_close_on_or_before, select_scoring_fy

ATTRIBUTION_ORDER = ("distress", "usability", "event_lane", "anchor")


@dataclass
class NameDate:
    key: str                      # <company token>_<YYYY-MM-DD>; company = up to the last underscore
    d0: date
    sector: str                   # screener.in Sector; Banks/Finance -> CAMEL class
    beta: float                   # sector beta, frozen pre-run by the pre-reg (input, not a table here)
    fy: dict                      # {fy_end_year: {field: value|None, results_published: date}}
    prices: list                  # [(date, adjusted weekly close)] ascending
    mcap_cr: Optional[float]
    mcap_price: Optional[float]   # the price mcap_cr was quoted at (shares = mcap / price)
    pledge: list = field(default_factory=list)
    eps_series: list = field(default_factory=list)      # publication-dated (unlagged) TTM EPS
    corp_actions: list = field(default_factory=list)
    events: list = field(default_factory=list)
    audited_prints: list = field(default_factory=list)  # [{results_date, fy_end}]
    equity_increase_solely_bonus_split: Optional[bool] = None
    audited_eps_by_fy: Optional[dict] = None
    category: Optional[str] = None                      # winner | mediocre | blowup (aggregation only)
    as_of: Optional[date] = None                        # T; defaults to the last price date

    @property
    def company(self):
        return self.key.rsplit("_", 1)[0]


def _first_touch(prices, d0, trigger):
    for d, p in prices:
        if d0 < d <= d0 + C.FILL_WINDOW and p <= trigger:
            return d, p
    return None


def leg_outcome(fill_date, fill_price, prices, scan, as_of):
    """Return computation (§5.4/§6): exited leg = (exit_price x 0.99 - fill)/fill, used
    identically in to-T and 24m. Never exited (or UNEXECUTED): entry->to-T and entry->24m at
    the last print (v3 convention: to-T = last available close; 24m = last close in fill+24m)."""
    latest = prices[-1]
    fwd = [(d, p) for d, p in prices if fill_date < d <= fill_date + C.FILL_WINDOW]
    raw_t = latest[1] / fill_price - 1
    raw_24 = (fwd[-1][1] / fill_price - 1) if fwd else None
    flags = {"fwd_truncated": bool(fwd and fwd[-1][0] < fill_date + C.FILL_WINDOW - timedelta(days=20)),
             "to_t_date": iso(latest[0]),
             "series_ends_before_as_of": latest[0] < as_of - timedelta(days=30)}
    if scan["fired"] and not scan.get("exit_unexecuted"):
        r = (scan["exit_price"] * C.EXIT_SLIPPAGE - fill_price) / fill_price
        return {"ret_to_t": r, "ret_24m": r, "realized_exit": True, "raw_ret_to_t": raw_t, "raw_ret_24m": raw_24, **flags}
    return {"ret_to_t": raw_t, "ret_24m": raw_24, "realized_exit": False, "raw_ret_to_t": raw_t,
            "raw_ret_24m": raw_24, **flags}


def run_name_date(nd):
    as_of = nd.as_of or nd.prices[-1][0]
    prices = [(d, p) for d, p in nd.prices if d <= as_of]
    graded = events.grade_all(nd.events)                 # SpecGapError propagates: never guessed
    fy_scoring = select_scoring_fy(nd.fy, nd.d0)
    p0 = last_close_on_or_before(nd.prices, nd.d0)

    # ---- all four gates, in parallel, none short-circuits the others ----
    dis = distress.evaluate(nd.fy, fy_scoring, nd.sector, nd.prices, nd.pledge, nd.d0,
                            nd.equity_increase_solely_bonus_split)
    use = usability.evaluate(nd.fy, fy_scoring, nd.eps_series, nd.corp_actions, nd.audited_eps_by_fy)
    anc = anchor.value_anchor(nd.fy, fy_scoring, distress.is_financial(nd.sector), nd.beta,
                              nd.mcap_cr, nd.mcap_price, p0[1] if p0 else None)
    ev0 = events.entry_veto(graded, nd.audited_prints, nd.d0)

    legs, shadow_legs = {}, {}
    for tier in C.TIERS:
        trig = anc["trigger"][tier] if anc["valued"] else None
        leg = {"tier": tier, "trigger": trig}
        if trig is None or trig <= 0:
            leg.update(status="NO_TRIGGER", reason=anc["reason"] if trig is None else f"non-positive trigger ({trig:.4g})")
            legs[tier] = leg
            continue
        touch = _first_touch(prices, nd.d0, trig)
        if touch is None:
            legs[tier] = {**leg, "status": "NO_TOUCH"}
            continue
        fill_date, fill_price = touch
        evf = events.entry_veto(graded, nd.audited_prints, fill_date)    # re-evaluated at each fill date
        blocked_by = [g for g, stop in (("distress", dis["verdict"] == "STOP"),
                                        ("usability", use["verdict"] == "STOP"),
                                        ("event_lane", evf["blocked"])) if stop]
        scan = events.exit_scan(fill_date, nd.d0, prices, graded)        # mandatory field, every filled leg
        outcome = leg_outcome(fill_date, fill_price, prices, scan, as_of)
        body = {"fill_date": iso(fill_date), "fill_price": fill_price, "event_veto_at_fill": evf,
                "exit_scan": scan, **outcome}
        if blocked_by:
            legs[tier] = {**leg, "status": "BLOCKED", "blocked_by": blocked_by, "would_have_filled": iso(fill_date)}
            shadow_legs[tier] = {**leg, "non_decisional": True, "blocked_by": blocked_by, **body}
        else:
            legs[tier] = {**leg, "status": "FILLED", **body}

    touched = [t for t, l in legs.items() if l["status"] in ("FILLED", "BLOCKED")]
    filled = [t for t, l in legs.items() if l["status"] == "FILLED"]
    event_blocked = [t for t, l in legs.items() if l["status"] == "BLOCKED" and "event_lane" in l["blocked_by"]]

    # SPEC-SILENT: §5.3 says the lane is evaluated at d0 AND each fill date, C8 (scoring veto blocks the
    # whole window) is retired, and §7 says the fill is blocked by the union of gates. Read together: the
    # d0 evaluation is REPORTED; the fill-date evaluation is what blocks a fill. The event-lane trace
    # column is STOP if the veto is active at d0 OR blocked any tier's fill.
    gates = {
        "distress": {"verdict": dis["verdict"], "label": dis["label"],
                     "reasons": dis["tripped"] + dis["uncomputable"]},
        "usability": {"verdict": use["verdict"], "label": use["label"], "reasons": [use.get("deciding_check")] if use["verdict"] == "STOP" else []},
        "event_lane": {"verdict": "STOP" if (ev0["blocked"] or event_blocked) else "PASS",
                       "label": "VETO" if (ev0["blocked"] or event_blocked) else "PASS",
                       "veto_at_d0": ev0["blocked"], "tiers_blocked_at_fill": event_blocked,
                       "reasons": [h["event"] for h in ev0["hits"]]},
        "anchor": ({"verdict": "PASS", "label": "PASS", "reasons": [], "tiers_touched": touched}
                   if touched else
                   {"verdict": "STOP", "label": "NOT-VALUED" if not anc["valued"] else "NO-TOUCH",
                    "reasons": [anc["reason"]] if not anc["valued"] else ["no weekly close <= trigger in (d0, d0+24m]"]}),
    }
    all_stops = [g for g in ATTRIBUTION_ORDER if gates[g]["verdict"] == "STOP"]
    excluded = not filled
    deciding = all_stops[0] if (excluded and all_stops) else None

    res = {"key": nd.key, "company": nd.company, "category": nd.category, "d0": iso(nd.d0),
           "scoring_fy": fy_scoring, "as_of": iso(as_of), "gates": gates, "all_stops": all_stops,
           "excluded": excluded, "deciding_stop": deciding,
           "distress": dis, "usability": use, "anchor": anc, "event_veto_at_d0": ev0,
           "events": [{**e, "event_date": iso(e["event_date"])} for e in graded],
           "legs": legs,
           # §8.2: distress is decisional iff its veto blocked a fill the anchor would otherwise have made.
           # SPEC-SILENT: the headline counts VETOED-DISTRESS (a tripped rule) only; VETOED-DATA is reported apart.
           "distress_decisional": bool(dis["tripped"]) and bool(touched),
           "distress_decisional_incl_data_vetoes": dis["verdict"] == "STOP" and bool(touched)}
    # shadow pass (non-decisional): vetoed name-dates are anchor-valued so exclusions cannot hide fills
    if anc["valued"] and (dis["verdict"] == "STOP" or use["verdict"] == "STOP" or ev0["blocked"] or event_blocked):
        res["shadow"] = {"non_decisional": True, "trigger": anc["trigger"], "p_d0": anc["p_d0"],
                         "implied": anc["implied"], "legs": shadow_legs}
    return res
