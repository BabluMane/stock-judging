#!/usr/bin/env python3
"""Build frontend-v2/data/marquee.json — Marquee Investors tab data.

Sources:
  master_dataset/named_holders.parquet  (current >1% holdings)
  master_dataset/pledge.parquet          (latest pledged %)
  master_dataset/prices/<SYM>_NS.parquet (sparkline closes)
  v2_scorer/v2_1_results.json            (our composite scores)
  promise-tracking/audits/*.json        (credibility scores)
  port/reviews/*.json                   (company display names)
  frontend-v2/data/investor_activity.json (recent moves feed)

Run:  python3 tools/build_marquee_json.py
Out:  ../data/marquee.json
"""
import json
import os
import sys
from datetime import date

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
FRONTEND_V2 = os.path.dirname(HERE)
PORT = os.path.dirname(FRONTEND_V2)
SJ = os.path.dirname(PORT)

sys.path.insert(0, os.path.join(SJ, "promise-tracking"))

NAMED_HOLDERS = os.path.join(SJ, "master_dataset", "named_holders.parquet")
PLEDGE = os.path.join(SJ, "master_dataset", "pledge.parquet")
PRICES_DIR = os.path.join(SJ, "master_dataset", "prices")
RESULTS = os.path.join(SJ, "v2_scorer", "v2_1_results.json")
AUDITS_DIR = os.path.join(SJ, "promise-tracking", "audits")
REVIEWS_DIR = os.path.join(PORT, "reviews")
ACTIVITY = os.path.join(FRONTEND_V2, "data", "investor_activity.json")
OUT = os.path.join(FRONTEND_V2, "data", "marquee.json")

INVESTORS = [
    {
        "id": "kacholia",
        "name": "Ashish Kacholia",
        "type": "Individual investor",
        "pattern": "KACHOLIA",
        "note": "No >1% positions in our 200-stock universe — tracked via deal flow.",
    },
    {
        "id": "mukul",
        "name": "Mukul Agrawal",
        "type": "Individual investor",
        "pattern": "MUKUL",
        "note": None,
    },
    {
        "id": "quant",
        "name": "Quant Mutual Fund",
        "type": "AMC",
        "pattern": "QUANT MUTUAL FUND",
        "note": None,
    },
    {
        "id": "nomura",
        "name": "Nomura India Investment Fund",
        "type": "FII",
        "pattern": "NOMURA",
        "note": None,
    },
]

# Fallback display names for held symbols with no review card.
NAME_FALLBACK = {
    "AUROPHARMA": "Aurobindo Pharma Ltd",
    "PREMIERENE": "Premier Energies Ltd",
    "MOTHERSON": "Samvardhana Motherson International Ltd",
    "ADANIGREEN": "Adani Green Energy Ltd",
    "TATACOMM": "Tata Communications Ltd",
    "LICHSGFIN": "LIC Housing Finance Ltd",
    "ZYDUSLIFE": "Zydus Lifesciences Ltd",
    "ADANIENT": "Adani Enterprises Ltd",
    "HDFCLIFE": "HDFC Life Insurance Co Ltd",
    "ADANIPOWER": "Adani Power Ltd",
    "AUBANK": "AU Small Finance Bank Ltd",
    "KALYANKJIL": "Kalyan Jewellers India Ltd",
}


def review_slug(symbol):
    return "".join(c for c in str(symbol).lower() if c.isalnum())


def load_review_names():
    names = {}
    if not os.path.isdir(REVIEWS_DIR):
        return names
    for fn in os.listdir(REVIEWS_DIR):
        if not fn.endswith(".json"):
            continue
        try:
            with open(os.path.join(REVIEWS_DIR, fn)) as f:
                d = json.load(f)
            sym = d.get("symbol")
            name = d.get("name")
            if sym and name:
                # key by slug ("J&KBANK" -> "jkbank") to match dataset symbols
                names[review_slug(sym)] = name
        except Exception:
            continue
    return names


def load_scores():
    with open(RESULTS) as f:
        d = json.load(f)
    out = {}
    for r in d["results"]:
        out[r["symbol"]] = {
            "composite": r.get("composite"),
            "tier": r.get("tier"),
            "sector": r.get("sector"),
        }
    return out


