#!/usr/bin/env python3
"""Build static JSONs for the calibration dashboard page.

Reads:
  ~/workspace/stock-judging/anchor_calibration/calibration.csv  (backtest rows)
  ~/workspace/stock-judging/forward_tracking/tracking.csv       (live reviews)
  ~/workspace/stock-judging/forward_tracking/snapshots.csv     (weekly prices)

Writes (both mirrors):
  port/frontend/data/calibration.json
  port/frontend/data/forward.json
  port/docs/data/calibration.json
  port/docs/data/forward.json

Re-run after every calibration batch or forward-snapshot refresh.
"""
import csv
import json
import os
import statistics
from datetime import date

WS = os.path.expanduser("~/workspace/stock-judging")
CAL_CSV = os.path.join(WS, "anchor_calibration/calibration.csv")
TRACK_CSV = os.path.join(WS, "forward_tracking/tracking.csv")
SNAP_CSV = os.path.join(WS, "forward_tracking/snapshots.csv")
PORT = os.path.join(WS, "port")

REGIMES = {
    "2020": "COVID crash → raging bull",
    "2023": "Bull",
    "2022": "Sideways/bear",
    "2024": "Late bull → sideways",
    "2018": "Bull",
}


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def pct(n, d):
    return round(100.0 * n / d, 1) if d else None


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(100.0 * statistics.median(xs), 1) if xs else None


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(100.0 * statistics.mean(xs), 1) if xs else None


