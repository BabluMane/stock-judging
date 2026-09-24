#!/usr/bin/env python3
"""Unit tests for engine v3 (spec §9 item 18). Run:  python3 -m unittest test_engine_v3 -v"""

import copy, json, math, os, unittest
import engine_v3 as E

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = json.load(open(os.path.join(HERE, "sample_input_v3.json")))
M_IN = E.MACRO["IN"]


def inp(**changes):
    d = copy.deepcopy(BASE)
    for path, val in changes.items():
        cur = d
        keys = path.split("__")
        for k in keys[:-1]:
            cur = cur.setdefault(k, {})
        if val is DELETE:
            cur.pop(keys[-1], None)
        else:
            cur[keys[-1]] = val
    return d


DELETE = object()


class Interpolation(unittest.TestCase):
    def test_exact_threshold_is_midpoint(self):
        self.assertEqual(E.ladder(0.12, [0.08, 0.12], [0, 1, 2]), 1.5)

    def test_band_edges_and_outside(self):
        self.assertEqual(E.ladder(0.108, [0.08, 0.12], [0, 1, 2]), 1.0)    # 0.9T
        self.assertEqual(E.ladder(0.132, [0.08, 0.12], [0, 1, 2]), 2.0)    # 1.1T
        self.assertEqual(E.ladder(0.10, [0.08, 0.12], [0, 1, 2]), 1.0)     # between bands
        self.assertEqual(E.ladder(0.05, [0.08, 0.12], [0, 1, 2]), 0.0)

    def test_birlasoft_knife_edge_smoothed(self):
        # r_val + 5pp = 19.87%; ROCE 19.80% -> ~1.5, not a 1-vs-2 cliff
        s = E.ladder(0.1980, [0.1487, 0.1987], [0, 1, 2])
        self.assertTrue(1.4 <= s <= 1.6, s)

    def test_monotone_across_range(self):
        xs = [i / 1000 for i in range(0, 300)]
        ys = [E.ladder(x, [0.08, 0.12], [0, 1, 2]) for x in xs]
        self.assertTrue(all(b >= a for a, b in zip(ys, ys[1:])))

    def test_lower_better_and_pp_mode(self):
        # A3 margin range: <=5pp = 2, <=10pp = 1; +-1pp band
        self.assertEqual(E.ladder(0.03, [0.05, 0.10], [0, 1, 2], higher_better=False, mode="pp"), 2.0)
        self.assertEqual(E.ladder(0.05, [0.05, 0.10], [0, 1, 2], higher_better=False, mode="pp"), 1.5)
        s = E.ladder(0.055, [0.05, 0.10], [0, 1, 2], higher_better=False, mode="pp")
        self.assertTrue(1.0 < s < 1.5, s)
        self.assertEqual(E.ladder(0.061, [0.05, 0.10], [0, 1, 2], higher_better=False, mode="pp"), 1.0)
        self.assertEqual(E.ladder(0.12, [0.05, 0.10], [0, 1, 2], higher_better=False, mode="pp"), 0.0)

    def test_bands_never_overlap(self):
        # thresholds 1.0 and 1.05: bands capped at half the gap
        self.assertEqual(E.ladder(1.025, [1.0, 1.05], [0, 1, 2]), 1.0)

    def test_E4_discrete_25pct_scores_2(self):
        r = E.run(inp())
        self.assertEqual(r["tests_today"]["E4"], 2.0)