def load_credibility():
    try:
        import scorer as cred_scorer
    except Exception:
        cred_scorer = None
    out = {}
    if not os.path.isdir(AUDITS_DIR):
        return out
    for fn in os.listdir(AUDITS_DIR):
        if not fn.endswith(".json"):
            continue
        slug = fn[:-5]
        try:
            with open(os.path.join(AUDITS_DIR, fn)) as f:
                d = json.load(f)
            if cred_scorer:
                r = cred_scorer.score_credibility(d)
                out[slug] = {
                    "score": r.get("credibility_score"),
                    "c5": r.get("c5"),
                    "calls": r.get("scored_calls"),
                }
            else:
                out[slug] = {"score": None, "c5": None, "calls": 0}
        except Exception:
            continue
    return out


def load_pledge():
    p = pd.read_parquet(PLEDGE)
    latest = p.sort_values("quarter_end").groupby("symbol").tail(1)
    return {
        r["symbol"]: {"pledge_pct": float(r["pledge_pct"]), "quarter": r["quarter_label"]}
        for _, r in latest.iterrows()
    }


def load_spark(symbol, n=60):
    path = os.path.join(PRICES_DIR, f"{symbol}_NS.parquet")
    if not os.path.exists(path):
        return None
    try:
        df = pd.read_parquet(path, columns=["Close"])
        closes = [round(float(x), 2) for x in df["Close"].dropna().tail(n).tolist()]
        return closes if len(closes) >= 2 else None
    except Exception:
        return None


def main():
    nh = pd.read_parquet(NAMED_HOLDERS)
    review_names = load_review_names()
    scores = load_scores()
    cred = load_credibility()
    pledge = load_pledge()

    with open(ACTIVITY) as f:
        activity = json.load(f)
    moves_by_investor = {}
    for inv in activity.get("investors", []):
        moves_by_investor[inv["name"]] = inv.get("activity", [])

    # symbol -> set of investor ids (for overlap)
    held_by = {}
    investors_out = []

    for inv in INVESTORS:
        m = nh[nh["holder_name"].str.contains(inv["pattern"], case=False, na=False)].copy()
        m = m.sort_values("holding_pct", ascending=False)
        holdings = []
        for _, r in m.iterrows():
            sym = r["symbol"]
            slug = review_slug(sym)
            sc = scores.get(slug, {})
            cr = cred.get(slug)
            pl = pledge.get(sym, {})
            name = review_names.get(slug) or NAME_FALLBACK.get(sym) or sym.title()
            holdings.append(
                {
                    "symbol": sym,
                    "slug": slug,
                    "name": name,
                    "holding_pct": round(float(r["holding_pct"]), 2),
                    "holder_label": r["holder_name"],
                    "in_review": slug in scores,
                    "composite": sc.get("composite"),
                    "tier": sc.get("tier"),
                    "sector": sc.get("sector"),
                    "credibility": cr.get("score") if cr else None,
                    "credibility_c5": cr.get("c5") if cr else None,
                    "pledge_pct": pl.get("pledge_pct"),
                    "pledge_quarter": pl.get("quarter"),
                    "spark": load_spark(sym),
                }
            )
            held_by.setdefault(sym, set()).add(inv["id"])

        investors_out.append(
            {
                "id": inv["id"],
                "name": inv["name"],
                "type": inv["type"],
                "note": inv["note"],
                "positions": len(holdings),
                "in_review_count": sum(1 for h in holdings if h["in_review"]),
                "top_holding": holdings[0]["symbol"] if holdings else None,
                "holdings": holdings,
                "moves": moves_by_investor.get(inv["name"], []),
            }
        )

    overlap = []
    for sym, inv_ids in held_by.items():
        if len(inv_ids) >= 2:
            slug = review_slug(sym)
            sc = scores.get(slug, {})
            overlap.append(
                {
                    "symbol": sym,
                    "slug": slug,
                    "name": review_names.get(slug) or NAME_FALLBACK.get(sym) or sym.title(),
                    "investors": sorted(inv_ids),
                    "in_review": slug in scores,
                    "composite": sc.get("composite"),
                }
            )
    overlap.sort(key=lambda o: (o["composite"] is None, -(o["composite"] or 0)))

    # name lookup for investor ids in overlap rendering
    id_to_name = {inv["id"]: inv["name"] for inv in investors_out}

    out = {
        "updated_at": date.today().isoformat(),
        "as_of": "Jun-2026 SHP filings",
        "investor_names": id_to_name,
        "investors": investors_out,
        "overlap": overlap,
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    total_holdings = sum(len(i["holdings"]) for i in investors_out)
    print(f"wrote {OUT}: {len(investors_out)} investors, {total_holdings} holdings, {len(overlap)} overlaps")


if __name__ == "__main__":
    main()
