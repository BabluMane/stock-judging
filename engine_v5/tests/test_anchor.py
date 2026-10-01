import importlib.util, math, os, unittest
from datetime import date

from engine_v5 import anchor, constants as C
from engine_v5.tests import fixtures as F

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
V311 = os.path.join(REPO, "validation", "v3_11_oos", "run_v311_validation.py")


def load_v311():
    spec = importlib.util.spec_from_file_location("run_v311_validation", V311)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def as_screener(fy, years):
    """Render our FY dict in the screener-table shape the frozen v3.11 runner reads (synthetic)."""
    cols = [f"Mar {y}" for y in years]
    row = lambda f: [str(fy[y].get(f)) if fy[y].get(f) is not None else "" for y in years]
    return {"x": {
        "profit_loss": {"years": cols, "rows": {"Net Profit&nbsp;+": row("net_profit"), "Dividend Payout %": row("dividend_payout_pct"),
                                                "Sales&nbsp;+": row("sales"), "OPM %": row("opm_pct"), "Depreciation": row("depreciation")}},
        "balance_sheet": {"years": cols, "rows": {"Equity Capital": row("equity_capital"), "Reserves": row("reserves")}}}}


class CarriedParity(unittest.TestCase):
    """The 'carried' pieces (g_sus C1-C5, margin, dep) must equal the frozen v3.11 runner's functions
    on the same synthetic tables. Synthetic data only: no prior validation set is re-run."""

    def setUp(self):
        self.v = load_v311()
        self.v.SECTOR_BETA["x"] = 1.0

    def check(self, fy):
        years = sorted(fy)
        fin = as_screener(fy, years)
        ref, _ = self.v.sustainable_growth(fin, "x", f"Mar {years[-1]}")
        mine, _ = anchor.sustainable_growth(fy, years[-1])
        self.assertAlmostEqual(ref["g"], mine["g_sus"], places=12)
        self.assertAlmostEqual(ref["roe_avg3"], mine["roe_avg3"], places=12)
        self.assertEqual(ref["g_cap_binding"], mine["cap_binding"])
        di, _ = self.v.dcf_inputs(fin, "x", f"Mar {years[-1]}")
        mi, _ = anchor.dcf_inputs(fy, years[-1], 1.0)
        self.assertAlmostEqual(di["margin_end"], mi["margin"], places=12)
        self.assertAlmostEqual(di["dep_pct"], mi["dep_pct"], places=12)
        self.assertAlmostEqual(di["rev0"], mi["rev0"], places=12)

    def test_plain(self):
        self.check(F.fy_records())

    def test_cap_binding_and_payout_over_100(self):
        fy = F.fy_records()
        for y in fy:
            fy[y]["net_profit"] = 500.0
        fy[2018]["dividend_payout_pct"] = 130.0
        self.check(fy)

    def test_negative_book_and_zero_book_year_skipped(self):
        fy = F.fy_records()
        fy[2016]["equity_capital"], fy[2016]["reserves"] = 50.0, -50.0       # zero book -> skipped (C5)
        fy[2017]["reserves"] = -900.0                                        # negative book computed literally
        self.check(fy)

    def test_fewer_than_three_and_five_years(self):
        fy = {y: r for y, r in F.fy_records().items() if y >= 2017}          # 2 FYs: C4 mean of available
        self.check(fy)

    def test_missing_opm_series_uses_latest_then_fallback(self):
        fy = F.fy_records()
        for y in (2014, 2015, 2016):
            fy[y]["opm_pct"] = None                                          # 2 points -> latest, not mean
        fy[2017]["opm_pct"], fy[2018]["opm_pct"] = 10.0, 30.0
        self.check(fy)