class TerminalFCFF(unittest.TestCase):
    def v(self, **k):
        v = copy.deepcopy(BASE["valuation"]); v.update(k); return v

    def test_normalised_fcff_uses_terminal_growth_and_maintenance_capex(self):
        v = self.v(growth=0.20)
        val, meta = E.dcf_value(v, 0.11, M_IN, detail=True)
        r5 = v["revenue"] * 1.20 ** 5
        tax = max(v["tax"], M_IN["tax_floor"])
        tg = 0.04
        expect = r5 * (v["margin_end"] - v["dep_pct"]) * (1 - tax) - r5 * tg / (1 + tg) * v["wc_pct"]
        self.assertAlmostEqual(meta["fcff_norm_y5"], round(expect, 2), places=1)
        # independent of explicit-period growth given the same year-5 revenue (v2 charged WC at explicit growth)
        self.assertNotAlmostEqual(meta["fcff_norm_y5"], meta["explicit_fcff"][-1], places=0)

    def test_gordon_equals_long_explicit_projection(self):
        v = self.v()
        w = 0.11
        val, meta = E.dcf_value(v, w, M_IN, detail=True)
        tg = meta["terminal_g"]
        r5 = meta["year5_revenue"]
        tax = max(v["tax"], M_IN["tax_floor"])
        pv_at5 = 0.0
        r = r5
        for t in range(1, 3000):
            prev = r; r = prev * (1 + tg)
            fcff = r * (v["margin_end"] - v["dep_pct"]) * (1 - tax) - (r - prev) * v["wc_pct"]
            pv_at5 += fcff / (1 + w) ** t
        self.assertAlmostEqual(pv_at5 / meta["tv"], 1.0, places=4)

    def test_terminal_g_hard_cap(self):
        v = self.v(terminal_g=0.06)
        _, meta = E.dcf_value(v, 0.11, M_IN, detail=True)
        self.assertEqual(meta["terminal_g"], 0.04)

    def test_terminal_g_default_4pct(self):
        v = self.v(); v.pop("terminal_g")
        _, meta = E.dcf_value(v, 0.11, M_IN, detail=True)
        self.assertEqual(meta["terminal_g"], 0.04)

    def test_degenerate_when_w_le_g(self):
        self.assertIsNone(E.dcf_value(self.v(), 0.043, M_IN))


class Solver(unittest.TestCase):
    def setUp(self):
        self.R = E.rates(inp(), M_IN)

    def test_solution_reproduces_price(self):
        v = BASE["valuation"]
        rd = E.reverse_dcf(v, 950.0, self.R, M_IN)
        t = dict(v); t["growth"] = rd["implied_growth"] / 100
        self.assertAlmostEqual(E.dcf_value(t, self.R["wacc_val"], M_IN), 950.0, delta=0.5)

    def test_scan_solver_takes_rising_side_of_a_hump(self):
        hump = lambda x: 100 - 1000 * (x - 0.30) ** 2      # rises to 0.30, then falls
        x, info = E._scan_solve(hump, 60.0, -0.20, 0.60)
        self.assertFalse(info["monotone"])
        self.assertAlmostEqual(info["turning_point"], 0.30, places=2)
        self.assertLess(x, 0.30)                              # rising-side root, not the falling one
        self.assertAlmostEqual(hump(x), 60.0, places=4)
        x2, info2 = E._scan_solve(hump, 120.0, -0.20, 0.60)  # above the peak: unsolvable
        self.assertIsNone(x2)
        self.assertIn("maximum", info2["reason"])

    def test_growth_destroying_value_is_unsolvable_and_restated(self):
        # heavy working capital: value FALLS with growth (incremental returns < WACC). v2's bisection assumed
        # an increasing function and returned a bound; v3 refuses the falling segment and restates twice.
        v = dict(BASE["valuation"]); v["wc_pct"] = 2.5
        f = lambda x: E.dcf_value({**v, "growth": x}, self.R["wacc_val"], M_IN)
        self.assertGreater(f(-0.10), f(0.10))
        rd = E.reverse_dcf(v, f(0.0), self.R, M_IN)
        self.assertTrue(rd["unsolvable_on_growth"])
        self.assertIsNotNone(rd["implied_terminal_margin"])
        self.assertIsNotNone(rd["implied_wacc"])

    def test_bounds_are_sane(self):
        self.assertEqual(E.GROWTH_BOUNDS, (-0.20, 0.60))


