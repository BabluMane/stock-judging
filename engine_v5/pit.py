"""Point-in-time helpers (§3 input vintage). FY records are dicts keyed by the
fiscal-year-end calendar year (2019 == 'Mar 2019'); a key being present is the
analogue of the screener column header existing (v3 `window_cols`)."""
from datetime import timedelta

from . import constants as C


def cell(fy, year, field):
    rec = fy.get(year)
    return None if rec is None else rec.get(field)


def window_years(fy, scoring_fy, n):
    """The last n FY labels ending at scoring_fy that exist in the table header."""
    return [y for y in range(scoring_fy - n + 1, scoring_fy + 1) if y in fy]


def select_scoring_fy(fy, d0):
    """§3: latest FY whose results were published >= 63 days before d0.
    Needs each FY record's `results_published` (date). None if no FY qualifies.
    SPEC-SILENT: which FY that is at d0 = the FY-end (Mar 31) is left to the data; the engine takes the
    literal §3 rule (published <= d0 - 63d), so an FY whose results land after d0 is never used."""
    cutoff = d0 - timedelta(days=C.PIT_LAG_DAYS)
    ok = [y for y, r in fy.items() if r.get("results_published") is not None
          and r["results_published"] <= cutoff]
    return max(ok) if ok else None


def last_close_on_or_before(prices, d):
    p = [(dd, pp) for dd, pp in prices if dd <= d]
    return p[-1] if p else None
