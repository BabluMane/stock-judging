#!/usr/bin/env python3
"""Fill-plausibility firewall for the v4 OOS blow-up candidates (V4_SPEC §8.2 pre-condition 2).

FIREWALL (per the Phase-C task): this script imports the FROZEN engine_v4 anchor unmodified
and computes ONLY the two numbers §8.2 pre-condition 2 needs -- P_d0 (last adjusted close at or
before the scoring date) and the tier-1 trigger P_G1 = V(g_h(0.875)) -- and tests
P_d0 <= 2.0 x P_G1 (engine_v4.anchor.fill_plausible). It selects WHICH blow-up dates are tested;
it asserts no outcome. It does NOT run the distress screen (§3), usability (§4), the event lane
(§5), the exit scan, the fill simulation, or any aggregation, and it never reads a forward price
(only closes at or before d0 are used). Only the fields named in OUT_FIELDS are emitted -- the
reporting-only g_implied solver output and the V(g_sus) diagnostic that value_anchor also returns
are dropped before anything is written or printed.

Inputs (all free, as V4_SPEC §0): screener.in company page (profit-loss / balance-sheet tables,
top ratios) and screener.in chart API (price series). Nothing is committed but the result table.
Scratch cache: argv[1] (outside the repo).

Conventions (each carried from the frozen v3.10/v3.11 runner or the engine_v4 build notes):
  * shares = screener Market Cap / Current Price (frozen v3.8-v3.11 method; engine_v4 takes the
    pair as an input, nothing else is used to size the share count).
  * scoring FY = engine_v4.pit.select_scoring_fy: latest FY whose results were published >= 63 days
    before d0. `results_published` for a screener FY column is NOT in the screener tables, so the
    NOMINAL date FY-end + 60 days (the SEBI LODR outer limit for audited annual results) is used
    here. For d0 = 31-Mar-N this selects FY(N-1). A blow-up that filed FY(N-1) after d0-63d would
    fall back to FY(N-2); that is a per-name-date PIT verification item in the pre-reg, not
    something this certification can settle.
  * beta 1.15 for every candidate (blow-up bucket, V310-C9). The pre-reg freezes it per name.
  * class split: V4_SPEC §3 says "screener.in Sector in {Banks, Finance}". screener.in has since re-cut its
    taxonomy into Broad Sector > Sector > Broad Industry > Industry; the labels "Banks" and "Finance" now
    sit at the Broad Industry level (Sector is "Financial Services" for both). The spec's stated coverage
    (banks, NBFCs, HFCs) is preserved by reading Broad Industry in {Banks, Finance} -> financial
    (inverse excess-return) variant. The reading is frozen in V4_OOS_PREREG.md.
"""
import csv
import json
import os
import re
import sys
import time
from datetime import date, timedelta

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, REPO)
sys.path.insert(0, os.path.join(REPO, "validation", "v3_11_oos"))
import fetch_data_v311 as fx                      # frozen screener parsing helpers (read-only import)
from engine_v4 import anchor, constants as C     # frozen v4 build (read-only import)
from engine_v4.pit import select_scoring_fy, last_close_on_or_before

BETA = 1.15
OUT_FIELDS = ("name_date", "symbol", "sector", "model", "beta", "scoring_fy", "p_d0", "p_g1",
              "p_d0_over_p_g1", "fill_plausible", "note")


def num(s):
    if s is None or s == "":
        return None
    try:
        return float(str(s).replace(",", "").replace("%", "").replace("₹", "").strip())
    except ValueError:
        return None


def get_company(sym, cache):
    path = os.path.join(cache, f"{sym}.json")
    if os.path.exists(path):
        return json.load(open(path))
    html, variant = None, None
    for v, url in (("consolidated", f"https://www.screener.in/company/{sym}/consolidated/"),
                   ("standalone", f"https://www.screener.in/company/{sym}/")):
        h = fx.curl(url)
        t = fx.page_tables(h)
        if fx.has_pnl(t):
            html, variant = h, v
            break
    if html is None:
        rec = {"symbol": sym, "error": "no profit-loss table on screener (consolidated or standalone)"}
        json.dump(rec, open(path, "w"))
        return rec
    m = re.search(r'data-company-id="(\d+)"', html)
    cls = {k: (re.search(r'title="%s"[^>]*>([^<]+)<' % k, html) or [None, None])[1]
           for k in ("Broad Sector", "Sector", "Broad Industry", "Industry")}
    name = re.search(r'overflow-wrap-anywhere">([^<]+)<', html)
    price = {}
    try:
        _, dp = fx.chart(int(m.group(1)), "Price-DMA50-DMA200-Volume", variant == "consolidated")
        price = {ds["metric"]: ds["values"] for ds in dp["datasets"]}.get("Price", [])
    except Exception as e:  # recorded, never swallowed silently
        price = []
        err = repr(e)[:100]
    rec = {"symbol": sym, "name": name.group(1).strip() if name else None, "variant": variant,
           "screener_id": int(m.group(1)) if m else None, "classification": cls,
           "top": fx.parse_top_ratios(html), "price": price, **fx.page_tables(html)}
    json.dump(rec, open(path, "w"))
    time.sleep(0.6)
    return rec


