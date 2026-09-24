#!/usr/bin/env python3
"""Re-fetch full-history P&L/Balance-Sheet tables directly from screener.in for
all 13 OOS companies (the mediocrity-group agent's dcf_financials/*.json only
captured a truncated recent-5yr window -- this repairs that gap so every
company has real point-in-time data covering its scoring dates, not just
today's trailing window)."""
import json
import re
import subprocess
import sys

COMPANIES = {
    "titan": ("TITAN", "consolidated"),
    "divislab": ("DIVISLAB", "consolidated"),
    "pageind": ("PAGEIND", ""),
    "dmart": ("DMART", "consolidated"),
    "polycab": ("POLYCAB", "consolidated"),
    "colpal": ("COLPAL", ""),
    "ashokley": ("ASHOKLEY", "consolidated"),
    "cipla": ("CIPLA", "consolidated"),
    "coalindia": ("COALINDIA", "consolidated"),
    "gail": ("GAIL", "consolidated"),
    "pcjeweller": ("PCJEWELLER", "consolidated"),
    "fretail": ("FRETAIL", "consolidated"),
    "cgpower": ("CGPOWER", "consolidated"),
}


def fetch(url):
    r = subprocess.run(["curl", "-s", url], capture_output=True, text=True, timeout=60)
    return r.stdout


def parse_table(html, section_id):
    idx = html.find(f'id="{section_id}"')
    if idx < 0:
        return None
    # table ends at the next "id=" section marker or a reasonable window
    seg = html[idx:idx + 40000]
    end = seg.find('id="', 400)
    seg = seg[:end] if end > 0 else seg[:25000]
    ths = [t.strip() for t in re.findall(r'<th[^>]*>(.*?)</th>', seg, re.S)]
    years = [t for t in ths if re.match(r'(Mar|Dec|TTM|Sep|Jun)\s*\d{0,4}$', t.strip())]
    rows = {}
    for m in re.finditer(r'<tr[^>]*>(.*?)</tr>', seg, re.S):
        tr = m.group(1)
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
        if not tds:
            continue
        label_m = re.search(r'>([^<]+)</button>|<td[^>]*class="text"[^>]*>\s*([^<]+)', tds[0])
        raw_label = re.sub(r'<[^>]+>', '', tds[0]).strip()
        vals = [re.sub(r'<[^>]+>', '', c).strip() for c in tds[1:]]
        if raw_label and vals:
            rows[raw_label] = vals
    return {"years": years, "rows": rows}


def main():
    out = {}
    for slug, (cid, variant) in COMPANIES.items():
        path = f"/{variant}/" if variant else "/"
        url = f"https://www.screener.in/company/{cid}{path}"
        html = fetch(url)
        pnl = parse_table(html, "profit-loss")
        bs = parse_table(html, "balance-sheet")
        cf = parse_table(html, "cash-flow")
        out[slug] = {"url": url, "profit_loss": pnl, "balance_sheet": bs, "cash_flow": cf}
        print(slug, "pnl_years=", pnl["years"] if pnl else None, file=sys.stderr)
    json.dump(out, open("full_financials_raw.json", "w"), indent=1, ensure_ascii=False)
    print("wrote full_financials_raw.json")


if __name__ == "__main__":
    main()