class Forensics(unittest.TestCase):
    def test_unverified_excluded_not_zeroed(self):
        r = E.run(inp(financials__contingent_liabilities=None))
        fx = r["forensic"]
        self.assertIn(5, fx["unverified"])
        self.assertEqual(fx["verified"], 9)
        self.assertEqual(fx["B"], round(10 * fx["passes"] / 9, 2))

    def test_check3_tests_both_limbs(self):
        d = inp()   # days +5 (limb 1 pass) but receivables 46% > revenue 43% (limb 2 fail)
        c3 = next(c for c in E.run(d)["forensic"]["checks"] if c["n"] == 3)
        self.assertEqual(c3["result"], "fail")
        d = inp(financials__receivables_growth_3y=None)
        c3 = next(c for c in E.run(d)["forensic"]["checks"] if c["n"] == 3)
        self.assertEqual(c3["result"], "unverified")

    def test_check9_pledge_materiality_floor(self):
        d = inp(pledge__pledge_pct_shares=0.000035)   # 0.0035% — failed under v2
        c9 = next(c for c in E.run(d)["forensic"]["checks"] if c["n"] == 9)
        self.assertEqual(c9["result"], "pass")
        d = inp(pledge__pledge_pct_shares=0.006)
        c9 = next(c for c in E.run(d)["forensic"]["checks"] if c["n"] == 9)
        self.assertEqual(c9["result"], "fail")

    def test_coverage_cap_when_verified_below_7(self):
        d = inp(financials__contingent_liabilities=None, financials__rpt_total=None,
                financials__dep_rate_start=None, financials__cash_yield=None)
        r = E.run(d)
        self.assertEqual(r["forensic"]["verified"], 6)
        self.assertEqual(r["forensic"]["gate_G1"], "COVERAGE")
        self.assertTrue(r["tier"].startswith("WATCH"))
        self.assertIn("promotion_condition", r)

    def test_G1_fails_when_no_retrieval_could_clear_it(self):
        d = inp(financials__cfo_pat_5y_avg=0.5, financials__other_income=200, auditor__reputable=False,
                financials__contingent_liabilities=None, financials__rpt_total=None,
                financials__dep_rate_start=None, financials__cash_yield=None)
        d["financials"]["cumulative"]["cfo"] = 500   # fail 1
        r = E.run(d)
        self.assertEqual(r["forensic"]["fails"], 5)
        self.assertEqual(r["forensic"]["gate_G1"], "FAIL")
        self.assertTrue(r["tier"].startswith("PASS"))

    def test_G1_pass_rate_rule(self):
        d = inp(financials__cfo_pat_5y_avg=0.5, financials__other_income=200)
        d["financials"]["cumulative"]["cfo"] = 500
        r = E.run(d)   # fails: 1, 2, 3, 4 -> 6/10 = 60% -> clears
        self.assertEqual(r["forensic"]["gate_G1"], "pass")
        d["financials"]["contingent_liabilities"] = 900   # 5/10 = 50%
        self.assertEqual(E.run(d)["forensic"]["gate_G1"], "FAIL")

    def test_check_verification_fills_but_never_contradicts(self):
        d = inp(financials__contingent_liabilities=None, check_verification={"5": "pass"})
        c5 = next(c for c in E.run(d)["forensic"]["checks"] if c["n"] == 5)
        self.assertEqual(c5["result"], "pass")
        d = inp(check_verification={"1": "fail"})
        with self.assertRaises(E.RenderRefused):
            E.run(d)


class RatesAndInputs(unittest.TestCase):
    def test_r_val_formula(self):
        R = E.rates(inp(), M_IN)
        self.assertAlmostEqual(R["r_val"], 0.0695 + 0.95 * 0.04)

    def test_net_debt_structure_derived_not_all_equity(self):
        d = inp(valuation__net_cash=-3000)
        R = E.rates(d, M_IN)
        self.assertGreater(R["debt_wt"], 0.2)
        self.assertLess(R["wacc_val"], R["r_val"])
        self.assertIn("derived", R["capital_structure"])

    def test_net_cash_stays_all_equity(self):
        R = E.rates(inp(valuation__debt_wt=0.3), M_IN)
        self.assertEqual(R["debt_wt"], 0.0)

    def test_beta_never_assumed(self):
        with self.assertRaises(E.RenderRefused):
            E.run(inp(valuation__beta=DELETE))
        with self.assertRaises(E.RenderRefused):
            E.run(inp(valuation__beta_source=DELETE))
        with self.assertRaises(E.RenderRefused):
            E.run(inp(valuation__beta_obs=30))

    def test_bear_weight_from_triggers(self):
        self.assertEqual(E.bear_weight({"bear_triggers": []})[0], 0.25)
        self.assertAlmostEqual(E.bear_weight({"bear_triggers": ["a", "b", "c"]})[0], 0.40)
        self.assertEqual(E.bear_weight({"bear_triggers": list("abcdefg")})[0], 0.45)
        with self.assertRaises(E.RenderRefused):
            E.bear_weight({})

    def test_scenario_weights_sum_to_one(self):
        ss = E.scenario_set(inp(bear_triggers=["x", "y"]))
        self.assertAlmostEqual(sum(c["weight"] for c in ss["cases"]), 1.0, places=6)
        self.assertAlmostEqual(ss["cases"][0]["weight"], 0.35)


