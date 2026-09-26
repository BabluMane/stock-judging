#!/usr/bin/env python3
"""Disjointness check for the v3.9 OOS pre-registration set.

Checks the 13 new companies against (a) the 25-company in-sample frozen set
(engine/standard_v3_scoring_spec.md §12, restated in
validation/v3_8_oos/OOS_SET_PREREG.md) and (b) the 13-company v3.8 OOS set
(validation/v3_8_oos/OOS_SET_PREREG.md). Pure name-membership check — no
price/EPS/fundamental data is touched, no validation or backtest is run.
"""

INSAMPLE_25 = {
    "aplapollo", "astral", "bajajcon", "bajfin", "bhel", "brightcom",
    "deepak", "dhfl", "hero", "itc", "lichf", "lupin", "manpasand", "mnm",
    "navin", "persistent", "piind", "safari", "suntv", "symphony",
    "tataelxsi", "trent", "vakrangee", "wipro", "yesbank",
}

V3_8_OOS_13 = {
    "titan", "divislab", "pageind", "dmart", "polycab", "colpal",
    "ashokley", "cipla", "coalindia", "gail", "pcjeweller", "fretail",
    "cgpower",
}

V3_9_OOS_13 = {
    # winners
    "asianpaint", "hdfcbank", "nestleind", "britannia", "havells",
    # mediocrities
    "bhartiartl", "tatasteel", "ntpc", "tatamotors", "bankbaroda",
    # blow-ups
    "zeel", "relcapital", "ilfstransport",
}

def main():
    assert len(INSAMPLE_25) == 25, len(INSAMPLE_25)
    assert len(V3_8_OOS_13) == 13, len(V3_8_OOS_13)
    assert len(V3_9_OOS_13) == 13, len(V3_9_OOS_13)

    overlap_insample = sorted(V3_9_OOS_13 & INSAMPLE_25)
    overlap_v38 = sorted(V3_9_OOS_13 & V3_8_OOS_13)
    overlap_all = sorted((INSAMPLE_25 | V3_8_OOS_13) & V3_9_OOS_13)

    print(f"in-sample frozen set size: {len(INSAMPLE_25)}")
    print(f"v3.8 OOS set size: {len(V3_8_OOS_13)}")
    print(f"v3.9 OOS candidate set size: {len(V3_9_OOS_13)}")
    print(f"overlap(v3.9, in-sample-25): {overlap_insample}")
    print(f"overlap(v3.9, v3.8-OOS-13): {overlap_v38}")
    print(f"overlap(v3.9, union): {overlap_all}")
    print(f"DISJOINT: {len(overlap_all) == 0}")

if __name__ == "__main__":
    main()
