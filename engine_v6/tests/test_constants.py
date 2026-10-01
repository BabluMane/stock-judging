"""§11 constants-table test. Every number in V6_SPEC §11 is asserted (1) as a literal against
constants.py, and (2) where feasible against the BEHAVIOUR of the implementation, so a constant
that drifts -- or is copied but not used -- fails. Also guards the frozen spec file and that every
§11 row is covered here (a new/renamed row fails the coverage test).

Run:  python3 -m unittest discover -s engine_v6/tests -t .
"""
import copy, hashlib, math, os, re, unittest
from datetime import date, timedelta

from engine_v6 import anchor, constants as C, distress, events, usability
from engine_v6.aggregate import bar
from engine_v6.common import add_months
from engine_v6.run import run_name_date
from engine_v6.tests import fixtures as F

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "V6_SPEC.md")
SPEC_SHA256 = "173f902a7ad637387e32eba93dbbb3a4d32987891d87a89fca74d5a9fa1d717e"
PIN_RE = re.compile(r"^Spec-SHA-256: [0-9a-fx]{64}$")


def spec_bytes_minus_pin():
    """§13 pin procedure: hash the file's bytes with the single pin line removed
    (the pin line itself is content-independent)."""
    with open(SPEC, "rb") as fh:
        lines = fh.read().split(b"\n")
    kept = [l for l in lines if not PIN_RE.match(l.decode("utf-8", "replace"))]
    assert len(kept) == len(lines) - 1, "the pin line must match exactly once"
    return b"\n".join(kept)

# One entry per §11 row (first column text, exactly as in the spec).
S11_ROWS = [
    "Rf / ERP / TAX / TG", "Anchor horizon", "Fade shape", "Margin",
    "WC 5% incr rev; capex≈dep; netcash = inv−borr; shares = mcap÷price; sector β pre-run",
    "g_sus family incl. C1/C2/C3", "k = 0.875 / 0.70", "g_implied solver bounds", "Fill mechanics",
    "Pledge level D1", "First-time pledge D2", "Altman Z'' D3", "Piotroski F D4", "Crash veto D5",
    "CAMEL D6", "Sloan accruals E1", "Cash conversion E2", "Interest coverage E3", "ETR E4",
    "Receivables-cash-collection E6", "E-rule scope", "Reporting-only fields", "New v5 input fields",
    "Usability U3", "Event window §5.3", "Cooling-off §5.3", "Exit slippage §5.4",
    "Delisting staleness §5.4", "Fill-plausibility band §8.2", "Decisional test set §8.2",
    "Aggregation", "Zero-overlap §8.3",
]


class SpecFile(unittest.TestCase):
    def test_spec_is_the_frozen_file(self):
        # §13: the pin is the SHA-256 of the file with the pin line itself removed.
        self.assertEqual(hashlib.sha256(spec_bytes_minus_pin()).hexdigest(), SPEC_SHA256)

    def test_every_s11_row_is_covered_by_this_test(self):
        with open(SPEC, encoding="utf-8") as fh:
            txt = fh.read()
        sec = txt.split("## §11")[1].split("## §12")[0]
        rows = [re.sub(r"^\*\*|\*\*$", "", l.split("|")[1].strip()) for l in sec.splitlines()
                if l.startswith("|") and not l.startswith("|---") and "Constant" not in l.split("|")[1]]
        self.assertEqual(rows, S11_ROWS)


