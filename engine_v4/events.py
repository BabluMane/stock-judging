"""§5 event lane: 7-type closed taxonomy, SEVERE/MODERATE/WATCH grading, entry veto
(trailing 12m at d0 and each fill), cooling-off, in-window exit on SEVERE.

Event records are dicts (the dated public record as logged):
  event_date, type in T1..T7 | "WATCH", subcase (closed list below),
  sources [{tier: 1|2|3, ref}]  -- 1 exchange filing, 2 regulator/agency document, 3 national press
  T6: underlying_grade, names_company_directly       T7: agency_publication_date
A record whose (type, subcase) is not on the closed list is not an event (ValueError).
A sub-case the spec lists in §5.1 but never grades in §5.2 raises SpecGapError: the
engine does not pick a grade (see GAPS).
"""
from . import constants as C
from .common import SpecGapError, add_months, iso, weekdays_between

SEVERE, MODERATE, WATCH = "SEVERE", "MODERATE", "WATCH"
_RANK = {WATCH: 0, MODERATE: 1, SEVERE: 2}
GAP = None   # grade the spec does not state

# (type, subcase) -> grade, exactly per §5.2.
GRADES = {
    ("T1", "order_fraud_cheating_misstatement"): SEVERE,
    ("T1", "order_trading_or_registrant_ban"): SEVERE,
    ("T1", "probe_or_scn_opened_no_adverse_finding"): MODERATE,
    ("T1", "order_or_direction_without_fraud_finding_or_ban"): GAP,      # GAPS[0]
    ("T2", "opinion_adverse_or_disclaimer"): SEVERE,
    ("T2", "opinion_qualified"): MODERATE,
    ("T2", "resignation_citing_disagreement_fraud_or_unpaid_fees"): SEVERE,  # §5.1 T2 (§5.2 omits 'unpaid fees'; GAPS[1])
    ("T2", "caro_suspected_fraud_flag"): SEVERE,
    ("T2", "resignation_no_stated_reasons"): MODERATE,
    ("T2", "resignation_other_stated_reasons"): GAP,                     # GAPS[2]
    ("T3", "pledge_invocation"): SEVERE,
    ("T3", "off_market_transfer_or_gift"): MODERATE,
    ("T4", "withdrawn_buyback_dividend_or_fundraise"): MODERATE,
    ("T5", "arrest_chargesheet_or_conviction"): SEVERE,
    ("T5", "mca_ordered_investigation_or_inspection"): MODERATE,
    ("T5", "named_fir"): GAP,                                            # GAPS[3]
    ("T6", "associate_contagion"): "DERIVED",
    ("T7", "downgrade_to_D_default_rationale"): SEVERE,
    ("T7", "downgrade_sub_investment_grade_not_D"): MODERATE,
    ("WATCH", "disclosure_lapse_no_order"): WATCH,
    ("WATCH", "rbi_special_audit_no_adverse_conclusion"): WATCH,
    ("WATCH", "sebi_settlement_no_admission"): WATCH,
    ("WATCH", "media_rumor_no_dated_record"): WATCH,
}

GAPS = [
    "§5.1 T1 lists adjudication/enforcement orders and interim directions; §5.2 grades only fraud-finding / ban orders (SEVERE) and probe/SCN-opened (MODERATE). An order with neither is ungraded.",
    "§5.1 T2 makes a resignation citing 'unpaid fees' SEVERE; §5.2's SEVERE list omits 'unpaid fees'. Carried as SEVERE per §5.1 (no contradiction, an omission) -- flagged for confirmation.",
    "§5.2 grades resignations 'citing disagreement/fraud' SEVERE and 'no stated reasons' MODERATE; a resignation with other stated reasons is ungraded.",
    "§5.1 T5 lists a 'named FIR'; §5.2 grades arrest / charge-sheet / conviction (SEVERE) and MCA-ordered investigation (MODERATE). A named FIR alone is ungraded.",
    "§5.1 T6: 'downgraded one grade (SEVERE->MODERATE)'; a MODERATE underlying action of a non-directly-named associate is not specified (WATCH by 'one grade', MODERATE by the §5.2 list).",
]

