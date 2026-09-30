#!/usr/bin/env python3
"""Disjointness check for the v4 OOS pre-registration R2 (V4_SPEC §8.3) -- VOID outcome version.

Pure name/date-membership check: no price/EPS/fundamental data is touched. The prior membership
lists are IMPORTED, never retyped (validation/v3_11_oos/check_disjoint_v311.py, which imports
INSAMPLE, V3_8, V3_9, V3_10 from validation/v3_10_oos/check_disjoint_v310.py): FIVE prior sets,
77 companies / 150 name-dates. No v4 set was ever frozen, so §9's "six priors" does not apply.

STATUS: R2 Gate 1 FAILED (see V4_OOS_PREREG_R2.md) -> VOID; no v4 set is frozen, V4 below is
intentionally empty and the §8.3 25/13 shape assertion is reported as not applicable. What this
script verifies is that every R2 Gate-1 candidate name-date (fill_plausibility_results_r2.json:
9 companies x 2019..2022-03-31) is disjoint from all five prior sets at company AND name-date
level, so no candidate was ineligible on overlap grounds. A future pre-reg re-runs the full
§8.3 procedure on its own frozen set.

Company identity: co() convention (name-date token up to the last underscore), lower-cased
screener symbol. Renamed/demerged-ticker mapping checked against prior company tokens (by eye, in
the pre-reg doc): none of simplexinf / fel / fconsumer / flfl / omaxe / mep / adaniports / fsc / pfs
maps to a prior token (the prior set carries `fretail` = Future Retail, a distinct listed legal
entity from FEL, FCONSUMER, FLFL and FSC).
"""
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v3_11_oos"))
sys.path.insert(0, os.path.join(HERE, "..", "v3_10_oos"))
from check_disjoint_v311 import INSAMPLE, V3_8, V3_9, V3_10, V3_11, co  # noqa: E402

V4 = []  # no frozen v4 set: VOID per V4_SPEC §8.2 / Gate 1 of the R2 task


def candidates():
    rows = json.load(open(os.path.join(HERE, "fill_plausibility_results_r2.json")))
    return sorted({r["name_date"].replace("&", "and") for r in rows})


def main():
    assert V4 == []
    assert len(co(INSAMPLE)) == 25 and len(INSAMPLE) == 50
    for s in (V3_8, V3_9, V3_10, V3_11):
        assert len(co(s)) == 13 and len(s) == 25
    priors = (("in-sample", INSAMPLE), ("v3.8", V3_8), ("v3.9", V3_9), ("v3.10", V3_10), ("v3.11", V3_11))
    cand = candidates()
    assert len(cand) == len(set(cand))
    assert min(n.rsplit("_", 1)[1] for n in cand) >= "2019-03-31"
    print("v4 frozen set: NONE (R2 Gate 1 failed -> VOID; s8.3 25/13 shape assertion not applicable)")
    print(f"R2 candidates examined: {len(co(cand))} companies / {len(cand)} name-dates; "
          f"scoring dates {min(n.rsplit('_',1)[1] for n in cand)} .. {max(n.rsplit('_',1)[1] for n in cand)}")
    print(f"candidate companies: {sorted(co(cand))}")
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
