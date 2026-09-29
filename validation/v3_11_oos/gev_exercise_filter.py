#!/usr/bin/env python3
"""GEV-exercise filter for the v3.11 blow-up candidates (specs/V3_11_DELTA.md,
"New rule -- GEV must be genuinely exercised").

FIREWALL: imports the FROZEN v3.10 valuation functions unmodified from
validation/v3_10_oos/run_v310_validation.py and computes ONLY fair value/share
and price-vs-fair-value diagnostics for candidate blow-up name-dates. It does
NOT run usability, QFV, GEV, fill simulation or any scorecard, and it asserts
no outcome. It selects which names are tested; nothing more.

Filter (per candidate name-date, scoring date d0 = FY-end 31-Mar):
  PASS iff  FV/share > 0   AND   min weekly close in (d0, d0+24m] <= 1.10 x ACC trigger
  where ACC trigger = 0.875 x FV (lowest-bar-to-hit tier that exists for every
  name; QFV is not evaluated here). 'touch' = first weekly close <= ACC trigger
  (diagnostic date only -- not a fill).
Assumption (filter only): beta 1.15 for every candidate (v3.10 blow-up-bucket
style). The validation session fixes its own betas before any run; FV here is
non-decisional.

Usage: python3 gev_exercise_filter.py DATA_DIR   (DATA_DIR is scratch, outside repo;
       it is populated from screener.in on first run)
"""
import json, os, re, sys, time
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "v3_10_oos"))
import fetch_data_v310 as fx          # frozen fetch helpers (screener parsing)
import run_v310_validation as r       # frozen valuation

CANDS = ["SREINFRA", "RELIGARE", "RELINFRA", "RPOWER", "ROLTA", "JPASSOCIAT", "FORTIS", "RCOM",
         "EROSMEDIA", "SUZLON", "UNITECH", "BALLARPUR", "HDIL", "RHFL", "SINTEX", "DISHTV",
         "SADBHAV", "GAYAPROJ", "ABAN", "GTLINFRA", "MCLEODRUSS", "PARSVNATH", "EDUCOMP", "KSK",
         "IFCI", "KOHINOOR", "JYOTISTRUC", "PUNJLLOYD"]
FIN_VARIANT = {"sreinfra", "religare", "rhfl"}
YEARS = (2019, 2020, 2021, 2022, 2023)


def fetch(data):
    fin, top = {}, {}
    for sym in CANDS:
        slug = sym.lower()
        html = fx.curl(f"https://www.screener.in/company/{sym}/consolidated/")
        t, var = fx.page_tables(html), "consolidated"
        if not fx.has_pnl(t):
            html = fx.curl(f"https://www.screener.in/company/{sym}/")
            t, var = fx.page_tables(html), "standalone"
        m = re.search(r'data-company-id="(\d+)"', html)
        if not m or not fx.has_pnl(t):
            print("skip (not on screener):", sym, file=sys.stderr)
            continue
        cid = int(m.group(1))
        top[slug] = fx.parse_top_ratios(html)
        fin[slug] = {"variant": var, "screener_id": cid, **t}
        fx.HERE = data
        fx.fetch_series(slug, cid, var == "consolidated")
        time.sleep(0.5)
    json.dump(fin, open(f"{data}/fin.json", "w"))
    json.dump(top, open(f"{data}/top.json", "w"))


def main():
    data = sys.argv[1]
    os.makedirs(data, exist_ok=True)
    if not os.path.exists(f"{data}/fin.json"):
        fetch(data)
    r.HERE = data
    fin, top = json.load(open(f"{data}/fin.json")), json.load(open(f"{data}/top.json"))
    for s in fin:
        r.SECTOR_BETA[s] = 1.15
    out = []
    print(f"{'name-date':26s} {'model':6s} {'FV/sh':>9s} {'px@d0':>8s} {'P/FV':>6s} {'minP/FV':>8s} {'first close<=0.875FV':>21s}  filter")
    for slug in fin:
        for y in YEARS:
            fy, d0 = f"Mar {y}", date(y, 3, 31)
            key = f"{slug}_{d0}"
            try:
                v, err = r.value_name_date(fin, top, slug, fy, d0, slug in FIN_VARIANT, r.load_prices(slug))
            except Exception as e:  # recorded, never swallowed silently
                out.append({"name_date": key, "filter": "N/A", "reason": repr(e)[:80]}); continue
            if v is None:
                out.append({"name_date": key, "filter": "N/A", "reason": err}); continue
            fv = v["fv"]
            if fv <= 0:
                out.append({"name_date": key, "filter": "FAIL", "reason": "FV<=0", "fv": round(fv, 2)}); continue
            prices = r.load_prices(slug)
            win = [(d, p) for d, p, _ in prices if d0 < d <= d0 + r.DAYS24M]
            acc = 0.875 * fv
            touch = next((d.isoformat() for d, p in win if p <= acc), None)
            near = bool(win) and min(p for _, p in win) <= 1.10 * acc
            out.append({"name_date": key, "model": "ER" if slug in FIN_VARIANT else "DCF", "filter": "PASS" if near else "FAIL",
                        "fv": round(fv, 2), "price_d0": v["price_at_d0"], "p_over_fv_d0": round(v["price_over_fv_d0"], 2),
                        "min_close_over_fv": round(v["min_close_24m_over_fv"], 3), "first_close_le_acc_trigger": touch})
    for o in out:
        if "fv" in o and "price_d0" in o:
            print(f"{o['name_date']:26s} {o['model']:6s} {o['fv']:9.1f} {o['price_d0']:8.2f} {o['p_over_fv_d0']:6.2f} {o['min_close_over_fv']:8.3f} {str(o['first_close_le_acc_trigger']):>21s}  {o['filter']}")
        else:
            print(f"{o['name_date']:26s} {o['filter']:6s} {o.get('reason','')}")
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gev_exercise_filter_results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