GAP_INDEX = {("T1", "order_or_direction_without_fraud_finding_or_ban"): 0,
             ("T2", "resignation_other_stated_reasons"): 2, ("T5", "named_fir"): 3}


def grade_event(rec):
    """Grade one record at log time (frozen then). Returns a flat dict with the effective
    grade after the source-severity cap (§5.2: SEVERE needs >=1 exchange-filing or
    agency-document source; press-only = WEAK-SOURCE, capped at MODERATE)."""
    key = (rec["type"], rec["subcase"])
    if key not in GRADES:
        raise ValueError(f"not on the closed taxonomy (§5.1): {key}")
    sources = rec.get("sources") or []
    if rec["type"] != "WATCH" and not sources:
        raise ValueError("a qualifying event is a dated public record: at least one source required")
    if rec["type"] == "T7":
        if rec.get("agency_publication_date") is None:
            raise ValueError("T7 needs agency_publication_date (event date = agency publication date, §5.1/§12 item 14)")
        event_date = rec["agency_publication_date"]    # court stays barring default recognition do not change the date
    else:
        event_date = rec["event_date"]
    g = GRADES[key]
    if g == "DERIVED":                                  # T6
        under = rec["underlying_grade"]
        if rec.get("names_company_directly"):
            g = under
        elif under == SEVERE:
            g = MODERATE
        elif under == WATCH:
            g = WATCH
        else:
            raise SpecGapError(f"§5.1 T6 / §5.2: {GAPS[4]}")
    if g is GAP:
        raise SpecGapError(f"{key}: {GAPS[GAP_INDEX[key]]}")
    weak = bool(sources) and all(s["tier"] == 3 for s in sources)
    eff = MODERATE if (g == SEVERE and weak) else g
    return {"event_date": event_date, "type": rec["type"], "subcase": rec["subcase"], "raw_grade": g,
            "grade": eff, "weak_source": weak, "capped": eff != g,
            "description": rec.get("description"), "print_search": rec.get("print_search")}


def grade_all(records):
    return sorted((grade_event(r) for r in records or []), key=lambda e: e["event_date"])


# ------------------------------------------------------------- §5.3 cooling-off
def validate_search_log(log):
    """Two-source search protocol: 'no publication on record' needs a documented search of
    two of (a) screener.in results calendar, (b) BSE/NSE announcements, (c) company AR PDFs,
    with sources named, search date and zero hits recorded."""
    if not log:
        return {"valid": False, "reason": "no search recorded"}
    srcs = {s for s in (log.get("sources") or []) if s in C.SEARCH_SOURCES}
    ok = len(srcs) >= C.SEARCH_SOURCES_REQUIRED and log.get("search_date") is not None and log.get("zero_hits") is True
    return {"valid": ok, "sources": sorted(srcs), "search_date": iso(log.get("search_date")),
            "reason": None if ok else "needs >=2 named sources, a search date, and zero_hits=True"}


def cooling_off(ev, prints, E):
    """Block from event `ev` persists until 12 months after the event date AND one audited
    annual print with (i) results date strictly after the event AND (ii) FY-end strictly
    after the event -- whichever is later. No qualifying print on record => release not
    satisfied, block persists (logged WEAK-SOURCE search). Release-skeptical by design."""
    end_12m = add_months(ev["event_date"], C.COOLING_OFF_MONTHS)
    qual = sorted((p for p in prints or [] if p["results_date"] > ev["event_date"] and p["fy_end"] > ev["event_date"]),
                  key=lambda p: p["results_date"])
    if len(qual) < C.COOLING_OFF_PRINTS:
        s = validate_search_log(ev.get("print_search"))
        return {"blocked": ev["event_date"] <= E, "release": None, "reason": "no post-event audited print on record",
                "weak_source_search": True, "search": s}
    release = max(end_12m, qual[C.COOLING_OFF_PRINTS - 1]["results_date"])
    return {"blocked": ev["event_date"] <= E < release, "release": iso(release),
            "print": iso(qual[0]["results_date"]), "reason": "12m + 1 audited print"}