class Scoring(unittest.TestCase):
    def test_D1_bands(self):
        R = E.rates(inp(), M_IN)
        dcfb = {"usable": True, "central": 100.0}
        f = lambda px: E.score_price_tests(inp(scenarios=[]), px, R, M_IN, dcfb, None, None)[0]["D1"]
        self.assertEqual(f(75), 2.0)    # 25% below
        self.assertEqual(f(85), 1.0)    # 15% below — the v2 gap, now 1
        self.assertEqual(f(105), 1.0)   # within +-10%
        self.assertEqual(f(115), 0.0)   # >10% above

    def test_D1_zero_on_negative_dcf(self):
        R = E.rates(inp(), M_IN)
        s = E.score_price_tests(inp(scenarios=[]), 50, R, M_IN, {"usable": False, "central": -20}, None, None)[0]
        self.assertEqual(s["D1"], 0.0)

    def test_D3_middle_band(self):
        R = E.rates(inp(), M_IN)
        d = inp(scenarios=[], financials__revenue_cagr_5y=0.10, financials__guided_growth=0.25)
        f = lambda ig: E.score_price_tests(d, 100, R, M_IN, None, {"implied_growth": ig}, None)[0]["D3"]
        self.assertEqual(f(8.0), 2.0)
        self.assertEqual(f(15.0), 1.0)   # above delivered, <= 0.7 x 25% = 17.5%
        self.assertEqual(f(22.0), 0.0)
        self.assertEqual(E.score_price_tests(d, 100, R, M_IN, None, {"unsolvable_on_growth": True}, None)[0]["D3"], 0.0)

    def test_D4_missing_median_is_neutral_1(self):
        r = E.run(inp(valuation__pe_10y_median=DELETE))
        self.assertEqual(r["tests_today"]["D4"], 1.0)

    def test_F5_skip_rescales_F(self):
        r = E.run(inp())
        t = r["tests_today"]
        self.assertAlmostEqual(r["dims_today"]["F"], round(sum(t[f"F{i}"] for i in range(1, 5)) / 8 * 10, 2))
        with self.assertRaises(E.RenderRefused):
            E.run(inp(mode="full", c5_mode="full"))

    def test_C5_lite_weights(self):
        sc, info = E.credibility(inp(), "lite")
        self.assertEqual(sc, 8.0)       # (2*4 + 1*3 + 2*2 + 1*1) / (2*10) * 10
        self.assertEqual(info["weights"], [4, 3, 2, 1])

    def test_C6_direction(self):
        R = E.rates(inp(), M_IN)
        fx = {"verified": 10}
        f = lambda x, v=None: E.score_fixed_tests(inp(pit={"net_buy_mcap_pct": x, "net_buy_value": v}), R, M_IN, fx,
                                                   {"sessions": 1}, "screen")[0]["C6"]
        self.assertEqual(f(0.02), 2.0)
        self.assertEqual(f(0.0), 1.0)
        self.assertEqual(f(-0.01), 0.0)
        self.assertEqual(f(0.001, 80.0), 2.0)    # > Rs 50 Cr limb


class Integrity(unittest.TestCase):
    def test_dimension_mismatch_refuses(self):
        tests = {f"{d}{i}": 1.0 for d, n in E.TEST_COUNT.items() for i in range(1, n + 1)}
        dims, _ = E.dimensions(tests, 8.0, False)
        dims["A"] = 9.99
        with self.assertRaises(E.RenderRefused):
            E.validate_dims(tests, dims, False)

    def test_claimed_numbers_must_match(self):
        r = E.run(inp())
        with self.assertRaises(E.RenderRefused):
            E.run(inp(claimed={"Q": r["Q"] + 0.3}))
        E.run(inp(claimed={"Q": r["Q"], "A": r["dims_today"]["A"]}))   # matching claims render

    def test_engine_only_tests_cannot_be_overridden(self):
        with self.assertRaises(E.RenderRefused):
            E.run(inp(manual_scores={**BASE["manual_scores"], "D1": 2}))

    def test_manual_score_range(self):
        with self.assertRaises(E.RenderRefused):
            E.run(inp(manual_scores={**BASE["manual_scores"], "A4": 3}))


