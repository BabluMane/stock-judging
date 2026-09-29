#!/usr/bin/env python3
"""Fetch full-history financials + price/PE/EPS chart series + top ratios
for all 13 v3.9 OOS companies, directly from screener.in (real data, PIT
methodology matches validation/v3_8_oos/fetch_full_financials.py)."""
import json
import re
import subprocess
import sys
import time

COMPANIES = {
    "asianpaint": ("ASIANPAINT", "consolidated", 295),
    "hdfcbank": ("HDFCBANK", "consolidated", 1298),
    "nestleind": ("NESTLEIND", "consolidated", 2236),
    "britannia": ("BRITANNIA", "consolidated", 553),
    "havells": ("HAVELLS", "consolidated", 1288),
    "bhartiartl": ("BHARTIARTL", "consolidated", 467),
    "tatasteel": ("TATASTEEL", "consolidated", 3373),
    "ntpc": ("NTPC", "consolidated", 2303),
    "tatamotors": ("TMPV", "consolidated", 3370),  # retained the original pre-2024-demerger listed entity/history
    "bankbaroda": ("BANKBARODA", "consolidated", 395),
    "zeel": ("ZEEL", "consolidated", 3788),
    "relcapital": ("RELCAPITAL", "consolidated", 2722),
    "ilfstransport": ("IL&FSTRANS", "", 1404),
}

SECTION_IDS = ["profit-loss", "quarters", "balance-sheet", "cash-flow", "ratios",
               "shareholding", "peers", "documents", "analysis"]


def fetch(url):
    r = subprocess.run(["curl", "-s", url], capture_output=True, text=True, timeout=60)
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
        tr = m.group(1)
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
        if not tds:
            continue
        raw_label = re.sub(r'<[^>]+>', '', tds[0]).strip()
        vals = [re.sub(r'<[^>]+>', '', c).strip() for c in tds[1:]]
        if raw_label and vals:
            rows[raw_label] = vals
    return {"years": years, "rows": rows}


def parse_top_ratios(html):
    idx = html.find('id="top-ratios"')
    if idx < 0:
        return {}
    seg = html[idx:idx + 4000]
    out = {}
    for m in re.finditer(r'<li[^>]*>\s*<span class="name">([^<]+)</span>\s*<span class="(?:nowrap )?value">(.*?)</span>', seg, re.S):
        label = m.group(1).strip()
        val = re.sub(r'<[^>]+>', ' ', m.group(2)).strip()
        val = re.sub(r'\s+', ' ', val)
        out[label] = val
    return out


def main():
    fin_out = {}
    top_ratios_out = {}
    for slug, (cid, variant, sid) in COMPANIES.items():
        path = f"/{variant}/" if variant else "/"
        url = f"https://www.screener.in/company/{cid}{path}"
        html = fetch(url)
        pnl = parse_table(html, "profit-loss")
        bs = parse_table(html, "balance-sheet")
        cf = parse_table(html, "cash-flow")
        ratios_tbl = parse_table(html, "ratios")
        top_ratios_out[slug] = parse_top_ratios(html)
        fin_out[slug] = {"url": url, "screener_id": sid, "profit_loss": pnl,
                          "balance_sheet": bs, "cash_flow": cf, "ratios_table": ratios_tbl}
        print(slug, "pnl_years=", pnl["years"] if pnl else None,
              "bs_years=", bs["years"] if bs else None, file=sys.stderr)
        time.sleep(0.5)
    json.dump(fin_out, open("full_financials_raw_v39.json", "w"), indent=1, ensure_ascii=False)
    json.dump(top_ratios_out, open("top_ratios_v39.json", "w"), indent=1, ensure_ascii=False)
    print("wrote full_financials_raw_v39.json, top_ratios_v39.json")


if __name__ == "__main__":
    main()
