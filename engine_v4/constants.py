"""Every number in V4_SPEC §11 (plus the §1 bar and §3-§5 numbers §11 points at).

One definition each. Tested against the spec table by tests/test_constants.py.
Nothing here is tunable: k, cutoffs, bands and floors are frozen (§0, §9, §11).
"""
from datetime import timedelta

# ---- §11 row: Rf / ERP / TAX / TG  (carried, v3.10) ------------------------
RF = 0.0695
ERP = 0.040
TAX = 0.2517
TG = 0.04

# ---- §11 row: Anchor horizon / Fade shape (§2.1) ---------------------------
GROWTH_YEARS = 10          # years 1-10 at g
FADE_YEARS = 10            # years 11-19 linear fade to TG; year 20+ = TG
HORIZON_YEARS = 20         # explicit forecast; terminal value struck at year 20
FADE_SHAPE = "linear"

# ---- §11 rows: Margin / WC / capex / netcash / shares / beta (carried) -----
MARGIN_WINDOW_FY = 5       # trailing-5FY average OPM, held FLAT (no fade)
WC_PCT = 0.05              # 5% of incremental revenue
CAPEX_EQUALS_DEP = True    # capex_pct = dp (cancellation written out in anchor.py)
# v3.10 runner defaults used when a whole trailing series is absent (carried verbatim,
# not spec numbers; flagged in the PR as carried silent defaults):
OPM_FALLBACK = 0.15
DEP_FALLBACK = 0.03
DEGENERATE_MARGIN = 0.005  # w <= TG + 0.5pp -> not valued

# ---- §11 row: g_sus family incl. C1/C2/C3 (§2.2) ---------------------------
G_CAP = 0.15
ROE_YEARS = 3

# ---- §11 row: k = 0.875 / 0.70 (§2.3) --------------------------------------
K_G1 = 0.875
K_G2 = 0.70
TIERS = {"G1": K_G1, "G2": K_G2}

# ---- §11 row: g_implied solver bounds (reporting only) ---------------------
SOLVER_LO = -0.50
SOLVER_HI_BELOW_W = 0.01   # upper bound = w - 0.01
SOLVER_ITERS = 200         # implementation detail of bisection, not a spec number

# ---- §11 row: Fill mechanics (carried, v3 #21) -----------------------------
FILL_WINDOW_DAYS = int(2 * 365.25)      # 24m, v3 runner DAYS24M
FILL_WINDOW = timedelta(days=FILL_WINDOW_DAYS)
LEGS_PER_TIER = 1

# ---- §3 PIT vintage ---------------------------------------------------------
PIT_LAG_DAYS = 63

# ---- §11 rows: D1 / D2 -------------------------------------------------------
PLEDGE_VETO_PCT = 50.0     # veto if >= 50% of promoter holding
D2_LOOKBACK_QUARTERS = 8
D2_MIN_QUARTERS = 4

# ---- §11 row: Altman Z'' D3 --------------------------------------------------
Z_COEF = (6.56, 3.26, 6.72, 1.05)       # X1..X4, NO +3.25 constant
Z_VETO_BELOW = 1.1
Z_GREY_TOP = 2.6                        # 1.1-2.6 grey zone PASSES

# ---- §11 row: Piotroski F D4 -------------------------------------------------
PIOTROSKI_VETO_AT_OR_BELOW = 2

# ---- §11 row: Crash veto D5 --------------------------------------------------
CRASH_VETO_DRAWDOWN = 0.60
CRASH_FULL_WINDOW_WEEKS = 52
CRASH_MIN_WEEKS = 26                    # <26 weeks -> UNCOMPUTABLE-DATA

# ---- §11 row: CAMEL D6 --------------------------------------------------------
CAMEL_VETO_AT_OR_BELOW = 4              # of 10
CAMEL_GNPA_HARD_FLOOR = 12.0            # GNPA > 12% -> veto
CAMEL_CAR_HARD_FLOOR = 9.0              # CAR < 9% -> veto
CAMEL_COMPONENT_MAX = 2
# Bands: (2-point threshold, 1-point threshold) with direction.  Boundaries follow
# the spec's open-ended sides: CAR >=15 ->2, >=11.5 ->1 else 0; GNPA <=3 ->2, <=6 ->1;
# C/I <=50 ->2, <=65 ->1; ROA >=1.0 ->2, >=0 ->1; CASA >=40 ->2, >=25 ->1;
# Leverage <=7 ->2, <=10 ->1.
CAMEL_BANDS = {
    "C": {"metric": "car_pct", "higher_better": True, "two": 15.0, "one": 11.5},
    "A": {"metric": "gnpa_pct", "higher_better": False, "two": 3.0, "one": 6.0},
    "M": {"metric": "cost_to_income_pct", "higher_better": False, "two": 50.0, "one": 65.0},
    "E": {"metric": "roa_pct", "higher_better": True, "two": 1.0, "one": 0.0},
    "L_banks": {"metric": "casa_pct", "higher_better": True, "two": 40.0, "one": 25.0},
    "L_nbfc": {"metric": "leverage_x", "higher_better": False, "two": 7.0, "one": 10.0},
}
FINANCIAL_SECTORS = ("Banks", "Finance")   # screener.in Sector -> CAMEL; else Z''+F

# ---- §11 row: Usability U3 ----------------------------------------------------
U3_TOLERANCE = 0.15
U3_MEDIAN_WINDOW_DAYS = 21               # results-week .. +21d
U3_JUMP_SKIP = 0.10                      # >10% jump skip rule

# ---- §11 rows: Event window / Cooling-off (§5.3) ------------------------------
EVENT_WINDOW_MONTHS = 12
COOLING_OFF_MONTHS = 12
COOLING_OFF_PRINTS = 1
SEARCH_SOURCES = ("screener_results_calendar", "bse_nse_corporate_announcements",
                  "company_annual_report_pdfs")
SEARCH_SOURCES_REQUIRED = 2

# ---- §11 rows: Exit slippage / Delisting staleness (§5.4) ---------------------
EXIT_SLIPPAGE = 0.99
DELIST_STALE_TRADING_DAYS = 20

# ---- §11 row: Fill-plausibility band (§8.2) -----------------------------------
FILL_PLAUSIBILITY_MULT = 2.0             # P_d0 <= 2.0 * P_G1

# ---- §11 row: Decisional test set (§8.2) / §1 leg (a') -------------------------
DECISIONAL_SET_SIZE = 5
DECISIONAL_MIN = 3

# ---- §11 row: Aggregation ------------------------------------------------------
AGGREGATION = "leg-weighted means, price return only"

# ---- §11 row: Zero-overlap (§8.3 / §9) -----------------------------------------
ZERO_OVERLAP_PRIOR_SETS_V4 = 5           # in-sample + v3.8-v3.11
ZERO_OVERLAP_PRIOR_SETS_ITERATIONS = 6   # + v4

# ---- §1 live bar ---------------------------------------------------------------
BAR_MAX_BLOWUP_FILLS = 0
BAR_MIN_WINNER_NAMES = 3
BAR_MIN_24M_MULT = 0.8
