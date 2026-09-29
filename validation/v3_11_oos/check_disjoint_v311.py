#!/usr/bin/env python3
"""Disjointness check for the v3.11 OOS pre-registration set.

Pure name/date-membership check -- no price/EPS/fundamental data is touched, no
valuation or backtest is run. Checks the 25 v3.11 name-dates (13 companies)
against ALL FOUR prior sets: in-sample 25 companies (50 name-dates), v3.8 OOS
(13 / 25), v3.9 OOS (13 / 25), v3.10 OOS (13 / 25). The prior membership lists
are imported from validation/v3_10_oos/check_disjoint_v310.py (which carries the
in-sample, v3.8, v3.9 and v3.10 lists verbatim) so they are not retyped.
Overlap is tested at company level (strict) and name-date level.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "v3_10_oos"))
from check_disjoint_v310 import INSAMPLE, V3_8, V3_9, V3_10, co  # noqa: E402

V3_11 = """tvsmotor_2019-03-31 tvsmotor_2020-03-31 jublfood_2019-03-31 jublfood_2020-03-31
tiindia_2020-03-31 tiindia_2021-03-31 kei_2019-03-31 kei_2020-03-31
pidilite_2019-03-31 pidilite_2021-03-31
emami_2019-03-31 emami_2020-03-31 marico_2019-03-31 marico_2021-03-31
ongc_2019-03-31 ongc_2021-03-31 sunpharma_2019-03-31 sunpharma_2020-03-31
nhpc_2019-03-31 nhpc_2021-03-31
gayatri_2019-03-31 gayatri_2020-03-31 sadbhav_2020-03-31 sadbhav_2021-03-31
srei_2020-03-31""".split()


def main():
    assert len(V3_11) == len(set(V3_11)) == 25
    assert len(co(V3_11)) == 13
    assert len(co(INSAMPLE)) == 25 and len(INSAMPLE) == 50
    for s in (V3_8, V3_9, V3_10):
        assert len(co(s)) == 13 and len(s) == 25
    assert all(n.rsplit("_", 1)[1] >= "2019-03-31" for n in V3_11)
    for label, prior in (("in-sample", INSAMPLE), ("v3.8", V3_8), ("v3.9", V3_9), ("v3.10", V3_10)):
        print(f"prior {label}: {len(co(prior))} companies / {len(prior)} name-dates")
        print(f"  company overlap:   {sorted(co(V3_11) & co(prior))}")
        print(f"  name-date overlap: {sorted(set(V3_11) & set(prior))}")
    allc = co(INSAMPLE) | co(V3_8) | co(V3_9) | co(V3_10)
    allnd = set(INSAMPLE) | set(V3_8) | set(V3_9) | set(V3_10)
    print(f"union of prior sets: {len(allc)} companies / {len(allnd)} name-dates")
    print(f"union company overlap:   {sorted(co(V3_11) & allc)}")
    print(f"union name-date overlap: {sorted(set(V3_11) & allnd)}")
    print(f"v3.11: {len(co(V3_11))} companies / {len(V3_11)} name-dates; min scoring date {min(n.rsplit('_',1)[1] for n in V3_11)}")
    print(f"DISJOINT: {not (co(V3_11) & allc) and not (set(V3_11) & allnd)}")


if __name__ == "__main__":
    main()
