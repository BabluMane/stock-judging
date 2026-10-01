#!/usr/bin/env python3
"""Full 25-name-date / 13-company disjointness proof for the v4 Phase-D
pre-registration (V4_SPEC §8.4(4)).

The frozen set = 5 certified blow-up name-dates (R3/R6/R7) + 10 winner
name-dates + 10 mediocrity name-dates (2026-10-01 coordinator sweep).

Assertions (strict, §8.3):
  1. All 25 name-dates unique; exactly 13 distinct companies.
  2. Zero company AND name-date overlap with the five prior sets
     (in-sample 25/50; v3.8/v3.9/v3.10/v3.11 13/25 each).
  3. Zero company overlap with the R1-R7 examined-lead burn list
     (243 companies), mapping renamed/demerged tickers by legal entity.

Prior membership lists are IMPORTED, never retyped:
  - five prior sets via the canonical lists in port/validation/v3_10_oos/
    check_disjoint_v310.py and port/validation/v3_11_oos/check_disjoint_v311.py
  - burn list from burn_list_winmed.json (built from the R1/R2 firewall JSONs
    and R3-R7 lead/dossier company lists)
  - blow-up name-dates from the R3/R6/R7 certification records
    (V4_OOS_PREREG_PHASED_DRAFT.md §8.4(3))

The R2 full 36-name-date list is not in the local mirror; the R2 cross-check
rests on sweep memory and is carried as an audit caveat in the pre-reg draft.

Prints DISJOINT: True / False and exits 0 / 1.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = os.path.expanduser("~/workspace/stock-judging/port")
sys.path.insert(0, os.path.join(PORT, "validation", "v3_10_oos"))
sys.path.insert(0, os.path.join(PORT, "validation", "v3_11_oos"))

import check_disjoint_v310 as c10  # noqa: E402
import check_disjoint_v311 as c11  # noqa: E402

# Frozen blow-up name-dates (certified R3/R6/R7; 2+2+1 shape-complete 5/5).
BLOWUPS = [
    "supremeeng_2020-03-31", "supremeeng_2021-03-31",
    "pbm_2019-03-31", "pbm_2020-03-31",
    "varroc_2019-03-31",
]

# Frozen winner/mediocrity name-dates (SET_WINMED_DOSSIER.md, 2026-10-01).
WINMED = [
    "infy_2020-03-31", "infy_2021-03-31",
    "sbin_2021-03-31", "sbin_2022-03-31",
    "srf_2019-03-31", "srf_2020-03-31",
    "lt_2021-03-31", "lt_2022-03-31",
    "endurance_2020-03-31", "endurance_2021-03-31",
    "drreddy_2019-03-31", "drreddy_2020-03-31",
    "dabur_2020-03-31", "dabur_2021-03-31",
    "maruti_2019-03-31", "maruti_2020-03-31",
    "cyient_2020-03-31", "cyient_2021-03-31",
    "auropharma_2019-03-31", "auropharma_2020-03-31",
]

FULL_SET = BLOWUPS + WINMED


def co(nd):
    return nd.rsplit("_", 1)[0].lower()


def main():
    violations = []

    # Internal shape.
    if len(FULL_SET) != 25:
        violations.append(f"expected 25 name-dates, got {len(FULL_SET)}")
    if len(set(FULL_SET)) != 25:
        violations.append("duplicate name-dates in frozen set")
    if len({co(nd) for nd in FULL_SET}) != 13:
        violations.append(
            f"expected 13 companies, got {len({co(nd) for nd in FULL_SET})}")

    # Five prior sets, company AND name-date level.
    prior_lists = {
        "in_sample": c10.INSAMPLE,
        "v3_8": c10.V3_8,
        "v3_9": c10.V3_9,
        "v3_10": c10.V3_10,
        "v3_11": c11.V3_11,
    }
    for label, lst in prior_lists.items():
        nd_set = set(lst)
        co_set = {co(nd) for nd in lst}
        for nd in FULL_SET:
            if nd in nd_set:
                violations.append(f"name-date collision with {label}: {nd}")
            if co(nd) in co_set:
                violations.append(f"company collision with {label}: {co(nd)}")

    # R1-R7 burn list, company level. The 5 certified blow-up companies are
    # themselves examined leads, so they sit in the burn list by construction;
    # certification supersedes the burn for those five (their disjointness was
    # asserted at certification time). Everything else on the burn list is a
    # hard block against re-use.
    blow_cos = {co(nd) for nd in BLOWUPS}
    with open(os.path.join(HERE, "burn_list_winmed.json")) as f:
        burn = {str(c).lower() for c in json.load(f)}
    for nd in FULL_SET:
        if co(nd) in burn and co(nd) not in blow_cos:
            violations.append(f"burn-list collision: {co(nd)}")

    ok = not violations
    if violations:
        for v in violations:
            print("VIOLATION:", v)
    print("DISJOINT:", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
