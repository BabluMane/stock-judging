"""Synthetic name-date builder for the v4 unit tests (no real data; no prior set is run)."""
import copy
from datetime import date, timedelta


D0 = date(2019, 3, 31)
SCORING_FY = 2018            # results published 2018-05-20 (>= 63d before D0)


def fy_records():
    fy = {}
    for i, y in enumerate(range(2014, 2019)):
        g = 1.1 ** i
        fy[y] = {
            "sales": 1000 * g, "opm_pct": 20.0, "depreciation": 30 * g, "net_profit": 120 * g,
            "eps": 12 * g, "equity_capital": 50.0, "reserves": 500.0 + 100 * i,
            "dividend_payout_pct": 30.0, "total_assets": 1500.0 + 150 * i,
            "current_assets": 600.0 + 80 * i, "current_liabilities": 400.0 + 30 * i,
            "pbt": 160 * g, "interest": 10.0 - i, "borrowings": 200.0 - 20 * i, "investments": 50.0,
            "cfo": 150 * g, "raw_material_pct": 40.0 - i,
            "results_published": date(y, 5, 20),
        }
    return fy


def weekly(start, end, fn):
    out, d = [], start
    while d <= end:
        out.append((d, fn(d)))
        d += timedelta(days=7)
    return out


def flat_prices(level=100.0, start=date(2017, 3, 31), end=date(2021, 6, 4)):
    return weekly(start, end, lambda d: level)


def quarters(n=12, pledged=0.0, end=D0):
    out, d = [], end
    for _ in range(n):
        out.append({"quarter_end": d, "pledged_pct": pledged, "promoter_holding_pct": 50.0})
        d = date(d.year - 1, 12, 31) if d.month == 3 else (date(d.year, d.month - 3, 30 if d.month - 3 in (6, 9) else 31))
    return sorted(out, key=lambda q: q["quarter_end"])


def eps_series():
    return [(date(2018, 5, 20), 12.3 * 1.1 ** 4), (date(2018, 6, 15), 12.5 * 1.1 ** 4)]


def make_nd(**over):
    from engine_v4.run import NameDate
    kw = dict(key="acme_2019-03-31", d0=D0, sector="Consumer", beta=1.0, fy=fy_records(),
              prices=flat_prices(), mcap_cr=10000.0, mcap_price=100.0, pledge=quarters(),
              eps_series=eps_series(), corp_actions=[], events=[], audited_prints=[],
              category="winner", as_of=date(2021, 6, 4))
    kw.update(over)
    return NameDate(**kw)


def with_prices(nd, edits):
    """edits: {date: price} overriding the flat series."""
    nd = copy.copy(nd)
    nd.prices = [(d, edits.get(d, p)) for d, p in nd.prices]
    return nd
