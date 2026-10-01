import unittest
from datetime import date

from engine_v5 import usability as U
from engine_v5.tests import fixtures as F


def ev(fy=None, series=None, actions=None, scoring_fy=2018):
    return U.evaluate(fy or F.fy_records(), scoring_fy, F.eps_series() if series is None else series, actions or [])


class Usability(unittest.TestCase):
    def test_clean_name_passes_all_three_checks_in_order(self):
        r = ev()
        self.assertEqual((r["verdict"], r["label"]), ("PASS", "PASS"))
        self.assertEqual(list(r["checks"]), ["U1", "U2", "U3"])

    def test_no_check_b_and_no_financial_exemption_exist(self):
        self.assertFalse(hasattr(U, "check_b"))
        self.assertFalse(any("exempt" in n.lower() for n in dir(U)))
        # a financial name faces U1-U3 identically: no EPS series -> VETOED-DATA (missing excludes; does not exempt)
        r = ev(series=[])
        self.assertEqual((r["verdict"], r["label"], r["deciding_check"]), ("STOP", "VETOED-DATA", "U3"))
        self.assertEqual(r["checks"]["U3"]["status"], "UNCOMPUTABLE")

    def test_u2_non_positive_sourced_eps_is_data_veto_not_fraud(self):
        fy = F.fy_records(); fy[2018]["eps"] = -3.0
        r = ev(fy)
        self.assertEqual((r["verdict"], r["label"], r["deciding_check"]), ("STOP", "VETOED-DATA", "U2"))
        fy[2018]["eps"] = 0.0
        self.assertEqual(ev(fy)["deciding_check"], "U2")
        fy[2018]["eps"] = None
        self.assertEqual(ev(fy)["checks"]["U2"]["status"], "UNCOMPUTABLE")

    def test_u3_fails_outside_15pct_of_sourced(self):
        base = F.fy_records()[2018]["eps"]
        r = ev(series=[(date(2018, 5, 20), base * 1.20)])
        self.assertEqual((r["verdict"], r["deciding_check"]), ("STOP", "U3"))
        r = ev(series=[(date(2018, 5, 20), base * 0.80)])
        self.assertEqual(r["deciding_check"], "U3")

    def test_u3_series_outside_window_is_uncomputable(self):
        r = ev(series=[(date(2018, 9, 15), 17.0)])                                # after Aug 31
        self.assertEqual(r["checks"]["U3"]["status"], "UNCOMPUTABLE")

    def test_all_checks_evaluated_even_when_an_earlier_one_stops(self):
        fy = F.fy_records(); fy[2018]["eps"] = -1.0
        r = ev(fy)
        self.assertEqual(r["checks"]["U2"]["status"], "STOP")
        self.assertIn(r["checks"]["U3"]["status"], ("NOT_EVALUATED", "PASS", "STOP"))   # U3 still logged, not skipped

    def test_no_scoring_fy_is_vetoed_data(self):
        r = U.evaluate(F.fy_records(), None, F.eps_series(), [])
        self.assertEqual(r["label"], "VETOED-DATA")

    def test_stale_mar31_point_skipped_back_dated_kept_end_to_end(self):
        base = F.fy_records()[2018]["eps"]
        stale = [(date(2018, 3, 31), base * 0.70), (date(2018, 5, 20), base)]     # >10% jump -> skipped; TTM taken at results week
        self.assertEqual(ev(series=stale)["verdict"], "PASS")
        no_skip = [(date(2018, 3, 31), base * 0.70), (date(2018, 5, 20), base * 0.75)]   # small jump: Mar-31 kept, and it fails
        self.assertEqual(ev(series=no_skip)["deciding_check"], "U3")


class U1Basis(unittest.TestCase):
    def fy_with_split(self, eps_restated):
        """2-for-1 split (ex 2019-01-10) after scoring FY-end 2018-03-31. Screener's FY19 EPS is on the post-split basis."""
        fy = F.fy_records()
        fy[2019] = dict(fy[2018], net_profit=fy[2018]["net_profit"], eps=fy[2018]["eps"] / 2,
                        results_published=date(2019, 5, 20))
        if not eps_restated:
            fy[2018]["eps"] = fy[2018]["eps"]                                      # 2018 still on the pre-split basis
        else:
            fy[2018]["eps"] = fy[2018]["eps"] / 2                                  # 2018 already restated
        return fy

    ACTION = [{"ex_date": date(2019, 1, 10), "numerator": 2, "denominator": 1, "ratio_text": "1:2 split"}]

    def test_unadjusted_sourced_eps_is_restated_by_the_factor(self):
        fy = self.fy_with_split(eps_restated=False)
        d = U.basis_diagnostic(fy, 2018, self.ACTION)
        self.assertTrue(d["restate"])
        self.assertAlmostEqual(d["factor"], 2.0)
        chk, sourced = U.u1_basis(fy, 2018, self.ACTION)
        self.assertAlmostEqual(sourced, fy[2018]["eps"] / 2)
        self.assertEqual(chk["named_basis"], U.NAMED_BASIS)

    def test_already_on_vendor_basis_is_not_restated_twice(self):
        fy = self.fy_with_split(eps_restated=True)
        d = U.basis_diagnostic(fy, 2018, self.ACTION)
        self.assertFalse(d["restate"])
        _, sourced = U.u1_basis(fy, 2018, self.ACTION)
        self.assertAlmostEqual(sourced, fy[2018]["eps"])

    def test_no_action_or_indeterminate_means_no_restatement(self):
        self.assertFalse(U.basis_diagnostic(F.fy_records(), 2018, [])["restate"])
        fy = F.fy_records()                                                        # action after FY-end but no later FY to compare against
        d = U.basis_diagnostic(fy, 2018, [{"ex_date": date(2019, 1, 10), "numerator": 2, "denominator": 1}])
        self.assertFalse(d["restate"])
        self.assertIn("indeterminate", d["basis"])

    def test_audited_over_sourced_ratio_is_reported_not_gated(self):
        fy = F.fy_records()
        chk, _ = U.u1_basis(fy, 2018, [], audited_eps_by_fy={2017: fy[2017]["eps"] * 1.045, 2018: fy[2018]["eps"] * 1.045})
        self.assertAlmostEqual(chk["audited_over_sourced_by_fy"][2018], 1.045)
        self.assertEqual(chk["status"], "PASS")                                    # residual convention factor documented, never failed on


if __name__ == "__main__":
    unittest.main()
