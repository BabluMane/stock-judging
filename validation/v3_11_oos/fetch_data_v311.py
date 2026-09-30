#!/usr/bin/env python3
"""Fetch fresh data for the 13 v3.11 OOS companies (25 name-dates).

Method = validation/v3_9_oos/fetch_full_financials_v39.py (screener.in company
page: profit-loss / balance-sheet / cash-flow / ratios / top-ratios) plus the
screener chart API for the weekly price/PE and publication-dated TTM EPS
series (validation/v3_8_oos/NOTES.md method). Nothing beyond the windows in
OOS_SET_PREREG.md is *used* downstream; the raw page tables are stored whole,
as in v3.9.

Variant rule (uniform, decided before looking at any figure): use the
screener CONSOLIDATED view if it parses to a profit-loss table with a
Net Profit row; otherwise the standalone page. The chart API is queried with
consolidated=true iff the consolidated view was chosen, so the vendor TTM-EPS
series and the audited EPS row are on the same basis.

Corporate actions: screener has no split/bonus table; BSE/NSE APIs return 403
and pocketful.in is now client-rendered. Splits/bonuses (Yahoo reports both
as split events) are taken from Yahoo Finance's public chart-events feed,
disclosed as a deviation from "screener only" in the result doc.
"""
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

# slug -> (screener symbol, screener company id (from page), yahoo symbol)
COMPANIES = {
    "tvsmotor": ("TVSMOTOR", 3502, "TVSMOTOR.NS"),
    "jublfood": ("JUBLFOOD", 1658, "JUBLFOOD.NS"),
    "tiindia": ("TIINDIA", 1274187, "TIINDIA.NS"),
    "kei": ("KEI", 1744, "KEI.NS"),
    "pidilite": ("PIDILITIND", 2478, "PIDILITIND.NS"),
    "emami": ("EMAMILTD", 918, "EMAMILTD.NS"),
    "marico": ("MARICO", 2014, "MARICO.NS"),
    "ongc": ("ONGC", 2320, "ONGC.NS"),
    "sunpharma": ("SUNPHARMA", 3245, "SUNPHARMA.NS"),
    "nhpc": ("NHPC", 2254, "NHPC.NS"),
    "gayatri": ("GAYAPROJ", 1107, "GAYAPROJ.NS"),
    "sadbhav": ("SADBHAV", 2829, "SADBHAV.NS"),
    "srei": ("SREINFRA", 3161, "SREINFRA.NS"),
}

SECTION_IDS = ["profit-loss", "quarters", "balance-sheet", "cash-flow", "ratios",
               "shareholding", "peers", "documents", "analysis"]


def curl(url, ua=None):
    cmd = ["curl", "-s", "-L", "-m", "60"]
    if ua:
        cmd += ["-A", ua]
    r = subprocess.run(cmd + [url], capture_output=True, text=True)
    return r.stdout


def parse_table(html, section_id):
    idx = html.find(f'id="{section_id}"')
    if idx < 0:
        return None
    seg = html[idx:idx + 60000]
    end = None
    for sid in SECTION_IDS:
        if sid == section_id:
            continue
        m = seg.find(f'id="{sid}"', 300)
        if m > 0 and (end is None or m < end):
            end = m
    seg = seg[:end] if end else seg[:40000]
    ths = [re.sub(r'<[^>]+>', '', t).strip() for t in re.findall(r'<th[^>]*>(.*?)</th>', seg, re.S)]
    years = [t for t in ths if re.match(r'(Mar|Dec|TTM|Sep|Jun)\s*\d{0,4}', t.strip())]
    rows = {}
    for m in re.finditer(r'<tr[^>]*>(.*?)</tr>', seg, re.S):
        tds = re.findall(r'<td[^>]*>(.*?)</td>', m.group(1), re.S)
        if not tds:
            continue
        label = re.sub(r'<[^>]+>', '', tds[0]).strip()
        vals = [re.sub(r'<[^>]+>', '', c).strip() for c in tds[1:]]
        if label and vals:
            rows[label] = vals
    return {"years": years, "rows": rows}


def parse_top_ratios(html):
    idx = html.find('id="top-ratios"')
    if idx < 0:
        return {}
    seg = html[idx:idx + 4000]
    out = {}
    for m in re.finditer(r'<li[^>]*>\s*<span class="name">([^<]+)</span>\s*<span class="(?:nowrap )?value">(.*?)</span>', seg, re.S):
        val = re.sub(r'<[^>]+>', ' ', m.group(2)).strip()
        out[m.group(1).strip()] = re.sub(r'\s+', ' ', val)
    return out


def page_tables(html):
    return {
        "profit_loss": parse_table(html, "profit-loss"),
        "balance_sheet": parse_table(html, "balance-sheet"),
        "cash_flow": parse_table(html, "cash-flow"),
        "ratios_table": parse_table(html, "ratios"),
    }


