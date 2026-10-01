import unittest
from datetime import date, timedelta

from engine_v5 import distress as D
from engine_v5.tests import fixtures as F


def fin_fy(**over):
    base = {"car_pct": 16.0, "gnpa_pct": 2.0, "cost_to_income_pct": 45.0, "roa_pct": 1.5, "casa_pct": 45.0,
            "leverage_x": 5.0, "results_published": date(2018, 5, 20)}
    base.update(over)
    return {2018: base}


def run(fy=None, sector="Consumer", prices=None, pledge=None, eq_flag=False, scoring_fy=2018):
    return D.evaluate(fy if fy is not None else F.fy_records(), scoring_fy, sector,
                      prices or F.flat_prices(), F.quarters() if pledge is None else pledge, F.D0, eq_flag)


class D1D2(unittest.TestCase):
    def test_equity_basis_is_normalised_to_promoter_holding(self):
        q = F.quarters(pledged=20.0)
        for x in q:
            x["basis"], x["promoter_holding_pct"] = "equity", 40.0          # 20% of equity / 40% promoter = 50% of promoter
        r = D.d1_pledge_level(q, F.D0)
        self.assertAlmostEqual(r["pledged_pct"], 50.0)
        self.assertEqual(r["status"], "TRIP")

    def test_missing_is_not_zero(self):
        self.assertEqual(D.d1_pledge_level([], F.D0)["status"], "UNCOMPUTABLE")
        q = F.quarters(); q[-1]["pledged_pct"] = None
        self.assertEqual(D.d1_pledge_level(q, F.D0)["status"], "UNCOMPUTABLE")
        self.assertEqual(D.d2_first_time_pledge(q, F.D0)["status"], "UNCOMPUTABLE")

    def test_uses_most_recent_quarter_on_or_before_d0(self):
        q = F.quarters(); q.append({"quarter_end": F.D0 + timedelta(days=91), "pledged_pct": 90.0, "promoter_holding_pct": 50.0})
        self.assertEqual(D.d1_pledge_level(q, F.D0)["status"], "PASS")       # future quarter ignored (PIT)

    def test_listed_already_pledging_is_not_first_time(self):
        q = F.quarters(12, 10.0)
        self.assertEqual(D.d2_first_time_pledge(q, F.D0)["status"], "PASS")   # D1 (level) is the only rule that applies


