import unittest
from datetime import date, timedelta

from engine_v4 import distress as D
from engine_v4.tests import fixtures as F


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


class Screen(unittest.TestCase):
    def test_clean_name_passes_with_all_rules_logged(self):
        r = run()
        self.assertEqual((r["verdict"], r["label"]), ("PASS", "PASS"))
        self.assertEqual({k: v["status"] for k, v in r["rules"].items()},
                         {"D1": "PASS", "D2": "PASS", "D3": "PASS", "D4": "PASS", "D5": "PASS", "D6": "N/A"})
        self.assertEqual(r["raw_pledged_pct"], 0.0)

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
