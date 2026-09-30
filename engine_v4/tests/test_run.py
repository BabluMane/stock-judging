import copy, unittest
from datetime import date, timedelta

from engine_v4 import aggregate as A, events as E
from engine_v4.run import ATTRIBUTION_ORDER, run_name_date
from engine_v4.tests import fixtures as F

FIRST = next(d for d, _ in F.flat_prices() if d > F.D0)            # first weekly close after d0


def dip(nd, start, price, weeks=None):
    """Prices from `start` (for `weeks` weeks, default: rest of series) set to `price`."""
    end = start + timedelta(weeks=weeks) if weeks else date(2100, 1, 1)
    return F.with_prices(nd, {d: price for d, _ in nd.prices if start <= d < end})


def triggers(nd=None):
    return run_name_date(nd or F.make_nd())["anchor"]["trigger"]


def ev(t, sub, d, tier=1, **kw):
    r = {"event_date": d, "type": t, "subcase": sub, "sources": [{"tier": tier, "ref": "x"}], **kw}
    if t == "T7":
        r["agency_publication_date"] = d
    return r


class Fills(unittest.TestCase):
    def test_clean_filled_leg_has_mandatory_exit_scan_and_realized_return(self):
        nd = F.make_nd()
        t = triggers(nd)
        d = FIRST + timedelta(weeks=10)
        res = run_name_date(dip(nd, d, t["G1"] * 0.9, weeks=1))               # one-week dip, then back to 100
        leg = res["legs"]["G1"]
        self.assertEqual(leg["status"], "FILLED")
        self.assertEqual(leg["fill_date"], d.isoformat())
        self.assertEqual(leg["exit_scan"], {"fired": False, "exit_date": None, "exit_price": None, "triggering_event": None,
                                            "note": "no SEVERE event in (fill, d0+24m]"})
        self.assertFalse(leg["realized_exit"])
        self.assertAlmostEqual(leg["ret_to_t"], 100.0 / leg["fill_price"] - 1)
        self.assertIn("ret_24m", leg)
        self.assertFalse(res["excluded"])
        self.assertIsNone(res["deciding_stop"])

    def test_first_weekly_close_at_or_below_trigger_one_leg_per_tier(self):
        nd = F.make_nd()
        t = triggers(nd)
        d1, d2 = FIRST + timedelta(weeks=3), FIRST + timedelta(weeks=12)
        nd = F.with_prices(nd, {d1: t["G1"] - 0.01, d2: t["G2"] - 0.01})
        res = run_name_date(nd)
        self.assertEqual(res["legs"]["G1"]["fill_date"], d1.isoformat())     # G1 touched first
        self.assertEqual(res["legs"]["G2"]["fill_date"], d2.isoformat())     # G2 needs the deeper dip
        self.assertEqual(run_name_date(F.with_prices(F.make_nd(), {d1: t["G1"]}))["legs"]["G1"]["status"], "FILLED")   # <= inclusive

    def test_no_touch_and_not_valued_legs(self):
        res = run_name_date(F.make_nd())
        self.assertEqual({t: l["status"] for t, l in res["legs"].items()}, {"G1": "NO_TOUCH", "G2": "NO_TOUCH"})
        self.assertEqual(res["gates"]["anchor"]["label"], "NO-TOUCH")
        nd = F.make_nd(mcap_cr=None)
        res = run_name_date(nd)
        self.assertEqual({l["status"] for l in res["legs"].values()}, {"NO_TRIGGER"})
        self.assertEqual(res["gates"]["anchor"]["label"], "NOT-VALUED")

    def test_to_t_and_24m_returns_for_unexited_leg(self):
        nd = F.make_nd()
        t = triggers(nd)
        d = FIRST + timedelta(weeks=5)
        nd = F.with_prices(nd, {d: t["G1"] - 1})
        leg = run_name_date(nd)["legs"]["G1"]
        fp = t["G1"] - 1
        self.assertAlmostEqual(leg["ret_to_t"], 100.0 / fp - 1)
        self.assertAlmostEqual(leg["ret_24m"], 100.0 / fp - 1)