class Literals(unittest.TestCase):
    def test_rf_erp_tax_tg(self):
        self.assertEqual((C.RF, C.ERP, C.TAX, C.TG), (0.0695, 0.040, 0.2517, 0.04))

    def test_horizon_and_fade(self):
        self.assertEqual((C.GROWTH_YEARS, C.FADE_YEARS, C.HORIZON_YEARS, C.FADE_SHAPE), (10, 10, 20, "linear"))

    def test_carried_simplifications(self):
        self.assertEqual(C.WC_PCT, 0.05)
        self.assertTrue(C.CAPEX_EQUALS_DEP)
        self.assertEqual(C.MARGIN_WINDOW_FY, 5)

    def test_gsus_family(self):
        self.assertEqual((C.G_CAP, C.ROE_YEARS), (0.15, 3))

    def test_k(self):
        self.assertEqual((C.K_G1, C.K_G2), (0.875, 0.70))
        self.assertEqual(C.TIERS, {"G1": 0.875, "G2": 0.70})

    def test_solver_bounds(self):
        self.assertEqual((C.SOLVER_LO, C.SOLVER_HI_BELOW_W), (-0.50, 0.01))

    def test_fill_mechanics(self):
        self.assertEqual((C.FILL_WINDOW_DAYS, C.LEGS_PER_TIER), (730, 1))

    def test_distress_cutoffs(self):
        self.assertEqual(C.PLEDGE_VETO_PCT, 50.0)
        self.assertEqual((C.D2_LOOKBACK_QUARTERS, C.D2_MIN_QUARTERS), (8, 4))
        self.assertEqual(C.Z_COEF, (6.56, 3.26, 6.72, 1.05))
        self.assertEqual((C.Z_VETO_BELOW, C.Z_GREY_TOP), (1.1, 2.6))
        self.assertEqual(C.PIOTROSKI_VETO_AT_OR_BELOW, 2)
        self.assertEqual((C.CRASH_VETO_DRAWDOWN, C.CRASH_FULL_WINDOW_WEEKS, C.CRASH_MIN_WEEKS), (0.60, 52, 26))
        self.assertEqual((C.CAMEL_VETO_AT_OR_BELOW, C.CAMEL_GNPA_HARD_FLOOR, C.CAMEL_CAR_HARD_FLOOR), (4, 12.0, 9.0))
        self.assertEqual(C.PIT_LAG_DAYS, 63)

    def test_camel_bands(self):
        b = C.CAMEL_BANDS
        self.assertEqual((b["C"]["two"], b["C"]["one"]), (15.0, 11.5))
        self.assertEqual((b["A"]["two"], b["A"]["one"]), (3.0, 6.0))
        self.assertEqual((b["M"]["two"], b["M"]["one"]), (50.0, 65.0))
        self.assertEqual((b["E"]["two"], b["E"]["one"]), (1.0, 0.0))
        self.assertEqual((b["L_banks"]["two"], b["L_banks"]["one"]), (40.0, 25.0))
        self.assertEqual((b["L_nbfc"]["two"], b["L_nbfc"]["one"]), (7.0, 10.0))
        self.assertEqual(C.FINANCIAL_SECTORS, ("Banks", "Finance"))

    def test_usability_event_exit(self):
        self.assertEqual((C.U3_TOLERANCE, C.U3_MEDIAN_WINDOW_DAYS, C.U3_JUMP_SKIP), (0.15, 21, 0.10))
        self.assertEqual((C.EVENT_WINDOW_MONTHS, C.COOLING_OFF_MONTHS, C.COOLING_OFF_PRINTS), (12, 12, 1))
        self.assertEqual((C.EXIT_SLIPPAGE, C.DELIST_STALE_TRADING_DAYS), (0.99, 20))
        self.assertEqual(C.SEARCH_SOURCES_REQUIRED, 2)

    def test_e_rule_literals(self):
        self.assertEqual((C.SLOAN_E1_THRESHOLD, C.E1_POSITIVE_ONLY, C.E1_FY_WINDOW), (0.10, True, 1))
        self.assertEqual((C.E2_CFO_PCT, C.E2_PERSISTENCE_FY), (0.5, 2))
        self.assertEqual(C.E3_IC_VETO_BELOW, 1.5)
        self.assertEqual((C.E4_ETR_VETO_BELOW, C.E4_PERSISTENCE_FY), (0.15, 2))
        self.assertEqual((C.E6_DAYS_VETO_ABOVE, C.E6_CFO_TRIP_AT_OR_BELOW), (90, 0))
        self.assertTrue(C.E_SCOPE_NONFINANCIAL_ONLY)

    def test_certification_bar_overlap(self):
        self.assertEqual(C.FILL_PLAUSIBILITY_MULT, 2.0)
        self.assertEqual((C.DECISIONAL_SET_SIZE, C.DECISIONAL_MIN), (5, 3))
        self.assertEqual(C.AGGREGATION, "leg-weighted means, price return only")
        self.assertEqual((C.ZERO_OVERLAP_PRIOR_SETS_V6, C.ZERO_OVERLAP_PRIOR_SETS_ITERATIONS), (7, 8))
        self.assertEqual((C.BAR_MAX_BLOWUP_FILLS, C.BAR_MIN_WINNER_NAMES, C.BAR_MIN_24M_MULT), (0, 3, 0.8))