def corr(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    n = len(pairs)
    if n < 3:
        return None
    mx = sum(p[0] for p in pairs) / n
    my = sum(p[1] for p in pairs) / n
    cov = sum((p[0] - mx) * (p[1] - my) for p in pairs)
    sx = sum((p[0] - mx) ** 2 for p in pairs) ** 0.5
    sy = sum((p[1] - my) ** 2 for p in pairs) ** 0.5
    return round(cov / (sx * sy), 2) if sx * sy else None


def build_calibration():
    rows = []
    with open(CAL_CSV, newline="") as fh:
        for r in csv.DictReader(fh):
            prem = fnum(r.get("premium"))
            ret = fnum(r.get("ret_12m"))
            if prem is None or ret is None:
                continue  # negative-FV rows etc.
            rows.append({
                "premium": prem,
                "ret": ret,
                "maxdd": fnum(r.get("max_dd_12m")),
                "mcap": (r.get("mcap_bucket") or "UNKNOWN").upper(),
                "sector": (r.get("sector") or "UNKNOWN").upper(),
                "year": (r.get("d0") or "")[:4],
            })

    cheap = [r for r in rows if r["premium"] < -0.20]
    overv = [r for r in rows if r["premium"] > 0.20]
    fair = [r for r in rows if -0.20 <= r["premium"] <= 0.20]

    def bucket(lo, hi):
        return [r for r in rows if lo < r["premium"] <= hi]

    buckets = [
        ("+50% and above", bucket(0.50, 999)),
        ("+20% to +50%", bucket(0.20, 0.50)),
        ("±20%", bucket(-0.20, 0.20)),
        ("−20% to −50%", bucket(-0.50, -0.20)),
        ("below −50%", bucket(-999, -0.50)),
    ]

    by_mcap = {}
    for m in ["LARGECAP", "MIDCAP", "SMALLCAP", "MICROCAP"]:
        g = [r for r in rows if r["mcap"] == m]
        c = [r for r in g if r["premium"] < -0.20]
        o = [r for r in g if r["premium"] > 0.20]
        by_mcap[m] = {
            "n": len(g),
            "cheap_hit_pct": pct(sum(1 for r in c if r["ret"] > 0), len(c)),
            "overval_fall_pct": pct(sum(1 for r in o if r["ret"] < 0), len(o)),
            "corr": corr([r["premium"] for r in g], [r["ret"] for r in g]),
        }

    sector_counts = {}
    for r in rows:
        sector_counts[r["sector"]] = sector_counts.get(r["sector"], 0) + 1
    top_sectors = sorted(sector_counts, key=sector_counts.get, reverse=True)[:8]
    by_sector = {}
    for s in top_sectors:
        g = [r for r in rows if r["sector"] == s]
        c = [r for r in g if r["premium"] < -0.20]
        o = [r for r in g if r["premium"] > 0.20]
        by_sector[s] = {
            "n": len(g),
            "cheap_n": len(c),
            "cheap_hit_pct": pct(sum(1 for r in c if r["ret"] > 0), len(c)),
            "overval_n": len(o),
            "overval_fall_pct": pct(sum(1 for r in o if r["ret"] < 0), len(o)),
        }

    by_regime = {}
    years = sorted({r["year"] for r in rows if r["year"]})
    for y in years:
        g = [r for r in rows if r["year"] == y]
        c = [r for r in g if r["premium"] < -0.20]
        o = [r for r in g if r["premium"] > 0.20]
        by_regime[y] = {
            "regime": REGIMES.get(y, "—"),
            "n": len(g),
            "cheap_hit_pct": pct(sum(1 for r in c if r["ret"] > 0), len(c)),
            "overval_fall_pct": pct(sum(1 for r in o if r["ret"] < 0), len(o)),
            "median_ret_pct": med([r["ret"] for r in g]),
        }

    return {
        "n": len(rows),
        "updated_at": date.today().isoformat(),
        "direction": {
            "cheap": {
                "n": len(cheap),
                "rose_pct": pct(sum(1 for r in cheap if r["ret"] > 0), len(cheap)),
                "rose_15_pct": pct(sum(1 for r in cheap if r["ret"] >= 0.15), len(cheap)),
                "median_ret_pct": med([r["ret"] for r in cheap]),
            },
            "overvalued": {
                "n": len(overv),
                "fell_pct": pct(sum(1 for r in overv if r["ret"] < 0), len(overv)),
                "fell_15_pct": pct(sum(1 for r in overv if r["ret"] <= -0.15), len(overv)),
                "median_ret_pct": med([r["ret"] for r in overv]),
            },
            "fair": {
                "n": len(fair),
                "rose_pct": pct(sum(1 for r in fair if r["ret"] > 0), len(fair)),
                "median_ret_pct": med([r["ret"] for r in fair]),
            },
            "premium_ret_corr": corr([r["premium"] for r in rows], [r["ret"] for r in rows]),
        },
        "buckets": [
            {
                "label": label,
                "n": len(b),
                "median_ret_pct": med([r["ret"] for r in b]),
                "mean_ret_pct": mean([r["ret"] for r in b]),
                "median_maxdd_pct": med([r["maxdd"] for r in b]),
            }
            for label, b in buckets
        ],
        "by_mcap": by_mcap,
        "by_sector": by_sector,
        "by_regime": by_regime,
        "standing_rules": [
            'Cheap = buy signal (65% overall, 74% largecap, 100% post-crash). Strongest in IT and FINANCIALS.',
            'Overvalued ≠ sell signal. It means "model can\'t price this" more often than "this will fall." Needs a second reason (distribution, momentum break, event).',
            'Never buy microcap "cheap" on the premium alone (18% hit rate).',
            'In bull markets, ignore the overvalued label for quality compounders (FMCG/PHARMA/IT) — the 15% growth cap mislabels them.',
            'Entry triggers (G1/G2) are rarely touched (~9% hit rate per the v7 trigger study) — use the direction call for timing, not the trigger level.',
        ],
    }


def build_forward():
    tracked = list(csv.DictReader(open(TRACK_CSV, newline="")))
    snaps = list(csv.DictReader(open(SNAP_CSV, newline="")))
    latest = {}
    for s in snaps:
        d = s.get("date", "")
        if d >= latest.get(s["symbol"], ("",))[0]:
            latest[s["symbol"]] = (d, s)

    today = date.today().isoformat()
    out = []
    for t in tracked:
        sym = t["symbol"]
        p0 = fnum(t.get("price_at_review"))
        fv = fnum(t.get("fv"))
        snap = latest.get(sym)
        lp = fnum(snap[1].get("price")) if snap else None
        ret = fnum(snap[1].get("ret_since_review")) if snap else None
        vsfv = fnum(snap[1].get("vs_fv")) if snap else None
        try:
            days = (date.fromisoformat(today) - date.fromisoformat(t["review_date"])).days
        except (ValueError, KeyError):
            days = None
        out.append({
            "symbol": sym,
            "name": t.get("name", sym),
            "category": t.get("category", ""),
            "conviction": fnum(t.get("conviction")),
            "review_date": t.get("review_date", ""),
            "price_at_review": p0,
            "fv": fv,
            "latest_price": lp,
            "ret_since_review": round(ret * 100, 1) if ret is not None else None,
            "vs_fv": round(vsfv * 100, 1) if vsfv is not None else None,
            "days_tracked": days,
        })
    out.sort(key=lambda r: (r["ret_since_review"] is None, -(r["ret_since_review"] or 0)))
    return {"updated_at": today, "n": len(out), "companies": out}


def main():
    cal = build_calibration()
    fwd = build_forward()
    for root in (os.path.join(PORT, "frontend"), os.path.join(PORT, "docs")):
        d = os.path.join(root, "data")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "calibration.json"), "w") as fh:
            json.dump(cal, fh, indent=1)
        with open(os.path.join(d, "forward.json"), "w") as fh:
            json.dump(fwd, fh, indent=1)
    print(f"calibration.json: n={cal['n']} rows -> frontend/data + docs/data")
    print(f"forward.json: n={fwd['n']} companies -> frontend/data + docs/data")


if __name__ == "__main__":
    main()
