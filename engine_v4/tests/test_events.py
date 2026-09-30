import unittest
from datetime import date

from engine_v4 import events as E
from engine_v4.tests import fixtures as F


def rec(t, sub, d=date(2019, 6, 1), tier=1, **kw):
    return {"event_date": d, "type": t, "subcase": sub, "sources": [{"tier": tier, "ref": "x"}], **kw}


class Grading(unittest.TestCase):
    SEVERE = [("T1", "order_fraud_cheating_misstatement"), ("T1", "order_trading_or_registrant_ban"),
              ("T2", "opinion_adverse_or_disclaimer"), ("T2", "resignation_citing_disagreement_fraud_or_unpaid_fees"),
              ("T2", "caro_suspected_fraud_flag"), ("T3", "pledge_invocation"),
              ("T5", "arrest_chargesheet_or_conviction"), ("T7", "downgrade_to_D_default_rationale")]
    MODERATE = [("T1", "probe_or_scn_opened_no_adverse_finding"), ("T2", "opinion_qualified"),
                ("T2", "resignation_no_stated_reasons"), ("T3", "off_market_transfer_or_gift"),
                ("T4", "withdrawn_buyback_dividend_or_fundraise"), ("T5", "mca_ordered_investigation_or_inspection"),
                ("T7", "downgrade_sub_investment_grade_not_D"),
                # pre-run amendment 1: formerly ungraded, now MODERATE
                ("T1", "order_or_direction_without_fraud_finding_or_ban"), ("T2", "resignation_other_stated_reasons"),
                ("T5", "named_fir")]
    WATCH = ["disclosure_lapse_no_order", "rbi_special_audit_no_adverse_conclusion", "sebi_settlement_no_admission",
             "media_rumor_no_dated_record"]

    def g(self, t, sub, **kw):
        r = rec(t, sub, **kw)
        if t == "T7":
            r["agency_publication_date"] = r["event_date"]
        return E.grade_event(r)

    def test_exact_membership_per_5_2(self):
        for t, s in self.SEVERE:
            self.assertEqual(self.g(t, s)["grade"], "SEVERE", (t, s))
        for t, s in self.MODERATE:
            self.assertEqual(self.g(t, s)["grade"], "MODERATE", (t, s))
        for s in self.WATCH:
            self.assertEqual(E.grade_event({"event_date": date(2019, 6, 1), "type": "WATCH", "subcase": s})["grade"], "WATCH")

    def test_every_table_entry_is_accounted_for(self):
        listed = set(self.SEVERE) | set(self.MODERATE) | {("WATCH", s) for s in self.WATCH}
        rest = set(E.GRADES) - listed
        self.assertEqual(rest, {("T6", "associate_contagion")})            # derived from the underlying action

    def test_closed_taxonomy_rejects_anything_else(self):
        for bad in (("T8", "x"), ("T1", "earnings_restatement"), ("T4", "dividend_cut"), ("T3", "promoter_purchase"),
                    ("T2", "scheduled_auditor_rotation")):
            with self.assertRaises(ValueError):
                E.grade_event(rec(*bad))

    def test_press_only_severe_capped_at_moderate_and_tagged_weak_source(self):
        r = self.g("T3", "pledge_invocation", tier=3)
        self.assertEqual((r["raw_grade"], r["grade"], r["weak_source"], r["capped"]), ("SEVERE", "MODERATE", True, True))
        mixed = rec("T3", "pledge_invocation"); mixed["sources"].append({"tier": 3, "ref": "press"})
        self.assertEqual(E.grade_event(mixed)["grade"], "SEVERE")                  # one exchange/agency source is enough
        self.assertEqual(self.g("T4", "withdrawn_buyback_dividend_or_fundraise", tier=3)["grade"], "MODERATE")
        agency = self.g("T1", "order_trading_or_registrant_ban", tier=2)
        self.assertEqual(agency["grade"], "SEVERE")

    def test_qualifying_event_needs_a_source(self):
        with self.assertRaises(ValueError):
            E.grade_event({"event_date": date(2019, 6, 1), "type": "T4", "subcase": "withdrawn_buyback_dividend_or_fundraise"})

    def test_t7_event_date_is_agency_publication_date_regardless_of_stay(self):
        r = E.grade_event({"event_date": date(2021, 1, 15), "agency_publication_date": date(2020, 12, 20), "type": "T7",
                           "subcase": "downgrade_to_D_default_rationale", "sources": [{"tier": 2, "ref": "rationale.pdf"}]})
        self.assertEqual(r["event_date"], date(2020, 12, 20))
        with self.assertRaises(ValueError):
            E.grade_event(rec("T7", "downgrade_to_D_default_rationale"))

    def test_t6_downgrades_one_grade_unless_order_names_company(self):
        base = dict(type="T6", subcase="associate_contagion", event_date=date(2019, 6, 1), sources=[{"tier": 2, "ref": "order"}])
        self.assertEqual(E.grade_event({**base, "underlying_grade": "SEVERE", "names_company_directly": False})["grade"], "MODERATE")
        self.assertEqual(E.grade_event({**base, "underlying_grade": "SEVERE", "names_company_directly": True})["grade"], "SEVERE")
        self.assertEqual(E.grade_event({**base, "underlying_grade": "MODERATE", "names_company_directly": True})["grade"], "MODERATE")
        self.assertEqual(E.grade_event({**base, "underlying_grade": "WATCH", "names_company_directly": False})["grade"], "WATCH")

    def test_amendment_1_newly_graded_subcases_are_moderate_and_veto_entry(self):
        for t, sub in (("T1", "order_or_direction_without_fraud_finding_or_ban"), ("T2", "resignation_other_stated_reasons"),
                       ("T5", "named_fir")):
            g = E.grade_event(rec(t, sub, date(2018, 12, 1)))
            self.assertEqual((g["grade"], g["weak_source"]), ("MODERATE", False), (t, sub))
            self.assertTrue(E.entry_veto([g], [], date(2019, 3, 31))["blocked"])          # MODERATE vetoes entry
            px = F.weekly(date(2019, 3, 29), date(2020, 3, 27), lambda d: 100.0)
            late = E.grade_event(rec(t, sub, date(2019, 6, 1)))
            self.assertFalse(E.exit_scan(date(2019, 4, 5), F.D0, px, [late])["fired"])     # MODERATE never forces an exit

    def test_amendment_2_t6_underlying_moderate_downgrades_to_watch(self):
        base = dict(type="T6", subcase="associate_contagion", event_date=date(2018, 12, 1), sources=[{"tier": 2, "ref": "order"}])
        g = E.grade_event({**base, "underlying_grade": "MODERATE", "names_company_directly": False})
        self.assertEqual(g["grade"], "WATCH")
        self.assertFalse(E.entry_veto([g], [], date(2019, 3, 31))["blocked"])             # WATCH: log only, no veto
        px = F.weekly(date(2019, 3, 29), date(2020, 3, 27), lambda d: 100.0)
        self.assertFalse(E.exit_scan(date(2019, 4, 5), F.D0, px, [g])["fired"])