class Structure(unittest.TestCase):
    def test_cancellation_is_auditable(self):
        v, _ = anchor.dcf_inputs(F.fy_records(), 2018, 1.0)
        for g in (-0.3, 0.0, 0.04, 0.15):
            anchor.enterprise_value(v, v["w"], g, audit=True)                # asserts long form == cancelled form each year

    def test_gordon_closed_form_at_terminal_growth(self):
        """g = TG => r_t and FCFF_t both grow at exactly TG, so EV = FCFF_1 / (w - TG)."""
        v = {"rev0": 1000.0, "margin": 0.20, "dep_pct": 0.03}
        w = 0.11
        r1 = 1000 * 1.04
        f1 = r1 * (0.20 - 0.03) * (1 - C.TAX) - (r1 - 1000) * C.WC_PCT
        self.assertAlmostEqual(anchor.enterprise_value(v, w, 0.04), f1 / (w - 0.04), places=8)

    def test_value_monotone_in_growth_for_positive_margin(self):
        v, _ = anchor.dcf_inputs(F.fy_records(), 2018, 1.0)
        vals = [anchor.enterprise_value(v, v["w"], g / 100) for g in range(-50, 10)]
        self.assertTrue(all(b > a for a, b in zip(vals, vals[1:])))

    def test_negative_g_uses_fade_up_to_tg(self):
        gp = anchor.growth_path(-0.10)
        self.assertAlmostEqual(gp[14], -0.10 + (0.04 + 0.10) * 5 / 10)

    def test_triggers_ordered_and_scale_nonlinearly(self):
        a = anchor.value_anchor(F.fy_records(), 2018, False, 1.0, 10000.0, 100.0, 100.0)
        self.assertTrue(a["valued"])
        self.assertLess(a["trigger"]["G2"], a["trigger"]["G1"])
        self.assertLess(a["trigger"]["G1"], a["v_at_g_sus"])
        # V(0.875 g) != 0.875 V(g): triggers are recomputed through the structure, never scaled
        self.assertNotAlmostEqual(a["trigger"]["G1"], 0.875 * a["v_at_g_sus"], places=3)

    def test_implied_growth_is_consistent_with_price_and_reporting_only(self):
        a = anchor.value_anchor(F.fy_records(), 2018, False, 1.0, 10000.0, 100.0, 40.0)
        imp = a["implied"]
        self.assertEqual(imp["status"], "solved")
        v, _ = anchor.dcf_inputs(F.fy_records(), 2018, 1.0)
        nc = 50.0 - 120.0
        px = (anchor.enterprise_value(v, v["w"], imp["g_implied"]) + nc) / 100.0
        self.assertAlmostEqual(px, 40.0, places=6)
        # decision is the trigger comparison, identical to g_implied <= g_h(k) where V is monotone
        self.assertEqual(40.0 <= a["trigger"]["G1"], imp["g_implied"] <= a["hurdle_growth"]["G1"])
        self.assertEqual(40.0 <= a["trigger"]["G2"], imp["g_implied"] <= a["hurdle_growth"]["G2"])

    def test_not_valued_paths(self):
        fy = F.fy_records()
        self.assertFalse(anchor.value_anchor(fy, None, False, 1.0, 1.0, 1.0, 1.0)["valued"])
        self.assertFalse(anchor.value_anchor(fy, 2018, False, 1.0, None, 100.0, 100.0)["valued"])
        neg = F.fy_records(); neg[2018]["sales"] = 0.0
        self.assertIn("revenue", anchor.value_anchor(neg, 2018, False, 1.0, 1.0, 1.0, 1.0)["reason"])
        degenerate = anchor.value_anchor(fy, 2018, False, -1.0, 1.0, 1.0, 1.0)     # w = 2.95% <= TG+0.5pp
        self.assertFalse(degenerate["valued"])
        self.assertIn("degenerate", degenerate["reason"])

    def test_cap_sensitivity_is_reporting_only(self):
        fy = F.fy_records()
        for y in fy:
            fy[y]["net_profit"] = 400.0
        base = anchor.value_anchor(fy, 2018, False, 1.0, 10000.0, 100.0, 100.0)
        alt = anchor.value_anchor(fy, 2018, False, 1.0, 10000.0, 100.0, 100.0, g_cap=0.20)
        self.assertEqual(base["g_sus"], 0.15)
        self.assertGreater(alt["g_sus"], 0.15)
        again = anchor.value_anchor(fy, 2018, False, 1.0, 10000.0, 100.0, 100.0)
        self.assertEqual(again["trigger"], base["trigger"])                        # default path unaffected


class FinancialVariant(unittest.TestCase):
    def fin_fy(self):
        fy = F.fy_records()
        return fy

    def test_formula_matches_literal_spec(self):
        book0, roe, w, g, sh = 1000.0, 0.15, 0.10, 0.08, 10.0
        pv, b = book0, book0
        for t in range(1, 21):
            roe_t = roe + (w - roe) * t / 20
            pv += (roe_t - w) * b / (1 + w) ** t
            b *= 1 + g
        pv += b / (1 + w) ** 20
        self.assertAlmostEqual(anchor.excess_return_value(book0, roe, w, g, sh), pv / sh, places=9)

    def test_roe_equal_w_gives_zero_excess_and_terminal_book(self):
        v = anchor.excess_return_value(1000.0, 0.10, 0.10, 0.0, 1.0)
        self.assertAlmostEqual(v, 1000.0 + 1000.0 / 1.10 ** 20)

    def test_financial_anchor_valued_with_same_hurdle_mechanics(self):
        a = anchor.value_anchor(self.fin_fy(), 2018, True, 1.0, 10000.0, 100.0, 100.0)
        self.assertTrue(a["valued"])
        self.assertEqual(a["model"], "inverse excess-return 20y")
        self.assertAlmostEqual(a["book0_cr"], 50.0 + 900.0)                        # equity capital + reserves at scoring FY
        self.assertLess(a["trigger"]["G2"], a["trigger"]["G1"])

    def test_financial_needs_scoring_fy_book(self):
        fy = self.fin_fy(); fy[2018]["reserves"] = None
        a = anchor.value_anchor(fy, 2018, True, 1.0, 10000.0, 100.0, 100.0)
        self.assertFalse(a["valued"])


class Certification(unittest.TestCase):
    def test_fill_plausible(self):
        self.assertTrue(anchor.fill_plausible(100.0, 50.0))
        self.assertFalse(anchor.fill_plausible(100.01, 50.0))


if __name__ == "__main__":
    unittest.main()
