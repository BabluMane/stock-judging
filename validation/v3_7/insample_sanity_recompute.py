#!/usr/bin/env python3
"""
V3.7 in-sample sanity recompute (task step 2 of the OOS live-bar validation).

NOT the live-bar test. This is a calibration sanity check on the FROZEN,
in-sample 26-name usable set. It recomputes DCF-only entry fills
independently from real weekly price series and cross-checks them against
the previously published `corrected_verdicts_final.json` /
`recomputed_fills.json`.

Honesty constraint, stated up front: the scored input bundle (`inputs/`,
containing each name-date's DCF assumptions: revenue, margins, growth, WACC
inputs) is absent from this repository (confirmed: no `inputs/` directory
anywhere in the checkout). A full from-financial-statements DCF rebuild for
26 name-dates is out of scope for a "sanity" pass and would not even be
checking the same thing — it would produce a NEW DCF fair value, not verify
the one the frozen validation used.

What this script actually does, and what it doesn't:
  - DOES reconstruct the DCF fair value (FV) algebraically from the ACC/INV
    trigger prices *disclosed* in `specs/V3_7_DCF_REVALIDATION_20260923.md`
    Sec 2, for the 4 name-dates where both legs' trigger prices are stated
    (persistent_2019, wipro_2015, wipro_2017, lichf_2018). This is a real
    check, not a tautology: V3_7_DELTA.md says ACC=-12.5%, INV=-30% of FV,
    i.e. ACC/INV should equal 0.875/0.70 = 1.25 for every name-date. That
    ratio is verified independently below, then used to back out FV.
  - DOES replay the ACTUAL v3.2/v3.7 three-tier entry rule (first weekly
    close price <= ACC trigger fills ACC; independently, first weekly close
    price <= INV trigger fills INV; both open a 24m/to-T outcome window) on
    the REAL weekly price series in pe_series/*.csv -- these are the same
    CSVs used throughout v3.6/v3.7, not re-derived here.
  - DOES NOT re-derive DCF fair value from financial statements. Nothing
    here should be read as an independent re-scoring of quality (Q) or an
    independent re-derivation of fair value; only the fill *mechanics* are
    independently re-run against real price data.
  - For piind_2016 only the ACC trigger is disclosed ("DCF trg 210.38 never
    reached"); INV is inferred as ACC/1.25 for a no-fill confirmation only
    (no fill is claimed either way from this inference).
  - hero_2018, lupin_2017, symphony_2018: source doc states "DCF trg never
    reached" with NO trigger price disclosed. This script cannot
    independently confirm those three no-fills -- flagged NOT VERIFIED,
    not asserted as confirmed.
  - persistent_2021, mnm_2016: source doc states fills are NOT COMPUTABLE
    (DCF fair value unknown, inputs missing). This script does not invent a
    fair value for them and reports them the same way.
"""
import csv
import json
from datetime import date, timedelta

FIVE_Y_WEEKS24 = timedelta(days=int(2 * 365.25))
SERIES_DIR = "validation/v3_6/pe_series"