class Behaviour(unittest.TestCase):
    """The implementation actually USES the constants (a copied-but-unused number fails here)."""

    def _val(self, **kw):
        a = dict(beta=1.0, mcap_cr=10000.0, mcap_price=100.0, price_d0=100.0)
        a.update(kw)
        return anchor.value_anchor(F.fy_records(), 2018, False, a["beta"], a["mcap_cr"], a["mcap_price"], a["price_d0"])

    def test_wacc_uses_rf_erp(self):
        for beta in (0.6, 1.0, 1.15):
            self.assertAlmostEqual(self._val(beta=beta)["w"], 0.0695 + beta * 0.040)

    def test_fade_is_linear_10_10_20(self):
        gp = anchor.growth_path(0.12)
        self.assertEqual(gp[:10], [0.12] * 10)
        for t in range(11, 20):
            self.assertAlmostEqual(gp[t - 1], 0.12 + (0.04 - 0.12) * (t - 10) / 10)
        self.assertEqual((gp[19], gp[20]), (0.04, 0.04))          # year 20 and terminal year 21
        self.assertEqual(len(gp), 21)

    def test_fcff_uses_tax_wc_and_capex_equals_dep(self):
        r0, r1, m, dp = 100.0, 110.0, 0.2, 0.03
        self.assertAlmostEqual(anchor.fcff_flow(r0, r1, m, dp), r1 * (m - dp) * (1 - 0.2517) - (r1 - r0) * 0.05)
        self.assertAlmostEqual(anchor.fcff_flow(r0, r1, m, dp), anchor.fcff_flow_uncancelled(r0, r1, m, dp, cp=dp))

    def test_margin_is_flat_trailing_5y_avg(self):
        fy = F.fy_records()
        for i, y in enumerate(range(2014, 2019)):
            fy[y]["opm_pct"] = 10.0 + 5 * i                      # 10,15,20,25,30 -> mean 20
        v, _ = anchor.dcf_inputs(fy, 2018, 1.0)
        self.assertAlmostEqual(v["margin"], 0.20)
        base = anchor.enterprise_value(v, v["w"], 0.05)
        v2 = dict(v, margin=0.20)                                # flat: same value if handed the mean directly
        self.assertAlmostEqual(base, anchor.enterprise_value(v2, v["w"], 0.05))

    def test_netcash_and_shares(self):
        a = self._val()
        self.assertAlmostEqual(a["net_cash_cr"], 50.0 - 120.0)   # investments - borrowings (2018: 200-80)
        self.assertAlmostEqual(a["shares_cr"], 10000.0 / 100.0)  # mcap / price
        v, _ = anchor.dcf_inputs(F.fy_records(), 2018, 1.0)
        ev = anchor.enterprise_value(v, v["w"], a["g_sus"])
        self.assertAlmostEqual(a["v_at_g_sus"], (ev + a["net_cash_cr"]) / a["shares_cr"])

    def test_degenerate_guard(self):
        v, _ = anchor.dcf_inputs(F.fy_records(), 2018, 1.0)
        self.assertIsNone(anchor.enterprise_value(v, 0.04 + 0.005, 0.05))
        self.assertIsNotNone(anchor.enterprise_value(v, 0.04 + 0.0051, 0.05))

    def test_gsus_cap_payout_no_floor(self):
        fy = F.fy_records()
        for y in fy:
            fy[y]["net_profit"] = 400.0                          # ROE ~ 0.5+ -> cap binds
        sg, _ = anchor.sustainable_growth(fy, 2018)
        self.assertEqual(sg["g_sus"], 0.15)
        self.assertTrue(sg["cap_binding"])
        fy[2018]["dividend_payout_pct"] = 150.0                  # C2 unclipped -> negative factor, C3 no floor
        sg, _ = anchor.sustainable_growth(fy, 2018)
        self.assertLess(sg["g_sus"], 0)
        self.assertAlmostEqual(sg["g_sus"], sg["roe_avg3"] * (1 - 1.5))

    def test_k_and_hurdle_sign_preserving(self):
        self.assertAlmostEqual(anchor.hurdle_growth(0.12, 0.875), 0.105)
        self.assertAlmostEqual(anchor.hurdle_growth(0.12, 0.70), 0.084)
        self.assertAlmostEqual(anchor.hurdle_growth(-0.10, 0.875), -0.1125)   # tightens, never loosens
        a = self._val()
        for t, k in (("G1", 0.875), ("G2", 0.70)):
            self.assertAlmostEqual(a["hurdle_growth"][t], a["g_sus"] * k)

    def test_solver_bounds_and_reporting_only(self):
        v = lambda g: 100 + 1000 * g
        hi_price = anchor.solve_implied_growth(v, 1e9, 0.11)
        self.assertEqual(hi_price["status"], ">w-1pp")
        self.assertAlmostEqual(hi_price["hi"], 0.11 - 0.01)
        lo_price = anchor.solve_implied_growth(v, -1e9, 0.11)
        self.assertEqual((lo_price["status"], lo_price["g_implied"]), ("at_-50%_floor", -0.50))
        mid = anchor.solve_implied_growth(v, 150.0, 0.11)
        self.assertAlmostEqual(mid["g_implied"], 0.05, places=9)
        self.assertTrue(mid["reporting_only"])

    def test_fill_window_and_one_leg_per_tier(self):
        nd = F.make_nd()
        trig = run_name_date(nd)["anchor"]["trigger"]["G2"]
        inside = F.D0 + timedelta(days=730)
        edits = {d: trig * 0.5 for d, _ in nd.prices if d > inside}       # touches only after 24m
        self.assertEqual(run_name_date(F.with_prices(nd, edits))["legs"]["G2"]["status"], "NO_TOUCH")
        edits = {d: trig * 0.5 for d, _ in nd.prices if F.D0 < d <= inside}
        res = run_name_date(F.with_prices(nd, edits))
        self.assertEqual(sorted(res["legs"]), ["G1", "G2"])               # one leg per tier
        first_after_d0 = next(d for d, _ in nd.prices if d > F.D0)
        self.assertEqual(res["legs"]["G2"]["fill_date"], first_after_d0.isoformat())

    def test_pledge_level_boundary(self):
        for pct, want in ((49.99, "PASS"), (50.0, "TRIP")):
            self.assertEqual(distress.d1_pledge_level(F.quarters(pledged=pct), F.D0)["status"], want)

    def test_first_time_pledge_8q_min4(self):
        q = F.quarters(12, 0.0)
        q[-1]["pledged_pct"] = 5.0
        self.assertEqual(distress.d2_first_time_pledge(q, F.D0)["status"], "TRIP")
        q7 = q[-8:]                                                  # 7 prior quarters, all 0 -> still TRIP (>=4)
        self.assertEqual(distress.d2_first_time_pledge(q7, F.D0)["status"], "TRIP")
        q4 = q[-5:]                                                  # exactly 4 prior
        self.assertEqual(distress.d2_first_time_pledge(q4, F.D0)["status"], "TRIP")
        q3 = q[-4:]                                                  # 3 prior -> N/A
        self.assertEqual(distress.d2_first_time_pledge(q3, F.D0)["status"], "N/A")
        old = F.quarters(12, 0.0)
        old[-9]["pledged_pct"] = 1.0                                 # a non-zero quarter within the 8 prior -> not first-time
        old[-1]["pledged_pct"] = 5.0
        self.assertEqual(distress.d2_first_time_pledge(old, F.D0)["status"], "PASS")
        old2 = F.quarters(12, 0.0)
        old2[-10]["pledged_pct"] = 1.0                               # 9th-prior quarter is outside the 8-quarter lookback
        old2[-1]["pledged_pct"] = 5.0
        self.assertEqual(distress.d2_first_time_pledge(old2, F.D0)["status"], "TRIP")

    def test_altman_coefficients_and_boundary(self):
        fy = F.fy_records()
        r = distress.d3_altman(fy, 2018)
        x1, x2, x3, x4 = r["x"]
        self.assertAlmostEqual(r["z"], 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4)   # no +3.25
        # push Z'' to either side of 1.1 by scaling total assets (X1..X3 scale 1/TA; X4 moves too)
        lo = None
        for ta in (2100, 3000, 5000, 8000, 12000, 20000, 40000):
            fy[2018]["total_assets"] = float(ta)
            z = distress.d3_altman(fy, 2018)
            if z["z"] < 1.1:
                lo = z
                break
        self.assertIsNotNone(lo)
        self.assertEqual(lo["status"], "TRIP")
        self.assertEqual(distress.d3_altman(F.fy_records(), 2018)["status"], "PASS")
        neg = F.fy_records(); neg[2018]["reserves"] = -60.0        # book equity <= 0 -> automatic veto
        self.assertEqual(distress.d3_altman(neg, 2018)["status"], "TRIP")

    def test_piotroski_boundary(self):
        fy = F.fy_records()
        self.assertEqual(distress.d4_piotroski(fy, 2018, False)["f"], 9)
        # F == 3 passes, F == 2 vetoes: zero out criteria
        def score(n_fail):
            f = F.fy_records()
            if n_fail >= 1: f[2018]["cfo"] = -1.0                     # F_CFO=0 and F_ACCRUAL=0
            if n_fail >= 2: f[2018]["net_profit"] = -1.0              # F_ROA=0, F_dROA=0
            if n_fail >= 3: f[2018]["borrowings"] = 9999.0            # F_dLEVER=0
            if n_fail >= 4: f[2018]["current_assets"] = 1.0           # F_dLIQUID=0
            if n_fail >= 5: f[2018]["raw_material_pct"] = 99.0        # F_dMARGIN=0
            if n_fail >= 6: f[2018]["sales"] = 1.0                    # F_dTURN=0
            return distress.d4_piotroski(f, 2018, False)
        self.assertLessEqual(score(6)["f"], 2)
        seen = {score(n)["f"]: score(n)["status"] for n in range(0, 7)}
        self.assertIn(3, seen)                                   # the F == 3 / F == 2 boundary is exercised
        self.assertIn(2, seen)
        for f, st in seen.items():
            self.assertEqual(st, "TRIP" if f <= 2 else "PASS", f)

    def test_crash_boundary_and_history(self):
        def series(drop):
            pts = F.weekly(date(2018, 3, 30), F.D0, lambda d: 100.0)
            pts[-1] = (pts[-1][0], 100.0 * (1 - drop))
            return pts
        self.assertEqual(distress.d5_crash(series(0.5999), F.D0)["status"], "PASS")
        self.assertEqual(distress.d5_crash(series(0.60), F.D0)["status"], "TRIP")
        short = F.weekly(F.D0 - timedelta(weeks=25), F.D0, lambda d: 100.0)
        self.assertEqual(distress.d5_crash(short, F.D0)["status"], "UNCOMPUTABLE")
        ok = F.weekly(F.D0 - timedelta(weeks=26), F.D0, lambda d: 100.0)
        self.assertEqual(distress.d5_crash(ok, F.D0)["status"], "PASS")

    def test_camel_bands_floors_total(self):
        def fin(**kw):
            base = {"car_pct": 16.0, "gnpa_pct": 2.0, "cost_to_income_pct": 45.0, "roa_pct": 1.5, "casa_pct": 45.0, "leverage_x": 5.0}
            base.update(kw)
            return {2018: base}
        self.assertEqual(distress.d6_camel(fin(), 2018, "Banks")["total"], 10)
        # each band boundary
        cases = [("car_pct", 15.0, "C", 2), ("car_pct", 14.99, "C", 1), ("car_pct", 11.5, "C", 1), ("car_pct", 11.49, "C", 0),
                 ("gnpa_pct", 3.0, "A", 2), ("gnpa_pct", 3.01, "A", 1), ("gnpa_pct", 6.0, "A", 1), ("gnpa_pct", 6.01, "A", 0),
                 ("cost_to_income_pct", 50.0, "M", 2), ("cost_to_income_pct", 50.01, "M", 1), ("cost_to_income_pct", 65.0, "M", 1), ("cost_to_income_pct", 65.01, "M", 0),
                 ("roa_pct", 1.0, "E", 2), ("roa_pct", 0.99, "E", 1), ("roa_pct", 0.0, "E", 1), ("roa_pct", -0.01, "E", 0),
                 ("casa_pct", 40.0, "L", 2), ("casa_pct", 39.99, "L", 1), ("casa_pct", 25.0, "L", 1), ("casa_pct", 24.99, "L", 0)]
        for field, val, comp, want in cases:
            self.assertEqual(distress.d6_camel(fin(**{field: val}), 2018, "Banks")["scores"][comp], want, (field, val))
        for val, want in ((7.0, 2), (7.01, 1), (10.0, 1), (10.01, 0)):
            self.assertEqual(distress.d6_camel(fin(leverage_x=val), 2018, "Finance")["scores"]["L"], want)
        # total <= 4 vetoes, 5 passes (CAR 11.5->1, GNPA 6->1, C/I 65->1, ROA 0->1, CASA 25->1 => 5)
        five = fin(car_pct=11.5, gnpa_pct=6.0, cost_to_income_pct=65.0, roa_pct=0.0, casa_pct=25.0)
        self.assertEqual((distress.d6_camel(five, 2018, "Banks")["total"], distress.d6_camel(five, 2018, "Banks")["status"]), (5, "PASS"))
        four = fin(car_pct=11.5, gnpa_pct=6.0, cost_to_income_pct=65.0, roa_pct=0.0, casa_pct=24.0)
        self.assertEqual((distress.d6_camel(four, 2018, "Banks")["total"], distress.d6_camel(four, 2018, "Banks")["status"]), (4, "TRIP"))
        # hard floors override a perfect total
        self.assertEqual(distress.d6_camel(fin(gnpa_pct=12.01), 2018, "Banks")["status"], "TRIP")
        self.assertEqual(distress.d6_camel(fin(gnpa_pct=12.0, car_pct=16.0), 2018, "Banks")["status"], "PASS")
        self.assertEqual(distress.d6_camel(fin(car_pct=8.99), 2018, "Banks")["status"], "TRIP")
        self.assertEqual(distress.d6_camel(fin(car_pct=9.0), 2018, "Banks")["status"], "PASS")

    def test_class_split(self):
        self.assertTrue(distress.is_financial("Banks") and distress.is_financial("Finance"))
        self.assertFalse(distress.is_financial("Consumer") or distress.is_financial("Insurance"))

    def test_u3_tolerance_window_and_jump_rule(self):
        s = 100.0
        for ttm, want in ((115.0, "PASS"), (115.01, "STOP"), (85.0, "PASS"), (84.99, "STOP")):
            r = usability.u3_check_a_prime([(date(2018, 5, 20), ttm)], 2018, s)
            self.assertEqual(r["status"], want, ttm)
        # median over results-week..+21d (points at +0, +10, +21 in; +22 out)
        pts = [(date(2018, 5, 20), 100.0), (date(2018, 5, 30), 200.0), (date(2018, 6, 10), 300.0), (date(2018, 6, 11), 9999.0)]
        self.assertEqual(usability.results_week_ttm(pts, 2018)["ttm"], 200.0)
        # Mar-31 point with >10% jump to the next -> skipped; <=10% -> kept (back-dated FY value)
        stale = [(date(2018, 3, 31), 100.0), (date(2018, 5, 20), 111.0)]
        self.assertEqual(usability.results_week_ttm(stale, 2018)["results_week"], date(2018, 5, 20))
        kept = [(date(2018, 3, 31), 100.0), (date(2018, 5, 20), 110.0)]
        self.assertEqual(usability.results_week_ttm(kept, 2018)["results_week"], date(2018, 3, 31))

    def test_event_window_12m_boundary_and_cooling_off(self):
        ev = events.grade_event({"event_date": date(2018, 4, 10), "type": "T3", "subcase": "off_market_transfer_or_gift",
                                 "sources": [{"tier": 1, "ref": "x"}]})
        self.assertTrue(events.entry_veto([ev], [], date(2019, 4, 9))["blocked"])       # inside trailing 12m
        # with a qualifying print the block lapses at exactly 12 months
        prt = [{"results_date": date(2018, 5, 20), "fy_end": date(2018, 3, 31)}]        # FY-end BEFORE event -> does not count
        self.assertTrue(events.entry_veto([ev], prt, date(2019, 4, 10))["blocked"])
        prt = [{"results_date": date(2018, 6, 1), "fy_end": date(2018, 6, 30)}]         # both strictly after event
        self.assertFalse(events.entry_veto([ev], prt, date(2019, 4, 10))["blocked"])
        self.assertTrue(events.entry_veto([ev], prt, date(2019, 4, 9))["blocked"])
        prt = [{"results_date": date(2018, 4, 10), "fy_end": date(2018, 6, 30)}]        # results date == event date -> not strictly after
        self.assertTrue(events.entry_veto([ev], prt, date(2019, 5, 1))["blocked"])

    def test_exit_slippage_and_delisting_staleness(self):
        fill = date(2019, 4, 5)
        px = F.weekly(date(2019, 3, 29), date(2019, 6, 28), lambda d: 100.0)
        ev = [{"event_date": date(2019, 5, 1), "grade": "SEVERE", "type": "T7", "weak_source": False}]
        s = events.exit_scan(fill, F.D0, px, ev)
        self.assertTrue(s["fired"])
        self.assertAlmostEqual(s["exit_price_after_slippage"], 99.0)
        # series truncated at 2019-06-28; event 2020-01-02 -> last print far older than 20 trading days -> UNEXECUTED
        late = [{"event_date": date(2020, 1, 2), "grade": "SEVERE", "type": "T7", "weak_source": False}]
        self.assertTrue(events.exit_scan(fill, F.D0, px, late)["exit_unexecuted"])
        # exactly 20 weekdays after the last print: executed (not stale); 21: UNEXECUTED
        last = px[-1][0]
        def n_weekdays_after(n):
            d, c = last, 0
            while c < n:
                d += timedelta(days=1)
                c += d.weekday() < 5
            return d
        for n, want in ((20, False), (21, True)):
            e = [{"event_date": n_weekdays_after(n), "grade": "SEVERE", "type": "T7", "weak_source": False}]
            self.assertEqual(events.exit_scan(fill, F.D0, px, e)["exit_unexecuted"], want, n)

    def test_fill_plausibility_band(self):
        self.assertTrue(anchor.fill_plausible(200.0, 100.0))
        self.assertFalse(anchor.fill_plausible(200.01, 100.0))
        self.assertFalse(anchor.fill_plausible(50.0, -1.0))

    def test_decisional_set_and_bar_constants(self):
        res = {}
        self.assertEqual(bar(res, ["a", "b", "c", "d"])["leg_a"], "VOID")                # <5 certified -> VOID
        five = list("abcde")
        self.assertEqual(bar({}, five)["leg_a"], "UNTESTED")                             # unexercised 0 != PASS
        self.assertTrue(bar({}, five)["run_void"])

    def test_aggregation_is_leg_weighted_price_return(self):
        import engine_v6.aggregate as A
        legs = [{"status": "FILLED", "ret_to_t": 1.0, "ret_24m": 0.0, "realized_exit": False, "exit_scan": {}},
                {"status": "FILLED", "ret_to_t": 0.0, "ret_24m": 0.0, "realized_exit": False, "exit_scan": {}}]
        results = {"x_2019-03-31": {"legs": {"G1": legs[0], "G2": legs[1]}}, "y_2019-03-31": {"legs": {"G1": dict(legs[0])}}}
        agg = A.aggregates(results)
        self.assertAlmostEqual(agg["mean_return_to_t"], 2 / 3)                            # legs, not name-dates
        self.assertAlmostEqual(agg["mean_mult_to_t"], 1 + 2 / 3)

    # ---- E1-E4 + E6: the implementation actually USES the new constants ----
    def _e(self, year=2018, **over):
        fy = F.fy_records()
        for k, v in over.items():
            fy[year][k] = v
        return fy

    def test_e1_strict_boundary_and_positive_only(self):
        # float-exact 0.10 boundary: strict > means it does NOT trip
        fy = F.fy_records(); fy[2018]["net_profit"] = 100.0; fy[2018]["cfo"] = 0.0; fy[2018]["total_assets"] = 1000.0
        r = distress.e1_sloan(fy, 2018)
        self.assertEqual(r["sloan"], 0.10)
        self.assertEqual(r["status"], "PASS")
        fy[2018]["cfo"] = -0.01
        self.assertEqual(distress.e1_sloan(fy, 2018)["status"], "TRIP")
        self.assertEqual(distress.e1_sloan(self._e(cfo=200.0), 2018)["status"], "PASS")   # CFO>NI: conservatism never trips
        self.assertEqual(distress.e1_sloan(self._e(total_assets=0.0), 2018)["status"], "UNCOMPUTABLE")
        self.assertEqual(distress.e1_sloan(self._e(cfo=None), 2018)["status"], "UNCOMPUTABLE")
        r = distress.e1_sloan(self._e(cfo=-60.0), 2018)                # (175.69+60)/2100 = 0.1122
        self.assertAlmostEqual(r["sloan"], (120 * 1.1 ** 4 + 60.0) / 2100.0)
        self.assertEqual(r["status"], "TRIP")

    def test_e2_needs_two_consecutive_years_applied_literally(self):
        fy = self._e(); fy[2017]["cfo"], fy[2018]["cfo"] = 40.0, 40.0    # 40 < 0.5*NI both years
        self.assertEqual(distress.e2_cash_conversion(fy, 2018)["status"], "TRIP")
        fy2 = self._e(); fy2[2017]["cfo"], fy2[2018]["cfo"] = 200.0, 40.0
        self.assertEqual(distress.e2_cash_conversion(fy2, 2018)["status"], "PASS")   # 1-yr only: cheap insurance, not the trigger
        fy3 = self._e(); fy3[2018]["net_profit"] = None
        self.assertEqual(distress.e2_cash_conversion(fy3, 2018)["status"], "UNCOMPUTABLE")

    def test_e3_boundary_and_interest_zero_guard(self):
        self.assertEqual(distress.e3_interest_coverage(self._e(pbt=50.0, interest=100.0), 2018)["status"], "PASS")  # ic == 1.5 exactly
        self.assertEqual(distress.e3_interest_coverage(self._e(pbt=49.0, interest=100.0), 2018)["status"], "TRIP")  # ic == 1.49
        self.assertEqual(distress.e3_interest_coverage(self._e(pbt=100.0, interest=0.0), 2018)["status"], "PASS")   # guard: no trip
        self.assertEqual(distress.e3_interest_coverage(self._e(pbt=-50.0, interest=100.0), 2018)["status"], "TRIP")  # signed PBT as-is: ic = 0.5
        self.assertEqual(distress.e3_interest_coverage(self._e(pbt=None), 2018)["status"], "UNCOMPUTABLE")

    def test_e4_two_years_and_pbt_guard_and_no_1_minus_ni_pbt(self):
        fy = self._e(); fy[2018]["tax_expense"] = fy[2018]["pbt"] * 0.10; fy[2017]["tax_expense"] = fy[2017]["pbt"] * 0.10
        self.assertEqual(distress.e4_etr(fy, 2018)["status"], "TRIP")       # 10% both years
        fy2 = self._e(); fy2[2018]["tax_expense"] = fy2[2018]["pbt"] * 0.10
        self.assertEqual(distress.e4_etr(fy2, 2018)["status"], "PASS")      # 1-yr only
        fy3 = self._e(); fy3[2018]["pbt"] = -5.0                            # PBT <= 0 -> non-trip, not UNCOMPUTABLE
        self.assertEqual(distress.e4_etr(fy3, 2018)["status"], "PASS")
        fy4 = self._e(); fy4[2018]["tax_expense"] = None
        self.assertEqual(distress.e4_etr(fy4, 2018)["status"], "UNCOMPUTABLE")
        # the PBM-FY18 trap: NI > PBT would print -33% on the forbidden 1-NI/PBT construction
        fy5 = self._e(); fy5[2018]["net_profit"] = 100.0; fy5[2018]["pbt"] = 80.0; fy5[2018]["tax_expense"] = 25.0
        r = distress.e4_etr(fy5, 2018)
        self.assertAlmostEqual(r["etr"][2018], 0.3125)                     # 25/80: tax-expense line only
        self.assertEqual(r["status"], "PASS")

    def test_e6_days_strict_cfo_inclusive_and_uses_both_constants(self):
        def fy6(days, cfo):
            fy = F.fy_records()
            fy[2018]["receivables"] = days * fy[2018]["sales"] / 365
            fy[2018]["cfo"] = cfo
            return fy
        # days exactly 90.0 + CFO<0 -> PASS (kills 90 -> 89)
        r = distress.e6_receivables_cash_collection(fy6(90.0, -1.0), 2018)
        self.assertEqual(r["days"], 90.0)
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(r["thresholds"], (90, 0))                 # both constants actually flow in
        # days 90.5 + CFO<0 -> TRIP (kills 90 -> 91)
        r = distress.e6_receivables_cash_collection(fy6(90.5, -1.0), 2018)
        self.assertAlmostEqual(r["days"], 90.5)
        self.assertEqual(r["status"], "TRIP")
        # CFO exactly 0.0 + days>90 -> TRIP (kills <= -> <)
        self.assertEqual(distress.e6_receivables_cash_collection(fy6(100.0, 0.0), 2018)["status"], "TRIP")
        # CFO +1 + days>90 -> PASS (kills sign flip)
        self.assertEqual(distress.e6_receivables_cash_collection(fy6(100.0, 1.0), 2018)["status"], "PASS")
        # days 89 + CFO<0 -> PASS (conjunction, not days-only; kills and -> or)
        self.assertEqual(distress.e6_receivables_cash_collection(fy6(89.0, -1.0), 2018)["status"], "PASS")
        # guards -> UNCOMPUTABLE (never a silent pass)
        self.assertEqual(distress.e6_receivables_cash_collection(self._e(cfo=None), 2018)["status"], "UNCOMPUTABLE")
        self.assertEqual(distress.e6_receivables_cash_collection(self._e(receivables=None), 2018)["status"], "UNCOMPUTABLE")
        self.assertEqual(distress.e6_receivables_cash_collection(self._e(sales=0.0), 2018)["status"], "UNCOMPUTABLE")

    def test_financial_names_are_e_na_by_construction(self):
        r = distress.evaluate({2018: {"results_published": date(2018, 5, 20)}}, 2018, "Banks",
                              F.flat_prices(), F.quarters(), F.D0)
        for e in ("E1", "E2", "E3", "E4", "E6"):
            self.assertEqual(r["rules"][e]["status"], "N/A", e)
        self.assertEqual(r["e_rules"], "N/A (financial variant)")

    def test_d7_order_puts_e_rules_between_d2_and_d3(self):
        self.assertEqual(distress.ORDER, ("D1", "D2", "E1", "E2", "E3", "E4", "E6", "D3", "D6", "D4", "D5"))

    def test_reporting_fields_are_stored_never_veto(self):
        fy = self._e()
        r = distress.evaluate(fy, 2018, "Consumer", F.flat_prices(), F.quarters(), F.D0)
        rep = r["reporting"]
        self.assertAlmostEqual(rep["SGI"], 1.1)
        self.assertAlmostEqual(rep["TATA"], (120 * 1.1 ** 4 - 150 * 1.1 ** 4) / (1500.0 + 150 * 4))
        self.assertEqual(rep["rpt_loans"], 0.0)
        fy2 = self._e(ppe_net=None)
        r2 = distress.evaluate(fy2, 2018, "Consumer", F.flat_prices(), F.quarters(), F.D0)
        self.assertIsNone(r2["reporting"]["DEPI"])
        self.assertTrue(any("DEPI" in l for l in r2["reporting_log"]))
        self.assertEqual(r2["label"], "PASS")      # reporting fields can never veto


if __name__ == "__main__":
    unittest.main()