class ParallelGates(unittest.TestCase):
    def worst_case(self):
        """distress STOP (pledge 60%), usability STOP (EPS<0), event lane STOP (MODERATE in trailing 12m),
        anchor would fill (dip)."""
        nd = F.make_nd(pledge=F.quarters(pledged=60.0), events=[ev("T4", "withdrawn_buyback_dividend_or_fundraise", date(2018, 12, 1))])
        nd.fy[2018]["eps"] = -2.0
        t = triggers(F.make_nd())
        return dip(nd, FIRST + timedelta(weeks=4), t["G1"] * 0.5)

    def test_every_gate_evaluated_and_reported_no_early_return(self):
        res = run_name_date(self.worst_case())
        self.assertEqual(set(res["gates"]), set(ATTRIBUTION_ORDER))
        self.assertTrue(all(g["verdict"] == "STOP" for g in res["gates"].values() if g is not res["gates"]["anchor"]))
        self.assertEqual(res["gates"]["anchor"]["verdict"], "PASS")
        self.assertEqual(res["all_stops"], ["distress", "usability", "event_lane"])
        self.assertEqual(res["distress"]["label"], "VETOED-DISTRESS:D1")
        self.assertEqual(res["usability"]["label"], "VETOED-DATA")

    def test_deciding_stop_order_distress_usability_event_anchor(self):
        self.assertEqual(ATTRIBUTION_ORDER, ("distress", "usability", "event_lane", "anchor"))
        res = run_name_date(self.worst_case())
        self.assertTrue(res["excluded"])
        self.assertEqual(res["deciding_stop"], "distress")
        nd = self.worst_case(); nd.pledge = F.quarters()                      # distress now passes
        self.assertEqual(run_name_date(nd)["deciding_stop"], "usability")
        nd.fy[2018]["eps"] = F.fy_records()[2018]["eps"]                      # usability passes
        self.assertEqual(run_name_date(nd)["deciding_stop"], "event_lane")
        nd.events = []                                                        # event lane passes -> fills
        res = run_name_date(nd)
        self.assertIsNone(res["deciding_stop"])
        self.assertEqual(res["legs"]["G1"]["status"], "FILLED")
        res = run_name_date(F.make_nd())                                      # only the anchor stops
        self.assertEqual((res["deciding_stop"], res["all_stops"]), ("anchor", ["anchor"]))

    def test_distress_blocks_every_fill_across_the_whole_window(self):
        res = run_name_date(dip(F.make_nd(pledge=F.quarters(pledged=60.0)), FIRST, triggers()["G2"] * 0.5))
        self.assertEqual({l["status"] for l in res["legs"].values()}, {"BLOCKED"})
        self.assertTrue(all(l["blocked_by"] == ["distress"] for l in res["legs"].values()))

    def test_union_blocks_and_blocked_legs_name_every_blocker(self):
        res = run_name_date(self.worst_case())
        self.assertEqual(res["legs"]["G1"]["blocked_by"], ["distress", "usability", "event_lane"])

    def test_anchor_not_valued_does_not_suppress_other_gates(self):
        nd = F.make_nd(mcap_cr=None, pledge=F.quarters(pledged=60.0))
        res = run_name_date(nd)
        self.assertEqual(res["all_stops"], ["distress", "anchor"])
        self.assertEqual(res["gates"]["distress"]["label"], "VETOED-DISTRESS:D1")
        self.assertEqual(res["usability"]["verdict"], "PASS")

    def test_amended_named_fir_is_moderate_and_vetoes_entry(self):
        nd = F.make_nd(events=[ev("T5", "named_fir", date(2018, 12, 1))])
        res = run_name_date(nd)
        self.assertEqual(res["events"][0]["grade"], "MODERATE")
        self.assertEqual(res["gates"]["event_lane"]["verdict"], "STOP")