def has_pnl(t):
    p = t["profit_loss"]
    return bool(p and p["years"] and any(k.startswith("Net Profit") for k in p["rows"]))


def chart(cid, q, consolidated):
    url = f"https://www.screener.in/api/company/{cid}/chart/?q={q}&days=6300" + ("&consolidated=true" if consolidated else "")
    return url, json.loads(curl(url))


def fetch_series(slug, cid, consolidated):
    url_p, dp = chart(cid, "Price-DMA50-DMA200-Volume", consolidated)
    url_e, de = chart(cid, "Price+to+Earning-Median+PE-EPS", consolidated)
    price = {ds["metric"]: ds["values"] for ds in dp["datasets"]}["Price"]
    ded = {ds["metric"]: ds["values"] for ds in de["datasets"]}
    pe = {d: v for d, v in ded.get("Price to Earning", [])}
    os.makedirs(f"{HERE}/pe_series", exist_ok=True)
    os.makedirs(f"{HERE}/eps_series", exist_ok=True)
    with open(f"{HERE}/pe_series/{slug}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "price", "pe"])
        for d, p in price:
            w.writerow([d, p, pe.get(d, "")])
    json.dump({"source": url_e, "symbol": slug, "metric": "EPS", "label": "TTM EPS",
               "note": "vendor publication-dated TTM EPS series as fetched, raw",
               "price_source": url_p, "values": ded.get("EPS", [])},
              open(f"{HERE}/eps_series/{slug}.json", "w"), indent=1)
    return len(price), len(ded.get("EPS", []))


def fetch_actions(slug, ysym):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ysym}?range=max&interval=1mo&events=splits%7Cdiv"
    try:
        d = json.loads(curl(url, ua="Mozilla/5.0"))
        res = d["chart"]["result"][0]
        splits = (res.get("events") or {}).get("splits") or {}
        acts = []
        for ts, s in sorted(splits.items(), key=lambda kv: int(kv[0])):
            ex = dt.datetime.fromtimestamp(int(s["date"]), dt.timezone.utc).date().isoformat()
            acts.append({"ex_date": ex, "numerator": s["numerator"], "denominator": s["denominator"],
                         "ratio_text": s.get("splitRatio"),
                         "note": "Yahoo reports splits and bonuses alike as split events (ratio = new:old shares)"})
        first = res["meta"].get("firstTradeDate")
        return {"source": url, "status": "ok", "yahoo_first_trade": first and dt.datetime.fromtimestamp(first, dt.timezone.utc).date().isoformat(),
                "actions": acts}
    except Exception as e:  # noqa: BLE001 - recorded, never silently swallowed
        return {"source": url, "status": f"unavailable: {type(e).__name__}: {str(e)[:120]}", "actions": []}


def main():
    fin_out, top_out, meta = {}, {}, {}
    os.makedirs(f"{HERE}/corp_actions", exist_ok=True)
    for slug, (sym, cid, ysym) in COMPANIES.items():
        url_c = f"https://www.screener.in/company/{sym}/consolidated/"
        html = curl(url_c)
        tbl = page_tables(html)
        variant, url = "consolidated", url_c
        if not has_pnl(tbl):
            url = f"https://www.screener.in/company/{sym}/"
            html = curl(url)
            tbl = page_tables(html)
            variant = "standalone"
        m = re.search(r'data-company-id="(\d+)"', html)
        assert m and int(m.group(1)) == cid, (slug, m and m.group(1), cid)
        top_out[slug] = parse_top_ratios(html)
        fin_out[slug] = {"url": url, "variant": variant, "screener_id": cid, **tbl}
        n_p, n_e = fetch_series(slug, cid, variant == "consolidated")
        ca = fetch_actions(slug, ysym)
        json.dump({"symbol": sym, **ca}, open(f"{HERE}/corp_actions/{slug}.json", "w"), indent=1)
        meta[slug] = {"variant": variant, "price_pts": n_p, "eps_pts": n_e, "actions": len(ca["actions"]),
                      "actions_status": ca["status"], "pnl_years": (tbl["profit_loss"] or {}).get("years")}
        print(slug, meta[slug], file=sys.stderr)
        time.sleep(0.5)
    json.dump(fin_out, open(f"{HERE}/full_financials_raw_v311.json", "w"), indent=1, ensure_ascii=False)
    json.dump(top_out, open(f"{HERE}/top_ratios_v311.json", "w"), indent=1, ensure_ascii=False)
    json.dump({"fetched_on": dt.date.today().isoformat(), "companies": meta},
              open(f"{HERE}/fetch_meta_v311.json", "w"), indent=1)
    print("done")


if __name__ == "__main__":
    main()