class D3D4(unittest.TestCase):
    def test_missing_component_is_uncomputable_and_negative_book_is_automatic(self):
        fy = F.fy_records(); fy[2018]["current_assets"] = None
        self.assertEqual(D.d3_altman(fy, 2018)["status"], "UNCOMPUTABLE")
        fy[2018]["reserves"], fy[2018]["equity_capital"] = -100.0, 50.0
        self.assertEqual(D.d3_altman(fy, 2018)["status"], "TRIP")             # even with another field missing

    def test_amendment_3_ca_cl_from_ar_unretrievable_is_uncomputable_data_veto(self):
        fy = F.fy_records(); fy[2018]["current_assets"] = fy[2018]["current_liabilities"] = None   # AR PDF not retrievable
        r = D.d3_altman(fy, 2018)
        self.assertEqual(r["status"], "UNCOMPUTABLE")
        self.assertIn("current_assets", r["reason"])
        full = run(fy)
        self.assertEqual((full["verdict"], full["label"]), ("STOP", "VETOED-DATA"))         # never a silent pass

    def test_revaluation_reserve_subtracted_only_when_disclosed(self):
        fy = F.fy_records()
        z0 = D.d3_altman(fy, 2018)["x"][1]
        fy[2018]["revaluation_reserve"] = 100.0
        z1 = D.d3_altman(fy, 2018)["x"][1]
        self.assertAlmostEqual(z0 - z1, 100.0 / fy[2018]["total_assets"])

    def test_ebit_is_pbt_plus_interest_plus_depreciation_as_written(self):
        fy = F.fy_records(); r = D.d3_altman(fy, 2018); y = fy[2018]
        self.assertAlmostEqual(r["x"][2], (y["pbt"] + y["interest"] + y["depreciation"]) / y["total_assets"])

    def test_piotroski_fail_closed_fallbacks_are_logged(self):
        fy = F.fy_records()
        for y in fy:
            fy[y]["current_assets"] = fy[y]["current_liabilities"] = None       # AR CA/CL not retrievable
            fy[y]["raw_material_pct"] = None                                     # no material cost, no raw-material %
        r = D.d4_piotroski(fy, 2018, False)
        self.assertEqual((r["components"]["F_dLIQUID"], r["components"]["F_dMARGIN"]), (0, 0))
        self.assertEqual(r["f"], 7)
        self.assertEqual(len(r["fail_closed_log"]), 2)

    def test_piotroski_material_cost_row_preferred_else_pct(self):
        fy = F.fy_records()
        for y in fy:
            fy[y]["material_cost"] = fy[y]["sales"] * 0.5                        # flat 50% -> margin not increased
        self.assertEqual(D.d4_piotroski(fy, 2018, False)["components"]["F_dMARGIN"], 0)

    def test_missing_prior_fy_delta_terms_score_zero(self):
        fy = {y: r for y, r in F.fy_records().items() if y >= 2017}             # no t-2
        r = D.d4_piotroski(fy, 2018, False)
        for k in ("F_dROA", "F_dLEVER", "F_dTURN"):
            self.assertEqual(r["components"][k], 0)

    def test_equity_issue_scores_zero_unless_solely_bonus_split(self):
        fy = F.fy_records(); fy[2018]["equity_capital"] = 60.0
        self.assertEqual(D.d4_piotroski(fy, 2018, True)["components"]["F_EQ"], 1)
        self.assertEqual(D.d4_piotroski(fy, 2018, False)["components"]["F_EQ"], 0)
        self.assertEqual(D.d4_piotroski(fy, 2018, None)["status"], "UNCOMPUTABLE")   # provenance missing -> never silent

    def test_missing_direct_field_is_uncomputable(self):
        fy = F.fy_records(); fy[2018]["cfo"] = None
        self.assertEqual(D.d4_piotroski(fy, 2018, False)["status"], "UNCOMPUTABLE")