def col(tbl, row, label):
    if not tbl or row not in tbl["rows"]:
        return None
    vals = tbl["rows"][row]
    yrs = tbl["years"][:len(vals)]
    return num(vals[yrs.index(label)]) if label in yrs else None


def build_fy(rec):
    pnl, bs = rec["profit_loss"], rec["balance_sheet"]
    fy = {}
    for lab in pnl["years"]:
        if not lab.startswith("Mar"):
            continue
        y = int(lab.split()[1])
        fy[y] = {
            "sales": col(pnl, "Sales&nbsp;+", lab), "opm_pct": col(pnl, "OPM %", lab),
            "depreciation": col(pnl, "Depreciation", lab), "net_profit": col(pnl, "Net Profit&nbsp;+", lab),
            "dividend_payout_pct": col(pnl, "Dividend Payout %", lab),
            "equity_capital": col(bs, "Equity Capital", lab), "reserves": col(bs, "Reserves", lab),
            "investments": col(bs, "Investments", lab), "borrowings": col(bs, "Borrowings&nbsp;+", lab),
            "results_published": date(y, 3, 31) + timedelta(days=60),   # NOMINAL (see module docstring)
        }
    return fy


def certify(sym, y, cache):
    """One name-date d0 = 31-Mar-y. Returns a row containing only OUT_FIELDS."""
    d0 = date(y, 3, 31)
    row = {k: None for k in OUT_FIELDS}
    row.update(name_date=f"{sym.lower()}_{d0}", symbol=sym, beta=BETA)
    rec = get_company(sym, cache)
    if "error" in rec:
        row["note"] = rec["error"]
        return row
    cls = rec.get("classification") or {}
    row["sector"] = " > ".join(str(cls.get(k)) for k in ("Sector", "Broad Industry", "Industry"))
    fy = build_fy(rec)
    sfy = select_scoring_fy(fy, d0)
    row["scoring_fy"] = sfy
    prices = sorted((date.fromisoformat(d[:10]), num(p)) for d, p in rec["price"] if num(p) is not None)
    p0 = last_close_on_or_before(prices, d0)
    if p0 is None or (d0 - p0[0]).days > 10:
        row["note"] = "no close within 10d at/before d0 (listing gap)"
        return row
    mcap, px = num(rec["top"].get("Market Cap")), num(rec["top"].get("Current Price"))
    is_fin = cls.get("Broad Industry") in C.FINANCIAL_SECTORS
    row["model"] = "financial (excess-return)" if is_fin else "non-financial (FCFF)"
    if sfy is None:
        row["note"] = "no FY published >=63d before d0 (nominal dates)"
        return row
    out = anchor.value_anchor(fy, sfy, is_fin, BETA, mcap, px, p0[1])
    if not out["valued"]:
        row["note"] = f"not valued: {out['reason']}"
        row["p_d0"] = round(p0[1], 2)
        return row
    p_g1 = out["trigger"]["G1"] if "G1" in out["trigger"] else out["trigger"][next(iter(out["trigger"]))]
    row.update(p_d0=round(p0[1], 2), p_g1=round(p_g1, 2),
               p_d0_over_p_g1=round(p0[1] / p_g1, 3) if p_g1 and p_g1 > 0 else None,
               fill_plausible=bool(anchor.fill_plausible(p0[1], p_g1)))
    if p_g1 is None or p_g1 <= 0:
        row["note"] = "non-positive P_G1 -> not fill-plausible"
    return row


def main():
    cache = sys.argv[1]
    os.makedirs(cache, exist_ok=True)
    syms = sys.argv[2].split(",")
    years = [int(x) for x in (sys.argv[3] if len(sys.argv) > 3 else "2019,2020,2021").split(",")]
    rows = []
    for s in syms:
        for y in years:
            rows.append(certify(s, y, cache))
    for r in rows:
        print("{:24s} {:9s} FY{} P_d0={} P_G1={} ratio={} plausible={} {}".format(
            r["name_date"], (r["model"] or "-")[:9], r["scoring_fy"], r["p_d0"], r["p_g1"],
            r["p_d0_over_p_g1"], r["fill_plausible"], r["note"] or ""))
    if len(sys.argv) > 4:
        json.dump(rows, open(sys.argv[4], "w"), indent=1)


if __name__ == "__main__":
    main()