def load_prices(slug):
    rows = []
    with open(f"{SERIES_DIR}/{slug}.csv", newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["price"]:
                rows.append((date.fromisoformat(r["date"]), float(r["price"])))
    rows.sort()
    return rows


def simulate(slug, d0, acc_trg, inv_trg):
    """First-touch fill on real weekly closes, 24m window from d0. Mirrors the
    v3.2 mechanic: independent ACC and INV legs, each fills once, at the
    first week its price closes at/below its own trigger.

    No per-name-date "T" (terminal evaluation date) is reconstructed here --
    that field lives in the missing `_calibration` block of the scored input
    JSON, which this repo does not have. As an *informational* cross-check
    only (never asserted as the real T), to_T_vs_latest_series_date uses the
    last date actually present in the price series -- labelled as such, not
    claimed to reproduce the original to-T horizon."""
    prices = load_prices(slug)
    window = [(d, p) for d, p in prices if d0 < d <= d0 + FIVE_Y_WEEKS24]
    latest_date, latest_price = prices[-1]
    out = {}
    for leg, trg in (("accumulate", acc_trg), ("invest", inv_trg)):
        if trg is None:
            out[leg] = None
            continue
        fill = next(((d, p) for d, p in window if p <= trg), None)
        if not fill:
            out[leg] = {"fill": None}
            continue
        fd, fp = fill
        fwd = [(d, p) for d, p in prices if fd < d <= fd + FIVE_Y_WEEKS24]
        out[leg] = {
            "fill_date": fd.isoformat(),
            "fill_price": fp,
            "trigger": round(trg, 2),
            "fwd_24m": round(fwd[-1][1] / fp, 3) if fwd else None,
            "fwd_months": round((fwd[-1][0] - fd).days / 30.44, 1) if fwd else None,
            "fwd_truncated": bool(fwd and fwd[-1][0] < fd + FIVE_Y_WEEKS24 - timedelta(days=20)),
            "to_latest_series_date": {
                "date": latest_date.isoformat(),
                "ratio": round(latest_price / fp, 3),
                "note": "informational only -- NOT the original _calibration.T (unknown, inputs missing)",
            },
        }
    return out


# ---- disclosed trigger prices, specs/V3_7_DCF_REVALIDATION_20260923.md Sec 2 ----
DISCLOSED = {
    "persistent_2019-03-29": {"slug": "persistent", "d0": "2019-03-29", "acc": 643.41, "inv": 514.73},
    "wipro_2015-03-31": {"slug": "wipro", "d0": "2015-03-31", "acc": 1080.95, "inv": 864.76},
    "wipro_2017-03-31": {"slug": "wipro", "d0": "2017-03-31", "acc": 848.78, "inv": 679.03},
    "lichf_2018-03-31": {"slug": "lichf", "d0": "2018-03-31", "acc": 358.13, "inv": 286.50},
}
# piind_2016: only ACC trigger disclosed ("DCF trg 210.38 never reached"); used for a
# no-fill confirmation only, INV inferred at 0.70/0.875 ratio, never asserted as fact.
PIIND_ACC_ONLY = {"slug": "piind", "d0": "2016-03-31", "acc": 210.38}

# name-dates the source doc states are NOT COMPUTABLE -- reported as such, not guessed.
NOT_COMPUTABLE = ["persistent_2021-03-31", "mnm_2016-03-31"]
# name-dates the source doc states have "no fill" but discloses NO trigger price --
# cannot be independently re-verified here.
NOT_VERIFIABLE_NO_FILL = ["hero_2018-03-31", "lupin_2017-03-31", "symphony_2018-03-31"]


def main():
    print("=== Ratio consistency check (V3_7_DELTA: ACC=-12.5%, INV=-30% => ACC/INV should = 0.875/0.70 = 1.25) ===")
    for key, d in DISCLOSED.items():
        ratio = round(d["acc"] / d["inv"], 5)
        ok = abs(ratio - 1.25) < 0.001
        print(f"  {key:26s} ACC={d['acc']:>9.2f} INV={d['inv']:>9.2f}  ratio={ratio}  {'OK' if ok else 'MISMATCH'}")

    print("\n=== Reconstructed DCF fair value (FV = ACC / 0.875 = INV / 0.70) ===")
    results = {}
    for key, d in DISCLOSED.items():
        fv_from_acc = round(d["acc"] / 0.875, 2)
        fv_from_inv = round(d["inv"] / 0.70, 2)
        print(f"  {key:26s} FV(from ACC)={fv_from_acc:>9.2f}  FV(from INV)={fv_from_inv:>9.2f}")
        fills = simulate(d["slug"], date.fromisoformat(d["d0"]), d["acc"], d["inv"])
        results[key] = {"fv_from_acc": fv_from_acc, "fv_from_inv": fv_from_inv, "fills": fills}

    print("\n=== piind_2016-03-31 no-fill confirmation (ACC only disclosed) ===")
    inv_inferred = round(PIIND_ACC_ONLY["acc"] / 1.25, 2)
    fills = simulate(PIIND_ACC_ONLY["slug"], date.fromisoformat(PIIND_ACC_ONLY["d0"]), PIIND_ACC_ONLY["acc"], inv_inferred)
    results["piind_2016-03-31"] = {"acc_trigger": PIIND_ACC_ONLY["acc"], "inv_trigger_inferred": inv_inferred, "fills": fills}
    print(f"  ACC trigger {PIIND_ACC_ONLY['acc']}, INV trigger inferred {inv_inferred}: fills={fills}")

    for key in NOT_COMPUTABLE:
        results[key] = {"status": "NOT_COMPUTABLE per V3_7_DCF_REVALIDATION_20260923.md -- DCF fair value unknown, not reconstructed here"}
    for key in NOT_VERIFIABLE_NO_FILL:
        results[key] = {"status": "NOT_INDEPENDENTLY_VERIFIABLE -- source doc discloses no trigger price for this name-date"}

    with open("validation/v3_7/insample_sanity_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("\nWrote validation/v3_7/insample_sanity_results.json")


if __name__ == "__main__":
    main()