def entry_veto(graded, prints, E):
    """SEVERE + MODERATE events => entry veto at evaluation date E (d0 and every fill date):
    (1) event date inside the trailing 12 months before E, union (2) cooling-off block. Events
    dated after E are ignored (PIT). WATCH has no veto power."""
    hits = []
    for ev in graded:
        if ev["grade"] not in (SEVERE, MODERATE) or ev["event_date"] > E:
            continue
        # SPEC-SILENT: "in the trailing 12 months" read as (E - 12m, E]; equals the cooling-off 12m edge.
        in_window = add_months(E, -C.EVENT_WINDOW_MONTHS) < ev["event_date"] <= E
        cool = cooling_off(ev, prints, E)
        if in_window or cool["blocked"]:
            hits.append({"event": f'{ev["type"]} {iso(ev["event_date"])}', "grade": ev["grade"],
                         "weak_source": ev["weak_source"], "in_trailing_12m": in_window, "cooling_off": cool})
    return {"blocked": bool(hits), "date": iso(E), "hits": hits}


# ----------------------------------------------------------------- §5.4 exit scan
def exit_scan(fill_date, d0, prices, graded, trading_days_between=weekdays_between):
    """Mandatory per filled leg. Weekly dates w1<w2<... after the fill date through d0+24m;
    exit at the FIRST w_i with a SEVERE event dated in (fill, w_i]. MODERATE/WATCH never exit.
    Exit price = the weekly close at w_i (the next weekly close >= the event's evaluation week);
    returns use exit_price x 0.99. Delisting/suspension: no w_i >= event inside the window ->
    last available weekly close; if that print predates the event by > 20 trading days the exit
    is UNEXECUTED (return at the endpoint value, no mark-to-model)."""
    # SPEC-SILENT: w_i are the frozen series' own weekly dates; "the next weekly close >= the evaluation
    # week" is the close at w_i itself; an UNEXECUTED scan is reported fired=True with exit_date/price null
    # and the last print in `mark_price`; trading days are Mon-Fri (no exchange calendar in the input list).
    end = d0 + C.FILL_WINDOW
    severe = [e for e in graded if e["grade"] == SEVERE and fill_date < e["event_date"] <= end]
    if not severe:
        return {"fired": False, "exit_date": None, "exit_price": None, "triggering_event": None,
                "note": "no SEVERE event in (fill, d0+24m]"}
    ev = min(severe, key=lambda e: e["event_date"])      # earliest SEVERE => first w_i that has one
    trig = f'{ev["type"]} {iso(ev["event_date"])}'
    weeks = [(d, p) for d, p in prices if fill_date < d <= end]
    wi = next(((d, p) for d, p in weeks if d >= ev["event_date"]), None)
    last = prices[-1] if prices else None
    before = [(d, p) for d, p in prices if d <= ev["event_date"]]
    last_before = before[-1] if before else None
    if wi is not None:
        out = {"fired": True, "exit_date": iso(wi[0]), "exit_price": wi[1], "triggering_event": trig,
               "exit_price_after_slippage": wi[1] * C.EXIT_SLIPPAGE, "exit_unexecuted": False,
               "note": f"SEVERE {trig}; exit at weekly close {iso(wi[0])} x {C.EXIT_SLIPPAGE}"}
        if last_before and trading_days_between(last_before[0], ev["event_date"]) > C.DELIST_STALE_TRADING_DAYS:
            out["exit_after_relisting"] = True
            out["note"] += " (no close between last print and event window; relisting close used, §5.4(3))"
        return out
    # no weekly close at/after the event inside the window: delisted / suspended / truncated
    stale = last is not None and trading_days_between(last[0], ev["event_date"]) > C.DELIST_STALE_TRADING_DAYS
    if stale:
        return {"fired": True, "exit_date": None, "exit_price": None, "triggering_event": trig,
                "exit_unexecuted": True, "mark_price": last[1], "last_print": iso(last[0]),
                "note": f"UNEXECUTED: last print {iso(last[0])} predates {trig} by > {C.DELIST_STALE_TRADING_DAYS} trading days; return at endpoint value"}
    return {"fired": True, "exit_date": iso(last[0]), "exit_price": last[1], "triggering_event": trig,
            "exit_price_after_slippage": last[1] * C.EXIT_SLIPPAGE, "exit_unexecuted": False, "last_print_rule": True,
            "note": f"SEVERE {trig}; no weekly close after event; last available close {iso(last[0])} x {C.EXIT_SLIPPAGE}"}