class EventLaneTiming(unittest.TestCase):
    def test_veto_is_evaluated_at_each_fill_date_not_only_d0(self):
        nd = F.make_nd()
        t = triggers(nd)
        fill = FIRST + timedelta(weeks=8)
        nd.events = [ev("T4", "withdrawn_buyback_dividend_or_fundraise", FIRST + timedelta(weeks=2))]      # lands after d0, before the fill
        res = run_name_date(dip(nd, fill, t["G1"] * 0.5))
        self.assertFalse(res["event_veto_at_d0"]["blocked"])
        self.assertEqual(res["legs"]["G1"]["status"], "BLOCKED")
        self.assertEqual(res["legs"]["G1"]["blocked_by"], ["event_lane"])
        self.assertEqual(res["gates"]["event_lane"]["tiers_blocked_at_fill"], ["G1", "G2"])
        self.assertEqual(res["deciding_stop"], "event_lane")

    def test_c8_retired_scoring_veto_does_not_block_the_whole_24m_window(self):
        """Event before d0, cooled off (12m + a later audited print) by the fill date -> fill allowed."""
        nd = F.make_nd()
        t = triggers(nd)
        nd.events = [ev("T4", "withdrawn_buyback_dividend_or_fundraise", date(2018, 6, 1))]
        nd.audited_prints = [{"results_date": date(2018, 8, 1), "fy_end": date(2018, 6, 30)}]
        fill = date(2019, 9, 6)                                               # > 12 months after the event
        res = run_name_date(dip(nd, fill, t["G1"] * 0.5))
        self.assertTrue(res["event_veto_at_d0"]["blocked"])                   # veto active at d0 (reported) ...
        self.assertEqual(res["legs"]["G1"]["status"], "FILLED")               # ... but only the fill-date evaluation decides
        self.assertEqual(res["legs"]["G1"]["fill_date"], fill.isoformat())

    def test_blocked_first_touch_is_not_retried_later_carried_v3_mechanics(self):
        nd = F.make_nd()
        t = triggers(nd)
        nd.events = [ev("T4", "withdrawn_buyback_dividend_or_fundraise", FIRST + timedelta(weeks=1))]
        nd = dip(nd, FIRST + timedelta(weeks=3), t["G1"] * 0.5)              # touch (blocked) and stays below thereafter
        self.assertEqual(run_name_date(nd)["legs"]["G1"]["status"], "BLOCKED")