class Veto(unittest.TestCase):
    def graded(self, t="T3", sub="off_market_transfer_or_gift", d=date(2018, 10, 1), tier=1):
        return [E.grade_event(rec(t, sub, d, tier))]

    def test_severe_and_moderate_veto_watch_does_not(self):
        sev = self.graded("T3", "pledge_invocation")
        mod = self.graded()
        wat = [E.grade_event({"event_date": date(2018, 10, 1), "type": "WATCH", "subcase": "disclosure_lapse_no_order"})]
        for g, want in ((sev, True), (mod, True), (wat, False)):
            self.assertEqual(E.entry_veto(g, [], date(2019, 3, 31))["blocked"], want)

    def test_event_after_evaluation_date_is_ignored_pit(self):
        self.assertFalse(E.entry_veto(self.graded(d=date(2019, 4, 2)), [], date(2019, 3, 31))["blocked"])

    def test_evaluated_at_d0_and_again_at_each_fill_date(self):
        g = self.graded(d=date(2019, 6, 1))
        self.assertFalse(E.entry_veto(g, [], date(2019, 3, 31))["blocked"])        # clean at d0
        self.assertTrue(E.entry_veto(g, [], date(2019, 6, 7))["blocked"])          # event lands before the fill -> blocks that fill

    def test_no_print_on_record_keeps_block_indefinitely_and_logs_search(self):
        g = self.graded(d=date(2017, 1, 1))
        v = E.entry_veto(g, [], date(2019, 3, 31))                                  # >12m later, still blocked: no audited print
        self.assertTrue(v["blocked"])
        cool = v["hits"][0]["cooling_off"]
        self.assertTrue(cool["weak_source_search"])
        self.assertFalse(cool["search"]["valid"])

    def test_search_log_requires_two_named_sources_date_and_zero_hits(self):
        ok = {"sources": ["screener_results_calendar", "bse_nse_corporate_announcements"], "search_date": date(2019, 4, 1), "zero_hits": True}
        self.assertTrue(E.validate_search_log(ok)["valid"])
        self.assertFalse(E.validate_search_log({**ok, "sources": ["screener_results_calendar"]})["valid"])
        self.assertFalse(E.validate_search_log({**ok, "sources": ["screener_results_calendar", "screener_results_calendar"]})["valid"])
        self.assertFalse(E.validate_search_log({**ok, "zero_hits": False})["valid"])
        self.assertFalse(E.validate_search_log({**ok, "search_date": None})["valid"])
        self.assertFalse(E.validate_search_log(None)["valid"])

    def test_release_needs_both_results_date_and_fy_end_strictly_after_event(self):
        g = self.graded(d=date(2018, 4, 10))
        E_ = date(2019, 6, 1)
        fy_before = [{"results_date": date(2018, 8, 1), "fy_end": date(2018, 3, 31)}]        # (i) ok, (ii) fails
        self.assertTrue(E.entry_veto(g, fy_before, E_)["blocked"])
        both = [{"results_date": date(2018, 8, 1), "fy_end": date(2018, 6, 30)}]
        self.assertFalse(E.entry_veto(g, both, E_)["blocked"])
        late_print = [{"results_date": date(2019, 7, 1), "fy_end": date(2019, 3, 31)}]        # print lands after E: still blocked at E
        self.assertTrue(E.entry_veto(g, late_print, E_)["blocked"])
        self.assertFalse(E.entry_veto(g, late_print, date(2019, 7, 1))["blocked"])            # released the day the print publishes

    def test_release_is_later_of_12m_and_the_print(self):
        g = self.graded(d=date(2018, 4, 10))
        early = [{"results_date": date(2018, 5, 1), "fy_end": date(2018, 6, 30)}]
        self.assertTrue(E.entry_veto(g, early, date(2019, 4, 9))["blocked"])
        self.assertFalse(E.entry_veto(g, early, date(2019, 4, 10))["blocked"])

    def test_new_event_resets_the_clock(self):
        old = self.graded(d=date(2017, 1, 1))[0]
        new = E.grade_event(rec("T4", "withdrawn_buyback_dividend_or_fundraise", date(2019, 1, 15)))
        prints = [{"results_date": date(2017, 6, 1), "fy_end": date(2017, 3, 31)}]
        self.assertFalse(E.entry_veto([old], prints, date(2019, 3, 31))["blocked"])          # old event released
        self.assertTrue(E.entry_veto([old, new], prints, date(2019, 3, 31))["blocked"])      # new one blocks from its own date