class TierAndTrigger(unittest.TestCase):
    def test_trigger_is_value_at_hurdle(self):
        r = E.run(inp(gates={"G2": "pass", "G4": "pass", "G5": "pass"}))
        v = BASE["valuation"]
        self.assertAlmostEqual(r["trigger"]["trigger"], E.dcf_value(v, 0.15, M_IN), places=1)
        self.assertLess(r["trigger"]["trigger"], r["dcf"]["central"])

    def test_invest_at_trigger_needs_defensible_trigger(self):
        self.assertEqual(E.tier_rule(6.5, [], [], False, None, 100), "WATCH (capped: no defensible trigger)")
        self.assertEqual(E.tier_rule(6.5, [], [], False, 80.0, 100), "INVEST AT TRIGGER")

    def test_tier_table(self):
        self.assertEqual(E.tier_rule(7.2, [], [], False, 120.0, 100), "INVEST NOW")
        self.assertEqual(E.tier_rule(7.2, [], [], False, 80.0, 100), "INVEST AT TRIGGER")
        self.assertEqual(E.tier_rule(5.5, [], [], False, 80.0, 100), "WATCH")
        self.assertEqual(E.tier_rule(4.9, [], [], False, 80.0, 100), "PASS")
        self.assertTrue(E.tier_rule(8.0, ["G2"], [], False, 80.0, 100).startswith("PASS"))
        self.assertTrue(E.tier_rule(8.0, [], [], True, 80.0, 100).startswith("WATCH"))

    def test_negative_dcf_no_trigger_watch_cap(self):
        d = inp(valuation__margin_start=0.02, valuation__margin_end=0.02,
                gates={"G2": "pass", "G4": "pass", "G5": "pass"})
        r = E.run(d)
        self.assertFalse(r["dcf"]["usable"])
        self.assertIsNone(r["trigger"]["trigger"])
        self.assertEqual(r["tests_today"]["D1"], 0.0)
        self.assertFalse(r["tier"].startswith("INVEST"))

    def test_full_sample_invest_at_trigger(self):
        r = E.run(inp(gates={"G2": "pass", "G5": "pass"}))
        self.assertEqual(r["gates"]["G4"][:4], "pass")
        self.assertEqual(r["tier"], "INVEST AT TRIGGER")
        self.assertIsNotNone(r["P_trigger"]); self.assertIsNotNone(r["P_today"])
        self.assertGreater(r["P_trigger"], r["P_today"])


class Jurisdictions(unittest.TestCase):
    def test_usa_macro(self):
        d = inp(jurisdiction="US")
        d["market"] = {"median_daily_dollar_value_usd": 5e7}
        d["ownership"].pop("median_daily_value")
        d["financials"].update({"cfo_ni_5y_avg": 0.9, "dso_start": 50, "dso_end": 52, "nonoperating_income": 10,
                                "pretax_income": 400, "contingencies": 50, "equity": 2400,
                                "diluted_shares_cagr_3y": 0.0, "sbc_pct_cfo": 0.05})
        d["auditor"] = {"name": "X", "opinion": "unqualified", "material_weakness": False,
                        "change_with_disagreement_3y": False, "restatement_4_02_3y": False,
                        "audit_fee_growth_3y": 0.1, "revenue_growth_3y": 0.4,
                        "going_concern": False, "ifc_qualified_2y": False, "resignation": False}
        d["manual_scores"]["C1"] = 2
        r = E.run(d)
        self.assertAlmostEqual(r["rates"]["r_val"], round(0.0496 + 0.95 * 0.04, 4))
        self.assertEqual(r["calibration"], "USA-cal v3.0")
        self.assertEqual(r["forensic"]["variant"], "US 10-check")

    def test_v2_engine_still_runs(self):
        import engine_v2
        with open(os.path.join(HERE, "sample_input_v2.json")) as fh:
            d = json.load(fh)
        r = engine_v2.run(d)
        self.assertEqual(r["scorecard"]["composite"], 7.1)