class Exits(unittest.TestCase):
    def setUp(self):
        nd = F.make_nd(category="blowup", key="bad_2019-03-31")
        self.t = triggers(nd)
        self.fill = FIRST + timedelta(weeks=6)
        self.nd = dip(nd, self.fill, self.t["G1"] * 0.9, weeks=1)             # fill at 0.9 x trigger, then back up
        self.fill_price = self.t["G1"] * 0.9

    def test_severe_event_exits_with_slippage_and_feeds_aggregates_as_realized(self):
        d_ev = self.fill + timedelta(weeks=20)
        self.nd.events = [ev("T3", "pledge_invocation", d_ev)]
        res = run_name_date(self.nd)
        leg = res["legs"]["G1"]
        sc = leg["exit_scan"]
        self.assertTrue(sc["fired"])
        self.assertEqual(sc["triggering_event"], f"T3 {d_ev.isoformat()}")
        self.assertTrue(leg["realized_exit"])
        self.assertAlmostEqual(leg["ret_to_t"], (sc["exit_price"] * 0.99 - self.fill_price) / self.fill_price)
        self.assertEqual(leg["ret_to_t"], leg["ret_24m"])                     # identical in both aggregates
        self.assertEqual(res["legs"]["G2"]["status"], "NO_TOUCH")            # 0.9 x G1 trigger is still above the G2 trigger
        self.assertEqual(A.aggregates({res["key"]: res})["n_realized_exits"], 1)

    def test_exit_never_unfails_a_blowup_fill(self):
        self.nd.events = [ev("T3", "pledge_invocation", self.fill + timedelta(weeks=20))]
        res = run_name_date(self.nd)
        self.assertTrue(res["legs"]["G1"]["exit_scan"]["fired"])
        b = A.bar({res["key"]: res}, list("abcde"))
        self.assertEqual(b["leg_a_blowup_fill_name_dates"], [res["key"]])     # scored at entry
        self.assertEqual(b["leg_a"], "UNTESTED")                              # also (a') unexercised -> not a PASS

    def test_moderate_event_never_exits(self):
        self.nd.events = [ev("T4", "withdrawn_buyback_dividend_or_fundraise", self.fill + timedelta(weeks=20))]
        self.assertFalse(run_name_date(self.nd)["legs"]["G1"]["exit_scan"]["fired"])

    def test_press_only_severe_never_forces_exit(self):
        self.nd.events = [ev("T3", "pledge_invocation", self.fill + timedelta(weeks=20), tier=3)]
        res = run_name_date(self.nd)
        self.assertFalse(res["legs"]["G1"]["exit_scan"]["fired"])
        self.assertTrue(res["events"][0]["weak_source"])

    def test_delisted_name_unexecuted_exit_uses_endpoint_value(self):
        cut = self.fill + timedelta(weeks=8)
        nd = self.nd
        nd.prices = [(d, p) for d, p in nd.prices if d <= cut]                # series truncated (delisted)
        nd.events = [ev("T7", "downgrade_to_D_default_rationale", cut + timedelta(weeks=30))]
        res = run_name_date(nd)
        leg = res["legs"]["G1"]
        self.assertTrue(leg["exit_scan"]["exit_unexecuted"])
        self.assertFalse(leg["realized_exit"])
        self.assertAlmostEqual(leg["ret_to_t"], nd.prices[-1][1] / self.fill_price - 1)   # last print, no slippage, no model mark

    def test_every_filled_leg_carries_exit_scan(self):
        res = run_name_date(self.nd)
        for leg in res["legs"].values():
            if leg["status"] == "FILLED":
                self.assertIn("exit_scan", leg)
                self.assertIn("fired", leg["exit_scan"])


class ShadowAndAggregation(unittest.TestCase):
    def test_vetoed_name_date_is_anchor_valued_in_a_non_decisional_shadow(self):
        nd = F.make_nd(pledge=F.quarters(pledged=60.0))
        res = run_name_date(dip(nd, FIRST + timedelta(weeks=4), triggers()["G1"] * 0.5))
        sh = res["shadow"]
        self.assertTrue(sh["non_decisional"])
        self.assertEqual(set(sh["legs"]), {"G1", "G2"})
        self.assertTrue(all(l["non_decisional"] and "exit_scan" in l for l in sh["legs"].values()))
        self.assertEqual(A.aggregates({res["key"]: res})["n_legs"], 0)        # shadow legs never reach the aggregates
        self.assertNotIn("shadow", run_name_date(F.make_nd()))                # nothing vetoed -> no shadow pass needed

    def test_bar_leg_a_needs_exercise_leg_b_distinct_winner_companies(self):
        results, keys = {}, []
        for i in range(5):
            nd = F.make_nd(key=f"blow{i}_2019-03-31", category="blowup", pledge=F.quarters(pledged=60.0))
            results[nd.key] = run_name_date(dip(nd, FIRST + timedelta(weeks=4), triggers()["G1"] * 0.5))
            keys.append(nd.key)
        b = A.bar(results, keys)
        self.assertEqual(len(b["leg_a_prime"]["decisional"]), 5)
        self.assertEqual((b["leg_a"], b["run_void"]), ("PASS", False))        # zero fills AND exercised
        b2 = A.bar(results, keys[:4])
        self.assertEqual((b2["leg_a"], b2["run_void"]), ("VOID", True))       # < 5 certified -> VOID
        results["blow0_2019-03-31"]["distress_decisional"] = False
        results["blow1_2019-03-31"]["distress_decisional"] = False
        results["blow2_2019-03-31"]["distress_decisional"] = False
        self.assertEqual(A.bar(results, keys)["leg_a"], "UNTESTED")           # 2 < 3 decisional -> UNTESTED, run VOID

    def test_winner_names_counted_by_company_token_up_to_last_underscore(self):
        results = {}
        for key in ("tvs_motor_2019-03-31", "tvs_motor_2020-03-31", "kei_2019-03-31"):
            nd = F.make_nd(key=key, category="winner")
            results[key] = run_name_date(dip(nd, FIRST + timedelta(weeks=4), triggers()["G1"] * 0.5))
        b = A.bar(results, list("abcde"))
        self.assertEqual(b["leg_b"]["winner_names_filled"], ["kei", "tvs_motor"])
        self.assertFalse(b["leg_b"]["pass"])                                  # 2 distinct names < 3

    def test_leg_c_is_reported_not_judged(self):
        b = A.bar({}, list("abcde"))
        self.assertIsNone(b["leg_c"]["pass"])

    def test_trace_table_has_one_column_per_gate(self):
        res = {"a_2019-03-31": run_name_date(F.make_nd(pledge=F.quarters(pledged=60.0)))}
        head = A.trace_table(res).splitlines()[0]
        self.assertEqual([h.strip() for h in head.strip("|").split("|")],
                         ["name-date", "distress", "usability", "event lane", "anchor", "deciding stop", "fills"])
        self.assertIn("VETOED-DISTRESS:D1", A.trace_table(res))