class E1E5(unittest.TestCase):
    """§3.1 earnings-quality vetoes. Each is an independent hard veto; missing a required
    field is UNCOMPUTABLE-DATA (never a silent pass). Regression anchors are synthetic
    reconstructions of the Phase-1 catch table, documented as such."""

    def test_supremeeng_2020_sloan_spike_trips_e1(self):
        fy = F.fy_records()                                   # synthetic: FY19 PAT 6.76cr, CFO -16.66cr, Sloan +12.2%
        fy[2018]["net_profit"], fy[2018]["cfo"] = 6.76, -16.66
        fy[2018]["total_assets"] = (6.76 + 16.66) / 0.122
        r = D.e1_sloan(fy, 2018)
        self.assertAlmostEqual(r["sloan"], 0.122, places=3)
        self.assertEqual(r["status"], "TRIP")
        self.assertEqual(run(fy)["label"], "VETOED-DISTRESS:E1")   # first tripped rule owns attribution

    def test_e1_positive_only_cfo_above_ni_never_trips(self):
        fy = F.fy_records(); fy[2018]["cfo"] = 300.0           # (175.69-300)/2100 < 0
        self.assertEqual(D.e1_sloan(fy, 2018)["status"], "PASS")

    def test_e1_missing_is_vetoed_data(self):
        for fld in ("net_profit", "cfo", "total_assets"):
            fy = F.fy_records(); fy[2018][fld] = None
            self.assertEqual(run(fy)["label"], "VETOED-DATA", fld)

    def test_e2_two_year_cash_conversion_is_a_hard_veto(self):
        fy = F.fy_records(); fy[2017]["cfo"], fy[2018]["cfo"] = 40.0, 40.0
        self.assertEqual(run(fy)["label"], "VETOED-DISTRESS:E2")

    def test_e2_missing_prior_year_is_vetoed_data(self):
        fy = F.fy_records(); fy[2017]["net_profit"] = None
        self.assertEqual(D.e2_cash_conversion(fy, 2018)["status"], "UNCOMPUTABLE")

    def test_supremeeng_2021_interest_coverage_trips_e3(self):
        fy = F.fy_records()                                   # synthetic: EBIT/Interest = 1.49x (the 1.5x bar)
        fy[2018]["pbt"], fy[2018]["interest"] = 49.0, 100.0
        r = D.e3_interest_coverage(fy, 2018)
        self.assertAlmostEqual(r["interest_coverage"], 1.49)
        self.assertEqual(r["status"], "TRIP")
        # E3 trips but D3's EBITDA-like EBIT is untouched: the two definitions coexist as written
        self.assertNotEqual(r["interest_coverage"],
                            (fy[2018]["pbt"] + fy[2018]["interest"] + fy[2018]["depreciation"]) / fy[2018]["interest"])

    def test_e3_interest_zero_is_no_trip_not_uncomputable(self):
        fy = F.fy_records(); fy[2018]["interest"] = 0.0
        r = D.e3_interest_coverage(fy, 2018)
        self.assertEqual(r["status"], "PASS")
        self.assertIn("infinite", r["reason"])

    def test_e4_two_year_low_etr_trips_and_trap_case_does_not(self):
        fy = F.fy_records()
        fy[2018]["tax_expense"], fy[2017]["tax_expense"] = fy[2018]["pbt"] * 0.10, fy[2017]["pbt"] * 0.10
        self.assertEqual(run(fy)["label"], "VETOED-DISTRESS:E4")
        trap = F.fy_records()                                 # PBM-FY18 trap shape: NI > PBT
        trap[2018]["net_profit"], trap[2018]["pbt"], trap[2018]["tax_expense"] = 100.0, 80.0, 25.0
        self.assertEqual(D.e4_etr(trap, 2018)["status"], "PASS")   # 31.25% from the tax-expense line, never 1-NI/PBT

    def test_e4_pbt_nonpositive_is_non_trip_not_uncomputable(self):
        fy = F.fy_records(); fy[2018]["pbt"] = -1.0
        r = D.e4_etr(fy, 2018)
        self.assertEqual(r["status"], "PASS")
        self.assertIn("no trip", r["reason"])
        fy[2018]["tax_expense"] = None
        self.assertEqual(D.e4_etr(fy, 2018)["status"], "UNCOMPUTABLE")   # but missing tax_expense IS uncomputable

    def test_e5_receivables_days_and_yoy_are_hard_vetoes(self):
        fy = F.fy_records(); fy[2018]["receivables"] = 400.0             # 99.7 days > 90
        self.assertEqual(run(fy)["label"], "VETOED-DISTRESS:E5")
        fy2 = F.fy_records()
        fy2[2018]["receivables"], fy2[2017]["receivables"] = 262.0, 200.0   # +31% YoY, 65.3 days
        self.assertEqual(run(fy2)["label"], "VETOED-DISTRESS:E5")

    def test_e5_missing_receivables_is_vetoed_data(self):
        fy = F.fy_records(); fy[2018]["receivables"] = None
        self.assertEqual(run(fy)["label"], "VETOED-DATA")

    # ---- boundary + mutation-kill gap fills (W-test audit, 2026-10-01) ----
    def test_e2_cfo_at_exactly_half_ni_is_no_trip(self):
        # strict <: CFO == 0.5 x NI trips neither year (kills E2_CFO_PCT 0.5 -> 0.51)
        fy = F.fy_records()
        for y in (2017, 2018):
            fy[y]["net_profit"], fy[y]["cfo"] = 200.0, 100.0
        self.assertEqual(D.e2_cash_conversion(fy, 2018)["status"], "PASS")

    def test_e2_ratio_just_below_half_trips(self):
        # ratio 0.495: TRIP under 0.5, PASS under mutant 0.49 -> kills the downward mutant
        fy = F.fy_records()
        for y in (2017, 2018):
            fy[y]["net_profit"], fy[y]["cfo"] = 200.0, 99.0
        self.assertEqual(D.e2_cash_conversion(fy, 2018)["status"], "TRIP")

    def test_e4_etr_at_exactly_15_pct_is_no_trip(self):
        # strict <: 15.0% both years does NOT trip (kills E4_ETR_VETO_BELOW 0.15 -> 0.16)
        fy = F.fy_records()
        for y in (2017, 2018):
            fy[y]["tax_expense"] = fy[y]["pbt"] * 0.15
        r = D.e4_etr(fy, 2018)
        self.assertEqual(r["status"], "PASS")
        self.assertAlmostEqual(r["etr"][2018], 0.15)

    def test_e4_etr_just_below_15_pct_trips(self):
        # 14.5% both years: TRIP under 0.15, PASS under mutant 0.14
        fy = F.fy_records()
        for y in (2017, 2018):
            fy[y]["tax_expense"] = fy[y]["pbt"] * 0.145
        self.assertEqual(D.e4_etr(fy, 2018)["status"], "TRIP")

    def test_e5_days_at_exactly_90_is_no_trip(self):
        # strict >: exactly 90 days does NOT trip (kills E5_DAYS_VETO_ABOVE 90 -> 89)
        fy = F.fy_records(); fy[2018]["receivables"] = 90.0 * fy[2018]["sales"] / 365
        fy[2017]["receivables"] = fy[2018]["receivables"]          # silence the YoY leg (1.0x)
        r = D.e5_receivables_days(fy, 2018)
        self.assertEqual(r["days"], 90.0)
        self.assertEqual(r["status"], "PASS")

    def test_e5_days_just_above_90_trips(self):
        # 90.5 days: TRIP under 90, PASS under mutant 91
        fy = F.fy_records(); fy[2018]["receivables"] = 90.5 * fy[2018]["sales"] / 365
        fy[2017]["receivables"] = fy[2018]["receivables"]          # silence the YoY leg (1.0x)
        r = D.e5_receivables_days(fy, 2018)
        self.assertAlmostEqual(r["days"], 90.5)
        self.assertEqual(r["status"], "TRIP")

    def test_e5_yoy_just_below_131_trips(self):
        # YoY 1.305: TRIP under 1.30, PASS under mutant 1.31
        # (the existing yoy==1.30-exact PASS test kills the 1.29 mutant)
        fy = F.fy_records()
        fy[2018]["receivables"], fy[2017]["receivables"] = 261.0, 200.0
        fy[2018]["sales"] = 100000.0                             # silence the days leg (~0.95d)
        r = D.e5_receivables_days(fy, 2018)
        self.assertAlmostEqual(r["yoy"], 1.305)
        self.assertEqual(r["status"], "TRIP")

    def test_financial_variant_skips_e_rules_by_construction(self):
        r = run(fin_fy(), sector="Banks")
        for e in ("E1", "E2", "E3", "E4", "E5"):
            self.assertEqual(r["rules"][e]["status"], "N/A", e)
        self.assertEqual(r["e_rules"], "N/A (financial variant)")

    def test_e_trip_outranks_d3_uncomputable_in_attribution(self):
        fy = F.fy_records(); fy[2018]["current_assets"] = None       # D3 uncomputable
        fy[2018]["cfo"] = -60.0                                      # E1 trips
        r = run(fy)
        self.assertEqual(r["label"], "VETOED-DISTRESS:E1")
        self.assertIn("D3", r["uncomputable"])