class AuditRegressions(unittest.TestCase):
    """Bugs found by the independent audit of 23 Sep 2026 — each must stay fixed."""

    def fin(self, **val):
        d = inp(sector_variant="financial", forensic_fs=[{"n": i, "check": f"c{i}", "result": "pass"} for i in range(1, 9)])
        d["valuation"] = {"beta": 1.0, "beta_source": "industry", "conservative_central": 700,
                          "conservative_range": [600, 800], "hurdle_price": 500, "multiples_range": [820, 1110], **val}
        return d

    def test_financial_variant_runs(self):
        r = E.run(self.fin())
        self.assertEqual(r["trigger"]["trigger"], 500)
        self.assertEqual(r["forensic"]["variant"], "financial 8-check")
        self.assertTrue(r["tier"].startswith("incomplete"))       # D3 (implied vs delivered ROTCE) is manual here
        d = self.fin(); d["manual_scores"]["D3"] = {"today": 0, "trigger": 1}
        r = E.run(d)
        self.assertFalse(r["tier"].startswith("incomplete"), r["tier"])

    def test_financial_bad_hurdle_price_is_not_defensible(self):
        for hp in (0, -50):
            r = E.run(self.fin(hurdle_price=hp))
            self.assertIsNone(r["trigger"]["trigger"])
            self.assertFalse(r["tier"].startswith("INVEST"))
        r = E.run(self.fin(conservative_central=None))
        self.assertFalse(r["tier"].startswith("INVEST"))

    def test_tier_rule_never_invests_on_nonpositive_trigger_via_run(self):
        self.assertFalse(E.run(self.fin(hurdle_price=-50))["tier"].startswith("INVEST"))

    def test_degenerate_grid_point_is_flagged(self):
        d = inp(valuation__beta=0.0, valuation__net_cash=-500, valuation__debt_wt=0.9, valuation__kd_pre=0.06)
        r = E.run(d)
        self.assertFalse(r["dcf"]["usable"])
        self.assertTrue(any("DEGENERATE" in f for f in r["flags"]))
        self.assertEqual(r["tests_today"]["D1"], 0.0)

    def test_us_terminal_tax_is_max_of_company_and_25(self):
        M = E.MACRO["US"]
        v = dict(BASE["valuation"]); v["tax"] = 0.30
        _, meta = E.dcf_value(v, 0.10, M, detail=True)
        r5 = meta["year5_revenue"]
        expect = r5 * (v["margin_end"] - v["dep_pct"]) * (1 - 0.30) - r5 * 0.04 / 1.04 * v["wc_pct"]
        self.assertAlmostEqual(meta["fcff_norm_y5"], round(expect, 2), places=1)

    def test_missing_scenarios_is_incomplete_not_invest(self):
        r = E.run(inp(scenarios=[], gates={"G2": "pass", "G5": "pass"}))
        self.assertTrue(r["tier"].startswith("incomplete"))

    def test_bad_inputs_refuse_cleanly(self):
        bad = [dict(valuation__shares=0), dict(price=0), dict(valuation__debt_wt=1.0),
               dict(valuation__terminal_g=4.0), dict(bear_triggers=2)]
        for b in bad:
            with self.assertRaises(E.RenderRefused, msg=str(b)):
                E.run(inp(**b))
        d = inp(); d["scenarios"][2].pop("weight")
        with self.assertRaises(E.RenderRefused):
            E.run(d)
        d = inp(); d["scenarios"][1].pop("exit_eps")
        with self.assertRaises(E.RenderRefused):
            E.run(d)

    def test_null_terminal_g_and_kd_default(self):
        r = E.run(inp(valuation__terminal_g=None, valuation__kd_pre=None))
        self.assertEqual(r["dcf"]["meta"]["terminal_g"], 0.04)

    def test_dict_manual_only_for_price_tests(self):
        with self.assertRaises(E.RenderRefused):
            E.run(inp(manual_scores={**BASE["manual_scores"], "A4": {"today": 2, "trigger": 0}}))

    def test_tier_claim_is_exact(self):
        with self.assertRaises(E.RenderRefused):
            E.run(inp(gates={"G2": "pass", "G5": "pass"}, claimed={"tier": "INVEST NOW"}))
        with self.assertRaises(E.RenderRefused):
            E.run(inp(gates={"G2": "pass", "G5": "pass"}, claimed={"tier": "INVEST"}))
        E.run(inp(gates={"G2": "pass", "G5": "pass"}, claimed={"tier": "INVEST AT TRIGGER"}))

    def test_duplicate_bear_triggers_counted_once(self):
        self.assertEqual(E.bear_weight({"bear_triggers": ["a", "a", " a "]})[0], 0.30)

    def test_spec_mini_example(self):
        # fair value ~100 at r_val 11%, g 4% => trigger in the spec's 60-65 range
        v = {"revenue": 100, "margin_start": 0.25, "margin_end": 0.25, "growth": 0.04, "terminal_g": 0.04,
             "capex_pct": 0.03, "dep_pct": 0.03, "wc_pct": 0.0, "tax": 0.2517, "shares": 1.0, "net_cash": 0}
        fv = E.dcf_value(v, 0.11, M_IN)
        p15 = E.dcf_value(v, 0.15, M_IN)
        self.assertTrue(0.60 <= p15 / fv <= 0.66, p15 / fv)


if __name__ == "__main__":
    unittest.main(verbosity=2)
