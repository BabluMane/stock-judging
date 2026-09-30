#!/usr/bin/env python3
"""Disjointness check for the v4 OOS pre-registration (V4_SPEC §8.3) -- VOID outcome version.

Pure name/date-membership check: no price/EPS/fundamental data is touched, no valuation or
backtest is run. The prior membership lists are IMPORTED, never retyped:
  validation/v3_11_oos/check_disjoint_v311.py  (V3_11; it in turn imports INSAMPLE, V3_8, V3_9, V3_10
  from validation/v3_10_oos/check_disjoint_v310.py). Five prior sets: in-sample 25 companies / 50
  name-dates; v3.8, v3.9, v3.10, v3.11 OOS 13 / 25 each = 77 companies.

STATUS: the v4 OOS set is VOID at pre-registration (§8.2: fewer than 5 blow-up name-dates could be
certified), so NO v4 set is frozen and V4 below is intentionally empty. The §8.3 shape assertions
(25 name-dates / 13 companies) therefore do not apply and are NOT made. What this script verifies
instead is that every candidate examined in V4_OOS_PREREG.md (the 171 name-dates in
fill_plausibility_results.json) is disjoint from all five prior sets at company AND name-date
level, so that none of them was ineligible on overlap grounds. A future pre-reg must re-run the
full §8.3 procedure on its own frozen set and on six prior sets.

Company identity: the co() convention (name-date token up to the last underscore), lower-cased
screener symbol with '&' spelled 'and'. No renamed/demerged ticker maps to a prior company among the
candidates (checked by eye in the pre-reg: e.g. Dhani Services = ex-Indiabulls Ventures, Reliance
Home Finance and Reliance Infra/Power are distinct legal entities from relcapital, FLFL is distinct
from fretail).
"""
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v3_11_oos"))
sys.path.insert(0, os.path.join(HERE, "..", "v3_10_oos"))
from check_disjoint_v311 import INSAMPLE, V3_8, V3_9, V3_10, V3_11, co  # noqa: E402

V4 = []  # no frozen v4 set: VOID per V4_SPEC §8.2 (see V4_OOS_PREREG.md)


def candidates():
    rows = json.load(open(os.path.join(HERE, "fill_plausibility_results.json")))
    return sorted({r["name_date"].replace("&", "and") for r in rows})


def main():
    assert V4 == []
    assert len(co(INSAMPLE)) == 25 and len(INSAMPLE) == 50
    for s in (V3_8, V3_9, V3_10, V3_11):
        assert len(co(s)) == 13 and len(s) == 25
    priors = (("in-sample", INSAMPLE), ("v3.8", V3_8), ("v3.9", V3_9), ("v3.10", V3_10), ("v3.11", V3_11))
    cand = candidates()
    assert len(cand) == len(set(cand))
    print("v4 frozen set: NONE (VOID per V4_SPEC s8.2; s8.3 25/13 shape assertion not applicable)")
    print(f"candidates examined: {len(co(cand))} companies / {len(cand)} name-dates; "
          f"scoring dates {min(n.rsplit('_',1)[1] for n in cand)} .. {max(n.rsplit('_',1)[1] for n in cand)}")
    for label, prior in priors:
        print(f"prior {label}: {len(co(prior))} companies / {len(prior)} name-dates")
        print(f"  company overlap:   {sorted(co(cand) & co(prior))}")
        print(f"  name-date overlap: {sorted(set(cand) & set(prior))}")
    allc = set().union(*(co(p) for _, p in priors))
    allnd = set().union(*(set(p) for _, p in priors))
    print(f"union of prior sets: {len(allc)} companies / {len(allnd)} name-dates")
    print(f"union company overlap:   {sorted(co(cand) & allc)}")
    print(f"union name-date overlap: {sorted(set(cand) & allnd)}")
    print(f"DISJOINT: {not (co(cand) & allc) and not (set(cand) & allnd)}")


if __name__ == "__main__":
    main()