class Screen(unittest.TestCase):
    def test_clean_name_passes_with_all_rules_logged(self):
        r = run()
        self.assertEqual((r["verdict"], r["label"]), ("PASS", "PASS"))
        self.assertEqual({k: v["status"] for k, v in r["rules"].items()},
                         {"D1": "PASS", "D2": "PASS", "E1": "PASS", "E2": "PASS", "E3": "PASS",
                          "E4": "PASS", "E5": "PASS", "D3": "PASS", "D4": "PASS", "D5": "PASS", "D6": "N/A"})
        self.assertEqual(r["raw_pledged_pct"], 0.0)
        self.assertEqual(r["e_rules"], "evaluated")

    def test_class_split_d3_d4_vs_d6(self):
        nonfin, fin = run(), run(fin_fy(), sector="Banks")
        self.assertEqual((nonfin["rules"]["D6"]["status"], nonfin["rules"]["D3"]["status"]), ("N/A", "PASS"))
        self.assertEqual((fin["rules"]["D3"]["status"], fin["rules"]["D4"]["status"], fin["rules"]["D6"]["status"]), ("N/A", "N/A", "PASS"))
        self.assertEqual(run(fin_fy(), sector="Finance")["class"], "financial")

    def test_pledge_and_crash_still_apply_to_financials(self):
        self.assertEqual(run(fin_fy(), "Banks", pledge=F.quarters(pledged=60.0))["label"], "VETOED-DISTRESS:D1")
        pts = F.weekly(date(2018, 3, 30), F.D0, lambda d: 100.0); pts[-1] = (pts[-1][0], 30.0)
        self.assertEqual(run(fin_fy(), "Banks", prices=pts)["label"], "VETOED-DISTRESS:D5")

    def test_all_tripped_rules_logged_first_in_d7_order_owns_attribution(self):
        q = F.quarters(pledged=60.0)                                              # D1 trips
        pts = F.weekly(date(2018, 3, 30), F.D0, lambda d: 100.0); pts[-1] = (pts[-1][0], 10.0)   # D5 trips
        fy = F.fy_records(); fy[2018]["reserves"] = -100.0                        # D3 trips (negative book)
        r = run(fy, prices=pts, pledge=q)
        self.assertEqual(r["tripped"], ["D1", "D3", "D5"])
        self.assertEqual(r["label"], "VETOED-DISTRESS:D1")

    def test_uncomputable_is_vetoed_data_never_a_silent_pass(self):
        r = run(pledge=[])
        self.assertEqual((r["verdict"], r["label"]), ("STOP", "VETOED-DATA"))
        self.assertIn("D1", r["uncomputable"])
        r = run(scoring_fy=None)
        self.assertEqual(r["label"], "VETOED-DATA")
        self.assertTrue({"D3", "D4"} <= set(r["uncomputable"]))

    def test_trip_outranks_data_label_but_data_defect_is_still_logged(self):
        fy = F.fy_records(); fy[2018]["current_assets"] = None                    # D3 uncomputable
        r = run(fy, pledge=F.quarters(pledged=90.0))                              # D1 trips
        self.assertEqual(r["label"], "VETOED-DISTRESS:D1")
        self.assertIn("D3", r["uncomputable"])

    def test_camel_missing_field_uncomputable_but_floor_still_evaluated(self):
        self.assertEqual(D.d6_camel(fin_fy(casa_pct=None), 2018, "Banks")["status"], "UNCOMPUTABLE")
        self.assertEqual(D.d6_camel(fin_fy(casa_pct=None, gnpa_pct=15.0), 2018, "Banks")["status"], "TRIP")
        # a Banks name needs CASA, a Finance name needs leverage; the other field is irrelevant
        self.assertEqual(D.d6_camel(fin_fy(leverage_x=None), 2018, "Banks")["status"], "PASS")
        self.assertEqual(D.d6_camel(fin_fy(casa_pct=None), 2018, "Finance")["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