class ExitScan(unittest.TestCase):
    FILL = date(2019, 4, 5)
    PX = F.weekly(date(2019, 3, 29), date(2021, 6, 4), lambda d: 100.0 + (d - date(2019, 3, 29)).days / 7)

    def sev(self, d, **kw):
        return {"event_date": d, "grade": "SEVERE", "type": "T5", **kw}

    def test_never_fired_is_an_observable_fact(self):
        s = E.exit_scan(self.FILL, F.D0, self.PX, [])
        self.assertEqual(s, {"fired": False, "exit_date": None, "exit_price": None, "triggering_event": None,
                             "note": "no SEVERE event in (fill, d0+24m]"})

    def test_moderate_and_watch_never_exit_and_pre_fill_events_are_out_of_scope(self):
        evs = [{"event_date": date(2019, 6, 1), "grade": "MODERATE", "type": "T1"},
               {"event_date": date(2019, 6, 2), "grade": "WATCH", "type": "WATCH"},
               self.sev(date(2019, 4, 5))]                                                    # event ON the fill date is not in (fill, wi]
        self.assertFalse(E.exit_scan(self.FILL, F.D0, self.PX, evs)["fired"])

    def test_exit_at_first_weekly_close_at_or_after_event_with_slippage(self):
        s = E.exit_scan(self.FILL, F.D0, self.PX, [self.sev(date(2019, 6, 1))])
        wi = next(d for d, _ in self.PX if d >= date(2019, 6, 1))
        self.assertEqual(s["exit_date"], wi.isoformat())
        self.assertEqual(s["triggering_event"], "T5 2019-06-01")
        self.assertAlmostEqual(s["exit_price_after_slippage"], s["exit_price"] * 0.99)

    def test_earliest_severe_event_triggers(self):
        s = E.exit_scan(self.FILL, F.D0, self.PX, [self.sev(date(2020, 1, 1)), self.sev(date(2019, 6, 1))])
        self.assertEqual(s["triggering_event"], "T5 2019-06-01")

    def test_scan_window_ends_at_d0_plus_24m(self):
        self.assertFalse(E.exit_scan(self.FILL, F.D0, self.PX, [self.sev(date(2021, 4, 5))])["fired"])   # d0 + 730d = 2021-03-30

    def test_last_print_rule_and_unexecuted_when_stale(self):
        px = [(d, p) for d, p in self.PX if d <= date(2019, 8, 30)]
        fresh = E.exit_scan(self.FILL, F.D0, px, [self.sev(date(2019, 9, 10))])
        self.assertEqual((fresh["fired"], fresh["exit_unexecuted"], fresh["exit_date"]), (True, False, "2019-08-30"))
        stale = E.exit_scan(self.FILL, F.D0, px, [self.sev(date(2019, 12, 1))])
        self.assertEqual((stale["fired"], stale["exit_unexecuted"], stale["exit_date"], stale["exit_price"]), (True, True, None, None))
        self.assertEqual(stale["last_print"], "2019-08-30")


if __name__ == "__main__":
    unittest.main()