class LaneExercise(unittest.TestCase):
    def test_entry_veto_clean_decisional_counts_as_exercised(self):
        nd = F.make_nd(events=[ev("T4", "withdrawn_buyback_dividend_or_fundraise", date(2018, 12, 1))])
        res = {nd.key: run_name_date(dip(nd, FIRST + timedelta(weeks=3), triggers()["G1"] * 0.5))}
        x = A.event_lane_exercise(res)
        self.assertEqual(x["a_clean_entry_veto"], [(nd.key, "G1"), (nd.key, "G2")])
        self.assertTrue(x["exercised"])

    def test_exit_fire_counts_and_shadow_only_is_not_exercised(self):
        nd = F.make_nd(category="blowup")
        t = triggers(nd)
        fill = FIRST + timedelta(weeks=6)
        nd2 = dip(nd, fill, t["G1"] * 0.9, weeks=1)
        nd2.events = [ev("T3", "pledge_invocation", fill + timedelta(weeks=20))]
        self.assertTrue(A.event_lane_exercise({"x": run_name_date(nd2)})["exercised"])
        # shadow only: distress stops the name; the lane would also have blocked in the shadow pass
        nd3 = F.make_nd(pledge=F.quarters(pledged=60.0), events=[ev("T4", "withdrawn_buyback_dividend_or_fundraise", date(2018, 12, 1))])
        r3 = run_name_date(dip(nd3, FIRST + timedelta(weeks=3), t["G1"] * 0.5))
        x = A.event_lane_exercise({"y": r3})
        self.assertTrue(x["c_shadow"])
        self.assertFalse(x["exercised"])                                      # a shadow-only lane is not exercised


class Hygiene(unittest.TestCase):
    def test_inputs_are_not_mutated(self):
        nd = F.make_nd(events=[ev("T4", "withdrawn_buyback_dividend_or_fundraise", date(2018, 12, 1))])
        before = copy.deepcopy((nd.fy, nd.prices, nd.events, nd.pledge))
        run_name_date(nd)
        self.assertEqual(before, (nd.fy, nd.prices, nd.events, nd.pledge))

    def test_no_lookahead_gates_use_only_data_at_or_before_d0(self):
        nd = F.make_nd()
        base = run_name_date(nd)
        nd2 = dip(F.make_nd(), F.D0 + timedelta(days=1), 1.0)                 # crash AFTER d0 must not trip D5 or move triggers
        res = run_name_date(nd2)
        self.assertEqual(res["distress"]["rules"]["D5"]["status"], "PASS")
        self.assertEqual(res["anchor"]["trigger"], base["anchor"]["trigger"])


if __name__ == "__main__":
    unittest.main()
